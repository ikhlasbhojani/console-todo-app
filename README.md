# TODO APP

A modern, colorful console-based todo application. Manage your tasks right from your terminal with an intuitive interface.

## Features

### Core Task Management
- **Add Tasks** - Create tasks with title, description, due date, and project
- **List Tasks** - View all tasks in a beautiful styled table
- **Complete Tasks** - Mark tasks as done with visual indicators
- **Update Tasks** - Modify task titles and descriptions
- **Delete Tasks** - Remove tasks with confirmation
- **Persistent Storage** - Tasks are saved automatically
- **Colorful UI** - Modern terminal styling with colors and icons

### Due Dates & Filters
- **Due Dates** - Set due dates when creating tasks (YYYY-MM-DD format)
- **Today's Tasks** - `list --today` shows tasks due today
- **Overdue Tasks** - `list --overdue` shows pending tasks past their due date
- **Upcoming Tasks** - `list --upcoming` shows tasks due in the next 7 days

### Project Management
- **Create Projects** - Organize tasks into projects
- **List Projects** - View all projects with task counts
- **View Project** - See all tasks within a specific project
- **Delete Projects** - Remove projects (with optional cascade delete)
- **Filter by Project** - `list --project <name>` shows tasks in a project

### Statistics Dashboard
- **Stats Command** - View your productivity metrics at a glance
- **Completion Rate** - Track your task completion percentage
- **Overdue Alerts** - Get notified about overdue tasks

## Installation

### One-Command Install

#### Linux / macOS

```bash
curl -fsSL https://raw.githubusercontent.com/ikhlasbhojani/console-todo-app/main/scripts/install.sh | bash
```

#### Windows (PowerShell)

```powershell
irm https://raw.githubusercontent.com/ikhlasbhojani/console-todo-app/main/scripts/install.ps1 | iex
```

**That's it!** The installer automatically handles everything:
- Installs `uv` package manager
- Downloads Python 3.13 (managed by uv)
- Installs todo-app globally
- Configures your PATH

No need to install Python or anything else first!

## Quick Start

After installation, open any terminal and type:

```bash
todo-app
```

You'll see the welcome screen:

```
╭──────────────────────────────────────╮
│  TODO APP - Console Edition          │
╰──────────────────────────────────────╯
Type 'help' for available commands.

todo ❯
```

## Usage

### Adding a Task

```
todo ❯ add
Enter title: Buy groceries
Enter description: Milk, eggs, bread
Due date (YYYY-MM-DD, leave blank for none): 2025-12-10
Project (leave blank for none): shopping

✓ Task created with ID: 1
```

### Listing Tasks

```
todo ❯ list

┌────┬─────────────────────┬────────────┬────────────┬──────────┬──────────────────┐
│ ID │ Title               │ Status     │ Due Date   │ Project  │ Created          │
├────┼─────────────────────┼────────────┼────────────┼──────────┼──────────────────┤
│  1 │ Buy groceries       │ ○ Pending  │ 2025-12-10 │ shopping │ 2025-12-04 10:30 │
│  2 │ Call dentist        │ ✓ Done     │            │          │ 2025-12-04 11:15 │
└────┴─────────────────────┴────────────┴────────────┴──────────┴──────────────────┘
```

### Filtering Tasks

```
# Show tasks due today
todo ❯ list --today

# Show overdue tasks
todo ❯ list --overdue

# Show tasks due in the next 7 days
todo ❯ list --upcoming

# Show tasks in a specific project
todo ❯ list --project shopping
```

### Completing a Task

```
todo ❯ complete
Enter task ID to mark complete: 1

✓ Task 1 marked as completed.
```

### Updating a Task

```
todo ❯ update
Enter task ID to update: 1
New title (leave blank to keep current): Buy groceries and snacks
New description (leave blank to keep current):

✓ Task 1 updated.
```

### Deleting a Task

```
todo ❯ delete
Enter task ID to delete: 1
Are you sure you want to delete task 1? (y/n): y

✓ Task 1 deleted.
```

### Managing Projects

```
# Create a new project
todo ❯ project create
Enter project name: work
Enter description: Work-related tasks

✓ Project 'work' created.

# List all projects
todo ❯ project list

┌────┬──────────┬───────────────────────┬───────┬──────────────────┐
│ ID │ Name     │ Description           │ Tasks │ Created          │
├────┼──────────┼───────────────────────┼───────┼──────────────────┤
│  1 │ shopping │ Shopping errands      │     2 │ 2025-12-04 10:00 │
│  2 │ work     │ Work-related tasks    │     0 │ 2025-12-04 14:30 │
└────┴──────────┴───────────────────────┴───────┴──────────────────┘

# View tasks in a project
todo ❯ project view
Enter project name: shopping

# Delete a project
todo ❯ project delete
Enter project name: work
Delete associated tasks? (y/n): n

✓ Project 'work' deleted.
```

### Viewing Statistics

```
todo ❯ stats

┌──────────────────────┬────────┐
│ Metric               │  Value │
├──────────────────────┼────────┤
│ Total Tasks          │     10 │
│ Pending              │      4 │
│ Completed            │      6 │
│                      │        │
│ Due Today            │      2 │
│ Overdue              │      1 │
│                      │        │
│ Completion Rate      │  60.0% │
└──────────────────────┴────────┘

⚠ You have 1 overdue tasks. Run 'list --overdue' to see them.
```

### Getting Help

```
todo ❯ help

Available Commands:
  add              - Add a new task
  list             - Show all tasks
  list --today     - Show tasks due today
  list --overdue   - Show overdue tasks
  list --upcoming  - Show tasks due in 7 days
  list --project   - Show tasks in a project
  update           - Update an existing task
  complete         - Mark a task as completed
  delete           - Delete a task
  project create   - Create a new project
  project list     - List all projects
  project view     - View tasks in a project
  project delete   - Delete a project
  stats            - Show task statistics
  help             - Show this help message
  exit             - Quit the application
```

### Exiting

```
todo ❯ exit

Goodbye! 👋
```

## Command Reference

| Command            | Description                                    |
|--------------------|------------------------------------------------|
| `add`              | Add a new task (with due date and project)     |
| `list`             | Show all tasks in a table                      |
| `list --today`     | Show tasks due today                           |
| `list --overdue`   | Show overdue pending tasks                     |
| `list --upcoming`  | Show tasks due in the next 7 days              |
| `list --project`   | Show tasks in a specific project               |
| `complete`         | Mark a task as done                            |
| `update`           | Edit a task's title or description             |
| `delete`           | Remove a task (with confirmation)              |
| `project create`   | Create a new project                           |
| `project list`     | List all projects with task counts             |
| `project view`     | View all tasks in a project                    |
| `project delete`   | Delete a project (optional cascade)            |
| `stats`            | Show task statistics dashboard                 |
| `help`             | Show available commands                        |
| `exit`             | Quit the application                           |

## Data Storage

Your tasks are stored locally in:

- **Linux/macOS**: `~/.todo-app/todo.db`
- **Windows**: `%USERPROFILE%\.todo-app\todo.db`

## Troubleshooting

### "command not found: todo-app"

Restart your terminal or run:

```bash
# Linux/macOS
source ~/.bashrc  # or ~/.zshrc

# Windows - restart PowerShell
```

### Python version issues

The installer uses `uv` to automatically manage Python 3.13. If you encounter issues, ensure `uv` is installed and try again.

### Uninstall

To remove the application:

```bash
uv tool uninstall console-todo-app
```

## Requirements

- Internet connection (for installation only)
- Everything else is installed automatically!

## License

MIT License - See LICENSE file for details.
