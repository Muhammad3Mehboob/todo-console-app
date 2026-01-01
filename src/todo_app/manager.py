# Task: T010-T013, T030, T035, T040 - Implement TodoManager with CRUD operations
# Spec: specs/001-phase1-console-app/spec.md#FR-002, FR-003, FR-008, FR-009, FR-010, FR-011

"""
Business logic for todo task management.

This module implements the TodoManager class which handles in-memory
task storage and CRUD operations.
"""

from typing import Optional
from todo_app.models import Task, TaskNotFoundError, ValidationError


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

    def update_task(
        self, task_id: int, title: Optional[str] = None, description: Optional[str] = None
    ) -> Task:
        """
        Update task title and/or description.

        Args:
            task_id: Unique task identifier
            title: New title (None to keep current)
            description: New description (None to keep current)

        Returns:
            Updated Task object

        Raises:
            TaskNotFoundError: If task ID doesn't exist
            ValidationError: If new title is invalid
        """
        task = self.get_task_by_id(task_id)

        if title is not None:
            # Validate new title by attempting to create a temporary task
            if not title or not title.strip():
                raise ValidationError(
                    "Title cannot be empty (1-200 characters required)"
                )
            if len(title) > 200:
                raise ValidationError("Title cannot exceed 200 characters")
            task.title = title

        if description is not None:
            task.description = description

        return task

    def delete_task(self, task_id: int) -> None:
        """
        Delete task from memory.

        Args:
            task_id: Unique task identifier

        Raises:
            TaskNotFoundError: If task ID doesn't exist
        """
        task = self.get_task_by_id(task_id)
        self._tasks.remove(task)
