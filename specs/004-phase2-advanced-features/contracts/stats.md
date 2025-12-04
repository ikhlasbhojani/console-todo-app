# CLI Contract: Statistics Dashboard

**Feature Branch**: `004-phase2-advanced-features`
**Date**: 2025-12-05

---

## Overview

Display comprehensive task statistics including counts, completion rates, and deadline status in a formatted dashboard.

---

## Commands

### stats

Show the task statistics dashboard.

**Input**:
```
todo ❯ stats
```

**Output (tasks exist)**:
```
📊 Task Statistics

┌────────────────────┬───────┐
│ Metric             │ Value │
├────────────────────┼───────┤
│ Total Tasks        │    15 │
│ Pending            │     8 │
│ Completed          │     7 │
├────────────────────┼───────┤
│ Due Today          │     2 │
│ Overdue            │     3 │
├────────────────────┼───────┤
│ Completion Rate    │ 46.7% │
└────────────────────┴───────┘
```

**Output (no tasks)**:
```
📊 Task Statistics

ℹ No tasks yet. Add one with 'add'.
```

**Output (all tasks completed)**:
```
📊 Task Statistics

┌────────────────────┬────────┐
│ Metric             │ Value  │
├────────────────────┼────────┤
│ Total Tasks        │     10 │
│ Pending            │      0 │
│ Completed          │     10 │
├────────────────────┼────────┤
│ Due Today          │      0 │
│ Overdue            │      0 │
├────────────────────┼────────┤
│ Completion Rate    │ 100.0% │
└────────────────────┴────────┘

🎉 Amazing! All tasks completed!
```

**Output (overdue tasks warning)**:
```
📊 Task Statistics

┌────────────────────┬───────┐
│ Metric             │ Value │
├────────────────────┼───────┤
│ Total Tasks        │    20 │
│ Pending            │    12 │
│ Completed          │     8 │
├────────────────────┼───────┤
│ Due Today          │     3 │
│ Overdue            │     5 │
├────────────────────┼───────┤
│ Completion Rate    │ 40.0% │
└────────────────────┴───────┘

⚠ You have 5 overdue tasks. Run 'list --overdue' to see them.
```

---

## Metric Definitions

| Metric | Definition | Calculation |
|--------|------------|-------------|
| Total Tasks | All tasks in the database | `COUNT(*)` |
| Pending | Tasks with status = 'pending' | `COUNT(*) WHERE status = 'pending'` |
| Completed | Tasks with status = 'done' | `COUNT(*) WHERE status = 'done'` |
| Due Today | Tasks due on current date | `COUNT(*) WHERE due_date = DATE('now', 'localtime')` |
| Overdue | Pending tasks with past due dates | `COUNT(*) WHERE due_date < DATE('now', 'localtime') AND status = 'pending'` |
| Completion Rate | Percentage of completed tasks | `(Completed / Total) * 100` |

---

## Special Cases

### No Due Dates Set

If no tasks have due dates, "Due Today" and "Overdue" still show as 0:

```
📊 Task Statistics

┌────────────────────┬───────┐
│ Metric             │ Value │
├────────────────────┼───────┤
│ Total Tasks        │     5 │
│ Pending            │     3 │
│ Completed          │     2 │
├────────────────────┼───────┤
│ Due Today          │     0 │
│ Overdue            │     0 │
├────────────────────┼───────┤
│ Completion Rate    │ 40.0% │
└────────────────────┴───────┘
```

### Zero Tasks

Display informational message instead of table with zeros:

```
📊 Task Statistics

ℹ No tasks yet. Add one with 'add'.
```

---

## Contextual Messages

| Condition | Message |
|-----------|---------|
| All tasks completed | `🎉 Amazing! All tasks completed!` |
| Overdue tasks exist | `⚠ You have N overdue tasks. Run 'list --overdue' to see them.` |
| Due today exists | (no special message) |
| No tasks | `ℹ No tasks yet. Add one with 'add'.` |

---

## Implementation Notes

- All statistics calculated in a single SQL query for efficiency
- Completion rate formatted to 1 decimal place (e.g., 46.7%)
- Completion rate shows 0.0% when no tasks exist (edge case: avoid division by zero)
- Table uses `rich` styling consistent with other tables
- Overdue warning appears only when overdue > 0
- "All completed" celebration appears only when pending = 0 AND total > 0
