# ===================================================================
# Clean Temp Files Script (cleantemp.ps1)
# Author: PowerShell Utility Script
# Description: Safely deletes temporary files from C:\Windows\Temp
# with user confirmation and detailed logging
# ===================================================================

# Set strict mode for better error handling
Set-StrictMode -Version Latest

# Define constants
$TEMP_PATH = "C:\Windows\Temp"
$LOG_FILE = "temp_cleanup_log.txt"
$TIMESTAMP = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

# Function to write to both console and log file
function Write-Log {
    param(
        [string]$Message,
        [string]$Level = "INFO"
    )
    
    $LogEntry = "[$TIMESTAMP] [$Level] $Message"
    Write-Host $LogEntry
    Add-Content -Path $LOG_FILE -Value $LogEntry
}

# Function to display script header
function Show-Header {
    Clear-Host
    Write-Host "=====================================================" -ForegroundColor Cyan
    Write-Host "       Windows Temp Files Cleanup Utility          " -ForegroundColor Cyan
    Write-Host "=====================================================" -ForegroundColor Cyan
    Write-Host ""
}

# Function to check if running as administrator
function Test-Administrator {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Function to get folder size in MB
function Get-FolderSize {
    param([string]$Path)
    
    try {
        $size = (Get-ChildItem -Path $Path -Recurse -File -ErrorAction SilentlyContinue | 
                 Measure-Object -Property Length -Sum).Sum
        return [math]::Round($size / 1MB, 2)
    }
    catch {
        return 0
    }
}

# Function to safely delete files and folders
function Remove-TempItems {
    param([string]$Path)
    
    $deletedCount = 0
    $errorCount = 0
    $totalSize = 0
    
    Write-Log "Starting cleanup of: $Path"
    
    try {
        # Get all items in the temp directory
        $items = Get-ChildItem -Path $Path -Force -ErrorAction SilentlyContinue
        
        if ($items.Count -eq 0) {
            Write-Log "No items found in temp directory" "INFO"
            return @{DeletedCount = 0; ErrorCount = 0; TotalSize = 0}
        }
        
        Write-Host "`nProcessing $($items.Count) items..." -ForegroundColor Yellow
        
        foreach ($item in $items) {
            try {
                # Calculate size before deletion
                if ($item.PSIsContainer) {
                    $itemSize = Get-FolderSize -Path $item.FullName
                } else {
                    $itemSize = [math]::Round($item.Length / 1MB, 2)
                }
                
                # Attempt to delete the item
                Remove-Item -Path $item.FullName -Recurse -Force -ErrorAction Stop
                
                # Log successful deletion
                $itemType = if ($item.PSIsContainer) { "Folder" } else { "File" }
                Write-Log "Deleted $itemType`: $($item.Name) (Size: $itemSize MB)" "SUCCESS"
                
                $deletedCount++
                $totalSize += $itemSize
                
                # Show progress
                Write-Host "." -NoNewline -ForegroundColor Green
            }
            catch {
                Write-Log "Failed to delete: $($item.Name) - Error: $($_.Exception.Message)" "ERROR"
                $errorCount++
                Write-Host "X" -NoNewline -ForegroundColor Red
            }
        }
    }
    catch {
        Write-Log "Error accessing temp directory: $($_.Exception.Message)" "ERROR"
        $errorCount++
    }
    
    Write-Host "" # New line after progress indicators
    
    return @{
        DeletedCount = $deletedCount
        ErrorCount = $errorCount
        TotalSize = $totalSize
    }
}

# Function to display cleanup summary
function Show-Summary {
    param($Result)
    
    Write-Host "`n=====================================================" -ForegroundColor Cyan
    Write-Host "                CLEANUP SUMMARY                     " -ForegroundColor Cyan
    Write-Host "=====================================================" -ForegroundColor Cyan
    Write-Host "Items Successfully Deleted: $($Result.DeletedCount)" -ForegroundColor Green
    Write-Host "Items Failed to Delete: $($Result.ErrorCount)" -ForegroundColor $(if($Result.ErrorCount -gt 0){"Red"}else{"Green"})
    Write-Host "Total Space Freed: $($Result.TotalSize) MB" -ForegroundColor Green
    Write-Host "Log File Location: $((Get-Location).Path)\$LOG_FILE" -ForegroundColor Cyan
    Write-Host "=====================================================" -ForegroundColor Cyan
}

# Main script execution
try {
    # Display header
    Show-Header
    
    # Initialize log file
    Write-Log "=== Temp Cleanup Script Started ===" "INFO"
    
    # Check if running as administrator
    if (-not (Test-Administrator)) {
        Write-Host "WARNING: Not running as Administrator!" -ForegroundColor Yellow
        Write-Host "Some files may not be deletable without admin privileges." -ForegroundColor Yellow
        Write-Host ""
        
        $continue = Read-Host "Do you want to continue anyway? (y/N)"
        if ($continue -notmatch '^[Yy]') {
            Write-Log "Script cancelled by user - insufficient privileges" "INFO"
            exit 0
        }
    }
    
    # Check if temp directory exists
    if (-not (Test-Path -Path $TEMP_PATH)) {
        Write-Host "ERROR: Temp directory not found: $TEMP_PATH" -ForegroundColor Red
        Write-Log "Temp directory not found: $TEMP_PATH" "ERROR"
        exit 1
    }
    
    # Get initial statistics
    $initialSize = Get-FolderSize -Path $TEMP_PATH
    $itemCount = (Get-ChildItem -Path $TEMP_PATH -Force -ErrorAction SilentlyContinue).Count
    
    # Display current status
    Write-Host "Current Status:" -ForegroundColor Yellow
    Write-Host "  Temp Directory: $TEMP_PATH" -ForegroundColor White
    Write-Host "  Items Found: $itemCount" -ForegroundColor White
    Write-Host "  Current Size: $initialSize MB" -ForegroundColor White
    Write-Host ""
    
    if ($itemCount -eq 0) {
        Write-Host "The temp directory is already clean!" -ForegroundColor Green
        Write-Log "Temp directory is already clean" "INFO"
        exit 0
    }
    
    # Confirmation prompt with detailed information
    Write-Host "SAFETY CONFIRMATION:" -ForegroundColor Red -BackgroundColor Black
    Write-Host "This script will attempt to delete $itemCount items from:" -ForegroundColor Red
    Write-Host "$TEMP_PATH" -ForegroundColor Red
    Write-Host ""
    Write-Host "Estimated space to be freed: $initialSize MB" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "This action cannot be undone!" -ForegroundColor Red -BackgroundColor Black
    Write-Host ""
    
    # Multiple confirmation prompts for safety
    $confirmation1 = Read-Host "Are you sure you want to proceed? Type 'YES' to continue"
    if ($confirmation1 -ne "YES") {
        Write-Log "Script cancelled by user at first confirmation" "INFO"
        Write-Host "Operation cancelled." -ForegroundColor Yellow
        exit 0
    }
    
    $confirmation2 = Read-Host "Final confirmation - Type 'DELETE' to proceed with cleanup"
    if ($confirmation2 -ne "DELETE") {
        Write-Log "Script cancelled by user at final confirmation" "INFO"
        Write-Host "Operation cancelled." -ForegroundColor Yellow
        exit 0
    }
    
    Write-Host "`nStarting cleanup process..." -ForegroundColor Green
    Write-Log "User confirmed cleanup operation" "INFO"
    
    # Perform the cleanup
    $result = Remove-TempItems -Path $TEMP_PATH
    
    # Display summary
    Show-Summary -Result $result
    
    # Final log entry
    Write-Log "=== Cleanup completed. Deleted: $($result.DeletedCount), Errors: $($result.ErrorCount), Size Freed: $($result.TotalSize) MB ===" "INFO"
    
    Write-Host "`nPress any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
}
catch {
    Write-Log "Critical error occurred: $($_.Exception.Message)" "CRITICAL"
    Write-Host "`nCRITICAL ERROR: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Check the log file for details: $LOG_FILE" -ForegroundColor Yellow
    
    Write-Host "`nPress any key to exit..."
    $null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")
    exit 1
}