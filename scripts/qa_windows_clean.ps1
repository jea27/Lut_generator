param([Parameter(Mandatory=$true)][string]$Installer,[Parameter(Mandatory=$true)][string]$ExpectedSha256,[string]$Output='beta-clean-preflight.json')
$ErrorActionPreference='Stop'
$lfResolved=(Resolve-Path -LiteralPath $Installer).Path
$lfHash=(Get-FileHash -LiteralPath $lfResolved -Algorithm SHA256).Hash.ToLower()
if($lfHash -ne $ExpectedSha256.ToLower()){throw 'Installer hash mismatch; do not install'}
$lfOs=Get-CimInstance Win32_OperatingSystem
$lfTools=@{}
foreach($lfName in @('python','node','cargo','git')){
 $lfCommand=Get-Command $lfName -ErrorAction SilentlyContinue
 $lfTools[$lfName]=if(-not $lfCommand){'absent'}elseif($lfCommand.Source -like '*WindowsApps*'){'WindowsApps_alias_not_verified_runtime'}else{'present_not_clean_baseline'}
}
$lfReport=@{
 schema='color-studio-clean-preflight-v1'; installer_sha256=$lfHash
 installer_bytes=(Get-Item -LiteralPath $lfResolved).Length
 signature=(Get-AuthenticodeSignature -LiteralPath $lfResolved).Status.ToString()
 windows_version=$lfOs.Version; architecture=$lfOs.OSArchitecture
 memory_gib=[math]::Round($lfOs.TotalVisibleMemorySize/1024/1024,1)
 development_tools=$lfTools; execution_status='preflight_only_not_tested'
 personal_identifiers_collected=$false
}
$lfReport | ConvertTo-Json -Depth 4 | Set-Content -LiteralPath $Output -Encoding UTF8
Write-Output 'Preflight saved. This does not install software or prove clean-Windows compatibility. Follow docs/BETA_QA_EXTERNA.md.'
