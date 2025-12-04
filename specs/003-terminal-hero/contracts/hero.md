# Visual Contract: Hero Section

**Feature Branch**: `003-terminal-hero`
**Date**: 2025-12-05
**Spec**: [../spec.md](../spec.md)

---

## Contract Purpose

This document defines the exact visual output of the hero section for testing and verification purposes.

---

## Full Mode Output (60+ character terminals)

When terminal width is 60 or more characters, the hero section displays:

```
████████╗ ██████╗ ██████╗  ██████╗
╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗
   ██║   ██║   ██║██║  ██║██║   ██║
   ██║   ╚██████╔╝██████╔╝╚██████╔╝
   ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝

       Manage your tasks with style

   v1.0.0 · Type 'help' for commands

───────────────────────────────────────

```

### Color Application

| Lines | Content | Color |
|-------|---------|-------|
| 1 | `████████╗ ██████╗ ██████╗  ██████╗` | bright_cyan |
| 2 | `╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗` | cyan |
| 3 | `   ██║   ██║   ██║██║  ██║██║   ██║` | blue |
| 4 | `   ██║   ╚██████╔╝██████╔╝╚██████╔╝` | magenta |
| 5 | `   ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝` | bright_magenta |
| 7 | Tagline | dim |
| 9 | Version + Help | dim cyan |
| 11 | Separator | dim |

---

## Compact Mode Output (40-59 character terminals)

When terminal width is between 40 and 59 characters:

```
╔════════════════════════╗
║   ■ T O D O  A P P ■   ║
╚════════════════════════╝

  Manage your tasks with style

v1.0.0 · Type 'help' for commands

──────────────────────────────────

```

### Color Application

| Lines | Content | Color |
|-------|---------|-------|
| 1 | Top border | cyan |
| 2 | Title line | bright_cyan (text), cyan (border) |
| 3 | Bottom border | magenta |
| 5 | Tagline | dim |
| 7 | Version + Help | dim cyan |
| 9 | Separator | dim |

---

## Text Mode Output (<40 character terminals)

When terminal width is less than 40 characters:

```
=== TODO APP ===

Manage your tasks with style

v1.0.0 · Type 'help'

────────────────────────

```

### Color Application

| Lines | Content | Color |
|-------|---------|-------|
| 1 | Title | bright_cyan |
| 3 | Tagline | dim |
| 5 | Version + Help | dim cyan |
| 7 | Separator | dim |

---

## ASCII Fallback (No Unicode Support)

When Unicode is not supported:

```
######## ####### ######  #######
   ##    ##   ## ##   ## ##   ##
   ##    ##   ## ##   ## ##   ##
   ##    ####### ######  #######
   ##    ####### ######  #######

       Manage your tasks with style

   v1.0.0 - Type 'help' for commands

---------------------------------------

```

---

## No Color Mode (NO_COLOR=1)

When colors are disabled, all text renders in default terminal color:

```
████████╗ ██████╗ ██████╗  ██████╗
╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗
   ██║   ██║   ██║██║  ██║██║   ██║
   ██║   ╚██████╔╝██████╔╝╚██████╔╝
   ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝

       Manage your tasks with style

   v1.0.0 · Type 'help' for commands

───────────────────────────────────────

```

No ANSI color codes in output.

---

## Terminal Clear Behavior

**Before displaying hero section**:
1. Clear all previous terminal content
2. Move cursor to position (0, 0) - top-left
3. Display hero section starting from line 1

**Expected behavior**: User sees clean terminal with hero section at top. No previous commands visible.

---

## Spacing Rules

| Element | Spacing |
|---------|---------|
| After ASCII art | 1 blank line |
| After tagline | 1 blank line |
| After version/help | 1 blank line |
| After separator | 1 blank line (before prompt) |

**Total lines**: 8-15 lines depending on mode (within spec limit)

---

## Acceptance Verification

### Manual Test 1: Full Mode
```bash
# Ensure terminal is at least 60 chars wide
todo-app
```
**Expected**: Full ASCII art with gradient colors, terminal cleared

### Manual Test 2: Narrow Terminal
```bash
# Resize terminal to 45 characters
todo-app
```
**Expected**: Compact box art

### Manual Test 3: No Color
```bash
NO_COLOR=1 todo-app
```
**Expected**: Art displays without colors

### Manual Test 4: Terminal Clear
```bash
echo "Previous command output"
echo "More output"
todo-app
```
**Expected**: Previous commands not visible, hero at top
