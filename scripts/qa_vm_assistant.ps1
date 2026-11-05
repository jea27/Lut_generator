param(
 [Parameter(Mandatory=$true)][string]$KitZip,
 [Parameter(Mandatory=$true)][ValidatePattern('^[a-f0-9]{64}$')][string]$ExpectedSha256,
 [guid]$CheckpointId=[guid]::Empty,
 [switch]$ConfirmCleanCheckpoint,
 [switch]$Run
)
# Read-only by default. -Run transfers only the verified kit and invokes its
# guest-only cycle. No VM start/restore, feature enable, share, permission or UAC.
$ErrorActionPreference='Stop'
$lfRoot=[IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
$lfPrivate=Join-Path $lfRoot '.lumaforge-local'
$lfZip=[IO.Path]::GetFullPath((Resolve-Path -LiteralPath $KitZip).Path)
function Test-LfUnlinked([string]$lfPath){
 $lfWalk=$lfPath
 while($lfWalk){
  if((Test-Path -LiteralPath $lfWalk) -and ((Get-Item -LiteralPath $lfWalk -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Linked handoff path rejected'}
  $lfNext=Split-Path -Parent $lfWalk;if($lfNext -eq $lfWalk){break};$lfWalk=$lfNext
 }
}
if(-not $lfZip.StartsWith($lfPrivate+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Use a private kit inside this workspace'}
Test-LfUnlinked $lfZip
if((Get-FileHash -LiteralPath $lfZip).Hash.ToLower() -ne $ExpectedSha256){throw 'Kit ZIP hash mismatch'}
if(-not(Get-Command Get-VM -ErrorAction SilentlyContinue)){throw 'Hyper-V cmdlets unavailable; no tool installation attempted'}
try{$lfVm=Get-VM -Name 'ColorStudio-QA-Win11' -ErrorAction Stop}catch{throw 'Cannot read the named VM. Run this script yourself in an elevated host PowerShell; no permissions will be changed'}
if(@($lfVm).Count -ne 1){throw 'VM selection must be unique'}
$lfCheckpoints=@(Get-VMSnapshot -VM $lfVm -ErrorAction Stop)
if($lfCheckpoints.Count -eq 0){throw 'No existing checkpoint; operator must prepare one. This script never creates or restores it'}
if($CheckpointId -eq [guid]::Empty){
 $lfCheckpoints|Select-Object Id,Name,CreationTime|Format-Table|Out-Host
 if(-not $Run){Write-Output 'Read-only inventory complete. Choose the clean checkpoint ID; no guest code executed.';return}
 $CheckpointId=[guid](Read-Host 'Paste the ID of the existing clean checkpoint; it will NOT be restored')
}
$lfSelected=@($lfCheckpoints|Where-Object {$_.Id -eq $CheckpointId})
if($lfSelected.Count -ne 1){throw 'Selected checkpoint is not associated with this VM'}
if(-not $Run){Write-Output 'Named VM and checkpoint metadata verified. -Run additionally requires an explicit clean-state confirmation.';return}
if(-not $ConfirmCleanCheckpoint){throw 'Confirm the guest currently has the clean test state. Existence/name of a checkpoint does not prove its contents or current application'}
if($lfVm.State -ne 'Running'){throw 'Start the VM yourself after checking resources. This script does not start or restore it'}
$lfSettings=@(Get-CimInstance -Namespace root/virtualization/v2 -ClassName Msvm_VirtualSystemSettingData -Filter ("VirtualSystemIdentifier='"+$lfVm.Id.ToString()+"'")|Where-Object {$_.VirtualSystemType -eq 'Microsoft:Hyper-V:System:Realized'})
if($lfSettings.Count -ne 1){throw 'Cannot obtain an unambiguous current BIOS identity'}
$lfBios=[guid]$lfSettings[0].BIOSGUID
if($lfBios -eq [guid]::Empty){throw 'Missing VM BIOS identity; never substitute the host or VM name'}
$lfOutput=Join-Path $lfPrivate ('vm-assistant-'+[guid]::NewGuid().ToString('N'));Test-LfUnlinked $lfOutput
New-Item -ItemType Directory -Path $lfOutput|Out-Null
# Validate ZIP entries before extraction; no traversal, duplicate paths, ADS,
# links, oversized expansion or undeclared payloads are accepted.
Add-Type -AssemblyName System.IO.Compression.FileSystem
$lfArchive=[IO.Compression.ZipFile]::OpenRead($lfZip)
try{
 $lfNames=New-Object 'Collections.Generic.HashSet[string]' ([StringComparer]::OrdinalIgnoreCase);$lfBytes=[long]0
 foreach($lfEntry in $lfArchive.Entries){
  if([string]::IsNullOrEmpty($lfEntry.Name) -or [IO.Path]::IsPathRooted($lfEntry.FullName) -or $lfEntry.FullName -match '(^|[\\/])\.\.([\\/]|$)|:|\\' -or -not $lfNames.Add($lfEntry.FullName) -or (($lfEntry.ExternalAttributes -shr 16) -band 0xF000) -eq 0xA000){throw 'Unsafe or duplicate ZIP member'}
  $lfBytes+=$lfEntry.Length;if($lfBytes -gt 300MB){throw 'QA kit exceeds the expansion budget'}
 }
}finally{$lfArchive.Dispose()}
$lfExtract=Join-Path $lfOutput 'verified-kit';Expand-Archive -LiteralPath $lfZip -DestinationPath $lfExtract
$lfManifest=Get-Content -LiteralPath "$lfExtract\kit-manifest.json" -Raw|ConvertFrom-Json
if($lfManifest.schema -ne 'color-studio-private-vm-kit-v2'){throw 'Use the cycle-enabled v2 kit'}
if($lfNames.Count -ne @($lfManifest.files.psobject.Properties).Count+1){throw 'ZIP has undeclared files'}
foreach($lfFile in $lfManifest.files.psobject.Properties){
 if(-not $lfNames.Contains($lfFile.Name) -or (Get-FileHash -LiteralPath (Join-Path $lfExtract $lfFile.Name)).Hash.ToLower() -ne $lfFile.Value){throw 'Kit file mismatch'}
}
$lfManifestHash=(Get-FileHash -LiteralPath "$lfExtract\kit-manifest.json").Hash.ToLower()
$lfAttestation=[ordered]@{schema='color-studio-private-vm-attestation-v1';vm_name='ColorStudio-QA-Win11';vm_id=$lfVm.Id.ToString();bios_guid=$lfBios.ToString();checkpoint_id=$CheckpointId.ToString();checkpoint_created=$lfSelected[0].CreationTime.ToUniversalTime().ToString('o');operator_confirms_clean_checkpoint=$true;checkpoint_restored_by_assistant=$false;kit_sha256=$ExpectedSha256;kit_manifest_sha256=$lfManifestHash}
$lfAttestation|ConvertTo-Json|Set-Content -LiteralPath "$lfOutput\host-attestation.json" -Encoding UTF8
$lfSession=$null
try{
 # Credentials are entered only in the operator's local prompt and held in
 # memory. No WinRM/network/share/service setting or saved credential is used.
 $lfCredential=Get-Credential -Message 'Administrator account INSIDE ColorStudio-QA-Win11; never paste credentials into chat/GitHub'
 if(-not $lfCredential){throw 'Guest credentials not provided'}
 $lfSession=New-PSSession -VMId $lfVm.Id -Credential $lfCredential -ErrorAction Stop
 $lfCredential=$null
 $lfGuest=Invoke-Command -Session $lfSession -ScriptBlock {
  $m=Get-CimInstance Win32_ComputerSystem;$o=Get-CimInstance Win32_OperatingSystem
  @{uuid=(Get-CimInstance Win32_ComputerSystemProduct).UUID;manufacturer=$m.Manufacturer;model=$m.Model;product_type=$o.ProductType;build=$o.BuildNumber;root_exists=(Test-Path -LiteralPath 'C:\LF-QA')}
 }
 if([guid]$lfGuest.uuid -ne $lfBios -or $lfGuest.manufacturer -ne 'Microsoft Corporation' -or $lfGuest.model -ne 'Virtual Machine' -or $lfGuest.product_type -ne 1 -or [int]$lfGuest.build -lt 22000){throw 'Guest identity mismatch; no files copied'}
 if($lfGuest.root_exists){throw 'Existing guest QA workspace preserved. Select a fresh state manually; never overwrite or restore automatically'}
 Invoke-Command -Session $lfSession -ScriptBlock {New-Item -ItemType Directory -Path 'C:\LF-QA\Kit'|Out-Null}
 foreach($lfFile in Get-ChildItem -LiteralPath $lfExtract){Copy-Item -LiteralPath $lfFile.FullName -Destination 'C:\LF-QA\Kit' -ToSession $lfSession -Recurse}
 Copy-Item -LiteralPath "$lfOutput\host-attestation.json" -Destination 'C:\LF-QA\Kit\host-attestation.json' -ToSession $lfSession
 # The copied script is checked against the trusted ZIP before being executed.
 $lfCycleHash=$lfManifest.files.'qa_vm_cycle.ps1'
 Invoke-Command -Session $lfSession -ArgumentList $lfCycleHash,$lfManifestHash -ScriptBlock {
  param($cycleHash,$manifestHash)
  if((Get-FileHash -LiteralPath 'C:\LF-QA\Kit\qa_vm_cycle.ps1').Hash.ToLower() -ne $cycleHash){throw 'Guest cycle script changed'}
  & 'C:\LF-QA\Kit\qa_vm_cycle.ps1' -ExpectedManifestSha256 $manifestHash
 }
}finally{
 if($lfSession){
  try{Copy-Item -Path 'C:\LF-QA\Reports\*\report.json' -Destination $lfOutput -FromSession $lfSession -ErrorAction Stop}catch{Write-Output 'No completed guest report copied; retain guest logs and inspect privately'}
  Remove-PSSession -Session $lfSession
 }
}
Write-Output ('Private reports: '+$lfOutput)
Write-Output 'Automation results are separate from GUI, legal and human acceptance. External beta and sale remain NO-GO.'
