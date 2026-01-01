# Implementation Quickstart: Phase I - In-Memory Console App

**Feature**: 001-phase1-console-app
**Created**: 2026-01-01
**Purpose**: Step-by-step guide for implementing Phase I from tasks

## Prerequisites

Before starting implementation:
- ✅ Specification complete ([spec.md](./spec.md))
- ✅ Architecture plan complete ([plan.md](./plan.md))
- ✅ Data model defined ([data-model.md](./data-model.md))
- ✅ Tasks generated ([tasks.md](./tasks.md)) - **Required before coding**
- ✅ Python 3.13+ installed
- ✅ UV package manager installed

## Quick Start Commands

```bash
# 1. Initialize project with UV
uv init todo-console
cd todo-console

# 2. Configure Python version
uv python pin 3.13

# 3. Create source structure
mkdir -p src/todo_app tests/unit tests/integration

# 4. Install dev dependencies
uv add --dev pytest pytest-cov

# 5. Run tests (should pass initially with no tests)
uv run pytest

# 6. Start development following tasks.md
```

## Project Structure Setup

### Step 1: Initialize Project

```bash
# Create project directory
mkdir todo-console
cd todo-console

# Initialize UV project
uv init

# Pin Python version to 3.13+
uv python pin 3.13
```

### Step 2: Create Directory Structure

```bash
# Create source package
mkdir -p src/todo_app
touch src/todo_app/__init__.py

# Create test directories
mkdir -p tests/unit tests/integration
touch tests/__init__.py
touch tests/unit/__init__.py
touch tests/integration/__init__.py

# Create placeholder files
touch src/todo_app/models.py
touch src/todo_app/manager.py
touch src/todo_app/cli.py
touch src/todo_app/main.py
```

### Step 3: Configure `pyproject.toml`

```toml
[project]
name = "todo-console"
version = "0.1.0"
description = "Phase I: In-memory console todo application"
readme = "README.md"
requires-python = ">=3.13"
dependencies = []

[project.scripts]
todo = "todo_app.main:main"

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = "test_*.py"
python_classes = "Test*"
python_functions = "test_*"
addopts = "--cov=src/todo_app --cov-report=term-missing --cov-report=html"

[tool.coverage.run]
source = ["src/todo_app"]
omit = ["tests/*", "**/__init__.py"]

[tool.coverage.report]
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise AssertionError",
    "raise NotImplementedError",
    "if __name__ == .__main__.:"
]
```

## Implementation Phases

### Phase 1: Core Data Model

**Goal**: Implement Task entity with validation

**Tasks from tasks.md**:
- Implement Task dataclass
- Add title validation (1-200 chars)
- Add `to_display_dict()` helper method
- Write unit tests for Task

**Implementation Steps**:

1. **Create `src/todo_app/models.py`**:
   ```python
   # Task: T001 - Implement Task dataclass
   # Spec: specs/001-phase1-console-app/spec.md#FR-001

   from dataclasses import dataclass, field
   from datetime import datetime


   class TodoAppError(Exception):
       """Base exception for todo app errors."""
       pass


   class ValidationError(TodoAppError):
       """Raised when task validation fails."""
       pass


   @dataclass
   class Task:
       """
       Represents a todo task.

       Attributes:
           title: Task heading (1-200 characters)
           description: Optional detailed information
           is_completed: Completion status (default: False)
           created_at: Creation timestamp (auto-assigned)
           id: Unique identifier (assigned by TodoManager)
       """
       title: str
       description: str = ""
       is_completed: bool = False
       created_at: datetime = field(default_factory=datetime.now)
       id: int = 0

       def __post_init__(self):
           """Validate title after initialization."""
           if not self.title or not self.title.strip():
               raise ValidationError(
                   "Title cannot be empty (1-200 characters required)"
               )
           if len(self.title) > 200:
               raise ValidationError("Title cannot exceed 200 characters")

       def to_display_dict(self) -> dict:
           """Convert to dictionary for CLI display."""
           status = "[X]" if self.is_completed else "[ ]"
           return {
               "id": str(self.id),
               "status": status,
               "title": self.title,
               "description": self.description or "-"
           }
   ```

2. **Create `tests/unit/test_models.py`**:
   ```python
   # Task: T002 - Write Task unit tests
   # Spec: specs/001-phase1-console-app/spec.md#AC-1

   import pytest
   from datetime import datetime
   from todo_app.models import Task, ValidationError


   def test_task_creation_minimal():
       """Test creating task with only title."""
       task = Task(title="Buy milk")
       assert task.title == "Buy milk"
       assert task.description == ""
       assert task.is_completed is False
       assert isinstance(task.created_at, datetime)
       assert task.id == 0  # Not yet assigned


   def test_task_creation_full():
       """Test creating task with all fields."""
       task = Task(
           title="Complete project",
           description="Finish documentation",
           is_completed=True,
           id=5
       )
       assert task.title == "Complete project"
       assert task.description == "Finish documentation"
       assert task.is_completed is True
       assert task.id == 5


   def test_task_title_validation_empty():
       """Test that empty title raises ValidationError."""
       with pytest.raises(ValidationError, match="cannot be empty"):
           Task(title="")


   def test_task_title_validation_whitespace():
       """Test that whitespace-only title raises ValidationError."""
       with pytest.raises(ValidationError, match="cannot be empty"):
           Task(title="   ")


   def test_task_title_validation_too_long():
       """Test that title >200 chars raises ValidationError."""
       with pytest.raises(ValidationError, match="cannot exceed 200"):
           Task(title="A" * 201)


   def test_task_title_validation_boundary():
       """Test title at exact 200 character boundary."""
       task = Task(title="A" * 200)
       assert len(task.title) == 200


   def test_task_to_display_dict_incomplete():
       """Test display dict for incomplete task."""
       task = Task(title="Buy groceries", description="Milk, eggs", id=1)
       display = task.to_display_dict()
       assert display["id"] == "1"
       assert display["status"] == "[ ]"
       assert display["title"] == "Buy groceries"
       assert display["description"] == "Milk, eggs"


   def test_task_to_display_dict_complete():
       """Test display dict for complete task."""
       task = Task(title="Call dentist", is_completed=True, id=2)
       display = task.to_display_dict()
       assert display["status"] == "[X]"


   def test_task_to_display_dict_no_description():
       """Test display dict shows '-' for empty description."""
       task = Task(title="Task", id=3)
       display = task.to_display_dict()
       assert display["description"] == "-"
   ```

3. **Run tests**:
   ```bash
   uv run pytest tests/unit/test_models.py -v
   ```

### Phase 2: Business Logic

**Goal**: Implement TodoManager with CRUD operations

**Tasks from tasks.md**:
- Implement TodoManager class with in-memory storage
- Implement add_task() with ID generation
- Implement get_all_tasks()
- Implement get_task_by_id()
- Implement update_task()
- Implement toggle_task()
- Implement delete_task()
- Write unit tests for all TodoManager methods

**Implementation Steps**:

1. **Create `src/todo_app/manager.py`**:
   ```python
   # Task: T003 - Implement TodoManager class
   # Spec: specs/001-phase1-console-app/spec.md#FR-003

   from typing import Optional
   from todo_app.models import Task, TodoAppError


   class TaskNotFoundError(TodoAppError):
       """Raised when task ID doesn't exist."""
       pass


   class TodoManager:
       """
       Manages in-memory todo task storage and operations.

       Attributes:
           _tasks: List of Task objects (in-memory storage)
           _next_id: Auto-increment counter for task IDs
       """

       def __init__(self):
           """Initialize empty task list with ID counter."""
           self._tasks: list[Task] = []
           self._next_id: int = 1

       def add_task(self, title: str, description: str = "") -> Task:
           """
           Create and store a new task with auto-assigned ID.

           Args:
               title: Task heading (1-200 characters)
               description: Optional detailed information

           Returns:
               Created Task object with assigned ID

           Raises:
               ValidationError: If title is invalid
           """
           task = Task(title=title, description=description)
           task.id = self._next_id
           self._next_id += 1
           self._tasks.append(task)
           return task

       def get_all_tasks(self) -> list[Task]:
           """
           Retrieve all tasks in creation order.

           Returns:
               List of Task objects (empty list if no tasks)
           """
           return self._tasks.copy()

       def get_task_by_id(self, task_id: int) -> Task:
           """
           Find task by ID.

           Args:
               task_id: Unique task identifier

           Returns:
               Task object

           Raises:
               TaskNotFoundError: If task ID doesn't exist
           """
           for task in self._tasks:
               if task.id == task_id:
                   return task
           raise TaskNotFoundError(f"Task ID {task_id} not found")

       def update_task(
           self,
           task_id: int,
           title: Optional[str] = None,
           description: Optional[str] = None
       ) -> Task:
           """
           Update task fields. Only provided fields are updated.

           Args:
               task_id: Unique task identifier
               title: New title (optional)
               description: New description (optional)

           Returns:
               Updated Task object

           Raises:
               TaskNotFoundError: If task ID doesn't exist
               ValidationError: If new title is invalid
           """
           task = self.get_task_by_id(task_id)

           if title is not None:
               # Create temporary task to validate title
               Task(title=title)  # Raises ValidationError if invalid
               task.title = title

           if description is not None:
               task.description = description

           return task

       def toggle_task(self, task_id: int) -> Task:
           """
           Toggle task completion status.

           Args:
               task_id: Unique task identifier

           Returns:
               Updated Task object

           Raises:
               TaskNotFoundError: If task ID doesn't exist
           """
           task = self.get_task_by_id(task_id)
           task.is_completed = not task.is_completed
           return task

       def delete_task(self, task_id: int) -> None:
           """
           Remove task from memory.

           Args:
               task_id: Unique task identifier

           Raises:
               TaskNotFoundError: If task ID doesn't exist
           """
           task = self.get_task_by_id(task_id)
           self._tasks.remove(task)
   ```

2. **Create `tests/unit/test_manager.py`** (see full test suite in tasks.md)

3. **Run tests**:
   ```bash
   uv run pytest tests/unit/test_manager.py -v
   ```

### Phase 3: CLI Interface

**Goal**: Implement command-line interface with user interaction

**Tasks from tasks.md**:
- Implement TodoCLI class with command loop
- Implement command parsing
- Implement display menu
- Implement all command handlers (add, list, update, toggle, delete)
- Implement table formatting
- Write unit tests for CLI

**Implementation Steps**:

1. **Create `src/todo_app/cli.py`** (see plan.md for complete interface)

2. **Create `tests/unit/test_cli.py`** (use mocks for input/output)

3. **Run tests**:
   ```bash
   uv run pytest tests/unit/test_cli.py -v
   ```

### Phase 4: Application Entry Point

**Goal**: Wire components together and create main entry point

**Tasks from tasks.md**:
- Implement main() function
- Add keyboard interrupt handling
- Write integration tests for full workflows

**Implementation Steps**:

1. **Create `src/todo_app/main.py`**:
   ```python
   # Task: T010 - Implement main entry point
   # Spec: specs/001-phase1-console-app/spec.md

   from todo_app.manager import TodoManager
   from todo_app.cli import TodoCLI


   def main() -> None:
       """
       Application entry point.

       Initializes TodoManager and TodoCLI, then starts command loop.
       Handles keyboard interrupts gracefully.
       """
       manager = TodoManager()
       cli = TodoCLI(manager)

       print("Welcome to Todo Console App!")
       print("Type 'help' to see available commands.\n")

       try:
           cli.run()
       except KeyboardInterrupt:
           print("\n\nExiting todo app. Goodbye!")
       except Exception as e:
           print(f"\nUnexpected error: {e}")
           print("Please report this issue.")


   if __name__ == "__main__":
       main()
   ```

2. **Create `tests/integration/test_workflows.py`**:
   ```python
   # Task: T011 - Write integration tests
   # Spec: specs/001-phase1-console-app/spec.md

   from todo_app.manager import TodoManager
   from todo_app.models import Task


   def test_complete_workflow():
       """
       Test full user journey: add → view → toggle → update → delete.

       This integration test verifies all components work together
       for the complete task lifecycle defined in spec.md.
       """
       manager = TodoManager()

       # Add task (User Story 2)
       task1 = manager.add_task("Buy groceries", "Milk, eggs, bread")
       assert task1.id == 1
       assert task1.title == "Buy groceries"
       assert task1.is_completed is False

       # View tasks (User Story 1)
       tasks = manager.get_all_tasks()
       assert len(tasks) == 1
       assert tasks[0].id == 1

       # Add more tasks
       task2 = manager.add_task("Call dentist")
       assert task2.id == 2

       # Toggle completion (User Story 3)
       updated = manager.toggle_task(1)
       assert updated.is_completed is True

       # Update task (User Story 4)
       updated = manager.update_task(2, description="Schedule cleaning")
       assert updated.description == "Schedule cleaning"
       assert updated.title == "Call dentist"  # Unchanged

       # View updated list
       tasks = manager.get_all_tasks()
       assert len(tasks) == 2
       assert tasks[0].is_completed is True  # First task complete
       assert tasks[1].is_completed is False  # Second task incomplete

       # Delete task (User Story 5)
       manager.delete_task(1)
       tasks = manager.get_all_tasks()
       assert len(tasks) == 1
       assert tasks[0].id == 2  # Only second task remains


   def test_edge_case_empty_list():
       """Test viewing tasks when list is empty."""
       manager = TodoManager()
       tasks = manager.get_all_tasks()
       assert tasks == []


   def test_edge_case_1000_tasks():
       """Test performance with 1000 tasks."""
       import time
       manager = TodoManager()

       # Add 1000 tasks
       start = time.time()
       for i in range(1000):
           manager.add_task(f"Task {i}")
       add_time = time.time() - start

       # View all tasks
       start = time.time()
       tasks = manager.get_all_tasks()
       view_time = time.time() - start

       assert len(tasks) == 1000
       assert add_time < 1.0  # SC-002: <1 second total
       assert view_time < 1.0  # SC-001: <1 second for 1000 tasks
   ```

3. **Run all tests with coverage**:
   ```bash
   uv run pytest --cov=src/todo_app --cov-report=term-missing --cov-report=html
   ```

## Running the Application

### Development Mode

```bash
# Run directly with UV
uv run python -m todo_app.main

# Or use the configured script
uv run todo
```

### Testing

```bash
# Run all tests
uv run pytest

# Run with coverage
uv run pytest --cov=src/todo_app --cov-report=term-missing

# Run specific test file
uv run pytest tests/unit/test_models.py -v

# Run integration tests only
uv run pytest tests/integration/ -v
```

### Linting

```bash
# Check PEP 8 compliance (install ruff first)
uv add --dev ruff
uv run ruff check src/

# Auto-format code
uv run ruff format src/
```

## Verification Checklist

Before considering Phase I complete, verify all acceptance criteria from spec.md:

### User Story 1 - View Tasks ✓
- [ ] Empty list shows "No tasks found."
- [ ] Tasks display with ID, status, title, description
- [ ] Status indicators are visually distinct: `[ ]` vs `[X]`
- [ ] Long titles/descriptions display properly formatted

### User Story 2 - Add Task ✓
- [ ] Can add task with title only
- [ ] Can add task with title and description
- [ ] System assigns unique auto-increment ID
- [ ] Confirmation message shows task name and ID
- [ ] Empty title shows error message
- [ ] Title >200 chars shows error message

### User Story 3 - Toggle Completion ✓
- [ ] Can mark incomplete task as complete
- [ ] Can mark complete task as incomplete
- [ ] Confirmation message shows new status
- [ ] Invalid ID shows "Task ID not found" error

### User Story 4 - Update Task ✓
- [ ] Can update title only (description unchanged)
- [ ] Can update description only (title unchanged)
- [ ] Can update both title and description
- [ ] Confirmation message shows task ID
- [ ] Invalid ID shows error
- [ ] Empty title shows error

### User Story 5 - Delete Task ✓
- [ ] Can delete existing task by ID
- [ ] Deleted task no longer appears in list
- [ ] Deleted ID cannot be accessed again
- [ ] Confirmation message shows deleted ID
- [ ] Invalid ID shows error

### Performance ✓
- [ ] View 1000 tasks completes in <1 second
- [ ] Add operation completes in <5 seconds
- [ ] Toggle operation completes in <3 seconds
- [ ] Application starts in <500ms

### Code Quality ✓
- [ ] Test coverage ≥90%
- [ ] All functions have type hints
- [ ] All public functions have docstrings
- [ ] PEP 8 compliance (no linting errors)
- [ ] All tests pass

## Troubleshooting

### Common Issues

**Issue**: `uv: command not found`
**Solution**: Install UV: `curl -LsSf https://astral.sh/uv/install.sh | sh`

**Issue**: Python 3.13 not found
**Solution**: Install Python 3.13: `uv python install 3.13`

**Issue**: Tests fail with import errors
**Solution**: Ensure you're running tests with `uv run pytest` (not plain `pytest`)

**Issue**: Coverage below 90%
**Solution**: Check coverage report (`htmlcov/index.html`) and add tests for uncovered lines

**Issue**: PEP 8 violations
**Solution**: Run `uv run ruff format src/` to auto-fix formatting issues

## Next Steps

After Phase I completion:

1. **Manual Testing**: Run through all user stories manually to verify UI/UX
2. **Documentation**: Write README.md with setup and usage instructions
3. **Git Commit**: Commit Phase I implementation with reference to tasks
4. **Demo**: Record <90 second video demonstrating all features
5. **Phase II Planning**: Begin specification for web app with persistent storage

---

**Quickstart Status**: ✅ Complete

**Related Documents**:
- [spec.md](./spec.md) - Requirements and acceptance criteria
- [plan.md](./plan.md) - Architecture and design decisions
- [data-model.md](./data-model.md) - Task entity definition
- [tasks.md](./tasks.md) - Atomic task breakdown (to be created)
