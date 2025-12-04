## Spec-Kit Plus – Phase 1 Slash Commands for This Todo App

This file defines the **only 5 slash commands** you will use with Spec‑Kit Plus for this Phase 1 project:

- `/sp.constitution`
- `/sp.specify`
- `/sp.plan`
- `/sp.tasks`
- `/sp.implement`

---

### 1. `/sp.constitution`

#### 📝 AI Prompt Instruction

```
/sp.constitution Create the constitution.md file with project governance rules for a Python console todo application. This document defines rules and regulations ONLY (no tech stack details).

**PROJECT CONTEXT:**
- Building a command-line todo application with SQLite persistence
- Using Python 3.13+ with package manager `uv`
- Following Spec-Driven Development methodology

**GOVERNANCE RULES TO INCLUDE:**

1. **Code Quality Rules:**
   - Always write clean, readable Python code with meaningful variable and function names
   - Always use explicit type hints (Python 3.13+ style) for all functions, methods, and variables
   - Keep functions small and focused on a single responsibility (max 20-30 lines)
   - Follow PEP 8 style guidelines enforced by `ruff` linter
   - Use `dataclasses` for data models instead of plain dictionaries
   - Prefer explicit imports over wildcard imports

2. **Testing Rules:**
   - Prefer test-driven development (write or design tests before/with code)
   - Every new feature or bugfix must have at least basic `pytest` automated tests
   - Never leave failing tests; fix tests before adding new features
   - Use `pytest` as the testing framework with fixtures for database setup/teardown
   - Test edge cases: empty inputs, invalid IDs, already-completed tasks

3. **Spec-Driven Development Rules:**
   - Specs in `specs/` folder must be written or updated BEFORE major code changes
   - Implementation must follow the written spec; if behavior needs to change, update the spec first
   - All CLI behaviors must match the documented console flows exactly
   - Console output messages must match the spec (e.g., "[OK] Task created with ID: X")

4. **Database and Persistence Rules:**
   - All data must persist in SQLite database at `data/todo.db`
   - Never use in-memory only storage; always write to disk
   - Use Python's built-in `sqlite3` module only (no ORMs like SQLAlchemy)
   - Create `data/` directory if it doesn't exist before database operations
   - Use parameterized queries to prevent SQL injection

5. **File and Directory Rules:**
   - Source code goes in `src/` directory
   - Tests go in `tests/` directory
   - Specifications go in `specs/` directory
   - Installation scripts go in `scripts/` directory
   - Database file goes in `data/` directory

6. **Review and Refactor Rules:**
   - Regularly review code to simplify and remove dead/duplicate logic
   - Prefer small, incremental changes over large, risky edits
   - Run `ruff check src/` and `ruff format src/` before every commit
   - No commented-out code should remain in production files

7. **AI Behavior Rules:**
   - AI must not change `constitution.md` or specs unless the user clearly asks for it
   - AI must explain major architectural changes before applying them
   - AI must follow the package manager `uv` for all dependency management
   - AI must respect the Spec-Driven Development workflow order
```

---

### 2. `/sp.specify`

#### 📝 AI Prompt Instruction

```
/sp.specify Create the functional specification for "TODO APP - SQLITE (PHASE 1)" - a console-based todo application with SQLite persistence.

**PROJECT OBJECTIVE:**
Build a command-line todo application that stores tasks in a SQLite database, adhering to Spec-Driven Development principles.

**FUNCTIONAL REQUIREMENTS (Basic Level):**

1. **Add Task**: Create new todo items with title and description
2. **View Task List**: Display all tasks with status indicators ([ ] or [x])
3. **Update Task**: Modify existing task details (title, description)
4. **Delete Task**: Remove tasks from the list by ID
5. **Mark as Complete**: Toggle task completion status

**TASK DATA MODEL:**
Each task has:
- **ID**: Unique integer identifier (auto-generated)
- **Title**: Short text of what needs to be done (required, cannot be empty)
- **Description**: Optional extra details
- **Status**: Either "pending" or "done" (default: pending)
- **Created At**: Timestamp when task was created
- **Updated At**: Timestamp when task was last modified

**CLI COMMANDS:**
Commands: `add`, `list`, `update`, `complete`, `delete`, `help`, `exit`

**CONSOLE INTERFACE DESIGN:**

**Initial Screen / Startup Banner:**
```

====================================
TODO APP - SQLITE (PHASE 1)
====================================
Type 'help' to see available commands.

>

```

**`help` command output:**
```

> help

Available commands:
add - Add a new task
list - Show all tasks
update - Update an existing task (title/description)
complete - Mark a task as completed
delete - Delete a task
exit - Quit the application

>

```

**`add` command flow:**
```

> add
> Enter title: Buy milk
> Enter description: Buy 2 liters of milk from the store.

[OK] Task created with ID: 1

>

```

**`list` command (no tasks):**
```

> list

No tasks found.

>

```

**`list` command (with tasks):**
```

> list

ID Title Status Created At

---

1 Buy milk [ ] Pending 2025-12-04 10:15
2 Finish report [x] Done 2025-12-04 10:30

>

```

**`update` command flow:**
```

> update
> Enter task ID to update: 1
> New title (leave blank to keep current): Buy milk and eggs
> New description (leave blank to keep current):

[OK] Task 1 updated.

>

```

**`complete` command flow:**
```

> complete
> Enter task ID to mark complete: 1

[OK] Task 1 marked as completed.

>

```

**`delete` command flow:**
```

> delete
> Enter task ID to delete: 2

Are you sure you want to delete task 2? (y/n): y

[OK] Task 2 deleted.

>

```

**Invalid command / error handling:**
```

> complet

[ERROR] Unknown command: 'complet'. Type 'help' to see commands.

>

```

**`exit` command:**
```

> exit

Goodbye! 👋

```

**VALIDATION RULES:**
- Title cannot be empty (after trimming whitespace)
- Task ID must be a valid integer
- Task ID must exist in the database for update/complete/delete operations
- Invalid IDs show clear error: "[ERROR] Task not found"
- Empty title shows error and allows retry
- Delete requires confirmation (y/n)
- If task is already completed, show: "Task is already complete."

**NON-FUNCTIONAL REQUIREMENTS:**
- Clear, friendly error messages
- Basic input validation
- Simple, clean console UI
- Data persists across app restarts
```

---

### 3. `/sp.plan`

#### 📝 AI Prompt Instruction

```
/sp.plan Create the technical implementation plan for the todo console application based on the specification.

**TECHNOLOGY STACK:**
- **Python 3.13+**: Core language for the console application
- **Package Manager**: `uv` - manages virtual environment and dependencies, runs app via `uv run`
- **Storage**: SQLite database using Python's built-in `sqlite3` module
- **Database Location**: `data/todo.db`
- **Testing**: `pytest` (dev dependency)
- **Linting/Formatting**: `ruff` (dev dependency)
- **Standard Library**: `dataclasses`, `datetime`, `typing`
- **Optional UI Libraries**: `rich` (for colored output) or `typer` (for CLI parsing) - but standard `input()`/`print()` is sufficient for Basic Level

**DIRECTORY STRUCTURE:**
```

console-todo-app/
├── .venv/ # Virtual environment (managed by uv)
├── data/ # Database folder
│ └── todo.db # SQLite database file (auto-created)
├── specs/ # Specification history
│ └── 001_initial_phase1_spec.md
├── src/ # Source code
│ ├── **init**.py
│ ├── main.py # Entry point (CLI loop)
│ ├── models.py # Data models (Task dataclass)
│ ├── todo_manager.py # Business logic (CRUD operations with SQLite)
│ └── utils.py # Helpers (formatting, input handling)
├── tests/ # Unit tests
│ ├── **init**.py
│ └── test_todo_manager.py
├── scripts/ # Installation scripts
│ ├── install.sh # Linux/macOS one-command install
│ └── install.ps1 # Windows PowerShell install
├── Specification-phase-1/ # Phase 1 specification documents
├── .gitignore
├── CLAUDE.md # Instructions for AI assistant
├── constitution.md # Project rules and guidelines
├── pyproject.toml # Project configuration (uv)
└── README.md # Setup and usage instructions

````

**DATA MODEL (`src/models.py`):**
```python
@dataclass
class Task:
    id: int
    title: str
    description: str
    status: str  # "pending" or "done"
    created_at: datetime
    updated_at: datetime
````

**DATABASE SCHEMA (`data/todo.db`):**

- Table: `tasks`
- Columns:
  - `id` INTEGER PRIMARY KEY AUTOINCREMENT
  - `title` TEXT NOT NULL
  - `description` TEXT
  - `status` TEXT DEFAULT 'pending'
  - `created_at` TEXT (ISO format datetime)
  - `updated_at` TEXT (ISO format datetime)

**BUSINESS LOGIC (`src/todo_manager.py`):**
`TodoManager` class with SQLite database as single source of truth:

- `__init__(db_path)`: Connect to SQLite, create table if not exists
- `add_task(title, description)` → INSERT into tasks table, return new Task
- `list_tasks()` → SELECT all tasks ordered by id, return List[Task]
- `get_task(id)` → SELECT single task by id, return Task or None
- `update_task(id, title=None, description=None)` → UPDATE matching row
- `complete_task(id)` → UPDATE status to 'done'
- `delete_task(id)` → DELETE the row

**CLI (`src/main.py`):**

- Show startup banner
- Infinite loop with `> ` prompt waiting for user input
- Parse command and call appropriate handler
- Commands: `add`, `list`, `update`, `complete`, `delete`, `exit`, `help`
- Formatted output matching the spec exactly
- Error handling for invalid commands and inputs

**DEVELOPMENT PHASES:**

1. Project initialization with `uv init`
2. Implement `Task` dataclass in `src/models.py`
3. Implement `TodoManager` with SQLite CRUD in `src/todo_manager.py`
4. Implement CLI loop in `src/main.py`
5. Add `pytest` tests for `TodoManager`
6. Create installation scripts
7. Document in README.md

**ONE-COMMAND INSTALLATION:**

- **Linux/macOS (bash/zsh):**

  ```bash
  curl -LsSf https://raw.githubusercontent.com/<USER>/<REPO>/main/scripts/install.sh | bash
  ```

  Script will: install `uv` if needed, clone repo, run `uv sync`, create wrapper command

- **Windows (PowerShell):**
  ```powershell
  powershell -ExecutionPolicy Bypass -Command "irm https://raw.githubusercontent.com/<USER>/<REPO>/main/scripts/install.ps1 | iex"
  ```
  Script will: download repo, ensure Python and uv available, set up environment

```

---

### 4. `/sp.tasks`

#### 📝 AI Prompt Instruction

```

/sp.tasks

```

> **Note:** This command takes NO arguments. The AI will automatically read the plan from `/sp.plan` and break it into tasks.

#### 📋 Expected Output (Tasks the AI Should Generate)

The AI should create the following **35 tasks across 6 phases**:

**PHASE 1: PROJECT INITIALIZATION**
- Task 1: Run `uv init` to initialize the project, set Python 3.13+ in pyproject.toml
- Task 2: Add dev dependencies: `uv add --dev pytest ruff`
- Task 3: Create directory structure: `src/`, `tests/`, `specs/`, `data/`, `scripts/`, `Specification-phase-1/`
- Task 4: Create `src/__init__.py` and `tests/__init__.py` (empty files)
- Task 5: Create `.gitignore` with: `.venv/`, `data/*.db`, `__pycache__/`, `*.pyc`

**PHASE 2: DATA MODEL**
- Task 6: Create `src/models.py` with `Task` dataclass (id, title, description, status, created_at, updated_at)

**PHASE 3: DATABASE & TODO MANAGER**
- Task 7: Create `src/todo_manager.py` with `TodoManager` class skeleton and `_create_table()`
- Task 8: Implement `add_task(title, description)` method
- Task 9: Implement `list_tasks()` method
- Task 10: Implement `get_task(id)` method
- Task 11: Implement `update_task(id, title=None, description=None)` method
- Task 12: Implement `complete_task(id)` method
- Task 13: Implement `delete_task(id)` method

**PHASE 4: CLI INTERFACE**
- Task 14: Create `src/main.py` with startup banner and main loop
- Task 15: Implement `help` command handler
- Task 16: Implement `add` command handler
- Task 17: Implement `list` command handler
- Task 18: Implement `update` command handler
- Task 19: Implement `complete` command handler
- Task 20: Implement `delete` command handler
- Task 21: Implement `exit` command handler
- Task 22: Add error handling for unknown commands

**PHASE 5: TESTING**
- Task 23: Create `tests/test_todo_manager.py` with pytest fixtures
- Task 24-29: Write tests for each TodoManager method
- Task 30: Write edge case tests

**PHASE 6: DOCUMENTATION & INSTALLATION**
- Task 31: Create `scripts/install.sh` for Linux/macOS
- Task 32: Create `scripts/install.ps1` for Windows PowerShell
- Task 33: Create `README.md`
- Task 34: Create `CLAUDE.md`
- Task 35: Create `specs/001_initial_phase1_spec.md`

---

### 5. `/sp.implement`

#### 📝 AI Prompt Instruction

```

/sp.implement

````

> **Note:** This command takes NO arguments. The AI will automatically read the tasks from `/sp.tasks` and execute them in order.

#### 📋 What the AI Will Do

**IMPLEMENTATION ORDER:**
1. Phase 1 (Tasks 1-5): Project initialization and directory structure
2. Phase 2 (Task 6): Data model - Task dataclass
3. Phase 3 (Tasks 7-13): TodoManager with SQLite CRUD operations
4. Phase 4 (Tasks 14-22): CLI interface with all commands
5. Phase 5 (Tasks 23-30): pytest tests
6. Phase 6 (Tasks 31-35): Documentation and installation scripts

#### 📋 Key Implementation Rules (AI Must Follow)

- Follow the spec exactly - console output must match the specified format
- Use type hints for all functions and methods
- Use `sqlite3` module only (no ORMs)
- Use `dataclasses` for the Task model
- Create `data/` directory before database operations if it doesn't exist
- Use parameterized queries for SQL (prevent injection)
- Follow constitution.md rules for code quality

#### 📋 Console Output Format (Must Match Exactly)

| Action | Output Message |
|--------|----------------|
| Add task | `[OK] Task created with ID: 1` |
| Update task | `[OK] Task 1 updated.` |
| Complete task | `[OK] Task 1 marked as completed.` |
| Delete task | `[OK] Task 1 deleted.` |
| Unknown command | `[ERROR] Unknown command: 'X'. Type 'help' to see commands.` |
| Task not found | `[ERROR] Task not found` |
| Exit | `Goodbye! 👋` |

#### 📋 Validation Checkpoints

- After Phase 2: `python -c "from src.models import Task; print('Models OK')"`
- After Phase 3: Run `uv run pytest tests/test_todo_manager.py`
- After Phase 4: Run `uv run python -m src.main` and test all commands
- After Phase 5: Run `uv run pytest` - all tests should pass
- After Phase 6: Test installation scripts

#### 📋 Run Commands

```bash
# Run the app
uv run python -m src.main

# Run tests
uv run pytest

# Lint code
uv run ruff check src/

# Format code
uv run ruff format src/
````

---

## Summary

| Command            | Purpose                         | Key Details from plan.md                                                             |
| ------------------ | ------------------------------- | ------------------------------------------------------------------------------------ |
| `/sp.constitution` | Create project governance rules | Code quality, testing, spec-driven development, database, AI behavior rules          |
| `/sp.specify`      | Define functional requirements  | All CLI commands, console flows, validation rules, exact output messages             |
| `/sp.plan`         | Technical implementation plan   | Python 3.13+, uv, SQLite, directory structure, TodoManager API, installation scripts |
| `/sp.tasks`        | Break into numbered tasks       | 35 tasks across 6 phases: setup, model, CRUD, CLI, testing, docs                     |
| `/sp.implement`    | Execute the implementation      | Implementation order, templates, validation checkpoints, exact output format         |

```

```
