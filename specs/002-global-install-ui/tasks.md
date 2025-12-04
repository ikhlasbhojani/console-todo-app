# Tasks: GLOBAL INSTALLATION & ENHANCED TERMINAL UI (PHASE 2)

**Input**: Design documents from `/specs/002-global-install-ui/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/theme.md, quickstart.md

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/`, `scripts/` at repository root
- Paths shown below follow the plan.md structure

---

## Phase 1: Setup (Dependencies & Configuration)

**Purpose**: Add rich dependency and configure entry point

- [x] T001 Add `rich>=13.0.0` dependency to pyproject.toml via `uv add rich`
- [x] T002 [P] Add `[project.scripts]` entry point `todo-app = "src.main:main"` to pyproject.toml
- [x] T003 [P] Run `uv sync` to install new dependencies
- [x] T004 Verify entry point works with `uv run todo-app` command

**Checkpoint**: Rich installed, entry point configured, `uv run todo-app` launches app

---

## Phase 2: Foundational (Theme Module)

**Purpose**: Create theme module with color definitions and styled output functions

- [x] T005 Create src/theme.py with ThemeColors dataclass and color constants
- [x] T006 [P] Implement `get_console()` function returning configured rich Console in src/theme.py
- [x] T007 [P] Implement `print_success(message)` function with green styling in src/theme.py
- [x] T008 [P] Implement `print_error(message)` function with red styling in src/theme.py
- [x] T009 [P] Implement `print_info(message)` function with cyan styling in src/theme.py
- [x] T010 [P] Implement `print_warning(message)` function with yellow styling in src/theme.py
- [x] T011 Implement `format_status(status)` returning styled status with icon in src/theme.py
- [x] T012 Implement `print_banner()` function with styled welcome box in src/theme.py
- [x] T013 Implement `print_task_table(tasks)` using rich Table in src/theme.py
- [x] T014 Implement `get_prompt()` returning styled prompt string in src/theme.py
- [x] T015 Add terminal capability detection with fallback in src/theme.py

**Checkpoint**: Theme module complete with all styled output functions

---

## Phase 3: User Story 1 - One-Command Global Installation (Priority: P1)

**Goal**: Users can install with single curl/PowerShell command and run `todo-app` globally

**Independent Test**: Run install command on fresh system, then type `todo-app` in any directory

### Implementation for User Story 1

- [x] T016 [US1] Update scripts/install.sh to check Python 3.13+ version
- [x] T017 [US1] Add uv auto-installation to scripts/install.sh using official installer
- [x] T018 [US1] Add `uv tool install` command with GitHub URL to scripts/install.sh
- [x] T019 [US1] Add PATH configuration instructions to scripts/install.sh
- [x] T020 [US1] Add styled success message with usage instructions to scripts/install.sh
- [x] T021 [P] [US1] Update scripts/install.ps1 to check Python 3.13+ version
- [x] T022 [P] [US1] Add uv auto-installation to scripts/install.ps1 using official installer
- [x] T023 [P] [US1] Add `uv tool install` command with GitHub URL to scripts/install.ps1
- [x] T024 [P] [US1] Add styled success message with usage instructions to scripts/install.ps1
- [x] T025 [US1] Update src/todo_manager.py to use ~/.todo-app/todo.db for global install
- [x] T026 [US1] Test installation: Run install script and verify `todo-app` command works

**Checkpoint**: US1 complete - Installation scripts work, `todo-app` runs globally

---

## Phase 4: User Story 2 - Enhanced Terminal UI with Colors (Priority: P2)

**Goal**: App displays with modern, colorful design using rich library

**Independent Test**: Run app and verify colored banner, prompts, success/error messages

### Implementation for User Story 2

- [x] T027 [US2] Update src/main.py to import theme module functions
- [x] T028 [US2] Replace print_banner() with theme.print_banner() in src/main.py
- [x] T029 [US2] Replace all print("[OK]...") with theme.print_success() in src/main.py
- [x] T030 [US2] Replace all print("[ERROR]...") with theme.print_error() in src/main.py
- [x] T031 [US2] Replace handle_list() table output with theme.print_task_table() in src/main.py
- [x] T032 [US2] Update command prompt to use theme.get_prompt() in src/main.py
- [x] T033 [US2] Add theme.print_info() for informational messages in src/main.py
- [x] T034 [US2] Add "Goodbye!" message with styling on exit in src/main.py
- [x] T035 [US2] Manual test: Verify all colored output displays correctly

**Checkpoint**: US2 complete - All output is styled with rich colors

---

## Phase 5: User Story 3 - Styled Task Status Indicators (Priority: P3)

**Goal**: Tasks show distinct visual indicators for pending vs completed status

**Independent Test**: Create tasks, complete some, verify status icons and colors in list

### Implementation for User Story 3

- [x] T036 [US3] Update format_status() to use ○ icon for pending in src/theme.py
- [x] T037 [US3] Update format_status() to use ✓ icon for completed in src/theme.py
- [x] T038 [US3] Add color styling (yellow pending, green done) to status in src/theme.py
- [x] T039 [US3] Update print_task_table() to use styled status column in src/theme.py
- [x] T040 [US3] Add Unicode fallback for terminals without Unicode support in src/theme.py
- [x] T041 [US3] Manual test: Create pending/completed tasks, verify visual distinction

**Checkpoint**: US3 complete - Status indicators are visually distinct

---

## Phase 6: User Story 4 - Updated README Documentation (Priority: P4)

**Goal**: README contains user-focused installation and usage instructions only

**Independent Test**: Follow README on fresh system, successfully install and use app

### Implementation for User Story 4

- [x] T042 [US4] Rewrite README.md with user-focused structure (not development docs)
- [x] T043 [P] [US4] Add one-command installation section with curl/PowerShell commands to README.md
- [x] T044 [P] [US4] Add Quick Start section showing `todo-app` command to README.md
- [x] T045 [P] [US4] Add Usage section with all commands and examples to README.md
- [x] T046 [P] [US4] Add Features section listing app capabilities to README.md
- [x] T047 [US4] Add example screenshots/output showing styled interface to README.md
- [x] T048 [US4] Add Troubleshooting section for common issues to README.md
- [x] T049 [US4] Review and verify all commands in README.md are accurate

**Checkpoint**: US4 complete - README is user-focused with accurate commands

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Final testing, linting, and verification

- [x] T050 [P] Run linter: `uv run ruff check src/ tests/`
- [x] T051 [P] Run formatter: `uv run ruff format src/ tests/`
- [x] T052 [P] Run full test suite: `uv run pytest -v`
- [x] T053 Manual test: Full user flow with styled output (add → list → complete → update → delete → exit)
- [x] T054 Manual test: Verify color fallback with NO_COLOR=1 environment variable
- [x] T055 Push changes to GitHub and verify install scripts fetch correctly
- [x] T056 Final test: Fresh install from GitHub URL, verify `todo-app` command works

**Checkpoint**: All tests pass, linting clean, installation works end-to-end

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup (rich must be installed)
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - US1 and US2 can run in parallel
  - US3 depends on US2 (builds on color system)
  - US4 depends on US1-US3 (documents final implementation)
- **Polish (Phase 7)**: Depends on all user stories being complete

### User Story Dependencies

| Story | Can Start After | Dependencies on Other Stories |
|-------|-----------------|-------------------------------|
| US1 (P1) | Phase 2 complete | None - standalone |
| US2 (P2) | Phase 2 complete | None - standalone |
| US3 (P3) | Phase 2 complete | US2 (uses color system) |
| US4 (P4) | US1-US3 complete | All stories (documents final implementation) |

### Parallel Opportunities

**Phase 1** (2 parallel tasks):
```
T002, T003 can run in parallel
```

**Phase 2** (5 parallel tasks):
```
T006, T007, T008, T009, T010 can run in parallel (all print functions)
```

**Phase 3** (4 parallel tasks):
```
T021, T022, T023, T024 can run in parallel (Windows script while Linux script)
```

**Phase 4** (No parallel - sequential updates to main.py)

**Phase 5** (No parallel - sequential updates to theme.py)

**Phase 6** (4 parallel tasks):
```
T043, T044, T045, T046 can run in parallel (README sections)
```

**Phase 7** (3 parallel tasks):
```
T050, T051, T052 can run in parallel
```

---

## Implementation Strategy

### MVP First (User Story 1 + 2)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (theme module)
3. Complete Phase 3: User Story 1 (Global Installation)
4. Complete Phase 4: User Story 2 (Colored UI)
5. **STOP and VALIDATE**: Test installation and UI independently
6. Demo-ready with colored interface and global command!

### Incremental Delivery

| Increment | Stories | Capability |
|-----------|---------|------------|
| MVP | US1 + US2 | Global install, colored output |
| +Status | US1-3 | Visual task status indicators |
| Full | US1-4 | Complete with user documentation |

### Recommended Execution Order

```
Phase 1 (Setup)              → 4 tasks
Phase 2 (Foundational)       → 11 tasks
Phase 3 (US1: Installation)  → 11 tasks  ← MVP PART 1
Phase 4 (US2: Colors)        → 9 tasks   ← MVP PART 2
Phase 5 (US3: Status Icons)  → 6 tasks
Phase 6 (US4: README)        → 8 tasks
Phase 7 (Polish)             → 7 tasks
                             ─────────────
                             TOTAL: 56 tasks
```

---

## Task Summary

| Phase | Tasks | Parallel | Story |
|-------|-------|----------|-------|
| Setup | 4 | 2 | - |
| Foundational | 11 | 5 | - |
| US1: Installation | 11 | 4 | P1 |
| US2: Colors | 9 | 0 | P2 |
| US3: Status Icons | 6 | 0 | P3 |
| US4: README | 8 | 4 | P4 |
| Polish | 7 | 3 | - |
| **TOTAL** | **56** | **18** | - |

### Agent Assignment

| Phase | Agent |
|-------|-------|
| Setup (T001-T004) | python-todo-cli-dev |
| Foundational (T005-T015) | python-todo-cli-dev |
| US1 Installation (T016-T026) | python-todo-cli-dev + todo-docs-writer (scripts) |
| US2 Colors (T027-T035) | python-todo-cli-dev |
| US3 Status Icons (T036-T041) | python-todo-cli-dev |
| US4 README (T042-T049) | todo-docs-writer |
| Polish (T050-T056) | todo-testing-agent |

---

## Notes

- [P] tasks = different files, no dependencies on incomplete tasks
- [Story] label maps task to specific user story for traceability
- Each user story is independently completable and testable
- GitHub URL: https://github.com/ikhlasbhojani/console-todo-app
- Install commands:
  - Linux/macOS: `curl -fsSL https://raw.githubusercontent.com/ikhlasbhojani/console-todo-app/main/scripts/install.sh | bash`
  - Windows: `irm https://raw.githubusercontent.com/ikhlasbhojani/console-todo-app/main/scripts/install.ps1 | iex`
- Run `uv run ruff check src/ tests/` before commits (constitution requirement)
