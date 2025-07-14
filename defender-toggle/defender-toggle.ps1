<#
.SYNOPSIS
  Interactive script to enable/disable Windows Defender Real-Time Protection.

.DESCRIPTION
  - Shows current status
  - Asks user for ON/OFF choice
  - Applies the change
  - Confirms after

.NOTES
  Must run as Administrator, and Tamper Protection must be OFF.
#>

# Admin check
if (-not ([Security.Principal.WindowsPrincipal] `
    [Security.Principal.WindowsIdentity]::GetCurrent() `
).IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)) {
    Write-Error "❌ Please run this script as Administrator."
    exit 1
}

# Ensure Defender module is loaded (built-in on Win10/11)
Import-Module Defender -ErrorAction SilentlyContinue

# Fetch current status
$currentPref = (Get-MpPreference).DisableRealtimeMonitoring
$currentSvc  = (Get-MpComputerStatus).RealTimeProtectionEnabled

Write-Host ""
Write-Host "=== Defender Real-Time Protection Status ==="
Write-Host ("  • DisableRealtimeMonitoring: {0}" -f $currentPref)
Write-Host ("  • RealTimeProtectionEnabled: {0}" -f $currentSvc)
Write-Host ""

# Ask user what to do
$action = Read-Host "Type 'OFF' to disable, 'ON' to enable, or 'Q' to quit"

switch ($action.ToUpper()) {
    'OFF' {
        if ($currentSvc -eq $false) {
            Write-Host "Already OFF. No action taken."
        } else {
            Set-MpPreference -DisableRealtimeMonitoring $true
            Write-Host "Attempted to DISABLE real-time protection."
        }
    }
    'ON' {
        if ($currentSvc -eq $true) {
            Write-Host "Already ON. No action taken."
        } else {
            Set-MpPreference -DisableRealtimeMonitoring $false
            Write-Host "Attempted to ENABLE real-time protection."
        }
    }
    'Q' {
        Write-Host "Quitting. No changes made."
        exit 0
    }
    Default {
        Write-Warning "Invalid input. Please type ON, OFF, or Q."
        exit 1
    }
}

# Confirm result
$afterPref = (Get-MpPreference).DisableRealtimeMonitoring
$afterSvc  = (Get-MpComputerStatus).RealTimeProtectionEnabled

Write-Host ""
Write-Host "=== Status After Change ==="
Write-Host ("  • DisableRealtimeMonitoring: {0}" -f $afterPref)
Write-Host ("  • RealTimeProtectionEnabled: {0}" -f $afterSvc)

if ($afterSvc -eq $false) {
    Write-Host "✅ Real-Time Protection is DISABLED."
} elseif ($afterSvc -eq $true) {
    Write-Host "✅ Real-Time Protection is ENABLED."
} else {
    Write-Host "⚠️ Status unknown."
}
