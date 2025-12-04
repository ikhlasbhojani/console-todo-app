# CLI Contract: Project Management

**Feature Branch**: `004-phase2-advanced-features`
**Date**: 2025-12-05

---

## Overview

Full CRUD operations for projects (categories) that organize tasks into logical groupings.

---

## Commands

### project create

Create a new project/category for organizing tasks.

**Input**:
```
todo ❯ project create
```

**Prompts**:
```
📁 Create New Project

Project name: work
Description (optional): Work-related tasks and deadlines
```

**Output (success)**:
```
✓ Project 'work' created successfully.
```

**Output (duplicate name)**:
```
✗ Project name already exists.
```

**Output (invalid name)**:
```
✗ Project name must be alphanumeric (underscores allowed).
```

**Output (empty name)**:
```
✗ Project name cannot be empty.
```

---

### project list

Show all projects with task counts.

**Input**:
```
todo ❯ project list
```

**Output (projects exist)**:
```
📁 Projects:

┌────┬──────────┬────────────────────────────┬───────┬──────────────────┐
│ ID │ Name     │ Description                │ Tasks │ Created          │
├────┼──────────┼────────────────────────────┼───────┼──────────────────┤
│  1 │ work     │ Work-related tasks         │     5 │ 2025-12-04 10:30 │
│  2 │ personal │ Personal errands           │     3 │ 2025-12-04 11:15 │
│  3 │ study    │                            │     0 │ 2025-12-05 09:00 │
└────┴──────────┴────────────────────────────┴───────┴──────────────────┘
```

**Output (no projects)**:
```
📁 Projects:

ℹ No projects yet. Create one with 'project create'.
```

---

### project view <name>

Show all tasks in a specific project.

**Input**:
```
todo ❯ project view work
```

**Output (tasks exist)**:
```
📁 Project: work
   Work-related tasks

┌────┬─────────────────────┬────────────┬────────────┬──────────────────┐
│ ID │ Title               │ Status     │ Due Date   │ Created          │
├────┼─────────────────────┼────────────┼────────────┼──────────────────┤
│  3 │ Team meeting        │ ○ Pending  │ 2025-12-05 │ 2025-12-04 11:15 │
│  7 │ Submit report       │ ✓ Done     │ 2025-12-03 │ 2025-12-04 14:00 │
│ 10 │ Project deadline    │ ○ Pending  │ 2025-12-10 │ 2025-12-05 09:30 │
└────┴─────────────────────┴────────────┴────────────┴──────────────────┘

Total: 3 tasks (2 pending, 1 completed)
```

**Output (no tasks in project)**:
```
📁 Project: study

ℹ No tasks in this project.
```

**Output (project not found)**:
```
✗ Project 'xyz' not found.
```

---

### project delete

Delete a project and optionally its associated tasks.

**Input**:
```
todo ❯ project delete
```

**Prompts (project has tasks)**:
```
📁 Delete Project

Project name: work

⚠ Project 'work' has 5 tasks. Delete project and all its tasks? (y/n): y
```

**Output (deleted with tasks)**:
```
✓ Project 'work' and 5 tasks deleted.
```

**Prompts (project has no tasks)**:
```
📁 Delete Project

Project name: study
```

**Output (deleted, no tasks)**:
```
✓ Project 'study' deleted.
```

**Output (cancelled)**:
```
ℹ Deletion cancelled.
```

**Output (project not found)**:
```
✗ Project 'xyz' not found.
```

---

## Task Assignment to Project

### add (updated prompts)

When adding a task, user can optionally assign it to a project.

**Input**:
```
todo ❯ add
```

**Prompts**:
```
📝 Add New Task

Title: Complete quarterly report
Description (optional): Q4 financial summary
Due date (YYYY-MM-DD, optional): 2025-12-15
Project (optional): work
```

**Output (success with project)**:
```
✓ Task added successfully! (ID: 12, Project: work)
```

**Output (success without project)**:
```
✓ Task added successfully! (ID: 12)
```

**Output (project not found)**:
```
✗ Project 'xyz' not found. Create it first with 'project create'.
```

---

## list --project <name>

Filter tasks by project (documented in list-filters.md but linked here for reference).

**Input**:
```
todo ❯ list --project work
```

**Output**: See `list-filters.md` for full specification.

---

## Error Handling

| Scenario | Message |
|----------|---------|
| Empty project name | `✗ Project name cannot be empty.` |
| Invalid characters | `✗ Project name must be alphanumeric (underscores allowed).` |
| Duplicate name | `✗ Project name already exists.` |
| Project not found | `✗ Project '<name>' not found.` |
| Delete with tasks (no confirm) | `ℹ Deletion cancelled.` |

---

## Implementation Notes

- Project names are stored as-is but matched case-insensitively
- Alphanumeric characters and underscores only: `^[a-zA-Z0-9_]+$`
- Task count is calculated via COUNT query on tasks.project_id
- Cascade delete removes all associated tasks when confirmed
- Project description can be empty (displays as blank cell)
- Created timestamp uses same format as tasks: `YYYY-MM-DD HH:MM`
