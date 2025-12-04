# Quickstart: Testing Terminal Hero Section

**Feature Branch**: `003-terminal-hero`
**Date**: 2025-12-05

---

## Prerequisites

1. Python 3.13+ (managed by uv)
2. Application installed or running from source

---

## Running the Application

### From Source (Development)

```bash
cd /path/to/console-todo-app
uv run python -m src.main
```

### Installed Globally

```bash
todo-app
```

---

## Visual Test Cases

### Test 1: Full Hero Section (Wide Terminal)

**Setup**: Ensure terminal is at least 80 characters wide

**Steps**:
1. Run some commands to fill terminal:
   ```bash
   ls -la
   echo "test"
   ```
2. Launch the app:
   ```bash
   todo-app
   ```

**Expected**:
- Terminal is cleared (previous commands gone)
- Large colorful ASCII art "TODO" heading at top
- Gradient colors from cyan to magenta
- Tagline "Manage your tasks with style" below
- Version and help hint visible
- Separator line before prompt

**Screenshot Check**:
- [ ] ASCII art spans 5 lines
- [ ] Colors gradient from top to bottom
- [ ] Tagline is dimmer than heading
- [ ] Clean, professional appearance

---

### Test 2: Compact Mode (Narrow Terminal)

**Setup**: Resize terminal to ~50 characters wide

**Steps**:
1. Launch the app

**Expected**:
- Compact boxed "TODO APP" heading
- Still colorful but simpler design
- All elements visible and readable

**Screenshot Check**:
- [ ] Box fits within terminal
- [ ] No text wrapping or overflow
- [ ] Elements properly aligned

---

### Test 3: Very Narrow Terminal

**Setup**: Resize terminal to ~35 characters wide

**Steps**:
1. Launch the app

**Expected**:
- Simple text-only heading
- All text readable
- No visual artifacts

---

### Test 4: No Color Mode

**Steps**:
```bash
NO_COLOR=1 todo-app
```

**Expected**:
- Hero section displays without colors
- ASCII art structure intact
- All text readable in default terminal color

---

### Test 5: Terminal Clear Verification

**Steps**:
1. Run several commands to fill terminal
2. Launch the app
3. Observe if previous content is visible

**Expected**:
- Terminal completely cleared
- Hero section starts at top row
- No scroll bar showing previous content

---

## Performance Check

**Test**: Hero section render time

**Steps**:
1. Launch the app
2. Observe startup delay

**Expected**:
- Hero section appears instantly (<100ms)
- No visible delay or flicker

---

## Edge Cases

### Unicode Fallback

If terminal doesn't support Unicode box characters:
- Should fall back to ASCII characters (+, -, |, #)
- Visual structure maintained

### Windows Terminal

Test on:
- [ ] Windows Terminal (Windows 10/11)
- [ ] PowerShell
- [ ] Command Prompt

### Linux/macOS

Test on:
- [ ] GNOME Terminal
- [ ] iTerm2
- [ ] Default macOS Terminal

---

## Quick Verification Checklist

Run these commands and verify each:

```bash
# 1. Normal launch (wide terminal)
todo-app
# ✓ Colorful ASCII art, terminal cleared

# 2. No color mode
NO_COLOR=1 todo-app
# ✓ No colors, structure intact

# 3. Help command still works
todo-app
> help
# ✓ Commands listed correctly

# 4. Exit command works
todo-app
> exit
# ✓ Goodbye message shown
```

---

## Troubleshooting

### Colors Not Showing

1. Check terminal color support: `echo $TERM`
2. Verify NO_COLOR not set: `echo $NO_COLOR`
3. Try different terminal emulator

### ASCII Art Garbled

1. Check terminal encoding: `locale`
2. Ensure UTF-8: `LANG=en_US.UTF-8`
3. Try ASCII fallback test

### Terminal Not Clearing

1. Check if running in IDE terminal (may not support clear)
2. Try standalone terminal
3. Check TERM variable is set correctly
