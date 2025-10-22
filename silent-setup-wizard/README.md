# 🧙 Silent Setup Wizard

A powerful PowerShell script that silently installs multiple software packages using winget or Chocolatey. Configure your software list in JSON or TXT format and let the wizard handle the rest!

## ✨ Features

- 📦 **Multiple Package Sources**: Uses winget (default) or Chocolatey
- 🔄 **Flexible Configuration**: Supports both JSON and TXT config files
- 🔇 **Silent Installation**: Installs applications without user interaction
- 📊 **Progress Tracking**: Shows real-time installation progress
- 🧪 **Test Mode**: Safely simulate installations without making changes
- 🖥️ **Dual Interface**: Choose between CLI or GUI mode
- 📝 **Detailed Reporting**: Get a complete success/failure summary

## 🛠️ Requirements

- **PowerShell 5.1+**
- **Windows 10/11** with App Installer (for winget)
- **Administrator privileges** (for software installation)
- **Chocolatey** (optional, only if using `-useChoco` parameter)

## 📋 Configuration Files

The script supports two configuration formats:

### JSON Format (packages.json)
```json
{
  "packages": [
    "Google.Chrome",
    "Mozilla.Firefox",
    "7zip.7zip",
    "Notepad++.Notepad++",
    "Git.Git"
  ]
}
```

### TXT Format (packages.txt)
```
Google.Chrome
Mozilla.Firefox
7zip.7zip
Notepad++.Notepad++
Git.Git
```

## 🚀 Usage Examples

### Basic Usage (CLI Mode)

```powershell
.\install.ps1
```
This will install all packages from the default `packages.json` file using winget.

### Specify a Different Config File

```powershell
.\install.ps1 -config "my-packages.txt"
```

### Use Chocolatey Instead of Winget

```powershell
.\install.ps1 -useChoco
```

### Launch in GUI Mode

```powershell
.\install.ps1 -gui
```

### Test Mode (Safe Simulation)

```powershell
.\install.ps1 -test
```
This will simulate the installation process without actually installing anything - perfect for testing your configuration!

## 🧪 Test Mode

The test mode is a safe way to verify your configuration and see how the script works without making any changes to your system:

- No actual software is installed
- Package manager commands are not executed
- Installation success/failure is simulated (90% success rate)
- Full summary report is still generated

This is useful for:
- Verifying your package list before actual installation
- Demonstrating the script's functionality
- Testing the script in environments where you don't have admin rights
- Checking the script's flow and output format

## 🖥️ GUI Mode

The GUI mode provides a user-friendly interface with:

- File browser to select configuration files
- Package list with multi-select capability
- Visual progress bar
- Installation status updates
- Summary dialog with results

## 📊 Command Line Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `-config` | String | Path to configuration file (default: packages.json) |
| `-gui` | Switch | Launch in GUI mode |
| `-useChoco` | Switch | Use Chocolatey instead of winget |
| `-test` | Switch | Run in test mode (simulation only) |

## 📝 Output Example

```
Silent Setup Wizard
Reading packages from packages.json...
Found 5 packages to install

========================================
         INSTALLATION SUMMARY
========================================
Google.Chrome: Success
Mozilla.Firefox: Success
7zip.7zip: Failed
  Details: Exit code: 1
Notepad++.Notepad++: Success
Git.Git: Success

----------------------------------------
Total packages: 5
Successful: 4
Failed: 1
----------------------------------------
```

## 🔧 Troubleshooting

### Common Issues

1. **"Winget is not installed" error**
   - Install App Installer from the Microsoft Store

2. **"Chocolatey is not installed" error when using -useChoco**
   - Install Chocolatey: https://chocolatey.org/install

3. **Access denied errors**
   - Run PowerShell as Administrator

4. **Package not found errors**
   - Verify the package ID is correct
   - For winget, check available packages with: `winget search [name]`
   - For Chocolatey, check with: `choco search [name]`

## 📜 License

This project is part of the Windows Automation Tools collection.
See the LICENSE file in the root directory for details.
