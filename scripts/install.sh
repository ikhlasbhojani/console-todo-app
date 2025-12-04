#!/usr/bin/env bash

# One-command global installation script for TODO APP
# Usage: curl -fsSL https://raw.githubusercontent.com/ikhlasbhojani/console-todo-app/main/scripts/install.sh | bash

set -e  # Exit on error

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
MAGENTA='\033[0;35m'
NC='\033[0m' # No Color
BOLD='\033[1m'

# Print functions
print_success() {
    echo -e "${GREEN}✓${NC} $1"
}

print_error() {
    echo -e "${RED}✗${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}!${NC} $1"
}

print_info() {
    echo -e "${CYAN}i${NC} $1"
}

print_step() {
    echo -e "\n${BOLD}${MAGENTA}==>${NC} $1"
}

# Banner
echo ""
echo -e "${CYAN}╔══════════════════════════════════════════════╗${NC}"
echo -e "${CYAN}║${NC}     ${BOLD}TODO APP - Global Installation${NC}           ${CYAN}║${NC}"
echo -e "${CYAN}╚══════════════════════════════════════════════╝${NC}"
echo ""

# Step 1: Check Python version (3.13+)
print_step "Checking Python installation..."

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 is not installed."
    echo ""
    echo "Please install Python 3.13 or higher from:"
    echo "  https://www.python.org/downloads/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
PYTHON_MAJOR=$(echo "$PYTHON_VERSION" | cut -d. -f1)
PYTHON_MINOR=$(echo "$PYTHON_VERSION" | cut -d. -f2)

print_info "Found Python $PYTHON_VERSION"

if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 13 ]); then
    print_error "Python 3.13 or higher is required (found $PYTHON_VERSION)"
    echo ""
    echo "Please upgrade Python from:"
    echo "  https://www.python.org/downloads/"
    exit 1
fi

print_success "Python version check passed"

# Step 2: Check/Install uv package manager
print_step "Checking uv package manager..."

if ! command -v uv &> /dev/null; then
    print_warning "uv is not installed. Installing uv automatically..."
    echo ""

    if command -v curl &> /dev/null; then
        curl -LsSf https://astral.sh/uv/install.sh | sh

        # Add uv to PATH for current session
        export PATH="$HOME/.local/bin:$PATH"

        # Also try cargo bin path
        export PATH="$HOME/.cargo/bin:$PATH"

        # Check if installation succeeded
        if ! command -v uv &> /dev/null; then
            print_error "Failed to install uv automatically"
            echo ""
            echo "Please install uv manually:"
            echo "  https://docs.astral.sh/uv/getting-started/installation/"
            exit 1
        fi

        print_success "uv installed successfully"
    else
        print_error "curl is not available. Cannot install uv automatically."
        echo ""
        echo "Please install uv manually:"
        echo "  https://docs.astral.sh/uv/getting-started/installation/"
        exit 1
    fi
else
    UV_VERSION=$(uv --version 2>&1 | head -1)
    print_info "Found $UV_VERSION"
    print_success "uv package manager check passed"
fi

# Step 3: Install todo-app globally using uv tool
print_step "Installing todo-app globally..."

GITHUB_URL="git+https://github.com/ikhlasbhojani/console-todo-app.git"

# Uninstall existing version if present (ignore errors)
uv tool uninstall console-todo-app 2>/dev/null || true

# Install globally using uv tool
if uv tool install "$GITHUB_URL"; then
    print_success "todo-app installed globally"
else
    print_error "Failed to install todo-app"
    echo ""
    echo "Please check the error messages above and try again."
    exit 1
fi

# Step 4: Verify installation
print_step "Verifying installation..."

# Check if todo-app is available
if command -v todo-app &> /dev/null; then
    print_success "todo-app command is available"
else
    print_warning "todo-app may not be in your PATH yet"
    echo ""
    print_info "Add the following to your shell configuration:"
    echo ""
    echo "  For bash (~/.bashrc):"
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "  For zsh (~/.zshrc):"
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "  Then restart your terminal or run:"
    echo "    source ~/.bashrc  # or ~/.zshrc"
fi

# Success message
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}     ${BOLD}Installation Complete!${NC}                    ${GREEN}║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════╝${NC}"
echo ""

print_success "Python $PYTHON_VERSION"
print_success "uv package manager installed"
print_success "todo-app installed globally"

echo ""
echo -e "${BOLD}To start using the app:${NC}"
echo ""
echo -e "  ${CYAN}todo-app${NC}"
echo ""
echo -e "${BOLD}Your tasks will be stored in:${NC}"
echo -e "  ~/.todo-app/todo.db"
echo ""
print_info "For help, type 'help' inside the app"
echo ""
