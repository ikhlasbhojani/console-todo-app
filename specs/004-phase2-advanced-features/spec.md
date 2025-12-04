# Feature Specification: TODO APP - PHASE 2 (Advanced Features)

**Feature Branch**: `004-phase2-advanced-features`
**Created**: 2025-12-05
**Status**: Draft
**Input**: Phase 2 advanced features building on Phase 1 SQLite todo application

---

## Overview

Enhance the Phase 1 console todo application with advanced task management capabilities including due dates with filtered views, project categorization with full CRUD operations, task statistics dashboard, and optional undo functionality.

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Due Dates and Filtered Task Views (Priority: P1)

As a user managing time-sensitive tasks, I want to assign due dates to my tasks and filter them by urgency (today, overdue, upcoming) so I can prioritize my work effectively and never miss a deadline.

**Why this priority**: Due dates are the most fundamental enhancement for task management. Without date awareness, users cannot prioritize effectively or identify missed deadlines.

**Independent Test**: Create tasks with various due dates, then use filter commands to view tasks due today, overdue tasks, and upcoming tasks. Each filter should show only relevant tasks.

**Acceptance Scenarios**:

1. **Given** the add command is executed, **When** prompted for details, **Then** user can optionally enter a due date in YYYY-MM-DD format
2. **Given** a due date is entered in invalid format, **When** submitted, **Then** system displays error and re-prompts
3. **Given** tasks exist with various due dates, **When** user runs `list --today`, **Then** only tasks due on current date are shown
4. **Given** pending tasks exist with past due dates, **When** user runs `list --overdue`, **Then** only overdue pending tasks are shown (completed tasks excluded)
5. **Given** tasks exist with future due dates, **When** user runs `list --upcoming`, **Then** tasks due within next 7 days are shown
6. **Given** the task table is displayed, **When** due date column is shown, **Then** dates appear in YYYY-MM-DD format

---

### User Story 2 - Project Management with Full CRUD (Priority: P2)

As a user organizing tasks by context, I want to create and manage projects (categories) and assign tasks to them so I can group related tasks and view them together.

**Why this priority**: Projects provide organizational structure that builds on due dates. Users need categories to manage tasks across different life areas (work, personal, etc.).

**Independent Test**: Create a project, add tasks to it, view project task list, and delete the project with its tasks.

**Acceptance Scenarios**:

1. **Given** user runs `project create`, **When** prompted, **Then** user can enter project name and optional description
2. **Given** project name already exists, **When** user tries to create it, **Then** system shows error "Project name already exists"
3. **Given** projects exist, **When** user runs `project list`, **Then** all projects are shown with task counts
4. **Given** a project exists with tasks, **When** user runs `project view <name>`, **Then** all tasks in that project are displayed
5. **Given** user runs `project delete`, **When** project has tasks, **Then** system asks for confirmation before cascade delete
6. **Given** adding a task, **When** prompted for project, **Then** user can assign to existing project or leave blank
7. **Given** user enters non-existent project name during task creation, **When** submitted, **Then** system shows error and suggests creating project first

---

### User Story 3 - Task Statistics Dashboard (Priority: P3)

As a user tracking my productivity, I want to see statistics about my tasks including total counts, completion rates, and deadline status so I can understand my task management performance.

**Why this priority**: Statistics provide insights but are not essential for core task management. This enhances user experience without blocking basic functionality.

**Independent Test**: Create various tasks (pending, completed, with different due dates), run `stats` command, verify all metrics are calculated correctly.

**Acceptance Scenarios**:

1. **Given** tasks exist in the system, **When** user runs `stats`, **Then** total task count is displayed
2. **Given** tasks have mixed statuses, **When** stats are shown, **Then** pending and completed counts are displayed separately
3. **Given** tasks have due dates, **When** stats are shown, **Then** "due today" and "overdue" counts are displayed
4. **Given** completed and total tasks exist, **When** stats are shown, **Then** completion rate percentage is calculated and displayed
5. **Given** no tasks exist, **When** stats are shown, **Then** appropriate "no tasks" message is displayed

---

### User Story 4 - Undo Last Action (Priority: P4 - Optional/Stretch)

As a user who occasionally makes mistakes, I want to undo my last action so I can recover from accidental deletions or modifications without losing my data.

**Why this priority**: Undo is a safety feature that enhances user confidence but is optional functionality. The core app works without it.

**Independent Test**: Perform an action (add, delete, complete), immediately run `undo`, verify the action is reversed.

**Acceptance Scenarios**:

1. **Given** user just added a task, **When** user runs `undo`, **Then** the newly added task is deleted
2. **Given** user just deleted a task, **When** user runs `undo`, **Then** the deleted task is restored with all its data
3. **Given** user just completed a task, **When** user runs `undo`, **Then** task status reverts to pending
4. **Given** no action has been performed yet, **When** user runs `undo`, **Then** system shows "Nothing to undo"
5. **Given** user already ran undo once, **When** user runs `undo` again, **Then** system shows "Nothing to undo" (single-level only)

---

### Edge Cases

- **Invalid date format**: User enters "12-25-2025" instead of "2025-12-25" - system rejects and shows format hint
- **Past due date on new task**: User assigns past date - system accepts (task is immediately overdue)
- **Empty project name**: User leaves project name blank during project create - system shows error
- **Delete project with 0 tasks**: No confirmation needed, project deleted immediately
- **Case sensitivity in project names**: Project names are stored as-is but matched case-insensitively
- **Special characters in project names**: Only alphanumeric and underscores allowed
- **Undo across session**: Undo history is cleared when app restarts (in-memory only)
- **Stats with no overdue tasks**: "Overdue: 0" displayed, not hidden

---

## Requirements *(mandatory)*

### Functional Requirements

**Due Dates & Filters:**
- **FR-001**: System MUST allow optional due date entry during task creation in YYYY-MM-DD format
- **FR-002**: System MUST validate due date format and reject invalid dates with error message
- **FR-003**: System MUST display due date column in task list when any task has a due date
- **FR-004**: System MUST support `list --today` filter showing only tasks due on current date
- **FR-005**: System MUST support `list --overdue` filter showing only pending tasks with past due dates
- **FR-006**: System MUST support `list --upcoming` filter showing tasks due within next 7 days
- **FR-007**: System MUST persist due dates in the database for all tasks

**Project Management:**
- **FR-008**: System MUST support `project create` command with name (required) and description (optional)
- **FR-009**: System MUST enforce unique project names (case-insensitive matching)
- **FR-010**: System MUST validate project names as alphanumeric with underscores only
- **FR-011**: System MUST support `project list` showing all projects with task counts
- **FR-012**: System MUST support `project view <name>` showing all tasks in a project
- **FR-013**: System MUST support `project delete` with cascade delete confirmation if tasks exist
- **FR-014**: System MUST allow task assignment to project during task creation
- **FR-015**: System MUST show error when assigning task to non-existent project
- **FR-016**: System MUST persist projects in a separate database table

**Statistics:**
- **FR-017**: System MUST support `stats` command displaying task statistics
- **FR-018**: System MUST calculate and display total, pending, and completed task counts
- **FR-019**: System MUST calculate and display "due today" and "overdue" counts
- **FR-020**: System MUST calculate and display completion rate as percentage

**Undo (Optional):**
- **FR-021**: System SHOULD support `undo` command for last action (add, delete, complete, update)
- **FR-022**: System SHOULD support single-level undo only (not undo stack)
- **FR-023**: System SHOULD clear undo state on application restart

**Help & UI:**
- **FR-024**: System MUST update help command to include all new commands and filters
- **FR-025**: System MUST display appropriate success/error messages for all operations

### Key Entities

- **Task** (extended): Original task fields plus `due_date` (optional, ISO date format) and `project_id` (optional, foreign key to projects)
- **Project**: Represents a category/grouping for tasks with `id` (auto-generated), `name` (unique, required), `description` (optional), `created_at` (timestamp)

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create tasks with due dates in under 30 seconds
- **SC-002**: Filter commands (`--today`, `--overdue`, `--upcoming`) return results instantly (under 1 second)
- **SC-003**: Project creation, listing, and viewing operations complete in under 2 seconds
- **SC-004**: Statistics calculation and display completes in under 1 second for up to 1000 tasks
- **SC-005**: 100% of tasks with due dates appear in appropriate filtered views
- **SC-006**: All project CRUD operations persist correctly across application restarts
- **SC-007**: Undo functionality (if implemented) reverses the last action with 100% accuracy
- **SC-008**: Help command displays all new commands and filters accurately

---

## Assumptions

1. Phase 1 todo application with SQLite persistence is fully functional
2. Existing tasks without due dates or projects will display blank/null in those columns
3. Database schema can be migrated to add new columns (due_date, project_id) and new table (projects)
4. Due dates are stored as TEXT in ISO format (YYYY-MM-DD) for simplicity
5. "Upcoming" is defined as the next 7 days including today
6. Undo is in-memory only and does not persist across sessions
7. Project deletion cascades to delete all associated tasks

---

## Out of Scope

- Recurring/repeating tasks
- Task priorities (high/medium/low)
- Task reminders or notifications
- Multiple undo levels (undo history stack)
- Task dependencies or subtasks
- Project archiving (only create/delete)
- Task sorting options (alphabetical, by date, etc.)
- Task search functionality
- Import/export of tasks or projects
