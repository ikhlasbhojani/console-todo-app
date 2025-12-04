"""Main CLI application for TODO APP - SQLITE.

This module provides the main command loop and command handlers
for the interactive console-based todo application.
"""

from src.todo_manager import TodoManager
from src.utils import format_task_table, validate_task_id, validate_title


def print_banner() -> None:
    """Display the startup banner."""
    print("====================================")
    print("      TODO APP - SQLITE (PHASE 1)")
    print("====================================")
    print("Type 'help' to see available commands.")
    print()


def handle_help() -> None:
    """Handle the 'help' command.

    Displays list of available commands with descriptions.
    """
    print()
    print("Available commands:")
    print("  add      - Add a new task")
    print("  list     - Show all tasks")
    print("  update   - Update an existing task (title/description)")
    print("  complete - Mark a task as completed")
    print("  delete   - Delete a task")
    print("  exit     - Quit the application")
    print()


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
            print(result)

    # Prompt for description (no validation, can be empty)
    description = input("Enter description: ")

    # Create task
    try:
        task = manager.add_task(valid_title, description)
        print()
        print(f"[OK] Task created with ID: {task.id}")
        print()
    except ValueError as e:
        print()
        print(f"[ERROR] {e}")
        print()


def handle_list(manager: TodoManager) -> None:
    """Handle the 'list' command.

    Retrieves all tasks and displays them in formatted table.
    """
    tasks = manager.list_tasks()

    print()
    if not tasks:
        print("No tasks found.")
    else:
        table = format_task_table(tasks)
        print(table)
    print()


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
        print()
        print(result)
        print()
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
        print()
        if success:
            print(f"[OK] Task {task_id} updated.")
        else:
            print("[ERROR] Task not found")
        print()

    except ValueError as e:
        # Handle validation errors (e.g., empty title)
        print()
        print(f"[ERROR] {e}")
        print()


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
        print()
        print(result)
        print()
        return

    # result is the valid task_id integer
    task_id = result

    # Complete the task
    success, message = manager.complete_task(task_id)

    # Display result
    print()
    print(message)
    print()


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
        print()
        print(result)
        print()
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
    print()
    if success:
        print(f"[OK] Task {task_id} deleted.")
    else:
        print("[ERROR] Task not found")
    print()


def main() -> None:
    """Main CLI loop for the TODO application.

    Displays startup banner, initializes TodoManager,
    and processes user commands in an infinite loop.
    """
    # Display startup banner
    print_banner()

    # Initialize TodoManager
    manager = TodoManager()

    # Main command loop
    while True:
        try:
            # Display prompt and get user input
            command = input("> ").strip().lower()

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
                print()
                print("Goodbye!")
                break
            else:
                # Unknown command
                print()
                print(f"[ERROR] Unknown command: '{command}'. Type 'help' to see commands.")
                print()

        except KeyboardInterrupt:
            # Handle Ctrl+C gracefully
            print()
            print("Goodbye!")
            break
        except EOFError:
            # Handle Ctrl+D gracefully
            print()
            print("Goodbye!")
            break


if __name__ == "__main__":
    main()
