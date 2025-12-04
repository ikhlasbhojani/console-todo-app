# Implementation Plan: TERMINAL HERO SECTION

**Branch**: `003-terminal-hero` | **Date**: 2025-12-05 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/003-terminal-hero/spec.md`

**Additional User Requirement**: When user runs the app, terminal should be cleared first so the app starts at the top of a clean screen - the application should not look blank or cluttered with previous commands.

## Summary

Transform the TODO application's startup experience with an impressive "hero section" featuring:
1. **Clear terminal on start** - Remove previous commands for a clean slate
2. **Large ASCII art heading** - Figlet-style "TODO APP" text using box-drawing characters
3. **Colorful styling** - Gradient/multi-color effect using rich library
4. **Tagline** - Descriptive subtitle below the heading
5. **Meta info** - Version number and help hint
6. **Visual hierarchy** - Professional layout with proper spacing

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: rich (already installed from Feature 002)
**Storage**: N/A (visual feature only)
**Testing**: pytest (manual visual verification)
**Target Platform**: Cross-platform terminals (Linux, macOS, Windows)
**Project Type**: Single project
**Performance Goals**: Hero section renders in <100ms (instant)
**Constraints**: Works on 40+ character terminals, graceful degradation
**Scale/Scope**: Extends existing theme.py module

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Code Quality | ✅ PASS | Type hints, clean functions, PEP 8 via ruff |
| II. Testing | ✅ PASS | Manual visual tests + edge case coverage |
| III. Spec-Driven Development | ✅ PASS | Spec written first, implementation follows |
| IV. Database and Persistence | ✅ N/A | No data changes - visual only |
| V. File and Directory Structure | ✅ PASS | Changes to src/theme.py, src/main.py |
| VI. Review and Refactor | ✅ PASS | Extends existing code, ruff checks |
| VII. AI Behavior | ✅ PASS | Using python-todo-cli-dev agent |

**All gates passed - proceeding to Phase 0.**

## Project Structure

### Documentation (this feature)

```text
specs/003-terminal-hero/
├── plan.md              # This file
├── research.md          # ASCII art approaches, terminal clearing methods
├── data-model.md        # Hero section structure definition
├── quickstart.md        # How to test the hero section
├── contracts/           # Visual contracts (hero.md)
└── tasks.md             # Implementation tasks (via /sp.tasks)
```

### Source Code (repository root)

```text
src/
├── theme.py             # MODIFY: Add hero section functions
├── main.py              # MODIFY: Use new print_hero() and clear_terminal()
├── models.py            # No changes
├── todo_manager.py      # No changes
└── utils.py             # No changes

tests/
├── test_cli.py          # MODIFY: Update banner tests
├── test_todo_manager.py # No changes
└── conftest.py          # No changes
```

**Structure Decision**: Single project - extending existing src/theme.py with new hero section functions.

## Complexity Tracking

> No violations - implementation extends existing theme module without adding complexity.

---

## Phase 0: Research

See [research.md](research.md) for detailed findings.

## Phase 1: Design

See:
- [data-model.md](data-model.md) - Hero section component structure
- [contracts/hero.md](contracts/hero.md) - Visual contract for hero section
- [quickstart.md](quickstart.md) - Testing the hero section
