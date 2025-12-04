# Installation script for console-todo-app (Windows PowerShell)
# This script checks prerequisites and installs the application

# Ensure script stops on errors
$ErrorActionPreference = "Stop"

# Color functions
function Write-Info {
    param([string]$Message)
    Write-Host "[INFO] $Message" -ForegroundColor Blue
}

function Write-Success {
    param([string]$Message)
    Write-Host "[OK] $Message" -ForegroundColor Green
}

function Write-Warning {
    param([string]$Message)
    Write-Host "[WARN] $Message" -ForegroundColor Yellow
}

function Write-Error-Custom {
    param([string]$Message)
    Write-Host "[ERROR] $Message" -ForegroundColor Red
}

function Write-Step {
    param([string]$Message)
    Write-Host ""
    Write-Host "==> $Message" -ForegroundColor Blue
}

# Banner
Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "  TODO APP - SQLITE INSTALLER" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

# Note about execution policy
if ((Get-ExecutionPolicy) -eq "Restricted") {
    Write-Warning "PowerShell execution policy is set to 'Restricted'"
    Write-Host "You may need to run: Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser"
    Write-Host "Or run this script with: powershell -ExecutionPolicy Bypass -File install.ps1"
    Write-Host ""
}

# Step 1: Check Python version
Write-Step "Checking Python installation..."

try {
    $pythonCmd = Get-Command python -ErrorAction Stop
    $pythonVersion = (python --version 2>&1) -replace 'Python ', ''
    Write-Info "Found Python $pythonVersion"

    # Parse version
    $versionParts = $pythonVersion.Split('.')
    $majorVersion = [int]$versionParts[0]
    $minorVersion = [int]$versionParts[1]

    if ($majorVersion -lt 3 -or ($majorVersion -eq 3 -and $minorVersion -lt 13)) {
        Write-Error-Custom "Python 3.13 or higher is required (found $pythonVersion)"
        Write-Host "Please upgrade Python from https://www.python.org/downloads/"
        exit 1
    }

    Write-Success "Python version check passed"
}
catch {
    Write-Error-Custom "Python is not installed or not in PATH"
    Write-Host "Please install Python 3.13 or higher from https://www.python.org/downloads/"
    Write-Host "Make sure to check 'Add Python to PATH' during installation"
    exit 1
}

# Step 2: Check/Install uv
Write-Step "Checking uv package manager..."

try {
    $uvCmd = Get-Command uv -ErrorAction Stop
    $uvVersion = (uv --version 2>&1) -replace 'uv ', ''
    Write-Info "Found uv $uvVersion"
    Write-Success "uv package manager check passed"
}
catch {
    Write-Warning "uv is not installed. Installing uv..."

    try {
        # Install uv using PowerShell method
        Write-Info "Downloading and installing uv..."
        powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

        # Refresh environment variables
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

        # Verify installation
        $uvCmd = Get-Command uv -ErrorAction Stop
        Write-Success "uv installed successfully"
        Write-Info "You may need to restart PowerShell or refresh your PATH"
    }
    catch {
        Write-Error-Custom "Failed to install uv automatically"
        Write-Host "Please install uv manually:"
        Write-Host "  powershell -c `"irm https://astral.sh/uv/install.ps1 | iex`""
        Write-Host ""
        Write-Host "Or visit: https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    }
}

# Step 3: Install project dependencies
Write-Step "Installing project dependencies..."

Write-Info "Running 'uv sync'..."
try {
    uv sync
    if ($LASTEXITCODE -ne 0) {
        throw "uv sync failed with exit code $LASTEXITCODE"
    }
    Write-Success "Dependencies installed successfully"
}
catch {
    Write-Error-Custom "Failed to install dependencies"
    Write-Host "Error: $_"
    Write-Host "Please check the error messages above and try again."
    exit 1
}

# Step 4: Verify installation
Write-Step "Verifying installation..."

# Check if virtual environment was created
if (Test-Path ".venv") {
    Write-Success "Virtual environment created"
}
else {
    Write-Warning "Virtual environment not found, but uv sync completed"
}

# Check if pyproject.toml exists
if (Test-Path "pyproject.toml") {
    Write-Success "Project configuration found"
}
else {
    Write-Error-Custom "pyproject.toml not found. Are you in the correct directory?"
    exit 1
}

# Success message
Write-Host ""
Write-Host "====================================" -ForegroundColor Green
Write-Host "  INSTALLATION COMPLETE!" -ForegroundColor Green
Write-Host "====================================" -ForegroundColor Green
Write-Host ""

Write-Host "Next steps:" -ForegroundColor Green
Write-Host "  1. Run the application:" -ForegroundColor White
Write-Host "     uv run python -m src.main" -ForegroundColor Blue
Write-Host ""
Write-Host "  2. Run tests:" -ForegroundColor White
Write-Host "     uv run pytest" -ForegroundColor Blue
Write-Host ""
Write-Host "  3. View help:" -ForegroundColor White
Write-Host "     Type 'help' in the application" -ForegroundColor Blue
Write-Host ""

Write-Info "Database will be created at 'data/todo.db' on first run"
Write-Info "For more information, see specs/001-todo-sqlite/quickstart.md"

Write-Host ""
Write-Success "Happy todo-ing!"
