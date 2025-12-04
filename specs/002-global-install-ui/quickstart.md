# Quickstart: TODO APP Installation & Usage

**Feature Branch**: `002-global-install-ui`
**Date**: 2025-12-04
**GitHub**: https://github.com/ikhlasbhojani/console-todo-app

---

## One-Command Installation

### Linux / macOS

Open your terminal and run:

```bash
curl -fsSL https://raw.githubusercontent.com/ikhlasbhojani/console-todo-app/main/scripts/install.sh | bash
```

### Windows (PowerShell)

Open PowerShell and run:

```powershell
irm https://raw.githubusercontent.com/ikhlasbhojani/console-todo-app/main/scripts/install.ps1 | iex
```

### What happens during installation:

1. ✓ Checks for Python 3.13+
2. ✓ Installs `uv` package manager (if not installed)
3. ✓ Installs `todo-app` globally
4. ✓ Adds command to your PATH
5. ✓ Shows success message

**Expected Output:**
```
╔══════════════════════════════════════════════╗
║     TODO APP - Installation Complete!         ║
╚══════════════════════════════════════════════╝

✓ uv package manager installed
✓ todo-app installed globally
✓ PATH configured

You can now run: todo-app
```

---

## Running the Application

After installation, open any terminal and type:

```bash
todo-app
```

You'll see:
```
╔══════════════════════════════════════╗
║       TODO APP - Console Edition      ║
╚══════════════════════════════════════╝
Type 'help' for available commands.

todo ❯
```

---

## Basic Usage

### Add a Task

```
todo ❯ add
Enter title: Buy groceries
Enter description: Milk, eggs, bread

[✓] Task created with ID: 1
```

### List Tasks

```
todo ❯ list

┌────┬─────────────────────┬────────────┬──────────────────┐
│ ID │ Title               │ Status     │ Created          │
├────┼─────────────────────┼────────────┼──────────────────┤
│  1 │ Buy groceries       │ ○ Pending  │ 2025-12-04 10:30 │
└────┴─────────────────────┴────────────┴──────────────────┘
```

### Complete a Task

```
todo ❯ complete
Enter task ID: 1

[✓] Task 1 marked as completed
```

### Update a Task

```
todo ❯ update
Enter task ID: 1
New title (blank to keep): Buy groceries and snacks
New description (blank to keep):

[✓] Task 1 updated
```

### Delete a Task

```
todo ❯ delete
Enter task ID: 1
Delete task 1? (y/n): y

[✓] Task 1 deleted
```

### Get Help

```
todo ❯ help

Available Commands:
  add       Add a new task
  list      Show all tasks
  complete  Mark task as done
  update    Edit task details
  delete    Remove a task
  help      Show this help
  exit      Quit application
```

### Exit

```
todo ❯ exit

Goodbye! 👋
```

---

## Troubleshooting

### "command not found: todo-app"

Restart your terminal or run:
```bash
source ~/.bashrc  # Linux
source ~/.zshrc   # macOS with zsh
```

For Windows, restart PowerShell.

### "Python 3.13+ required"

Install Python 3.13 or higher from [python.org](https://python.org)

### "Permission denied"

The installer doesn't require sudo. If you see permission errors, check that `~/.local/bin` is writable.

---

## Uninstall

To remove todo-app:

```bash
uv tool uninstall todo-app
```

---

## Data Location

Your tasks are stored in:
- **Linux/macOS**: `~/.todo-app/todo.db`
- **Windows**: `%USERPROFILE%\.todo-app\todo.db`
