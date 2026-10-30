param([string]$PythonPath)
$ErrorActionPreference = 'Stop'
$lfRoot = Split-Path -Parent $PSScriptRoot
Set-Location -LiteralPath $lfRoot
if (-not $PythonPath) {
  $lfBundled = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
  if (Test-Path -LiteralPath $lfBundled) { $PythonPath = $lfBundled }
  else { $PythonPath = 'python' }
}
if (-not (Test-Path -LiteralPath '.venv-mvp/Scripts/python.exe')) {
  & $PythonPath -m venv .venv-mvp
  if ($LASTEXITCODE -ne 0) { throw 'No se pudo crear el entorno Python 3.12. Indica -PythonPath.' }
}
& ./.venv-mvp/Scripts/python.exe -m pip install -r requirements-mvp.txt
if ($LASTEXITCODE -ne 0) { throw 'Instalacion Python incompleta' }
Push-Location apps/web
try {
  & npm.cmd ci
  if ($LASTEXITCODE -ne 0) { throw 'Instalacion frontend incompleta' }
  & npm.cmd run build
  if ($LASTEXITCODE -ne 0) { throw 'Compilacion frontend incompleta' }
} finally { Pop-Location }
Write-Output 'Preparado. Ejecuta Iniciar-LumaForge.cmd y abre http://127.0.0.1:8790'
