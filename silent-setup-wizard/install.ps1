<#
.SYNOPSIS
  Installs software silently using winget, reads from JSON or TXT config,
  and shows a GUI progress bar if enabled.

.DESCRIPTION
  Silent Setup Wizard - Automatically installs software packages from a configuration file
  using winget or chocolatey. Supports both CLI mode with progress bar and GUI mode with
  Windows Forms interface.

.PARAMETER config
  Path to the configuration file (JSON or TXT format)

.PARAMETER gui
  Switch to enable GUI mode using Windows Forms

.PARAMETER useChoco
  Switch to use Chocolatey instead of winget

.EXAMPLE
  .\install.ps1
  Installs packages from default packages.json using winget

.EXAMPLE
  .\install.ps1 -config "my-packages.txt"
  Installs packages from my-packages.txt using winget

.EXAMPLE
  .\install.ps1 -gui
  Launches GUI installer using default packages.json

.EXAMPLE
  .\install.ps1 -useChoco
  Installs packages using Chocolatey instead of winget
#>

param (
    [string]$config = "packages.json",
    [switch]$gui,
    [switch]$useChoco,
    [switch]$test
)

# Function to read packages from config file (JSON or TXT)
function Read-Packages {
    param ([string]$path)
    
    if (Test-Path $path) {
        if ($path -like "*.json") {
            return (Get-Content $path | ConvertFrom-Json).packages
        } 
        elseif ($path -like "*.txt") {
            return Get-Content $path | Where-Object { $_ -ne "" -and -not $_.StartsWith("#") }
        }
        else {
            Write-Error "Unsupported file format. Please use .json or .txt"
            exit 1
        }
    } 
    else {
        Write-Error "Config file not found: $path"
        exit 1
    }
}

# Function to install packages using winget or chocolatey
function Install-Packages {
    param (
        [array]$packages,
        [bool]$useChocolatey = $false,
        [bool]$testMode = $false
    )

    $results = @()
    $i = 1
    $total = $packages.Count
    $successCount = 0
    $failCount = 0

    foreach ($pkg in $packages) {
        $packageName = $pkg.Trim()
        Write-Progress -Activity "Installing packages" -Status "$packageName ($i of $total)" -PercentComplete (($i / $total) * 100)

        $result = @{
            name = $packageName
            status = "Pending"
            details = ""
        }

        # Test mode - simulate installation with random success/failure
        if ($testMode) {
            Start-Sleep -Milliseconds 500  # Simulate installation time
            
            # Simulate 90% success rate in test mode
            $randomSuccess = (Get-Random -Minimum 1 -Maximum 11) -le 9
            
            if ($randomSuccess) {
                $result.status = "Success (TEST MODE)"
                $successCount++
            } else {
                $result.status = "Failed (TEST MODE)"
                $result.details = "Simulated failure for testing"
                $failCount++
            }
            
            Write-Host "TEST MODE: $($result.status) for package $packageName" -ForegroundColor Yellow
        }
        # Real installation mode
        else {
            try {
                if ($useChocolatey) {
                    $output = choco install $packageName -y
                    if ($LASTEXITCODE -eq 0) {
                        $result.status = "Success"
                        $successCount++
                    } 
                    else {
                        $result.status = "Failed"
                        $result.details = "Exit code: $LASTEXITCODE"
                        $failCount++
                    }
                } 
                else {
                    $output = winget install --id $packageName --silent --accept-source-agreements --accept-package-agreements
                    if ($LASTEXITCODE -eq 0) {
                        $result.status = "Success"
                        $successCount++
                    } 
                    else {
                        $result.status = "Failed"
                        $result.details = "Exit code: $LASTEXITCODE"
                        $failCount++
                    }
                }
            } 
            catch {
                $result.status = "Failed"
                $result.details = $_.Exception.Message
                $failCount++
            }
        }

        $results += $result
        $i++
    }

    return @{
        results = $results
        summary = @{
            total = $total
            success = $successCount
            failed = $failCount
        }
    }
}

# Function to display installation results in console
function Show-Results {
    param ([PSCustomObject]$installationData)

    $results = $installationData.results
    $summary = $installationData.summary

    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "         INSTALLATION SUMMARY          " -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    
    foreach ($r in $results) {
        $color = if ($r.status -eq "Success") { "Green" } else { "Red" }
        Write-Host "$($r.name): " -NoNewline
        Write-Host "$($r.status)" -ForegroundColor $color
        if ($r.details -ne "") {
            Write-Host "  Details: $($r.details)" -ForegroundColor Gray
        }
    }
    
    Write-Host "`n----------------------------------------" -ForegroundColor Cyan
    Write-Host "Total packages: $($summary.total)" -ForegroundColor White
    Write-Host "Successful: $($summary.success)" -ForegroundColor Green
    Write-Host "Failed: $($summary.failed)" -ForegroundColor $(if ($summary.failed -gt 0) { "Red" } else { "Green" })
    Write-Host "----------------------------------------`n" -ForegroundColor Cyan
}

# Function to create and show GUI
function Start-GUI {
    param (
        [string]$configPath,
        [bool]$useChocolatey = $false
    )

    Add-Type -AssemblyName System.Windows.Forms
    Add-Type -AssemblyName System.Drawing

    # Create main form
    $form = New-Object Windows.Forms.Form
    $form.Text = "Silent Setup Wizard"
    $form.Size = New-Object Drawing.Size(500, 400)
    $form.StartPosition = "CenterScreen"
    $form.FormBorderStyle = "FixedDialog"
    $form.MaximizeBox = $false

    # Create title label
    $titleLabel = New-Object Windows.Forms.Label
    $titleLabel.Text = "Silent Setup Wizard"
    $titleLabel.Font = New-Object Drawing.Font("Segoe UI", 16, [System.Drawing.FontStyle]::Bold)
    $titleLabel.AutoSize = $true
    $titleLabel.Location = New-Object Drawing.Point(20, 20)
    $form.Controls.Add($titleLabel)

    # Create description label
    $descLabel = New-Object Windows.Forms.Label
    $descLabel.Text = "Install software packages silently from configuration"
    $descLabel.AutoSize = $true
    $descLabel.Location = New-Object Drawing.Point(20, 55)
    $form.Controls.Add($descLabel)

    # Create config file label and textbox
    $configLabel = New-Object Windows.Forms.Label
    $configLabel.Text = "Config File:"
    $configLabel.AutoSize = $true
    $configLabel.Location = New-Object Drawing.Point(20, 90)
    $form.Controls.Add($configLabel)

    $configTextBox = New-Object Windows.Forms.TextBox
    $configTextBox.Text = $configPath
    $configTextBox.Location = New-Object Drawing.Point(100, 87)
    $configTextBox.Size = New-Object Drawing.Size(280, 23)
    $form.Controls.Add($configTextBox)

    $browseButton = New-Object Windows.Forms.Button
    $browseButton.Text = "Browse"
    $browseButton.Location = New-Object Drawing.Point(390, 86)
    $browseButton.Size = New-Object Drawing.Size(80, 25)
    $form.Controls.Add($browseButton)

    # Create package list box
    $packagesLabel = New-Object Windows.Forms.Label
    $packagesLabel.Text = "Packages to install:"
    $packagesLabel.AutoSize = $true
    $packagesLabel.Location = New-Object Drawing.Point(20, 125)
    $form.Controls.Add($packagesLabel)

    $packageListBox = New-Object Windows.Forms.ListBox
    $packageListBox.Location = New-Object Drawing.Point(20, 150)
    $packageListBox.Size = New-Object Drawing.Size(450, 120)
    $packageListBox.SelectionMode = "MultiExtended"
    $form.Controls.Add($packageListBox)

    # Create progress bar
    $progressBar = New-Object Windows.Forms.ProgressBar
    $progressBar.Location = New-Object Drawing.Point(20, 280)
    $progressBar.Size = New-Object Drawing.Size(450, 25)
    $progressBar.Style = "Continuous"
    $form.Controls.Add($progressBar)

    # Create status label
    $statusLabel = New-Object Windows.Forms.Label
    $statusLabel.Text = "Ready to install"
    $statusLabel.AutoSize = $true
    $statusLabel.Location = New-Object Drawing.Point(20, 315)
    $form.Controls.Add($statusLabel)

    # Create install button
    $installButton = New-Object Windows.Forms.Button
    $installButton.Text = "Install Packages"
    $installButton.Location = New-Object Drawing.Point(350, 320)
    $installButton.Size = New-Object Drawing.Size(120, 30)
    $form.Controls.Add($installButton)

    # Function to load packages from config
    function Load-PackagesFromConfig {
        param ([string]$path)
        
        $packageListBox.Items.Clear()
        
        try {
            $packages = Read-Packages -path $path
            foreach ($pkg in $packages) {
                $packageListBox.Items.Add($pkg)
            }
            $statusLabel.Text = "Loaded $($packages.Count) packages from config"
            return $true
        }
        catch {
            [System.Windows.Forms.MessageBox]::Show("Error loading config file: $($_.Exception.Message)", "Error", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Error)
            return $false
        }
    }

    # Browse button click event
    $browseButton.Add_Click({
        $openFileDialog = New-Object Windows.Forms.OpenFileDialog
        $openFileDialog.Filter = "Config Files (*.json;*.txt)|*.json;*.txt|All Files (*.*)|*.*"
        $openFileDialog.Title = "Select Config File"
        
        if ($openFileDialog.ShowDialog() -eq "OK") {
            $configTextBox.Text = $openFileDialog.FileName
            Load-PackagesFromConfig -path $openFileDialog.FileName
        }
    })

    # Install button click event
    $installButton.Add_Click({
        if ($packageListBox.Items.Count -eq 0) {
            [System.Windows.Forms.MessageBox]::Show("No packages to install", "Warning", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Warning)
            return
        }

        $installButton.Enabled = $false
        $browseButton.Enabled = $false
        
        $selectedPackages = @()
        if ($packageListBox.SelectedItems.Count -gt 0) {
            foreach ($item in $packageListBox.SelectedItems) {
                $selectedPackages += $item
            }
        } else {
            foreach ($item in $packageListBox.Items) {
                $selectedPackages += $item
            }
        }
        
        $total = $selectedPackages.Count
        $current = 0
        $successful = 0
        $failed = 0
        $results = @()
        
        foreach ($pkg in $selectedPackages) {
            $current++
            $progressBar.Value = [int](($current / $total) * 100)
            $statusLabel.Text = "Installing $pkg ($current of $total)"
            $form.Refresh()
            
            try {
                if ($useChocolatey) {
                    $output = choco install $pkg -y
                    if ($LASTEXITCODE -eq 0) {
                        $successful++
                        $results += @{ name = $pkg; status = "Success" }
                    } else {
                        $failed++
                        $results += @{ name = $pkg; status = "Failed" }
                    }
                } else {
                    $output = winget install --id $pkg --silent --accept-source-agreements --accept-package-agreements
                    if ($LASTEXITCODE -eq 0) {
                        $successful++
                        $results += @{ name = $pkg; status = "Success" }
                    } else {
                        $failed++
                        $results += @{ name = $pkg; status = "Failed" }
                    }
                }
            } catch {
                $failed++
                $results += @{ name = $pkg; status = "Failed" }
            }
        }
        
        $progressBar.Value = 100
        $statusLabel.Text = "Installation complete: $successful succeeded, $failed failed"
        
        # Create summary message
        $summaryMessage = "Installation Summary:`n`n"
        foreach ($r in $results) {
            $summaryMessage += "$($r.name): $($r.status)`n"
        }
        $summaryMessage += "`nTotal: $total, Successful: $successful, Failed: $failed"
        
        [System.Windows.Forms.MessageBox]::Show($summaryMessage, "Installation Complete", [System.Windows.Forms.MessageBoxButtons]::OK, [System.Windows.Forms.MessageBoxIcon]::Information)
        
        $installButton.Enabled = $true
        $browseButton.Enabled = $true
    })

    # Load packages from initial config
    Load-PackagesFromConfig -path $configPath

    # Show the form
    $form.ShowDialog()
}

# Check if winget or chocolatey is available
function Test-PackageManager {
    param ([bool]$useChocolatey = $false)
    
    if ($useChocolatey) {
        $chocoAvailable = Get-Command choco -ErrorAction SilentlyContinue
        if (-not $chocoAvailable) {
            Write-Error "Chocolatey is not installed. Please install it first: https://chocolatey.org/install"
            return $false
        }
    } else {
        $wingetAvailable = Get-Command winget -ErrorAction SilentlyContinue
        if (-not $wingetAvailable) {
            Write-Error "Winget is not installed. Please install App Installer from the Microsoft Store."
            return $false
        }
    }
    
    return $true
}

# Main execution
if (-not $test) {
    if (-not (Test-PackageManager -useChocolatey $useChoco)) {
        exit 1
    }
} else {
    Write-Host "RUNNING IN TEST MODE - No packages will actually be installed" -ForegroundColor Yellow -BackgroundColor Black
}

if ($gui) {
    # TODO: Add test mode to GUI in future version
    Start-GUI -configPath $config -useChocolatey $useChoco
} else {
    Write-Host "Silent Setup Wizard" -ForegroundColor Cyan
    Write-Host "Reading packages from $config..." -ForegroundColor Yellow
    
    $packages = Read-Packages -path $config
    Write-Host "Found $($packages.Count) packages to install" -ForegroundColor Yellow
    
    $installationData = Install-Packages -packages $packages -useChocolatey $useChoco -testMode $test
    Show-Results -installationData $installationData
}