# 📦 App Exporter

A PowerShell script to list all installed applications on a Windows system and export them to a CSV file. Supports optional filters by publisher and estimated size.

# 🚀 Usage

```powershell
# Basic usage
.\export-apps.ps1
```

## Filter by publisher
```
.\export-apps.ps1 -Publisher "Microsoft"
```

## Filter by minimum size
```
.\export-apps.ps1 -MinSizeMB 100
```
## Save to a custom path
```
.\export-apps.ps1 -OutputPath "C:\apps.csv"
```