# TODO APP - SQLITE

A powerful, interactive console-based todo application with SQLite persistence. Manage your tasks efficiently right from your terminal with an intuitive command-line interface.

[![Python Version](https://img.shields.io/badge/python-3.13%2B-blue.svg)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Package Manager](https://img.shields.io/badge/package%20manager-uv-purple.svg)](https://github.com/astral-sh/uv)

---

## Features

- **Add Tasks** - Create new tasks with title and optional description
- **List Tasks** - View all your tasks in a beautifully formatted table
- **Update Tasks** - Modify task titles and descriptions
- **Complete Tasks** - Mark tasks as completed when you're done
- **Delete Tasks** - Remove tasks you no longer need (with confirmation)
- **SQLite Persistence** - All tasks are saved to a local database
- **Input Validation** - Robust validation prevents invalid data
- **Interactive CLI** - Simple, intuitive command-line interface
- **Cross-Platform** - Works on Linux, macOS, and Windows

---

## Table of Contents

- [Prerequisites](#prerequisites)
- [Installation](#installation)
  - [Quick Install (Recommended)](#quick-install-recommended)
  - [Manual Installation](#manual-installation)
- [Quick Start](#quick-start)
- [Usage Tutorial](#usage-tutorial)
- [Command Reference](#command-reference)
- [Project Structure](#project-structure)
- [Development](#development)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Prerequisites

Before you begin, ensure you have the following installed:

- **Python 3.13 or higher** - [Download Python](https://www.python.org/downloads/)
- **uv package manager** - [Install uv](https://github.com/astral-sh/uv)

To verify your Python version:

```console
$ python --version
Python 3.13.0
```

To install `uv` (if not already installed):

```console
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

---

## Installation

### Quick Install (Recommended)

Choose the installation script for your operating system:

#### Linux / macOS

```console
$ cd /path/to/console-todo-app
$ chmod +x scripts/install.sh
$ ./scripts/install.sh
```

The installation script will:
1. Check for Python 3.13+ and `uv`
2. Create a virtual environment using `uv`
3. Install all dependencies
4. Verify the installation

**Expected Output:**
```console
========================================
  Console Todo App Installation Script
========================================

Checking for Python 3.13+...
✓ Python 3.13.0 found

Checking for uv package manager...
✓ uv found

Creating virtual environment with uv...
✓ Virtual environment created

Installing dependencies...
✓ Dependencies installed

Installation completed successfully!

To activate the virtual environment:
  source .venv/bin/activate

To run the app:
  python src/main.py

To run tests:
  pytest
```

#### Windows (PowerShell)

```powershell
PS> cd \path\to\console-todo-app
PS> .\scripts\install.ps1
```

> **Note:** If you encounter an execution policy error, run:
> ```powershell
> PS> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### Manual Installation

If you prefer to install manually:

```console
$ git clone <repository-url>
$ cd console-todo-app
$ uv venv
$ source .venv/bin/activate  # On Windows: .venv\Scripts\activate
$ uv pip install -e .
$ uv pip install -e ".[dev]"  # For development dependencies
```

---

## Quick Start

After installation, activate your virtual environment and run the app:

```console
$ source .venv/bin/activate  # On Windows: .venv\Scripts\activate
$ python src/main.py
```

You'll see the welcome banner:

```
====================================
      TODO APP - SQLITE (PHASE 1)
====================================
Type 'help' to see available commands.

>
```

Now you're ready to start managing your tasks!

---

## Usage Tutorial

Let's walk through a complete workflow using the Todo App.

### 1. Starting the Application

```console
$ python src/main.py
====================================
      TODO APP - SQLITE (PHASE 1)
====================================
Type 'help' to see available commands.

>
```

### 2. Getting Help

Type `help` to see all available commands:

```console
> help

Available commands:
  add      - Add a new task
  list     - Show all tasks
  update   - Update an existing task (title/description)
  complete - Mark a task as completed
  delete   - Delete a task
  exit     - Quit the application

>
```

### 3. Adding Your First Task

Use the `add` command to create a new task:

```console
> add
Enter title: Buy groceries
Enter description: Get milk, eggs, bread, and vegetables

[OK] Task created with ID: 1

>
```

Let's add a few more tasks:

```console
> add
Enter title: Call dentist
Enter description: Schedule teeth cleaning appointment

[OK] Task created with ID: 2

> add
Enter title: Finish project report
Enter description: Complete the Q4 analysis report by Friday

[OK] Task created with ID: 3

>
```

### 4. Listing All Tasks

View all your tasks with the `list` command:

```console
> list

┌────┬─────────────────────────┬─────────────────────────────────────────┬──────────┬─────────────────────┐
│ ID │ Title                   │ Description                             │ Status   │ Created             │
├────┼─────────────────────────┼─────────────────────────────────────────┼──────────┼─────────────────────┤
│ 1  │ Buy groceries           │ Get milk, eggs, bread, and vegetables   │ pending  │ 2025-12-04 10:30:15 │
│ 2  │ Call dentist            │ Schedule teeth cleaning appointment     │ pending  │ 2025-12-04 10:31:22 │
│ 3  │ Finish project report   │ Complete the Q4 analysis report by Fr...│ pending  │ 2025-12-04 10:32:10 │
└────┴─────────────────────────┴─────────────────────────────────────────┴──────────┴─────────────────────┘

>
```

### 5. Completing a Task

Mark a task as completed using the `complete` command:

```console
> complete
Enter task ID to mark complete: 1

[OK] Task 1 marked as completed.

>
```

List tasks again to see the status change:

```console
> list

┌────┬─────────────────────────┬─────────────────────────────────────────┬──────────┬─────────────────────┐
│ ID │ Title                   │ Description                             │ Status   │ Created             │
├────┼─────────────────────────┼─────────────────────────────────────────┼──────────┼─────────────────────┤
│ 1  │ Buy groceries           │ Get milk, eggs, bread, and vegetables   │ complete │ 2025-12-04 10:30:15 │
│ 2  │ Call dentist            │ Schedule teeth cleaning appointment     │ pending  │ 2025-12-04 10:31:22 │
│ 3  │ Finish project report   │ Complete the Q4 analysis report by Fr...│ pending  │ 2025-12-04 10:32:10 │
└────┴─────────────────────────┴─────────────────────────────────────────┴──────────┴─────────────────────┘

>
```

### 6. Updating a Task

Update the title or description of an existing task:

```console
> update
Enter task ID to update: 2
New title (leave blank to keep current): Call dentist - URGENT
New description (leave blank to keep current):

[OK] Task 2 updated.

>
```

You can also update just the description:

```console
> update
Enter task ID to update: 3
New title (leave blank to keep current):
New description (leave blank to keep current): Complete the Q4 analysis report and send to manager by Friday 5pm

[OK] Task 3 updated.

>
```

### 7. Deleting a Task

Remove a task you no longer need:

```console
> delete
Enter task ID to delete: 1
Are you sure you want to delete task 1? (y/n): y

[OK] Task 1 deleted.

> list

┌────┬─────────────────────────┬─────────────────────────────────────────┬──────────┬─────────────────────┐
│ ID │ Title                   │ Description                             │ Status   │ Created             │
├────┼─────────────────────────┼─────────────────────────────────────────┼──────────┼─────────────────────┤
│ 2  │ Call dentist - URGENT   │ Schedule teeth cleaning appointment     │ pending  │ 2025-12-04 10:31:22 │
│ 3  │ Finish project report   │ Complete the Q4 analysis report and s...│ pending  │ 2025-12-04 10:32:10 │
└────┴─────────────────────────┴─────────────────────────────────────────┴──────────┴─────────────────────┘

>
```

### 8. Exiting the Application

When you're done, type `exit` to quit:

```console
> exit

Goodbye!
```

You can also press `Ctrl+C` or `Ctrl+D` at any time to exit gracefully.

---

## Command Reference

| Command    | Description                                      | Example Usage                |
|------------|--------------------------------------------------|------------------------------|
| `add`      | Add a new task with title and description        | `> add`                      |
| `list`     | Display all tasks in a formatted table           | `> list`                     |
| `update`   | Update an existing task's title or description   | `> update`                   |
| `complete` | Mark a task as completed                         | `> complete`                 |
| `delete`   | Delete a task (requires confirmation)            | `> delete`                   |
| `help`     | Display list of available commands               | `> help`                     |
| `exit`     | Exit the application                             | `> exit`                     |

### Input Validation Rules

- **Task Title**: Cannot be empty or contain only whitespace (automatically trimmed)
- **Task ID**: Must be a positive integer
- **Delete Confirmation**: Requires typing `y` to confirm deletion
- **Update Fields**: Blank input keeps the current value

### Error Handling Examples

**Invalid Task ID:**
```console
> complete
Enter task ID to mark complete: abc

[ERROR] Invalid ID format. Please enter a positive number.

>
```

**Empty Title:**
```console
> add
Enter title:

[ERROR] Title cannot be empty or whitespace only.

Enter title: Buy milk
Enter description: 2% milk from store

[OK] Task created with ID: 4

>
```

**Task Not Found:**
```console
> complete
Enter task ID to mark complete: 999

[ERROR] Task not found

>
```

---

## Project Structure

```
console-todo-app/
├── src/                          # Source code directory
│   ├── __init__.py              # Package initializer
│   ├── main.py                  # Main CLI application and command handlers
│   ├── models.py                # Data models (Task dataclass)
│   ├── todo_manager.py          # Business logic and database operations
│   └── utils.py                 # Utility functions (validation, formatting)
│
├── tests/                        # Test suite
│   ├── __init__.py
│   ├── conftest.py              # Pytest fixtures and test configuration
│   ├── test_cli.py              # CLI command handler tests
│   └── test_todo_manager.py     # TodoManager unit tests
│
├── scripts/                      # Installation and utility scripts
│   ├── install.sh               # Linux/macOS installation script
│   └── install.ps1              # Windows PowerShell installation script
│
├── data/                         # Data directory (created at runtime)
│   └── todo.db                  # SQLite database (created automatically)
│
├── specs/                        # Specification documents
│   └── 001-todo-sqlite/         # Feature specifications
│       ├── spec.md              # Main specification
│       ├── plan.md              # Implementation plan
│       ├── tasks.md             # Task breakdown
│       └── ...
│
├── pyproject.toml               # Project metadata and dependencies
├── uv.lock                      # Dependency lock file
├── README.md                    # This file
├── CLAUDE.md                    # AI assistant context and rules
└── .venv/                       # Virtual environment (created during install)
```

### Key Files Explained

- **src/main.py** - Entry point for the application; contains the main CLI loop and command handlers
- **src/todo_manager.py** - Core business logic; manages database operations and task lifecycle
- **src/models.py** - Defines the `Task` dataclass with typed fields
- **src/utils.py** - Helper functions for validation, formatting, and table rendering
- **pyproject.toml** - Project configuration including dependencies and tool settings
- **tests/** - Comprehensive test suite using pytest framework

---

## Development

### Setting Up Development Environment

1. Clone the repository and install with development dependencies:

```console
$ git clone <repository-url>
$ cd console-todo-app
$ ./scripts/install.sh
$ source .venv/bin/activate
```

2. Install development dependencies (if not already installed):

```console
$ uv pip install -e ".[dev]"
```

### Running Tests

Run the complete test suite with pytest:

```console
$ pytest
```

**Expected Output:**
```console
======================== test session starts =========================
platform linux -- Python 3.13.0, pytest-9.0.1, pluggy-1.5.0
rootdir: /path/to/console-todo-app
collected 45 items

tests/test_cli.py ...................                          [ 42%]
tests/test_todo_manager.py .........................           [100%]

========================= 45 passed in 0.52s =========================
```

Run tests with verbose output:

```console
$ pytest -v
```

Run tests with coverage report:

```console
$ pytest --cov=src --cov-report=term-missing
```

Run specific test files or functions:

```console
$ pytest tests/test_cli.py
$ pytest tests/test_todo_manager.py::TestTodoManager::test_add_task
```

### Code Quality

#### Linting with Ruff

Check code for style and quality issues:

```console
$ ruff check .
```

Fix auto-fixable issues:

```console
$ ruff check --fix .
```

#### Formatting with Ruff

Check code formatting:

```console
$ ruff format --check .
```

Format code automatically:

```console
$ ruff format .
```

### Project Standards

This project follows:
- **PEP 8** - Python style guide
- **Type Hints** - All functions use Python 3.13+ type annotations
- **Spec-Driven Development** - Implementation follows written specifications
- **Test-Driven Development** - Tests written before or alongside code
- **Clean Code** - Small, focused functions with clear names

See `CLAUDE.md` and `.specify/memory/constitution.md` for complete coding standards.

---

## Troubleshooting

### Common Issues and Solutions

#### Issue: "Command not found: python"

**Solution:** You might need to use `python3` instead:

```console
$ python3 src/main.py
```

Or create an alias in your shell configuration:

```bash
alias python=python3
```

---

#### Issue: "ModuleNotFoundError: No module named 'src'"

**Solution:** Make sure you're running from the project root directory and the virtual environment is activated:

```console
$ cd /path/to/console-todo-app
$ source .venv/bin/activate
$ python src/main.py
```

---

#### Issue: Virtual environment activation fails on Windows

**Solution:** Use the correct activation command for your shell:

**CMD:**
```cmd
.venv\Scripts\activate.bat
```

**PowerShell:**
```powershell
.venv\Scripts\Activate.ps1
```

---

#### Issue: "Permission denied" when running install.sh

**Solution:** Make the script executable:

```console
$ chmod +x scripts/install.sh
$ ./scripts/install.sh
```

---

#### Issue: Database file locked

**Solution:** Ensure no other instances of the app are running. If the issue persists, restart your terminal and try again.

---

#### Issue: Tests failing with database errors

**Solution:** The test suite uses a temporary in-memory database. If tests fail, try deleting the `data/todo.db` file and run tests again:

```console
$ rm -f data/todo.db
$ pytest
```

---

#### Issue: "uv: command not found"

**Solution:** Install the `uv` package manager:

```console
$ curl -LsSf https://astral.sh/uv/install.sh | sh
```

Then restart your terminal or source your shell configuration:

```console
$ source ~/.bashrc  # or ~/.zshrc
```

---

### Getting Help

If you encounter issues not listed here:

1. Check the specification documents in `specs/001-todo-sqlite/`
2. Review the test files in `tests/` for usage examples
3. Examine the source code in `src/` for implementation details
4. Open an issue on the project repository with:
   - Your operating system and Python version
   - Complete error message
   - Steps to reproduce the issue

---

## License

This project is licensed under the MIT License.

```
MIT License

Copyright (c) 2025 Console Todo App Contributors

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## About This Project

This Console Todo App was built using **Spec-Driven Development (SDD)** methodology, where all features are fully specified before implementation. The project demonstrates:

- Clean architecture with separation of concerns
- Comprehensive test coverage
- Type-safe Python code
- SQLite database integration
- Interactive CLI design patterns
- Professional software development practices

**Built with:**
- Python 3.13+
- SQLite3 (built-in)
- pytest (testing)
- ruff (linting and formatting)
- uv (package management)

---

**Happy Task Managing!**
