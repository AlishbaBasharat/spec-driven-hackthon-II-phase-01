"""
UI components for the CLI application using rich for formatting and displaying tasks.
Implements task display functions with color coding for completed/pending tasks.
"""
from typing import List
from rich.console import Console
from rich.table import Table
from rich.text import Text
from rich.prompt import Prompt
from rich.panel import Panel
from rich import print
from ..models.task import Task


class UI:
    """
    UI components for displaying tasks and interacting with the user.
    Uses rich library for formatting and visual appeal.
    """
    def __init__(self):
        self.console = Console(force_terminal=True)

    def display_tasks(self, tasks: List[Task]):
        """
        Display a list of tasks with color coding for completion status.
        Shows clear visual indicators for completed and pending tasks.
        """
        if not tasks:
            self.console.print("[yellow]No tasks found.[/yellow]")
            return

        table = Table(title="Task List", show_header=True, header_style="bold magenta")
        table.add_column("ID", style="dim", width=38)  # UUID length
        table.add_column("Title", min_width=15)
        table.add_column("Description", min_width=20)
        table.add_column("Status", justify="center")
        table.add_column("Created", justify="center")

        for task in tasks:
            status = "[green]✓ Completed[/green]" if task.completed else "[red]○ Pending[/red]"
            description = task.description if task.description else "[italic dim]No description[/italic dim]"

            table.add_row(
                task.id,
                task.title,
                description,
                status,
                task.created_at.strftime("%Y-%m-%d %H:%M")
            )

        self.console.print(table)

    def display_task_summary(self, all_tasks: List[Task]):
        """
        Display a summary of task statistics.
        """
        total = len(all_tasks)
        completed = len([t for t in all_tasks if t.completed])
        pending = total - completed
        
        summary_text = f"[bold]Task Summary:[/bold] Total: {total}, Completed: {completed}, Pending: {pending}"
        self.console.print(Panel(summary_text))

    def get_user_input(self, prompt_text: str, default: str = None) -> str:
        """
        Get input from the user with a styled prompt.
        """
        if default:
            return Prompt.ask(f"[bold blue]{prompt_text}[/bold blue]", default=default)
        else:
            return Prompt.ask(f"[bold blue]{prompt_text}[/bold blue]")

    def get_task_selection(self, tasks: List[Task], prompt_text: str = "Select a task by ID or index") -> str:
        """
        Allow user to select a task from the list.
        """
        if not tasks:
            self.console.print("[yellow]No tasks available to select.[/yellow]")
            return None

        self.display_tasks(tasks)
        task_ids = [task.id for task in tasks]

        while True:
            selection = self.get_user_input(f"{prompt_text} (Enter ID or index 1-{len(tasks)}, or 'q' to quit)")

            if selection.lower() == 'q':
                return None

            # Check if it's an index
            try:
                index = int(selection) - 1
                if 0 <= index < len(tasks):
                    return tasks[index].id
            except ValueError:
                pass

            # Check if it's a valid ID
            if selection in task_ids:
                return selection

            self.console.print("[red]Invalid selection. Please try again.[/red]")

    def show_message(self, message: str, style: str = "green"):
        """
        Display a styled message to the user.
        """
        self.console.print(f"[{style}]{message}[/{style}]")

    def show_error(self, error_message: str):
        """
        Display an error message to the user.
        """
        self.console.print(f"[red]Error: {error_message}[/red]")

    def show_success(self, success_message: str):
        """
        Display a success message to the user.
        """
        self.console.print(f"[green]✓ {success_message}[/green]")

    def clear_screen(self):
        """
        Clear the console screen.
        """
        self.console.clear()

    def display_menu_options(self, options: List[str]):
        """
        Display menu options in a formatted way.
        """
        self.console.print("[bold]Menu Options[/bold]")
        for i, option in enumerate(options, 1):
            self.console.print(f"[cyan]{i}.[/cyan] {option}")
        self.console.print("-" * 50)