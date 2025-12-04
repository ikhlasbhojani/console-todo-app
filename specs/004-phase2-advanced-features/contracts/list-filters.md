# CLI Contract: List Filters

**Feature Branch**: `004-phase2-advanced-features`
**Date**: 2025-12-05

---

## Overview

Extensions to the `list` command with filter flags for due date-based views.

---

## Commands

### list --today

Show all tasks due today (regardless of status).

**Input**:
```
todo ❯ list --today
```

**Output (tasks exist)**:
```
Tasks due today (2025-12-05):

┌────┬─────────────────────┬────────────┬────────────┬──────────┐
│ ID │ Title               │ Status     │ Due Date   │ Project  │
├────┼─────────────────────┼────────────┼────────────┼──────────┤
│  3 │ Team meeting        │ ○ Pending  │ 2025-12-05 │ work     │
│  7 │ Submit report       │ ✓ Done     │ 2025-12-05 │ work     │
└────┴─────────────────────┴────────────┴────────────┴──────────┘
```

**Output (no tasks)**:
```
Tasks due today (2025-12-05):

ℹ No tasks due today.
```

---

### list --overdue

Show all **pending** tasks with past due dates.

**Input**:
```
todo ❯ list --overdue
```

**Output (tasks exist)**:
```
Overdue tasks:

┌────┬─────────────────────┬────────────┬────────────┬──────────┐
│ ID │ Title               │ Status     │ Due Date   │ Project  │
├────┼─────────────────────┼────────────┼────────────┼──────────┤
│  1 │ Submit taxes        │ ○ Pending  │ 2025-12-01 │ personal │
│  5 │ Pay bills           │ ○ Pending  │ 2025-11-30 │ personal │
└────┴─────────────────────┴────────────┴────────────┴──────────┘
```

**Output (no overdue tasks)**:
```
Overdue tasks:

ℹ No overdue tasks. Great job!
```

**Note**: Completed tasks are NOT shown in overdue view.

---

### list --upcoming

Show all tasks due within the next 7 days (including today).

**Input**:
```
todo ❯ list --upcoming
```

**Output (tasks exist)**:
```
Upcoming tasks (next 7 days):

┌────┬─────────────────────┬────────────┬────────────┬──────────┐
│ ID │ Title               │ Status     │ Due Date   │ Project  │
├────┼─────────────────────┼────────────┼────────────┼──────────┤
│  3 │ Team meeting        │ ○ Pending  │ 2025-12-05 │ work     │
│  8 │ Doctor appointment  │ ○ Pending  │ 2025-12-08 │ personal │
│ 10 │ Project deadline    │ ○ Pending  │ 2025-12-10 │ work     │
└────┴─────────────────────┴────────────┴────────────┴──────────┘
```

**Output (no upcoming tasks)**:
```
Upcoming tasks (next 7 days):

ℹ No upcoming tasks in the next 7 days.
```

---

### list --project <name>

Show all tasks in a specific project.

**Input**:
```
todo ❯ list --project work
```

**Output (tasks exist)**:
```
Tasks in project 'work':

┌────┬─────────────────────┬────────────┬────────────┐
│ ID │ Title               │ Status     │ Due Date   │
├────┼─────────────────────┼────────────┼────────────┤
│  3 │ Team meeting        │ ○ Pending  │ 2025-12-05 │
│  7 │ Submit report       │ ✓ Done     │ 2025-12-03 │
│ 10 │ Project deadline    │ ○ Pending  │ 2025-12-10 │
└────┴─────────────────────┴────────────┴────────────┘
```

**Output (project not found)**:
```
✗ Project 'xyz' not found.
```

**Output (no tasks in project)**:
```
Tasks in project 'work':

ℹ No tasks in this project.
```

---

### list (default - updated)

Show all tasks with new columns for due date and project.

**Input**:
```
todo ❯ list
```

**Output**:
```
┌────┬─────────────────────┬────────────┬────────────┬──────────┬──────────────────┐
│ ID │ Title               │ Status     │ Due Date   │ Project  │ Created          │
├────┼─────────────────────┼────────────┼────────────┼──────────┼──────────────────┤
│  1 │ Submit taxes        │ ○ Pending  │ 2025-12-01 │ personal │ 2025-12-04 10:30 │
│  3 │ Team meeting        │ ○ Pending  │ 2025-12-05 │ work     │ 2025-12-04 11:15 │
│  5 │ Buy groceries       │ ✓ Done     │            │          │ 2025-12-04 12:00 │
└────┴─────────────────────┴────────────┴────────────┴──────────┴──────────────────┘
```

**Note**: Empty due_date and project show as blank cells.

---

## Error Handling

| Scenario | Message |
|----------|---------|
| Invalid flag | `✗ Unknown option: --invalid. See 'help' for usage.` |
| Project not found | `✗ Project 'xyz' not found.` |
| Multiple conflicting flags | Use first flag only (silent) |

---

## Implementation Notes

- Filters are mutually exclusive (--today, --overdue, --upcoming, --project)
- If multiple flags provided, use first one in order: --today > --overdue > --upcoming > --project
- Case-insensitive project matching
- Due date column shows formatted date or blank for null
- Project column shows project name (looked up by project_id) or blank for null
