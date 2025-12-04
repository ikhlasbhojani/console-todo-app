"""Utility functions for input validation and formatting.

This module provides helper functions for validating user input
and formatting task data for display.
"""

from src.models import Task


def validate_task_id(id_str: str) -> tuple[bool, int | str]:
    """Validate and parse a task ID string.

    Args:
        id_str: User input string to validate as task ID.

    Returns:
        Tuple of (success, result) where:
        - (True, int) if valid integer
        - (False, error_message) if invalid

    Example:
        >>> validate_task_id("42")
        (True, 42)
        >>> validate_task_id("abc")
        (False, "[ERROR] Invalid task ID. Please enter a number.")
    """
    try:
        task_id = int(id_str)
        return (True, task_id)
    except ValueError:
        return (False, "[ERROR] Invalid task ID. Please enter a number.")


def validate_title(title: str) -> tuple[bool, str]:
    """Validate a task title.

    Strips whitespace and checks if the title is empty.

    Args:
        title: User input string to validate as title.

    Returns:
        Tuple of (success, result) where:
        - (True, stripped_title) if valid
        - (False, error_message) if empty after stripping

    Example:
        >>> validate_title("  Buy milk  ")
        (True, "Buy milk")
        >>> validate_title("   ")
        (False, "[ERROR] Title cannot be empty. Please enter a valid title.")
    """
    stripped_title = title.strip()
    if not stripped_title:
        return (False, "[ERROR] Title cannot be empty. Please enter a valid title.")
    return (True, stripped_title)


def format_task_table(tasks: list[Task]) -> str:
    """Format a list of tasks as a table string.

    Creates a formatted table with columns for ID, Title (truncated to 17 chars),
    Status, and Created At timestamp.

    Args:
        tasks: List of Task objects to format.

    Returns:
        Formatted table string with header, separator line, and task rows.
        Each row is on a separate line.

    Example:
        >>> tasks = [Task(id=1, title="Buy milk", ...)]
        >>> print(format_task_table(tasks))
        ID   Title              Status        Created At
        ---  -----------------  ------------  ----------------
        1    Buy milk           [ ] Pending   2025-12-04 10:15
    """
    # Define column widths
    id_width = 3
    title_width = 17
    status_width = 12
    date_width = 16

    # Build header
    header = (
        f"{'ID':<{id_width}}  "
        f"{'Title':<{title_width}}  "
        f"{'Status':<{status_width}}  "
        f"{'Created At':<{date_width}}"
    )

    # Build separator
    separator = f"{'-' * id_width}  {'-' * title_width}  {'-' * status_width}  {'-' * date_width}"

    # Build rows
    rows = []
    for task in tasks:
        # Truncate title if longer than column width
        title_display = task.title[:title_width]

        row = (
            f"{task.id:<{id_width}}  "
            f"{title_display:<{title_width}}  "
            f"{task.format_status():<{status_width}}  "
            f"{task.format_date():<{date_width}}"
        )
        rows.append(row)

    # Combine all parts
    table_lines = [header, separator] + rows
    return "\n".join(table_lines)
