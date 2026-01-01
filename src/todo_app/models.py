# Task: T007, T008, T009 - Implement Task model with exceptions and validation
# Spec: specs/001-phase1-console-app/spec.md#FR-001, FR-002, FR-012

"""
Data models for the todo console application.

This module defines the Task entity and custom exceptions for the application.
"""

from dataclasses import dataclass, field
from datetime import datetime


class TodoAppError(Exception):
    """Base exception for todo app errors."""
    pass


class ValidationError(TodoAppError):
    """Raised when task validation fails."""
    pass


class TaskNotFoundError(TodoAppError):
    """Raised when task ID doesn't exist."""
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

    Raises:
        ValidationError: If title is invalid (empty or >200 chars)
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
        """
        Convert to dictionary for CLI display.

        Returns:
            Dictionary with formatted fields for table display
        """
        status = "[X]" if self.is_completed else "[ ]"
        return {
            "id": str(self.id),
            "status": status,
            "title": self.title,
            "description": self.description or "-"
        }
