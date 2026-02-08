"""
Database service abstraction layer.
Currently uses SQLite storage for persistence.
Can be extended to support other storage mechanisms.
"""
from typing import List, Optional
from ..models.task import Task
from ..models.storage import Storage
from .in_memory_storage import InMemoryStorage
from .sqlite_storage import SQLiteStorage


class DatabaseService:
    """
    Service class that handles database operations using the storage abstraction.
    Currently configured to use SQLite storage for persistence.
    """
    def __init__(self, storage: Storage = None):
        self.storage = storage or SQLiteStorage()

    def save_task(self, task: Task) -> Task:
        """Save a task to storage"""
        return self.storage.save_task(task)

    def get_task(self, task_id: str) -> Optional[Task]:
        """Get a specific task by ID"""
        return self.storage.get_task(task_id)

    def get_all_tasks(self) -> List[Task]:
        """Get all tasks"""
        return self.storage.get_all_tasks()

    def update_task(self, task_id: str, updates: dict) -> Optional[Task]:
        """Update a task with the provided updates"""
        return self.storage.update_task(task_id, updates)

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID"""
        return self.storage.delete_task(task_id)

    def clear_all_tasks(self) -> bool:
        """Clear all tasks"""
        return self.storage.clear_all_tasks()