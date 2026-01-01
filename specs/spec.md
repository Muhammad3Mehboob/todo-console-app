# Feature Specification: Phase I - In-Memory Console App

**Feature Branch**: `001-phase1-console-app`
**Created**: 2026-01-01
**Status**: Draft
**Input**: User description: "Build a command-line interface (CLI) todo application that allows users to manage tasks stored in-memory. This serves as the foundation for the evolving system, focusing on core logic and clean Python structure."

## User Scenarios & Testing *(mandatory)*

### User Story 1 - View All Tasks (Priority: P1)

A user wants to see their current task list to understand what needs to be done.

**Why this priority**: Viewing tasks is the most fundamental operation - users need to see what exists before they can interact with it. This is the MVP baseline that demonstrates the system works.

**Independent Test**: Can be fully tested by launching the app, executing the view command, and verifying the output displays correctly (formatted list or "No tasks found" message).

**Acceptance Scenarios**:

1. **Given** no tasks exist, **When** user views the task list, **Then** system displays "No tasks found."
2. **Given** 3 tasks exist (1 complete, 2 incomplete), **When** user views the task list, **Then** system displays all 3 tasks with ID, status indicator, title, and description in a formatted table/list
3. **Given** tasks exist with varying title and description lengths, **When** user views the list, **Then** display remains readable and properly formatted

---

### User Story 2 - Add a New Task (Priority: P2)

A user wants to create a new task with a title and optional description so they can track something they need to do.

**Why this priority**: Adding tasks is the second most critical operation - without it, the list remains empty. This enables basic task capture.

**Independent Test**: Can be tested by adding a task with title only, adding a task with title and description, and verifying both are stored and displayed correctly with auto-assigned IDs.

**Acceptance Scenarios**:

1. **Given** user provides a valid title (1-200 characters), **When** user adds a task, **Then** system assigns unique ID, stores task with "Incomplete" status, and confirms "Task '[title]' added with ID [N]"
2. **Given** user provides title and description, **When** user adds a task, **Then** system stores both fields and displays confirmation
3. **Given** user provides empty title, **When** user attempts to add task, **Then** system displays error "Title cannot be empty (1-200 characters required)"
4. **Given** user provides title exceeding 200 characters, **When** user attempts to add task, **Then** system displays error "Title cannot exceed 200 characters"
5. **Given** multiple tasks have been added, **When** user adds a new task, **Then** system assigns next sequential ID (auto-increment)

---

### User Story 3 - Toggle Task Completion (Priority: P3)

A user wants to mark a task as complete or incomplete to track progress.

**Why this priority**: Completion tracking provides the core value of a todo list - showing what's done vs. what remains. This makes the list actionable.

**Independent Test**: Can be tested by creating a task, toggling it to complete (status indicator changes), toggling back to incomplete, and verifying status changes are reflected in the view.

**Acceptance Scenarios**:

1. **Given** an incomplete task with ID 5, **When** user toggles completion for ID 5, **Then** system marks task as complete and confirms "Task 5 marked as Complete"
2. **Given** a complete task with ID 3, **When** user toggles completion for ID 3, **Then** system marks task as incomplete and confirms "Task 3 marked as Incomplete"
3. **Given** user provides non-existent task ID 99, **When** user attempts to toggle completion, **Then** system displays error "Task ID not found"

---

### User Story 4 - Update Task Details (Priority: P4)

A user wants to modify a task's title or description to correct mistakes or add information.

**Why this priority**: Updates allow users to refine tasks without deleting and recreating them. This is a quality-of-life feature that enhances usability.

**Independent Test**: Can be tested by creating a task, updating its title only, updating its description only, updating both, and verifying changes are reflected while other fields remain unchanged.

**Acceptance Scenarios**:

1. **Given** task ID 2 exists with title "Old Title", **When** user updates title to "New Title", **Then** system updates only the title and confirms "Task 2 updated"
2. **Given** task ID 4 exists with description "Old Desc", **When** user updates description to "New Desc", **Then** system updates only the description and confirms "Task 4 updated"
3. **Given** task ID 7 exists, **When** user updates both title and description, **Then** system updates both fields and preserves ID and completion status
4. **Given** user provides non-existent task ID 50, **When** user attempts to update, **Then** system displays error "Task ID not found"
5. **Given** user provides empty title in update, **When** user attempts to update, **Then** system displays error "Title cannot be empty (1-200 characters required)"

---

### User Story 5 - Delete a Task (Priority: P5)

A user wants to remove a task that's no longer relevant or was added by mistake.

**Why this priority**: Deletion keeps the list clean and focused. It's the lowest priority because users can work effectively even without deletion (they can just ignore tasks).

**Independent Test**: Can be tested by creating tasks, deleting one by ID, verifying it no longer appears in the list, and confirming the ID cannot be accessed again.

**Acceptance Scenarios**:

1. **Given** task ID 8 exists, **When** user deletes task ID 8, **Then** system removes task from memory and confirms "Task 8 deleted"
2. **Given** task ID 8 has been deleted, **When** user views task list, **Then** task ID 8 does not appear
3. **Given** task ID 8 has been deleted, **When** user attempts to view/update/toggle/delete ID 8, **Then** system displays error "Task ID not found"
4. **Given** user provides non-existent task ID 100, **When** user attempts to delete, **Then** system displays error "Task ID not found"

---

### Edge Cases

- What happens when user attempts to add a task with special characters in title/description (e.g., quotes, newlines, unicode)?
- How does the system handle rapid successive operations (add 100 tasks quickly)?
- What happens when user provides invalid input types (e.g., letters instead of numbers for task ID)?
- How does the system behave when user interrupts an operation (Ctrl+C)?
- What happens when the system reaches memory limits (thousands of tasks)?

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST allow users to create a task with a mandatory title (1-200 characters) and optional description (any length)
- **FR-002**: System MUST assign a unique, auto-incrementing integer ID to each task starting from 1
- **FR-003**: System MUST store tasks in memory during the session (volatile storage - data lost on exit)
- **FR-004**: System MUST display all tasks in a formatted table or list showing ID, status indicator, title, and description
- **FR-005**: System MUST use clear visual status indicators: `[ ]` for incomplete tasks, `[X]` for complete tasks
- **FR-006**: System MUST display "No tasks found." when the task list is empty
- **FR-007**: System MUST allow users to update the title and/or description of an existing task by providing its ID
- **FR-008**: System MUST preserve unchanged fields when updating a task (e.g., updating only title preserves description and status)
- **FR-009**: System MUST allow users to toggle a task's completion status between "Complete" and "Incomplete" by providing its ID
- **FR-010**: System MUST allow users to delete a task by providing its ID, removing it from memory
- **FR-011**: System MUST display error message "Task ID not found" when user attempts to operate on a non-existent ID
- **FR-012**: System MUST display error message "Title cannot be empty (1-200 characters required)" when user provides invalid title
- **FR-013**: System MUST confirm successful operations with appropriate messages (e.g., "Task 5 added", "Task 3 updated", "Task 7 deleted")
- **FR-014**: System MUST set new tasks to "Incomplete" status by default
- **FR-015**: System MUST operate as a command-line interface (CLI) accepting text commands

### Key Entities *(include if feature involves data)*

- **Task**: Represents a todo item that users want to track. Contains:
  - **ID**: Unique auto-incrementing integer identifier (starts at 1)
  - **Title**: Short descriptive text (1-200 characters, mandatory)
  - **Description**: Detailed text (optional, any length)
  - **Status**: Completion state (boolean: Complete or Incomplete)

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can view their task list and see all tasks or receive a clear "No tasks found" message in under 1 second
- **SC-002**: Users can add a new task with just a title in under 5 seconds (including typing time)
- **SC-003**: Users can toggle a task's completion status in under 3 seconds
- **SC-004**: System correctly handles and stores at least 1000 tasks without performance degradation (operations still complete in under 1 second)
- **SC-005**: 100% of operations (add, view, update, delete, toggle) provide clear confirmation or error messages
- **SC-006**: Users can complete a full workflow (add task → view list → mark complete → delete task) in under 30 seconds
- **SC-007**: System displays task list in a readable format that clearly distinguishes complete vs incomplete tasks at a glance
- **SC-008**: All task IDs are unique within a session with no ID collisions or duplicates

## Assumptions *(include if making default choices)*

- **Assumption 1**: Users will interact with the system through a standard terminal/console (no GUI required)
- **Assumption 2**: Tasks are personal and do not need to be shared with other users (single-user system)
- **Assumption 3**: Performance targets assume modern hardware (2+ GHz CPU, 4+ GB RAM)
- **Assumption 4**: Users understand basic CLI operations (typing commands, reading output)
- **Assumption 5**: Session length is reasonable (under 8 hours); no need to optimize for days-long sessions
- **Assumption 6**: Task descriptions can contain any printable text including special characters (system will handle display appropriately)
- **Assumption 7**: CLI commands will follow common patterns (e.g., `add`, `list`, `update`, `delete`, `toggle`) for intuitive use
- **Assumption 8**: Error messages will be displayed to stderr while normal output goes to stdout (standard CLI practice)

## Constraints *(mandatory)*

### Technical Constraints

- **TC-001**: MUST use Python 3.13 or later
- **TC-002**: MUST use UV for package management and dependency handling
- **TC-003**: MUST NOT use external databases (SQL, NoSQL, file storage) - all data in-memory only
- **TC-004**: MUST implement as a CLI/Console application (no web server, no GUI)
- **TC-005**: MUST follow PEP 8 code style guidelines
- **TC-006**: MUST include type hints for all function signatures
- **TC-007**: MUST include docstrings for all public functions and classes
- **TC-008**: MUST achieve 90% code coverage with unit tests

### Business Constraints

- **BC-001**: This is Phase I of a 5-phase evolution - must maintain clean architecture to support future extensions
- **BC-002**: Code must be structured to easily transition to persistent storage in Phase II
- **BC-003**: Must demonstrate core task management logic independent of storage technology
- **BC-004**: Must serve as foundation for REST API in later phases - business logic should be separable from CLI interface

## Out of Scope *(mandatory)*

The following are explicitly NOT part of Phase I:

- **Data persistence** (database, file storage, cloud storage)
- **User authentication or multi-user support**
- **Task sharing or collaboration features**
- **Task categories, tags, or labels**
- **Task priorities or due dates**
- **Recurring tasks or reminders**
- **Search or filter capabilities**
- **Undo/redo functionality**
- **Task history or audit trail**
- **Import/export functionality**
- **Web interface or API**
- **Mobile app or desktop GUI**
- **Cloud synchronization**
- **Natural language processing for task input**

These features are planned for later phases as defined in the project constitution.
