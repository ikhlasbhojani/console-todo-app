# Research: TERMINAL HERO SECTION

**Feature Branch**: `003-terminal-hero`
**Date**: 2025-12-05
**Spec**: [spec.md](spec.md)

---

## Research Questions

### RQ-001: How to create large ASCII art text in Python?

**Finding**: Multiple approaches available:

1. **Hardcoded ASCII art** - Define custom text art as string constants
   - Pros: No dependencies, full control over design, fast
   - Cons: Manual work to create, limited to predefined text
   - Example: Box-drawing characters (╔═╗ ║ ╚═╝)

2. **pyfiglet library** - Python port of figlet
   - Pros: Many fonts, dynamic text generation
   - Cons: Extra dependency, some fonts don't look good at all sizes
   - NOT recommended: Adds unnecessary dependency

3. **Rich library built-in** - Rich has Text and Panel for styling
   - Pros: Already installed, consistent with existing code
   - Cons: No built-in ASCII art generator
   - RECOMMENDED: Use rich for colors + custom ASCII art for heading

**Decision**: Use hardcoded ASCII art with Rich for coloring. No new dependencies needed.

### RQ-002: How to clear terminal screen in Python (cross-platform)?

**Finding**: Multiple approaches for cross-platform terminal clearing:

1. **os.system with clear/cls**:
   ```python
   import os
   os.system('cls' if os.name == 'nt' else 'clear')
   ```
   - Pros: Simple, reliable
   - Cons: Spawns subprocess, may show briefly

2. **ANSI escape sequences**:
   ```python
   print("\033[2J\033[H", end="")
   ```
   - `\033[2J` - Clear entire screen
   - `\033[H` - Move cursor to home position (0,0)
   - Pros: Fast, no subprocess
   - Cons: May not work on all Windows terminals

3. **Rich Console.clear()**:
   ```python
   console = Console()
   console.clear()
   ```
   - Pros: Already using Rich, handles cross-platform
   - Cons: None for our use case
   - RECOMMENDED: Use rich's built-in clear method

**Decision**: Use `Console.clear()` from Rich library - already installed and handles cross-platform.

### RQ-003: How to create gradient/multi-color text with Rich?

**Finding**: Rich supports multiple color styling approaches:

1. **Named colors**: `[cyan]text[/cyan]`, `[magenta]text[/magenta]`
2. **RGB colors**: `[rgb(255,128,0)]text[/rgb(255,128,0)]`
3. **Multiple styles per line**: Apply different colors to different parts
4. **Gradient effect**: Apply different colors to each character/line

**Example gradient approach**:
```python
from rich.text import Text
from rich.console import Console

# Create gradient by coloring each line differently
colors = ["bright_cyan", "cyan", "blue", "magenta", "bright_magenta"]
lines = ascii_art.split('\n')
text = Text()
for i, line in enumerate(lines):
    color = colors[i % len(colors)]
    text.append(line + "\n", style=color)
```

**Decision**: Use color gradient across lines of ASCII art for striking visual effect.

### RQ-004: What ASCII art style for "TODO APP" heading?

**Finding**: Evaluated several styles:

1. **Simple box-drawing**:
   ```
   ╔════════════════╗
   ║   TODO APP     ║
   ╚════════════════╝
   ```
   - Too similar to current banner

2. **Block letters using box characters**:
   ```
   ████████╗ ██████╗ ██████╗  ██████╗
   ╚══██╔══╝██╔═══██╗██╔══██╗██╔═══██╗
      ██║   ██║   ██║██║  ██║██║   ██║
      ██║   ╚██████╔╝██████╔╝╚██████╔╝
      ╚═╝    ╚═════╝ ╚═════╝  ╚═════╝
   ```
   - Bold, impressive, uses Unicode block characters
   - Good balance of size and readability

3. **3D shadow effect**:
   ```
   ___________  ________  ________  ________
   |\___   ___\|\   __  \|\   ___ \|\   __  \
   \|___ \  \_|\ \  \|\  \ \  \_|\ \ \  \|\  \
        \ \  \ \ \  \\\  \ \  \ \\ \ \  \\\  \
         \ \  \ \ \  \\\  \ \  \_\\ \ \  \\\  \
          \ \__\ \ \_______\ \_______\ \_______\
           \|__|  \|_______|\|_______|\|_______|
   ```
   - Complex, may not render well in all terminals

**Decision**: Use block-style letters with Unicode box characters. Compact but impressive.

### RQ-005: Terminal width handling for ASCII art

**Finding**: Rich provides terminal size detection:

```python
from rich.console import Console
console = Console()
width = console.width  # Get terminal width
```

**Strategies**:
1. **Full art for wide terminals** (80+ chars): Show complete ASCII art
2. **Compact art for narrow terminals** (40-79 chars): Simplified version
3. **Text-only for very narrow** (<40 chars): Plain text with colors

**Decision**: Implement width detection with graceful degradation.

---

## Technical Decisions

| Decision | Choice | Rationale |
|----------|--------|-----------|
| ASCII Art Source | Hardcoded | No extra dependencies, full design control |
| Terminal Clearing | Rich Console.clear() | Already using Rich, cross-platform |
| Coloring | Rich gradient per line | Visually striking, uses existing library |
| Art Style | Block letters with Unicode | Modern, impressive, compact |
| Width Handling | Detect and degrade | Professional experience on all terminals |

---

## Implementation Approach

1. **Clear terminal first** using `console.clear()`
2. **Detect terminal width** using `console.width`
3. **Select appropriate ASCII art** based on width
4. **Apply gradient colors** to ASCII art lines
5. **Display tagline** below heading
6. **Show version and help hint** in dimmer style
7. **Add separator** before command prompt

---

## Dependencies

**Existing (no changes)**:
- `rich` - Already installed from Feature 002

**New**:
- None required

---

## Risks and Mitigations

| Risk | Probability | Mitigation |
|------|-------------|------------|
| Unicode not supported | Low | ASCII fallback characters |
| Terminal too narrow | Low | Graceful degradation to simple text |
| Colors disabled | Low | Respect NO_COLOR, plain text fallback |
| Performance | Very Low | Static strings, instant render |

---

## References

- [Rich Console Documentation](https://rich.readthedocs.io/en/stable/console.html)
- [Rich Text Styling](https://rich.readthedocs.io/en/stable/text.html)
- [ANSI Escape Codes](https://en.wikipedia.org/wiki/ANSI_escape_code)
- [NO_COLOR Standard](https://no-color.org/)
