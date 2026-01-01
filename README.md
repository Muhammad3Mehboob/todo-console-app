# Todo Console App

Phase I: In-memory console todo application built with Python 3.13+ and UV.

## Features

- ✅ **View Tasks**: Display all tasks in formatted table
- ✅ **Add Tasks**: Create new tasks with title and optional description
- ✅ **Toggle Completion**: Mark tasks as complete or incomplete
- ✅ **Update Tasks**: Modify task title and/or description
- ✅ **Delete Tasks**: Remove tasks from list
- ✅ **Input Validation**: Title validation (1-200 characters required)
- ✅ **Error Handling**: Clear error messages for invalid operations
- ✅ **In-Memory Storage**: Volatile storage (tasks lost on exit)

## Requirements

- **Python**: 3.13 or higher
- **UV**: Python package manager ([installation guide](https://github.com/astral-sh/uv))

## Installation

1. **Navigate to project directory**:
   ```bash
   cd todo-console
   ```

2. **Install package in development mode**:
   ```bash
   uv pip install -e .
   ```

## Usage

### Launch the application:
```bash
uv run todo
```

### Available Commands:

- **`list`** - View all tasks in formatted table
- **`add`** - Add a new task (prompts for title and description)
- **`toggle`** - Toggle task completion status (prompts for task ID)
- **`update`** - Update task details (prompts for task ID and new values)
- **`delete`** - Delete a task (prompts for task ID)
- **`help`** - Show available commands
- **`exit`** - Exit the application

### Example Session:

```
Welcome to Todo Console App!
Type 'help' to see available commands.

todo> add
Enter task title: Buy groceries
Enter description (optional): Milk and bread
[SUCCESS] Task 'Buy groceries' added with ID 1

todo> add
Enter task title: Call dentist
Enter description (optional):
[SUCCESS] Task 'Call dentist' added with ID 2

todo> list
ID  | Status | Title                    | Description
----------------------------------------------------------------------
1   | [ ]    | Buy groceries            | Milk and bread
2   | [ ]    | Call dentist             | -

todo> toggle
Enter task ID to toggle: 1
[SUCCESS] Task 1 marked as Complete

todo> list
ID  | Status | Title                    | Description
----------------------------------------------------------------------
1   | [X]    | Buy groceries            | Milk and bread
2   | [ ]    | Call dentist             | -

todo> update
Enter task ID to update: 2

Current title: Call dentist
Current description: (none)

Enter new title (press Enter to keep current):
Enter new description (press Enter to keep current): Schedule for next week
[SUCCESS] Task 2 updated

todo> delete
Enter task ID to delete: 1
[SUCCESS] Task 1 deleted

todo> list
ID  | Status | Title                    | Description
----------------------------------------------------------------------
2   | [ ]    | Call dentist             | Schedule for next week

todo> exit
Goodbye!
```

## Development

### Run Tests:
```bash
uv run pytest
```

### Run Tests with Coverage:
```bash
uv run pytest --cov=src/todo_app --cov-report=term-missing
```

### Run Integration Tests Only:
```bash
uv run pytest tests/integration/
```

### Run with Verbose Output:
```bash
uv run pytest -v
```

## Project Structure

```
todo-console/
├── src/
│   └── todo_app/
│       ├── __init__.py
│       ├── models.py       # Task dataclass and exceptions
│       ├── manager.py      # TodoManager (business logic)
│       ├── cli.py          # TodoCLI (user interface)
│       └── main.py         # Application entry point
├── tests/
│   ├── unit/               # Unit tests (not implemented)
│   └── integration/
│       └── test_workflows.py  # Integration tests
├── pyproject.toml          # Project configuration
├── README.md               # This file
└── .gitignore              # Git ignore patterns
```

## Architecture

### Components:

1. **`models.py`**: Data models and exceptions
   - `Task` dataclass with validation
   - Custom exceptions: `ValidationError`, `TaskNotFoundError`

2. **`manager.py`**: Business logic (TodoManager)
   - In-memory task storage (list)
   - CRUD operations: add, get, toggle, update, delete
   - Auto-incrementing ID assignment

3. **`cli.py`**: User interface (TodoCLI)
   - Command loop and input handling
   - Formatted table display
   - Success/error message display

4. **`main.py`**: Application entry point
   - Initializes manager and CLI
   - Error handling (KeyboardInterrupt, exceptions)

### Data Model:

```python
@dataclass
class Task:
    title: str              # 1-200 characters (required)
    description: str        # Optional
    is_completed: bool      # Default: False
    created_at: datetime    # Auto-assigned
    id: int                 # Auto-assigned by TodoManager
```

## Validation Rules

- **Title**: Required, 1-200 characters
- **Description**: Optional, no length limit
- **Task ID**: Must exist in current task list

## Error Messages

- `[ERROR] Title cannot be empty (1-200 characters required)`
- `[ERROR] Title cannot exceed 200 characters`
- `[ERROR] Task ID not found`
- `[ERROR] Invalid task ID. Please enter a number.`
- `[ERROR] No changes made. Both fields were empty.`

## Success Messages

- `[SUCCESS] Task '[title]' added with ID [N]`
- `[SUCCESS] Task [N] marked as Complete/Incomplete`
- `[SUCCESS] Task [N] updated`
- `[SUCCESS] Task [N] deleted`

## Limitations (Phase I)

- **Volatile Storage**: Tasks are stored in memory only and lost on exit
- **No Persistence**: No database or file storage
- **No Filtering**: Cannot filter by status or search
- **No Sorting**: Tasks displayed in creation order only
- **No Categories**: No tags or categories
- **Single User**: No multi-user support

## Future Phases

- **Phase II**: Web interface with database persistence
- **Phase III**: AI chatbot integration
- **Phase IV**: Kubernetes deployment
- **Phase V**: Cloud infrastructure

## Technical Specifications

- **Python Version**: 3.13+
- **Package Manager**: UV
- **Testing Framework**: pytest
- **Code Coverage Target**: 90%
- **Code Style**: PEP 8

## License

See project root for license information.

## Support

For issues or questions, please refer to the project specification at:
`specs/001-phase1-console-app/spec.md`
