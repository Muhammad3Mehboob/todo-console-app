# Task: T021 - Implement main entry point
# Spec: specs/001-phase1-console-app/spec.md

"""
Application entry point for the todo console app.

This module initializes the TodoManager and TodoCLI, then starts the
command loop with proper error handling.
"""

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
