# TODO APP

A modern, colorful console-based todo application. Manage your tasks right from your terminal with an intuitive interface.

## Features

- **Add Tasks** - Create tasks with title and description
- **List Tasks** - View all tasks in a beautiful styled table
- **Complete Tasks** - Mark tasks as done with visual indicators
- **Update Tasks** - Modify task titles and descriptions
- **Delete Tasks** - Remove tasks with confirmation
- **Persistent Storage** - Tasks are saved automatically
- **Colorful UI** - Modern terminal styling with colors and icons

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

✓ Task created with ID: 1
```

### Listing Tasks

```
todo ❯ list

┌────┬─────────────────────┬────────────┬──────────────────┐
│ ID │ Title               │ Status     │ Created          │
├────┼─────────────────────┼────────────┼──────────────────┤
│  1 │ Buy groceries       │ ○ Pending  │ 2025-12-04 10:30 │
│  2 │ Call dentist        │ ✓ Done     │ 2025-12-04 11:15 │
└────┴─────────────────────┴────────────┴──────────────────┘
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

### Getting Help

```
todo ❯ help

Available Commands:
  add      - Add a new task
  list     - Show all tasks
  update   - Update an existing task (title/description)
  complete - Mark a task as completed
  delete   - Delete a task
  help     - Show this help message
  exit     - Quit the application
```

### Exiting

```
todo ❯ exit

Goodbye! 👋
```

## Command Reference

| Command    | Description                           |
|------------|---------------------------------------|
| `add`      | Add a new task                        |
| `list`     | Show all tasks in a table             |
| `complete` | Mark a task as done                   |
| `update`   | Edit a task's title or description    |
| `delete`   | Remove a task (with confirmation)     |
| `help`     | Show available commands               |
| `exit`     | Quit the application                  |

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
