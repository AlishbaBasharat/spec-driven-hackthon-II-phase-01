"""
Main CLI application entry point.
Implements the interactive menu system and all task operations.
"""
import sys
from typing import List
from ..models.task import Task
from ..services.database_service import DatabaseService
from ..services.task_service import TaskService
from .ui import UI


class TodoApp:
    """
    Main application class that orchestrates the CLI interface,
    task services, and user interactions.
    """
    def __init__(self):
        # Initialize services
        self.database_service = DatabaseService()
        self.task_service = TaskService(self.database_service)
        self.ui = UI()

    def run(self):
        """
        Start the main application loop with the interactive menu.
        """
        self.ui.clear_screen()
        self.ui.show_message("Welcome to the Interactive CLI To-Do Application!", "bold green")

        while True:
            try:
                self.display_menu()
                choice = self.ui.get_user_input("Enter your choice (1-6) or 'q' to quit")

                if choice.lower() == 'q':
                    self.ui.show_message("Thank you for using the To-Do App. Goodbye!", "bold green")
                    break

                self.handle_menu_choice(choice)
            except KeyboardInterrupt:
                self.ui.show_message("\n\nExiting application. Goodbye!", "bold red")
                break
            except Exception as e:
                self.ui.show_error(f"An unexpected error occurred: {str(e)}")

    def display_menu(self):
        """
        Display the main menu options to the user.
        """
        self.ui.clear_screen()
        # Enhanced main menu title with better formatting
        from rich.panel import Panel
        from rich.align import Align
        from rich.text import Text

        # Create a fancy main menu title
        title_text = Text("Welcome to the Interactive CLI To-Do Application", style="bold magenta", justify="center")
        title_panel = Panel(
            Align.center(title_text),
            title="[bold blue]📋 TODO APP 📋[/bold blue]",
            title_align="left",
            border_style="bright_blue",
            padding=(1, 2)
        )
        self.ui.console.print(title_panel)

        self.ui.display_task_summary(self.task_service.get_all_tasks())
        print()  # Empty line for spacing

        menu_options = [
            "View all tasks",
            "Add a new task",
            "Update an existing task",
            "Delete a task",
            "Mark task as complete/incomplete",
            "Exit application"
        ]
        self.ui.display_menu_options(menu_options)

    def handle_menu_choice(self, choice: str):
        """
        Handle the user's menu choice and execute the corresponding action.
        """
        try:
            if choice == '1':
                self.view_all_tasks()
            elif choice == '2':
                self.add_task()
            elif choice == '3':
                self.update_task()
            elif choice == '4':
                self.delete_task()
            elif choice == '5':
                self.toggle_task_completion()
            elif choice == '6':
                self.ui.show_message("Thank you for using the To-Do App. Goodbye!", "bold green")
                sys.exit(0)
            else:
                self.ui.show_error("Invalid choice. Please enter a number between 1-6 or 'q' to quit.")
        except Exception as e:
            self.ui.show_error(f"Error processing your request: {str(e)}")

    def view_all_tasks(self):
        """
        Implement view all tasks functionality in CLI.
        Add display formatting for tasks with completion status indicators.
        Handle case where no tasks exist with appropriate message.
        """
        self.ui.clear_screen()
        self.ui.show_message("Viewing All Tasks", "bold blue")

        tasks = self.task_service.get_all_tasks()
        if not tasks:
            self.ui.show_message("No tasks found. Add some tasks to get started!", "yellow")
        else:
            self.ui.display_tasks(tasks)

        input("\nPress Enter to return to the main menu...")

    def add_task(self):
        """
        Implement add task functionality in CLI.
        Add input validation for task title (required, 1-200 chars).
        Implement optional description input.
        Generate unique ID for new tasks.
        Set default completion status to pending.
        Auto-generate creation and update timestamps.
        """
        self.ui.clear_screen()
        self.ui.show_message("Add New Task", "bold blue")

        try:
            title = self.ui.get_user_input("Enter task title (required)")
            if not title.strip():
                self.ui.show_error("Title cannot be empty.")
                input("\nPress Enter to return to the main menu...")
                return

            description = self.ui.get_user_input("Enter task description (optional, press Enter to skip)")

            # If description is empty string, set to None
            if description.strip() == "":
                description = None

            task = self.task_service.create_task(title=title, description=description)
            self.ui.show_success(f"Task '{task.title}' added successfully with ID: {task.id}")

        except Exception as e:
            self.ui.show_error(f"Failed to add task: {str(e)}")

        input("\nPress Enter to return to the main menu...")

    def update_task(self):
        """
        Implement update task functionality in CLI.
        Add ability to select task by ID or index for updating.
        Allow updating of title field with validation.
        Allow updating of description field.
        Update task's updated_at timestamp when fields are changed.
        Provide feedback when task is successfully updated.
        """
        self.ui.clear_screen()
        self.ui.show_message("Update Task", "bold blue")

        all_tasks = self.task_service.get_all_tasks()
        if not all_tasks:
            self.ui.show_message("No tasks available to update.", "yellow")
            input("\nPress Enter to return to the main menu...")
            return

        task_id = self.ui.get_task_selection(all_tasks, "Select a task to update by ID or index")
        if not task_id:
            input("\nPress Enter to return to the main menu...")
            return

        try:
            # Get the current task details
            current_task = self.task_service.get_task(task_id)
            if not current_task:
                self.ui.show_error("Task not found.")
                input("\nPress Enter to return to the main menu...")
                return

            # Get new values from user
            new_title = self.ui.get_user_input(f"Enter new title (current: '{current_task.title}', press Enter to keep current)")
            if new_title.strip() == "":
                new_title = None  # Keep current title

            new_description = self.ui.get_user_input(f"Enter new description (current: '{current_task.description or 'None'}', press Enter to keep current)")
            if new_description.strip() == "":
                new_description = None  # Keep current description or None

            # Update the task
            updated_task = self.task_service.update_task(
                task_id=task_id,
                title=new_title,
                description=new_description
            )

            if updated_task:
                self.ui.show_success(f"Task '{updated_task.title}' updated successfully!")
            else:
                self.ui.show_error("Failed to update task.")

        except Exception as e:
            self.ui.show_error(f"Failed to update task: {str(e)}")

        input("\nPress Enter to return to the main menu...")

    def delete_task(self):
        """
        Implement delete task functionality in CLI.
        Add ability to select task by ID or index for deletion.
        Add confirmation prompt to prevent accidental deletion.
        Remove task from storage.
        Provide feedback when task is successfully deleted.
        """
        self.ui.clear_screen()
        self.ui.show_message("Delete Task", "bold blue")

        all_tasks = self.task_service.get_all_tasks()
        if not all_tasks:
            self.ui.show_message("No tasks available to delete.", "yellow")
            input("\nPress Enter to return to the main menu...")
            return

        task_id = self.ui.get_task_selection(all_tasks, "Select a task to delete by ID or index")
        if not task_id:
            input("\nPress Enter to return to the main menu...")
            return

        try:
            # Confirm deletion
            task = self.task_service.get_task(task_id)
            if not task:
                self.ui.show_error("Task not found.")
                input("\nPress Enter to return to the main menu...")
                return

            confirm = self.ui.get_user_input(f"Are you sure you want to delete task '{task.title}'? (y/N)")
            if confirm.lower() in ['y', 'yes']:
                success = self.task_service.delete_task(task_id)
                if success:
                    self.ui.show_success(f"Task '{task.title}' deleted successfully!")
                else:
                    self.ui.show_error("Failed to delete task.")
            else:
                self.ui.show_message("Deletion cancelled.")

        except Exception as e:
            self.ui.show_error(f"Failed to delete task: {str(e)}")

        input("\nPress Enter to return to the main menu...")

    def toggle_task_completion(self):
        """
        Implement mark task complete/incomplete functionality in CLI.
        Add ability to select task by ID or index.
        Update task completion status in storage.
        Update task's updated_at timestamp when status changes.
        Provide feedback when task status is successfully updated.
        """
        self.ui.clear_screen()
        self.ui.show_message("Toggle Task Completion Status", "bold blue")

        all_tasks = self.task_service.get_all_tasks()
        if not all_tasks:
            self.ui.show_message("No tasks available.", "yellow")
            input("\nPress Enter to return to the main menu...")
            return

        task_id = self.ui.get_task_selection(all_tasks, "Select a task to toggle completion status")
        if not task_id:
            input("\nPress Enter to return to the main menu...")
            return

        try:
            # Get current task to check status
            current_task = self.task_service.get_task(task_id)
            if not current_task:
                self.ui.show_error("Task not found.")
                input("\nPress Enter to return to the main menu...")
                return

            # Toggle the status
            if current_task.completed:
                updated_task = self.task_service.mark_task_incomplete(task_id)
                action = "marked as incomplete"
            else:
                updated_task = self.task_service.mark_task_complete(task_id)
                action = "marked as complete"

            if updated_task:
                self.ui.show_success(f"Task '{updated_task.title}' {action} successfully!")
            else:
                self.ui.show_error("Failed to update task status.")

        except Exception as e:
            self.ui.show_error(f"Failed to toggle task status: {str(e)}")

        input("\nPress Enter to return to the main menu...")


def main():
    """
    Main entry point for the application.
    """
    app = TodoApp()
    app.run()


if __name__ == "__main__":
    main()