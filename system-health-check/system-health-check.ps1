#Requires -Version 5.1

<#
.SYNOPSIS
    Comprehensive System Health Check PowerShell Toolkit
    
.DESCRIPTION
    Generates detailed system health reports including CPU, memory, disk space, 
    battery status, event logs, OS info, uptime, and pending updates.
    
.PARAMETER Basic
    Run basic health check (CPU, Memory, Disk)
    
.PARAMETER Full
    Run comprehensive health check (all modules)
    
.PARAMETER Export
    Export report to files (.txt and .html)
    
.PARAMETER OutputPath
    Specify custom output directory (default: current directory)
    
.EXAMPLE
    .\system-health-check.ps1 -Basic
    
.EXAMPLE
    .\system-health-check.ps1 -Full -Export
    
.EXAMPLE
    .\system-health-check.ps1 -Full -Export -OutputPath "C:\Reports"
#>

param(
    [switch]$Basic,
    [switch]$Full,
    [switch]$Export,
    [string]$OutputPath = (Get-Location).Path
)

# Global variables
$Script:ReportData = @{}
$Script:HtmlContent = ""
$Script:TextContent = ""

# Helper Functions
function Write-Header {
    param([string]$Title)
    
    $separator = "=" * 60
    $header = @"

$separator
$Title
$separator

"@
    
    Write-Host $header -ForegroundColor Cyan
    $Script:TextContent += $header
    $Script:HtmlContent += "<h2>$Title</h2>`n"
}

function Write-SubHeader {
    param([string]$Title)
    
    $subHeader = "`n--- $Title ---`n"
    Write-Host $subHeader -ForegroundColor Yellow
    $Script:TextContent += $subHeader
    $Script:HtmlContent += "<h3>$Title</h3>`n"
}

function Write-Info {
    param([string]$Label, [string]$Value, [string]$Status = "")
    
    $line = "{0,-25}: {1} {2}" -f $Label, $Value, $Status
    Write-Host $line
    $Script:TextContent += "$line`n"
    
    $statusClass = switch ($Status) {
        { $_ -match "OK|Good|Healthy" } { "status-good" }
        { $_ -match "Warning|Medium" } { "status-warning" }
        { $_ -match "Critical|High|Error" } { "status-critical" }
        default { "" }
    }
    
    $Script:HtmlContent += "<p><strong>$Label" + ":</strong> $Value <span class='$statusClass'>$Status</span></p>`n"
}

# Core Health Check Modules
function Get-SystemInfo {
    Write-Header "System Information"
    
    try {
        $os = Get-CimInstance -ClassName Win32_OperatingSystem
        $computer = Get-CimInstance -ClassName Win32_ComputerSystem
        $bios = Get-CimInstance -ClassName Win32_BIOS
        
        Write-Info "Computer Name" $env:COMPUTERNAME
        Write-Info "OS Name" $os.Caption
        Write-Info "OS Version" $os.Version
        Write-Info "OS Architecture" $os.OSArchitecture
        Write-Info "Manufacturer" $computer.Manufacturer
        Write-Info "Model" $computer.Model
        Write-Info "BIOS Version" $bios.SMBIOSBIOSVersion
        
        $uptime = (Get-Date) - $os.LastBootUpTime
        $uptimeString = "{0} days, {1} hours, {2} minutes" -f $uptime.Days, $uptime.Hours, $uptime.Minutes
        Write-Info "System Uptime" $uptimeString
        
        $Script:ReportData.SystemInfo = @{
            ComputerName = $env:COMPUTERNAME
            OSName = $os.Caption
            OSVersion = $os.Version
            Uptime = $uptimeString
        }
    }
    catch {
        Write-Warning "Error retrieving system information: $($_.Exception.Message)"
    }
}

function Get-CPUInfo {
    Write-Header "CPU Information & Usage"
    
    try {
        $cpu = Get-CimInstance -ClassName Win32_Processor
        $cpuUsage = (Get-Counter "\Processor(_Total)\% Processor Time" -SampleInterval 1 -MaxSamples 3 | 
                    Select-Object -ExpandProperty CounterSamples | 
                    Measure-Object -Property CookedValue -Average).Average
        
        Write-Info "Processor" $cpu.Name
        Write-Info "Cores" $cpu.NumberOfCores
        Write-Info "Logical Processors" $cpu.NumberOfLogicalProcessors
        Write-Info "Max Clock Speed" "$($cpu.MaxClockSpeed) MHz"
        
        $cpuUsageRounded = [math]::Round($cpuUsage, 2)
        $cpuStatus = if ($cpuUsageRounded -lt 70) { "(Good)" } 
                    elseif ($cpuUsageRounded -lt 90) { "(Warning)" } 
                    else { "(Critical)" }
        
        Write-Info "Current CPU Usage" "$cpuUsageRounded%" $cpuStatus
        
        $Script:ReportData.CPU = @{
            Name = $cpu.Name
            Usage = $cpuUsageRounded
            Status = $cpuStatus
        }
    }
    catch {
        Write-Warning "Error retrieving CPU information: $($_.Exception.Message)"
    }
}

function Get-MemoryInfo {
    Write-Header "Memory Information"
    
    try {
        $os = Get-CimInstance -ClassName Win32_OperatingSystem
        $totalMemoryGB = [math]::Round($os.TotalVisibleMemorySize / 1MB, 2)
        $freeMemoryGB = [math]::Round($os.FreePhysicalMemory / 1MB, 2)
        $usedMemoryGB = $totalMemoryGB - $freeMemoryGB
        $memoryUsagePercent = [math]::Round(($usedMemoryGB / $totalMemoryGB) * 100, 2)
        
        $memoryStatus = if ($memoryUsagePercent -lt 80) { "(Good)" } 
                       elseif ($memoryUsagePercent -lt 95) { "(Warning)" } 
                       else { "(Critical)" }
        
        Write-Info "Total Memory" "$totalMemoryGB GB"
        Write-Info "Used Memory" "$usedMemoryGB GB"
        Write-Info "Free Memory" "$freeMemoryGB GB"
        Write-Info "Memory Usage" "$memoryUsagePercent%" $memoryStatus
        
        $Script:ReportData.Memory = @{
            Total = $totalMemoryGB
            Used = $usedMemoryGB
            UsagePercent = $memoryUsagePercent
            Status = $memoryStatus
        }
    }
    catch {
        Write-Warning "Error retrieving memory information: $($_.Exception.Message)"
    }
}

function Get-DiskInfo {
    Write-Header "Disk Space Information"
    
    try {
        $disks = Get-CimInstance -ClassName Win32_LogicalDisk | Where-Object { $_.DriveType -eq 3 }
        
        foreach ($disk in $disks) {
            Write-SubHeader "Drive $($disk.DeviceID)"
            
            $totalSizeGB = [math]::Round($disk.Size / 1GB, 2)
            $freeSizeGB = [math]::Round($disk.FreeSpace / 1GB, 2)
            $usedSizeGB = $totalSizeGB - $freeSizeGB
            $usagePercent = [math]::Round(($usedSizeGB / $totalSizeGB) * 100, 2)
            
            $diskStatus = if ($usagePercent -lt 80) { "(Good)" } 
                         elseif ($usagePercent -lt 95) { "(Warning)" } 
                         else { "(Critical)" }
            
            Write-Info "Total Size" "$totalSizeGB GB"
            Write-Info "Used Space" "$usedSizeGB GB"
            Write-Info "Free Space" "$freeSizeGB GB"
            Write-Info "Usage Percentage" "$usagePercent%" $diskStatus
        }
        
        $Script:ReportData.Disks = $disks | ForEach-Object {
            @{
                Drive = $_.DeviceID
                TotalGB = [math]::Round($_.Size / 1GB, 2)
                FreeGB = [math]::Round($_.FreeSpace / 1GB, 2)
                UsagePercent = [math]::Round((($_.Size - $_.FreeSpace) / $_.Size) * 100, 2)
            }
        }
    }
    catch {
        Write-Warning "Error retrieving disk information: $($_.Exception.Message)"
    }
}

function Get-BatteryInfo {
    Write-Header "Battery Information"
    
    try {
        $battery = Get-CimInstance -ClassName Win32_Battery
        
        if ($battery) {
            foreach ($bat in $battery) {
                Write-Info "Battery Name" $bat.Name
                Write-Info "Charge Status" $(
                    switch ($bat.BatteryStatus) {
                        1 { "Other" }
                        2 { "Unknown" }
                        3 { "Fully Charged" }
                        4 { "Low" }
                        5 { "Critical" }
                        6 { "Charging" }
                        7 { "Charging and High" }
                        8 { "Charging and Low" }
                        9 { "Charging and Critical" }
                        10 { "Undefined" }
                        11 { "Partially Charged" }
                        default { "Unknown" }
                    }
                )
                
                if ($bat.EstimatedChargeRemaining) {
                    $chargeStatus = if ($bat.EstimatedChargeRemaining -gt 50) { "(Good)" }
                                   elseif ($bat.EstimatedChargeRemaining -gt 20) { "(Warning)" }
                                   else { "(Critical)" }
                    Write-Info "Charge Remaining" "$($bat.EstimatedChargeRemaining)%" $chargeStatus
                }
            }
            
            $Script:ReportData.Battery = @{
                Present = $true
                ChargeRemaining = $battery[0].EstimatedChargeRemaining
            }
        } else {
            Write-Info "Battery Status" "No battery detected (Desktop system)"
            $Script:ReportData.Battery = @{ Present = $false }
        }
    }
    catch {
        Write-Warning "Error retrieving battery information: $($_.Exception.Message)"
    }
}

function Get-EventLogSummary {
    Write-Header "Event Log Summary (Last 24 Hours)"
    
    try {
        $last24Hours = (Get-Date).AddHours(-24)
        
        # System Log
        Write-SubHeader "System Log"
        $systemEvents = Get-WinEvent -FilterHashtable @{LogName='System'; StartTime=$last24Hours} -ErrorAction SilentlyContinue
        if ($systemEvents) {
            $systemCritical = ($systemEvents | Where-Object { $_.LevelDisplayName -eq "Critical" }).Count
            $systemError = ($systemEvents | Where-Object { $_.LevelDisplayName -eq "Error" }).Count
            $systemWarning = ($systemEvents | Where-Object { $_.LevelDisplayName -eq "Warning" }).Count
            
            Write-Info "Critical Events" $systemCritical $(if ($systemCritical -gt 0) { "(Critical)" } else { "(Good)" })
            Write-Info "Error Events" $systemError $(if ($systemError -gt 5) { "(Warning)" } elseif ($systemError -gt 0) { "(Medium)" } else { "(Good)" })
            Write-Info "Warning Events" $systemWarning $(if ($systemWarning -gt 10) { "(Warning)" } else { "(Good)" })
        } else {
            Write-Info "System Events" "No events found"
        }
        
        # Application Log
        Write-SubHeader "Application Log"
        $appEvents = Get-WinEvent -FilterHashtable @{LogName='Application'; StartTime=$last24Hours} -ErrorAction SilentlyContinue
        if ($appEvents) {
            $appCritical = ($appEvents | Where-Object { $_.LevelDisplayName -eq "Critical" }).Count
            $appError = ($appEvents | Where-Object { $_.LevelDisplayName -eq "Error" }).Count
            $appWarning = ($appEvents | Where-Object { $_.LevelDisplayName -eq "Warning" }).Count
            
            Write-Info "Critical Events" $appCritical $(if ($appCritical -gt 0) { "(Critical)" } else { "(Good)" })
            Write-Info "Error Events" $appError $(if ($appError -gt 10) { "(Warning)" } elseif ($appError -gt 0) { "(Medium)" } else { "(Good)" })
            Write-Info "Warning Events" $appWarning $(if ($appWarning -gt 20) { "(Warning)" } else { "(Good)" })
        } else {
            Write-Info "Application Events" "No events found"
        }
        
        $Script:ReportData.EventLogs = @{
            SystemCritical = if ($systemEvents) { $systemCritical } else { 0 }
            SystemErrors = if ($systemEvents) { $systemError } else { 0 }
            AppCritical = if ($appEvents) { $appCritical } else { 0 }
            AppErrors = if ($appEvents) { $appError } else { 0 }
        }
    }
    catch {
        Write-Warning "Error retrieving event log information: $($_.Exception.Message)"
    }
}

function Get-PendingUpdates {
    Write-Header "Windows Update Status"
    
    try {
        # Try using Windows Update API
        $updateSession = New-Object -ComObject Microsoft.Update.Session -ErrorAction SilentlyContinue
        if ($updateSession) {
            $updateSearcher = $updateSession.CreateUpdateSearcher()
            $searchResult = $updateSearcher.Search("IsInstalled=0")
            
            if ($searchResult.Updates.Count -gt 0) {
                Write-Info "Pending Updates" $searchResult.Updates.Count $(if ($searchResult.Updates.Count -gt 10) { "(Warning)" } else { "(Medium)" })
                
                Write-SubHeader "Update Details"
                $updateList = @()
                foreach ($update in $searchResult.Updates) {
                    $updateInfo = "$($update.Title)"
                    Write-Info "Update" $updateInfo
                    $updateList += $updateInfo
                }
                
                $Script:ReportData.Updates = @{
                    PendingCount = $searchResult.Updates.Count
                    Updates = $updateList
                }
            } else {
                Write-Info "Pending Updates" "0" "(Good)"
                $Script:ReportData.Updates = @{ PendingCount = 0 }
            }
        } else {
            # Fallback method using Get-WindowsUpdate if available
            if (Get-Command Get-WindowsUpdate -ErrorAction SilentlyContinue) {
                $updates = Get-WindowsUpdate -MicrosoftUpdate
                Write-Info "Pending Updates" $updates.Count $(if ($updates.Count -gt 10) { "(Warning)" } else { "(Medium)" })
                $Script:ReportData.Updates = @{ PendingCount = $updates.Count }
            } else {
                Write-Info "Update Status" "Unable to check (requires elevated permissions or PSWindowsUpdate module)"
                $Script:ReportData.Updates = @{ PendingCount = "Unknown" }
            }
        }
    }
    catch {
        Write-Warning "Error checking for pending updates: $($_.Exception.Message)"
        Write-Info "Update Status" "Unable to check updates"
        $Script:ReportData.Updates = @{ PendingCount = "Error" }
    }
}

function Get-NetworkInfo {
    Write-Header "Network Information"
    
    try {
        $adapters = Get-NetAdapter | Where-Object { $_.Status -eq "Up" }
        
        foreach ($adapter in $adapters) {
            Write-SubHeader $adapter.Name
            Write-Info "Interface Description" $adapter.InterfaceDescription
            $linkSpeedMbps = if ($adapter.LinkSpeed -match '^\d+$') { 
                [math]::Round($adapter.LinkSpeed / 1MB, 0) 
            } else { 
                $adapter.LinkSpeed 
            }
            Write-Info "Link Speed" "$linkSpeedMbps"
            Write-Info "Status" $adapter.Status $(if ($adapter.Status -eq "Up") { "(Good)" } else { "(Warning)" })
            
            # Get IP configuration
            $ipConfig = Get-NetIPAddress -InterfaceIndex $adapter.InterfaceIndex -AddressFamily IPv4 -ErrorAction SilentlyContinue
            if ($ipConfig) {
                Write-Info "IP Address" $ipConfig.IPAddress
            }
        }
        
        # Test internet connectivity
        $internetTest = Test-NetConnection -ComputerName "8.8.8.8" -Port 53 -InformationLevel Quiet
        Write-Info "Internet Connectivity" $(if ($internetTest) { "Connected" } else { "Disconnected" }) $(if ($internetTest) { "(Good)" } else { "(Critical)" })
        
        $Script:ReportData.Network = @{
            ActiveAdapters = $adapters.Count
            InternetConnected = $internetTest
        }
    }
    catch {
        Write-Warning "Error retrieving network information: $($_.Exception.Message)"
    }
}

function Get-ServiceStatus {
    Write-Header "Critical Services Status"
    
    try {
        $criticalServices = @(
            "Winmgmt",      # Windows Management Instrumentation
            "EventLog",     # Windows Event Log
            "Spooler",      # Print Spooler
            "Themes",       # Themes
            "AudioSrv",     # Windows Audio
            "BITS",         # Background Intelligent Transfer Service
            "Dhcp",         # DHCP Client
            "Dnscache",     # DNS Client
            "LanmanServer", # Server
            "LanmanWorkstation" # Workstation
        )
        
        foreach ($serviceName in $criticalServices) {
            $service = Get-Service -Name $serviceName -ErrorAction SilentlyContinue
            if ($service) {
                $status = if ($service.Status -eq "Running") { "(Good)" } else { "(Warning)" }
                Write-Info $service.DisplayName $service.Status $status
            }
        }
        
        $runningServices = (Get-Service | Where-Object { $_.Status -eq "Running" }).Count
        $stoppedServices = (Get-Service | Where-Object { $_.Status -eq "Stopped" }).Count
        
        Write-SubHeader "Service Summary"
        Write-Info "Running Services" $runningServices
        Write-Info "Stopped Services" $stoppedServices
        
        $Script:ReportData.Services = @{
            RunningCount = $runningServices
            StoppedCount = $stoppedServices
        }
    }
    catch {
        Write-Warning "Error retrieving service information: $($_.Exception.Message)"
    }
}

# Export Functions
function Export-TextReport {
    param([string]$OutputPath)
    
    $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $filename = "SystemHealthReport_$timestamp.txt"
    $filepath = Join-Path $OutputPath $filename
    
    $header = @"
SYSTEM HEALTH REPORT
Generated: $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")
Computer: $env:COMPUTERNAME
$("=" * 60)
"@
    
    $fullContent = $header + "`n" + $Script:TextContent
    $fullContent | Out-File -FilePath $filepath -Encoding UTF8
    
    Write-Host "`nText report exported to: $filepath" -ForegroundColor Green
    return $filepath
}

function Export-HtmlReport {
    param([string]$OutputPath)
    
    $timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
    $filename = "SystemHealthReport_$timestamp.html"
    $filepath = Join-Path $OutputPath $filename
    
    $htmlTemplate = @"
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>System Health Report - $env:COMPUTERNAME</title>
    <style>
        body { font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; margin: 20px; background-color: #f5f5f5; }
        .container { max-width: 1200px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 0 10px rgba(0,0,0,0.1); }
        h1 { color: #2c3e50; text-align: center; border-bottom: 3px solid #3498db; padding-bottom: 10px; }
        h2 { color: #34495e; border-left: 4px solid #3498db; padding-left: 15px; margin-top: 30px; }
        h3 { color: #7f8c8d; margin-top: 20px; }
        p { margin: 5px 0; line-height: 1.6; }
        .status-good { color: #27ae60; font-weight: bold; }
        .status-warning { color: #f39c12; font-weight: bold; }
        .status-critical { color: #e74c3c; font-weight: bold; }
        .header-info { background-color: #ecf0f1; padding: 15px; border-radius: 5px; margin-bottom: 20px; }
        .summary-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }
        .summary-card { background-color: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid #3498db; }
        .footer { text-align: center; margin-top: 30px; color: #7f8c8d; font-size: 0.9em; }
    </style>
</head>
<body>
    <div class="container">
        <h1>System Health Report</h1>
        <div class="header-info">
            <p><strong>Computer:</strong> $env:COMPUTERNAME</p>
            <p><strong>Generated:</strong> $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")</p>
            <p><strong>Report Type:</strong> $(if ($Full) { "Full Report" } else { "Basic Report" })</p>
        </div>
        
        $Script:HtmlContent
        
        <div class="footer">
            <p>Report generated by PowerShell System Health Check Toolkit</p>
        </div>
    </div>
</body>
</html>
"@
    
    $htmlTemplate | Out-File -FilePath $filepath -Encoding UTF8
    
    Write-Host "HTML report exported to: $filepath" -ForegroundColor Green
    return $filepath
}

# Main execution logic
function Start-HealthCheck {
    Write-Host "PowerShell System Health Check Toolkit" -ForegroundColor Cyan
    Write-Host "=======================================" -ForegroundColor Cyan
    Write-Host "Started: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Gray
    
    # Initialize content
    $Script:TextContent = ""
    $Script:HtmlContent = ""
    
    # Determine what checks to run
    if (-not $Basic -and -not $Full) {
        Write-Host "No mode specified. Use -Basic or -Full parameter." -ForegroundColor Yellow
        Write-Host "Running basic check by default..." -ForegroundColor Yellow
        $Basic = $true
    }
    
    # Basic checks (always included)
    Get-SystemInfo
    Get-CPUInfo
    Get-MemoryInfo
    Get-DiskInfo
    
    # Full checks (additional modules)
    if ($Full) {
        Get-BatteryInfo
        Get-EventLogSummary
        Get-PendingUpdates
        Get-NetworkInfo
        Get-ServiceStatus
    }
    
    # Export reports if requested
    if ($Export) {
        Write-Host "`nExporting reports..." -ForegroundColor Yellow
        
        if (-not (Test-Path $OutputPath)) {
            New-Item -ItemType Directory -Path $OutputPath -Force | Out-Null
        }
        
        $textFile = Export-TextReport -OutputPath $OutputPath
        $htmlFile = Export-HtmlReport -OutputPath $OutputPath
        
        Write-Host "`nReports exported successfully!" -ForegroundColor Green
        Write-Host "Text Report: $textFile" -ForegroundColor Gray
        Write-Host "HTML Report: $htmlFile" -ForegroundColor Gray
    }
    
    Write-Host "`nHealth check completed at $(Get-Date -Format 'HH:mm:ss')" -ForegroundColor Green
}

# Script entry point
try {
    Start-HealthCheck
}
catch {
    Write-Error "An error occurred during health check: $($_.Exception.Message)"
    exit 1
}