param(
 [Parameter(Mandatory=$true)][ValidateSet('Snapshot','Verify')][string]$Mode,
 [Parameter(Mandatory=$true)][string]$DataDirectory,
 [Parameter(Mandatory=$true)][string]$Baseline,
 [string]$Report
)
# Run with Color Studio closed. Baseline is private: relative filenames may identify data.
# Read-only for application data; no installation, registry or privilege changes.
$ErrorActionPreference='Stop'
$lfRoot=[IO.Path]::GetFullPath((Resolve-Path -LiteralPath $DataDirectory).ProviderPath).TrimEnd('\')
$lfPrefix=$lfRoot+'\'
$lfBaseline=[IO.Path]::GetFullPath($Baseline)
if($lfBaseline.StartsWith($lfPrefix,[StringComparison]::OrdinalIgnoreCase)){throw 'Store private baseline outside the data directory'}
if((Get-Item -LiteralPath $lfRoot).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Reparse point root is not allowed'}
if(Get-ChildItem -LiteralPath $lfRoot -Force -Recurse | Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}){throw 'Reparse points are not allowed'}
function Get-LfStoreIdentity {
 $lfIdOutput=@(& "$env:SystemRoot/System32/fsutil.exe" file queryfileid $lfRoot 2>&1)
 if($LASTEXITCODE -ne 0){throw 'Cannot bind preservation evidence to a directory identity'}
 $lfIdMatch=[regex]::Match([string]::Join(' ',$lfIdOutput),'(?i)0x[0-9a-f]{32}')
 $lfVolumeOutput=@(& "$env:SystemRoot/System32/mountvol.exe" ([IO.Path]::GetPathRoot($lfRoot)) /L 2>&1)
 if($LASTEXITCODE -ne 0){throw 'Cannot bind preservation evidence to a volume identity'}
 $lfVolumeMatch=[regex]::Match([string]::Join(' ',$lfVolumeOutput),'(?i)Volume\{[a-f0-9-]{36}\}')
 if(-not $lfIdMatch.Success -or -not $lfVolumeMatch.Success){throw 'Missing NTFS/volume identity; no preservation claim'}
 return ($lfVolumeMatch.Value+'|'+$lfIdMatch.Value).ToLowerInvariant()
}
$lfIdentity=Get-LfStoreIdentity
if($Mode -eq 'Snapshot'){
 if(Test-Path -LiteralPath $lfBaseline){throw 'Refusing to overwrite an existing baseline'}
 $lfFiles=@(Get-ChildItem -LiteralPath $lfRoot -File -Recurse -Force | Sort-Object FullName | ForEach-Object {
  @{relative=([IO.Path]::GetFullPath($_.FullName)).Substring($lfPrefix.Length);sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLower();bytes=$_.Length}
 })
 if($lfFiles.Count -eq 0){throw 'Empty directory is not evidence of data preservation'}
 if((Get-LfStoreIdentity) -ne $lfIdentity){throw 'Directory changed during snapshot; preserve evidence and retry'}
 @{schema='color-studio-private-data-baseline-v2';store_identity=$lfIdentity;files=$lfFiles;privacy='private_do_not_publish'} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $lfBaseline -Encoding UTF8
 Write-Output 'Private baseline saved. Close application again before Verify.'
 exit 0
}
if(-not $Report){throw 'Report is required in Verify mode'}
$lfReport=[IO.Path]::GetFullPath($Report)
if($lfReport -eq $lfBaseline -or $lfReport.StartsWith($lfPrefix,[StringComparison]::OrdinalIgnoreCase)){throw 'Report must be outside data and different from baseline'}
if(Test-Path -LiteralPath $lfReport){throw 'Refusing to overwrite an existing report'}
$lfSaved=Get-Content -LiteralPath $lfBaseline -Raw | ConvertFrom-Json
if($lfSaved.schema -ne 'color-studio-private-data-baseline-v2' -or -not $lfSaved.files -or $lfSaved.store_identity -notmatch '^volume\{[a-f0-9-]{36}\}\|0x[a-f0-9]{32}$'){throw 'Use a v2 baseline with captured physical identity; retain old evidence separately'}
if($lfSaved.store_identity -ne $lfIdentity){
 @{schema='color-studio-preservation-result-v2';checked=0;missing=$null;changed=$null;identity_verified=$false;passed=$false;reason='different_store_identity';personal_identifiers_collected=$false} | ConvertTo-Json | Set-Content -LiteralPath $lfReport -Encoding UTF8
 Write-Output 'Different volume/directory identity: hashes cannot certify this store';exit 2
}
$lfMissing=0;$lfChanged=0;$lfChecked=0
foreach($lfFile in $lfSaved.files){
 if(-not ($lfFile.relative -is [string]) -or [IO.Path]::IsPathRooted($lfFile.relative)){throw 'Invalid relative baseline path'}
 $lfPath=[IO.Path]::GetFullPath((Join-Path $lfRoot $lfFile.relative))
 if(-not $lfPath.StartsWith($lfPrefix,[StringComparison]::OrdinalIgnoreCase)){throw 'Baseline path escapes data directory'}
 if($lfFile.sha256 -notmatch '^[a-f0-9]{64}$'){throw 'Invalid baseline digest'}
 $lfChecked++
 if(-not (Test-Path -LiteralPath $lfPath -PathType Leaf)){$lfMissing++;continue}
 if((Get-FileHash -LiteralPath $lfPath -Algorithm SHA256).Hash.ToLower() -ne $lfFile.sha256){$lfChanged++}
}
$lfIdentitySame=((Get-LfStoreIdentity) -eq $lfIdentity)
@{schema='color-studio-preservation-result-v2';checked=$lfChecked;missing=$lfMissing;changed=$lfChanged;identity_verified=$lfIdentitySame;passed=($lfIdentitySame -and $lfMissing -eq 0 -and $lfChanged -eq 0);scope='Sampled volume/directory identity and baseline hashes in this context, not cross-namespace or Windows-clean certification';personal_identifiers_collected=$false} | ConvertTo-Json | Set-Content -LiteralPath $lfReport -Encoding UTF8
if(-not $lfIdentitySame -or $lfMissing -or $lfChanged){Write-Output 'Preservation failed; review privately before proceeding';exit 2}
Write-Output 'All baseline file hashes preserved. New files are permitted; this does not approve the application.'
