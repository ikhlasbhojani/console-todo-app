## Spec-Kit Plus – Phase 2 Slash Commands for This Todo App

This file defines the **4 slash commands** you will use with Spec‑Kit Plus for Phase 2 (Advanced Features):

> **Note:** `/sp.constitution` is NOT included here because it's a **one-time command** that was already run in Phase 1. The constitution.md file created in Phase 1 will continue to govern Phase 2 development.

- `/sp.specify`
- `/sp.plan`
- `/sp.tasks`
- `/sp.implement`

---

### 1. `/sp.specify`

#### 📝 AI Prompt Instruction

```
/sp.specify Create the functional specification for "TODO APP - PHASE 2 (Advanced Features)" building on the Phase 1 SQLite todo application.

**PHASE 2 OBJECTIVE:**
Add advanced features to the Phase 1 console todo app: due dates with filtered views, project categorization, statistics, and optional undo functionality.

**NEW DATA MODEL FIELDS:**
- **due_date**: Optional date when task is due (stored as TEXT in ISO format: YYYY-MM-DD)
- **project**: Optional project/category name (e.g., "work", "personal", "study")

**NEW FEATURES:**

### Feature 2.1: Due Dates & Filtered Views

**Add command update:**
```

> add
> Enter title: Submit report
> Enter description: Q4 financial report
> Enter due date (YYYY-MM-DD or leave blank): 2025-12-10
> Enter project (optional): work

[OK] Task created with ID: 5

```

**New list filters:**
```

> list --today
> Tasks due today (2025-12-04):

ID Title Status Due Date Project

---

3 Team meeting [ ] Pending 2025-12-04 work

> list --overdue
> Overdue tasks:

ID Title Status Due Date Project

---

1 Submit taxes [ ] Pending 2025-12-01 personal

> list --upcoming
> Upcoming tasks (next 7 days):

ID Title Status Due Date Project

---

5 Submit report [ ] Pending 2025-12-10 work

```

### Feature 2.2: Project Management (Full CRUD)

Projects are now **separate entities** that can be created, listed, viewed, and deleted.

**New `projects` table:**
- id (auto-generated)
- name (unique, required)
- description (optional)
- created_at

**Project Commands:**

```

> project create
> Enter project name: work
> Enter description (optional): Office related tasks

[OK] Project 'work' created with ID: 1

> project list

ID Name Tasks Created At

---

1 work 5 2025-12-04 10:00
2 personal 3 2025-12-04 10:15
3 study 2 2025-12-04 10:30

> project view work

Tasks in project 'work':

ID Title Status Due Date

---

1 Team meeting [ ] Pending 2025-12-04
3 Submit report [x] Done 2025-12-03

> project delete
> Enter project name to delete: study

Are you sure you want to delete project 'study'? This will also delete 2 tasks. (y/n): y

[OK] Project 'study' and its 2 tasks deleted.

```

**Task-Project Association (updated add command):**

```

> add
> Enter title: New task
> Enter description: Task description
> Enter due date (YYYY-MM-DD or leave blank): 2025-12-10
> Assign to project (leave blank for none): work

[OK] Task created with ID: 10 in project 'work'

```

**Error handling:**
- `[ERROR] Project 'xyz' not found. Create it first with 'project create'.`
- `[ERROR] Project name already exists.`
- `[ERROR] Cannot delete project with tasks. Delete tasks first or confirm cascade delete.`

### Feature 2.3: Stats Command

```

> stats

# 📊 Task Statistics

Total tasks: 15
Pending: 8
Completed: 7
Due today: 2
Overdue: 1

Completion rate: 47%

```

### Feature 2.4: Undo Command (Optional/Stretch)

```

> add
> Enter title: Test task
> ...
> [OK] Task created with ID: 10

> undo

[OK] Undone: Deleted task 10 (Test task)

> delete
> Enter task ID to delete: 5
> ...
> [OK] Task 5 deleted.

> undo

[OK] Undone: Restored task 5 (Submit report)

```

**UPDATED HELP OUTPUT:**
```

> help

Available commands:
add - Add a new task
list - Show all tasks
list --today - Show tasks due today
list --overdue - Show overdue pending tasks
list --upcoming - Show tasks due in next 7 days
update - Update an existing task
complete - Mark a task as completed
delete - Delete a task

project create - Create a new project
project list - Show all projects with task counts
project view <name> - Show all tasks in a project
project delete - Delete a project and its tasks

stats - Show task statistics
undo - Undo the last action (if available)
help - Show this help message
exit - Quit the application

```

**VALIDATION RULES:**
- due_date must be valid date format (YYYY-MM-DD) or empty
- project name should be alphanumeric with underscores (e.g., work, personal_tasks)
- --project filter should be case-insensitive
- undo only works for the last action (single-level undo)
```

---

### 2. `/sp.plan`

#### 📝 AI Prompt Instruction

````
/sp.plan Create the technical implementation plan for Phase 2 advanced features.

**TECHNOLOGY STACK (Same as Phase 1):**
- Python 3.13+
- Package manager: `uv`
- Storage: SQLite database `data/todo.db`
- Testing: `pytest`
- Linting: `ruff`

**DATABASE SCHEMA CHANGES:**

**Updated `tasks` table:**
```sql
ALTER TABLE tasks ADD COLUMN due_date TEXT;
ALTER TABLE tasks ADD COLUMN project TEXT;
````

**New `action_history` table (for undo feature):**

```sql
CREATE TABLE IF NOT EXISTS action_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    action_type TEXT NOT NULL,  -- 'add', 'update', 'delete', 'complete'
    task_id INTEGER,
    old_data TEXT,  -- JSON of previous task state
    new_data TEXT,  -- JSON of new task state
    created_at TEXT
);
```

**UPDATED DATA MODEL (`src/models.py`):**

```python
@dataclass
class Task:
    id: int
    title: str
    description: str
    status: str
    created_at: datetime
    updated_at: datetime
    due_date: Optional[date] = None      # NEW
    project: Optional[str] = None         # NEW
```

**NEW/UPDATED TODOMANAGER METHODS:**

```python
class TodoManager:
    # Updated methods
    def add_task(title, description, due_date=None, project=None)
    def update_task(id, title=None, description=None, due_date=None, project=None)

    # New filter methods
    def list_tasks_today() -> List[Task]
    def list_tasks_overdue() -> List[Task]
    def list_tasks_upcoming(days=7) -> List[Task]
    def list_tasks_by_project(project: str) -> List[Task]

    # Stats method
    def get_stats() -> dict

    # Undo methods (optional)
    def record_action(action_type, task_id, old_data, new_data)
    def undo_last_action() -> bool
```

**CLI UPDATES (`src/main.py`):**

- Parse `--today`, `--overdue`, `--upcoming`, `--project` flags for `list` command
- Add `stats` command handler
- Add `undo` command handler (optional)
- Update `add` prompts for due_date and project
- Update `list` output format to include due_date and project columns

**DIRECTORY STRUCTURE (additions):**

```
console-todo-app/
├── src/
│   ├── filters.py          # NEW: Filter logic for list command
│   ├── stats.py             # NEW: Statistics calculations
│   └── history.py           # NEW: Action history for undo (optional)
├── Specification-phase-2/   # NEW: Phase 2 specs
│   └── Specification2.md
└── ...
```

**DEVELOPMENT PHASES:**

1. Database migration (add new columns)
2. Update Task model and TodoManager
3. Implement filter methods
4. Implement stats command
5. Update CLI with new commands/options
6. Implement undo (optional)
7. Add tests for new features
8. Update documentation

```

---

### 3. `/sp.tasks`

#### 📝 AI Prompt Instruction

```

/sp.tasks

```

> **Note:** This command takes NO arguments. The AI will automatically read the plan and break it into tasks.

#### 📋 Expected Output (Tasks the AI Should Generate)

The AI should create the following tasks:

**PHASE 2.1: DATABASE MIGRATION**
- Task 1: Create migration script to add `due_date` column to tasks table
- Task 2: Create migration script to add `project` column to tasks table
- Task 3: Create `action_history` table for undo feature (optional)
- Task 4: Test migrations with existing Phase 1 data

**PHASE 2.2: MODEL UPDATES**
- Task 5: Update `Task` dataclass with `due_date` and `project` fields
- Task 6: Update `TodoManager.add_task()` to accept due_date and project
- Task 7: Update `TodoManager.update_task()` to handle new fields

**PHASE 2.3: FILTER METHODS**
- Task 8: Implement `list_tasks_today()` - tasks where due_date = today
- Task 9: Implement `list_tasks_overdue()` - pending tasks where due_date < today
- Task 10: Implement `list_tasks_upcoming(days=7)` - tasks due within N days
- Task 11: Implement `list_tasks_by_project(project)` - filter by project name

**PHASE 2.4: STATS FEATURE**
- Task 12: Create `src/stats.py` with `get_stats()` function
- Task 13: Calculate: total, pending, completed, due today, overdue
- Task 14: Implement `stats` command in CLI

**PHASE 2.5: CLI UPDATES**
- Task 15: Update `add` command to prompt for due_date and project
- Task 16: Parse list command flags: --today, --overdue, --upcoming, --project
- Task 17: Update `list` output format to show due_date and project columns
- Task 18: Update `help` command with new options

**PHASE 2.6: UNDO FEATURE (Optional)**
- Task 19: Create `src/history.py` with action recording functions
- Task 20: Record actions in `action_history` table
- Task 21: Implement `undo_last_action()` method
- Task 22: Implement `undo` command in CLI

**PHASE 2.7: TESTING**
- Task 23: Write tests for new Task model fields
- Task 24: Write tests for filter methods
- Task 25: Write tests for stats calculations
- Task 26: Write tests for undo functionality (optional)

**PHASE 2.8: DOCUMENTATION**
- Task 27: Update README.md with Phase 2 features
- Task 28: Update help output in CLI
- Task 29: Document database schema changes

---

### 4. `/sp.implement`

#### 📝 AI Prompt Instruction

```

/sp.implement

````

> **Note:** This command takes NO arguments. The AI will automatically read the tasks and execute them in order.

#### 📋 What the AI Will Do

**IMPLEMENTATION ORDER:**
1. Phase 2.1 (Tasks 1-4): Database migration
2. Phase 2.2 (Tasks 5-7): Model updates
3. Phase 2.3 (Tasks 8-11): Filter methods
4. Phase 2.4 (Tasks 12-14): Stats feature
5. Phase 2.5 (Tasks 15-18): CLI updates
6. Phase 2.6 (Tasks 19-22): Undo feature (optional)
7. Phase 2.7 (Tasks 23-26): Testing
8. Phase 2.8 (Tasks 27-29): Documentation

#### 📋 Key Implementation Rules

- Maintain backward compatibility with Phase 1
- New fields should have NULL defaults
- Use ISO 8601 date format (YYYY-MM-DD)
- All existing tests must continue to pass
- Follow constitution.md rules

#### 📋 Console Output Format (New Commands)

| Action | Output Message |
|--------|----------------|
| List today | `Tasks due today (YYYY-MM-DD):` |
| List overdue | `Overdue tasks:` |
| List by project | `Tasks in project 'NAME':` |
| Stats header | `📊 Task Statistics` |
| Undo success | `[OK] Undone: <action description>` |
| Undo nothing | `[INFO] Nothing to undo.` |
| Invalid date | `[ERROR] Invalid date format. Use YYYY-MM-DD.` |

#### 📋 Validation Checkpoints

- After Phase 2.1: Verify database has new columns with `sqlite3 data/todo.db ".schema tasks"`
- After Phase 2.3: Test filter commands manually
- After Phase 2.4: Run `stats` command and verify output
- After Phase 2.7: Run `uv run pytest` - all tests should pass

#### 📋 Run Commands

```bash
# Run the app
uv run python -m src.main

# Run tests
uv run pytest

# Check database schema
sqlite3 data/todo.db ".schema"
````

---

## Summary

| Command         | Key Details from plan2.md                                                 |
| --------------- | ------------------------------------------------------------------------- |
| `/sp.specify`   | Due dates, projects, filters (--today, --overdue, --project), stats, undo |
| `/sp.plan`      | Schema changes, new TodoManager methods, CLI updates                      |
| `/sp.tasks`     | 29 tasks across 8 phases                                                  |
| `/sp.implement` | Implementation order, output format, validation checkpoints               |
