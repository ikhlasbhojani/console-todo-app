# One-command global installation script for TODO APP (Windows PowerShell)
# Usage: irm https://raw.githubusercontent.com/ikhlasbhojani/console-todo-app/main/scripts/install.ps1 | iex
#
# This script installs EVERYTHING automatically:
# 1. uv package manager
# 2. Python 3.13 (managed by uv)
# 3. todo-app globally

# Ensure script stops on errors
$ErrorActionPreference = "Stop"

# Color functions with Unicode support
function Write-SuccessMsg {
    param([string]$Message)
    Write-Host ([char]0x2713) -ForegroundColor Green -NoNewline
    Write-Host " $Message"
}

function Write-ErrorMsg {
    param([string]$Message)
    Write-Host ([char]0x2717) -ForegroundColor Red -NoNewline
    Write-Host " $Message"
}

function Write-WarningMsg {
    param([string]$Message)
    Write-Host "!" -ForegroundColor Yellow -NoNewline
    Write-Host " $Message"
}

function Write-InfoMsg {
    param([string]$Message)
    Write-Host "i" -ForegroundColor Cyan -NoNewline
    Write-Host " $Message"
}

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==>" -ForegroundColor Magenta -NoNewline
    Write-Host " $Message" -ForegroundColor White
}

# Banner
Write-Host ""
Write-Host ([char]0x2554) -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 46) -ForegroundColor Cyan -NoNewline
Write-Host ([char]0x2557) -ForegroundColor Cyan
Write-Host ([char]0x2551) -ForegroundColor Cyan -NoNewline
Write-Host "     TODO APP - Global Installation           " -NoNewline
Write-Host ([char]0x2551) -ForegroundColor Cyan
Write-Host ([char]0x255A) -ForegroundColor Cyan -NoNewline
Write-Host ("=" * 46) -ForegroundColor Cyan -NoNewline
Write-Host ([char]0x255D) -ForegroundColor Cyan
Write-Host ""

# Step 1: Install uv package manager (it will manage Python for us)
Write-Step "Installing uv package manager..."

try {
    # Always install/update uv
    Write-InfoMsg "Downloading uv..."
    Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression

    # Refresh environment variables
    $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

    # Add common install locations
    $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
    $env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"

    # Verify installation
    $uvCmd = Get-Command uv -ErrorAction Stop
    $uvVersion = (uv --version 2>&1) | Select-Object -First 1
    Write-SuccessMsg "uv installed ($uvVersion)"
}
catch {
    Write-ErrorMsg "Failed to install uv"
    Write-Host ""
    Write-Host "Please try running this command manually:"
    Write-Host "  irm https://astral.sh/uv/install.ps1 | iex"
    exit 1
}

# Step 2: Install todo-app globally
# uv will automatically download Python 3.13 if needed - no separate Python installation required!
Write-Step "Installing todo-app..."

$githubUrl = "git+https://github.com/ikhlasbhojani/console-todo-app.git"

# Uninstall existing version if present (ignore errors)
try {
    uv tool uninstall console-todo-app 2>$null
} catch {}

Write-InfoMsg "Downloading Python 3.13 and todo-app (this may take a moment)..."
Write-Host ""

# Install globally using uv tool with Python version specification
# uv automatically downloads Python 3.13 - user doesn't need Python installed!
try {
    uv tool install --python 3.13 $githubUrl
    if ($LASTEXITCODE -ne 0) {
        throw "uv tool install failed with exit code $LASTEXITCODE"
    }
    Write-SuccessMsg "todo-app installed successfully"
}
catch {
    Write-ErrorMsg "Failed to install todo-app"
    Write-Host ""
    Write-Host "Error: $_"
    Write-Host "Please check the error messages above and try again."
    exit 1
}

# Step 3: Verify installation
Write-Step "Verifying installation..."

# Refresh PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"

# Check if todo-app is available
try {
    $todoCmd = Get-Command todo-app -ErrorAction Stop
    Write-SuccessMsg "todo-app command is ready"
}
catch {
    Write-WarningMsg "todo-app installed but not in PATH yet"
    Write-Host ""
    Write-Host "  Add this to your PowerShell profile:"
    Write-Host ""
    Write-Host '    $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"'
    Write-Host ""
    Write-Host "  Or simply restart your terminal."
}

# Success message
Write-Host ""
Write-Host ([char]0x2554) -ForegroundColor Green -NoNewline
Write-Host ("=" * 46) -ForegroundColor Green -NoNewline
Write-Host ([char]0x2557) -ForegroundColor Green
Write-Host ([char]0x2551) -ForegroundColor Green -NoNewline
Write-Host "     Installation Complete!                    " -NoNewline
Write-Host ([char]0x2551) -ForegroundColor Green
Write-Host ([char]0x255A) -ForegroundColor Green -NoNewline
Write-Host ("=" * 46) -ForegroundColor Green -NoNewline
Write-Host ([char]0x255D) -ForegroundColor Green
Write-Host ""

Write-SuccessMsg "uv package manager"
Write-SuccessMsg "Python 3.13 (managed by uv)"
Write-SuccessMsg "todo-app"

Write-Host ""
Write-Host "To start using the app, run:" -ForegroundColor White
Write-Host ""
Write-Host "  todo-app" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your tasks will be stored in:" -ForegroundColor White
Write-Host "  $env:USERPROFILE\.todo-app\todo.db"
Write-Host ""
Write-InfoMsg "Type 'help' inside the app for commands"
Write-Host ""

# Hint about restart if needed
try {
    Get-Command todo-app -ErrorAction Stop | Out-Null
} catch {
    Write-Host "Note: You may need to restart your terminal first." -ForegroundColor Yellow
    Write-Host ""
}
