# Task: T044, T045, T046 - Integration tests for complete workflows
# Spec: specs/001-phase1-console-app/spec.md

"""
Integration tests for todo console application workflows.

Tests complete user journeys across TodoManager and TodoCLI.
"""

import pytest
from todo_app.manager import TodoManager
from todo_app.models import Task, ValidationError, TaskNotFoundError


class TestCompleteWorkflow:
    """Test complete add→view→toggle→update→delete workflow."""

    def test_complete_workflow(self):
        """Test full CRUD workflow from start to finish."""
        manager = TodoManager()

        # Start with empty list
        assert manager.get_all_tasks() == []

        # Add first task
        task1 = manager.add_task("Buy groceries", "Milk and bread")
        assert task1.id == 1
        assert task1.title == "Buy groceries"
        assert task1.description == "Milk and bread"
        assert task1.is_completed is False

        # Add second task
        task2 = manager.add_task("Call dentist")
        assert task2.id == 2
        assert task2.title == "Call dentist"
        assert task2.description == ""
        assert task2.is_completed is False

        # View all tasks
        all_tasks = manager.get_all_tasks()
        assert len(all_tasks) == 2
        assert all_tasks[0].id == 1
        assert all_tasks[1].id == 2

        # Toggle first task to complete
        toggled = manager.toggle_task(1)
        assert toggled.is_completed is True

        # Toggle back to incomplete
        toggled_again = manager.toggle_task(1)
        assert toggled_again.is_completed is False

        # Update task title
        updated = manager.update_task(1, title="Buy groceries and snacks")
        assert updated.title == "Buy groceries and snacks"
        assert updated.description == "Milk and bread"  # Description unchanged

        # Update task description
        updated2 = manager.update_task(1, description="Milk, bread, and chips")
        assert updated2.title == "Buy groceries and snacks"  # Title unchanged
        assert updated2.description == "Milk, bread, and chips"

        # Delete second task
        manager.delete_task(2)
        remaining = manager.get_all_tasks()
        assert len(remaining) == 1
        assert remaining[0].id == 1

        # Verify deleted task cannot be accessed
        with pytest.raises(TaskNotFoundError):
            manager.get_task_by_id(2)

        # Delete remaining task
        manager.delete_task(1)
        assert manager.get_all_tasks() == []


class TestEmptyListEdgeCase:
    """Test edge cases with empty task list."""

    def test_empty_list_returns_empty_array(self):
        """Empty manager should return empty list."""
        manager = TodoManager()
        assert manager.get_all_tasks() == []
        assert isinstance(manager.get_all_tasks(), list)

    def test_get_nonexistent_task_raises_error(self):
        """Getting task from empty list should raise TaskNotFoundError."""
        manager = TodoManager()
        with pytest.raises(TaskNotFoundError, match="Task ID 1 not found"):
            manager.get_task_by_id(1)

    def test_toggle_nonexistent_task_raises_error(self):
        """Toggling nonexistent task should raise TaskNotFoundError."""
        manager = TodoManager()
        with pytest.raises(TaskNotFoundError):
            manager.toggle_task(1)

    def test_update_nonexistent_task_raises_error(self):
        """Updating nonexistent task should raise TaskNotFoundError."""
        manager = TodoManager()
        with pytest.raises(TaskNotFoundError):
            manager.update_task(1, title="New title")

    def test_delete_nonexistent_task_raises_error(self):
        """Deleting nonexistent task should raise TaskNotFoundError."""
        manager = TodoManager()
        with pytest.raises(TaskNotFoundError):
            manager.delete_task(1)

    def test_add_to_empty_list_assigns_id_one(self):
        """First task added should get ID 1."""
        manager = TodoManager()
        task = manager.add_task("First task")
        assert task.id == 1


class TestLargeScalePerformance:
    """Test performance with 1000+ tasks."""

    def test_1000_tasks_operations(self):
        """Verify app handles 1000 tasks without degradation."""
        manager = TodoManager()

        # Add 1000 tasks
        for i in range(1, 1001):
            task = manager.add_task(f"Task {i}", f"Description {i}")
            assert task.id == i

        # Verify all tasks exist
        all_tasks = manager.get_all_tasks()
        assert len(all_tasks) == 1000

        # Access task in middle
        middle_task = manager.get_task_by_id(500)
        assert middle_task.title == "Task 500"
        assert middle_task.description == "Description 500"

        # Access last task
        last_task = manager.get_task_by_id(1000)
        assert last_task.title == "Task 1000"

        # Toggle multiple tasks
        for i in [1, 500, 1000]:
            toggled = manager.toggle_task(i)
            assert toggled.is_completed is True

        # Update task in middle
        updated = manager.update_task(500, title="Updated Task 500")
        assert updated.title == "Updated Task 500"

        # Delete tasks
        manager.delete_task(1)
        manager.delete_task(500)
        manager.delete_task(1000)

        remaining = manager.get_all_tasks()
        assert len(remaining) == 997

        # Verify deleted tasks cannot be accessed
        with pytest.raises(TaskNotFoundError):
            manager.get_task_by_id(1)
        with pytest.raises(TaskNotFoundError):
            manager.get_task_by_id(500)
        with pytest.raises(TaskNotFoundError):
            manager.get_task_by_id(1000)

    def test_id_sequence_continues_after_delete(self):
        """ID counter should continue even after deletes."""
        manager = TodoManager()

        # Add 3 tasks
        task1 = manager.add_task("Task 1")
        task2 = manager.add_task("Task 2")
        task3 = manager.add_task("Task 3")
        assert task1.id == 1
        assert task2.id == 2
        assert task3.id == 3

        # Delete task 2
        manager.delete_task(2)

        # Add new task - should get ID 4, not 2
        task4 = manager.add_task("Task 4")
        assert task4.id == 4

        all_tasks = manager.get_all_tasks()
        assert len(all_tasks) == 3
        assert [t.id for t in all_tasks] == [1, 3, 4]


class TestValidationEdgeCases:
    """Test validation edge cases."""

    def test_empty_title_validation(self):
        """Empty title should raise ValidationError."""
        manager = TodoManager()
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            manager.add_task("")

    def test_whitespace_only_title_validation(self):
        """Whitespace-only title should raise ValidationError."""
        manager = TodoManager()
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            manager.add_task("   ")

    def test_title_exactly_200_chars(self):
        """Title with exactly 200 characters should be valid."""
        manager = TodoManager()
        title_200 = "A" * 200
        task = manager.add_task(title_200)
        assert len(task.title) == 200

    def test_title_201_chars_validation(self):
        """Title with 201 characters should raise ValidationError."""
        manager = TodoManager()
        title_201 = "A" * 201
        with pytest.raises(ValidationError, match="Title cannot exceed 200 characters"):
            manager.add_task(title_201)

    def test_update_to_empty_title_validation(self):
        """Updating to empty title should raise ValidationError."""
        manager = TodoManager()
        task = manager.add_task("Valid title")
        with pytest.raises(ValidationError, match="Title cannot be empty"):
            manager.update_task(task.id, title="")

    def test_update_to_long_title_validation(self):
        """Updating to >200 char title should raise ValidationError."""
        manager = TodoManager()
        task = manager.add_task("Valid title")
        long_title = "A" * 201
        with pytest.raises(ValidationError, match="Title cannot exceed 200 characters"):
            manager.update_task(task.id, title=long_title)

    def test_optional_description_can_be_empty(self):
        """Description can be empty or omitted."""
        manager = TodoManager()
        task1 = manager.add_task("Task with no description")
        assert task1.description == ""

        task2 = manager.add_task("Task with description", "Some description")
        assert task2.description == "Some description"
