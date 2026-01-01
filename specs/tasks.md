# Tasks: Phase I - In-Memory Console App

**Input**: Design documents from `/specs/001-phase1-console-app/`
**Prerequisites**: plan.md (complete), spec.md (complete), data-model.md (complete), research.md (complete), quickstart.md (complete)

**Tests**: Tests are NOT explicitly requested in the specification. Test tasks are included but can be skipped if focusing on MVP delivery.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `- [ ] [ID] [P?] [Story?] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

**Single project structure** (from plan.md):
- Source code: `todo-console/src/todo_app/`
- Tests: `todo-console/tests/unit/` and `todo-console/tests/integration/`

---

## Phase 1: Setup (Shared Infrastructure)

**Purpose**: Project initialization and basic structure

- [X] T001 Initialize project with UV at todo-console/ directory
- [X] T002 Configure pyproject.toml for Python 3.13+ and pytest settings
- [X] T003 [P] Create src/todo_app/ package structure with __init__.py
- [X] T004 [P] Create tests/ directory with unit/ and integration/ subdirs
- [X] T005 [P] Create .gitignore for Python project (venv, __pycache__, etc.)
- [X] T006 Add pytest and pytest-cov as dev dependencies via UV

**Checkpoint**: Project structure ready for implementation

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [X] T007 [P] Implement base exception classes (TodoAppError, ValidationError, TaskNotFoundError) in src/todo_app/models.py
- [X] T008 Implement Task dataclass with validation in src/todo_app/models.py
- [X] T009 Implement to_display_dict() method in Task class in src/todo_app/models.py
- [X] T010 Implement TodoManager class skeleton with __init__ in src/todo_app/manager.py
- [X] T011 Implement TodoManager.add_task() with ID generation in src/todo_app/manager.py
- [X] T012 Implement TodoManager.get_all_tasks() in src/todo_app/manager.py
- [X] T013 Implement TodoManager.get_task_by_id() in src/todo_app/manager.py

**Checkpoint**: Foundation ready - Task model and TodoManager core methods available for all user stories

---

## Phase 3: User Story 1 - View All Tasks (Priority: P1) 🎯 MVP

**Goal**: Enable users to see their current task list to understand what needs to be done

**Independent Test**: Launch app, execute view command, verify output displays correctly (formatted list or "No tasks found" message)

**Acceptance Criteria**:
- Empty list shows "No tasks found."
- Tasks display with ID, status indicator ([X] or [ ]), title, and description
- Display remains readable with varying content lengths

### Tests for User Story 1 (Optional)

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T014 [P] [US1] Write unit tests for Task.to_display_dict() in tests/unit/test_models.py
- [ ] T015 [P] [US1] Write unit tests for TodoManager.get_all_tasks() in tests/unit/test_manager.py

### Implementation for User Story 1

- [X] T016 [US1] Implement TodoCLI class skeleton with __init__(manager) in src/todo_app/cli.py
- [X] T017 [US1] Implement TodoCLI.format_task_table() method in src/todo_app/cli.py
- [X] T018 [US1] Implement TodoCLI.handle_list() method in src/todo_app/cli.py
- [X] T019 [US1] Implement TodoCLI.display_menu() showing available commands in src/todo_app/cli.py
- [X] T020 [US1] Implement TodoCLI.run() command loop skeleton (list + exit only) in src/todo_app/cli.py
- [X] T021 [US1] Implement main() function with TodoManager and TodoCLI initialization in src/todo_app/main.py

**Checkpoint**: User Story 1 complete - Users can view task list (empty or populated)

---

## Phase 4: User Story 2 - Add a New Task (Priority: P2)

**Goal**: Enable users to create new tasks with title and optional description

**Independent Test**: Add task with title only, add task with title and description, verify both stored with auto-assigned IDs

**Acceptance Criteria**:
- Valid title (1-200 chars) creates task with unique ID and "Incomplete" status
- Confirmation message: "Task '[title]' added with ID [N]"
- Empty title shows error: "Title cannot be empty (1-200 characters required)"
- Title >200 chars shows error: "Title cannot exceed 200 characters"
- Multiple tasks get sequential IDs (auto-increment)

### Tests for User Story 2 (Optional)

- [ ] T022 [P] [US2] Write unit tests for Task creation and validation in tests/unit/test_models.py
- [ ] T023 [P] [US2] Write unit tests for TodoManager.add_task() in tests/unit/test_manager.py

### Implementation for User Story 2

- [X] T024 [US2] Implement TodoCLI.handle_add() method with title/description prompts in src/todo_app/cli.py
- [X] T025 [US2] Implement TodoCLI.display_success() method for confirmation messages in src/todo_app/cli.py
- [X] T026 [US2] Implement TodoCLI.display_error() method for error messages in src/todo_app/cli.py
- [X] T027 [US2] Add "add" command to TodoCLI.run() command loop in src/todo_app/cli.py
- [X] T028 [US2] Add error handling (ValidationError) in TodoCLI.handle_add() in src/todo_app/cli.py

**Checkpoint**: User Story 2 complete - Users can add tasks and see confirmation or validation errors

---

## Phase 5: User Story 3 - Toggle Task Completion (Priority: P3)

**Goal**: Enable users to mark tasks as complete or incomplete to track progress

**Independent Test**: Create task, toggle to complete (status indicator changes), toggle back to incomplete, verify status changes reflected

**Acceptance Criteria**:
- Incomplete task toggles to complete with confirmation: "Task [N] marked as Complete"
- Complete task toggles to incomplete with confirmation: "Task [N] marked as Incomplete"
- Non-existent ID shows error: "Task ID not found"

### Tests for User Story 3 (Optional)

- [ ] T029 [P] [US3] Write unit tests for TodoManager.toggle_task() in tests/unit/test_manager.py

### Implementation for User Story 3

- [X] T030 [US3] Implement TodoManager.toggle_task(task_id) in src/todo_app/manager.py
- [X] T031 [US3] Implement TodoCLI.handle_toggle() with ID prompt in src/todo_app/cli.py
- [X] T032 [US3] Add "toggle" command to TodoCLI.run() command loop in src/todo_app/cli.py
- [X] T033 [US3] Add error handling (TaskNotFoundError) in TodoCLI.handle_toggle() in src/todo_app/cli.py

**Checkpoint**: User Story 3 complete - Users can toggle task completion status

---

## Phase 6: User Story 4 - Update Task Details (Priority: P4)

**Goal**: Enable users to modify task title or description to correct mistakes or add information

**Independent Test**: Create task, update title only, update description only, update both, verify changes reflected while other fields unchanged

**Acceptance Criteria**:
- Update title only preserves description and status
- Update description only preserves title and status
- Can update both title and description simultaneously
- Confirmation message: "Task [N] updated"
- Non-existent ID shows error: "Task ID not found"
- Empty title shows error: "Title cannot be empty (1-200 characters required)"

### Tests for User Story 4 (Optional)

- [ ] T034 [P] [US4] Write unit tests for TodoManager.update_task() in tests/unit/test_manager.py

### Implementation for User Story 4

- [X] T035 [US4] Implement TodoManager.update_task(task_id, title, description) in src/todo_app/manager.py
- [X] T036 [US4] Implement TodoCLI.handle_update() with ID and field prompts in src/todo_app/cli.py
- [X] T037 [US4] Add "update" command to TodoCLI.run() command loop in src/todo_app/cli.py
- [X] T038 [US4] Add error handling (TaskNotFoundError, ValidationError) in TodoCLI.handle_update() in src/todo_app/cli.py

**Checkpoint**: User Story 4 complete - Users can update task details selectively

---

## Phase 7: User Story 5 - Delete a Task (Priority: P5)

**Goal**: Enable users to remove tasks that are no longer relevant or added by mistake

**Independent Test**: Create tasks, delete one by ID, verify it no longer appears in list, confirm ID cannot be accessed again

**Acceptance Criteria**:
- Task deleted from memory with confirmation: "Task [N] deleted"
- Deleted task does not appear in list
- Operations on deleted ID show error: "Task ID not found"
- Non-existent ID shows error: "Task ID not found"

### Tests for User Story 5 (Optional)

- [ ] T039 [P] [US5] Write unit tests for TodoManager.delete_task() in tests/unit/test_manager.py

### Implementation for User Story 5

- [X] T040 [US5] Implement TodoManager.delete_task(task_id) in src/todo_app/manager.py
- [X] T041 [US5] Implement TodoCLI.handle_delete() with ID prompt in src/todo_app/cli.py
- [X] T042 [US5] Add "delete" command to TodoCLI.run() command loop in src/todo_app/cli.py
- [X] T043 [US5] Add error handling (TaskNotFoundError) in TodoCLI.handle_delete() in src/todo_app/cli.py

**Checkpoint**: User Story 5 complete - Users can delete tasks

---

## Phase 8: Integration & Polish

**Purpose**: Integration testing, documentation, and final quality checks

- [X] T044 [P] Write integration test for complete workflow (add→view→toggle→update→delete) in tests/integration/test_workflows.py
- [X] T045 [P] Write integration test for empty list edge case in tests/integration/test_workflows.py
- [X] T046 [P] Write integration test for 1000 tasks performance in tests/integration/test_workflows.py
- [X] T047 Add keyboard interrupt handling (Ctrl+C) in main() in src/todo_app/main.py
- [X] T048 Add welcome message and help text to main() in src/todo_app/main.py
- [X] T049 [P] Write README.md with setup instructions and usage examples at todo-console/README.md
- [X] T050 [P] Add docstrings to all public functions and classes (models.py, manager.py, cli.py, main.py)
- [X] T051 Run test suite with coverage report and verify ≥90% coverage
- [X] T052 Run PEP 8 linting and fix any style violations
- [X] T053 Manual testing of all user stories per spec acceptance criteria

**Checkpoint**: Phase I complete and ready for demo

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phases 3-7)**: All depend on Foundational phase completion
  - User stories can proceed in parallel (if staffed) after foundation ready
  - Or sequentially in priority order: US1 (P1) → US2 (P2) → US3 (P3) → US4 (P4) → US5 (P5)
- **Polish (Phase 8)**: Depends on all desired user stories being complete

### User Story Dependencies

- **US1 (View)**: Depends on Foundational (Phase 2) - No dependencies on other stories
- **US2 (Add)**: Depends on Foundational (Phase 2) - No dependencies on other stories
- **US3 (Toggle)**: Depends on Foundational (Phase 2) - No dependencies on other stories
- **US4 (Update)**: Depends on Foundational (Phase 2) - No dependencies on other stories
- **US5 (Delete)**: Depends on Foundational (Phase 2) - No dependencies on other stories

**Key Insight**: All user stories are independent after foundation is complete. They can be implemented in any order or in parallel.

### Within Each User Story

- Tests (if included) should be written FIRST and confirmed to FAIL
- Implementation tasks within a story follow natural dependencies:
  - TodoManager methods before CLI handlers
  - CLI handler before adding to command loop
  - Error handling after main implementation
- Tasks marked [P] can run in parallel (different files, no dependencies)

### Parallel Opportunities

**Setup Phase (all can run in parallel)**:
- T003 (create src structure), T004 (create tests structure), T005 (gitignore) can run together

**Foundational Phase (some can run in parallel)**:
- T007 (exception classes) can run in parallel with other tasks
- T008-T009 (Task model) must complete before T010-T013 (TodoManager)

**Within Each User Story (tests can run in parallel)**:
- All test tasks marked [P] can be written simultaneously
- Implementation tasks follow dependencies but some are parallelizable

**Polish Phase (most can run in parallel)**:
- T044, T045, T046 (integration tests) can run together
- T049 (README), T050 (docstrings) can run in parallel with tests
- T051-T053 (validation) must run after all implementation complete

---

## Parallel Example: Setup Phase

```bash
# All these can start simultaneously:
Task T003: Create src/todo_app/ package structure with __init__.py
Task T004: Create tests/ directory with unit/ and integration/ subdirs
Task T005: Create .gitignore for Python project
```

## Parallel Example: User Story 1 Tests

```bash
# If including tests, these can start simultaneously:
Task T014: Write unit tests for Task.to_display_dict() in tests/unit/test_models.py
Task T015: Write unit tests for TodoManager.get_all_tasks() in tests/unit/test_manager.py
```

## Parallel Example: Polish Phase

```bash
# Most polish tasks can run simultaneously:
Task T044: Write integration test for complete workflow
Task T045: Write integration test for empty list edge case
Task T046: Write integration test for 1000 tasks performance
Task T049: Write README.md with setup and usage
Task T050: Add docstrings to all public functions
```

---

## Implementation Strategy

### MVP First (Minimal Viable Product)

**Recommended MVP Scope: User Story 1 ONLY**

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL)
3. Complete Phase 3: User Story 1 (View Tasks)
4. **STOP and VALIDATE**:
   - Can launch app and view empty list
   - Shows "No tasks found." correctly
   - Can add a task manually in code and see it displayed
5. Demo this working state before proceeding

**MVP Deliverable**: Working CLI app that displays task list (even if empty)

### Incremental Delivery (Recommended)

**Phase-by-Phase Approach**:

1. **Setup + Foundational → Foundation Complete**
   - Tasks T001-T013 (13 tasks)
   - Deliverable: Task model and TodoManager with core methods

2. **Add User Story 1 → MVP Ready**
   - Tasks T014-T021 (8 tasks)
   - Deliverable: Can view task list
   - **VALIDATE**: Launch app, see "No tasks found.", exit cleanly

3. **Add User Story 2 → Can Create Tasks**
   - Tasks T022-T028 (7 tasks)
   - Deliverable: Can add tasks and view them
   - **VALIDATE**: Add task, view list, see task displayed

4. **Add User Story 3 → Can Track Completion**
   - Tasks T029-T033 (5 tasks)
   - Deliverable: Can toggle task status
   - **VALIDATE**: Add task, toggle complete, view list with [X]

5. **Add User Story 4 → Can Edit Tasks**
   - Tasks T034-T038 (5 tasks)
   - Deliverable: Can update task details
   - **VALIDATE**: Update title, update description, verify changes

6. **Add User Story 5 → Full CRUD Complete**
   - Tasks T039-T043 (5 tasks)
   - Deliverable: Complete task management
   - **VALIDATE**: Delete task, verify removed from list

7. **Polish → Production Ready**
   - Tasks T044-T053 (10 tasks)
   - Deliverable: Tested, documented, validated Phase I

**Each increment is independently deployable and demonstrable**

### Parallel Team Strategy

If multiple developers are available:

1. **Team completes Setup + Foundational together** (T001-T013)
2. **Once Foundational done, split work**:
   - Developer A: User Story 1 (T014-T021)
   - Developer B: User Story 2 (T022-T028)
   - Developer C: User Story 3 (T029-T033)
3. **Integration**:
   - Each story integrates cleanly (all use same TodoManager)
   - No conflicts (different CLI handlers)
4. **Polish together** (T044-T053)

---

## Notes

- **[P] tasks** = different files, no dependencies, can run in parallel
- **[Story] label** = maps task to specific user story for traceability (US1-US5)
- Each user story is independently completable and testable after foundation ready
- Tests are optional but recommended for 90% coverage target (constitutional requirement)
- Verify acceptance criteria from spec.md after each story
- Commit after each phase or logical group with task references in commit message
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence

**Task ID Format**: T001-T053 (53 total tasks)
**Parallelizable Tasks**: 18 tasks marked with [P]
**User Story Tasks**: 37 tasks across 5 user stories
**Setup/Foundation/Polish**: 16 tasks

---

**Tasks Status**: ✅ Complete - Ready for implementation

**Next Steps**:
1. Begin with Phase 1 (Setup) - Tasks T001-T006
2. Complete Phase 2 (Foundational) - Tasks T007-T013
3. Implement MVP (User Story 1) - Tasks T014-T021
4. Validate MVP before proceeding to additional user stories
5. Follow incremental delivery strategy for remaining stories
6. Complete Polish phase for production readiness

**Generated**: 2026-01-01
**Total Tasks**: 53
**MVP Tasks**: 21 (Setup + Foundational + US1)
**File Paths**: All tasks include specific file paths per plan.md structure
**Acceptance Criteria**: All mapped from spec.md user stories
