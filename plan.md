# Phase 1: Todo Console App with SQLite Persistence - Implementation Plan

## 0. Technologies, Libraries & Their Purpose

- **Python 3.13+**: Core language to build the console-based todo application.
- **Standard Library (`dataclasses`, `datetime`, `typing`)**: 
  - `dataclasses` for defining the `Task` model in a clean, structured way.
  - `datetime` for storing `created_at` and `updated_at` timestamps.
  - `typing` for type hints (e.g., `List[Task]`) to keep the code clear and maintainable.
- **SQLite (`sqlite3` standard library module)**: Primary storage for all tasks in **Phase 1**; data is stored in a local `.db` file and persists across app restarts.
- **Package Manager: `uv`**: Manages the virtual environment and dependencies, and runs the app via `uv run`.
- **Testing: `pytest` (dev dependency)**: Used to write and run unit tests for `TodoManager` and other logic.
- **Linting/Formatting: `ruff` (dev dependency)**: Ensures code quality, consistent style, and catches common errors early.
- **Optional UI Libraries**:
  - **`rich`**: For more beautiful and readable terminal output (colored text, tables, etc.) if richer console UI is desired.
  - **`typer`**: For structured CLI command parsing instead of manual `input()` handling, if we later decide to upgrade the CLI experience.

## 1. Project Overview

**Objective:** Build a command-line todo application that stores tasks in memory, adhering to Spec-Driven Development principles.

## 2. Requirements Analysis

### Functional Requirements (Basic Level)

1.  **Add Task**: Create new todo items with title and description.
2.  **View Task List**: Display all tasks with status indicators (e.g., [x] or [ ]).
3.  **Update Task**: Modify existing task details (title, description).
4.  **Delete Task**: Remove tasks from the list by ID.
5.  **Mark as Complete**: Toggle task completion status.

### Technical Requirements

- **Language**: Python 3.13+
- **Package Manager**: `uv`
- **Storage**: Local SQLite database using Python’s built-in `sqlite3` module so tasks persist across app restarts (no in-memory-only mode).
- **Development Methodology**: Spec-Driven Development (using Spec-Kit Plus principles).

### Deliverables

- GitHub Repository structure:
  - `constitution.md` (Project rules and guidelines)
  - `specs/` (Folder for specification history)
  - `src/` (Source code)
  - `README.md` (Setup and usage instructions)
  - `CLAUDE.md` (Instructions for AI assistant)

## 3. Architecture & Design

### Directory Structure

```
console-todo-app/
├── .venv/                  # Virtual environment (managed by uv)
├── specs/                  # Specification history
│   └── 001_initial_phase1_spec.md
├── src/                    # Source code
│   ├── __init__.py
│   ├── main.py             # Entry point (CLI loop)
│   ├── models.py           # Data models (Task class)
│   ├── todo_manager.py     # Business logic (CRUD operations, uses SQLite)
│   └── utils.py            # Helpers (formatting, input handling)
├── tests/                  # Unit tests
│   ├── __init__.py
│   └── test_todo_manager.py
├── .gitignore
├── CLAUDE.md
├── constitution.md
├── pyproject.toml          # Project configuration (uv)
└── README.md
```

### Data Model (`models.py`)

- **Task Class**:
  - `id`: int (Unique identifier)
  - `title`: str
  - `description`: str
  - `status`: str (or bool for is_completed) - Default: Pending/False
  - `created_at`: datetime
  - `updated_at`: datetime

### Persistence with SQLite (`sqlite3`)

Phase 1 will **directly** use **SQLite** via Python’s built-in `sqlite3` module:

- **Database file location**: `data/todo.db`.
- **Main table**: `tasks`
  - `id` INTEGER PRIMARY KEY AUTOINCREMENT
  - `title` TEXT NOT NULL
  - `description` TEXT
  - `status` TEXT (e.g., `"pending"` / `"done"`)
  - `created_at` TEXT / DATETIME
  - `updated_at` TEXT / DATETIME

All core operations (`add`, `list`, `update`, `complete`, `delete`) in Phase 1 will read/write directly to this SQLite database so that tasks persist across app restarts.

### Business Logic (`todo_manager.py`)

- `TodoManager` Class:
  - Uses a SQLite database (via `sqlite3`) as the **single source of truth** for tasks.
  - `add_task(title, description)` → `INSERT` into `tasks` table.
  - `list_tasks()` → `SELECT` all tasks (optionally ordered by created date or ID).
  - `get_task(id)` → `SELECT` a single task by `id`.
  - `update_task(id, title=None, description=None)` → `UPDATE` the matching row.
  - `complete_task(id)` → `UPDATE status` to completed/done.
  - `delete_task(id)` → `DELETE` the row (or mark as deleted if we choose soft-delete later).

### User Interface (`main.py`)

- Infinite loop waiting for user input.
- Commands: `add`, `list`, `update`, `complete`, `delete`, `exit`, `help`.
- Formatted output (tables or clean text).

### Console Interface Design (Example)

Below is an example of how the console-based UI should look and behave. This is **not strict**, but a target style for clarity and consistency.

**Initial screen / prompt**

```text
====================================
  TODO APP - SQLITE (PHASE 1)
====================================
Type 'help' to see available commands.

> 
```

**`help` command**

```text
> help

Available commands:
  add         - Add a new task
  list        - Show all tasks
  update      - Update an existing task (title/description)
  complete    - Mark a task as completed
  delete      - Delete a task
  exit        - Quit the application

> 
```

**`add` command**

```text
> add
Enter title: Buy milk
Enter description: Buy 2 liters of milk from the store.

[OK] Task created with ID: 1

> 
```

**`list` command (no tasks)**

```text
> list

No tasks found.

> 
```

**`list` command (with tasks)**

```text
> list

ID  Title           Status      Created At
--  --------------  ----------  -------------------
1   Buy milk        [ ] Pending 2025-12-04 10:15
2   Finish report   [x] Done    2025-12-04 10:30

> 
```

**`update` command**

```text
> update
Enter task ID to update: 1
New title (leave blank to keep current): Buy milk and eggs
New description (leave blank to keep current): 

[OK] Task 1 updated.

> 
```

**`complete` command**

```text
> complete
Enter task ID to mark complete: 1

[OK] Task 1 marked as completed.

> 
```

**`delete` command**

```text
> delete
Enter task ID to delete: 2

Are you sure you want to delete task 2? (y/n): y

[OK] Task 2 deleted.

> 
```

**Invalid command / error example**

```text
> complet

[ERROR] Unknown command: 'complet'. Type 'help' to see commands.

> 
```

**`exit` command**

```text
> exit

Goodbye! 👋
```

## 4. Development Plan (Step-by-Step)

### Step 1: Project Initialization

1.  Initialize project with `uv init`.
2.  Set up Python 3.13+.
3.  Create directory structure (`src`, `specs`, `tests`).
4.  Create `constitution.md` and `CLAUDE.md`.

### Step 2: Specification

1.  Draft `specs/001_initial_phase1_spec.md` detailing the exact behavior of the CLI and data structures.

### Step 3: Core Implementation

1.  **Models**: Implement `Task` class in `src/models.py`.
2.  **Logic**: Implement `TodoManager` in `src/todo_manager.py` with basic CRUD methods.
3.  **Testing**: Write basic unit tests for `TodoManager` to ensure logic is correct.

### Step 4: CLI Implementation

1.  Implement `src/main.py`.
2.  Create a command loop to accept user input.
3.  Connect user inputs to `TodoManager` methods.
4.  Add error handling (e.g., invalid ID, empty input).

### Step 5: Refinement & Documentation

1.  Polish the UI (better formatting, clear messages).
2.  Update `README.md` with how to run the app using `uv run`.
3.  Verify all requirements are met.

### Step 6: Spec-Kit Plus Commands for Phase 1

During Phase 1 you will use **five main spec commands** (run inside your AI tool, not the terminal) to create and maintain specifications:

- **`/spec-phase1-overview`**: Create/update the high-level spec for the whole Phase 1 todo app.
- **`/spec-phase1-models-db`**: Specify the `Task` model and SQLite `tasks` table schema in detail.
- **`/spec-phase1-todo-manager`**: Specify the `TodoManager` API (methods, inputs/outputs, errors, and how it talks to SQLite).
- **`/spec-phase1-cli`**: Specify the CLI commands, prompts, and console output formats.
- **`/spec-phase1-installation`**: Specify the installation scripts and one-command install experience for Linux/macOS and Windows.

These commands and their details are documented in `Specification-phase-1/Specification1.md` and should be used to keep the code aligned with the written specs.

## 5. Tools & Libraries

- **Core**: Python Standard Library (`dataclasses`, `datetime`, `typing`).
- **Package Management**: `uv`.
- **Testing**: `pytest` (dev dependency).
- **Formatting/Linting**: `ruff` (dev dependency).
- **Persistence**: Python Standard Library `sqlite3` module for storing tasks in a local SQLite database file.
- **UI (Optional)**: `rich` (for beautiful terminal output) or `typer` (for CLI parsing), though standard `input()`/`print()` is sufficient for "Basic Level". _Recommendation: Stick to standard library for simplicity unless "Rich Aesthetics" is strictly required for console too, in which case `rich` is excellent._

## 6. One-Command Local Installation (Planned)

**Goal:** User opens a terminal and runs **one command** to install and set up the todo app locally.

> **Note:** Replace `<GITHUB_USER>`, `<REPO_NAME>`, and script paths with the actual GitHub URL for your project once the repository is created.

- **Linux / macOS (bash/zsh):**

  ```bash
  curl -LsSf https://raw.githubusercontent.com/<GITHUB_USER>/<REPO_NAME>/main/scripts/install.sh | bash
  ```

  - `install.sh` (in your repo) will:
    - Install `uv` if not already installed (optional, or just assume it exists).
    - Clone the GitHub repository to a local folder.
    - Run `uv sync` / `uv run` or equivalent to set up dependencies.
    - Optionally create a small shell wrapper so the user can run the app with a short command (e.g., `todo-app`).

- **Windows (PowerShell):**

  ```powershell
  powershell -ExecutionPolicy Bypass -Command "irm https://raw.githubusercontent.com/<GITHUB_USER>/<REPO_NAME>/main/scripts/install.ps1 | iex"
  ```

  - `install.ps1` (in your repo) will:
    - Download/clone the repository.
    - Ensure Python and `uv` are available (or show a clear message if not).
    - Set up the environment and create a convenient command/shortcut to run the app.

## 7. Next Steps

1.  Approve this plan.
2.  Initialize the repository and folder structure.
3.  Create the first spec file.
