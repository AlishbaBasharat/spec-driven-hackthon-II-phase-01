from typing import List, Optional, Dict
from ..models.storage import Storage
from ..models.task import Task


class InMemoryStorage(Storage):
    """
    In-memory storage implementation for tasks.
    Tasks stored in a Python dictionary with task ID as key.
    Data is volatile and lost when application exits.
    Satisfies Phase I constitution requirement for in-memory storage.
    """
    def __init__(self):
        self._tasks: Dict[str, Task] = {}

    def save_task(self, task: Task) -> Task:
        """Persist a task and return the saved task"""
        self._tasks[task.id] = task
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by ID"""
        return self._tasks.get(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks"""
        return list(self._tasks.values())

    def update_task(self, task_id: str, updates: dict) -> Optional[Task]:
        """Update a task"""
        task = self.get_task(task_id)
        if task:
            # Update the task fields based on the updates dict
            for key, value in updates.items():
                if hasattr(task, key):
                    setattr(task, key, value)
            # Update the timestamp
            task.updated_at = task.updated_at  # This will trigger the model's __setattr__ if needed
            # Since we're modifying the task in place, update the timestamp explicitly
            import datetime
            task.updated_at = datetime.datetime.now()
            self._tasks[task_id] = task
            return task
        return None

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID (returns success status)"""
        if task_id in self._tasks:
            del self._tasks[task_id]
            return True
        return False

    def clear_all_tasks(self) -> bool:
        """Remove all tasks (returns success status)"""
        self._tasks.clear()
        return True