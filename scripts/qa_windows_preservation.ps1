param(
 [Parameter(Mandatory=$true)][ValidateSet('Snapshot','Verify')][string]$Mode,
 [Parameter(Mandatory=$true)][string]$DataDirectory,
 [Parameter(Mandatory=$true)][string]$Baseline,
 [string]$Report
)
# Run with Color Studio closed. Baseline is private: relative filenames may identify data.
# Read-only for application data; no installation, registry or privilege changes.
$ErrorActionPreference='Stop'
$lfRoot=(Resolve-Path -LiteralPath $DataDirectory).Path.TrimEnd('\')
$lfPrefix=$lfRoot+'\'
$lfBaseline=[IO.Path]::GetFullPath($Baseline)
if($lfBaseline.StartsWith($lfPrefix,[StringComparison]::OrdinalIgnoreCase)){throw 'Store private baseline outside the data directory'}
if((Get-Item -LiteralPath $lfRoot).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Reparse point root is not allowed'}
if(Get-ChildItem -LiteralPath $lfRoot -Force -Recurse | Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}){throw 'Reparse points are not allowed'}
if($Mode -eq 'Snapshot'){
 if(Test-Path -LiteralPath $lfBaseline){throw 'Refusing to overwrite an existing baseline'}
 $lfFiles=@(Get-ChildItem -LiteralPath $lfRoot -File -Recurse -Force | Sort-Object FullName | ForEach-Object {
  @{relative=$_.FullName.Substring($lfPrefix.Length);sha256=(Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLower();bytes=$_.Length}
 })
 if($lfFiles.Count -eq 0){throw 'Empty directory is not evidence of data preservation'}
 @{schema='color-studio-private-data-baseline-v1';files=$lfFiles;privacy='private_do_not_publish'} | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath $lfBaseline -Encoding UTF8
 Write-Output 'Private baseline saved. Close application again before Verify.'
 exit 0
}
if(-not $Report){throw 'Report is required in Verify mode'}
$lfReport=[IO.Path]::GetFullPath($Report)
if($lfReport -eq $lfBaseline -or $lfReport.StartsWith($lfPrefix,[StringComparison]::OrdinalIgnoreCase)){throw 'Report must be outside data and different from baseline'}
if(Test-Path -LiteralPath $lfReport){throw 'Refusing to overwrite an existing report'}
$lfSaved=Get-Content -LiteralPath $lfBaseline -Raw | ConvertFrom-Json
if($lfSaved.schema -ne 'color-studio-private-data-baseline-v1' -or -not $lfSaved.files){throw 'Invalid or empty baseline'}
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
@{schema='color-studio-preservation-result-v1';checked=$lfChecked;missing=$lfMissing;changed=$lfChanged;passed=($lfMissing -eq 0 -and $lfChanged -eq 0);scope='Only baseline files, not a Windows-clean claim';personal_identifiers_collected=$false} | ConvertTo-Json | Set-Content -LiteralPath $lfReport -Encoding UTF8
if($lfMissing -or $lfChanged){Write-Output 'Preservation failed; review privately before proceeding';exit 2}
Write-Output 'All baseline file hashes preserved. New files are permitted; this does not approve the application.'
