#!/usr/bin/env bash

# Installation script for console-todo-app (Linux/macOS)
# This script checks prerequisites and installs the application

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Print functions
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[OK]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_step() {
    echo -e "\n${BLUE}==>${NC} $1"
}

# Banner
echo -e "${GREEN}"
echo "===================================="
echo "  TODO APP - SQLITE INSTALLER"
echo "===================================="
echo -e "${NC}"

# Step 1: Check Python version
print_step "Checking Python installation..."

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed."
    echo "Please install Python 3.13 or higher from https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

print_info "Found Python $PYTHON_VERSION"

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 13 ]); then
    print_error "Python 3.13 or higher is required (found $PYTHON_VERSION)"
    echo "Please upgrade Python from https://www.python.org/downloads/"
    exit 1
fi

print_success "Python version check passed"

# Step 2: Check/Install uv
print_step "Checking uv package manager..."

if ! command -v uv &> /dev/null; then
    print_warning "uv is not installed. Installing uv..."

    if command -v curl &> /dev/null; then
        curl -LsSf https://astral.sh/uv/install.sh | sh

        # Add uv to PATH for current session
        export PATH="$HOME/.local/bin:$PATH"

        # Check if installation succeeded
        if ! command -v uv &> /dev/null; then
            print_error "Failed to install uv automatically"
            echo "Please install uv manually: https://docs.astral.sh/uv/getting-started/installation/"
            exit 1
        fi

        print_success "uv installed successfully"
        print_info "You may need to restart your shell or run: export PATH=\"\$HOME/.local/bin:\$PATH\""
    else
        print_error "curl is not available. Cannot install uv automatically."
        echo "Please install uv manually: https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    fi
else
    UV_VERSION=$(uv --version 2>&1 | awk '{print $2}')
    print_info "Found uv $UV_VERSION"
    print_success "uv package manager check passed"
fi

# Step 3: Install project dependencies
print_step "Installing project dependencies..."

print_info "Running 'uv sync'..."
if uv sync; then
    print_success "Dependencies installed successfully"
else
    print_error "Failed to install dependencies"
    echo "Please check the error messages above and try again."
    exit 1
fi

# Step 4: Verify installation
print_step "Verifying installation..."

# Check if virtual environment was created
if [ -d ".venv" ]; then
    print_success "Virtual environment created"
else
    print_warning "Virtual environment not found, but uv sync completed"
fi

# Check if pyproject.toml exists
if [ -f "pyproject.toml" ]; then
    print_success "Project configuration found"
else
    print_error "pyproject.toml not found. Are you in the correct directory?"
    exit 1
fi

# Success message
echo -e "\n${GREEN}"
echo "===================================="
echo "  INSTALLATION COMPLETE!"
echo "===================================="
echo -e "${NC}"

echo -e "\n${GREEN}Next steps:${NC}"
echo "  1. Run the application:"
echo -e "     ${BLUE}uv run python -m src.main${NC}"
echo ""
echo "  2. Run tests:"
echo -e "     ${BLUE}uv run pytest${NC}"
echo ""
echo "  3. View help:"
echo -e "     ${BLUE}Type 'help' in the application${NC}"
echo ""

print_info "Database will be created at 'data/todo.db' on first run"
print_info "For more information, see specs/001-todo-sqlite/quickstart.md"

echo ""
print_success "Happy todo-ing!"
