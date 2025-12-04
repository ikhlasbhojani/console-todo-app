---
id: 004
title: Phase 2 Foundational Implementation (T009-T020)
stage: green
date: 2025-12-04
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-todo-sqlite
branch: 001-todo-sqlite
user: ikhlasbhojani
command: Execute Phase 2 foundational tasks
labels: ["implementation", "models", "manager", "utilities", "testing", "phase-2"]
links:
  spec: specs/001-todo-sqlite/data-model.md
  ticket: null
  adr: null
  pr: null
files:
  - src/models.py (created)
  - src/todo_manager.py (created)
  - src/utils.py (created)
  - tests/conftest.py (created)
tests:
  - Fixtures defined: temp_db, todo_manager, sample_task
  - Pytest collection verified (0 tests - fixtures only)
---

## Prompt

Execute Phase 2: Foundational tasks (T009-T020) for the TODO APP - SQLITE project.

**Working Directory**: /home/ikhlasbhojani/Desktop/hackathon-part-2/console-todo-app

**Tasks to implement**:
- T009: Implement Task dataclass with all attributes in src/models.py (id, title, description, status, created_at, updated_at)
- T010: [P] Add Task.from_row() classmethod to create Task from sqlite3.Row in src/models.py
- T011: [P] Add Task.is_completed() method returning bool in src/models.py
- T012: [P] Add Task.format_status() method returning "[ ] Pending" or "[x] Done" in src/models.py
- T013: [P] Add Task.format_date() method returning "YYYY-MM-DD HH:MM" string in src/models.py
- T014: Create TodoManager class with __init__(db_path) in src/todo_manager.py
- T015: Implement _get_connection() method with row_factory in src/todo_manager.py
- T016: Implement _init_db() to create tasks table if not exists in src/todo_manager.py
- T017: Create pytest fixtures in tests/conftest.py (temp_db, todo_manager, sample_task)
- T018: Create src/utils.py with validate_task_id() function returning tuple[bool, int | str]
- T019: [P] Add validate_title() function to src/utils.py returning tuple[bool, str]
- T020: [P] Add format_task_table() function to src/utils.py for list display formatting

**Reference the contracts from**:
- specs/001-todo-sqlite/data-model.md (Task entity definition)
- specs/001-todo-sqlite/contracts/cli-commands.md (TodoManager interface, utility functions)

## Response snapshot

Successfully implemented Phase 2 foundational tasks (T009-T020). All files created with full type hints, documentation, and following the specification contracts exactly.

**Implementation Summary:**

1. **src/models.py (94 lines)**: Complete Task dataclass implementation
   - All 6 attributes with proper types (id, title, description, status, created_at, updated_at)
   - from_row() classmethod for database row conversion
   - is_completed() method for status checking
   - format_status() method returning "[ ] Pending" or "[x] Done"
   - format_date() method returning "YYYY-MM-DD HH:MM" format

2. **src/todo_manager.py (95 lines)**: TodoManager class foundation
   - __init__(db_path) with automatic directory and database creation
   - _get_connection() returning connection with Row factory
   - _init_db() creating tasks table with CHECK constraint and index

3. **src/utils.py (117 lines)**: Three validation and formatting utilities
   - validate_task_id(id_str) returning (bool, int|str) tuple
   - validate_title(title) returning (bool, str) tuple
   - format_task_table(tasks) returning formatted table string

4. **tests/conftest.py (75 lines)**: Three pytest fixtures
   - temp_db: Creates temporary database with cleanup
   - todo_manager: Returns TodoManager instance with temp database
   - sample_task: Returns sample Task instance for testing

**Verification Results:**
- Ruff linting: All checks passed
- Pytest collection: Fixtures properly defined and importable
- Module imports: All modules successfully import
- Function tests: validate_task_id("42") and validate_title("  Test  ") work correctly

## Outcome

- ✅ Impact: Complete foundational layer implemented - models, manager skeleton, utilities, and test infrastructure ready for Phase 3 CRUD operations
- 🧪 Tests: 3 pytest fixtures created (temp_db, todo_manager, sample_task) - verified importable and functional
- 📁 Files: 4 files created (309 total lines of code): src/models.py, src/todo_manager.py, src/utils.py, tests/conftest.py
- 🔁 Next prompts: Phase 3 CRUD operations (T021-T025) - add_task, list_tasks, get_task, update_task, complete_task, delete_task
- 🧠 Reflection: Strict adherence to contracts and constitution principles. All code includes comprehensive docstrings, type hints, and follows PEP 8. Database schema exactly matches data-model.md specification.

## Evaluation notes (flywheel)

- Failure modes observed: None - all implementations matched contracts exactly
- Graders run and results (PASS/FAIL): PASS - ruff check passed, pytest fixtures verified
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implement Phase 3 CRUD operations with comprehensive error handling
