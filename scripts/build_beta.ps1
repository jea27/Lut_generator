$ErrorActionPreference='Stop'
$lfRoot=Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $lfRoot
$env:PATH="$env:USERPROFILE\.cargo\bin;$env:PATH"
$env:CARGO_ENCODED_RUSTFLAGS="--remap-path-prefix=$env:USERPROFILE=/build-user"+[char]31+"--remap-path-prefix=$lfRoot=/src"
& ./.venv-mvp/Scripts/python.exe scripts/audit_beta_licenses.py
if($LASTEXITCODE -ne 0){throw 'Dependency notice inventory failed'}
& ./.venv-mvp/Scripts/python.exe -m unittest discover -s tests_mvp -v
if($LASTEXITCODE -ne 0){throw 'Beta tests failed'}
& npm.cmd --prefix apps/web run build
if($LASTEXITCODE -ne 0){throw 'Frontend build failed'}
& ./.venv-mvp/Scripts/python.exe -m PyInstaller --noconfirm --distpath .lumaforge-local/beta-build --workpath .lumaforge-local/beta-work packaging/ColorEngine.spec
if($LASTEXITCODE -ne 0){throw 'Engine bundle failed'}
$lfBinaries=Join-Path $lfRoot 'apps/desktop/src-tauri/binaries'
if(Test-Path -LiteralPath $lfBinaries){
 if(-not (Test-Path -LiteralPath (Join-Path $lfBinaries '.generated-by-color-studio'))){
   throw 'Refusing to replace unmarked binary staging directory'
 }
 if([IO.Path]::GetFullPath($lfBinaries) -ne [IO.Path]::GetFullPath((Join-Path $lfRoot 'apps/desktop/src-tauri/binaries'))){throw 'Unsafe staging path'}
 Remove-Item -LiteralPath $lfBinaries -Recurse -Force
}
New-Item -ItemType Directory -Force $lfBinaries | Out-Null
Set-Content -LiteralPath (Join-Path $lfBinaries '.generated-by-color-studio') -Value 'Generated binary staging only'
Copy-Item -LiteralPath '.lumaforge-local/beta-build/ColorEngine/ColorEngine.exe' -Destination (Join-Path $lfBinaries 'ColorEngine-x86_64-pc-windows-msvc.exe') -Force
Copy-Item -LiteralPath '.lumaforge-local/beta-build/ColorEngine/_internal' -Destination $lfBinaries -Recurse -Force
Push-Location apps/desktop
try {
 & ../../apps/web/node_modules/.bin/tauri.cmd build
 if($LASTEXITCODE -ne 0){throw 'Native installer build failed'}
} finally {Pop-Location}
$lfConfig=Get-Content -LiteralPath (Join-Path $lfRoot 'apps/desktop/src-tauri/tauri.conf.json') -Raw | ConvertFrom-Json
$lfExpectedName=$lfConfig.productName+'_'+$lfConfig.version+'_x64-setup.exe'
$lfInstaller=Get-Item -LiteralPath (Join-Path $lfRoot ('apps/desktop/src-tauri/target/release/bundle/nsis/'+$lfExpectedName))
if(-not $lfInstaller){throw 'Installer artifact not found'}
$lfArtifact=@{
 version=$lfConfig.version; file=$lfInstaller.Name; bytes=$lfInstaller.Length
 sha256=(Get-FileHash -LiteralPath $lfInstaller.FullName -Algorithm SHA256).Hash.ToLower()
 signature=(Get-AuthenticodeSignature -LiteralPath $lfInstaller.FullName).Status.ToString()
 source=(git rev-parse HEAD); dirty=[bool](git status --porcelain)
 python=(& ./.venv-mvp/Scripts/python.exe --version); rust=(& rustc --version); node=(& node --version)
 status='candidate_not_approved'; windows_clean_install='not_tested'
}
& ./.venv-mvp/Scripts/python.exe scripts/audit_beta_artifact.py .lumaforge-local/beta-build/ColorEngine .lumaforge-local/beta-payload-audit.json --native apps/desktop/src-tauri/target/release/color-studio-beta.exe
$lfPayload=Get-Content .lumaforge-local/beta-payload-audit.json -Raw | ConvertFrom-Json
$lfArtifact['payload_audit_passed']=$lfPayload.passed
$lfArtifact['distribution_status']='blocked_pending_QA_and_payload_review'
if($lfPayload.findings | Where-Object {$_.reason -in @('local_private_profile_path','secret_pattern','development_or_private_file')}){throw 'Payload contains a blocking private/development finding'}
$lfArtifact | ConvertTo-Json | Set-Content -LiteralPath (Join-Path $lfRoot '.lumaforge-local/beta-artifact.json') -Encoding UTF8
Write-Output 'Candidate installer built. This is not approval for distribution or sale.'
