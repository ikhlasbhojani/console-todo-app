## Phase 2: Advanced Features on Top of SQLite

### 1. Phase 2 Overview

- **Goal:** Build on the Phase 1 SQLite-based console todo app by adding more powerful, user-friendly features.
- **Scope:** Keep the same persistent SQLite storage, and add selected “smart” features (filters, projects, stats, etc.).

### 2. New Features for Phase 2

Below are selected “good” features to implement in Phase 2, making use of SQLite where useful.

#### 2.1 Reminders & “Due Today” View

- **New field:** `due_date` on `Task` (stored in SQLite as text/datetime).
- **Commands / options:**
  - `list --today` → Shows tasks with `due_date = today`.
  - `list --overdue` → Shows tasks where `due_date < today` and `status = 'pending'`.
  - `list --upcoming` → Shows tasks with `due_date > today` (up to some range).
- Purpose: Even without real OS notifications, these filtered views feel like reminders.

#### 2.2 Project Management (Full CRUD)

Projects are now **separate entities** with their own table and full CRUD operations.

- **New table:** `projects`

  - `id` INTEGER PRIMARY KEY AUTOINCREMENT
  - `name` TEXT NOT NULL UNIQUE
  - `description` TEXT
  - `created_at` TEXT

- **Task linkage:** `tasks.project_id` (foreign key to `projects.id`)

**Project Commands:**

| Command               | Description                          |
| --------------------- | ------------------------------------ |
| `project create`      | Create a new project                 |
| `project list`        | Show all projects with task counts   |
| `project delete`      | Delete a project (with confirmation) |
| `project view <name>` | Show all tasks in a specific project |

**Console Flows:**

```text
> project create
Enter project name: work
Enter description (optional): Office related tasks

[OK] Project 'work' created with ID: 1

> project list

ID  Name       Tasks   Created At
--  ---------  ------  -------------------
1   work       5       2025-12-04 10:00
2   personal   3       2025-12-04 10:15
3   study      2       2025-12-04 10:30

> project view work

Tasks in project 'work':

ID  Title           Status      Due Date
--  --------------  ----------  ----------
1   Team meeting    [ ] Pending 2025-12-04
3   Submit report   [x] Done    2025-12-03

> project delete
Enter project name to delete: study

Are you sure you want to delete project 'study'? This will also delete 2 tasks. (y/n): y

[OK] Project 'study' and its 2 tasks deleted.
```

**Task-Project Association:**

When creating a task, user can assign it to an existing project:

```text
> add
Enter title: New task
Enter description: Task description
Enter due date (YYYY-MM-DD or leave blank):
Assign to project (leave blank for none): work

[OK] Task created with ID: 10 in project 'work'
```

- If project doesn't exist, show error: `[ERROR] Project 'xyz' not found. Create it first with 'project create'.`
- Tasks without project are shown in "No Project" category

#### 2.3 Saved Filters / Views (Optional / Stretch)

- Let the user define named views that store a filter.
- Example concept:
  - `view add focus "status='pending' AND project='work'"`.
  - `view focus` → Runs the stored filter and shows matching tasks.
- **Storage:** Could be another table, e.g. `views` with `name` and `query/filter`.

#### 2.4 Undo Last Action (Optional / Stretch)

- Track recent actions (add, update, delete, complete) in a small history.
- `undo` command:
  - For `add` → delete the newly added task.
  - For `delete` → restore the deleted task (possibly from a backup/trash table).
  - For `update` → restore old values.
  - For `complete` → revert `status` to previous value.

#### 2.5 Stats / Summary Command

- New command: `stats`
  - Show:
    - Total tasks.
    - Pending vs completed.
    - Tasks due today.
    - Overdue tasks.
  - Optional: “streak” – number of days in a row with at least one completed task.

### 3. CLI Additions / Changes

- Extend `help` output to include new filters and commands, for example:

```text
  list --today        - Show tasks due today
  list --overdue      - Show overdue pending tasks
  list --project NAME - Show tasks in a specific project
  stats               - Show task statistics
  undo                - Undo the last action (optional/stretch)
```

### 4. Development Plan for Phase 2 (High Level)

1. **Design DB schema**
   - Decide final columns for `tasks` (and extra tables like `views`, `history` if needed).
2. **Ensure SQLite layer is solid**
   - Reuse/extend existing `init_db()` and connection helpers from Phase 1.
3. **Add new CLI commands & options**
   - `list` filters (`--today`, `--overdue`, `--project`), `stats`, maybe `undo`.
4. **Testing**
   - Add tests to ensure data is correctly stored/retrieved from SQLite.
   - Test new filters and stats.
5. **Documentation**
   - Update `README.md` to explain Phase 2 features.
   - Describe how SQLite file is created and where it is stored.
