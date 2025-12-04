# Tasks: TERMINAL HERO SECTION

**Input**: Design documents from `/specs/003-terminal-hero/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/hero.md, quickstart.md

**Tests**: Manual visual verification only (no automated tests for this visual feature)

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root
- Primary files: `src/theme.py`, `src/main.py`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: No project setup needed - extending existing codebase

- [x] T001 Verify rich library is installed and working in pyproject.toml
- [x] T002 [P] Review current print_banner() in src/theme.py for deprecation

**Checkpoint**: Existing code reviewed, ready to extend

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core functions that ALL user stories depend on

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [x] T003 Implement clear_terminal() function in src/theme.py using Console.clear()
- [x] T004 Implement supports_unicode() enhancement in src/theme.py for ASCII fallback detection
- [x] T005 [P] Define ASCII art constants (HERO_ART_FULL, HERO_ART_COMPACT, HERO_ART_TEXT) in src/theme.py
- [x] T006 [P] Define gradient colors list (HERO_GRADIENT_COLORS) in src/theme.py
- [x] T007 Implement _get_art_mode(terminal_width: int) helper function in src/theme.py
- [x] T008 Implement _apply_gradient(text: str, colors: list[str]) helper function in src/theme.py

**Checkpoint**: Foundation ready - user story implementation can now begin

---

## Phase 3: User Story 1 - Big Colorful Heading Display (Priority: P1) 🎯 MVP

**Goal**: Display large, eye-catching colorful ASCII art heading when app launches

**Independent Test**: Launch app and verify large colorful heading appears at top with gradient colors

### Implementation for User Story 1

- [x] T009 [US1] Implement _get_ascii_art(mode: str) function to return appropriate art in src/theme.py
- [x] T010 [US1] Implement print_hero_heading() function with gradient coloring in src/theme.py
- [x] T011 [US1] Integrate clear_terminal() call at start of print_hero() in src/theme.py
- [x] T012 [US1] Implement width detection using console.width in print_hero() in src/theme.py
- [x] T013 [US1] Add ASCII fallback for non-Unicode terminals in _get_ascii_art() in src/theme.py

**Checkpoint**: At this point, User Story 1 should be fully functional - colorful heading displays

---

## Phase 4: User Story 2 - Tagline/Subtitle Text (Priority: P2)

**Goal**: Display descriptive tagline below the main heading

**Independent Test**: Launch app and verify tagline "Manage your tasks with style" appears below heading

### Implementation for User Story 2

- [x] T014 [US2] Define HERO_TAGLINE constant in src/theme.py
- [x] T015 [US2] Implement print_hero_tagline() function with dim styling in src/theme.py
- [x] T016 [US2] Add proper spacing (1 blank line) after heading before tagline in print_hero() in src/theme.py
- [x] T017 [US2] Center-align tagline based on terminal width in print_hero_tagline() in src/theme.py

**Checkpoint**: At this point, User Stories 1 AND 2 should both work - heading + tagline display

---

## Phase 5: User Story 3 - Version and Quick Help Display (Priority: P3)

**Goal**: Show version number and help hint for polish

**Independent Test**: Launch app and verify version "v1.0.0" and help hint visible below tagline

### Implementation for User Story 3

- [x] T018 [US3] Define HERO_VERSION constant in src/theme.py
- [x] T019 [US3] Define HERO_HELP_HINT constant in src/theme.py
- [x] T020 [US3] Implement print_hero_meta() function with dim cyan styling in src/theme.py
- [x] T021 [US3] Add separator line function print_hero_separator() in src/theme.py
- [x] T022 [US3] Add proper spacing between meta info and separator in print_hero() in src/theme.py

**Checkpoint**: All user stories should now be independently functional - complete hero section

---

## Phase 6: Integration & Main.py Update

**Purpose**: Wire up hero section to main application

- [x] T023 Implement complete print_hero() function that orchestrates all components in src/theme.py
- [x] T024 Replace print_banner() call with print_hero() in main() function in src/main.py
- [x] T025 [P] Keep print_banner() for backward compatibility (deprecated) or remove in src/theme.py
- [x] T026 Verify hero section respects NO_COLOR environment variable in src/theme.py

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [x] T027 [P] Test hero section on wide terminal (80+ chars) per quickstart.md
- [x] T028 [P] Test hero section on narrow terminal (40-59 chars) per quickstart.md
- [x] T029 [P] Test hero section with NO_COLOR=1 per quickstart.md
- [x] T030 [P] Test terminal clearing behavior per quickstart.md
- [x] T031 Verify all existing tests still pass with ruff and pytest
- [x] T032 Run quickstart.md validation checklist

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-5)**: All depend on Foundational phase completion
  - User stories can proceed sequentially in priority order (P1 → P2 → P3)
- **Integration (Phase 6)**: Depends on all user stories complete
- **Polish (Phase 7)**: Depends on Integration complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after US1 complete (builds on print_hero structure)
- **User Story 3 (P3)**: Can start after US2 complete (adds to print_hero structure)

### Within Each User Story

- Helper functions before main functions
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- T001/T002 can run in parallel (Setup phase)
- T005/T006 can run in parallel (different constants)
- T027/T028/T029/T030 can run in parallel (independent manual tests)

---

## Parallel Example: Foundational Phase

```bash
# Launch parallel constant definitions:
Task: "Define ASCII art constants (HERO_ART_FULL, HERO_ART_COMPACT, HERO_ART_TEXT) in src/theme.py"
Task: "Define gradient colors list (HERO_GRADIENT_COLORS) in src/theme.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1 (Big Colorful Heading)
4. **STOP and VALIDATE**: Test heading displays with colors and gradient
5. Can stop here for minimal visual impact

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test colorful heading → Visual impact achieved (MVP!)
3. Add User Story 2 → Test tagline → More polished
4. Add User Story 3 → Test version/help → Complete hero section
5. Each story adds visual polish without breaking previous stories

### Single Developer Strategy

Follow sequential order:
1. Phase 1 (Setup)
2. Phase 2 (Foundational)
3. Phase 3 (US1 - Heading)
4. Phase 4 (US2 - Tagline)
5. Phase 5 (US3 - Meta)
6. Phase 6 (Integration)
7. Phase 7 (Polish)

---

## Task Summary

| Phase | Task Count | Description |
|-------|------------|-------------|
| Phase 1 (Setup) | 2 | Review existing code |
| Phase 2 (Foundational) | 6 | Core helper functions |
| Phase 3 (US1 - Heading) | 5 | Big colorful heading |
| Phase 4 (US2 - Tagline) | 4 | Subtitle text |
| Phase 5 (US3 - Meta) | 5 | Version and help |
| Phase 6 (Integration) | 4 | Wire to main.py |
| Phase 7 (Polish) | 6 | Testing and validation |
| **Total** | **32** | |

---

## Notes

- [P] tasks = different files or constants, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- This is a visual feature - testing is manual visual verification
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
