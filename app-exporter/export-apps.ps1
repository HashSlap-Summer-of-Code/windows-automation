[CmdletBinding()]
param (
    [string]$Publisher,
    [int]$MinSizeMB,
    [string]$OutputPath = "installed_apps.csv"
)

function Get-InstalledApps {
    $registryPaths = @(
        "HKLM:\Software\Microsoft\Windows\CurrentVersion\Uninstall\*",
        "HKLM:\Software\WOW6432Node\Microsoft\Windows\CurrentVersion\Uninstall\*"
    )

    $apps = @()

    foreach ($path in $registryPaths) {
        $items = Get-ItemProperty -Path $path -ErrorAction SilentlyContinue

        foreach ($item in $items) {
            if (-not $item.DisplayName) { continue }

            $app = [PSCustomObject]@{
                Name        = $item.DisplayName
                Version     = $item.DisplayVersion
                InstallDate = $item.InstallDate
                Publisher   = $item.Publisher
                SizeMB      = if ($item.EstimatedSize) { [math]::Round($item.EstimatedSize / 1024, 2) } else { "N/A" }
            }

            $apps += $app
        }
    }

    return $apps
}

# Run scan
Write-Host "Scanning installed applications..." -ForegroundColor Cyan
$apps = Get-InstalledApps

# Filter by Publisher
if ($Publisher) {
    Write-Host "Filtering by Publisher: $Publisher" -ForegroundColor Yellow
    $apps = $apps | Where-Object { $_.Publisher -match [regex]::Escape($Publisher) }
}

# Filter by Size
if ($MinSizeMB) {
    Write-Host "Filtering by Minimum Size: $MinSizeMB MB" -ForegroundColor Yellow
    $apps = $apps | Where-Object {
        ($_."SizeMB" -ne "N/A") -and ($_."SizeMB" -ge $MinSizeMB)
    }
}

# Export
Write-Host "Exporting results to: $OutputPath" -ForegroundColor Green
$apps | Export-Csv -Path $OutputPath -NoTypeInformation -Encoding UTF8

Write-Host "Done. Exported $($apps.Count) app(s)." -ForegroundColor Green
