from typing import List, Optional
from .task import Task


class TaskList:
    """
    Collection of Task entities that supports add, view, update, delete,
    and mark complete operations
    """
    def __init__(self):
        self.tasks: List[Task] = []

    def add_task(self, task: Task) -> Task:
        """Add a new task to the collection"""
        self.tasks.append(task)
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a specific task by ID"""
        for task in self.tasks:
            if task.id == task_id:
                return task
        return None

    def update_task(self, task_id: str, updates: dict) -> Optional[Task]:
        """Update task properties"""
        task = self.get_task(task_id)
        if task:
            task.update(**updates)
            return task
        return None

    def delete_task(self, task_id: str) -> bool:
        """Remove a task from the collection"""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            return True
        return False

    def mark_complete(self, task_id: str) -> Optional[Task]:
        """Mark a task as complete"""
        task = self.get_task(task_id)
        if task:
            task.mark_complete()
            return task
        return None

    def mark_incomplete(self, task_id: str) -> Optional[Task]:
        """Mark a task as incomplete"""
        task = self.get_task(task_id)
        if task:
            task.mark_incomplete()
            return task
        return None

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks"""
        return self.tasks

    def get_pending_tasks(self) -> List[Task]:
        """Retrieve only pending tasks"""
        return [task for task in self.tasks if not task.completed]

    def get_completed_tasks(self) -> List[Task]:
        """Retrieve only completed tasks"""
        return [task for task in self.tasks if task.completed]

    @property
    def total_count(self) -> int:
        """Total number of tasks in the collection"""
        return len(self.tasks)

    @property
    def completed_count(self) -> int:
        """Number of completed tasks"""
        return len(self.get_completed_tasks())

    @property
    def pending_count(self) -> int:
        """Number of pending tasks"""
        return len(self.get_pending_tasks())