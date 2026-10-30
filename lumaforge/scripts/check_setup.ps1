# Comprueba el estado local sin instalar software ni crear recursos remotos.
$ErrorActionPreference = 'Continue'
$root = Split-Path -Parent $PSScriptRoot
Set-Location $root
Write-Host "LumaForge - comprobacion no destructiva" -ForegroundColor Cyan
foreach ($cmd in @('git', 'python', 'gh', 'codex')) {
    $found = Get-Command $cmd -ErrorAction SilentlyContinue
    if ($found) { Write-Host "OK ${cmd}: $($found.Source)" -ForegroundColor Green }
    else { Write-Host "FALTA $cmd" -ForegroundColor Yellow }
}
if (Get-Command python -ErrorAction SilentlyContinue) {
    python -m unittest discover -s tests -v
    python scripts/import_issues.py
}
if (Get-Command git -ErrorAction SilentlyContinue) {
    git status --short
    git remote -v
}
if (Get-Command gh -ErrorAction SilentlyContinue) {
    gh auth status
}
Write-Host "No se han hecho commits, pushes ni cambios remotos." -ForegroundColor Cyan

