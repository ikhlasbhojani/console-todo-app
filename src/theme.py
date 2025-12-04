"""Theme module for enhanced terminal UI with rich library.

This module provides styled output functions, color definitions,
and terminal capability detection for the TODO application.
"""

import os
from dataclasses import dataclass

# Type alias for Task to avoid circular import
from typing import TYPE_CHECKING

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.theme import Theme

if TYPE_CHECKING:
    pass


@dataclass
class ThemeColors:
    """Color definitions for the theme."""

    success: str = "green bold"
    error: str = "red bold"
    warning: str = "yellow"
    info: str = "cyan"
    pending: str = "yellow"
    completed: str = "green"
    header: str = "blue bold"
    prompt: str = "magenta bold"
    title: str = "cyan bold"
    dim: str = "dim white"


# Custom theme definition
CUSTOM_THEME = Theme(
    {
        "success": "green bold",
        "error": "red bold",
        "warning": "yellow",
        "info": "cyan",
        "pending": "yellow",
        "completed": "green",
        "header": "blue bold",
        "prompt": "magenta bold",
        "title": "cyan bold",
        "dim": "dim white",
    }
)

# Module-level console instance
_console: Console | None = None


def supports_color() -> bool:
    """Check if terminal supports color output.

    Returns:
        True if colors supported, False otherwise.

    Checks:
        - NO_COLOR environment variable
        - TERM=dumb
        - Console.is_terminal
    """
    # Check NO_COLOR environment variable (standard convention)
    if os.environ.get("NO_COLOR"):
        return False

    # Check TERM=dumb
    if os.environ.get("TERM") == "dumb":
        return False

    return True


def supports_unicode() -> bool:
    """Check if terminal supports Unicode characters.

    Returns:
        True if Unicode supported, False for ASCII fallback.
    """
    # Check LANG/LC_ALL for UTF-8
    lang = os.environ.get("LANG", "") + os.environ.get("LC_ALL", "")
    if "utf" in lang.lower() or "UTF" in lang:
        return True

    # Default to True for most modern terminals
    # Rich handles fallback automatically
    return True


def get_console() -> Console:
    """Get or create the configured rich Console instance.

    Returns:
        Configured Console with custom theme.
    """
    global _console
    if _console is None:
        force_terminal = None
        no_color = not supports_color()
        _console = Console(theme=CUSTOM_THEME, force_terminal=force_terminal, no_color=no_color)
    return _console


def print_success(message: str) -> None:
    """Display a success message with green styling.

    Args:
        message: The success message to display.

    Output Format:
        [✓] {message}
    """
    console = get_console()
    icon = "✓" if supports_unicode() else "[x]"
    console.print(f"[success]{icon}[/success] {message}")


def print_error(message: str) -> None:
    """Display an error message with red styling.

    Args:
        message: The error message to display.

    Output Format:
        [✗] {message}
    """
    console = get_console()
    icon = "✗" if supports_unicode() else "[!]"
    console.print(f"[error]{icon}[/error] {message}")


def print_warning(message: str) -> None:
    """Display a warning message with yellow styling.

    Args:
        message: The warning message to display.

    Output Format:
        [!] {message}
    """
    console = get_console()
    console.print(f"[warning]![/warning] {message}")


def print_info(message: str) -> None:
    """Display an info message with cyan styling.

    Args:
        message: The informational message to display.

    Output Format:
        [i] {message}
    """
    console = get_console()
    console.print(f"[info]i[/info] {message}")


def format_status(status: str) -> str:
    """Format task status with icon and color markup.

    Args:
        status: Task status ("pending" or "done").

    Returns:
        Rich markup string with icon and color.

    Examples:
        >>> format_status("pending")
        "[yellow]○ Pending[/yellow]"
        >>> format_status("done")
        "[green]✓ Done[/green]"
    """
    if supports_unicode():
        if status == "done":
            return "[green]✓ Done[/green]"
        return "[yellow]○ Pending[/yellow]"
    else:
        if status == "done":
            return "[green][x] Done[/green]"
        return "[yellow][ ] Pending[/yellow]"


def print_banner() -> None:
    """Display the styled welcome banner.

    Output:
        Displays a boxed banner with:
        - Double-line border in cyan
        - Application title centered
        - Help instruction below
    """
    console = get_console()
    banner_text = "[title]TODO APP - Console Edition[/title]"
    panel = Panel(
        banner_text,
        border_style="cyan",
        padding=(0, 2),
    )
    console.print(panel)
    console.print("Type [info]'help'[/info] for available commands.\n")


def print_task_table(tasks: list) -> None:
    """Display tasks in a styled table.

    Args:
        tasks: List of Task objects to display.

    Output:
        - Styled table with borders
        - Colored header row (blue)
        - Status column with icons and colors
        - Truncated titles if too long

    Note:
        If tasks list is empty, displays info message instead.
    """
    console = get_console()

    if not tasks:
        print_info("No tasks found.")
        return

    table = Table(
        show_header=True,
        header_style="header",
        border_style="dim",
        row_styles=["", "dim"],
    )

    # Define columns
    table.add_column("ID", justify="right", style="dim", width=4)
    table.add_column("Title", justify="left", width=20, overflow="ellipsis")
    table.add_column("Status", justify="center", width=12)
    table.add_column("Created", justify="left", style="dim", width=16)

    # Add rows
    for task in tasks:
        status_str = format_status(task.status)
        created_str = task.created_at.strftime("%Y-%m-%d %H:%M")
        table.add_row(str(task.id), task.title, status_str, created_str)

    console.print(table)


def get_prompt() -> str:
    """Get the styled command prompt string.

    Returns:
        Styled prompt string for display.

    Example:
        "todo ❯ " (with colors applied)
    """
    if supports_unicode():
        return "[prompt]todo ❯[/prompt] "
    return "[prompt]todo >[/prompt] "


def print_goodbye() -> None:
    """Display a styled goodbye message."""
    console = get_console()
    if supports_unicode():
        console.print("\n[info]Goodbye![/info] 👋")
    else:
        console.print("\n[info]Goodbye![/info]")
