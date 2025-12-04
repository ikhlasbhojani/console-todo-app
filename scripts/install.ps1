# One-command global installation script for TODO APP (Windows PowerShell)
# Usage: irm https://raw.githubusercontent.com/ikhlasbhojani/console-todo-app/main/scripts/install.ps1 | iex

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

# Note about execution policy
if ((Get-ExecutionPolicy) -eq "Restricted") {
    Write-WarningMsg "PowerShell execution policy is set to 'Restricted'"
    Write-Host "You may need to run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
    Write-Host ""
}

# Step 1: Check Python version (3.13+)
Write-Step "Checking Python installation..."

try {
    $pythonCmd = Get-Command python -ErrorAction Stop
    $pythonVersion = (python --version 2>&1) -replace 'Python ', ''
    Write-InfoMsg "Found Python $pythonVersion"

    # Parse version
    $versionParts = $pythonVersion.Split('.')
    $majorVersion = [int]$versionParts[0]
    $minorVersion = [int]$versionParts[1]

    if ($majorVersion -lt 3 -or ($majorVersion -eq 3 -and $minorVersion -lt 13)) {
        Write-ErrorMsg "Python 3.13 or higher is required (found $pythonVersion)"
        Write-Host ""
        Write-Host "Please upgrade Python from:"
        Write-Host "  https://www.python.org/downloads/"
        exit 1
    }

    Write-SuccessMsg "Python version check passed"
}
catch {
    Write-ErrorMsg "Python is not installed or not in PATH"
    Write-Host ""
    Write-Host "Please install Python 3.13 or higher from:"
    Write-Host "  https://www.python.org/downloads/"
    Write-Host ""
    Write-Host "Make sure to check 'Add Python to PATH' during installation"
    exit 1
}

# Step 2: Check/Install uv package manager
Write-Step "Checking uv package manager..."

try {
    $uvCmd = Get-Command uv -ErrorAction Stop
    $uvVersion = (uv --version 2>&1) | Select-Object -First 1
    Write-InfoMsg "Found $uvVersion"
    Write-SuccessMsg "uv package manager check passed"
}
catch {
    Write-WarningMsg "uv is not installed. Installing uv automatically..."
    Write-Host ""

    try {
        # Install uv using PowerShell method
        Write-InfoMsg "Downloading and installing uv..."
        Invoke-RestMethod https://astral.sh/uv/install.ps1 | Invoke-Expression

        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

        # Also add common install locations
        $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"
        $env:Path = "$env:USERPROFILE\.cargo\bin;$env:Path"

        # Verify installation
        $uvCmd = Get-Command uv -ErrorAction Stop
        Write-SuccessMsg "uv installed successfully"
    }
    catch {
        Write-ErrorMsg "Failed to install uv automatically"
        Write-Host ""
        Write-Host "Please install uv manually:"
        Write-Host "  irm https://astral.sh/uv/install.ps1 | iex"
        Write-Host ""
        Write-Host "Or visit: https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    }
}

# Step 3: Install todo-app globally using uv tool
Write-Step "Installing todo-app globally..."

$githubUrl = "git+https://github.com/ikhlasbhojani/console-todo-app.git"

# Uninstall existing version if present (ignore errors)
try {
    uv tool uninstall console-todo-app 2>$null
} catch {}

# Install globally using uv tool
try {
    uv tool install $githubUrl
    if ($LASTEXITCODE -ne 0) {
        throw "uv tool install failed with exit code $LASTEXITCODE"
    }
    Write-SuccessMsg "todo-app installed globally"
}
catch {
    Write-ErrorMsg "Failed to install todo-app"
    Write-Host ""
    Write-Host "Error: $_"
    Write-Host "Please check the error messages above and try again."
    exit 1
}

# Step 4: Verify installation
Write-Step "Verifying installation..."

# Refresh PATH
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
$env:Path = "$env:USERPROFILE\.local\bin;$env:Path"

# Check if todo-app is available
try {
    $todoCmd = Get-Command todo-app -ErrorAction Stop
    Write-SuccessMsg "todo-app command is available"
}
catch {
    Write-WarningMsg "todo-app may not be in your PATH yet"
    Write-Host ""
    Write-InfoMsg "You may need to restart PowerShell or add to your PATH:"
    Write-Host ""
    Write-Host "  Add to your PowerShell profile:"
    Write-Host '    $env:Path = "$env:USERPROFILE\.local\bin;$env:Path"'
    Write-Host ""
    Write-Host "  Or restart your terminal"
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

Write-SuccessMsg "Python $pythonVersion"
Write-SuccessMsg "uv package manager installed"
Write-SuccessMsg "todo-app installed globally"

Write-Host ""
Write-Host "To start using the app:" -ForegroundColor White
Write-Host ""
Write-Host "  todo-app" -ForegroundColor Cyan
Write-Host ""
Write-Host "Your tasks will be stored in:" -ForegroundColor White
Write-Host "  $env:USERPROFILE\.todo-app\todo.db"
Write-Host ""
Write-InfoMsg "For help, type 'help' inside the app"
Write-Host ""
