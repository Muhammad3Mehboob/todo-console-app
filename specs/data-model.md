# Data Model: Phase I - In-Memory Console App

**Feature**: 001-phase1-console-app
**Created**: 2026-01-01
**Status**: Design Complete

## Overview

Phase I requires a single entity: **Task**. This document defines the Task entity structure, validation rules, state transitions, and relationships (none in Phase I, prepared for future phases).

## Entities

### Task

**Purpose**: Represents a single todo item that users can create, view, update, complete, and delete.

**Attributes**:

| Attribute      | Type     | Required | Default | Validation | Description |
|:---------------|:---------|:---------|:--------|:-----------|:------------|
| `id`           | int      | Yes      | Auto    | Positive integer | Unique identifier assigned by TodoManager |
| `title`        | str      | Yes      | -       | 1-200 chars | Short descriptive text for the task |
| `description`  | str      | No       | ""      | No limit | Detailed information about the task |
| `is_completed` | bool     | Yes      | False   | True/False | Completion status indicator |
| `created_at`   | datetime | Yes      | Auto    | Valid datetime | Timestamp of task creation |

**Validation Rules**:

1. **Title Validation**:
   - MUST be 1-200 characters (inclusive)
   - MUST NOT be empty string or whitespace-only
   - CAN contain any printable characters (unicode supported)
   - Enforced in `Task.__post_init__` method

2. **Description Validation**:
   - No length restrictions
   - Optional (empty string if not provided)
   - CAN contain any printable characters including newlines

3. **ID Validation**:
   - MUST be positive integer (≥1)
   - MUST be unique within session
   - Assigned by TodoManager, not by user input
   - Auto-incremented starting from 1

4. **Status Validation**:
   - MUST be boolean (True for complete, False for incomplete)
   - Defaults to False for new tasks

5. **Timestamp Validation**:
   - MUST be valid datetime object
   - Auto-assigned at creation time
   - Immutable after creation

**State Transitions**:

```
┌─────────────┐
│   [Create]  │
│  id=None    │
└──────┬──────┘
       │
       ↓ TodoManager.add_task()
┌─────────────────────────────┐
│  [Stored in Memory]         │
│  id=1 (auto-assigned)       │
│  is_completed=False         │
│  created_at=now()           │
└──────┬──────────────────────┘
       │
       ├─→ View (no state change)
       │
       ├─→ Update title/description
       │   └→ [Stored in Memory] (modified fields)
       │
       ├─→ Toggle completion
       │   ├→ is_completed=True
       │   └→ is_completed=False (repeatable)
       │
       └─→ Delete
           └→ [Removed from Memory]
```

**State Invariants**:
- Once assigned, ID never changes
- created_at timestamp never changes
- is_completed can toggle between True/False any number of times
- title/description can be updated any number of times
- After deletion, task no longer accessible (ID not reused)

**Relationships**:

Phase I: **None** (single-user, no relationships)

Future Phases (design preview):
- Phase II: `user_id` foreign key → User entity (multi-user support)
- Phase III: `conversation_id` foreign key → Conversation entity (chatbot context)
- Later: `category_id`, `tag_ids` for organization

## Implementation Notes

### Python Dataclass Implementation

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class Task:
    """
    Represents a todo task with title, description, and completion status.

    Attributes:
        title: Short heading for the task (1-200 characters)
        description: Detailed information (optional)
        is_completed: Completion status (default: False)
        created_at: Timestamp of creation (auto-assigned)
        id: Unique identifier (assigned by TodoManager)

    Raises:
        ValidationError: If title is invalid (empty or >200 chars)
    """
    title: str
    description: str = ""
    is_completed: bool = False
    created_at: datetime = field(default_factory=datetime.now)
    id: int = 0  # Assigned by TodoManager after creation

    def __post_init__(self):
        """Validate title length after initialization."""
        if not self.title or not self.title.strip():
            raise ValidationError("Title cannot be empty (1-200 characters required)")
        if len(self.title) > 200:
            raise ValidationError("Title cannot exceed 200 characters")

    def to_display_dict(self) -> dict:
        """
        Convert task to dictionary format for CLI display.

        Returns:
            Dictionary with formatted fields for table display
        """
        status_indicator = "[X]" if self.is_completed else "[ ]"
        return {
            "id": str(self.id),
            "status": status_indicator,
            "title": self.title,
            "description": self.description or "-"
        }
```

### Storage Structure

**In-Memory Representation** (Phase I):

```python
class TodoManager:
    def __init__(self):
        self._tasks: list[Task] = []  # Ordered list of tasks
        self._next_id: int = 1         # Auto-increment counter
```

**Storage Characteristics**:
- Linear list structure: `[Task1, Task2, Task3, ...]`
- Insertion order preserved (natural chronological ordering)
- Lookup by ID: O(n) linear search (acceptable for 1000 tasks)
- Iteration: O(n) single pass
- Memory overhead: ~1KB per task → ~1MB for 1000 tasks

**Future Storage Evolution**:

Phase II (PostgreSQL):
```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(200) NOT NULL,
    description TEXT,
    is_completed BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT NOW(),
    user_id INTEGER REFERENCES users(id)
);
```

## Indexing Strategy (Future)

Phase I: No indexes needed (in-memory list)

Phase II+:
- Primary index: `id` (auto-generated)
- Secondary index: `user_id` (for multi-user filtering)
- Optional index: `created_at` (for chronological queries)
- Optional index: `is_completed` (for filtering complete/incomplete)

## Data Constraints Summary

**Hard Constraints** (enforced by code):
1. Title length: 1-200 characters
2. ID uniqueness: Guaranteed by auto-increment
3. ID immutability: Never changes after assignment
4. Timestamp immutability: created_at never changes

**Soft Constraints** (recommendations):
1. Keep descriptions under 1000 characters for display readability
2. Limit total tasks to 1000 for optimal performance

## Data Migration Path

### Phase I → Phase II

**Changes Required**:
1. Add `user_id` field to Task
2. Convert in-memory list to database table
3. Replace auto-increment counter with database SERIAL
4. Add foreign key constraint to users table

**Backward Compatibility**:
- Existing Task structure remains valid
- New fields added as nullable initially
- Migration script to assign user_id to existing tasks

**Data Preservation**:
- Phase I data is volatile (lost on exit) - no migration needed
- Phase II starts fresh with persistent storage

### Phase II → Phase III

**Changes Required**:
1. Add `conversation_id` field (nullable, for chatbot context)
2. Optional: Add `due_date` field if specified in Phase III spec
3. Optional: Add `priority` field if specified in Phase III spec

## Validation Error Handling

**ValidationError Exception**:

```python
class ValidationError(TodoAppError):
    """Raised when task data fails validation rules."""
    pass
```

**Error Messages**:
- Empty title: `"Title cannot be empty (1-200 characters required)"`
- Title too long: `"Title cannot exceed 200 characters"`

**Error Handling Flow**:
1. Task validation fails in `__post_init__`
2. ValidationError raised with descriptive message
3. TodoManager catches and re-raises (no additional handling)
4. CLI catches and displays user-friendly error message

## Test Data Examples

**Valid Tasks**:

```python
# Minimal task
Task(title="Buy milk", id=1)

# Full task
Task(
    title="Complete project documentation",
    description="Write README, API docs, and architecture guide",
    is_completed=False,
    created_at=datetime(2026, 1, 1, 10, 30),
    id=1
)

# Completed task
Task(title="Call dentist", is_completed=True, id=2)

# Task with special characters
Task(title="Review O'Reilly's \"Python Mastery\" book", id=3)

# Task with unicode
Task(title="学习中文 (Learn Chinese)", id=4)
```

**Invalid Tasks** (raise ValidationError):

```python
# Empty title
Task(title="")  # ValidationError: Title cannot be empty

# Whitespace-only title
Task(title="   ")  # ValidationError: Title cannot be empty

# Title too long
Task(title="A" * 201)  # ValidationError: Title cannot exceed 200 characters
```

## Entity Diagram

```
┌───────────────────────────────────┐
│           Task                     │
├───────────────────────────────────┤
│ + id: int (PK)                    │
│ + title: str (1-200 chars)        │
│ + description: str (optional)     │
│ + is_completed: bool (default: F) │
│ + created_at: datetime (auto)     │
├───────────────────────────────────┤
│ + to_display_dict() -> dict       │
└───────────────────────────────────┘

Phase I: No relationships

Future Phases:
           ┌───────────┐
           │   User    │ (Phase II)
           └─────┬─────┘
                 │ 1
                 │
                 │ *
           ┌─────▼─────┐
           │   Task    │
           └─────┬─────┘
                 │ *
                 │
                 │ 1
           ┌─────▼────────────┐
           │ Conversation     │ (Phase III)
           └──────────────────┘
```

---

**Data Model Status**: ✅ Complete

**Next Steps**:
- Implement Task dataclass in `src/todo_app/models.py`
- Write unit tests for validation rules
- Implement TodoManager with ID generation logic
