param(
 [Parameter(Mandatory=$true)][string]$IncidentLocalTime,
 [string]$TimeZoneId='Romance Standard Time',
 [string]$SnapshotPath,
 [string]$OutputPath,
 [switch]$ValidateOnly
)
# Read existing Security events only; never enables auditing or elevates itself.
$ErrorActionPreference='Stop'
$lfRoot=[IO.Path]::GetFullPath((Join-Path $PSScriptRoot '..'))
$lfPrivate=Join-Path $lfRoot '.lumaforge-local'
function Assert-LfPrivate([string]$Value){
 $lfFull=[IO.Path]::GetFullPath($Value)
 if(-not $lfFull.StartsWith($lfPrivate.TrimEnd('\','/')+[IO.Path]::DirectorySeparatorChar,[StringComparison]::OrdinalIgnoreCase)){throw 'Evidence paths must stay in the private workspace'}
 $lfPart=$lfFull
 while($lfPart -and $lfPart.Length -ge $lfPrivate.Length){
  if((Test-Path -LiteralPath $lfPart) -and ((Get-Item -LiteralPath $lfPart -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Linked evidence paths refused'}
  $lfNext=Split-Path -Parent $lfPart;if($lfNext -eq $lfPart){break};$lfPart=$lfNext
 }
 return $lfFull
}
if(-not $SnapshotPath){$SnapshotPath=Join-Path $lfPrivate 'existing-data-snapshot.json'}
if(-not $OutputPath){$OutputPath=Join-Path $lfPrivate ('security-event-evidence-'+[guid]::NewGuid().ToString('N')+'.json')}
$SnapshotPath=Assert-LfPrivate $SnapshotPath;$OutputPath=Assert-LfPrivate $OutputPath
if((Test-Path -LiteralPath $OutputPath) -or -not(Test-Path -LiteralPath (Split-Path -Parent $OutputPath) -PathType Container)){throw 'Use a fresh evidence file in an existing private directory'}
$lfLocal=[DateTime]::ParseExact($IncidentLocalTime,'yyyy-MM-ddTHH:mm:ss',[Globalization.CultureInfo]::InvariantCulture)
$lfZone=[TimeZoneInfo]::FindSystemTimeZoneById($TimeZoneId)
$lfUtc=[TimeZoneInfo]::ConvertTimeToUtc([DateTime]::SpecifyKind($lfLocal,[DateTimeKind]::Unspecified),$lfZone)
$lfSnapshot=Get-Content -LiteralPath $SnapshotPath -Raw | ConvertFrom-Json
$lfNames=@{}
foreach($lfRow in $lfSnapshot.PSObject.Properties){
 if($lfRow.Name -notmatch '^(preferences\.json|(?:images|presets)/[a-f0-9-]{36}\.(?:png|json))$' -or [string]$lfRow.Value -notmatch '^[a-f0-9]{64}$'){throw 'Invalid snapshot entry'}
 $lfNames[(Split-Path -Leaf $lfRow.Name)]=$true
}
if(-not $lfNames.Count){throw 'Empty private snapshot is not usable evidence'}
function Select-LfTargetEvents($Events,$Names){
 $lfParsed=@();$lfHandles=@{};$lfSelected=@()
 foreach($lfEvent in $Events){
  $lfXml=[xml]$lfEvent.ToXml();$lfData=@{}
  foreach($lfField in $lfXml.Event.EventData.Data){$lfData[$lfField.GetAttribute('Name')]=$lfField.InnerText}
  $lfObject=[string]$lfData['ObjectName'];$lfName=if($lfObject){Split-Path -Leaf $lfObject}else{''}
  $lfTarget=($lfObject -match '(?i)[\\/]ColorStudioBetaData[\\/]' -and $Names.ContainsKey($lfName))
  $lfHandle=([string]$lfData['ProcessId'])+'|'+([string]$lfData['HandleId'])
  if($lfTarget -and $lfData['ProcessId'] -and $lfData['HandleId'] -and [string]$lfData['HandleId'] -notin @('0','0x0','-')){$lfHandles[$lfHandle]=$true}
  $lfParsed+=@{id=$lfEvent.Id;time_utc=$lfEvent.TimeCreated.ToUniversalTime().ToString('o');record_id=$lfEvent.RecordId;data=$lfData;target=$lfTarget;handle=$lfHandle}
 }
 foreach($lfRow in $lfParsed){if($lfRow.target -or ($lfRow.id -eq 4660 -and $lfHandles.ContainsKey($lfRow.handle))){$lfSelected+=@{id=$lfRow.id;time_utc=$lfRow.time_utc;record_id=$lfRow.record_id;data=$lfRow.data}}}
 return @{retained=$lfSelected}
}
$lfPrincipal=New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$lfStatus='not_queried';$lfRetained=@();$lfRead=0;$lfErrorId=$null
if($ValidateOnly){$lfStatus='validation_only_no_events_read'}
elseif(-not $lfPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)){$lfStatus='requires_elevated_operator'}
else{
 try{
  $lfEvents=@(Get-WinEvent -FilterHashtable @{LogName='Security';Id=4656,4660,4663;StartTime=$lfUtc.AddMinutes(-3);EndTime=$lfUtc.AddMinutes(3)} -MaxEvents 5000 -ErrorAction Stop)
  $lfRead=$lfEvents.Count;$lfRetained=@((Select-LfTargetEvents $lfEvents $lfNames).retained)
  $lfStatus='queried_existing_audit'
 }catch{
  $lfErrorId=$_.FullyQualifiedErrorId
  $lfStatus=if($lfErrorId -like 'NoMatchingEventsFound*'){'no_matching_events_in_existing_audit'}else{'audit_unavailable'}
 }
}
$lfReport=@{schema='color-studio-private-security-evidence-v1';incident_local=$IncidentLocalTime;timezone=$TimeZoneId;incident_utc=$lfUtc.ToString('o');observed_at_utc=[DateTime]::UtcNow.ToString('o');status=$lfStatus;error_id=$lfErrorId;events_examined=$lfRead;possibly_truncated=($lfRead -ge 5000);matching_events=$lfRetained;logging_configuration_changed=$false;data_files_read_or_modified=$false;automatic_attribution=$false;limits='Existing logs only. No matching event does not prove no deletion. Correlate object/handle/time before attributing a process.';privacy='Private only; never attach to GitHub.'}
$lfBytes=(New-Object Text.UTF8Encoding($false)).GetBytes(($lfReport | ConvertTo-Json -Depth 12)+"`n")
$lfStream=[IO.File]::Open($OutputPath,[IO.FileMode]::CreateNew,[IO.FileAccess]::Write,[IO.FileShare]::None)
try{$lfStream.Write($lfBytes,0,$lfBytes.Length)}finally{$lfStream.Dispose()}
Write-Output ('Status='+$lfStatus+'; matching_events='+$lfRetained.Count)
Write-Output ('Private report: '+$OutputPath)
