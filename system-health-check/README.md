# PowerShell System Health Check Toolkit

A comprehensive PowerShell script that generates detailed system health reports for Windows systems. This toolkit provides modular health checking capabilities with multiple output formats and CLI options.

## Features

### 🔍 **System Monitoring**
- **CPU Usage**: Real-time processor utilization and specifications
- **Memory Information**: RAM usage, available memory, and utilization percentages
- **Disk Space**: Storage usage across all drives with capacity warnings
- **Battery Status**: Charge level and status for laptops (desktop detection included)

### 📊 **Advanced Diagnostics**
- **Event Log Analysis**: Critical, error, and warning events from the last 24 hours
- **OS Information**: Version, uptime, architecture, and system specifications
- **Pending Updates**: Windows Update status and available updates
- **Network Status**: Active adapters, connectivity, and IP configuration
- **Service Status**: Critical Windows services monitoring

### 📄 **Export Options**
- **Text Report**: Clean, readable `.txt` format
- **HTML Report**: Professional web-based report with styling and status indicators
- **Custom Output Path**: Specify where reports are saved

## Usage

### Basic Syntax
```powershell
.\system-health-check.ps1 [Parameters]
```

### Parameters

| Parameter | Type | Description |
|-----------|------|-------------|
| `-Basic` | Switch | Run basic health check (CPU, Memory, Disk) |
| `-Full` | Switch | Run comprehensive health check (all modules) |
| `-Export` | Switch | Export reports to .txt and .html files |
| `-OutputPath` | String | Custom directory for exported reports (default: current directory) |

### Examples

#### Quick Basic Check
```powershell
.\system-health-check.ps1 -Basic
```

#### Comprehensive Health Check
```powershell
.\system-health-check.ps1 -Full
```

#### Full Check with Export
```powershell
.\system-health-check.ps1 -Full -Export
```

#### Custom Output Location
```powershell
.\system-health-check.ps1 -Full -Export -OutputPath "C:\HealthReports"
```

## Sample Output

### Console Output
```
PowerShell System Health Check Toolkit
=======================================
Started: 2024-01-15 14:30:25

============================================================
System Information
============================================================

Computer Name            : DESKTOP-ABC123
OS Name                  : Microsoft Windows 11 Pro
OS Version               : 10.0.22621
OS Architecture          : 64-bit
Manufacturer             : Dell Inc.
Model                    : OptiPlex 7090
BIOS Version             : 2.8.0
System Uptime            : 2 days, 14 hours, 23 minutes

============================================================
CPU Information & Usage
============================================================

Processor                : Intel(R) Core(TM) i7-10700 CPU @ 2.90GHz
Cores                    : 8
Logical Processors       : 16
Max Clock Speed          : 2904 MHz
Current CPU Usage        : 15.67% (Good)

============================================================
Memory Information
============================================================

Total Memory             : 16.00 GB
Used Memory              : 8.45 GB
Free Memory              : 7.55 GB
Memory Usage             : 52.81% (Good)
```

### HTML Report Features
- **Professional Styling**: Clean, modern web interface
- **Status Indicators**: Color-coded health status (Good/Warning/Critical)
- **Responsive Design**: Works on desktop and mobile devices
- **Organized Sections**: Easy navigation through different health categories
- **Timestamp**: Report generation date and time

## Health Status Indicators

The toolkit uses intelligent thresholds to categorize system health:

### CPU Usage
- 🟢 **Good**: < 70%
- 🟡 **Warning**: 70-90%
- 🔴 **Critical**: > 90%

### Memory Usage
- 🟢 **Good**: < 80%
- 🟡 **Warning**: 80-95%
- 🔴 **Critical**: > 95%

### Disk Usage
- 🟢 **Good**: < 80%
- 🟡 **Warning**: 80-95%
- 🔴 **Critical**: > 95%

### Battery Level
- 🟢 **Good**: > 50%
- 🟡 **Warning**: 20-50%
- 🔴 **Critical**: < 20%

## Requirements

- **PowerShell**: Version 5.1 or higher
- **Windows**: Windows 10/11 or Windows Server 2016+
- **Permissions**: 
  - Standard user permissions for basic checks
  - Administrator privileges recommended for full event log access and Windows Update checking

## File Structure

```
system-health-check/
├── system-health-check.ps1    # Main script
├── README.md                  # This documentation
└── [Generated Reports]
    ├── SystemHealthReport_YYYY-MM-DD_HH-mm-ss.txt
    └── SystemHealthReport_YYYY-MM-DD_HH-mm-ss.html
```

## Troubleshooting

### Common Issues

**"Execution Policy" Error**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**"Access Denied" for Event Logs**
- Run PowerShell as Administrator for full event log access

**Windows Update Check Fails**
- Requires elevated permissions or PSWindowsUpdate module
- Install with: `Install-Module PSWindowsUpdate`

### Error Handling
The script includes comprehensive error handling and will continue running even if individual modules fail. Warnings are displayed for any components that cannot be accessed.

## Contributing

This is part of an open-source toolkit. Contributions are welcome! Please ensure:
- PowerShell best practices are followed
- Error handling is implemented
- Documentation is updated for new features
- Cross-platform compatibility is considered where possible

## License

This project is open source. Please refer to the repository's LICENSE file for details.

## Changelog

### Version 1.0
- Initial release with basic and full health check modes
- Text and HTML export functionality
- Modular architecture for easy extension
- Comprehensive system monitoring capabilities