# Quickstart: TODO APP - SQLITE (PHASE 1)

**Feature Branch**: `001-todo-sqlite`
**Date**: 2025-12-04

## Prerequisites

- Python 3.13 or higher
- `uv` package manager ([install guide](https://docs.astral.sh/uv/getting-started/installation/))

## Quick Setup

```bash
# Clone the repository (if not already done)
git clone <repository-url>
cd console-todo-app

# Install dependencies
uv sync

# Run the application
uv run python -m src.main
```

## Running the Application

### Standard Mode

```bash
uv run python -m src.main
```

You'll see:
```
====================================
      TODO APP - SQLITE (PHASE 1)
====================================
Type 'help' to see available commands.

>
```

### Quick Test

```bash
# Run all tests
uv run pytest

# Run with verbose output
uv run pytest -v

# Run specific test file
uv run pytest tests/test_todo_manager.py
```

## Basic Usage

### Add a Task

```
> add
Enter title: Buy groceries
Enter description: Milk, bread, eggs

[OK] Task created with ID: 1
```

### List Tasks

```
> list

ID   Title              Status        Created At
---  -----------------  ------------  ----------------
1    Buy groceries      [ ] Pending   2025-12-04 10:15
```

### Complete a Task

```
> complete
Enter task ID to mark complete: 1

[OK] Task 1 marked as completed.
```

### Update a Task

```
> update
Enter task ID to update: 1
New title (leave blank to keep current): Buy groceries and snacks
New description (leave blank to keep current):

[OK] Task 1 updated.
```

### Delete a Task

```
> delete
Enter task ID to delete: 1
Are you sure you want to delete task 1? (y/n): y

[OK] Task 1 deleted.
```

### Exit

```
> exit

Goodbye!
```

## Development Commands

### Linting

```bash
# Check for issues
uv run ruff check src/ tests/

# Auto-fix issues
uv run ruff check src/ tests/ --fix

# Format code
uv run ruff format src/ tests/
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src

# Run specific test
uv run pytest tests/test_todo_manager.py::test_add_task_success
```

### Database

The SQLite database is stored at `data/todo.db`. It's created automatically on first run.

```bash
# View database (optional)
sqlite3 data/todo.db ".schema"
sqlite3 data/todo.db "SELECT * FROM tasks;"

# Reset database (delete all data)
rm data/todo.db
```

## Project Structure

```
console-todo-app/
├── src/
│   ├── __init__.py      # Package marker
│   ├── main.py          # CLI entry point
│   ├── models.py        # Task dataclass
│   ├── todo_manager.py  # Business logic
│   └── utils.py         # Helpers
├── tests/
│   ├── conftest.py      # pytest fixtures
│   └── test_*.py        # Test files
├── data/
│   └── todo.db          # SQLite database
├── specs/               # Specifications
├── scripts/             # Installation scripts
└── pyproject.toml       # Project config
```

## Troubleshooting

### "ModuleNotFoundError: No module named 'src'"

Make sure you're running from the project root:
```bash
cd console-todo-app
uv run python -m src.main
```

### "Database is locked"

Close any other database connections:
```bash
# Find processes using the database
lsof data/todo.db

# Or simply delete and recreate
rm data/todo.db
```

### "uv: command not found"

Install uv:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

## Next Steps

1. Run `/sp.tasks` to see the implementation task list
2. Use `python-todo-cli-dev` agent to implement features
3. Use `todo-testing-agent` to write tests
4. Run `uv run pytest` to verify implementation
