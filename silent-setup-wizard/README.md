<#
.SYNOPSIS
  Installs software silently using winget, reads from JSON or TXT config,
  and shows a GUI progress bar if enabled.

.DESCRIPTION
  Supports headless CLI mode and GUI mode using WinForms.
#>

param (
    [string]$config = "packages.json",
    [switch]$gui
)

function Read-Packages {
    param ([string]$path)
    if (Test-Path $path) {
        if ($path -like "*.json") {
            return (Get-Content $path | ConvertFrom-Json).packages
        } elseif ($path -like "*.txt") {
            return Get-Content $path | Where-Object { $_ -ne "" }
        }
    } else {
        Write-Error "Config file not found: $path"
        exit 1
    }
}

function Install-Packages {
    param ([array]$packages)

    $results = @()
    $i = 1
    $total = $packages.Count

    foreach ($pkg in $packages) {
        Write-Progress -Activity "Installing packages" -Status "$pkg ($i of $total)" -PercentComplete (($i / $total) * 100)

        $result = @{
            name = $pkg
            status = "Pending"
        }

        $installCmd = "winget install --id $pkg --silent --accept-source-agreements --accept-package-agreements"
        try {
            $output = Invoke-Expression $installCmd
            $result.status = "Success"
        } catch {
            $result.status = "Failed"
        }

        $results += $result
        $i++
    }

    return $results
}

function Show-Results {
    param ([array]$results)

    Write-Host "`nInstallation Summary:"
    foreach ($r in $results) {
        $color = if ($r.status -eq "Success") { "Green" } else { "Red" }
        Write-Host "$($r.name): $($r.status)" -ForegroundColor $color
    }
}

function Start-GUI {
    Add-Type -AssemblyName System.Windows.Forms

    $form = New-Object Windows.Forms.Form
    $form.Text = "Silent Setup Wizard"
    $form.Width = 400
    $form.Height = 180

    $label = New-Object Windows.Forms.Label
    $label.Text = "Click to install packages from config."
    $label.AutoSize = $true
    $label.Top = 20
    $label.Left = 30
    $form.Controls.Add($label)

    $progressBar = New-Object Windows.Forms.ProgressBar
    $progressBar.Width = 300
    $progressBar.Height = 20
    $progressBar.Top = 60
    $progressBar.Left = 30
    $form.Controls.Add($progressBar)

    $button = New-Object Windows.Forms.Button
    $button.Text = "Start Installation"
    $button.Top = 100
    $button.Left = 30
    $form.Controls.Add($button)

    $button.Add_Click({
        $packages = Read-Packages -path $config
        $total = $packages.Count
        $i = 0
        foreach ($pkg in $packages) {
            $progressBar.Value = ($i / $total) * 100
            Start-Sleep -Milliseconds 500
            try {
                Invoke-Expression "winget install --id $pkg --silent --accept-source-agreements --accept-package-agreements"
            } catch {}
            $i++
        }
        $progressBar.Value = 100
        [System.Windows.Forms.MessageBox]::Show("Installation complete!")
    })

    $form.ShowDialog()
}

# MAIN
$packages = Read-Packages -path $config
if ($gui) {
    Start-GUI
} else {
    $result = Install-Packages -packages $packages
    Show-Results -results $result
}


# 🧙 Silent Setup Wizard

Install all your essential Windows software silently using `winget`, with optional GUI support.

## ✅ Features

- 📦 Reads from JSON or TXT config
- 🔇 Installs apps silently
- 📊 Displays CLI progress bar or GUI
- 📝 Outputs success/failure summary

## 🛠 Requirements

- PowerShell 5.1+
- winget (Windows 10/11)
- Admin access (required for installation)
- Optional: GUI requires Windows Forms (pre-installed)

## 🚀 Usage

### CLI Mode (Default)

```powershell
.\install.ps1 -config "packages.json"
