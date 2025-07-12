<#
.DESCRIPTION
    - Detects and warns if browsers are running
    - Lets user choose which browser(s) to clean
    - Summarizes deleted file count and space saved
    - Supports all user profiles (Default, Profile 1, etc.)

.NOTES
    Author: Surge77
    Tested on: Windows 10/11
#>

function Confirm-Continue {
    param (
        [string]$Message = "Continue?"
    )
    $confirm = Read-Host "$Message (y/n)"
    if ($confirm -ne 'y') {
        Write-Host "Aborted by user." -ForegroundColor Red
        exit
    }
}

function Check-BrowserRunning {
    param (
        [string]$browser
    )

    $process = switch ($browser) {
        "Edge"   { "msedge" }
        "Chrome" { "chrome" }
    }

    if (Get-Process $process -ErrorAction SilentlyContinue) {
        Write-Warning "$browser is currently running. Please close it for full cleanup."
        Confirm-Continue -Message "Still want to continue with $browser cleanup?"
    }
}

function Get-ProfilePaths {
    param (
        [string]$basePath
    )

    if (-Not (Test-Path $basePath)) {
        return @()
    }

    Get-ChildItem -Path $basePath -Directory |
        Where-Object { $_.Name -match '^Default$|^Profile \d+$' } |
        ForEach-Object {
            @{
                Name = $_.Name
                FullPath = $_.FullName
            }
        }
}

function Clear-BrowserCache {
    param (
        [string]$browser,
        [string]$basePath
    )

    $profiles = Get-ProfilePaths -basePath $basePath
    if ($profiles.Count -eq 0) {
        Write-Warning "No $browser profiles found at $basePath"
        return
    }

    $foldersToClear = @("Cache", "GPUCache", "Code Cache")
    Write-Host "`nStarting cleanup for $browser..." -ForegroundColor Cyan

    foreach ($profile in $profiles) {
        $totalFiles = 0
        $totalSize = 0

        foreach ($folder in $foldersToClear) {
            $fullPath = Join-Path $profile.FullPath $folder
            if (Test-Path $fullPath) {
                $files = Get-ChildItem -Path $fullPath -Recurse -File -ErrorAction SilentlyContinue
                $totalFiles += $files.Count
                $totalSize += ($files | Measure-Object -Property Length -Sum).Sum
                $files | Remove-Item -Force -ErrorAction SilentlyContinue
            }
        }

        $sizeMB = [Math]::Round($totalSize / 1MB, 2)
        Write-Host "[$browser > $($profile.Name)] $totalFiles files deleted (~$sizeMB MB)"
    }
}

# ===== Main Script Starts Here =====
Write-Host "Browser Cache Cleaner - Edge & Chrome" -ForegroundColor Green

# Ask which browser(s) to clean
$choice = Read-Host "Clean Edge, Chrome, or Both? (e/c/b)"
$cleanEdge = $false
$cleanChrome = $false

switch ($choice.ToLower()) {
    "e" { $cleanEdge = $true }
    "c" { $cleanChrome = $true }
    "b" { $cleanEdge = $true; $cleanChrome = $true }
    default {
        Write-Warning "Invalid option. Please enter e, c, or b."
        exit
    }
}

# Always check running state
$edgeRunning   = Get-Process "msedge" -ErrorAction SilentlyContinue
$chromeRunning = Get-Process "chrome" -ErrorAction SilentlyContinue

# Display warnings *only* for selected browsers
if ($cleanEdge -and $edgeRunning) {
    Write-Warning "⚠️ Edge is currently running. Please close it for full cleanup."
    Confirm-Continue -Message "Still want to continue with Edge cleanup?"
}
if ($cleanChrome -and $chromeRunning) {
    Write-Warning "⚠️ Chrome is currently running. Please close it for full cleanup."
    Confirm-Continue -Message "Still want to continue with Chrome cleanup?"
}
# Confirm before deletion
Confirm-Continue -Message "Ready to delete cache files. Proceed?"

# Run cleanup
if ($cleanEdge) {
    $edgePath = Join-Path $env:LOCALAPPDATA "Microsoft\Edge\User Data"
    Clear-BrowserCache -browser "Edge" -basePath $edgePath
}

if ($cleanChrome) {
    $chromePath = Join-Path $env:LOCALAPPDATA "Google\Chrome\User Data"
    Clear-BrowserCache -browser "Chrome" -basePath $chromePath
}

Write-Host ""
Write-Host "Cleanup complete!" -ForegroundColor Green
