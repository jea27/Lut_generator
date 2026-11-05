param([string]$Output)
# Windows host inspection only. Never enables features, installs tools or starts a VM.
# Writes one sanitized receipt inside this checkout's ignored private QA directory.
$ErrorActionPreference='Stop'
$lfRoot=[IO.Path]::GetFullPath((Split-Path -Parent $PSScriptRoot))
$lfPrivate=Join-Path $lfRoot '.lumaforge-local'
if(-not $Output){$Output='.lumaforge-local/vm-preflight-'+[DateTime]::UtcNow.ToString('yyyyMMdd-HHmmss')+'-'+[guid]::NewGuid().ToString('N')+'.json'}
$lfTarget=if([IO.Path]::IsPathRooted($Output)){[IO.Path]::GetFullPath($Output)}else{[IO.Path]::GetFullPath((Join-Path $lfRoot $Output))}
$lfPrivatePrefix=$lfPrivate.TrimEnd('\','/')+[IO.Path]::DirectorySeparatorChar
if(-not $lfTarget.StartsWith($lfPrivatePrefix,[StringComparison]::OrdinalIgnoreCase)){throw 'Receipt must stay inside the checkout private QA directory'}
if(Test-Path -LiteralPath $lfTarget){throw 'Receipt already exists; choose a new name to preserve it'}
$lfParent=Split-Path -Parent $lfTarget
$lfWalk=$lfParent
while($lfWalk -and $lfWalk.Length -ge $lfRoot.Length){
    if(Test-Path -LiteralPath $lfWalk){
        if((Get-Item -LiteralPath $lfWalk -Force).Attributes -band [IO.FileAttributes]::ReparsePoint){throw 'Linked receipt directories are not supported'}
    }
    if($lfWalk -eq $lfRoot){break}
    $lfWalk=Split-Path -Parent $lfWalk
}

function Get-LfQueryFailure($LfException){
    $lfCode=[int32]$LfException.HResult
    $lfUnsigned=[BitConverter]::ToUInt32([BitConverter]::GetBytes($lfCode),0)
    $lfHex='0x'+$lfUnsigned.ToString('X8')
    $lfKind=if($lfHex -eq '0x800702E4'){'requires_elevation'}elseif($lfHex -eq '0x80070005'){'access_denied'}else{'query_unavailable'}
    # Never serialize exception messages/stack traces: they can contain profile paths.
    return [ordered]@{status=$lfKind;hresult=$lfHex;win32_low_word=($lfCode -band 65535)}
}

$lfOs=Get-CimInstance Win32_OperatingSystem
$lfComputer=Get-CimInstance Win32_ComputerSystem
$lfProcessors=@(Get-CimInstance Win32_Processor)
$lfProcessor=$lfProcessors | Select-Object -First 1
$lfDisks=@(Get-CimInstance Win32_LogicalDisk -Filter 'DriveType=3' | Sort-Object DeviceID | ForEach-Object {
    [ordered]@{drive=$_.DeviceID;size_gib=[math]::Round($_.Size/1GB,2);free_gib=[math]::Round($_.FreeSpace/1GB,2);file_system=$_.FileSystem}
})
$lfFreeRam=[math]::Round($lfOs.FreePhysicalMemory/1MB,2)
$lfTotalRam=[math]::Round($lfComputer.TotalPhysicalMemory/1GB,2)
$lfWorkspaceDrive=[IO.Path]::GetPathRoot($lfRoot).TrimEnd('\','/')
$lfWorkspaceDisk=$lfDisks | Where-Object {$_.drive -eq $lfWorkspaceDrive} | Select-Object -First 1

$lfFeatureNames=@('Microsoft-Hyper-V-All','Microsoft-Hyper-V','Microsoft-Hyper-V-Tools-All',
    'Microsoft-Hyper-V-Management-PowerShell','Microsoft-Hyper-V-Hypervisor',
    'Microsoft-Hyper-V-Services','Microsoft-Hyper-V-Management-Clients',
    'HypervisorPlatform','VirtualMachinePlatform','Containers-DisposableClientVM')
$lfWmi=[ordered]@{status='completed';features=@()}
try {
    $lfWmi.features=@(Get-CimInstance Win32_OptionalFeature | Where-Object {$_.Name -in $lfFeatureNames} | Sort-Object Name | ForEach-Object {
        $lfState=switch([int]$_.InstallState){1{'enabled'}2{'disabled'}3{'absent'}default{'unknown'}}
        [ordered]@{name=$_.Name;install_state=[int]$_.InstallState;state=$lfState}
    })
} catch {$lfWmi=Get-LfQueryFailure $_.Exception}

$lfDism=@()
foreach($lfName in @('Microsoft-Hyper-V-All','Microsoft-Hyper-V-Management-PowerShell','HypervisorPlatform','VirtualMachinePlatform')){
    try {
        $lfResult=Get-WindowsOptionalFeature -Online -FeatureName $lfName -ErrorAction Stop
        $lfDism+=[ordered]@{name=$lfName;status='completed';state=$lfResult.State.ToString()}
    } catch {
        $lfFailure=Get-LfQueryFailure $_.Exception
        $lfDism+=[ordered]@{name=$lfName;status=$lfFailure.status;hresult=$lfFailure.hresult;win32_low_word=$lfFailure.win32_low_word}
    }
}

$lfCommands=[ordered]@{}
foreach($lfName in @('Get-VM','New-VM','VBoxManage','vmrun','WindowsSandbox.exe')){
    $lfCommands[$lfName]=[bool](Get-Command $lfName -ErrorAction SilentlyContinue)
}
$lfPaths=[ordered]@{
    hyperv_module='C:/Windows/System32/WindowsPowerShell/v1.0/Modules/Hyper-V'
    vmconnect='C:/Windows/System32/vmconnect.exe'
    vmms='C:/Windows/System32/vmms.exe'
    hyperv_manager='C:/Windows/System32/virtmgmt.msc'
    virtualbox='C:/Program Files/Oracle/VirtualBox/VirtualBox.exe'
    vboxmanage='C:/Program Files/Oracle/VirtualBox/VBoxManage.exe'
    vmware_vmrun='C:/Program Files (x86)/VMware/VMware Workstation/vmrun.exe'
    windows_sandbox='C:/Windows/System32/WindowsSandbox.exe'
}
$lfPresent=[ordered]@{}
foreach($lfKey in $lfPaths.Keys){$lfPresent[$lfKey]=[bool](Test-Path -LiteralPath $lfPaths[$lfKey])}
$lfServices=@()
foreach($lfName in @('vmms','vmcompute','HvHost','hns')){
    $lfService=Get-Service -Name $lfName -ErrorAction SilentlyContinue
    if($lfService){$lfServices+=[ordered]@{name=$lfName;status=$lfService.Status.ToString();start_type=$lfService.StartType.ToString()}}
}
$lfNamespace=[ordered]@{status='completed';available=$false}
try {
    $lfNamespace.available=[bool](Get-CimInstance -Namespace root/virtualization/v2 -ClassName Msvm_VirtualSystemManagementService -ErrorAction Stop)
} catch {$lfNamespace=Get-LfQueryFailure $_.Exception;$lfNamespace.available=$false}
$lfVbs=[ordered]@{status='completed'}
try {
    $lfGuard=Get-CimInstance -Namespace root/Microsoft/Windows/DeviceGuard -ClassName Win32_DeviceGuard -ErrorAction Stop
    $lfVbs.virtualization_based_security_status=$lfGuard.VirtualizationBasedSecurityStatus
    $lfVbs.security_services_running=@($lfGuard.SecurityServicesRunning)
} catch {$lfVbs=Get-LfQueryFailure $_.Exception}

$lfHyperVManageable=$lfCommands['Get-VM'] -and $lfCommands['New-VM'] -and $lfNamespace.available
$lfRamHeadroom=8 # Engineering start gate for a 6GiB guest; not a Windows minimum.
$lfDiskBudget=268 # 96GiB VHDX + 96GiB checkpoint + 12GiB ISO + 64GiB host headroom.
$lfDiskSufficient=if($lfWorkspaceDisk){$lfWorkspaceDisk.free_gib -ge $lfDiskBudget}else{$null}
$lfReasons=@()
if(-not $lfHyperVManageable){$lfReasons+='hyperv_management_not_available_to_this_session'}
if($lfFreeRam -lt $lfRamHeadroom){$lfReasons+='available_ram_below_recommended_start_gate'}
if($lfDiskSufficient -ne $true){$lfReasons+='workspace_disk_budget_not_confirmed'}
if(@($lfDism | Where-Object {$_.status -eq 'requires_elevation'}).Count){$lfReasons+='feature_query_requires_operator_elevation_740'}

$lfReport=[ordered]@{
    schema='color-studio-vm-preflight-v1'
    collected_at=[DateTime]::UtcNow.ToString('o')
    scope='Read-only inspection of existing host, not VM creation or clean-Windows QA'
    os=[ordered]@{caption=$lfOs.Caption;version=$lfOs.Version;build=$lfOs.BuildNumber;architecture=$lfOs.OSArchitecture}
    hardware=[ordered]@{cpu_model=$lfProcessor.Name.Trim();physical_cores=($lfProcessors | Measure-Object NumberOfCores -Sum).Sum;
        logical_processors=$lfComputer.NumberOfLogicalProcessors;total_ram_gib=$lfTotalRam;available_ram_gib=$lfFreeRam}
    virtualization=[ordered]@{firmware_enabled=$lfProcessor.VirtualizationFirmwareEnabled;hypervisor_present=$lfComputer.HypervisorPresent;
        reported_vm_monitor_extensions=$lfProcessor.VMMonitorModeExtensions;reported_slat=$lfProcessor.SecondLevelAddressTranslationExtensions;
        interpretation='A detected hypervisor does not prove VM management is installed; detailed CPU flags can be unavailable under an active hypervisor'}
    fixed_disks=$lfDisks
    optional_features_wmi=$lfWmi
    optional_features_dism=$lfDism
    management=[ordered]@{hyperv_manageable=$lfHyperVManageable;commands_present=$lfCommands;standard_locations_present=$lfPresent;
        namespace=$lfNamespace;services=$lfServices;scope='PATH and standard locations only; custom portable installations are not ruled out'}
    existing_vbs=$lfVbs
    recommendation=[ordered]@{preferred='Microsoft Hyper-V on the existing Pro host, after operator setup';guest_generation=2;guest_vcpus=4;
        guest_ram_gib=6;guest_ram_if_sufficient_headroom_gib=8;recommended_available_ram_before_start_gib=$lfRamHeadroom;
        guest_disk='Dynamic VHDX file inside the workspace, never a physical disk';guest_disk_max_gib=96;
        disk_budget_with_one_checkpoint_gib=$lfDiskBudget;workspace_disk_budget_sufficient=$lfDiskSufficient;
        secure_boot=$true;virtual_tpm=$true;manager_and_resource_preflight_satisfied=($lfReasons.Count -eq 0);
        start_vm_now_recommended=($lfReasons.Count -eq 0);reason_codes=$lfReasons;
        limits='Positive preflight is not VM availability, guest licensing, ISO verification or a successful Windows test'}
    operator_requirements=@('Save work and release RAM before the next host check',
        'Enable or confirm Hyper-V with administrator control and any agreed restart; never disable VBS/protections',
        'Obtain a Microsoft ISO and a valid guest license/evaluation; complete registration/authentication personally',
        'Verify ISO hash before attaching it only to the virtual DVD drive')
    system_changes_performed=$false
    tools_installed=$false
    iso_downloaded=$false
    vm_created=$false
    clean_windows_verified=$false
    personal_identifiers_collected=$false
}
if(-not(Test-Path -LiteralPath $lfParent)){[IO.Directory]::CreateDirectory($lfParent) | Out-Null}
$lfJson=$lfReport | ConvertTo-Json -Depth 10
[IO.File]::WriteAllText($lfTarget,$lfJson+[Environment]::NewLine,(New-Object Text.UTF8Encoding($false)))
[ordered]@{receipt_file=[IO.Path]::GetFileName($lfTarget);hyperv_manageable=$lfHyperVManageable;
    available_ram_gib=$lfFreeRam;start_vm_now_recommended=$lfReport.recommendation.start_vm_now_recommended;
    reason_codes=$lfReasons;clean_windows_verified=$false} | ConvertTo-Json -Depth 4
