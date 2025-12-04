# Data Model: Global Installation & Enhanced Terminal UI

**Feature Branch**: `002-global-install-ui`
**Date**: 2025-12-04
**Status**: Complete

## Overview

This feature primarily adds UI styling and installation capabilities. The core Task entity remains unchanged from Phase 1. This document defines the Theme/Styling model for the enhanced terminal UI.

## Existing Entity (Unchanged)

### Task

The Task entity from Phase 1 remains unchanged:

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

## New Entities

### Theme Configuration

Defines the visual styling for the terminal interface.

```python
@dataclass
class ThemeColors:
    """Color definitions for terminal output."""
    success: str      # Green - for success messages
    error: str        # Red - for error messages
    warning: str      # Yellow - for warnings
    info: str         # Cyan - for informational text
    pending: str      # Yellow - for pending task status
    completed: str    # Green - for completed task status
    header: str       # Blue - for table headers
    border: str       # White - for table borders
    prompt: str       # Magenta - for input prompt
    title: str        # Bold cyan - for app title
```

### Status Indicators

Visual indicators for task status:

| Status | Icon | Color |
|--------|------|-------|
| pending | ○ (circle) or ⏳ (hourglass) | Yellow |
| done | ✓ (checkmark) or ✅ | Green |

### Message Types

```python
class MessageType(Enum):
    SUCCESS = "success"   # [✓] prefix, green
    ERROR = "error"       # [✗] prefix, red
    INFO = "info"         # [i] prefix, cyan
    WARNING = "warning"   # [!] prefix, yellow
```

## UI Components

### Welcome Banner

```
╔══════════════════════════════════════╗
║       TODO APP - Console Edition      ║
║           Manage your tasks           ║
╚══════════════════════════════════════╝
Type 'help' for available commands.
```

**Styling**:
- Border: Double-line box (cyan)
- Title: Bold white
- Subtitle: Dim white

### Task Table

```
┌────┬─────────────────────┬────────────┬──────────────────┐
│ ID │ Title               │ Status     │ Created          │
├────┼─────────────────────┼────────────┼──────────────────┤
│  1 │ Buy groceries       │ ○ Pending  │ 2025-12-04 10:30 │
│  2 │ Call dentist        │ ✓ Done     │ 2025-12-04 11:15 │
└────┴─────────────────────┴────────────┴──────────────────┘
```

**Styling**:
- Header row: Bold blue background
- Pending status: Yellow with ○ icon
- Done status: Green with ✓ icon
- Borders: White/gray

### Command Prompt

```
todo ❯
```

**Styling**:
- "todo": Cyan
- "❯": Magenta

### Success Message

```
[✓] Task created with ID: 1
```

**Styling**: Green text with checkmark

### Error Message

```
[✗] Task not found
```

**Styling**: Red text with X mark

## Application Configuration

### Global Installation Paths

```python
@dataclass
class AppPaths:
    """Application path configuration."""

    @staticmethod
    def get_data_dir() -> Path:
        """Get data directory based on installation type."""
        # Global install: ~/.todo-app/
        # Development: ./data/
        home = Path.home()
        global_dir = home / ".todo-app"
        local_dir = Path("data")

        # Prefer global if exists or if not in dev environment
        if global_dir.exists() or not local_dir.exists():
            return global_dir
        return local_dir

    @staticmethod
    def get_db_path() -> Path:
        """Get database file path."""
        return AppPaths.get_data_dir() / "todo.db"
```

## Validation Rules

### Theme Colors

- All color values must be valid rich color names or hex codes
- Colors must be readable on both light and dark terminal backgrounds
- Fallback to plain text if terminal doesn't support colors

### Status Icons

- Must use Unicode characters supported by most terminals
- Fallback characters for terminals without Unicode:
  - Pending: `[ ]` instead of `○`
  - Done: `[x]` instead of `✓`

## State Transitions

No new state transitions. Task status transitions remain:
- `pending` → `done` (via complete command)

## Database Schema

No changes to database schema. Same as Phase 1:

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
