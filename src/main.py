"""Main CLI application for TODO APP.

This module provides the main command loop and command handlers
for the interactive console-based todo application with rich styling.
"""

from datetime import date

from src import theme
from src.project_manager import ProjectManager
from src.todo_manager import TodoManager
from src.utils import validate_due_date, validate_project_name, validate_task_id, validate_title


def handle_help() -> None:
    """Handle the 'help' command.

    Displays list of available commands with descriptions.
    """
    console = theme.get_console()
    console.print()
    console.print("[header]Available Commands:[/header]")
    console.print()
    console.print("[dim cyan]Task Management:[/dim cyan]")
    console.print("  [info]add[/info]              - Add a new task (with due date and project)")
    console.print("  [info]list[/info]             - Show all tasks")
    console.print("  [info]list --today[/info]     - Show tasks due today")
    console.print("  [info]list --overdue[/info]   - Show overdue tasks")
    console.print("  [info]list --upcoming[/info]  - Show tasks due in next 7 days")
    console.print("  [info]list --project <name>[/info] - Show tasks in a project")
    console.print("  [info]update[/info]           - Update an existing task (title/description)")
    console.print("  [info]complete[/info]         - Mark a task as completed")
    console.print("  [info]delete[/info]           - Delete a task")
    console.print()
    console.print("[dim cyan]Project Management:[/dim cyan]")
    console.print("  [info]project create[/info]   - Create a new project")
    console.print("  [info]project list[/info]     - Show all projects")
    console.print("  [info]project view <name>[/info] - View project details and tasks")
    console.print("  [info]project delete[/info]   - Delete a project")
    console.print()
    console.print("[dim cyan]Statistics & Info:[/dim cyan]")
    console.print("  [info]stats[/info]            - Show task statistics dashboard")
    console.print("  [info]help[/info]             - Show this help message")
    console.print("  [info]exit[/info]             - Quit the application")
    console.print()


def handle_add(manager: TodoManager, project_manager: ProjectManager) -> None:
    """Handle the 'add' command.

    Prompts user for title, description, due date, and project,
    validates input, creates task via manager, and displays result.
    """
    console = theme.get_console()
    console.print("\n[header]📝 Add New Task[/header]\n")

    # Prompt for title with validation loop
    while True:
        title = input("Title: ")
        is_valid, result = validate_title(title)

        if is_valid:
            # result is the stripped title
            valid_title = result
            break
        else:
            # result is the error message
            theme.print_error(result)

    # Prompt for description (no validation, can be empty)
    description = input("Description (optional): ")

    # Prompt for due date with validation
    due_date_obj: date | None = None
    while True:
        due_date_input = input("Due date (YYYY-MM-DD, optional): ")
        is_valid, result = validate_due_date(due_date_input)

        if is_valid:
            # result is either a date object or None
            due_date_obj = result
            break
        else:
            # result is the error message
            theme.print_error(result)

    # Prompt for project with validation
    project_id: int | None = None
    project_name_display = ""
    while True:
        project_input = input("Project (optional): ").strip()

        if not project_input:
            # No project specified
            break

        # Validate project name format
        is_valid, result = validate_project_name(project_input)
        if not is_valid:
            theme.print_error(result)
            continue

        # Check if project exists
        project = project_manager.get_project(result)
        if project is None:
            theme.print_error(
                f"Project '{result}' not found. Create it first with 'project create'."
            )
            # Allow user to continue without project
            retry = input("Try another project? (y/n): ").strip().lower()
            if retry != "y":
                break
            continue

        # Project found
        project_id = project.id
        project_name_display = project.name
        break

    # Create task
    try:
        task = manager.add_task(
            valid_title, description, due_date=due_date_obj, project_id=project_id
        )
        console.print()
        if project_id:
            theme.print_success(
                f"Task added successfully! (ID: {task.id}, Project: {project_name_display})"
            )
        else:
            theme.print_success(f"Task added successfully! (ID: {task.id})")
        console.print()
    except ValueError as e:
        console.print()
        theme.print_error(str(e))
        console.print()


def handle_list(manager: TodoManager, project_manager: ProjectManager, args: list[str]) -> None:
    """Handle the 'list' command with optional filters.

    Supports filters: --today, --overdue, --upcoming, --project <name>

    Args:
        manager: TodoManager instance
        project_manager: ProjectManager instance for project lookups
        args: Command arguments (e.g., ['--today'] or ['--project', 'work'])
    """
    console = theme.get_console()
    console.print()

    # Parse filter arguments
    if len(args) == 0:
        # No filter - show all tasks
        tasks = manager.list_tasks()
        theme.print_task_table(tasks, show_project=True, project_manager=project_manager)
    elif args[0] == "--today":
        # Show tasks due today
        today_str = date.today().isoformat()
        console.print(f"[header]Tasks due today ({today_str}):[/header]\n")
        tasks = manager.list_tasks_today()
        if not tasks:
            theme.print_info("No tasks due today.")
        else:
            theme.print_task_table(tasks, show_project=True, project_manager=project_manager)
    elif args[0] == "--overdue":
        # Show overdue tasks
        console.print("[header]Overdue tasks:[/header]\n")
        tasks = manager.list_tasks_overdue()
        if not tasks:
            theme.print_info("No overdue tasks. Great job!")
        else:
            theme.print_task_table(tasks, show_project=True, project_manager=project_manager)
    elif args[0] == "--upcoming":
        # Show upcoming tasks
        console.print("[header]Upcoming tasks (next 7 days):[/header]\n")
        tasks = manager.list_tasks_upcoming()
        if not tasks:
            theme.print_info("No upcoming tasks in the next 7 days.")
        else:
            theme.print_task_table(tasks, show_project=True, project_manager=project_manager)
    elif args[0] == "--project":
        # Show tasks in a specific project
        if len(args) < 2:
            theme.print_error("Project name required. Usage: list --project <name>")
        else:
            project_name = args[1]
            project = project_manager.get_project(project_name)
            if project is None:
                theme.print_error(f"Project '{project_name}' not found.")
            else:
                console.print(f"[header]Tasks in project '{project.name}':[/header]\n")
                tasks = manager.list_tasks_by_project(project.id)
                if not tasks:
                    theme.print_info("No tasks in this project.")
                else:
                    theme.print_task_table(
                        tasks, show_project=False, project_manager=project_manager
                    )
    else:
        # Unknown filter
        theme.print_error(f"Unknown option: {args[0]}. See 'help' for usage.")

    console.print()


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


def handle_project_create(project_manager: ProjectManager) -> None:
    """Handle the 'project create' command.

    Prompts for project name and description, validates input,
    creates project via manager, and displays result.
    """
    console = theme.get_console()
    console.print("\n[header]📁 Create New Project[/header]\n")

    # Prompt for project name with validation
    while True:
        name = input("Project name: ")
        is_valid, result = validate_project_name(name)

        if is_valid:
            valid_name = result
            break
        else:
            theme.print_error(result)

    # Prompt for description (optional)
    description = input("Description (optional): ")

    # Create project
    try:
        project = project_manager.create_project(valid_name, description)
        console.print()
        theme.print_success(f"Project '{project.name}' created successfully.")
        console.print()
    except ValueError as e:
        console.print()
        theme.print_error(str(e))
        console.print()


def handle_project_list(project_manager: ProjectManager) -> None:
    """Handle the 'project list' command.

    Retrieves all projects and displays them in formatted table.
    """
    console = theme.get_console()
    console.print("\n[header]📁 Projects:[/header]\n")

    projects = project_manager.list_projects()
    theme.print_project_table(projects)
    console.print()


def handle_project_view(
    project_manager: ProjectManager, manager: TodoManager, args: list[str]
) -> None:
    """Handle the 'project view <name>' command.

    Shows project details and all tasks in the project.

    Args:
        project_manager: ProjectManager instance
        manager: TodoManager instance
        args: Command arguments (project name)
    """
    console = theme.get_console()

    if len(args) == 0:
        console.print()
        theme.print_error("Project name required. Usage: project view <name>")
        console.print()
        return

    project_name = args[0]
    project = project_manager.get_project(project_name)

    if project is None:
        console.print()
        theme.print_error(f"Project '{project_name}' not found.")
        console.print()
        return

    # Display project header
    console.print()
    console.print(f"[header]📁 Project: {project.name}[/header]")
    if project.description:
        console.print(f"   [dim]{project.description}[/dim]")
    console.print()

    # Display tasks in project
    tasks = manager.list_tasks_by_project(project.id)
    if not tasks:
        theme.print_info("No tasks in this project.")
    else:
        theme.print_task_table(tasks, show_project=False, project_manager=project_manager)
        console.print()
        # Display summary
        pending = sum(1 for t in tasks if t.status == "pending")
        completed = sum(1 for t in tasks if t.status == "done")
        console.print(f"Total: {len(tasks)} tasks ({pending} pending, {completed} completed)")

    console.print()


def handle_project_delete(project_manager: ProjectManager) -> None:
    """Handle the 'project delete' command.

    Prompts for project name, confirms deletion with cascade option,
    deletes project via manager if confirmed, and displays result.
    """
    console = theme.get_console()
    console.print("\n[header]📁 Delete Project[/header]\n")

    # Prompt for project name
    project_name = input("Project name: ")

    # Check if project exists
    project = project_manager.get_project(project_name)
    if project is None:
        console.print()
        theme.print_error(f"Project '{project_name}' not found.")
        console.print()
        return

    # Check if project has tasks
    cascade = False
    if project.task_count > 0:
        console.print()
        confirmation = (
            input(
                f"[warning]⚠[/warning] Project '{project.name}' has {project.task_count} tasks. "
                f"Delete project and all its tasks? (y/n): "
            )
            .strip()
            .lower()
        )

        if confirmation != "y":
            console.print()
            theme.print_info("Deletion cancelled.")
            console.print()
            return

        cascade = True

    # Delete the project
    success, deleted_count = project_manager.delete_project(project.name, cascade=cascade)

    console.print()
    if success:
        if deleted_count > 0:
            theme.print_success(f"Project '{project.name}' and {deleted_count} tasks deleted.")
        else:
            theme.print_success(f"Project '{project.name}' deleted.")
    else:
        theme.print_error(f"Project '{project_name}' not found.")
    console.print()


def handle_stats(manager: TodoManager) -> None:
    """Handle the 'stats' command.

    Retrieves task statistics and displays them in formatted table.
    """
    console = theme.get_console()
    console.print("\n[header]📊 Task Statistics[/header]\n")

    stats = manager.get_stats()
    theme.print_stats_table(stats)


def main() -> None:
    """Main CLI loop for the TODO application.

    Displays startup hero section, initializes TodoManager and ProjectManager,
    and processes user commands in an infinite loop.
    """
    # Display hero section (clears terminal and shows colorful heading)
    theme.print_hero()

    # Initialize managers (uses ~/.todo-app/todo.db by default)
    manager = TodoManager()
    project_manager = ProjectManager()

    # Get console for styled prompt
    console = theme.get_console()

    # Main command loop
    while True:
        try:
            # Display styled prompt and get user input
            prompt_str = theme.get_prompt()
            console.print(prompt_str, end="")
            user_input = input().strip()

            # Skip empty commands
            if not user_input:
                continue

            # Parse command and arguments
            parts = user_input.split()
            command = parts[0].lower()
            args = parts[1:]

            # Command dispatcher (case-insensitive)
            if command == "add":
                handle_add(manager, project_manager)
            elif command == "list":
                handle_list(manager, project_manager, args)
            elif command == "update":
                handle_update(manager)
            elif command == "complete":
                handle_complete(manager)
            elif command == "delete":
                handle_delete(manager)
            elif command == "project":
                # Parse project subcommands
                if len(args) == 0:
                    console.print()
                    theme.print_error(
                        "Project subcommand required. Usage: project <create|list|view|delete>"
                    )
                    console.print()
                elif args[0] == "create":
                    handle_project_create(project_manager)
                elif args[0] == "list":
                    handle_project_list(project_manager)
                elif args[0] == "view":
                    handle_project_view(project_manager, manager, args[1:])
                elif args[0] == "delete":
                    handle_project_delete(project_manager)
                else:
                    console.print()
                    msg = f"Unknown project subcommand: '{args[0]}'. "
                    msg += "Use create, list, view, or delete."
                    theme.print_error(msg)
                    console.print()
            elif command == "stats":
                handle_stats(manager)
            elif command == "help":
                handle_help()
            elif command == "exit":
                theme.print_goodbye()
                break
            else:
                # Unknown command
                console.print()
                theme.print_error(f"Unknown command: '{command}'. Type 'help' to see commands.")
                console.print()

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
