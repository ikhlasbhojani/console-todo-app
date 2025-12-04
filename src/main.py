"""Main CLI application for TODO APP.

This module provides the main command loop and command handlers
for the interactive console-based todo application with rich styling.
"""

from src import theme
from src.todo_manager import TodoManager
from src.utils import validate_task_id, validate_title


def handle_help() -> None:
    """Handle the 'help' command.

    Displays list of available commands with descriptions.
    """
    console = theme.get_console()
    console.print()
    console.print("[header]Available Commands:[/header]")
    console.print("  [info]add[/info]      - Add a new task")
    console.print("  [info]list[/info]     - Show all tasks")
    console.print("  [info]update[/info]   - Update an existing task (title/description)")
    console.print("  [info]complete[/info] - Mark a task as completed")
    console.print("  [info]delete[/info]   - Delete a task")
    console.print("  [info]help[/info]     - Show this help message")
    console.print("  [info]exit[/info]     - Quit the application")
    console.print()


def handle_add(manager: TodoManager) -> None:
    """Handle the 'add' command.

    Prompts user for title and description, validates input,
    creates task via manager, and displays result.
    """
    # Prompt for title with validation loop
    while True:
        title = input("Enter title: ")
        is_valid, result = validate_title(title)

        if is_valid:
            # result is the stripped title
            valid_title = result
            break
        else:
            # result is the error message
            theme.print_error(result)

    # Prompt for description (no validation, can be empty)
    description = input("Enter description: ")

    # Create task
    try:
        task = manager.add_task(valid_title, description)
        theme.get_console().print()
        theme.print_success(f"Task created with ID: {task.id}")
        theme.get_console().print()
    except ValueError as e:
        theme.get_console().print()
        theme.print_error(str(e))
        theme.get_console().print()


def handle_list(manager: TodoManager) -> None:
    """Handle the 'list' command.

    Retrieves all tasks and displays them in formatted table.
    """
    tasks = manager.list_tasks()

    theme.get_console().print()
    theme.print_task_table(tasks)
    theme.get_console().print()


def handle_update(manager: TodoManager) -> None:
    """Handle the 'update' command.

    Prompts for task ID and new values, validates input,
    updates task via manager, and displays result.
    """
    # Prompt for task ID
    task_id_str = input("Enter task ID to update: ")

    # Validate task ID
    is_valid, result = validate_task_id(task_id_str)

    if not is_valid:
        # result is the error message
        theme.get_console().print()
        theme.print_error(result)
        theme.get_console().print()
        return

    # result is the valid task_id integer
    task_id = result

    # Prompt for new title (blank = keep current)
    new_title_input = input("New title (leave blank to keep current): ")

    # Prompt for new description (blank = keep current)
    new_description_input = input("New description (leave blank to keep current): ")

    # Determine which fields to update (blank input means None = keep current)
    new_title = new_title_input if new_title_input else None
    new_description = new_description_input if new_description_input else None

    # Update the task
    try:
        success = manager.update_task(task_id, title=new_title, description=new_description)

        # Display result
        theme.get_console().print()
        if success:
            theme.print_success(f"Task {task_id} updated.")
        else:
            theme.print_error("Task not found")
        theme.get_console().print()

    except ValueError as e:
        # Handle validation errors (e.g., empty title)
        theme.get_console().print()
        theme.print_error(str(e))
        theme.get_console().print()


def handle_complete(manager: TodoManager) -> None:
    """Handle the 'complete' command.

    Prompts for task ID, validates input, completes task
    via manager, and displays result.
    """
    # Prompt for task ID
    task_id_str = input("Enter task ID to mark complete: ")

    # Validate task ID
    is_valid, result = validate_task_id(task_id_str)

    if not is_valid:
        # result is the error message
        theme.get_console().print()
        theme.print_error(result)
        theme.get_console().print()
        return

    # result is the valid task_id integer
    task_id = result

    # Complete the task
    success, message = manager.complete_task(task_id)

    # Display result with appropriate styling
    theme.get_console().print()
    if success:
        theme.print_success(f"Task {task_id} marked as completed.")
    elif "already" in message.lower():
        theme.print_warning(message)
    else:
        theme.print_error(message.replace("[ERROR] ", "").replace("[OK] ", ""))
    theme.get_console().print()


def handle_delete(manager: TodoManager) -> None:
    """Handle the 'delete' command.

    Prompts for task ID, confirms deletion, deletes task
    via manager if confirmed, and displays result.
    """
    # Prompt for task ID
    task_id_str = input("Enter task ID to delete: ")

    # Validate task ID
    is_valid, result = validate_task_id(task_id_str)

    if not is_valid:
        # result is the error message
        theme.get_console().print()
        theme.print_error(result)
        theme.get_console().print()
        return

    # result is the valid task_id integer
    task_id = result

    # Prompt for confirmation
    confirmation = input(f"Are you sure you want to delete task {task_id}? (y/n): ").strip().lower()

    # Only proceed if user confirms with 'y'
    if confirmation != "y":
        # User cancelled - return silently to prompt
        return

    # Delete the task
    success = manager.delete_task(task_id)

    # Display result
    theme.get_console().print()
    if success:
        theme.print_success(f"Task {task_id} deleted.")
    else:
        theme.print_error("Task not found")
    theme.get_console().print()


def main() -> None:
    """Main CLI loop for the TODO application.

    Displays startup banner, initializes TodoManager,
    and processes user commands in an infinite loop.
    """
    # Display startup banner
    theme.print_banner()

    # Initialize TodoManager (uses ~/.todo-app/todo.db by default)
    manager = TodoManager()

    # Get console for styled prompt
    console = theme.get_console()

    # Main command loop
    while True:
        try:
            # Display styled prompt and get user input
            prompt_str = theme.get_prompt()
            console.print(prompt_str, end="")
            command = input().strip().lower()

            # Skip empty commands
            if not command:
                continue

            # Command dispatcher (case-insensitive)
            if command == "add":
                handle_add(manager)
            elif command == "list":
                handle_list(manager)
            elif command == "update":
                handle_update(manager)
            elif command == "complete":
                handle_complete(manager)
            elif command == "delete":
                handle_delete(manager)
            elif command == "help":
                handle_help()
            elif command == "exit":
                theme.print_goodbye()
                break
            else:
                # Unknown command
                theme.get_console().print()
                theme.print_error(f"Unknown command: '{command}'. Type 'help' to see commands.")
                theme.get_console().print()

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            theme.print_goodbye()
            break
        except EOFError:
            # Handle Ctrl+D gracefully
            theme.print_goodbye()
            break


if __name__ == "__main__":
    main()
