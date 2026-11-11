param(
 [string]$SnapshotPath,
 [string]$DataDir=(Join-Path $env:LOCALAPPDATA 'ColorStudioBetaData'),
 [string]$OutputPath,
 [switch]$ReadUsn
)
# Read-only diagnosis. No restore/delete, permissions change or journal mutation.
$ErrorActionPreference='Stop'
$lfRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$lfPrivate=Join-Path $lfRoot '.lumaforge-local'
if(-not $SnapshotPath){$SnapshotPath=Join-Path $lfPrivate 'existing-data-snapshot.json'}
if(-not $OutputPath){$OutputPath=Join-Path $lfPrivate ('store-diagnosis-'+[guid]::NewGuid().ToString('N')+'.json')}
function Assert-PrivatePath([string]$Value){
 $lfFull=[IO.Path]::GetFullPath($Value)
 $lfPrefix=$lfPrivate.TrimEnd('\','/')+[IO.Path]::DirectorySeparatorChar
 if(-not $lfFull.StartsWith($lfPrefix,[StringComparison]::OrdinalIgnoreCase)){throw 'Snapshot/output must stay in the private workspace directory'}
 $lfPart=$lfFull
 while($lfPart -and $lfPart.Length -ge $lfPrivate.Length){
  if(Test-Path -LiteralPath $lfPart){
   if((Get-Item -LiteralPath $lfPart -Force).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Linked private paths are refused'}
  }
  $lfNext=Split-Path -Parent $lfPart
  if($lfNext -eq $lfPart){break};$lfPart=$lfNext
 }
 return $lfFull
}
$SnapshotPath=Assert-PrivatePath $SnapshotPath
$OutputPath=Assert-PrivatePath $OutputPath
if(Test-Path -LiteralPath $OutputPath){throw 'Preserve existing output; choose a fresh filename'}
if(-not(Test-Path -LiteralPath (Split-Path -Parent $OutputPath) -PathType Container)){throw 'Output directory must already exist'}
$lfSnapshot=Get-Content -LiteralPath $SnapshotPath -Raw | ConvertFrom-Json
$DataDir=[IO.Path]::GetFullPath($DataDir)
if((Split-Path -Leaf $DataDir) -ne 'ColorStudioBetaData'){throw 'Expected the explicit ColorStudioBetaData directory'}
$lfFsutil=Join-Path $env:SystemRoot 'System32/fsutil.exe'
function Get-LfDirectoryIdentity([string]$Directory){
 # Read an existing NTFS object id without creating files or changing privileges.
 if(-not(Test-Path -LiteralPath $Directory -PathType Container)){return @{status='absent'}}
 $lfItem=Get-Item -LiteralPath $Directory -Force
 if($lfItem.Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Linked data paths are refused'}
 $lfSavedPreference=$ErrorActionPreference
 try{
  $ErrorActionPreference='Continue'
  $lfIdentity=@(& $lfFsutil file queryfileid $Directory 2>&1 | ForEach-Object {[string]$_})
  $lfIdentityExit=$LASTEXITCODE
 }finally{$ErrorActionPreference=$lfSavedPreference}
 return @{status=if($lfIdentityExit -eq 0){'queried'}else{'query_failed'};exit=$lfIdentityExit
  volume=[IO.Path]::GetPathRoot($Directory);file_id_query=$lfIdentity
  creation_utc=$lfItem.CreationTimeUtc.ToString('o');last_write_utc=$lfItem.LastWriteTimeUtc.ToString('o')}
}
$lfIdentities=@{}
foreach($lfDirectory in @($DataDir,(Join-Path $DataDir 'images'),(Join-Path $DataDir 'presets'))){
 $lfIdentities[$lfDirectory]=Get-LfDirectoryIdentity $lfDirectory
}
$lfMissing=New-Object 'System.Collections.Generic.List[string]'
$lfChanged=New-Object 'System.Collections.Generic.List[string]'
$lfPresent=0
$lfRows=@($lfSnapshot.PSObject.Properties)
foreach($lfRow in $lfRows){
 if($lfRow.Name -notmatch '^(preferences\.json|(?:images|presets)/[a-f0-9-]{36}\.(?:png|json))$' -or [string]$lfRow.Value -notmatch '^[a-f0-9]{64}$'){throw 'Invalid private snapshot entry'}
 $lfFile=Join-Path $DataDir $lfRow.Name.Replace('/','\')
 if(-not(Test-Path -LiteralPath $lfFile -PathType Leaf)){[void]$lfMissing.Add($lfRow.Name);continue}
 $lfPart=$lfFile
 while($lfPart.Length -ge $DataDir.Length){
  if((Get-Item -LiteralPath $lfPart -Force).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Linked data paths are refused'}
  $lfNext=Split-Path -Parent $lfPart
  if($lfNext -eq $lfPart){break};$lfPart=$lfNext
 }
 $lfPresent++
 $lfHasher=[Security.Cryptography.SHA256]::Create()
 $lfInput=[IO.File]::OpenRead($lfFile)
 try{$lfHash=[BitConverter]::ToString($lfHasher.ComputeHash($lfInput)).Replace('-','').ToLowerInvariant()}
 finally{$lfInput.Dispose();$lfHasher.Dispose()}
 if($lfHash -ne [string]$lfRow.Value){[void]$lfChanged.Add($lfRow.Name)}
}
$lfJournal=@{requested=[bool]$ReadUsn;status='not_requested';matched_rows=@();exit=$null;matches_truncated=$false}
if($ReadUsn -and $lfMissing.Count){
 $lfPrincipal=New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
 if(-not $lfPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)){
  $lfJournal.status='not_run_requires_elevated_operator'
 } else {
  if($DataDir -notmatch '^[A-Za-z]:\\'){throw 'USN diagnosis only supports the explicit local volume'}
  $lfVolume=$DataDir.Substring(0,2)
  $lfPattern=(@($lfMissing | ForEach-Object {[regex]::Escape((Split-Path -Leaf $_))}) -join '|')
  $lfMatches=New-Object 'System.Collections.Generic.List[string]'
  $lfSavedPreference=$ErrorActionPreference
  try{
   # Native read failures must still produce a private diagnostic receipt.
   $ErrorActionPreference='Continue'
   $lfQuery=& $lfFsutil usn queryjournal $lfVolume 2>&1
   $lfJournal.query_exit=$LASTEXITCODE
   $lfJournal.query_metadata=@($lfQuery | ForEach-Object {[string]$_})
   # Finite read; no wait/tail, no create/delete/enablerangetracking commands.
   & $lfFsutil usn readjournal $lfVolume csv 2>&1 | ForEach-Object {
    $lfLine=[string]$_
    if($lfLine -match $lfPattern){
     if($lfMatches.Count -lt 2048){[void]$lfMatches.Add($lfLine)}else{$lfJournal.matches_truncated=$true}
    }
   }
   $lfJournal.exit=$LASTEXITCODE
   $lfJournal.status=if($LASTEXITCODE -eq 0){'read_completed'}else{'read_failed'}
  }finally{$ErrorActionPreference=$lfSavedPreference}
  $lfJournal.matched_rows=@($lfMatches.ToArray())
 }
}
$lfReport=@{
 schema='color-studio-private-store-diagnosis-v1';observed_at_utc=[DateTime]::UtcNow.ToString('o')
 data_directory=$DataDir;snapshot=$SnapshotPath;snapshot_files=$lfRows.Count
 directory_identities=$lfIdentities
 present_files=$lfPresent;missing=@($lfMissing.ToArray());changed=@($lfChanged.ToArray())
 all_snapshot_files_present=($lfMissing.Count -eq 0);present_hashes_equal=($lfChanged.Count -eq 0)
 data_directory_last_write_utc=if(Test-Path -LiteralPath $DataDir){(Get-Item -LiteralPath $DataDir).LastWriteTimeUtc.ToString('o')}else{$null}
 usn=$lfJournal;files_restored=0;files_deleted=0;permissions_changed=$false
 limits='A retained journal may omit older events and does not identify the deleting process. No cause, recovery or human acceptance is inferred.'
 share='Private operator result only. Do not upload paths, filenames or raw journal rows to GitHub.'
}
$lfJson=$lfReport | ConvertTo-Json -Depth 8
$lfEncoding=New-Object Text.UTF8Encoding($false)
$lfBytes=$lfEncoding.GetBytes($lfJson+"`n")
$lfStream=[IO.File]::Open($OutputPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$lfStream.Write($lfBytes,0,$lfBytes.Length)}finally{$lfStream.Dispose()}
Write-Output ('Private diagnosis saved. Missing='+$lfMissing.Count+'; changed='+$lfChanged.Count+'; USN='+$lfJournal.status)
Write-Output ('Private report: '+$OutputPath)
