<#
.SYNOPSIS
Monitors free space on the C: drive every 10 minutes.
Logs each check to a file in the script's current folder and alerts if space drops below 10 GB.

.DESCRIPTION
This script checks the C: drive for free space and logs the result every 10 minutes.
If space falls below 10 GB, it alerts in the console and in the log file.

🛠 No external tools required.
#>

# ---------------------------
# CONFIGURATION
# ---------------------------

$DriveLetter = "C"
$ThresholdGB = 10
$IntervalMinutes = 10

# Save log file in the same folder as this script
$ScriptDirectory = Split-Path -Parent $MyInvocation.MyCommand.Definition
$LogFile = Join-Path $ScriptDirectory "disk-monitor-log.txt"

# ---------------------------
# INTRODUCTION
# ---------------------------

Write-Host "`n=== Disk Space Monitor Started ===" -ForegroundColor Cyan
Write-Host "[Drive]: ${DriveLetter}:"
Write-Host "[Interval]: Every $IntervalMinutes minute(s)"
Write-Host "[Alert Threshold]: $ThresholdGB GB"
Write-Host "[Log File]: $LogFile`n"

# Confirm with user
$response = Read-Host "Start monitoring now? (Y/N)"
if ($response -ne 'Y' -and $response -ne 'y') {
    Write-Host "❌ Monitoring cancelled by user." -ForegroundColor Red
    exit
}

# ---------------------------
# MAIN MONITORING LOOP
# ---------------------------

while ($true) {
    $timestamp = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    $volume = Get-Volume -DriveLetter $DriveLetter -ErrorAction SilentlyContinue

    if ($null -eq $volume) {
        $errorMsg = "$timestamp | ERROR: Drive ${DriveLetter}: not found!"
        Write-Host "❌ $errorMsg" -ForegroundColor Red
        Add-Content -Path $LogFile -Value $errorMsg
    }
    else {
        $freeGB = [math]::Round($volume.SizeRemaining / 1GB, 2)
        $statusMsg = "$timestamp | Free space: $freeGB GB on drive ${DriveLetter}:"

        if ($freeGB -lt $ThresholdGB) {
            $statusMsg += "  << BELOW THRESHOLD!"
            Write-Host "$statusMsg" -ForegroundColor Yellow
        } else {
            Write-Host "$statusMsg" -ForegroundColor Green
        }

        Add-Content -Path $LogFile -Value $statusMsg
    }

    # Wait for next check
    Start-Sleep -Seconds ($IntervalMinutes * 60)
}
