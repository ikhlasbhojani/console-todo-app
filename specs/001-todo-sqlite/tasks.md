# Tasks: TODO APP - SQLITE (PHASE 1)

**Input**: Design documents from `/specs/001-todo-sqlite/`
**Prerequisites**: plan.md (required), spec.md (required), data-model.md, contracts/cli-commands.md, quickstart.md

**Tests**: Tests are included following TDD approach per constitution (Principle II).

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Paths shown below follow the plan.md structure

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [x] T001 Initialize project with `uv init` and configure pyproject.toml with Python 3.13+ requirement
- [x] T002 [P] Create directory structure: src/, tests/, data/, scripts/ per plan.md
- [x] T003 [P] Create src/__init__.py package marker file
- [x] T004 [P] Create tests/__init__.py package marker file
- [x] T005 [P] Configure ruff linter settings in pyproject.toml (line-length=100, target Python 3.13)
- [x] T006 Add pytest as dev dependency in pyproject.toml via `uv add --dev pytest`
- [x] T007 Add ruff as dev dependency in pyproject.toml via `uv add --dev ruff`
- [x] T008 Run `uv sync` to create virtual environment and install dependencies

**Checkpoint**: Project structure ready, `uv run pytest` runs (with no tests yet)

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T009 Implement Task dataclass with all attributes in src/models.py (id, title, description, status, created_at, updated_at)
- [x] T010 [P] Add Task.from_row() classmethod to create Task from sqlite3.Row in src/models.py
- [x] T011 [P] Add Task.is_completed() method returning bool in src/models.py
- [x] T012 [P] Add Task.format_status() method returning "[ ] Pending" or "[x] Done" in src/models.py
- [x] T013 [P] Add Task.format_date() method returning "YYYY-MM-DD HH:MM" string in src/models.py
- [x] T014 Create TodoManager class with __init__(db_path) in src/todo_manager.py
- [x] T015 Implement _get_connection() method with row_factory in src/todo_manager.py
- [x] T016 Implement _init_db() to create tasks table if not exists in src/todo_manager.py
- [x] T017 Create pytest fixtures in tests/conftest.py (temp_db, todo_manager, sample_task)
- [x] T018 Create src/utils.py with validate_task_id() function returning tuple[bool, int | str]
- [x] T019 [P] Add validate_title() function to src/utils.py returning tuple[bool, str]
- [x] T020 [P] Add format_task_table() function to src/utils.py for list display formatting

**Checkpoint**: Foundation ready - Task model works, TodoManager connects to DB, fixtures available

---

## Phase 3: User Story 1 - Add and View Tasks (Priority: P1)

**Goal**: Users can add new tasks and view all tasks in a formatted list

**Independent Test**: Run `add` command, enter title/description, verify task created; run `list` to see tasks

### Tests for User Story 1

- [x] T021 [P] [US1] Write test_add_task_success in tests/test_todo_manager.py
- [x] T022 [P] [US1] Write test_add_task_empty_title_raises_error in tests/test_todo_manager.py
- [x] T023 [P] [US1] Write test_list_tasks_returns_all_tasks in tests/test_todo_manager.py
- [x] T024 [P] [US1] Write test_list_tasks_empty_returns_empty_list in tests/test_todo_manager.py

### Implementation for User Story 1

- [x] T025 [US1] Implement add_task(title, description) method in src/todo_manager.py (INSERT + return Task)
- [x] T026 [US1] Implement list_tasks() method in src/todo_manager.py (SELECT all ORDER BY id)
- [x] T027 [US1] Create main CLI loop skeleton in src/main.py with startup banner
- [x] T028 [US1] Implement command dispatcher (case-insensitive) in src/main.py
- [x] T029 [US1] Implement handle_add() function in src/main.py (prompt title/description, validate, create)
- [x] T030 [US1] Implement handle_list() function in src/main.py (fetch tasks, format table or "No tasks found")
- [x] T031 [US1] Run tests: `uv run pytest tests/test_todo_manager.py -v`

**Checkpoint**: US1 complete - `add` and `list` commands work, tests pass

---

## Phase 4: User Story 2 - Mark Tasks Complete (Priority: P2)

**Goal**: Users can mark pending tasks as completed

**Independent Test**: Create task, run `complete` with task ID, verify status changes to [x] Done

### Tests for User Story 2

- [x] T032 [P] [US2] Write test_complete_task_success in tests/test_todo_manager.py
- [x] T033 [P] [US2] Write test_complete_task_not_found in tests/test_todo_manager.py
- [x] T034 [P] [US2] Write test_complete_task_already_done in tests/test_todo_manager.py

### Implementation for User Story 2

- [x] T035 [US2] Implement get_task(task_id) method in src/todo_manager.py (SELECT by id)
- [x] T036 [US2] Implement complete_task(task_id) method in src/todo_manager.py returning tuple[bool, str]
- [x] T037 [US2] Implement handle_complete() function in src/main.py (prompt ID, validate, complete)
- [x] T038 [US2] Run tests: `uv run pytest tests/test_todo_manager.py -v -k complete`

**Checkpoint**: US2 complete - `complete` command works, tests pass

---

## Phase 5: User Story 3 - Update Task Details (Priority: P3)

**Goal**: Users can update title and/or description of existing tasks

**Independent Test**: Create task, run `update` with task ID, change title, verify changes in `list`

### Tests for User Story 3

- [x] T039 [P] [US3] Write test_update_task_title_only in tests/test_todo_manager.py
- [x] T040 [P] [US3] Write test_update_task_description_only in tests/test_todo_manager.py
- [x] T041 [P] [US3] Write test_update_task_not_found in tests/test_todo_manager.py
- [x] T042 [P] [US3] Write test_update_task_preserves_unchanged_fields in tests/test_todo_manager.py

### Implementation for User Story 3

- [x] T043 [US3] Implement update_task(task_id, title, description) method in src/todo_manager.py
- [x] T044 [US3] Implement handle_update() function in src/main.py (prompt ID, new values, validate, update)
- [x] T045 [US3] Run tests: `uv run pytest tests/test_todo_manager.py -v -k update`

**Checkpoint**: US3 complete - `update` command works, tests pass

---

## Phase 6: User Story 4 - Delete Tasks (Priority: P4)

**Goal**: Users can delete tasks with confirmation prompt

**Independent Test**: Create task, run `delete` with task ID, confirm with 'y', verify task removed from `list`

### Tests for User Story 4

- [x] T046 [P] [US4] Write test_delete_task_success in tests/test_todo_manager.py
- [x] T047 [P] [US4] Write test_delete_task_not_found in tests/test_todo_manager.py

### Implementation for User Story 4

- [x] T048 [US4] Implement delete_task(task_id) method in src/todo_manager.py (DELETE by id)
- [x] T049 [US4] Implement handle_delete() function in src/main.py (prompt ID, confirm y/n, delete)
- [x] T050 [US4] Run tests: `uv run pytest tests/test_todo_manager.py -v -k delete`

**Checkpoint**: US4 complete - `delete` command works with confirmation, tests pass

---

## Phase 7: User Story 5 - Application Navigation (Priority: P5)

**Goal**: Users can see help, exit gracefully, and get clear error for unknown commands

**Independent Test**: Run `help` to see commands, run `exit` to quit, run invalid command to see error

### Tests for User Story 5

- [x] T051 [P] [US5] Write test_unknown_command_error in tests/test_cli.py
- [x] T052 [P] [US5] Write test_help_displays_all_commands in tests/test_cli.py

### Implementation for User Story 5

- [x] T053 [US5] Implement handle_help() function in src/main.py (print command list)
- [x] T054 [US5] Implement handle_exit() function in src/main.py (print "Goodbye!", return exit flag)
- [x] T055 [US5] Implement handle_unknown(cmd) function in src/main.py (print error message)
- [x] T056 [US5] Wire up all handlers in command dispatcher in src/main.py
- [x] T057 [US5] Run all tests: `uv run pytest -v`

**Checkpoint**: US5 complete - `help`, `exit`, unknown commands work, all tests pass

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final testing, documentation, and installation scripts

- [x] T058 [P] Run full test suite: `uv run pytest -v --tb=short`
- [x] T059 [P] Run linter: `uv run ruff check src/ tests/`
- [x] T060 [P] Run formatter: `uv run ruff format src/ tests/`
- [x] T061 [P] Create scripts/install.sh for Linux/macOS installation
- [x] T062 [P] Create scripts/install.ps1 for Windows PowerShell installation
- [x] T063 Manual test: Run full user flow (add → list → complete → update → delete → exit)
- [x] T064 Verify data persistence: Add tasks, exit, restart, verify tasks remain

**Checkpoint**: All tests pass, linting clean, installation scripts work, persistence verified

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-7)**: All depend on Foundational phase completion
  - User stories can proceed sequentially in priority order (P1 → P2 → P3 → P4 → P5)
  - Or in parallel if team capacity allows
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

| Story | Can Start After | Dependencies on Other Stories |
|-------|-----------------|-------------------------------|
| US1 (P1) | Phase 2 complete | None - standalone |
| US2 (P2) | Phase 2 complete | None (uses add from US1 for setup, but independently testable) |
| US3 (P3) | Phase 2 complete | None (uses add from US1 for setup, but independently testable) |
| US4 (P4) | Phase 2 complete | None (uses add from US1 for setup, but independently testable) |
| US5 (P5) | Phase 2 complete | None - standalone |

### Within Each User Story

1. Tests MUST be written first (TDD per constitution)
2. Tests MUST fail before implementation
3. Models/Services before handlers
4. Run story-specific tests after implementation
5. Story complete when all its tests pass

### Parallel Opportunities

**Phase 1** (4 parallel tasks):
```
T002, T003, T004, T005 can run in parallel
```

**Phase 2** (5 parallel tasks):
```
T010, T011, T012, T013 can run in parallel (all Task methods)
T018, T019, T020 can run in parallel (all utils functions)
```

**Each User Story** (tests in parallel):
```
US1: T021, T022, T023, T024 can run in parallel
US2: T032, T033, T034 can run in parallel
US3: T039, T040, T041, T042 can run in parallel
US4: T046, T047 can run in parallel
US5: T051, T052 can run in parallel
```

**Phase 8** (4 parallel tasks):
```
T058, T059, T060, T061, T062 can run in parallel
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational
3. Complete Phase 3: User Story 1 (Add and View)
4. **STOP and VALIDATE**: Test US1 independently with manual verification
5. Deploy/demo if ready - users can add and view tasks!

### Incremental Delivery

| Increment | Stories | Capability |
|-----------|---------|------------|
| MVP | US1 | Add tasks, view task list |
| +Complete | US1 + US2 | Track task completion |
| +Update | US1-3 | Edit task details |
| +Delete | US1-4 | Full CRUD operations |
| Full | US1-5 | Complete app with help/exit |

### Recommended Execution Order

```
Phase 1 (Setup)           → 8 tasks, ~15 min
Phase 2 (Foundational)    → 12 tasks, ~30 min
Phase 3 (US1: Add/View)   → 11 tasks, ~45 min  ← MVP HERE
Phase 4 (US2: Complete)   → 7 tasks, ~20 min
Phase 5 (US3: Update)     → 7 tasks, ~20 min
Phase 6 (US4: Delete)     → 5 tasks, ~15 min
Phase 7 (US5: Navigation) → 7 tasks, ~15 min
Phase 8 (Polish)          → 7 tasks, ~20 min
                          ─────────────────────
                          TOTAL: 64 tasks
```

---

## Task Summary

| Phase | Tasks | Parallel | Story |
|-------|-------|----------|-------|
| Setup | 8 | 4 | - |
| Foundational | 12 | 7 | - |
| US1: Add/View | 11 | 4 | P1 |
| US2: Complete | 7 | 3 | P2 |
| US3: Update | 7 | 4 | P3 |
| US4: Delete | 5 | 2 | P4 |
| US5: Navigation | 7 | 2 | P5 |
| Polish | 7 | 5 | - |
| **TOTAL** | **64** | **31** | - |

### Agent Assignment

| Phase | Agent |
|-------|-------|
| Setup (T001-T008) | python-todo-cli-dev |
| Foundational (T009-T020) | python-todo-cli-dev |
| US1-US5 Tests | todo-testing-agent |
| US1-US5 Implementation | python-todo-cli-dev |
| Polish - Scripts (T061-T062) | todo-docs-writer |
| Polish - Testing (T058-T060, T063-T064) | todo-testing-agent |

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- Verify tests fail before implementing (TDD)
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Run `uv run ruff check src/ tests/` before commits (constitution requirement)
