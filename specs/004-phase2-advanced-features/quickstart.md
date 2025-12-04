# Quickstart Guide: TODO APP - PHASE 2 (Advanced Features)

**Feature Branch**: `004-phase2-advanced-features`
**Date**: 2025-12-05
**Spec**: [spec.md](spec.md)

---

## Prerequisites

- Phase 1 todo application installed and working
- Python 3.13+
- `uv` package manager

---

## Testing the New Features

### 1. Due Dates

**Create a task with a due date:**
```
todo ❯ add
📝 Add New Task

Title: Submit quarterly report
Description (optional): Q4 financial summary
Due date (YYYY-MM-DD, optional): 2025-12-10
Project (optional):

✓ Task added successfully! (ID: 1)
```

**Create more tasks with different due dates:**
```
# Task due today
todo ❯ add
Title: Team standup
Due date (YYYY-MM-DD, optional): 2025-12-05

# Task due yesterday (overdue)
todo ❯ add
Title: Send invoice
Due date (YYYY-MM-DD, optional): 2025-12-04

# Task due next week
todo ❯ add
Title: Project review
Due date (YYYY-MM-DD, optional): 2025-12-12
```

**Filter tasks by due date:**
```
# Tasks due today
todo ❯ list --today

# Overdue pending tasks
todo ❯ list --overdue

# Tasks due in next 7 days
todo ❯ list --upcoming
```

---

### 2. Project Management

**Create a project:**
```
todo ❯ project create
📁 Create New Project

Project name: work
Description (optional): Work-related tasks

✓ Project 'work' created successfully.
```

**List all projects:**
```
todo ❯ project list
📁 Projects:

┌────┬──────┬──────────────────────┬───────┬──────────────────┐
│ ID │ Name │ Description          │ Tasks │ Created          │
├────┼──────┼──────────────────────┼───────┼──────────────────┤
│  1 │ work │ Work-related tasks   │     0 │ 2025-12-05 10:00 │
└────┴──────┴──────────────────────┴───────┴──────────────────┘
```

**Add a task to a project:**
```
todo ❯ add
📝 Add New Task

Title: Prepare presentation
Description (optional): Q4 sales deck
Due date (YYYY-MM-DD, optional): 2025-12-08
Project (optional): work

✓ Task added successfully! (ID: 5, Project: work)
```

**View project tasks:**
```
todo ❯ project view work
📁 Project: work
   Work-related tasks

┌────┬──────────────────────┬────────────┬────────────┬──────────────────┐
│ ID │ Title                │ Status     │ Due Date   │ Created          │
├────┼──────────────────────┼────────────┼────────────┼──────────────────┤
│  5 │ Prepare presentation │ ○ Pending  │ 2025-12-08 │ 2025-12-05 10:05 │
└────┴──────────────────────┴────────────┴────────────┴──────────────────┘

Total: 1 tasks (1 pending, 0 completed)
```

**Filter list by project:**
```
todo ❯ list --project work
```

**Delete a project:**
```
todo ❯ project delete
📁 Delete Project

Project name: work

⚠ Project 'work' has 1 tasks. Delete project and all its tasks? (y/n): y

✓ Project 'work' and 1 tasks deleted.
```

---

### 3. Statistics Dashboard

**View task statistics:**
```
todo ❯ stats
📊 Task Statistics

┌────────────────────┬───────┐
│ Metric             │ Value │
├────────────────────┼───────┤
│ Total Tasks        │     4 │
│ Pending            │     3 │
│ Completed          │     1 │
├────────────────────┼───────┤
│ Due Today          │     1 │
│ Overdue            │     1 │
├────────────────────┼───────┤
│ Completion Rate    │ 25.0% │
└────────────────────┴───────┘

⚠ You have 1 overdue tasks. Run 'list --overdue' to see them.
```

---

### 4. Undo (Optional Feature)

**Undo the last action:**
```
# Add a task
todo ❯ add
Title: Test task
✓ Task added successfully! (ID: 6)

# Undo the add
todo ❯ undo
✓ Undo: Task 6 deleted.

# Try undo again
todo ❯ undo
ℹ Nothing to undo.
```

**Other undo scenarios:**
```
# Complete a task, then undo
todo ❯ done
Task ID to complete: 1
✓ Task 1 marked as done!

todo ❯ undo
✓ Undo: Task 1 restored to pending.

# Delete a task, then undo
todo ❯ delete
Task ID to delete: 2
✓ Task deleted.

todo ❯ undo
✓ Undo: Task 2 restored.
```

---

## Running Tests

```bash
# Run all tests
uv run pytest

# Run only Phase 2 tests
uv run pytest tests/test_todo_manager.py -k "filter or project or stats"
uv run pytest tests/test_project_manager.py
uv run pytest tests/test_stats.py

# Run with coverage
uv run pytest --cov=src

# Lint check
uv run ruff check src tests
```

---

## Database Verification

After running the app, verify the database schema:

```bash
# Check the database
sqlite3 ~/.todo-app/todo.db

# Verify tasks table has new columns
.schema tasks
-- Should show: due_date TEXT, project_id INTEGER

# Verify projects table exists
.schema projects
-- Should show: id, name, description, created_at

# Exit sqlite
.quit
```

---

## Validation Checklist

- [ ] Can add task with due date in YYYY-MM-DD format
- [ ] Invalid date format shows error message
- [ ] `list --today` shows only today's tasks
- [ ] `list --overdue` shows only pending overdue tasks
- [ ] `list --upcoming` shows next 7 days of tasks
- [ ] Can create project with name and description
- [ ] Duplicate project name shows error
- [ ] `project list` shows all projects with task counts
- [ ] `project view <name>` shows project's tasks
- [ ] `project delete` confirms if project has tasks
- [ ] Can assign task to project during creation
- [ ] `stats` shows all metrics correctly
- [ ] Completion rate calculated correctly
- [ ] Undo reverses last action (if implemented)
- [ ] Help shows all new commands
