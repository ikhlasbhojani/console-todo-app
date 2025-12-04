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
from rich.text import Text
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


def print_task_table(tasks: list, show_project: bool = True, project_manager=None) -> None:
    """Display tasks in a styled table.

    Args:
        tasks: List of Task objects to display.
        show_project: Whether to display the Project column (default: True).
        project_manager: ProjectManager instance for looking up project names (optional).

    Output:
        - Styled table with borders
        - Colored header row (blue)
        - Status column with icons and colors
        - Due Date column with formatted dates
        - Project column with project names (if show_project=True)
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
    table.add_column("Due Date", justify="left", width=10)
    if show_project:
        table.add_column("Project", justify="left", width=10)
    table.add_column("Created", justify="left", style="dim", width=16)

    # Add rows
    for task in tasks:
        status_str = format_status(task.status)
        created_str = task.created_at.strftime("%Y-%m-%d %H:%M")
        due_date_str = task.format_due_date() if task.due_date else ""

        # Lookup project name if project_id exists
        project_str = ""
        if task.project_id and project_manager:
            project = project_manager.get_project_by_id(task.project_id)
            if project:
                project_str = project.name

        if show_project:
            table.add_row(
                str(task.id), task.title, status_str, due_date_str, project_str, created_str
            )
        else:
            table.add_row(str(task.id), task.title, status_str, due_date_str, created_str)

    console.print(table)


def print_project_table(projects: list) -> None:
    """Display projects in a styled table.

    Args:
        projects: List of Project objects to display.

    Output:
        - Styled table with borders
        - Colored header row (blue)
        - Task count column
        - Created timestamp column

    Note:
        If projects list is empty, displays info message instead.
    """
    console = get_console()

    if not projects:
        print_info("No projects yet. Create one with 'project create'.")
        return

    table = Table(
        show_header=True,
        header_style="header",
        border_style="dim",
        row_styles=["", "dim"],
    )

    # Define columns
    table.add_column("ID", justify="right", style="dim", width=4)
    table.add_column("Name", justify="left", width=10)
    table.add_column("Description", justify="left", width=30, overflow="ellipsis")
    table.add_column("Tasks", justify="right", width=5)
    table.add_column("Created", justify="left", style="dim", width=16)

    # Add rows
    for project in projects:
        created_str = project.created_at.strftime("%Y-%m-%d %H:%M")
        description_str = project.description if project.description else ""
        table.add_row(
            str(project.id),
            project.name,
            description_str,
            str(project.task_count),
            created_str,
        )

    console.print(table)


def print_stats_table(stats) -> None:
    """Display task statistics in a styled table.

    Args:
        stats: TaskStats object with metrics.

    Output:
        - Styled table with borders
        - Colored header row (blue)
        - Metrics and values displayed
        - Contextual messages based on stats
    """
    console = get_console()

    # Check for zero tasks case
    if stats.total == 0:
        print_info("No tasks yet. Add one with 'add'.")
        return

    table = Table(
        show_header=True,
        header_style="header",
        border_style="dim",
        show_lines=False,
    )

    # Define columns
    table.add_column("Metric", justify="left", width=20)
    table.add_column("Value", justify="right", width=7)

    # Add rows
    table.add_row("Total Tasks", str(stats.total))
    table.add_row("Pending", str(stats.pending))
    table.add_row("Completed", str(stats.completed))
    table.add_row("", "")  # Separator row
    table.add_row("Due Today", str(stats.due_today))
    table.add_row("Overdue", str(stats.overdue))
    table.add_row("", "")  # Separator row
    table.add_row("Completion Rate", f"{stats.completion_rate:.1f}%")

    console.print(table)
    console.print()

    # Contextual messages
    if stats.pending == 0 and stats.total > 0:
        console.print("[success]🎉 Amazing! All tasks completed![/success]")
        console.print()
    elif stats.overdue > 0:
        msg = f"[warning]⚠ You have {stats.overdue} overdue tasks. "
        msg += "Run 'list --overdue' to see them.[/warning]"
        console.print(msg)
        console.print()


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


# =============================================================================
# HERO SECTION - Terminal Hero Section (Feature 003)
# =============================================================================

# Hero section constants
HERO_VERSION = "v1.0.0"
HERO_TAGLINE = "Manage your tasks with style"
HERO_HELP_HINT = "Type 'help' for commands"

# Gradient colors for ASCII art (top to bottom)
HERO_GRADIENT_COLORS = [
    "bright_cyan",
    "cyan",
    "blue",
    "magenta",
    "bright_magenta",
]

# Full ASCII art for wide terminals (60+ chars)
HERO_ART_FULL = """\
████████╗ ██████╗ ██████╗  ██████╗
╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗
   ██║   ██║   ██║██║  ██║██║   ██║
   ██║   ╚██████╔╝██████╔╝╚██████╔╝
   ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝\
"""

# Compact ASCII art for narrow terminals (40-59 chars)
HERO_ART_COMPACT = """\
╔════════════════════════╗
║   ■ T O D O  A P P ■   ║
╚════════════════════════╝\
"""

# Text-only fallback for very narrow terminals (<40 chars)
HERO_ART_TEXT = "=== TODO APP ==="

# ASCII fallback art (no Unicode)
HERO_ART_ASCII = """\
######## ####### ######  #######
   ##    ##   ## ##   ## ##   ##
   ##    ##   ## ##   ## ##   ##
   ##    ####### ######  #######
   ##    ####### ######  #######\
"""


def clear_terminal() -> None:
    """Clear the terminal screen.

    Uses Rich Console.clear() for cross-platform compatibility.
    This ensures the app starts at the top of a clean screen.
    """
    console = get_console()
    console.clear()


def _get_art_mode(terminal_width: int) -> str:
    """Determine which ASCII art mode to use based on terminal width.

    Args:
        terminal_width: Current terminal width in characters.

    Returns:
        "full" for wide terminals (60+),
        "compact" for medium terminals (40-59),
        "text" for narrow terminals (<40).
    """
    if terminal_width >= 60:
        return "full"
    elif terminal_width >= 40:
        return "compact"
    else:
        return "text"


def _get_ascii_art(mode: str) -> str:
    """Get ASCII art for the specified mode.

    Args:
        mode: "full", "compact", or "text"

    Returns:
        ASCII art string appropriate for the terminal.
    """
    if not supports_unicode():
        # Use ASCII fallback if Unicode not supported
        if mode == "full":
            return HERO_ART_ASCII
        elif mode == "compact":
            return (
                "+------------------------+\n|   * T O D O  A P P *   |\n+------------------------+"
            )
        else:
            return HERO_ART_TEXT

    if mode == "full":
        return HERO_ART_FULL
    elif mode == "compact":
        return HERO_ART_COMPACT
    else:
        return HERO_ART_TEXT


def _apply_gradient(text: str, colors: list[str]) -> Text:
    """Apply gradient colors to multi-line text.

    Args:
        text: Multi-line ASCII art string.
        colors: List of Rich color names to apply as gradient.

    Returns:
        Rich Text object with gradient colors applied line by line.
    """
    lines = text.split("\n")
    styled_text = Text()

    for i, line in enumerate(lines):
        # Cycle through colors for each line
        color = colors[i % len(colors)]
        styled_text.append(line, style=color)
        if i < len(lines) - 1:
            styled_text.append("\n")

    return styled_text


def _print_hero_heading(console: Console, mode: str) -> None:
    """Print the hero heading with gradient colors.

    Args:
        console: Rich Console instance.
        mode: Art mode ("full", "compact", or "text").
    """
    art = _get_ascii_art(mode)

    if supports_color():
        styled_art = _apply_gradient(art, HERO_GRADIENT_COLORS)
        console.print(styled_art)
    else:
        # No colors - print plain
        console.print(art)


def _print_hero_tagline(console: Console) -> None:
    """Print the hero tagline with dim styling.

    Args:
        console: Rich Console instance.
    """
    console.print()  # Blank line after heading
    console.print(f"[dim]       {HERO_TAGLINE}[/dim]")


def _print_hero_meta(console: Console) -> None:
    """Print version and help hint with dim cyan styling.

    Args:
        console: Rich Console instance.
    """
    console.print()  # Blank line after tagline
    separator = "·" if supports_unicode() else "-"
    console.print(f"[dim cyan]   {HERO_VERSION} {separator} {HERO_HELP_HINT}[/dim cyan]")


def _print_hero_separator(console: Console) -> None:
    """Print a separator line before the command prompt.

    Args:
        console: Rich Console instance.
    """
    console.print()  # Blank line after meta
    width = min(console.width, 40)
    separator_char = "─" if supports_unicode() else "-"
    console.print(f"[dim]{separator_char * width}[/dim]")
    console.print()  # Blank line before prompt


def print_hero() -> None:
    """Display the complete hero section.

    This function:
    1. Clears the terminal for a clean slate
    2. Detects terminal width and selects appropriate ASCII art
    3. Displays colorful gradient heading
    4. Shows tagline, version, and help hint
    5. Adds separator before command prompt

    The hero section transforms the app's startup experience
    with an impressive, modern visual design.
    """
    console = get_console()

    # Clear terminal for clean slate
    clear_terminal()

    # Detect terminal width and get appropriate art mode
    width = console.width
    mode = _get_art_mode(width)

    # Display hero components
    _print_hero_heading(console, mode)
    _print_hero_tagline(console)
    _print_hero_meta(console)
    _print_hero_separator(console)
