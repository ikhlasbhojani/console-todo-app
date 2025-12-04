# Research: TODO APP - SQLITE (PHASE 1)

**Feature Branch**: `001-todo-sqlite`
**Date**: 2025-12-04
**Status**: Complete

## Overview

This document captures technical research and decisions made during the planning phase for the console-based todo application with SQLite persistence.

---

## Research Areas

### 1. Database Connection Strategy

**Question**: How should we manage SQLite database connections?

**Options Evaluated**:

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A. Per-operation | Open/close connection for each CRUD operation | Simple, no lock issues, safe for CLI | Slight overhead per operation |
| B. Persistent | Keep one connection open for app lifetime | Faster operations | Risk of database locks, cleanup needed |
| C. Connection pool | Pool of reusable connections | Best for concurrent access | Overkill for single-user CLI |

**Decision**: **Option A - Per-operation connections**

**Rationale**:
- Single-user CLI application doesn't benefit from persistent connections
- Context managers (`with conn:`) ensure proper cleanup
- SQLite file locking is simpler with short-lived connections
- No risk of stale connections or lock conflicts

**Implementation Pattern**:
```python
def _get_connection(self) -> sqlite3.Connection:
    conn = sqlite3.connect(self.db_path)
    conn.row_factory = sqlite3.Row
    return conn

def add_task(self, title: str, description: str = "") -> Task:
    with self._get_connection() as conn:
        cursor = conn.execute(...)
        conn.commit()
        return task
```

---

### 2. ID Generation Strategy

**Question**: How should task IDs be generated?

**Options Evaluated**:

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A. AUTOINCREMENT | SQLite built-in auto-increment | Simple, no gaps reuse, standard | IDs can have gaps after deletes |
| B. Application UUID | Generate UUIDs in Python | Globally unique, no DB dependency | Harder for users to type/remember |
| C. Sequential counter | Track max ID in application | Full control over sequence | Race conditions, complexity |

**Decision**: **Option A - SQLite AUTOINCREMENT**

**Rationale**:
- Users interact with IDs via command line; integers are easy to type
- AUTOINCREMENT guarantees uniqueness without application logic
- Gaps after deletion are acceptable (users don't care about continuous IDs)
- Standard SQLite pattern, well-understood behavior

**Schema**:
```sql
id INTEGER PRIMARY KEY AUTOINCREMENT
```

---

### 3. Datetime Storage Format

**Question**: How should timestamps be stored in SQLite?

**Options Evaluated**:

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A. ISO 8601 TEXT | "2025-12-04T10:30:00" | Human-readable, sortable, standard | Larger storage than integer |
| B. Unix timestamp | Integer seconds since epoch | Compact, fast comparison | Not human-readable in raw DB |
| C. SQLite DATETIME | Native datetime functions | Built-in date functions | Limited timezone support |

**Decision**: **Option A - ISO 8601 TEXT format**

**Rationale**:
- Human-readable when inspecting database directly
- Sortable as strings (lexicographic order matches chronological)
- Easy to parse with Python's `datetime.fromisoformat()`
- Standard format understood by all tools
- Storage overhead negligible for this scale

**Format**: `YYYY-MM-DDTHH:MM:SS` (e.g., `2025-12-04T10:30:00`)

**Display Format**: `YYYY-MM-DD HH:MM` (without seconds, per spec)

---

### 4. Input Validation Strategy

**Question**: Where should input validation logic live?

**Options Evaluated**:

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A. Centralized utils | All validation in utils.py | Reusable, consistent, testable | Extra module to maintain |
| B. Inline in handlers | Validate in each CLI handler | Close to usage point | Code duplication |
| C. In manager class | Validate in TodoManager methods | Single responsibility | Mixes validation with business logic |

**Decision**: **Option A - Centralized validation in utils.py**

**Rationale**:
- Validation logic is reused across multiple commands (ID validation, title validation)
- Consistent error messages across the application
- Easy to unit test validation functions independently
- Keeps CLI handlers clean and focused on flow

**Functions to implement**:
```python
def validate_task_id(id_str: str) -> tuple[bool, int | str]:
    """Returns (True, int) on success, (False, error_message) on failure."""

def validate_title(title: str) -> tuple[bool, str]:
    """Returns (True, trimmed_title) on success, (False, error_message) on failure."""

def format_task_row(task: Task) -> str:
    """Format a task for display in the list table."""
```

---

### 5. Output Formatting Strategy

**Question**: How should task lists be formatted for console display?

**Options Evaluated**:

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A. Fixed-width columns | Manual string formatting | No dependencies, works everywhere | Manual width management |
| B. rich library | Third-party table formatting | Beautiful output, colors | External dependency |
| C. tabulate library | Simple table formatting | Easy API | External dependency |

**Decision**: **Option A - Fixed-width columns with string formatting**

**Rationale**:
- Constitution prefers standard library (no external dependencies for basic level)
- Simple f-string formatting is sufficient for this table size
- Works in all terminals without color/unicode issues
- Can add rich/tabulate in future phases if needed

**Format Pattern**:
```python
HEADER = "ID   Title              Status        Created At"
SEP =    "---  -----------------  ------------  ----------------"
ROW =    f"{task.id:<4} {task.title[:17]:<17}  {status:<12}  {date}"
```

---

### 6. Error Handling Strategy

**Question**: How should errors be communicated to users?

**Options Evaluated**:

| Option | Description | Pros | Cons |
|--------|-------------|------|------|
| A. Return tuples | Return (success, message) | Explicit, no exceptions | Verbose return handling |
| B. Custom exceptions | Raise TodoError | Clean separation | Exception handling overhead |
| C. Print and continue | Print error, return None | Simple | Hard to test, unclear flow |

**Decision**: **Mixed approach - Return tuples for expected cases, exceptions for unexpected**

**Rationale**:
- "Task not found" is an expected case → return `(False, "error message")`
- Database errors are unexpected → raise exception
- This matches spec behavior: user sees `[ERROR]` messages, app continues

**Pattern**:
```python
def complete_task(self, task_id: int) -> tuple[bool, str]:
    task = self.get_task(task_id)
    if task is None:
        return (False, "[ERROR] Task not found")
    if task.status == "done":
        return (False, "Task is already complete.")
    # ... update task
    return (True, f"[OK] Task {task_id} marked as completed.")
```

---

## Technology Stack Confirmation

| Component | Choice | Reason |
|-----------|--------|--------|
| Language | Python 3.13+ | Modern features, type hints, match statements |
| Package Manager | uv | Fast, modern, manages venv and deps |
| Database | SQLite via sqlite3 | Constitution requirement, built-in |
| Testing | pytest | Constitution requirement, fixtures support |
| Linting | ruff | Constitution requirement, fast |
| CLI Framework | None (input/print) | Basic level, no complexity needed |

---

## Risks and Mitigations

| Risk | Impact | Mitigation |
|------|--------|------------|
| Database corruption | Data loss | Use transactions, write-ahead logging |
| Large task lists | Slow display | Paginate in future phase if needed |
| Special characters in input | Display issues | Proper escaping, test edge cases |
| Concurrent access | Lock errors | Single-user design, per-operation connections |

---

## References

- [SQLite Documentation](https://www.sqlite.org/docs.html)
- [Python sqlite3 Module](https://docs.python.org/3/library/sqlite3.html)
- [PEP 557 - Data Classes](https://peps.python.org/pep-0557/)
- [Project Constitution](../../.specify/memory/constitution.md)
