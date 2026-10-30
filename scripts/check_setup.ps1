# Auditoria local: no instala software ni modifica recursos remotos.
param([string]$PythonPath, [string]$GhPath, [switch]$SkipGitHub)
$ErrorActionPreference = 'Stop'
$script:failed = $false
function Invoke-Check {
    param([string]$Executable, [string[]]$Arguments)
    try {
        & $Executable @Arguments
        if ($LASTEXITCODE -ne 0) { $script:failed = $true }
    } catch { Write-Warning $_.Exception.Message; $script:failed = $true }
}
Push-Location (Split-Path -Parent $PSScriptRoot)
try {
    if (!$PythonPath) {
        $candidate = Get-Command python -ErrorAction SilentlyContinue
        if ($candidate -and $candidate.Source -notlike '*\WindowsApps\*') {
            $PythonPath = $candidate.Source
        } else {
            $bundled = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'
            if (Test-Path -LiteralPath $bundled) { $PythonPath = $bundled }
        }
    }
    if ($PythonPath) {
        Write-Host "Python: $PythonPath"
        Invoke-Check $PythonPath @('--version')
        Invoke-Check $PythonPath @('-m', 'unittest', 'discover', '-s', 'tests', '-v')
        Invoke-Check $PythonPath @('scripts/import_issues.py')
    } else { Write-Warning 'Falta Python funcional: usa -PythonPath'; $script:failed = $true }
    Invoke-Check 'node' @('--version')
    Invoke-Check 'node' @('--check', 'site/app.js')
    Invoke-Check 'git' @('--version')
    Invoke-Check 'git' @('status', '--short', '--branch')
    Invoke-Check 'git' @('remote', '-v')
    if (!$SkipGitHub) {
        if (!$GhPath) {
            $candidate = Get-Command gh -ErrorAction SilentlyContinue
            if ($candidate) { $GhPath = $candidate.Source }
            elseif (Test-Path -LiteralPath (Join-Path $env:ProgramFiles 'GitHub CLI\gh.exe')) {
                $GhPath = Join-Path $env:ProgramFiles 'GitHub CLI\gh.exe'
            }
        }
        if ($GhPath) {
            Invoke-Check $GhPath @('--version')
            Invoke-Check $GhPath @('auth', 'status')
        } else { Write-Warning 'gh no disponible; autenticacion sin verificar'; $script:failed = $true }
    } else { Write-Host 'GitHub omitido expresamente: autenticacion sin verificar.' }
} finally { Pop-Location }
Write-Host 'Sin instalaciones ni escrituras remotas.'
if ($script:failed) { exit 1 }
exit 0
