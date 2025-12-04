# Data Model: TERMINAL HERO SECTION

**Feature Branch**: `003-terminal-hero`
**Date**: 2025-12-05
**Spec**: [spec.md](spec.md)

---

## Overview

This feature is purely visual - no persistent data storage. This document defines the internal data structures used to render the hero section.

---

## Hero Section Components

### HeroConfig (Dataclass)

Configuration for hero section rendering.

```python
@dataclass
class HeroConfig:
    """Configuration for hero section display."""

    # Version info
    version: str = "1.0.0"

    # Tagline text
    tagline: str = "Manage your tasks with style"

    # Help hint text
    help_hint: str = "Type 'help' for commands"

    # Minimum width for full ASCII art
    full_art_min_width: int = 60

    # Minimum width for compact ASCII art
    compact_art_min_width: int = 40
```

---

## ASCII Art Definitions

### Full ASCII Art (60+ characters wide)

```
████████╗ ██████╗ ██████╗  ██████╗
╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗
   ██║   ██║   ██║██║  ██║██║   ██║
   ██║   ╚██████╔╝██████╔╝╚██████╔╝
   ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝
```

Width: ~40 characters (fits 60+ char terminals with padding)

### Compact ASCII Art (40-59 characters wide)

```
╔════════════════════════╗
║   ■ T O D O  A P P ■   ║
╚════════════════════════╝
```

Width: 26 characters

### Text-Only Fallback (<40 characters)

```
=== TODO APP ===
```

Width: 16 characters

---

## Color Scheme

### Gradient Colors (top to bottom)

| Line | Color Name | Rich Style |
|------|------------|------------|
| 1 | Bright Cyan | `bright_cyan` |
| 2 | Cyan | `cyan` |
| 3 | Blue | `blue` |
| 4 | Magenta | `magenta` |
| 5 | Bright Magenta | `bright_magenta` |

### Supporting Element Colors

| Element | Color | Rich Style |
|---------|-------|------------|
| Tagline | Dim White | `dim` |
| Version | Dim Cyan | `dim cyan` |
| Help Hint | Info Cyan | `cyan` |
| Separator | Dim | `dim` |

---

## Visual Hierarchy

```
┌─────────────────────────────────────────────────────────┐
│                                                         │
│   [GRADIENT COLORED ASCII ART - "TODO APP"]             │  ← Primary (largest, colorful)
│                                                         │
│   "Manage your tasks with style"                        │  ← Secondary (tagline, dim)
│                                                         │
│   v1.0.0 · Type 'help' for commands                     │  ← Tertiary (meta info, dimmer)
│                                                         │
│   ─────────────────────────────────────────────────     │  ← Separator
│                                                         │
└─────────────────────────────────────────────────────────┘
```

---

## Width Detection Logic

```python
def get_art_mode(terminal_width: int) -> str:
    """Determine which ASCII art mode to use.

    Args:
        terminal_width: Current terminal width in characters.

    Returns:
        "full" | "compact" | "text"
    """
    if terminal_width >= 60:
        return "full"
    elif terminal_width >= 40:
        return "compact"
    else:
        return "text"
```

---

## Function Signatures

### theme.py additions

```python
def clear_terminal() -> None:
    """Clear the terminal screen using Rich Console.

    Uses Console.clear() for cross-platform compatibility.
    """
    pass

def print_hero() -> None:
    """Display the hero section with ASCII art heading.

    Steps:
    1. Clear terminal
    2. Detect terminal width
    3. Select appropriate ASCII art
    4. Apply gradient colors
    5. Print tagline
    6. Print version and help hint
    7. Print separator
    """
    pass

def _get_ascii_art(mode: str) -> str:
    """Get ASCII art for the specified mode.

    Args:
        mode: "full", "compact", or "text"

    Returns:
        ASCII art string
    """
    pass

def _apply_gradient(text: str, colors: list[str]) -> Text:
    """Apply gradient colors to multi-line text.

    Args:
        text: Multi-line ASCII art string
        colors: List of Rich color names

    Returns:
        Rich Text object with gradient applied
    """
    pass
```

### main.py changes

```python
def main() -> None:
    """Main CLI loop."""
    # OLD: theme.print_banner()
    # NEW: theme.print_hero()
    theme.print_hero()

    # ... rest unchanged
```

---

## Compatibility Matrix

| Terminal Type | Unicode | Colors | Art Mode |
|---------------|---------|--------|----------|
| Modern (80+ cols) | Yes | Yes | Full + Gradient |
| Modern (60-79) | Yes | Yes | Full + Gradient |
| Narrow (40-59) | Yes | Yes | Compact + Colors |
| Very Narrow (<40) | Yes | Yes | Text + Colors |
| NO_COLOR set | Yes | No | Art without colors |
| ASCII-only | No | Yes | ASCII fallback + Colors |
| Minimal | No | No | Plain ASCII text |

---

## File Changes Summary

| File | Change Type | Description |
|------|-------------|-------------|
| `src/theme.py` | MODIFY | Add `clear_terminal()`, `print_hero()`, helper functions |
| `src/main.py` | MODIFY | Replace `print_banner()` with `print_hero()` |
| `tests/test_cli.py` | MODIFY | Update banner tests to hero section tests |
