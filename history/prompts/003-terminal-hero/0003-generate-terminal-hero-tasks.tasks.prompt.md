---
id: 0003
title: Generate Terminal Hero Tasks
stage: tasks
date: 2025-12-05
surface: agent
model: claude-opus-4-5-20251101
feature: 003-terminal-hero
branch: 003-terminal-hero
user: ikhlasbhojani
command: /sp.tasks
labels: ["tasks", "terminal-ui", "hero-section", "implementation-tasks"]
links:
  spec: specs/003-terminal-hero/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/003-terminal-hero/tasks.md
tests:
  - null
---

## Prompt

$ARGUMENTS

## Response snapshot

Generated comprehensive tasks.md for Terminal Hero Section feature (003-terminal-hero) with:

**Task Summary:**
- **Total Tasks**: 32 tasks
- Phase 1 (Setup): 2 tasks - Review existing code
- Phase 2 (Foundational): 6 tasks - Core helper functions (clear_terminal, ASCII art constants, gradient colors, helper functions)
- Phase 3 (US1 - Heading): 5 tasks - Big colorful ASCII art heading with gradient
- Phase 4 (US2 - Tagline): 4 tasks - Subtitle text with dim styling
- Phase 5 (US3 - Meta): 5 tasks - Version and help hint display
- Phase 6 (Integration): 4 tasks - Wire print_hero() to main.py
- Phase 7 (Polish): 6 tasks - Manual visual testing per quickstart.md

**Key Features:**
- Tasks organized by user story for independent implementation
- Parallel opportunities identified for constants and testing
- Sequential story dependency (US1 → US2 → US3)
- MVP scope: Phase 1-3 delivers colorful heading (visual impact)
- All tasks have specific file paths (src/theme.py, src/main.py)

**Independent Test Criteria:**
- US1: Launch app, verify large colorful heading with gradient
- US2: Verify tagline appears below heading
- US3: Verify version and help hint visible

## Outcome

- Impact: Actionable task list for terminal hero section implementation
- Tests: Manual visual verification (6 test tasks in Phase 7)
- Files: specs/003-terminal-hero/tasks.md
- Next prompts: /sp.implement to execute tasks
- Reflection: Tasks properly decomposed by user story enabling incremental delivery

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): All format validations PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A
