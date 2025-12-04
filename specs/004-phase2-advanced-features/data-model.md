# Data Model: TODO APP - PHASE 2 (Advanced Features)

**Feature Branch**: `004-phase2-advanced-features`
**Date**: 2025-12-05
**Spec**: [spec.md](spec.md)

---

## Overview

Phase 2 extends the existing Task entity with due dates and project association, and introduces a new Project entity for task categorization.

---

## Entity Definitions

### Task (Extended)

The existing Task dataclass is extended with optional due_date and project_id fields.

```python
from dataclasses import dataclass
from datetime import datetime, date
from typing import Optional

@dataclass
class Task:
    """A task with optional due date and project assignment."""

    id: int
    title: str
    description: str
    status: str  # 'pending' or 'done'
    created_at: datetime
    updated_at: datetime | None = None
    due_date: date | None = None          # NEW: Optional due date
    project_id: int | None = None         # NEW: Optional project FK
```

**Field Descriptions:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | int | Yes | Auto-generated primary key |
| title | str | Yes | Task title (non-empty) |
| description | str | Yes | Task description (can be empty) |
| status | str | Yes | 'pending' or 'done' |
| created_at | datetime | Yes | Creation timestamp |
| updated_at | datetime | No | Last update timestamp |
| due_date | date | No | Due date in YYYY-MM-DD format |
| project_id | int | No | Foreign key to projects table |

---

### Project (New)

A new entity for organizing tasks into categories.

```python
@dataclass
class Project:
    """A project/category for grouping tasks."""

    id: int
    name: str
    description: str
    created_at: datetime

    @property
    def task_count(self) -> int:
        """Number of tasks in this project (populated by query)."""
        return getattr(self, '_task_count', 0)

    @task_count.setter
    def task_count(self, value: int) -> None:
        self._task_count = value
```

**Field Descriptions:**
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | int | Yes | Auto-generated primary key |
| name | str | Yes | Unique project name (case-insensitive) |
| description | str | No | Project description |
| created_at | datetime | Yes | Creation timestamp |
| task_count | int | Computed | Number of tasks (not stored in DB) |

---

### UndoAction (Optional - for undo feature)

In-memory representation of the last action for undo functionality.

```python
@dataclass
class UndoAction:
    """Represents an action that can be undone."""

    action_type: str  # 'add', 'delete', 'complete', 'update'
    task_id: int
    previous_state: dict | None = None  # Task data before action (as dict)
    new_state: dict | None = None       # Task data after action (as dict)
```

---

## Database Schema

### tasks Table (Extended)

```sql
CREATE TABLE IF NOT EXISTS tasks (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    description TEXT,
    status TEXT DEFAULT 'pending',
    created_at TEXT NOT NULL,
    updated_at TEXT,
    due_date TEXT,           -- NEW: ISO format YYYY-MM-DD
    project_id INTEGER       -- NEW: FK to projects.id
);
```

**Migration SQL (run once):**
```sql
ALTER TABLE tasks ADD COLUMN due_date TEXT;
ALTER TABLE tasks ADD COLUMN project_id INTEGER;
```

---

### projects Table (New)

```sql
CREATE TABLE IF NOT EXISTS projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE COLLATE NOCASE,
    description TEXT,
    created_at TEXT NOT NULL
);
```

**Constraint Notes:**
- `UNIQUE COLLATE NOCASE` ensures project names are unique regardless of case
- No explicit FK constraint (SQLite limitation with ALTER TABLE)
- Referential integrity enforced in application code

---

## Validation Rules

### Task Validation

| Field | Rule | Error Message |
|-------|------|---------------|
| title | Non-empty after trim | "Title cannot be empty" |
| due_date | Valid YYYY-MM-DD or empty | "Invalid date format. Use YYYY-MM-DD" |
| project_id | Must exist in projects table or null | "Project 'X' not found. Create it first with 'project create'" |

### Project Validation

| Field | Rule | Error Message |
|-------|------|---------------|
| name | Non-empty after trim | "Project name cannot be empty" |
| name | Alphanumeric with underscores only | "Project name must be alphanumeric (underscores allowed)" |
| name | Unique (case-insensitive) | "Project name already exists" |

---

## Date Handling

### Storage Format
- SQLite: TEXT column with ISO format (YYYY-MM-DD)
- Python: `date` object

### Conversion Functions

```python
def parse_due_date(date_str: str) -> date | None:
    """Parse date string to date object."""
    if not date_str:
        return None
    return date.fromisoformat(date_str)

def format_due_date(due_date: date | None) -> str:
    """Format date object for display."""
    if due_date is None:
        return ""
    return due_date.isoformat()
```

### Filter Queries

```python
# Today's tasks
"SELECT * FROM tasks WHERE due_date = DATE('now', 'localtime')"

# Overdue pending tasks
"SELECT * FROM tasks WHERE due_date < DATE('now', 'localtime') AND status = 'pending'"

# Upcoming tasks (next 7 days)
"SELECT * FROM tasks WHERE due_date BETWEEN DATE('now', 'localtime') AND DATE('now', 'localtime', '+7 days')"
```

---

## Relationships

```text
┌─────────────┐       ┌─────────────┐
│   Project   │       │    Task     │
├─────────────┤       ├─────────────┤
│ id (PK)     │◄──────│ project_id  │
│ name        │  0..* │ id (PK)     │
│ description │       │ title       │
│ created_at  │       │ due_date    │
└─────────────┘       │ ...         │
                      └─────────────┘

Cardinality: Project 1 ──── 0..* Task (optional relationship)
```

---

## Statistics Data

```python
@dataclass
class TaskStats:
    """Statistics about tasks."""

    total: int
    pending: int
    completed: int
    due_today: int
    overdue: int

    @property
    def completion_rate(self) -> float:
        """Completion rate as percentage (0-100)."""
        if self.total == 0:
            return 0.0
        return (self.completed / self.total) * 100
```

---

## File Changes Summary

| File | Change Type | Description |
|------|-------------|-------------|
| `src/models.py` | MODIFY | Add due_date, project_id to Task; add Project dataclass |
| `src/project_manager.py` | NEW | Project CRUD operations |
| `src/todo_manager.py` | MODIFY | Add filter methods, stats, migration |
| `src/utils.py` | MODIFY | Add date validation, project name validation |
| `src/undo.py` | NEW (optional) | UndoAction class and undo logic |
