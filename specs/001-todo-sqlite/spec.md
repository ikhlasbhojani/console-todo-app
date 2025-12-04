# Feature Specification: TODO APP - SQLITE (PHASE 1)

**Feature Branch**: `001-todo-sqlite`
**Created**: 2025-12-04
**Status**: Draft
**Input**: Console-based todo application with SQLite persistence for basic task management

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Add and View Tasks (Priority: P1)

As a user, I want to add new tasks with a title and description, and then view all my tasks in a list format, so that I can keep track of what I need to do.

**Why this priority**: This is the core functionality - without adding and viewing tasks, the application has no value. Users must be able to create tasks and see them.

**Independent Test**: Can be fully tested by adding tasks via the `add` command and viewing them via `list` command. Delivers immediate value by allowing task tracking.

**Acceptance Scenarios**:

1. **Given** the application is running, **When** I type `add` and provide a title "Buy milk" and description "Buy 2 liters from store", **Then** the system displays `[OK] Task created with ID: 1`
2. **Given** I have added tasks, **When** I type `list`, **Then** I see all tasks displayed with ID, Title, Status indicator ([ ] for pending), and Created date
3. **Given** no tasks exist, **When** I type `list`, **Then** I see "No tasks found."
4. **Given** I am prompted for a title, **When** I enter an empty string or whitespace only, **Then** the system shows an error and prompts again

---

### User Story 2 - Mark Tasks Complete (Priority: P2)

As a user, I want to mark tasks as completed, so that I can track my progress and know what is done versus what remains.

**Why this priority**: Completing tasks is the second most essential function after creating them. Without completion tracking, the todo list cannot show progress.

**Independent Test**: Can be tested by creating a task, marking it complete, and verifying the status changes from [ ] Pending to [x] Done in the list view.

**Acceptance Scenarios**:

1. **Given** a pending task with ID 1 exists, **When** I type `complete` and enter ID 1, **Then** the system displays `[OK] Task 1 marked as completed.`
2. **Given** task 1 is already completed, **When** I try to complete it again, **Then** the system displays "Task is already complete."
3. **Given** I enter a non-existent task ID, **When** I try to complete it, **Then** the system displays `[ERROR] Task not found`
4. **Given** I enter an invalid ID (non-integer), **When** I try to complete it, **Then** the system shows an appropriate error message

---

### User Story 3 - Update Task Details (Priority: P3)

As a user, I want to update the title or description of an existing task, so that I can correct mistakes or add more detail as needed.

**Why this priority**: Updating tasks is important but secondary to core create/complete workflow. Users can manage tasks without updates initially.

**Independent Test**: Can be tested by creating a task, updating its title/description, and verifying changes appear in list view.

**Acceptance Scenarios**:

1. **Given** a task with ID 1 exists, **When** I type `update`, enter ID 1, and provide a new title "Buy milk and eggs", **Then** the system displays `[OK] Task 1 updated.`
2. **Given** I am updating a task, **When** I leave the title blank, **Then** the original title is preserved
3. **Given** I am updating a task, **When** I leave the description blank, **Then** the original description is preserved
4. **Given** I enter a non-existent task ID, **When** I try to update it, **Then** the system displays `[ERROR] Task not found`

---

### User Story 4 - Delete Tasks (Priority: P4)

As a user, I want to delete tasks I no longer need, so that my task list stays clean and relevant.

**Why this priority**: Deletion is a secondary operation. Users can ignore old tasks without deleting them. Also includes confirmation to prevent accidental deletion.

**Independent Test**: Can be tested by creating a task, deleting it with confirmation, and verifying it no longer appears in list.

**Acceptance Scenarios**:

1. **Given** a task with ID 2 exists, **When** I type `delete`, enter ID 2, and confirm with 'y', **Then** the system displays `[OK] Task 2 deleted.`
2. **Given** I am deleting a task, **When** I enter 'n' at confirmation, **Then** the task is NOT deleted and I return to the prompt
3. **Given** I enter a non-existent task ID, **When** I try to delete it, **Then** the system displays `[ERROR] Task not found`

---

### User Story 5 - Application Navigation (Priority: P5)

As a user, I want to see available commands via help and exit the application gracefully, so that I can learn to use the app and close it properly.

**Why this priority**: Help and exit are utility functions that support the main workflow but are not core task management features.

**Independent Test**: Can be tested by running `help` to see command list and `exit` to close the application.

**Acceptance Scenarios**:

1. **Given** the application starts, **When** I see the initial screen, **Then** I see a banner with app name and prompt to type 'help'
2. **Given** I am at the prompt, **When** I type `help`, **Then** I see a list of all available commands with descriptions
3. **Given** I am at the prompt, **When** I type `exit`, **Then** I see "Goodbye!" and the application closes
4. **Given** I type an unknown command like `complet`, **When** I press enter, **Then** the system displays `[ERROR] Unknown command: 'complet'. Type 'help' to see commands.`

---

### Edge Cases

- **Empty title**: When user enters empty or whitespace-only title during `add`, show error and re-prompt
- **Invalid task ID format**: When user enters non-integer ID (e.g., "abc", "1.5"), show clear error
- **Non-existent task ID**: When user enters valid integer but task doesn't exist, show `[ERROR] Task not found`
- **Already completed task**: When user tries to complete an already-completed task, show "Task is already complete."
- **Delete confirmation**: User must type 'y' to confirm deletion; any other input cancels the operation
- **Data persistence**: Tasks must survive application restart (stored in database file)
- **Case sensitivity**: Commands should be case-insensitive (e.g., `ADD`, `Add`, `add` all work the same)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display a startup banner showing "TODO APP - SQLITE (PHASE 1)" and prompt instructions
- **FR-002**: System MUST accept commands: `add`, `list`, `update`, `complete`, `delete`, `help`, `exit`
- **FR-003**: System MUST handle commands case-insensitively
- **FR-004**: System MUST display `[ERROR] Unknown command: '<cmd>'. Type 'help' to see commands.` for invalid commands
- **FR-005**: System MUST prompt for title and description when user types `add`
- **FR-006**: System MUST validate that title is not empty (after trimming whitespace)
- **FR-007**: System MUST auto-generate unique integer IDs for new tasks
- **FR-008**: System MUST display `[OK] Task created with ID: <id>` upon successful task creation
- **FR-009**: System MUST display tasks in a formatted table with columns: ID, Title, Status, Created At
- **FR-010**: System MUST show "[ ] Pending" for incomplete tasks and "[x] Done" for completed tasks
- **FR-011**: System MUST display "No tasks found." when list is empty
- **FR-012**: System MUST prompt for task ID when user types `update`, `complete`, or `delete`
- **FR-013**: System MUST validate task ID is a valid integer
- **FR-014**: System MUST display `[ERROR] Task not found` when task ID does not exist
- **FR-015**: System MUST allow partial updates (blank input preserves current value)
- **FR-016**: System MUST require confirmation (y/n) before deleting a task
- **FR-017**: System MUST display "Task is already complete." when completing an already-done task
- **FR-018**: System MUST persist all task data to a database file that survives restarts
- **FR-019**: System MUST display "Goodbye!" and exit cleanly when user types `exit`
- **FR-020**: System MUST auto-set created_at timestamp when task is created
- **FR-021**: System MUST auto-update updated_at timestamp when task is modified

### Key Entities

- **Task**: Represents a single todo item with the following attributes:
  - **ID**: Unique identifier (auto-generated integer, starts at 1)
  - **Title**: Required short text describing what needs to be done (cannot be empty)
  - **Description**: Optional longer text with additional details (can be empty)
  - **Status**: Current state - either "pending" (default) or "done"
  - **Created At**: Timestamp when the task was first created
  - **Updated At**: Timestamp when the task was last modified (including completion)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can create a new task in under 30 seconds (type `add`, enter title, enter description)
- **SC-002**: Users can view all their tasks with a single command (`list`)
- **SC-003**: Users can mark a task complete in under 10 seconds (type `complete`, enter ID)
- **SC-004**: 100% of tasks persist after application restart (no data loss)
- **SC-005**: Users see clear feedback for every action (`[OK]` for success, `[ERROR]` for failures)
- **SC-006**: New users can discover all commands within 5 seconds by typing `help`
- **SC-007**: All error messages clearly indicate what went wrong and how to fix it
- **SC-008**: Task list displays all relevant information (ID, title, status, date) in aligned columns

## Console Interface Specification

### Startup Banner

```
====================================
      TODO APP - SQLITE (PHASE 1)
====================================
Type 'help' to see available commands.

>
```

### Help Command Output

```
> help

Available commands:
  add      - Add a new task
  list     - Show all tasks
  update   - Update an existing task (title/description)
  complete - Mark a task as completed
  delete   - Delete a task
  exit     - Quit the application

>
```

### Add Command Flow

```
> add
Enter title: Buy milk
Enter description: Buy 2 liters of milk from the store.

[OK] Task created with ID: 1

>
```

### List Command Output (with tasks)

```
> list

ID   Title              Status        Created At
---  -----------------  ------------  ----------------
1    Buy milk           [ ] Pending   2025-12-04 10:15
2    Finish report      [x] Done      2025-12-04 10:30

>
```

### List Command Output (empty)

```
> list

No tasks found.

>
```

### Update Command Flow

```
> update
Enter task ID to update: 1
New title (leave blank to keep current): Buy milk and eggs
New description (leave blank to keep current):

[OK] Task 1 updated.

>
```

### Complete Command Flow

```
> complete
Enter task ID to mark complete: 1

[OK] Task 1 marked as completed.

>
```

### Delete Command Flow

```
> delete
Enter task ID to delete: 2
Are you sure you want to delete task 2? (y/n): y

[OK] Task 2 deleted.

>
```

### Error Examples

```
> complet
[ERROR] Unknown command: 'complet'. Type 'help' to see commands.

> complete
Enter task ID to mark complete: 999
[ERROR] Task not found

> add
Enter title:
[ERROR] Title cannot be empty. Please enter a valid title.
Enter title:
```

### Exit Command

```
> exit

Goodbye!
```

## Assumptions

1. **Single user**: This is a single-user application; no authentication or multi-user support needed
2. **Local storage**: Database is stored locally on the user's machine
3. **Sequential IDs**: Task IDs are simple auto-incrementing integers starting from 1
4. **No categories/tags**: Phase 1 does not include task categorization or tagging
5. **No due dates**: Phase 1 does not include due date functionality
6. **No priorities**: Phase 1 does not include task priority levels
7. **Simple status**: Only two states (pending/done); no in-progress or other states
8. **Text-based UI**: Pure console/terminal interface; no GUI
9. **Immediate persistence**: Changes are saved immediately; no explicit "save" command needed
10. **Date format**: Dates displayed as YYYY-MM-DD HH:MM format
