# Research: TODO APP - PHASE 2 (Advanced Features)

**Feature Branch**: `004-phase2-advanced-features`
**Date**: 2025-12-05
**Spec**: [spec.md](spec.md)

---

## Research Questions

### RQ-001: How to add columns to existing SQLite table?

**Finding**: SQLite supports `ALTER TABLE ... ADD COLUMN` for adding new columns.

```sql
ALTER TABLE tasks ADD COLUMN due_date TEXT;
ALTER TABLE tasks ADD COLUMN project_id INTEGER;
```

**Key points**:
- New columns are added with NULL as default value (perfect for optional fields)
- Existing data is preserved
- No need for complex migration
- Cannot add FOREIGN KEY constraint via ALTER TABLE in SQLite

**Decision**: Use ALTER TABLE for simple column additions. Handle FK constraint in application logic.

### RQ-002: Best approach for database schema migration?

**Finding**: Two approaches for SQLite migrations:

1. **Check-and-add approach** (recommended for this project):
   ```python
   def _ensure_columns_exist(self):
       cursor.execute("PRAGMA table_info(tasks)")
       columns = [row[1] for row in cursor.fetchall()]
       if "due_date" not in columns:
           cursor.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT")
       if "project_id" not in columns:
           cursor.execute("ALTER TABLE tasks ADD COLUMN project_id INTEGER")
   ```

2. **Version-based migration**: Track schema version in a meta table

**Decision**: Use check-and-add approach for simplicity. Called once during TodoManager init.

### RQ-003: Date storage format and validation

**Finding**: ISO 8601 format (YYYY-MM-DD) is the standard for date storage.

**Validation approach**:
```python
from datetime import date

def validate_due_date(date_str: str) -> date | None:
    if not date_str:
        return None
    try:
        return date.fromisoformat(date_str)
    except ValueError:
        raise ValueError("Invalid date format. Use YYYY-MM-DD")
```

**Key points**:
- Store as TEXT in SQLite (YYYY-MM-DD)
- Parse to Python `date` object in application
- Compare dates using Python's date comparison operators

**Decision**: Store as TEXT (YYYY-MM-DD), parse to `date` in models.

### RQ-004: Implementing list filters efficiently

**Finding**: SQL WHERE clauses with date comparisons:

```sql
-- Today's tasks
WHERE due_date = DATE('now', 'localtime')

-- Overdue tasks (past due, still pending)
WHERE due_date < DATE('now', 'localtime') AND status = 'pending'

-- Upcoming tasks (next 7 days)
WHERE due_date BETWEEN DATE('now', 'localtime') AND DATE('now', 'localtime', '+7 days')
```

**Decision**: Use SQL date functions for filtering. SQLite's `DATE()` function handles timezone correctly.

### RQ-005: Project entity design

**Finding**: Two approaches for task-project relationship:

1. **Simple text column** (project name stored directly in tasks table):
   - Pros: Simple, no joins needed
   - Cons: No project metadata, inconsistent naming

2. **Separate projects table with FK** (recommended):
   - Pros: Project CRUD, task counts, consistent naming
   - Cons: Additional table, joins needed

**Decision**: Use separate projects table for full CRUD support.

```sql
CREATE TABLE projects (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL UNIQUE COLLATE NOCASE,
    description TEXT,
    created_at TEXT NOT NULL
);

-- Tasks table gets project_id
ALTER TABLE tasks ADD COLUMN project_id INTEGER;
```

### RQ-006: Statistics calculation approach

**Finding**: Use SQL aggregate functions for efficiency:

```sql
SELECT
    COUNT(*) as total,
    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END) as pending,
    SUM(CASE WHEN status = 'done' THEN 1 ELSE 0 END) as completed,
    SUM(CASE WHEN due_date = DATE('now', 'localtime') THEN 1 ELSE 0 END) as due_today,
    SUM(CASE WHEN due_date < DATE('now', 'localtime') AND status = 'pending' THEN 1 ELSE 0 END) as overdue
FROM tasks;
```

**Decision**: Single SQL query for all stats, calculated on-demand.

### RQ-007: Undo implementation strategy

**Finding**: Two approaches:

1. **Command pattern with action history** (database-backed):
   - Store action type, task ID, old/new data as JSON
   - Persistent across sessions
   - Complex implementation

2. **In-memory last action only** (recommended for simplicity):
   - Store last action in memory
   - Cleared on app restart
   - Simple implementation, meets spec requirements

**Decision**: In-memory single-action undo. Simpler and matches spec (single-level only).

```python
@dataclass
class UndoAction:
    action_type: str  # 'add', 'delete', 'complete', 'update'
    task_id: int
    previous_state: dict | None  # Task data before action
```

---

## Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| Column migration | ALTER TABLE ADD COLUMN | Simple, preserves data |
| Date storage | TEXT (YYYY-MM-DD) | Standard ISO format, easy comparison |
| Date validation | Python date.fromisoformat() | Built-in, strict validation |
| List filters | SQL WHERE with DATE() | Efficient, database-level filtering |
| Project storage | Separate table with FK | Full CRUD support, consistent naming |
| Statistics | SQL aggregates | Single query, efficient |
| Undo approach | In-memory, single action | Simple, meets spec requirements |

---

## Implementation Approach

### Database Migration (called in TodoManager.__init__)

1. Check if columns exist using PRAGMA table_info
2. Add missing columns (due_date, project_id)
3. Create projects table if not exists

### Filter Implementation

1. Add methods to TodoManager: `list_tasks_today()`, `list_tasks_overdue()`, `list_tasks_upcoming()`
2. Each method uses SQL WHERE clause with date comparison
3. Return List[Task] objects

### Project Management

1. Create ProjectManager class in project_manager.py
2. Methods: create_project(), list_projects(), get_project(), delete_project()
3. Task count calculated via JOIN or subquery

### Statistics

1. Add get_stats() method to TodoManager
2. Single SQL query with aggregates
3. Return dict with all metrics

### Undo (Optional)

1. Create undo.py with UndoAction dataclass
2. Store last action after each modifying operation
3. Execute reverse action on undo command

---

## Dependencies

**Existing (no changes)**:
- `rich` - Terminal styling
- `sqlite3` - Database (built-in)

**New**:
- None required

---

## Risks and Mitigations

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Schema migration fails | Low | Check columns before adding, handle errors gracefully |
| Date parsing errors | Medium | Validate input format, clear error messages |
| Project FK violations | Low | Check project exists before task assignment |
| Undo data loss | Low (expected) | Document in-memory limitation in help |

---

## References

- [SQLite ALTER TABLE](https://www.sqlite.org/lang_altertable.html)
- [SQLite Date Functions](https://www.sqlite.org/lang_datefunc.html)
- [Python datetime.date](https://docs.python.org/3/library/datetime.html#date-objects)
