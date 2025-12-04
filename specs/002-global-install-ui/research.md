# Research: Global Installation & Enhanced Terminal UI

**Feature Branch**: `002-global-install-ui`
**Date**: 2025-12-04
**Status**: Complete

## Research Questions

### 1. Global Installation Method

**Decision**: Use `uv tool install` for global installation

**Rationale**:
- `uv tool install` creates isolated environments for CLI tools
- Automatically manages dependencies without polluting system Python
- Faster than pip/pipx (Rust-based)
- Aligns with project's existing uv usage
- Creates entry points automatically from pyproject.toml

**Alternatives Considered**:
- `pipx`: Good option but requires separate installation; uv is already part of our toolchain
- `pip install --user`: Pollutes user site-packages, dependency conflicts possible
- System package managers: Platform-specific, harder to maintain

### 2. Terminal Styling Library

**Decision**: Use `rich` library for terminal styling

**Rationale**:
- Industry standard for Python terminal UIs
- Excellent table formatting with borders and colors
- Automatic terminal capability detection (fallback for dumb terminals)
- Well-maintained, actively developed
- Simple API for console output

**Alternatives Considered**:
- `colorama`: Cross-platform but basic; no tables or panels
- `termcolor`: Simple colors only; no advanced formatting
- `blessed/curses`: Too complex for our needs; full TUI overkill
- ANSI codes directly: Platform compatibility issues, no fallback

### 3. Entry Point Configuration

**Decision**: Use pyproject.toml `[project.scripts]` entry point

**Rationale**:
- Standard Python packaging method
- Works with uv tool install automatically
- Entry point: `todo-app = "src.main:main"`
- Simple, no wrapper scripts needed

**Implementation**:
```toml
[project.scripts]
todo-app = "src.main:main"
```

### 4. Installation Script Approach

**Decision**: Shell scripts that download from GitHub and use uv tool install

**Rationale**:
- Single curl/irm command for users
- Scripts hosted on GitHub raw content
- Auto-install uv if missing using official installer
- No sudo/admin required (user-local installation)

**Linux/macOS Flow**:
1. Check Python 3.13+
2. Install uv via `curl -LsSf https://astral.sh/uv/install.sh | sh`
3. Run `uv tool install git+https://github.com/ikhlasbhojani/console-todo-app`
4. Ensure `~/.local/bin` is in PATH

**Windows Flow**:
1. Check Python 3.13+
2. Install uv via `irm https://astral.sh/uv/install.ps1 | iex`
3. Run `uv tool install git+https://github.com/ikhlasbhojani/console-todo-app`
4. PATH configured automatically by uv

### 5. Color Scheme Design

**Decision**: Modern color scheme with semantic meaning

**Color Assignments**:
| Element | Color | Meaning |
|---------|-------|---------|
| Success messages | Green | Positive outcome |
| Error messages | Red | Problem/failure |
| Pending tasks | Yellow | Attention needed |
| Completed tasks | Green | Done |
| Headers/Titles | Cyan/Blue | Information |
| Borders | White/Gray | Structure |
| Prompt | Magenta | Input expected |

**Rationale**: Standard semantic colors that users instinctively understand.

### 6. Terminal Capability Detection

**Decision**: Use rich's automatic detection with manual override option

**Rationale**:
- `rich` detects terminal capabilities automatically
- Falls back to plain text on dumb terminals
- Environment variable `NO_COLOR` respected
- Consistent behavior across platforms

### 7. Database Location for Global Install

**Decision**: Store database in user's home directory

**Implementation**:
- Location: `~/.todo-app/todo.db` (Linux/macOS) or `%USERPROFILE%\.todo-app\todo.db` (Windows)
- Fallback: Current directory `./data/todo.db` for development

**Rationale**:
- Global install needs consistent data location regardless of working directory
- User home directory is always writable
- Hidden directory keeps it clean

## Key Technical Decisions Summary

| Decision | Choice | Key Reason |
|----------|--------|------------|
| Global install method | uv tool install | Isolated environments, fast, aligns with toolchain |
| Terminal styling | rich library | Industry standard, tables, auto-fallback |
| Entry point | pyproject.toml scripts | Standard packaging |
| Install scripts | curl/irm to GitHub | One command, no dependencies |
| Color scheme | Semantic colors | Intuitive meaning |
| Database location | ~/.todo-app/ | Global consistent storage |

## Dependencies to Add

```toml
dependencies = [
    "rich>=13.0.0",
]
```

## Files to Create/Modify

1. **pyproject.toml**: Add entry point, add rich dependency
2. **src/theme.py**: NEW - Color and styling definitions
3. **src/main.py**: UPDATE - Use rich for all output
4. **scripts/install.sh**: UPDATE - One-command installer
5. **scripts/install.ps1**: UPDATE - One-command installer
6. **README.md**: UPDATE - User-focused documentation
