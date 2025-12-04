#!/usr/bin/env bash

# One-command global installation script for TODO APP
# Usage: curl -fsSL https://raw.githubusercontent.com/ikhlasbhojani/console-todo-app/main/scripts/install.sh | bash
#
# This script installs EVERYTHING automatically:
# 1. uv package manager
# 2. Python 3.13 (managed by uv)
# 3. todo-app globally

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

# Step 1: Install uv package manager (it will manage Python for us)
print_step "Installing uv package manager..."

# Always try to install/update uv first
if command -v curl &> /dev/null; then
    curl -LsSf https://astral.sh/uv/install.sh | sh

    # Add uv to PATH for current session
    export PATH="$HOME/.local/bin:$PATH"
    export PATH="$HOME/.cargo/bin:$PATH"

    # Source shell config if exists
    [ -f "$HOME/.bashrc" ] && source "$HOME/.bashrc" 2>/dev/null || true
    [ -f "$HOME/.zshrc" ] && source "$HOME/.zshrc" 2>/dev/null || true

elif command -v wget &> /dev/null; then
    wget -qO- https://astral.sh/uv/install.sh | sh

    export PATH="$HOME/.local/bin:$PATH"
    export PATH="$HOME/.cargo/bin:$PATH"
else
    print_error "Neither curl nor wget is available."
    echo ""
    echo "Please install curl first:"
    echo "  Ubuntu/Debian: sudo apt install curl"
    echo "  Fedora: sudo dnf install curl"
    echo "  macOS: curl is pre-installed"
    exit 1
fi

# Verify uv is available
if ! command -v uv &> /dev/null; then
    print_error "Failed to install uv"
    echo ""
    echo "Please try installing uv manually:"
    echo "  curl -LsSf https://astral.sh/uv/install.sh | sh"
    exit 1
fi

UV_VERSION=$(uv --version 2>&1 | head -1)
print_success "uv installed ($UV_VERSION)"

# Step 2: Install todo-app globally
# uv will automatically download Python 3.13 if needed - no separate Python installation required!
print_step "Installing todo-app..."

GITHUB_URL="git+https://github.com/ikhlasbhojani/console-todo-app.git"

# Uninstall existing version if present (ignore errors)
uv tool uninstall console-todo-app 2>/dev/null || true

print_info "Downloading Python 3.13 and todo-app (this may take a moment)..."
echo ""

# Install globally using uv tool with Python version specification
# uv automatically downloads Python 3.13 - user doesn't need Python installed!
if uv tool install --python 3.13 "$GITHUB_URL"; then
    print_success "todo-app installed successfully"
else
    print_error "Failed to install todo-app"
    echo ""
    echo "Please check the error messages above and try again."
    exit 1
fi

# Step 3: Verify installation
print_step "Verifying installation..."

# Ensure PATH includes uv tools directory
export PATH="$HOME/.local/bin:$PATH"

# Check if todo-app is available
if command -v todo-app &> /dev/null; then
    print_success "todo-app command is ready"
else
    print_warning "todo-app installed but not in PATH yet"
    echo ""
    echo "  Add this line to your ~/.bashrc or ~/.zshrc:"
    echo ""
    echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
    echo ""
    echo "  Then run: source ~/.bashrc (or ~/.zshrc)"
    echo ""
    echo "  Or simply restart your terminal."
fi

# Success message
echo ""
echo -e "${GREEN}╔══════════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║${NC}     ${BOLD}Installation Complete!${NC}                    ${GREEN}║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════════════╝${NC}"
echo ""

print_success "uv package manager"
print_success "Python 3.13 (managed by uv)"
print_success "todo-app"

echo ""
echo -e "${BOLD}To start using the app, run:${NC}"
echo ""
echo -e "  ${CYAN}todo-app${NC}"
echo ""
echo -e "${BOLD}Your tasks will be stored in:${NC}"
echo -e "  ~/.todo-app/todo.db"
echo ""
print_info "Type 'help' inside the app for commands"
echo ""

# Hint about PATH if needed
if ! command -v todo-app &> /dev/null; then
    echo -e "${YELLOW}Note: You may need to restart your terminal first.${NC}"
    echo ""
fi
