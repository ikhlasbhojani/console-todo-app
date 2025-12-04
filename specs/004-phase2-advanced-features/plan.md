# Implementation Plan: TODO APP - PHASE 2 (Advanced Features)

**Branch**: `004-phase2-advanced-features` | **Date**: 2025-12-05 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `/specs/004-phase2-advanced-features/spec.md`

## Summary

Add advanced task management features to the Phase 1 console todo application:
1. **Due dates with filtered views** - Assign optional due dates to tasks, filter by today/overdue/upcoming
2. **Project management** - Full CRUD for projects, task-project association
3. **Statistics dashboard** - Task counts, completion rate, deadline status
4. **Undo functionality** (optional) - Single-level undo for last action

Technical approach: Extend existing SQLite database with new columns (due_date, project_id) and new table (projects). Add filter methods to TodoManager, new CLI commands, and optional in-memory action history for undo.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: rich (existing), sqlite3 (built-in)
**Storage**: SQLite database at `~/.todo-app/todo.db`
**Testing**: pytest with fixtures for database setup/teardown
**Target Platform**: Cross-platform terminals (Linux, macOS, Windows)
**Project Type**: Single project
**Performance Goals**: All operations complete in <1 second for up to 1000 tasks
**Constraints**: No external database, no ORMs, parameterized queries only
**Scale/Scope**: Single-user local application

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Code Quality | ✅ PASS | Type hints, dataclasses, ruff enforcement, small functions |
| II. Testing | ✅ PASS | pytest with fixtures, edge case coverage planned |
| III. Spec-Driven Development | ✅ PASS | Spec written first, implementation follows |
| IV. Database and Persistence | ✅ PASS | SQLite at ~/.todo-app/todo.db, parameterized queries |
| V. File and Directory Structure | ✅ PASS | src/, tests/, specs/ structure maintained |
| VI. Review and Refactor | ✅ PASS | Incremental changes, ruff checks before commits |
| VII. AI Behavior | ✅ PASS | Using python-todo-cli-dev agent for implementation |

**All gates passed - proceeding to Phase 0.**

## Project Structure

### Documentation (this feature)

```text
specs/004-phase2-advanced-features/
├── plan.md              # This file
├── research.md          # Phase 0 - Database migration, date handling
├── data-model.md        # Phase 1 - Extended Task, new Project entity
├── quickstart.md        # Phase 1 - Testing new features
├── contracts/           # Phase 1 - CLI command contracts
│   ├── list-filters.md  # --today, --overdue, --upcoming filters
│   ├── projects.md      # project create/list/view/delete
│   └── stats.md         # stats command output
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── models.py            # MODIFY: Add due_date, project_id to Task dataclass
├── todo_manager.py      # MODIFY: Add filter methods, stats, project CRUD
├── project_manager.py   # NEW: Project CRUD operations
├── main.py              # MODIFY: New commands, updated add prompts
├── theme.py             # MODIFY: Updated table columns for due_date, project
├── utils.py             # MODIFY: Date validation utilities
└── undo.py              # NEW (optional): Action history for undo

tests/
├── test_todo_manager.py # MODIFY: Tests for new filter methods
├── test_project_manager.py # NEW: Project CRUD tests
├── test_cli.py          # MODIFY: Tests for new CLI commands
├── test_stats.py        # NEW: Statistics calculation tests
└── conftest.py          # MODIFY: Fixtures for projects
```

**Structure Decision**: Single project structure maintained. New files for project_manager.py (separation of concerns) and undo.py (optional feature isolation).

## Complexity Tracking

> No violations - implementation extends existing patterns without adding complexity.

---

## Phase 0: Research

See [research.md](research.md) for detailed findings.

## Phase 1: Design

See:
- [data-model.md](data-model.md) - Extended Task, new Project entity
- [contracts/list-filters.md](contracts/list-filters.md) - Filter command contracts
- [contracts/projects.md](contracts/projects.md) - Project CRUD contracts
- [contracts/stats.md](contracts/stats.md) - Statistics command contract
- [quickstart.md](quickstart.md) - Testing the new features
