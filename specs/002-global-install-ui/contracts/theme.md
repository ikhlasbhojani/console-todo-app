# Theme Contract: Enhanced Terminal UI

**Feature Branch**: `002-global-install-ui`
**Date**: 2025-12-04
**Status**: Complete

## Overview

This document defines the contract for terminal styling using the `rich` library. All UI components must follow these styling rules for consistency.

---

## Console Interface

### Console Initialization

```python
from rich.console import Console
from rich.theme import Theme

# Custom theme definition
CUSTOM_THEME = Theme({
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
})

console = Console(theme=CUSTOM_THEME)
```

---

## Function Contracts

### print_banner

```python
def print_banner() -> None:
    """Display the styled welcome banner.

    Output:
        Displays a boxed banner with:
        - Double-line border in cyan
        - Application title centered
        - Help instruction below

    Example Output:
        ╔══════════════════════════════════════╗
        ║       TODO APP - Console Edition      ║
        ╚══════════════════════════════════════╝
        Type 'help' for available commands.
    """
```

### print_success

```python
def print_success(message: str) -> None:
    """Display a success message with green styling.

    Args:
        message: The success message to display.

    Output Format:
        [✓] {message}

    Example:
        >>> print_success("Task created with ID: 1")
        [✓] Task created with ID: 1  (in green)
    """
```

### print_error

```python
def print_error(message: str) -> None:
    """Display an error message with red styling.

    Args:
        message: The error message to display.

    Output Format:
        [✗] {message}

    Example:
        >>> print_error("Task not found")
        [✗] Task not found  (in red)
    """
```

### print_warning

```python
def print_warning(message: str) -> None:
    """Display a warning message with yellow styling.

    Args:
        message: The warning message to display.

    Output Format:
        [!] {message}

    Example:
        >>> print_warning("Task is already complete")
        [!] Task is already complete  (in yellow)
    """
```

### print_info

```python
def print_info(message: str) -> None:
    """Display an info message with cyan styling.

    Args:
        message: The informational message to display.

    Output Format:
        [i] {message}

    Example:
        >>> print_info("No tasks found")
        [i] No tasks found  (in cyan)
    """
```

### print_task_table

```python
def print_task_table(tasks: list[Task]) -> None:
    """Display tasks in a styled table.

    Args:
        tasks: List of Task objects to display.

    Output:
        - Styled table with borders
        - Colored header row (blue)
        - Status column with icons and colors:
          - Pending: ○ yellow
          - Done: ✓ green
        - Truncated titles if too long

    Example Output:
        ┌────┬─────────────────────┬────────────┬──────────────────┐
        │ ID │ Title               │ Status     │ Created          │
        ├────┼─────────────────────┼────────────┼──────────────────┤
        │  1 │ Buy groceries       │ ○ Pending  │ 2025-12-04 10:30 │
        │  2 │ Call dentist        │ ✓ Done     │ 2025-12-04 11:15 │
        └────┴─────────────────────┴────────────┴──────────────────┘

    Note:
        If tasks list is empty, displays info message instead.
    """
```

### get_prompt

```python
def get_prompt() -> str:
    """Get the styled command prompt string.

    Returns:
        Styled prompt string for rich.prompt.Prompt.

    Example:
        "todo ❯ "  (with colors applied)
    """
```

### format_status

```python
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
```

---

## Color Palette

| Name | Rich Style | Hex Equivalent | Usage |
|------|------------|----------------|-------|
| success | green bold | #00FF00 | Success messages |
| error | red bold | #FF0000 | Error messages |
| warning | yellow | #FFFF00 | Warnings |
| info | cyan | #00FFFF | Information |
| pending | yellow | #FFFF00 | Pending status |
| completed | green | #00FF00 | Done status |
| header | blue bold | #0000FF | Table headers |
| prompt | magenta bold | #FF00FF | Input prompt |
| title | cyan bold | #00FFFF | App title |
| dim | dim white | #888888 | Secondary text |

---

## Icons

| Icon | Unicode | Fallback | Usage |
|------|---------|----------|-------|
| ✓ | U+2713 | [x] | Success/Done |
| ✗ | U+2717 | [!] | Error |
| ○ | U+25CB | [ ] | Pending |
| ❯ | U+276F | > | Prompt |
| ! | U+0021 | ! | Warning |
| i | U+0069 | i | Info |

---

## Table Styling

### Column Definitions

| Column | Width | Alignment | Style |
|--------|-------|-----------|-------|
| ID | 4 | Right | Default |
| Title | 20 | Left | Default, truncate |
| Status | 10 | Center | Colored |
| Created | 16 | Left | Dim |

### Border Style

- Use `rich.box.ROUNDED` for tables
- Header separator enabled
- Row separators disabled

---

## Terminal Capability Detection

```python
def supports_color() -> bool:
    """Check if terminal supports color output.

    Returns:
        True if colors supported, False otherwise.

    Checks:
        - NO_COLOR environment variable
        - TERM=dumb
        - Console.is_terminal
    """

def supports_unicode() -> bool:
    """Check if terminal supports Unicode characters.

    Returns:
        True if Unicode supported, False for ASCII fallback.
    """
```

---

## Error Handling

- All styling functions must handle exceptions gracefully
- On styling failure, fallback to plain text output
- Never let styling errors crash the application

---

## Testing Requirements

1. Test each message type displays correct format
2. Test table rendering with various task counts
3. Test color fallback on NO_COLOR environment
4. Test Unicode fallback on ASCII-only terminals
5. Test banner displays correctly
