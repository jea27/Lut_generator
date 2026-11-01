param([string]$BuildPython='.venv-mvp/Scripts/python.exe',[switch]$Offline,[switch]$AllowDirtyInternal)
$ErrorActionPreference='Stop'
$lfRoot=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $lfRoot
$lfPython=(Resolve-Path -LiteralPath $BuildPython).Path
$lfCommonGit=(git rev-parse --path-format=absolute --git-common-dir).Trim()
$lfSharedRoot=Split-Path -Parent $lfCommonGit
$lfSevenZipCandidates=@(
 (Get-Command 7z.exe -ErrorAction SilentlyContinue).Source,
 (Join-Path $lfRoot '.lumaforge-local/tools/7zip/full/7z.exe'),
 (Join-Path $lfSharedRoot '.lumaforge-local/tools/7zip/full/7z.exe'),
 'C:/Program Files/7-Zip/7z.exe'
)
$lfSevenZip=$lfSevenZipCandidates | Where-Object {$_ -and (Test-Path -LiteralPath $_)} | Select-Object -First 1
if(-not $lfSevenZip){throw 'An authorized 7-Zip extractor is required for full NSIS audit; no automatic installation'}
$lfArchiveArgs=@('-c','from scripts.audit_nsis_payload import prepare_archive; import sys; prepare_archive(offline=sys.argv[1]=="1")', [string][int][bool]$Offline)
& $lfPython @lfArchiveArgs
if($LASTEXITCODE -ne 0){throw 'Pinned NSIS audit archive unavailable'}
$lfTools=Get-Content -LiteralPath packaging/build-environment.json -Raw | ConvertFrom-Json
if((node --version).Trim() -ne ('v'+$lfTools.node)){throw 'Use the recorded Node version; no automatic local tool installation'}
$lfDirty=[bool](git status --porcelain --untracked-files=normal)
if($lfDirty -and -not $AllowDirtyInternal){throw 'Commit reviewable sources first, or explicitly choose an internal dirty build'}
$lfOldPath=$env:PATH;$lfOldFlags=$env:CARGO_ENCODED_RUSTFLAGS;$lfOldJobs=$env:CARGO_BUILD_JOBS
try {
 $env:PATH="$env:USERPROFILE\.cargo\bin;$env:PATH"
 $env:CARGO_BUILD_JOBS='2'
 if((rustc --version) -notlike ('rustc '+$lfTools.rust+' *')){throw 'Use the recorded Rust version; no automatic local tool installation'}
 $env:CARGO_ENCODED_RUSTFLAGS="--remap-path-prefix=$env:USERPROFILE=/build-user"+[char]31+"--remap-path-prefix=$lfRoot=/src"
 if(-not $Offline){
  Push-Location apps/desktop/src-tauri
  try { & cargo fetch --locked; if($LASTEXITCODE -ne 0){throw 'Pinned Cargo inputs unavailable'} } finally {Pop-Location}
 }
 & $lfPython -m unittest discover -s tests_mvp -v
 if($LASTEXITCODE -ne 0){throw 'Beta tests failed'}
 & npm.cmd --prefix apps/web run build
 if($LASTEXITCODE -ne 0){throw 'Frontend build failed'}
 $lfRuntime=Join-Path $lfRoot ('.lumaforge-local/runtime-'+[guid]::NewGuid().ToString('N'))
 $lfBuildArgs=@('scripts/build_embedded_runtime.py',$lfRuntime)
 if($Offline){$lfBuildArgs+='--offline'}
 & $lfPython @lfBuildArgs
 if($LASTEXITCODE -ne 0){throw 'Hash/architecture/dependency origin gate failed'}
 & $lfPython scripts/audit_beta_licenses.py --runtime $lfRuntime
 if($LASTEXITCODE -ne 0){throw 'Dependency notice inventory failed'}
 & "$PSScriptRoot/audit_runtime_signatures.ps1" -Runtime $lfRuntime -Report .lumaforge-local/runtime-signatures.json
 & $lfPython scripts/audit_embedded_payload.py $lfRuntime .lumaforge-local/runtime-payload.json
 if($LASTEXITCODE -ne 0){throw 'Embedded payload privacy gate failed'}
 $lfBinaries=Join-Path $lfRoot 'apps/desktop/src-tauri/binaries'
 if(Test-Path -LiteralPath $lfBinaries){
  if([IO.Path]::GetFullPath($lfBinaries) -ne [IO.Path]::GetFullPath((Join-Path $lfRoot 'apps/desktop/src-tauri/binaries'))){throw 'Unsafe staging path'}
  if((Get-Item -LiteralPath $lfBinaries -Force).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Refusing linked staging'}
  if(-not(Test-Path -LiteralPath (Join-Path $lfBinaries '.generated-by-color-studio'))){throw 'Refusing unmarked staging'}
  if(Get-ChildItem -LiteralPath $lfBinaries -Force | Where-Object {$_.Name -notin @('.generated-by-color-studio','runtime')}){throw 'Unexpected staging files; preserve and inspect'}
  if(Get-ChildItem -LiteralPath $lfBinaries -Force -Recurse | Where-Object {$_.Attributes -band [IO.FileAttributes]::ReparsePoint}){throw 'Refusing linked staging contents'}
  & $lfPython -c 'from pathlib import Path; from scripts.build_embedded_runtime import verify_bundle; import sys; verify_bundle(Path(sys.argv[1]))' (Join-Path $lfBinaries 'runtime')
  if($LASTEXITCODE -ne 0){throw 'Existing staging changed; preserve it instead of replacing'}
  # Only this resolved, marked, fully verified generated tree is replaced.
  Remove-Item -LiteralPath $lfBinaries -Recurse -Force
 }
 New-Item -ItemType Directory -Path $lfBinaries | Out-Null
 Set-Content -LiteralPath (Join-Path $lfBinaries '.generated-by-color-studio') -Value 'Verified embedded runtime staging only'
 Copy-Item -LiteralPath $lfRuntime -Destination (Join-Path $lfBinaries 'runtime') -Recurse
 Push-Location apps/desktop
 try {
  & ../../apps/web/node_modules/.bin/tauri.cmd build --bundles nsis -- --locked --offline
  if($LASTEXITCODE -ne 0){throw 'Native installer build failed'}
 } finally {Pop-Location}
 & $lfPython scripts/audit_embedded_payload.py $lfRuntime .lumaforge-local/beta-payload-audit.json --native apps/desktop/src-tauri/target/release/color-studio-beta.exe
 if($LASTEXITCODE -ne 0){throw 'Native/payload privacy or import gate failed'}
 $lfConfig=Get-Content -LiteralPath apps/desktop/src-tauri/tauri.conf.json -Raw | ConvertFrom-Json
 $lfExpectedName=$lfConfig.productName+'_'+$lfConfig.version+'_x64-setup.exe'
 $lfInstaller=Get-Item -LiteralPath (Join-Path $lfRoot ('apps/desktop/src-tauri/target/release/bundle/nsis/'+$lfExpectedName))
 & $lfPython scripts/audit_nsis_payload.py $lfInstaller.FullName .lumaforge-local/beta-nsis-audit.json $lfSevenZip apps/desktop/src-tauri/target/release/color-studio-beta.exe .lumaforge-local/downloads/nsis-3.13.zip (Join-Path $env:LOCALAPPDATA 'tauri/NSIS')
 if($LASTEXITCODE -ne 0){throw 'Full NSIS provenance/architecture/privacy gate failed'}
 $lfArtifact=@{
  version=$lfConfig.version;file=$lfInstaller.Name;bytes=$lfInstaller.Length
  sha256=(Get-FileHash -LiteralPath $lfInstaller.FullName -Algorithm SHA256).Hash.ToLower()
  signature=(Get-AuthenticodeSignature -LiteralPath $lfInstaller.FullName).Status.ToString()
  source=(git rev-parse HEAD);dirty=$lfDirty
  python_runtime='PSF CPython3.14.10 embedded';build_python=(& $lfPython --version);rust=(& rustc --version);node=(& node --version)
  runtime_manifest_sha256=(Get-FileHash -LiteralPath (Join-Path $lfRuntime 'runtime-manifest.json') -Algorithm SHA256).Hash.ToLower()
  build_origin_gate_passed=$true;payload_audit_passed=$true
  webview2='Evergreen downloaded officially if absent; first install then requires Internet'
  status='internal_candidate_not_approved';windows_clean_install='not_tested'
  nsis_full_audit='passed';distribution_status='NO-GO_pending_clean_Windows_upgrade_QA_rights_and_owner_review'
 }
 $lfArtifact | ConvertTo-Json -Depth 5 | Set-Content -LiteralPath .lumaforge-local/beta-artifact.json -Encoding UTF8
 Write-Output 'Internal candidate built and NSIS audited. Do not distribute: clean-Windows/upgrade/editor/rights/owner gates remain.'
} finally {
 $env:PATH=$lfOldPath;$env:CARGO_ENCODED_RUSTFLAGS=$lfOldFlags;$env:CARGO_BUILD_JOBS=$lfOldJobs
}
