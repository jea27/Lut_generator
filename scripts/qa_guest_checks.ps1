param([switch]$Install,[switch]$InstallPrevious,[switch]$RunFixtures,[switch]$RunProbes,[switch]$Launch)
$ErrorActionPreference='Stop'
$lfComputer=Get-CimInstance Win32_ComputerSystem
$lfOs=Get-CimInstance Win32_OperatingSystem
if($lfComputer.Model -notmatch 'Virtual Machine|VirtualBox|VMware|KVM|QEMU' -or $lfOs.ProductType -ne 1 -or [int]$lfOs.BuildNumber -lt 22000){throw 'Requires an isolated Windows11 VM; never run this QA on the personal host'}
$lfKit=[IO.Path]::GetFullPath($PSScriptRoot)
if($lfKit -ne 'C:\LF-QA\Kit'){throw 'Extract the verified kit into C:\LF-QA\Kit inside the VM'}
function Test-LfUnlinked([string]$lfPath){
 $lfWalk=$lfPath
 while($lfWalk){
  if((Test-Path -LiteralPath $lfWalk) -and ((Get-Item -LiteralPath $lfWalk -Force).Attributes -band [IO.FileAttributes]::ReparsePoint)){throw 'Linked QA paths are not supported'}
  $lfNext=Split-Path -Parent $lfWalk
  if($lfNext -eq $lfWalk){break};$lfWalk=$lfNext
 }
}
Test-LfUnlinked $lfKit
$lfManifest=Get-Content -LiteralPath (Join-Path $lfKit 'kit-manifest.json') -Raw | ConvertFrom-Json
if($lfManifest.schema -notin @('color-studio-private-vm-kit-v1','color-studio-private-vm-kit-v2')){throw 'Unknown kit schema'}
foreach($lfFile in $lfManifest.files.psobject.Properties){
 if([IO.Path]::IsPathRooted($lfFile.Name) -or $lfFile.Name -match '(^|[\\/])\.\.([\\/]|$)|:'){throw 'Unsafe kit member'}
 $lfPath=Join-Path $lfKit $lfFile.Name;Test-LfUnlinked $lfPath
 if((Get-FileHash -LiteralPath $lfPath -Algorithm SHA256).Hash.ToLower() -ne $lfFile.Value){throw 'Kit hash mismatch'}
}
$lfPrivate=Join-Path $lfKit 'private';Test-LfUnlinked $lfPrivate
if(-not(Test-Path -LiteralPath $lfPrivate)){New-Item -ItemType Directory -Path $lfPrivate | Out-Null}
$lfTools=@{}
foreach($lfName in @('python','node','cargo','git')){
 $lfCommand=Get-Command $lfName -ErrorAction SilentlyContinue
 $lfTools[$lfName]=if(-not $lfCommand){'absent'}elseif($lfCommand.Source -like '*WindowsApps*'){'unverified_windowsapps_alias'}else{'present_not_clean'}
}
$lfReport=[ordered]@{schema='color-studio-guest-preflight-v1';version=$lfManifest.version;windows_build=$lfOs.BuildNumber;virtual_guest=$true;development_tools=$lfTools;clean_windows_test_passed=$false;native_capture_verified=$false;external_beta='NO-GO'}
$lfReport | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath (Join-Path $lfPrivate ('preflight-'+[guid]::NewGuid().ToString('N')+'.json')) -Encoding UTF8
if($InstallPrevious -and ($Install -or $RunFixtures -or $RunProbes -or $Launch)){throw 'Previous baseline installation must be a separate step'}
if($Install -or $InstallPrevious -or $Launch){
 Test-LfUnlinked 'C:\LF-QA\Data'
 $lfMarker='C:\LF-QA\Data\.synthetic-qa-only'
 if((Test-Path -LiteralPath 'C:\LF-QA\Data') -and -not(Test-Path -LiteralPath $lfMarker)){throw 'Existing unclassified data directory preserved; use the fresh VM checkpoint'}
 if(-not(Test-Path -LiteralPath 'C:\LF-QA\Data')){
  New-Item -ItemType Directory -Path 'C:\LF-QA\Data' | Out-Null
  Set-Content -LiteralPath $lfMarker -Value 'Dedicated synthetic VM fixture only'
 }
}
if($Install -or $InstallPrevious){
 Test-LfUnlinked 'C:\LF-QA\App'
 $lfSetup=if($InstallPrevious){'previous.exe'}else{'candidate.exe'}
 if($InstallPrevious -and -not $lfManifest.previous_installer_sha256){throw 'Pinned previous installer was not included'}
 $lfExit=(Start-Process -FilePath (Join-Path $lfKit $lfSetup) -ArgumentList @('/S','/D=C:\LF-QA\App') -WindowStyle Hidden -Wait -PassThru).ExitCode
 [ordered]@{installer=$lfSetup;exit_code=$lfExit;clean_windows_test_passed=$false} | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $lfPrivate ('install-'+[guid]::NewGuid().ToString('N')+'.json')) -Encoding UTF8
 if($lfExit -ne 0){throw 'Installation/upgrade failed. Preserve logs and data; never substitute uninstall/reinstall for an upgrade pass'}
}
$lfPython='C:\LF-QA\App\runtime\python.exe'
if($Install -or $RunFixtures -or $RunProbes -or $Launch){
 Test-LfUnlinked 'C:\LF-QA\App';Test-LfUnlinked 'C:\LF-QA\Data';Test-LfUnlinked 'C:\LF-QA\Inputs'
 if(-not(Test-Path -LiteralPath $lfPython)){throw 'Install the candidate into C:\LF-QA\App first'}
 if((Get-FileHash -LiteralPath 'C:\LF-QA\App\installer-manifest.json' -Algorithm SHA256).Hash.ToLower() -ne $lfManifest.installer_manifest_sha256){throw 'Installed ledger differs from the candidate'}
 if((Get-FileHash -LiteralPath 'C:\LF-QA\App\runtime\runtime-manifest.json' -Algorithm SHA256).Hash.ToLower() -ne $lfManifest.runtime_manifest_sha256){throw 'Installed runtime manifest differs from the candidate'}
 $lfLedger=Get-Content -LiteralPath 'C:\LF-QA\App\installer-manifest.json' -Raw | ConvertFrom-Json
 if((Get-FileHash -LiteralPath 'C:\LF-QA\App\color-studio-beta.exe' -Algorithm SHA256).Hash.ToLower() -ne $lfLedger.files.'color-studio-beta.exe'){throw 'Installed launcher bytes changed'}
 $lfRuntime=Get-Content -LiteralPath 'C:\LF-QA\App\runtime\runtime-manifest.json' -Raw | ConvertFrom-Json
 foreach($lfFile in $lfRuntime.files.psobject.Properties){
  if([IO.Path]::IsPathRooted($lfFile.Name) -or $lfFile.Name -match '(^|[\\/])\.\.([\\/]|$)|:'){throw 'Unsafe installed runtime member'}
  $lfPath=Join-Path 'C:\LF-QA\App\runtime' $lfFile.Name;Test-LfUnlinked $lfPath
  if((Get-FileHash -LiteralPath $lfPath -Algorithm SHA256).Hash.ToLower() -ne $lfFile.Value.sha256){throw 'Installed runtime bytes changed; do not execute it'}
 }
}
if($RunFixtures){
 $lfLog=Join-Path $lfPrivate ('fixtures-'+[guid]::NewGuid().ToString('N')+'.log')
 $lfCode='import sys,unittest,json;sys.path.append(sys.argv[1]);s=unittest.defaultTestLoader.loadTestsFromName("tests_mvp.test_installer_transaction");r=unittest.TextTestRunner(verbosity=2).run(s);print(json.dumps({"tests":r.testsRun,"skipped":len(r.skipped),"successful":r.wasSuccessful(),"clean_windows_test_passed":False}));raise SystemExit(not r.wasSuccessful() or bool(r.skipped))'
 & $lfPython -I -S -B -c $lfCode $lfKit *> $lfLog
 if($LASTEXITCODE -ne 0){throw 'Fixtures failed or skipped. Read the private log; do not change protections to force a pass'}
}
if($RunProbes){
 foreach($lfMode in @('legacy','contained')){
  foreach($lfProbe in @('images','batch-part')){
   $lfLog=Join-Path $lfPrivate ('probe-'+$lfMode+'-'+$lfProbe+'-'+[guid]::NewGuid().ToString('N')+'.log')
   & $lfPython -I -S -B (Join-Path $lfKit 'scripts/reproduce_private_deletion.py') --mode $lfMode --probe $lfProbe --direct-endpoint *> $lfLog
   if($LASTEXITCODE -ne 0){throw 'Synthetic probe failed; preserve the private trace and stop dependent QA'}
  }
 }
}
if($Launch){
 $lfOldData=$env:LUMAFORGE_DATA_DIR
 try{
  $env:LUMAFORGE_DATA_DIR='C:\LF-QA\Data'
  Start-Process -FilePath 'C:\LF-QA\App\color-studio-beta.exe' -WindowStyle Normal
 }finally{$env:LUMAFORGE_DATA_DIR=$lfOldData}
}
Write-Output 'QA scope verified. This preflight/fixture result does not approve clean Windows, native capture or distribution.'
