# Tasks: TODO APP - PHASE 2 (Advanced Features)

**Input**: Design documents from `/specs/004-phase2-advanced-features/`
**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Tests are OPTIONAL - not explicitly requested in this feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3, US4)
- Include exact file paths in descriptions

## Path Conventions

- **Single project**: `src/`, `tests/` at repository root

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Database migration and model extensions for Phase 2 features

- [X] T001 Add date validation utility function `validate_due_date()` in src/utils.py
- [X] T002 [P] Add project name validation utility function `validate_project_name()` in src/utils.py
- [X] T003 Extend Task dataclass with `due_date: date | None` and `project_id: int | None` fields in src/models.py
- [X] T004 [P] Add Project dataclass with id, name, description, created_at, task_count in src/models.py
- [X] T005 [P] Add TaskStats dataclass with total, pending, completed, due_today, overdue, completion_rate in src/models.py

---

## Phase 2: Foundational (Database Migration & Core Infrastructure)

**Purpose**: Core database changes that MUST be complete before ANY user story can be implemented

**CRITICAL**: No user story work can begin until this phase is complete

- [X] T006 Add `_ensure_columns_exist()` migration method to TodoManager in src/todo_manager.py
- [X] T007 Implement migration logic: check PRAGMA table_info, add due_date and project_id columns if missing
- [X] T008 Create projects table with `CREATE TABLE IF NOT EXISTS` in TodoManager._create_table()
- [X] T009 Update `_row_to_task()` to handle due_date and project_id columns in src/todo_manager.py
- [X] T010 Update `add_task()` to accept optional due_date and project_id parameters in src/todo_manager.py
- [X] T011 Update `list_tasks()` to return tasks with due_date and project_id populated in src/todo_manager.py
- [X] T012 Create ProjectManager class skeleton in src/project_manager.py with db_path parameter
- [X] T013 Update help command output to include Phase 2 commands placeholder in src/main.py

**Checkpoint**: Foundation ready - database schema extended, models updated, user story implementation can now begin

---

## Phase 3: User Story 1 - Due Dates and Filtered Task Views (Priority: P1) MVP

**Goal**: Allow users to assign due dates to tasks and filter by today/overdue/upcoming

**Independent Test**: Create tasks with various due dates, run `list --today`, `list --overdue`, `list --upcoming` to verify filters show correct tasks

### Implementation for User Story 1

- [X] T014 [US1] Implement `list_tasks_today()` method using SQL WHERE due_date = DATE('now', 'localtime') in src/todo_manager.py
- [X] T015 [P] [US1] Implement `list_tasks_overdue()` method using SQL WHERE due_date < DATE('now', 'localtime') AND status = 'pending' in src/todo_manager.py
- [X] T016 [P] [US1] Implement `list_tasks_upcoming()` method using SQL WHERE due_date BETWEEN DATE('now', 'localtime') AND DATE('now', 'localtime', '+7 days') in src/todo_manager.py
- [X] T017 [US1] Update `add` command prompts to include "Due date (YYYY-MM-DD, optional):" in src/main.py
- [X] T018 [US1] Add due date validation with error message "Invalid date format. Use YYYY-MM-DD" in add command handler
- [X] T019 [US1] Update task table display to include Due Date column in src/theme.py
- [X] T020 [US1] Implement `list --today` command handler in src/main.py with header "Tasks due today (YYYY-MM-DD):"
- [X] T021 [P] [US1] Implement `list --overdue` command handler in src/main.py with header "Overdue tasks:"
- [X] T022 [P] [US1] Implement `list --upcoming` command handler in src/main.py with header "Upcoming tasks (next 7 days):"
- [X] T023 [US1] Handle empty results for each filter with appropriate info messages per contracts/list-filters.md
- [X] T024 [US1] Update help command to document list --today, --overdue, --upcoming filters in src/main.py

**Checkpoint**: User Story 1 complete - users can add tasks with due dates and filter by urgency

---

## Phase 4: User Story 2 - Project Management with Full CRUD (Priority: P2)

**Goal**: Allow users to create/manage projects and assign tasks to them

**Independent Test**: Run `project create` to create a project, `add` a task to it, `project view` to see tasks, `project delete` to remove

### Implementation for User Story 2

- [X] T025 [US2] Implement `create_project(name, description)` in src/project_manager.py with name uniqueness check
- [X] T026 [US2] Implement `list_projects()` in src/project_manager.py with task count via COUNT query
- [X] T027 [P] [US2] Implement `get_project(name)` in src/project_manager.py with case-insensitive lookup
- [X] T028 [P] [US2] Implement `get_project_by_id(id)` in src/project_manager.py for FK lookups
- [X] T029 [US2] Implement `delete_project(name, cascade=False)` in src/project_manager.py with cascade delete logic
- [X] T030 [US2] Implement `get_tasks_by_project(project_id)` in src/todo_manager.py for project view
- [X] T031 [US2] Add `project create` command handler with name/description prompts in src/main.py
- [X] T032 [US2] Add `project list` command handler with table display per contracts/projects.md in src/main.py
- [X] T033 [US2] Add `project view <name>` command handler with task table in src/main.py
- [X] T034 [US2] Add `project delete` command handler with cascade confirmation prompt in src/main.py
- [X] T035 [US2] Update `add` command prompts to include "Project (optional):" with validation in src/main.py
- [X] T036 [US2] Add project lookup and validation when assigning task to project in add handler
- [X] T037 [US2] Implement `list --project <name>` command handler in src/main.py
- [X] T038 [US2] Update task table display to include Project column (lookup name from project_id) in src/theme.py
- [X] T039 [US2] Update help command to document project create/list/view/delete and list --project in src/main.py

**Checkpoint**: User Story 2 complete - users can manage projects and organize tasks

---

## Phase 5: User Story 3 - Task Statistics Dashboard (Priority: P3)

**Goal**: Display comprehensive task statistics including counts and completion rates

**Independent Test**: Create various tasks (pending, completed, with due dates), run `stats` command, verify metrics match

### Implementation for User Story 3

- [X] T040 [US3] Implement `get_stats()` method in src/todo_manager.py using single SQL aggregate query
- [X] T041 [US3] Return TaskStats dataclass with total, pending, completed, due_today, overdue counts
- [X] T042 [US3] Calculate completion_rate property avoiding division by zero (0.0% if total=0)
- [X] T043 [US3] Add `stats` command handler in src/main.py with table display per contracts/stats.md
- [X] T044 [US3] Handle zero tasks case with "No tasks yet. Add one with 'add'." message
- [X] T045 [US3] Add contextual messages: "All tasks completed!" when pending=0, "You have N overdue tasks" when overdue>0
- [X] T046 [US3] Update help command to document stats command in src/main.py

**Checkpoint**: User Story 3 complete - users can view task statistics dashboard

---

## Phase 6: User Story 4 - Undo Last Action (Priority: P4 - Optional/Stretch)

**Goal**: Allow users to undo their last action (add, delete, complete)

**Independent Test**: Add a task, run `undo`, verify task is deleted. Delete a task, run `undo`, verify task is restored.

### Implementation for User Story 4

- [ ] T047 [P] [US4] Create UndoAction dataclass with action_type, task_id, previous_state, new_state in src/undo.py
- [ ] T048 [P] [US4] Create UndoManager class with store_action() and get_last_action() methods in src/undo.py
- [ ] T049 [US4] Integrate UndoManager into main.py - create single instance at startup
- [ ] T050 [US4] Store add action after successful task creation (task_id, new_state)
- [ ] T051 [US4] Store delete action before task deletion (task_id, previous_state)
- [ ] T052 [US4] Store complete action before status change (task_id, previous_state='pending')
- [ ] T053 [US4] Implement `undo` command handler that reverses last action in src/main.py
- [ ] T054 [US4] Handle undo add: delete the newly added task
- [ ] T055 [US4] Handle undo delete: restore task with all original data
- [ ] T056 [US4] Handle undo complete: revert task status to pending
- [ ] T057 [US4] Clear undo state after successful undo (single-level only)
- [ ] T058 [US4] Handle "Nothing to undo" when no action stored
- [ ] T059 [US4] Update help command to document undo command with limitations in src/main.py

**Checkpoint**: User Story 4 complete - users can undo their last action

---

## Phase 7: Polish & Cross-Cutting Concerns

**Purpose**: Improvements that affect multiple user stories

- [X] T060 Verify all error messages match contracts (list-filters.md, projects.md, stats.md)
- [ ] T061 Run ruff check and fix any linting issues in src/ and tests/ (skipped - use ruff CLI directly)
- [ ] T062 [P] Run existing tests to ensure Phase 1 functionality not broken (optional - tests exist in tests/)
- [ ] T063 [P] Run quickstart.md validation checklist manually (optional - manual testing)
- [ ] T064 Update CLAUDE.md if needed for new commands (not needed - CLAUDE.md is for agent behavior)

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3-6)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3 → P4)
- **Polish (Phase 7)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P2)**: Can start after Foundational (Phase 2) - Uses shared table display from US1 but independently testable
- **User Story 3 (P3)**: Can start after Foundational (Phase 2) - Uses due_date filters internally but independently testable
- **User Story 4 (P4)**: Can start after Foundational (Phase 2) - Optional, may be skipped

### Within Each User Story

- TodoManager/ProjectManager methods before CLI handlers
- Core implementation before table display updates
- All features before help command updates
- Story complete before moving to next priority

### Parallel Opportunities

- T001 and T002 can run in parallel (different validation functions)
- T003, T004, T005 can run in parallel (different dataclasses)
- T014, T015, T016 can run in parallel (different filter methods)
- T020, T021, T022 can run in parallel (different command handlers)
- T025-T029 ProjectManager methods can partially run in parallel
- T047, T048 can run in parallel (undo dataclass and manager)

---

## Parallel Example: User Story 1

```bash
# Launch filter methods in parallel:
Task T014: "Implement list_tasks_today() in src/todo_manager.py"
Task T015: "Implement list_tasks_overdue() in src/todo_manager.py"
Task T016: "Implement list_tasks_upcoming() in src/todo_manager.py"

# After methods complete, launch command handlers in parallel:
Task T020: "Implement list --today command handler in src/main.py"
Task T021: "Implement list --overdue command handler in src/main.py"
Task T022: "Implement list --upcoming command handler in src/main.py"
```

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup (T001-T005)
2. Complete Phase 2: Foundational (T006-T013)
3. Complete Phase 3: User Story 1 (T014-T024)
4. **STOP and VALIDATE**: Test due dates and filters independently
5. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 (optional) → Test independently → Deploy/Demo
6. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (due dates & filters)
   - Developer B: User Story 2 (projects)
   - Developer C: User Story 3 (statistics)
3. Stories complete and integrate independently

---

## Summary

| Phase | Description | Task Count |
|-------|-------------|------------|
| Phase 1 | Setup | 5 tasks |
| Phase 2 | Foundational | 8 tasks |
| Phase 3 | US1 - Due Dates & Filters (P1) | 11 tasks |
| Phase 4 | US2 - Project Management (P2) | 15 tasks |
| Phase 5 | US3 - Statistics Dashboard (P3) | 7 tasks |
| Phase 6 | US4 - Undo (P4 - Optional) | 13 tasks |
| Phase 7 | Polish | 5 tasks |
| **Total** | | **64 tasks** |

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- US4 (Undo) is optional/stretch - can be skipped if time-constrained
