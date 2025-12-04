# Implementation Plan: TODO APP - SQLITE (PHASE 1)

**Branch**: `001-todo-sqlite` | **Date**: 2025-12-04 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-todo-sqlite/spec.md`

## Summary

Build a console-based todo application with SQLite persistence that allows users to manage tasks through CLI commands (add, list, update, complete, delete). The application uses Python 3.13+ with `uv` package manager, stores data in `data/todo.db`, and follows a clean architecture with dataclass models, a manager class for business logic, and a CLI loop for user interaction.

## Technical Context

**Language/Version**: Python 3.13+
**Primary Dependencies**: None (standard library only: `sqlite3`, `dataclasses`, `datetime`, `typing`)
**Storage**: SQLite database at `data/todo.db`
**Testing**: pytest (dev dependency)
**Target Platform**: Cross-platform (Linux, macOS, Windows) console application
**Project Type**: Single project
**Performance Goals**: Instant response (<100ms) for all operations; handles hundreds of tasks
**Constraints**: No external runtime dependencies; offline-capable; single-user
**Scale/Scope**: Single user, local storage, ~100-1000 tasks typical usage

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Requirement | Status |
|-----------|-------------|--------|
| I. Code Quality | Type hints on all functions, dataclasses for models, PEP 8 via ruff | PASS |
| II. Testing | pytest with fixtures, edge case coverage | PASS |
| III. Spec-Driven Development | Spec exists at specs/001-todo-sqlite/spec.md | PASS |
| IV. Database/Persistence | SQLite at data/todo.db, parameterized queries | PASS |
| V. File/Directory Structure | src/, tests/, specs/, scripts/, data/ | PASS |
| VI. Review/Refactor | ruff check/format before commits | PASS |
| VII. AI Behavior | Using python-todo-cli-dev agent for implementation | PASS |

**Gate Status**: ALL PASS - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-todo-sqlite/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (internal CLI contracts)
│   └── cli-commands.md  # Command interface specification
└── tasks.md             # Phase 2 output (/sp.tasks command)
```

### Source Code (repository root)

```text
src/
├── __init__.py          # Package marker
├── main.py              # Entry point: CLI loop, command dispatcher
├── models.py            # Task dataclass
├── todo_manager.py      # Business logic: CRUD operations with SQLite
└── utils.py             # Helpers: formatting, input validation

tests/
├── __init__.py          # Package marker
├── conftest.py          # pytest fixtures (temp database)
├── test_models.py       # Task dataclass tests
├── test_todo_manager.py # CRUD operation tests
└── test_cli.py          # CLI integration tests

data/
└── todo.db              # SQLite database (auto-created)

scripts/
├── install.sh           # Linux/macOS installation
└── install.ps1          # Windows PowerShell installation
```

**Structure Decision**: Single project layout selected. This is a simple CLI application with no web/mobile components. All source code in `src/`, all tests in `tests/`, data persistence in `data/`.

## Complexity Tracking

> No constitution violations. Design follows all principles.

| Aspect | Decision | Rationale |
|--------|----------|-----------|
| No ORM | Direct sqlite3 | Constitution requires sqlite3 only; simpler for this scale |
| No CLI framework | Standard input() | Sufficient for basic level; no typer/click complexity |
| Single manager class | TodoManager | Single entity (Task) doesn't need multiple managers |

---

## Phase 0: Research Summary

See [research.md](./research.md) for full details.

### Key Decisions

1. **Database Connection Strategy**: Per-operation connection with context managers
   - Rationale: Simpler than connection pooling; adequate for single-user CLI
   - Alternative rejected: Persistent connection (risk of lock issues)

2. **ID Generation**: SQLite AUTOINCREMENT
   - Rationale: Built-in, handles gaps correctly, no application logic needed
   - Alternative rejected: Application-managed IDs (complexity, race conditions)

3. **Datetime Storage**: ISO 8601 strings in SQLite TEXT columns
   - Rationale: Human-readable, sortable, standard format
   - Alternative rejected: Unix timestamps (less readable in raw DB inspection)

4. **Input Validation**: Centralized in utils.py with clear error returns
   - Rationale: Reusable across commands, consistent error messages
   - Alternative rejected: Inline validation (code duplication)

5. **Output Formatting**: Simple string formatting with fixed-width columns
   - Rationale: Works in all terminals, no color dependencies
   - Alternative rejected: rich library (adds dependency for basic level)

---

## Phase 1: Design Artifacts

### Data Model

See [data-model.md](./data-model.md) for full entity definitions.

**Task Entity**:
```python
@dataclass
class Task:
    id: int
    title: str
    description: str
    status: str  # "pending" | "done"
    created_at: datetime
    updated_at: datetime
```

**Database Schema**:
```sql
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT DEFAULT '',
    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'done')),
    created_at TEXT NOT NULL,
    updated_at TEXT NOT NULL
);
```

### API Contracts

See [contracts/cli-commands.md](./contracts/cli-commands.md) for full interface specification.

**TodoManager Interface**:
```python
class TodoManager:
    def __init__(self, db_path: str = "data/todo.db") -> None: ...
    def add_task(self, title: str, description: str = "") -> Task: ...
    def list_tasks(self) -> list[Task]: ...
    def get_task(self, task_id: int) -> Task | None: ...
    def update_task(self, task_id: int, title: str | None = None,
                    description: str | None = None) -> bool: ...
    def complete_task(self, task_id: int) -> tuple[bool, str]: ...
    def delete_task(self, task_id: int) -> bool: ...
```

### Quickstart

See [quickstart.md](./quickstart.md) for setup and run instructions.

**Quick Commands**:
```bash
# Setup
uv sync

# Run
uv run python -m src.main

# Test
uv run pytest

# Lint
uv run ruff check src/ tests/
uv run ruff format src/ tests/
```

---

## Implementation Phases Summary

### Phase 1: Setup (Shared Infrastructure)
- T001: Initialize project with `uv init`, configure pyproject.toml
- T002: Create directory structure (src/, tests/, data/, scripts/)
- T003: Configure ruff in pyproject.toml

### Phase 2: Foundational (Blocking Prerequisites)
- T004: Implement Task dataclass in src/models.py
- T005: Implement database initialization in TodoManager
- T006: Create pytest fixtures in tests/conftest.py

### Phase 3: User Story 1 - Add and View Tasks (P1)
- T007-T012: Implement add_task, list_tasks, CLI handlers

### Phase 4: User Story 2 - Mark Tasks Complete (P2)
- T013-T016: Implement complete_task, CLI handler

### Phase 5: User Story 3 - Update Task Details (P3)
- T017-T020: Implement update_task, CLI handler

### Phase 6: User Story 4 - Delete Tasks (P4)
- T021-T024: Implement delete_task with confirmation, CLI handler

### Phase 7: User Story 5 - Application Navigation (P5)
- T025-T028: Implement help, exit, unknown command handling

### Phase 8: Polish
- T029-T032: Documentation, installation scripts, final testing

---

## Next Steps

1. Run `/sp.tasks` to generate detailed task breakdown
2. Use `python-todo-cli-dev` agent for implementation
3. Use `todo-testing-agent` for test creation
4. Use `todo-docs-writer` for documentation
