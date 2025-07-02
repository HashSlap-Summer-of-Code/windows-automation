# Windows Temp Files Cleanup Script

## Overview
This PowerShell script safely deletes temporary files from `C:\Windows\Temp` with comprehensive logging, user confirmation prompts, and error handling.

## Files Included
- `cleantemp.ps1` - Main cleanup script
- `README.md` - This instruction file
- `temp_cleanup_log.txt` - Generated log file (created after first run)

## Features
- ✅ Interactive confirmation prompts for safety
- ✅ Administrator privilege detection
- ✅ Detailed logging of all operations
- ✅ Progress indicators during cleanup
- ✅ Comprehensive error handling
- ✅ Space calculation and reporting
- ✅ Safe deletion with multiple confirmations

## System Requirements
- Windows 10/11 or Windows Server
- PowerShell 5.1 or later
- Recommended: Administrator privileges for complete cleanup

## How to Run

### Method 1: PowerShell Console (Recommended)
1. Open PowerShell as Administrator (right-click PowerShell → "Run as administrator")
2. Navigate to the script directory:
   ```powershell
   cd "C:\path\to\script\directory"
   ```
3. Run the script:
   ```powershell
   .\cleantemp.ps1
   ```

### Method 2: From File Explorer
1. Right-click on `cleantemp.ps1`
2. Select "Run with PowerShell"
3. If prompted about execution policy, choose "Yes" or "Yes to All"

### Method 3: Direct PowerShell Command
```powershell
PowerShell -ExecutionPolicy Bypass -File "C:\path\to\cleantemp.ps1"
```

## Execution Policy Issues
If you encounter execution policy errors, you can temporarily bypass them:

```powershell
# Check current policy
Get-ExecutionPolicy

# Temporarily allow script execution (run as Administrator)
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Or run with bypass (one-time)
PowerShell -ExecutionPolicy Bypass -File ".\cleantemp.ps1"
```

## Safety Features

### Multiple Confirmation Prompts
The script requires TWO confirmations before proceeding:
1. Type `YES` to confirm you want to proceed
2. Type `DELETE` to final confirm the cleanup operation

### Administrator Check
- Script detects if running with admin privileges
- Warns user about potential limitations without admin rights
- Allows user to continue or cancel

### Detailed Logging
All operations are logged to `temp_cleanup_log.txt` including:
- Start/end times
- Files and folders processed
- Success/failure status for each item
- Error details for failed deletions
- Summary statistics

## What Gets Deleted
The script targets all files and folders in:
- `C:\Windows\Temp`

**Important**: Only system temporary files in the Windows temp directory are affected. User temp files and other directories are NOT touched.

## Safety Notes

### ⚠️ IMPORTANT WARNINGS
- **This operation cannot be undone** - deleted files are permanently removed
- **Close all applications** before running to avoid "file in use" errors
- **Run as Administrator** for complete cleanup capability
- **Some files may be locked** by running processes and cannot be deleted

### What's Safe to Delete
- Temporary installation files
- Cached system files
- Old log files
- Temporary download files
- System cleanup remnants

### What Might Cause Issues
- **Active installer files** - may cause installation failures
- **Files locked by running processes** - will generate errors but won't break anything
- **System files in use** - protected by Windows, script will skip them

## Troubleshooting

### Common Issues

**"Execution of scripts is disabled on this system"**
- Run PowerShell as Administrator
- Execute: `Set-ExecutionPolicy RemoteSigned`
- Or use bypass method shown above

**"Access denied" errors**
- Run PowerShell as Administrator
- Close applications that might be using temp files
- Some locked files are normal and safe to skip

**Script shows "0 items found"**
- Temp directory is already clean
- Check if you have the correct permissions
- Verify the path `C:\Windows\Temp` exists

**Many "failed to delete" messages**
- Normal for files in use by system processes
- Try closing unnecessary applications
- Reboot and run script immediately after startup

## Log File Information
The script creates `temp_cleanup_log.txt` in the same directory with:
- Timestamp for each operation
- Success/failure status for each file
- Error details for troubleshooting
- Summary statistics

Example log entry:
```
[2024-07-02 14:30:15] [INFO] === Temp Cleanup Script Started ===
[2024-07-02 14:30:16] [SUCCESS] Deleted File: temp_file.tmp (Size: 2.5 MB)
[2024-07-02 14:30:16] [ERROR] Failed to delete: locked_file.tmp - Error: Access denied
[2024-07-02 14:30:20] [INFO] === Cleanup completed. Deleted: 15, Errors: 2, Size Freed: 45.7 MB ===
```

## Best Practices
1. **Schedule Regular Cleanups** - Run monthly or as needed
2. **Monitor Log Files** - Check for recurring errors
3. **Close Applications First** - Minimize locked file conflicts
4. **Run After Reboots** - Fewer files will be locked
5. **Keep Backups** - Though temp files are generally safe to delete

## Support
If you encounter issues:
1. Check the log file for specific error details
2. Ensure you're running as Administrator
3. Try rebooting and running the script immediately
4. Close unnecessary applications before running

## Version History
- v1.0 - Initial release with core functionality
- Features: Interactive prompts, logging, error handling, progress tracking