# Implementation Plan: Global Installation & Enhanced Terminal UI

**Branch**: `002-global-install-ui` | **Date**: 2025-12-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/002-global-install-ui/spec.md`
**GitHub Repository**: https://github.com/ikhlasbhojani/console-todo-app

## Summary

This feature adds one-command global installation capability and enhanced terminal UI design. Users will run a single curl/PowerShell command to install uv (if needed) and the todo-app globally. After installation, typing `todo-app` from any directory launches the application with a modern, colorful interface.

**Key Deliverables:**
1. One-line installation commands for Linux/macOS and Windows
2. Global `todo-app` entry point command
3. Enhanced terminal UI with `rich` library for colors and styling
4. User-focused README with installation and usage instructions

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**:
- `rich` - Terminal styling, colored output, tables
- `uv` - Package manager (auto-installed by installer)
**Storage**: SQLite at `data/todo.db` (unchanged from Phase 1)
**Testing**: pytest (existing test suite)
**Target Platform**: Linux, macOS, Windows 10+
**Project Type**: Single CLI application
**Performance Goals**: Installation under 60 seconds, instant app startup
**Constraints**: No sudo/admin privileges required, works offline after install
**Scale/Scope**: Single user CLI tool

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Code Quality | PASS | Type hints, PEP 8, ruff enforced |
| II. Testing | PASS | Existing tests maintained, new UI tests added |
| III. Spec-Driven Development | PASS | Spec written before implementation |
| IV. Database and Persistence | PASS | SQLite unchanged, data/ directory |
| V. File and Directory Structure | PASS | Using src/, tests/, scripts/, data/ |
| VI. Review and Refactor | PASS | Ruff check before commits |
| VII. AI Behavior | PASS | Using appropriate agents per constitution |

**All 7 principles PASS** - Proceed to Phase 0.

## Project Structure

### Documentation (this feature)

```text
specs/002-global-install-ui/
├── spec.md              # Feature specification
├── plan.md              # This file
├── research.md          # Phase 0: Research decisions
├── data-model.md        # Phase 1: Theme/styling model
├── quickstart.md        # Phase 1: Installation guide
├── contracts/           # Phase 1: CLI styling contracts
│   └── theme.md         # Color and styling definitions
└── tasks.md             # Phase 2: Implementation tasks
```

### Source Code (repository root)

```text
src/
├── __init__.py          # Package marker
├── main.py              # CLI entry point (UPDATE: add rich styling)
├── models.py            # Task dataclass (unchanged)
├── todo_manager.py      # Database operations (unchanged)
├── utils.py             # Validation utilities (unchanged)
└── theme.py             # NEW: Color/styling definitions

tests/
├── __init__.py          # Package marker
├── conftest.py          # pytest fixtures
├── test_todo_manager.py # Manager tests (unchanged)
├── test_cli.py          # CLI tests (UPDATE: verify styled output)
└── test_theme.py        # NEW: Theme/styling tests

scripts/
├── install.sh           # UPDATE: One-command Linux/macOS installer
└── install.ps1          # UPDATE: One-command Windows installer

pyproject.toml           # UPDATE: Add entry point and rich dependency
README.md                # UPDATE: User-focused documentation
```

**Structure Decision**: Single project layout maintained. Adding `theme.py` for styling, updating existing files for rich integration.

## Installation Commands

### Linux/macOS (One Command)

```bash
curl -fsSL https://raw.githubusercontent.com/ikhlasbhojani/console-todo-app/main/scripts/install.sh | bash
```

### Windows PowerShell (One Command)

```powershell
irm https://raw.githubusercontent.com/ikhlasbhojani/console-todo-app/main/scripts/install.ps1 | iex
```

### What the installer does:
1. Checks for Python 3.13+
2. Installs `uv` package manager if not present
3. Installs `todo-app` globally using `uv tool install`
4. Adds uv tools to PATH
5. Displays success message with usage instructions

### After Installation:
```bash
todo-app    # Run from any directory
```

## Complexity Tracking

No constitution violations. No complexity justification needed.
