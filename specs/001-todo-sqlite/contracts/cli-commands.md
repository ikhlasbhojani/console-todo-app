# CLI Commands Contract: TODO APP - SQLITE (PHASE 1)

**Feature Branch**: `001-todo-sqlite`
**Date**: 2025-12-04
**Status**: Complete

## Overview

This document defines the contract for CLI commands and the TodoManager interface. It serves as the specification for implementation and testing.

---

## TodoManager Interface

### Class Definition

```python
class TodoManager:
    """Manages todo tasks with SQLite persistence.

    This class provides CRUD operations for tasks and handles
    all database interactions. It creates the database and
    table if they don't exist.

    Attributes:
        db_path: Path to the SQLite database file.
    """

    def __init__(self, db_path: str = "data/todo.db") -> None:
        """Initialize the TodoManager.

        Args:
            db_path: Path to SQLite database file. Creates parent
                     directories and database if they don't exist.
        """
        ...
```

### Method Contracts

#### add_task

```python
def add_task(self, title: str, description: str = "") -> Task:
    """Create a new task.

    Args:
        title: Task title (required, non-empty after strip)
        description: Optional task description (default: empty string)

    Returns:
        The newly created Task with generated ID and timestamps.

    Raises:
        ValueError: If title is empty or whitespace-only.

    Example:
        >>> manager.add_task("Buy milk", "2 liters from store")
        Task(id=1, title="Buy milk", description="2 liters from store",
             status="pending", created_at=..., updated_at=...)
    """
```

#### list_tasks

```python
def list_tasks(self) -> list[Task]:
    """Retrieve all tasks ordered by ID.

    Returns:
        List of all Task objects, empty list if no tasks exist.
        Tasks are ordered by id ascending.

    Example:
        >>> manager.list_tasks()
        [Task(id=1, ...), Task(id=2, ...)]
    """
```

#### get_task

```python
def get_task(self, task_id: int) -> Task | None:
    """Retrieve a single task by ID.

    Args:
        task_id: The unique identifier of the task.

    Returns:
        The Task if found, None if no task with that ID exists.

    Example:
        >>> manager.get_task(1)
        Task(id=1, title="Buy milk", ...)
        >>> manager.get_task(999)
        None
    """
```

#### update_task

```python
def update_task(
    self,
    task_id: int,
    title: str | None = None,
    description: str | None = None
) -> bool:
    """Update an existing task's title and/or description.

    Args:
        task_id: The unique identifier of the task to update.
        title: New title (None = keep current). Empty string not allowed.
        description: New description (None = keep current).

    Returns:
        True if task was found and updated, False if task not found.

    Raises:
        ValueError: If title is provided but empty/whitespace-only.

    Note:
        - If both title and description are None, no update occurs but returns True if task exists.
        - Always updates updated_at timestamp on success.

    Example:
        >>> manager.update_task(1, title="Buy milk and eggs")
        True
        >>> manager.update_task(999, title="New title")
        False
    """
```

#### complete_task

```python
def complete_task(self, task_id: int) -> tuple[bool, str]:
    """Mark a task as completed.

    Args:
        task_id: The unique identifier of the task to complete.

    Returns:
        Tuple of (success: bool, message: str):
        - (True, "[OK] Task {id} marked as completed.") on success
        - (False, "[ERROR] Task not found") if task doesn't exist
        - (False, "Task is already complete.") if already done

    Example:
        >>> manager.complete_task(1)
        (True, "[OK] Task 1 marked as completed.")
        >>> manager.complete_task(999)
        (False, "[ERROR] Task not found")
    """
```

#### delete_task

```python
def delete_task(self, task_id: int) -> bool:
    """Delete a task.

    Args:
        task_id: The unique identifier of the task to delete.

    Returns:
        True if task was found and deleted, False if task not found.

    Note:
        Confirmation is handled by the CLI layer, not this method.

    Example:
        >>> manager.delete_task(1)
        True
        >>> manager.delete_task(999)
        False
    """
```

---

## CLI Command Handlers

### Command: add

**Input Flow**:
```
> add
Enter title: <user input>
Enter description: <user input>
```

**Output**:
- Success: `[OK] Task created with ID: {id}`
- Error (empty title): `[ERROR] Title cannot be empty. Please enter a valid title.`
  - Then re-prompt: `Enter title:`

**Handler Contract**:
```python
def handle_add(manager: TodoManager) -> None:
    """Handle the 'add' command.

    Prompts user for title and description, validates input,
    creates task via manager, and displays result.
    """
```

### Command: list

**Input**: None (no prompts)

**Output**:
- With tasks:
  ```
  ID   Title              Status        Created At
  ---  -----------------  ------------  ----------------
  1    Buy milk           [ ] Pending   2025-12-04 10:15
  ```
- No tasks: `No tasks found.`

**Handler Contract**:
```python
def handle_list(manager: TodoManager) -> None:
    """Handle the 'list' command.

    Retrieves all tasks and displays them in formatted table.
    """
```

### Command: update

**Input Flow**:
```
> update
Enter task ID to update: <user input>
New title (leave blank to keep current): <user input>
New description (leave blank to keep current): <user input>
```

**Output**:
- Success: `[OK] Task {id} updated.`
- Error (not found): `[ERROR] Task not found`
- Error (invalid ID): `[ERROR] Invalid task ID. Please enter a number.`

**Handler Contract**:
```python
def handle_update(manager: TodoManager) -> None:
    """Handle the 'update' command.

    Prompts for task ID and new values, validates input,
    updates task via manager, and displays result.
    """
```

### Command: complete

**Input Flow**:
```
> complete
Enter task ID to mark complete: <user input>
```

**Output**:
- Success: `[OK] Task {id} marked as completed.`
- Already done: `Task is already complete.`
- Not found: `[ERROR] Task not found`
- Invalid ID: `[ERROR] Invalid task ID. Please enter a number.`

**Handler Contract**:
```python
def handle_complete(manager: TodoManager) -> None:
    """Handle the 'complete' command.

    Prompts for task ID, validates input, completes task
    via manager, and displays result.
    """
```

### Command: delete

**Input Flow**:
```
> delete
Enter task ID to delete: <user input>
Are you sure you want to delete task {id}? (y/n): <user input>
```

**Output**:
- Success: `[OK] Task {id} deleted.`
- Cancelled: (returns to prompt silently)
- Not found: `[ERROR] Task not found`
- Invalid ID: `[ERROR] Invalid task ID. Please enter a number.`

**Handler Contract**:
```python
def handle_delete(manager: TodoManager) -> None:
    """Handle the 'delete' command.

    Prompts for task ID, confirms deletion, deletes task
    via manager if confirmed, and displays result.
    """
```

### Command: help

**Input**: None

**Output**:
```
Available commands:
  add      - Add a new task
  list     - Show all tasks
  update   - Update an existing task (title/description)
  complete - Mark a task as completed
  delete   - Delete a task
  exit     - Quit the application
```

**Handler Contract**:
```python
def handle_help() -> None:
    """Handle the 'help' command.

    Displays list of available commands with descriptions.
    """
```

### Command: exit

**Input**: None

**Output**: `Goodbye!`

**Behavior**: Terminates the main loop.

---

## Utility Functions Contract

### validate_task_id

```python
def validate_task_id(id_str: str) -> tuple[bool, int | str]:
    """Validate and parse a task ID string.

    Args:
        id_str: User input string to validate as task ID.

    Returns:
        (True, int) if valid integer, (False, error_message) if invalid.

    Example:
        >>> validate_task_id("42")
        (True, 42)
        >>> validate_task_id("abc")
        (False, "[ERROR] Invalid task ID. Please enter a number.")
    """
```

### validate_title

```python
def validate_title(title: str) -> tuple[bool, str]:
    """Validate a task title.

    Args:
        title: User input string to validate as title.

    Returns:
        (True, stripped_title) if valid, (False, error_message) if empty.

    Example:
        >>> validate_title("  Buy milk  ")
        (True, "Buy milk")
        >>> validate_title("   ")
        (False, "[ERROR] Title cannot be empty. Please enter a valid title.")
    """
```

### format_task_table

```python
def format_task_table(tasks: list[Task]) -> str:
    """Format a list of tasks as a table string.

    Args:
        tasks: List of Task objects to format.

    Returns:
        Formatted table string with header, separator, and rows.

    Example:
        ID   Title              Status        Created At
        ---  -----------------  ------------  ----------------
        1    Buy milk           [ ] Pending   2025-12-04 10:15
    """
```

---

## Error Handling Summary

| Scenario | Error Message |
|----------|---------------|
| Unknown command | `[ERROR] Unknown command: '{cmd}'. Type 'help' to see commands.` |
| Empty title | `[ERROR] Title cannot be empty. Please enter a valid title.` |
| Invalid ID format | `[ERROR] Invalid task ID. Please enter a number.` |
| Task not found | `[ERROR] Task not found` |
| Already complete | `Task is already complete.` |

---

## Test Cases Reference

Each contract method should have tests for:

1. **Happy path**: Normal successful operation
2. **Edge cases**: Empty inputs, boundary values
3. **Error cases**: Invalid inputs, not found scenarios
4. **State verification**: Database state after operation

See `tests/test_todo_manager.py` for implementation.
