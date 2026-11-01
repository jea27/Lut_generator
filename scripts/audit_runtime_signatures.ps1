param([Parameter(Mandatory=$true)][string]$Runtime,[Parameter(Mandatory=$true)][string]$Report)
$ErrorActionPreference='Stop'
$lfRuntime=(Resolve-Path -LiteralPath $Runtime).Path
$lfManifest=Get-Content -LiteralPath (Join-Path $lfRuntime 'runtime-manifest.json') -Raw | ConvertFrom-Json
$lfRows=@()
foreach($lfEntry in $lfManifest.native_files){
 $lfFile=Join-Path $lfRuntime $lfEntry.file
 if((Get-FileHash -LiteralPath $lfFile -Algorithm SHA256).Hash.ToLower() -ne $lfEntry.sha256){throw 'Native signature input hash mismatch'}
 $lfSignature=Get-AuthenticodeSignature -LiteralPath $lfFile
 $lfRequired=if($lfEntry.file -in @('python.exe','pythonw.exe','python314.dll','python3.dll')){'Python Software Foundation'}elseif($lfEntry.file -match '(^|/)(vcruntime140[^/]*|msvcp140[^/]*)\.dll$'){'Microsoft'}else{''}
 if($lfRequired -and ($lfSignature.Status.ToString() -ne 'Valid' -or $lfSignature.SignerCertificate.Subject -notlike "*$lfRequired*")){throw 'Required PSF/Microsoft signature not valid'}
 $lfRows+=@{file=$lfEntry.file;sha256=$lfEntry.sha256;status=$lfSignature.Status.ToString();publisher=$lfSignature.SignerCertificate.Subject;file_version=(Get-Item -LiteralPath $lfFile).VersionInfo.FileVersion;required_publisher=$lfRequired}
}
@{schema='color-studio-native-signatures-v1';required_signatures_passed=$true;unsigned_wheels='Hash/origin verified separately; no claim that every upstream wheel is signed';files=$lfRows} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $Report -Encoding UTF8
Write-Output 'Native signatures checked without changing Windows security settings.'
