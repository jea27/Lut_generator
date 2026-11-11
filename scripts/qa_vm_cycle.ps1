param([Parameter(Mandatory=$true)][string]$ExpectedManifestSha256,[switch]$CleanCandidate)
$ErrorActionPreference='Stop'
function Test-LfColorStudioRegistration {
 foreach($lfHive in @([Microsoft.Win32.RegistryHive]::CurrentUser,[Microsoft.Win32.RegistryHive]::LocalMachine)){
  foreach($lfView in @([Microsoft.Win32.RegistryView]::Registry32,[Microsoft.Win32.RegistryView]::Registry64)){
   $lfBase=$null;$lfKey=$null
   try{
    $lfBase=[Microsoft.Win32.RegistryKey]::OpenBaseKey($lfHive,$lfView)
    $lfKey=$lfBase.OpenSubKey('Software\Microsoft\Windows\CurrentVersion\Uninstall\Color Studio Beta',$false)
    if($null -ne $lfKey){return $true}
   }finally{if($lfKey){$lfKey.Dispose()};if($lfBase){$lfBase.Dispose()}}
  }
 }
 return $false
}
function Assert-LfNoExistingColorStudio {
 $lfLocal=[Environment]::GetFolderPath('LocalApplicationData')
 if(-not $lfLocal){throw 'Cannot certify an empty guest profile; preserve existing state'}
 foreach($lfRelative in @('ColorStudioBetaData','Color Studio Beta','Programs\Color Studio Beta')){
  if(Test-Path -LiteralPath (Join-Path $lfLocal $lfRelative)){throw 'Existing Color Studio state preserved; operator must select a fresh guest checkpoint'}
 }
 if(Test-LfColorStudioRegistration){throw 'Existing registered Color Studio preserved; operator must select a fresh guest checkpoint'}
}
$lfKit=[IO.Path]::GetFullPath($PSScriptRoot)
if($lfKit -ne 'C:\LF-QA\Kit'){throw 'Requires the dedicated VM kit path'}
function Test-LfPath([string]$lfPath){
 $lfPath=[IO.Path]::GetFullPath($lfPath)
 if(-not $lfPath.StartsWith('C:\LF-QA\',[StringComparison]::OrdinalIgnoreCase)){throw 'Path outside synthetic guest workspace'}
 $lfWalk=$lfPath
 while($lfWalk){
  if((Test-Path -LiteralPath $lfWalk) -and ((Get-Item -LiteralPath $lfWalk -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Linked guest path rejected'}
  $lfNext=Split-Path -Parent $lfWalk;if($lfNext -eq $lfWalk){break};$lfWalk=$lfNext
 }
}
Test-LfPath $lfKit
if($ExpectedManifestSha256 -notmatch '^[a-f0-9]{64}$' -or (Get-FileHash -LiteralPath "$lfKit\kit-manifest.json").Hash.ToLower() -ne $ExpectedManifestSha256){throw 'Untrusted kit manifest'}
$lfManifest=Get-Content -LiteralPath "$lfKit\kit-manifest.json" -Raw|ConvertFrom-Json
if($lfManifest.schema -ne 'color-studio-private-vm-kit-v2'){throw 'Requires the cycle-enabled v2 kit'}
if($CleanCandidate -and $lfManifest.version -ne '0.3.0-beta.7'){throw 'This clean-candidate cycle is pinned to beta.7'}
foreach($lfFile in $lfManifest.files.psobject.Properties){
 if([IO.Path]::IsPathRooted($lfFile.Name) -or $lfFile.Name -match '(^|[\\/])\.\.([\\/]|$)|:'){throw 'Unsafe kit member'}
 $lfPath=Join-Path $lfKit $lfFile.Name;Test-LfPath $lfPath
 if((Get-FileHash -LiteralPath $lfPath).Hash.ToLower() -ne $lfFile.Value){throw 'Kit member changed'}
}
$lfAttestation=Get-Content -LiteralPath "$lfKit\host-attestation.json" -Raw|ConvertFrom-Json
$lfMachine=Get-CimInstance Win32_ComputerSystem;$lfOs=Get-CimInstance Win32_OperatingSystem
$lfUuid=[guid](Get-CimInstance Win32_ComputerSystemProduct).UUID
if($lfAttestation.schema -ne 'color-studio-private-vm-attestation-v1' -or $lfAttestation.vm_name -ne 'ColorStudio-QA-Win11' -or -not $lfAttestation.operator_confirms_clean_checkpoint -or $lfUuid -ne [guid]$lfAttestation.bios_guid -or $lfMachine.Manufacturer -ne 'Microsoft Corporation' -or $lfMachine.Model -ne 'Virtual Machine' -or $lfOs.ProductType -ne 1 -or [int]$lfOs.BuildNumber -lt 22000){throw 'Guest identity or selected checkpoint attestation does not match'}
Assert-LfNoExistingColorStudio
if(Test-Path -LiteralPath 'C:\LF-QA\App'){throw 'Preserve existing installation. Operator must select a fresh test state; no automatic restore'}
if(Test-Path -LiteralPath 'C:\LF-QA\Data'){throw 'Existing data preserved. No automatic cleanup or overwrite'}
Test-LfPath 'C:\LF-QA\Reports';$lfRun='C:\LF-QA\Reports\'+[guid]::NewGuid().ToString('N')
New-Item -ItemType Directory -Path $lfRun|Out-Null
$lfSteps=[ordered]@{};foreach($lfId in @('guest_identity','previous_install','seed_api','failed_upgrade','upgrade','clean_candidate_install','candidate_api','restart_api','interruption_fixtures','offline_api','uninstall')){$lfSteps[$lfId]=[ordered]@{status='NOT_RUN'}}
$lfReport=[ordered]@{schema='color-studio-private-vm-cycle-v1';kit_version=$lfManifest.version;source=$lfManifest.source;installer_sha256=$lfManifest.installer_sha256;windows_build=$lfOs.BuildNumber;steps=$lfSteps;technical_automation_passed=$false;clean_windows_human_accepted=$false;gui_review='NOT_RUN';native_procmon_capture='NOT_RUN';external_editor_lut_import='NOT_RUN';human_accepted=$false;external_beta='NO-GO';commercial='NO-GO'}
$lfReport['cycle']=if($CleanCandidate){'clean_candidate'}else{'previous_to_candidate'}
$lfActive='guest_identity';$lfNetwork=@();$lfNetworkChanged=$false;$lfLock=[IntPtr]::Zero
$lfOldTemp=$env:TEMP;$lfOldTmp=$env:TMP;$lfOldVerified=$env:LF_QA_VM_VERIFIED
function Invoke-LfSetup([string]$lfName){
 $lfLogs=Join-Path $env:LOCALAPPDATA 'ColorStudioInstallerLogs'
 $lfBefore=@(Get-ChildItem -LiteralPath $lfLogs -File -ErrorAction SilentlyContinue|ForEach-Object {$_.FullName})
 $lfProcess=Start-Process -FilePath "$lfKit\$lfName" -ArgumentList @('/S','/D=C:\LF-QA\App') -WindowStyle Hidden -PassThru
 if(-not $lfProcess.WaitForExit(300000)){throw 'Owned setup timed out; preserve its process, logs and data for operator inspection'}
 $script:lfLastSetupEvents=@()
 foreach($lfLog in @(Get-ChildItem -LiteralPath $lfLogs -File -ErrorAction SilentlyContinue|Where-Object {$_.FullName -notin $lfBefore})){
  if($lfLog.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Linked installer log rejected'}
  Copy-Item -LiteralPath $lfLog.FullName -Destination (Join-Path $lfRun ('native-installer-'+[guid]::NewGuid().ToString('N')+'.log'))
  foreach($lfLine in Get-Content -LiteralPath $lfLog.FullName){try{$script:lfLastSetupEvents+=($lfLine|ConvertFrom-Json -ErrorAction Stop)}catch{}}
 }
 $lfProcess.Refresh()
 $lfReport['last_setup']=[ordered]@{file=$lfName;exit_code=$lfProcess.ExitCode}
 return $lfProcess.ExitCode
}
function Test-LfRuntime([bool]$lfPrevious){
 Test-LfPath 'C:\LF-QA\App'
 $lfLedgerHash=if($lfPrevious){$lfManifest.previous_installer_manifest_sha256}else{$lfManifest.installer_manifest_sha256}
 $lfRuntimeHash=if($lfPrevious){$lfManifest.previous_runtime_manifest_sha256}else{$lfManifest.runtime_manifest_sha256}
 if((Get-FileHash -LiteralPath 'C:\LF-QA\App\runtime\runtime-manifest.json').Hash.ToLower() -ne $lfRuntimeHash){throw 'Installed runtime provenance differs from the pinned installer'}
 $lfLedger=$null
 if($lfPrevious -and -not $lfLedgerHash){
  # Audited beta3 predates the transaction ledger. Do not invent one or skip
  # runtime verification: pin its launcher and complete runtime independently.
  if(Test-Path -LiteralPath 'C:\LF-QA\App\installer-manifest.json'){throw 'Unexpected ledger in legacy beta3'}
  if((Get-FileHash -LiteralPath 'C:\LF-QA\App\color-studio-beta.exe').Hash.ToLower() -ne $lfManifest.previous_launcher_sha256){throw 'Legacy launcher differs from its full NSIS audit'}
 }else{
  if((Get-FileHash -LiteralPath 'C:\LF-QA\App\installer-manifest.json').Hash.ToLower() -ne $lfLedgerHash){throw 'Installed ledger differs from the pinned installer'}
  $lfLedger=Get-Content -LiteralPath 'C:\LF-QA\App\installer-manifest.json' -Raw|ConvertFrom-Json
 }
 $lfRuntime=Get-Content -LiteralPath 'C:\LF-QA\App\runtime\runtime-manifest.json' -Raw|ConvertFrom-Json
 foreach($lfFile in $lfLedger.files.psobject.Properties){
  if([IO.Path]::IsPathRooted($lfFile.Name) -or $lfFile.Name -match '(^|[\\/])\.\.([\\/]|$)|:'){throw 'Unsafe installed ledger path'}
  $lfPath=Join-Path 'C:\LF-QA\App' $lfFile.Name;Test-LfPath $lfPath
  if((Get-FileHash -LiteralPath $lfPath).Hash.ToLower() -ne $lfFile.Value){throw 'Installed application bytes changed'}
 }
 foreach($lfFile in $lfRuntime.files.psobject.Properties){
  if([IO.Path]::IsPathRooted($lfFile.Name) -or $lfFile.Name -match '(^|[\\/])\.\.([\\/]|$)|:'){throw 'Unsafe runtime path'}
  $lfPath=Join-Path 'C:\LF-QA\App\runtime' $lfFile.Name;Test-LfPath $lfPath
  if((Get-FileHash -LiteralPath $lfPath).Hash.ToLower() -ne $lfFile.Value.sha256){throw 'Installed runtime bytes changed'}
 }
}
function Invoke-LfApi([string]$lfName,[string]$lfSeed,[switch]$Cancel){
 $lfArgs=@('-I','-S','-B',"$lfKit\scripts\qa_guest_api.py",'--output',"$lfRun\$lfName")
 if($lfSeed){$lfArgs+=@('--seed',$lfSeed)};if($Cancel){$lfArgs+='--cancellation'}
 if($lfName -ne 'seed' -and $lfManifest.version -eq '0.3.0-beta.7'){$lfArgs+='--projects'}
 & 'C:\LF-QA\App\runtime\python.exe' @lfArgs *> "$lfRun\$lfName.log"
 if($LASTEXITCODE -ne 0){throw 'Installed API check failed; inspect the private log'}
 $lfResult=Get-Content -LiteralPath "$lfRun\$lfName\result.json" -Raw|ConvertFrom-Json
 $lfExpectedVersion=if($lfName -eq 'seed'){$lfManifest.previous_version}else{$lfManifest.version}
 if($lfResult.version -ne $lfExpectedVersion){throw 'Wrong application version exercised'}
 if($Cancel -and $lfResult.cancellation -ne 'PASS'){throw 'Cancellation was not exercised; not a pass'}
 return $lfResult
}
function Save-LfBaseline([string]$lfName){
 & "$lfKit\qa_windows_preservation.ps1" -Mode Snapshot -DataDirectory 'C:\LF-QA\Data' -Baseline "$lfRun\$lfName.json" | Out-Null
 if($LASTEXITCODE -ne 0){throw 'Cannot capture a preservation baseline'}
}
function Test-LfBaseline([string]$lfName,[string]$lfResult){
 & "$lfKit\qa_windows_preservation.ps1" -Mode Verify -DataDirectory 'C:\LF-QA\Data' -Baseline "$lfRun\$lfName.json" -Report "$lfRun\$lfResult.json"|Out-Null
 if($LASTEXITCODE -ne 0 -or -not(Get-Content -LiteralPath "$lfRun\$lfResult.json" -Raw|ConvertFrom-Json).passed){throw 'Data preservation failed; do not continue'}
}
function Restore-LfNetwork{
 $lfRestoreFailed=$false
 foreach($lfAdapter in $lfNetwork){
  try{
   Enable-NetAdapter -InputObject $lfAdapter -Confirm:$false
   $lfRestored=@(Get-NetAdapter -IncludeHidden|Where-Object {$_.InterfaceGuid -eq $lfAdapter.InterfaceGuid})
   if($lfRestored.Count -ne 1 -or $lfRestored[0].AdminStatus -ne 'Up'){$lfRestoreFailed=$true}
  }catch{$lfRestoreFailed=$true}
 }
 if($lfRestoreFailed){$lfReport['network_restore_failed']=$true;throw 'Guest adapter restoration not verified; inspect the guest, not the host'}
}
try{
 foreach($lfTool in @('python','node','git','cargo')){
  $lfCommand=Get-Command $lfTool -ErrorAction SilentlyContinue
  if($lfCommand -and $lfCommand.Source -notlike '*WindowsApps*'){throw 'Development tool present; clean-guest context is not verified'}
 }
 $lfSteps.guest_identity=@{status='PASS';checkpoint_metadata_matched=$true;checkpoint_contents='operator attestation plus guest preflight, not restored or independently certified'}
 New-Item -ItemType Directory -Path "$lfRun\tmp"|Out-Null;$env:TEMP="$lfRun\tmp";$env:TMP=$env:TEMP;$env:LF_QA_VM_VERIFIED='1'
 if($CleanCandidate){
  $lfActive='clean_candidate_install';if((Invoke-LfSetup 'candidate.exe') -ne 0){throw 'Clean candidate installation failed'}
  Test-LfRuntime $false;$lfSteps.clean_candidate_install=@{status='PASS'}
 }else{
  $lfActive='previous_install';if((Invoke-LfSetup 'previous.exe') -ne 0){throw 'Beta3 installation failed'}
  Test-LfRuntime $true;$lfSteps.previous_install=@{status='PASS'}
 }
 New-Item -ItemType Directory -Path 'C:\LF-QA\Data'|Out-Null
 Set-Content -LiteralPath 'C:\LF-QA\Data\.synthetic-qa-only' -Value 'Dedicated synthetic VM fixture only'
 $lfSeed=''
 if(-not $CleanCandidate){
 $lfActive='seed_api';$lfSteps.seed_api=@{status='PASS';result=(Invoke-LfApi 'seed' '')};Save-LfBaseline 'before-update'
 $lfActive='failed_upgrade'
 Add-Type -TypeDefinition 'using System; using System.Runtime.InteropServices; public static class LfQaDirectoryLock { [DllImport("kernel32.dll",CharSet=CharSet.Unicode,SetLastError=true)] public static extern IntPtr CreateFileW(string p,uint a,uint s,IntPtr q,uint c,uint f,IntPtr t); [DllImport("kernel32.dll")] public static extern bool CloseHandle(IntPtr h); }'
 $lfLock=[LfQaDirectoryLock]::CreateFileW('C:\LF-QA\App',0x80,3,[IntPtr]::Zero,3,0x02000000,[IntPtr]::Zero)
 if($lfLock -eq [IntPtr](-1)){throw 'Cannot acquire the synthetic sharing lock'}
 try{$lfFailedExit=Invoke-LfSetup 'candidate.exe'}finally{[LfQaDirectoryLock]::CloseHandle($lfLock)|Out-Null;$lfLock=[IntPtr]::Zero}
 if($lfFailedExit -ne 2){throw 'Expected controlled upgrade failure was not observed; preserve state'}
 $lfSwitch=@($script:lfLastSetupEvents|Where-Object {$_.phase -eq 'directory_switch_failed'})
 if($lfSwitch.Count -ne 1 -or $lfSwitch[0].winerror -notin @(5,32)){throw 'Expected native failure phase not demonstrated; inspect the private installer logs'}
 Test-LfBaseline 'before-update' 'after-failed-update';Test-LfRuntime $true
 $lfSteps.failed_upgrade=@{status='PASS';exit_code=$lfFailedExit;helper_phase=$lfSwitch[0].phase;winerror=$lfSwitch[0].winerror;fault='Real Win32 directory handle without delete sharing; not a historical attribution'}
 $lfActive='upgrade';if((Invoke-LfSetup 'candidate.exe') -ne 0){throw "Direct upgrade from $($lfManifest.previous_version) to $($lfManifest.version) failed"}
 Test-LfRuntime $false;Test-LfBaseline 'before-update' 'after-update';$lfSteps.upgrade=@{status='PASS'}
 $lfSeed="$lfRun\seed\state.json"
 }
 $lfActive='candidate_api';$lfSteps.candidate_api=@{status='PASS';result=(Invoke-LfApi 'candidate' $lfSeed -Cancel)}
 $lfCandidateState="$lfRun\candidate\state.json"
 Save-LfBaseline 'before-restart'
 $lfActive='restart_api';$lfRestart=Invoke-LfApi 'restart' $lfCandidateState
 Test-LfBaseline 'before-restart' 'after-restart';$lfSteps.restart_api=@{status='PASS';result=$lfRestart}
 $lfActive='interruption_fixtures'; & "$lfKit\qa_guest_checks.ps1" -RunFixtures *> "$lfRun\interruption-fixtures.log"
 if($LASTEXITCODE -ne 0){throw 'Interruption fixture failed or skipped'};$lfSteps.interruption_fixtures=@{status='PASS';scope='Fixture interruptions; not a power cut or cancellation of the full NSIS'}
 $lfActive='offline_api';$lfNetwork=@(Get-NetAdapter -IncludeHidden|Where-Object {$_.Status -eq 'Up'})
 if($lfNetwork.Count -eq 0){throw 'No connected guest adapter to demonstrate a real disconnection'}
 $lfNetworkChanged=$true
 try{
  foreach($lfAdapter in $lfNetwork){Disable-NetAdapter -InputObject $lfAdapter -Confirm:$false}
  if(@(Get-NetAdapter -IncludeHidden|Where-Object {$_.Status -eq 'Up'}).Count -ne 0){throw 'Guest still has an active network adapter'}
  $lfSteps.offline_api=@{status='PASS';adapters_actually_disabled=$lfNetwork.Count;result=(Invoke-LfApi 'offline' $lfCandidateState)}
 }finally{Restore-LfNetwork;$lfNetworkChanged=$false}
 $lfActive='uninstall';Save-LfBaseline 'before-uninstall'
 if((Get-FileHash -LiteralPath 'C:\LF-QA\App\uninstall.exe').Hash.ToLower() -ne $lfManifest.candidate_uninstaller_sha256){throw 'Uninstaller hash differs; do not execute'}
 $lfUninstaller=Start-Process -FilePath 'C:\LF-QA\App\uninstall.exe' -ArgumentList '/S' -WindowStyle Hidden -PassThru
 if(-not $lfUninstaller.WaitForExit(180000)){throw 'Uninstall timed out; preserve its process and test data'}
 $lfUninstaller.Refresh();if($lfUninstaller.ExitCode -ne 0){throw 'Uninstall failed'}
 # NSIS can hand off to a temporary child. Parent exit0 alone is not completion.
 $lfDeadline=[DateTime]::UtcNow.AddSeconds(180)
 while((Test-Path -LiteralPath 'C:\LF-QA\App') -and [DateTime]::UtcNow -lt $lfDeadline){Start-Sleep -Milliseconds 250}
 if(Test-Path -LiteralPath 'C:\LF-QA\App'){throw 'Uninstall completion not observed; do not delete residual files to force a pass'}
 Test-LfBaseline 'before-uninstall' 'after-uninstall'
 if(Test-Path -LiteralPath 'C:\LF-QA\App\color-studio-beta.exe'){throw 'Launcher remains after uninstall'}
 $lfSteps.uninstall=@{status='PASS'};$lfReport.technical_automation_passed=$true
}catch{
 $lfSteps[$lfActive]=@{status='FAIL';error_type=$_.Exception.GetType().Name;error_id=$_.FullyQualifiedErrorId}
 $_|Out-String|Set-Content -LiteralPath "$lfRun\failure-private.txt"
}finally{
 if($lfLock -ne [IntPtr]::Zero -and $lfLock -ne [IntPtr](-1)){[LfQaDirectoryLock]::CloseHandle($lfLock)|Out-Null}
 if($lfNetworkChanged){try{Restore-LfNetwork}catch{$lfReport.technical_automation_passed=$false}}
 $env:TEMP=$lfOldTemp;$env:TMP=$lfOldTmp;$env:LF_QA_VM_VERIFIED=$lfOldVerified
 $lfReport|ConvertTo-Json -Depth 12|Set-Content -LiteralPath "$lfRun\report.json" -Encoding UTF8
}
Write-Output $lfRun
if(-not $lfReport.technical_automation_passed){throw 'Cycle incomplete. Read report.json; original evidence is preserved'}
