from abc import ABC, abstractmethod
from typing import List, Optional
from .task import Task


class Storage(ABC):
    """
    Abstract storage interface that defines the methods for task persistence.
    Allows switching between different storage implementations (in-memory, SQLite, etc.)
    """

    @abstractmethod
    def save_task(self, task: Task) -> Task:
        """Persist a task and return the saved task"""
        pass

    @abstractmethod
    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by ID"""
        pass

    @abstractmethod
    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks"""
        pass

    @abstractmethod
    def update_task(self, task_id: str, updates: dict) -> Optional[Task]:
        """Update a task"""
        pass

    @abstractmethod
    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID (returns success status)"""
        pass

    @abstractmethod
    def clear_all_tasks(self) -> bool:
        """Remove all tasks (returns success status)"""
        pass