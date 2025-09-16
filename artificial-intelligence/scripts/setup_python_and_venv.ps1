<#
setup_python_and_venv.ps1

This script attempts to ensure Python 3.13 is available and creates
a virtual environment named `ai-dev` inside the repository.

Usage (run in PowerShell as Administrator to allow installer to run):
  .\scripts\setup_python_and_venv.ps1

Notes:
- The script will try to detect an existing Python >= 3.13 on PATH.
- If missing, it will download the official Windows installer for
  Python 3.13.0 and run it silently (requires elevation).
#>

param()

function Get-PythonVersion {
    try {
        $ver = & python --version 2>&1
        if ($LASTEXITCODE -ne 0) { return $null }
        # output like: Python 3.13.0
        if ($ver -match 'Python\s+(\d+)\.(\d+)\.(\d+)') {
            return [version]("$($matches[1]).$($matches[2]).$($matches[3])")
        }
        return $null
    } catch {
        return $null
    }
}

Write-Host "Checking for Python on PATH..."
$pv = Get-PythonVersion
if ($pv -and $pv -ge [version]'3.13.0') {
    Write-Host "Found Python $pv"
} else {
    Write-Host "Python 3.13 not found on PATH. The script will download and run the official installer (requires admin)."
    $downloadUrl = 'https://www.python.org/ftp/python/3.13.0/python-3.13.0-amd64.exe'
    $installer = Join-Path $env:TEMP 'python-3.13.0-amd64.exe'
    Write-Host "Downloading Python 3.13 installer to $installer"
    try {
        Invoke-WebRequest -Uri $downloadUrl -OutFile $installer -UseBasicParsing -ErrorAction Stop
    } catch {
        Write-Error "Failed to download Python installer. Please download manually from https://www.python.org/downloads/ and run it, then re-run this script."
        exit 1
    }

    Write-Host "Running installer (will request elevation)..."
    $args = '/quiet InstallAllUsers=1 PrependPath=1'
    Start-Process -FilePath $installer -ArgumentList $args -Wait -Verb RunAs

    Write-Host "Installer finished. You may need to restart the shell for PATH changes to take effect. Trying to detect Python again..."
    Start-Sleep -Seconds 3
    $pv = Get-PythonVersion
    if (-not ($pv -and $pv -ge [version]'3.13.0')) {
        Write-Warning "Python not detected after install. Restart your PowerShell session and run this script again, or install Python manually."
        exit 1
    }
}

# Create the virtual environment
$venvPath = Join-Path (Get-Location) 'ai-dev'
if (Test-Path $venvPath) {
    Write-Host "Virtual environment 'ai-dev' already exists at $venvPath"
} else {
    Write-Host "Creating virtual environment at $venvPath"
    & python -m venv $venvPath
    if ($LASTEXITCODE -ne 0) {
        Write-Error "Failed to create virtual environment."
        exit 1
    }
    Write-Host "Virtual environment created. To activate (PowerShell):"
    Write-Host "  .\\ai-dev\\Scripts\\Activate.ps1"
}

Write-Host "To install dependencies into the venv:"
Write-Host "  .\\ai-dev\\Scripts\\Activate.ps1"
Write-Host "  pip install -r requirements.txt"
