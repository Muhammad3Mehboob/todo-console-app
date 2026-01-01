# Task: T016-T021, T024-T028, T031-T033, T036-T038, T041-T043 - Implement TodoCLI for User Stories 1-5
# Spec: specs/001-phase1-console-app/spec.md#FR-001, FR-004, FR-005, FR-006, FR-007, FR-008, FR-009, FR-010, FR-012

"""
Command-line interface for the todo console application.

This module implements the TodoCLI class which handles user interaction,
command parsing, and output formatting.
"""

from todo_app.manager import TodoManager
from todo_app.models import Task, ValidationError, TaskNotFoundError


class TodoCLI:
    """
    CLI interface for todo task management.

    Attributes:
        manager: TodoManager instance for business logic
    """

    def __init__(self, manager: TodoManager):
        """
        Initialize CLI with TodoManager.

        Args:
            manager: TodoManager instance
        """
        self.manager = manager

    def format_task_table(self, tasks: list[Task]) -> str:
        """
        Format tasks as readable table.

        Args:
            tasks: List of Task objects to display

        Returns:
            Formatted string table or "No tasks found." message
        """
        if not tasks:
            return "No tasks found."

        lines = []
        lines.append("ID  | Status | Title                    | Description")
        lines.append("-" * 70)

        for task in tasks:
            display = task.to_display_dict()
            # Truncate long titles/descriptions for display
            title_display = display["title"][:24].ljust(24)
            desc_display = display["description"][:30] if display["description"] != "-" else "-"

            line = f"{display['id']:3} | {display['status']:6} | {title_display} | {desc_display}"
            lines.append(line)

        return "\n".join(lines)

    def handle_list(self) -> None:
        """Display all tasks in formatted table."""
        tasks = self.manager.get_all_tasks()
        output = self.format_task_table(tasks)
        print(output)

    def display_menu(self) -> None:
        """Show available commands."""
        menu = """
Todo Console App - Available Commands:
  list   - View all tasks
  add    - Add a new task
  toggle - Toggle task completion status
  update - Update task details
  delete - Delete a task
  exit   - Exit the application
"""
        print(menu)

    def display_success(self, message: str) -> None:
        """Display success message to user."""
        print(f"[SUCCESS] {message}")

    def display_error(self, message: str) -> None:
        """Display error message to user."""
        print(f"[ERROR] {message}")

    def handle_add(self) -> None:
        """Prompt for task details and add new task."""
        try:
            title = input("Enter task title: ").strip()
            description = input("Enter description (optional): ").strip()

            task = self.manager.add_task(title, description)
            self.display_success(f"Task '{task.title}' added with ID {task.id}")
        except ValidationError as e:
            self.display_error(str(e))

    def handle_toggle(self) -> None:
        """Prompt for task ID and toggle completion status."""
        try:
            task_id_str = input("Enter task ID to toggle: ").strip()
            task_id = int(task_id_str)

            task = self.manager.toggle_task(task_id)
            status = "Complete" if task.is_completed else "Incomplete"
            self.display_success(f"Task {task.id} marked as {status}")
        except ValueError:
            self.display_error("Invalid task ID. Please enter a number.")
        except TaskNotFoundError as e:
            self.display_error(str(e))

    def handle_update(self) -> None:
        """Prompt for task ID and fields to update."""
        try:
            task_id_str = input("Enter task ID to update: ").strip()
            task_id = int(task_id_str)

            # Get current task to show current values
            current_task = self.manager.get_task_by_id(task_id)
            print(f"\nCurrent title: {current_task.title}")
            print(f"Current description: {current_task.description or '(none)'}\n")

            new_title = input("Enter new title (press Enter to keep current): ").strip()
            new_description = input("Enter new description (press Enter to keep current): ").strip()

            # Only update if something was entered
            title_update = new_title if new_title else None
            desc_update = new_description if new_description else None

            if title_update is None and desc_update is None:
                self.display_error("No changes made. Both fields were empty.")
                return

            self.manager.update_task(task_id, title=title_update, description=desc_update)
            self.display_success(f"Task {task_id} updated")
        except ValueError:
            self.display_error("Invalid task ID. Please enter a number.")
        except (TaskNotFoundError, ValidationError) as e:
            self.display_error(str(e))

    def handle_delete(self) -> None:
        """Prompt for task ID and delete task."""
        try:
            task_id_str = input("Enter task ID to delete: ").strip()
            task_id = int(task_id_str)

            self.manager.delete_task(task_id)
            self.display_success(f"Task {task_id} deleted")
        except ValueError:
            self.display_error("Invalid task ID. Please enter a number.")
        except TaskNotFoundError as e:
            self.display_error(str(e))

    def run(self) -> None:
        """
        Main command loop.

        This is the entry point for the CLI application.
        Processes user commands until 'exit' is entered.
        """
        while True:
            command = input("\ntodo> ").strip().lower()

            if command == "list":
                self.handle_list()
            elif command == "add":
                self.handle_add()
            elif command == "toggle":
                self.handle_toggle()
            elif command == "update":
                self.handle_update()
            elif command == "delete":
                self.handle_delete()
            elif command == "exit":
                print("Goodbye!")
                break
            elif command == "help":
                self.display_menu()
            else:
                print(f"Unknown command: '{command}'. Type 'help' for available commands.")
