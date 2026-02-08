"""
Task service that implements all required task operations:
create_task, get_task, update_task, delete_task, mark_task_complete,
mark_task_incomplete, get_all_tasks, get_tasks_by_status
"""
from typing import List, Optional
from datetime import datetime
import uuid
from ..models.task import Task
from ..models.errors import ValidationError, NotFoundError
from .database_service import DatabaseService


class TaskService:
    """
    Business logic layer for task operations.
    Handles all task management functionality with validation and error handling.
    """
    def __init__(self, database_service: DatabaseService):
        self.database_service = database_service

    def create_task(self, title: str, description: str = None) -> Task:
        """
        Create a new task with the given title and optional description.
        Title is required and must be valid.
        """
        # Validate inputs
        if not title or not title.strip():
            raise ValidationError("Title cannot be empty or contain only whitespace")

        if len(title.strip()) > 200:
            raise ValidationError("Title must be 200 characters or less")

        if description and len(description) > 1000:
            raise ValidationError("Description must be 1000 characters or less")

        # Create task with provided details
        task_data = {
            "id": str(uuid.uuid4()),  # Generate unique ID
            "title": title.strip(),
            "description": description,
            "completed": False,  # Default to pending
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }

        task = Task(**task_data)
        return self.database_service.save_task(task)

    def get_task(self, task_id: str) -> Optional[Task]:
        """
        Retrieve a task by its ID.
        Returns None if task doesn't exist.
        """
        return self.database_service.get_task(task_id)

    def update_task(self, task_id: str, title: str = None, description: str = None) -> Optional[Task]:
        """
        Update a task's title and/or description.
        Returns the updated task or None if task doesn't exist.
        """
        # Get the existing task
        task = self.database_service.get_task(task_id)
        if not task:
            raise NotFoundError(task_id)

        # Prepare updates
        updates = {}
        if title is not None:
            if not title or not title.strip():
                raise ValidationError("Title cannot be empty or contain only whitespace")

            if len(title.strip()) > 200:
                raise ValidationError("Title must be 200 characters or less")

            updates["title"] = title.strip()

        if description is not None:
            if len(description) > 1000:
                raise ValidationError("Description must be 1000 characters or less")

            updates["description"] = description

        # Update the task
        if updates:
            # Update the timestamp
            updates["updated_at"] = datetime.now()
            updated_task = self.database_service.update_task(task_id, updates)
            return updated_task

        return task

    def delete_task(self, task_id: str) -> bool:
        """
        Delete a task by its ID.
        Returns True if successful, False if task doesn't exist.
        """
        return self.database_service.delete_task(task_id)

    def mark_task_complete(self, task_id: str) -> Optional[Task]:
        """
        Mark a task as complete.
        Returns the updated task or None if task doesn't exist.
        """
        task = self.database_service.get_task(task_id)
        if not task:
            raise NotFoundError(task_id)

        # Update the task to mark as complete
        updates = {
            "completed": True,
            "updated_at": datetime.now()
        }
        return self.database_service.update_task(task_id, updates)

    def mark_task_incomplete(self, task_id: str) -> Optional[Task]:
        """
        Mark a task as incomplete.
        Returns the updated task or None if task doesn't exist.
        """
        task = self.database_service.get_task(task_id)
        if not task:
            raise NotFoundError(task_id)

        # Update the task to mark as incomplete
        updates = {
            "completed": False,
            "updated_at": datetime.now()
        }
        return self.database_service.update_task(task_id, updates)

    def get_all_tasks(self) -> List[Task]:
        """
        Retrieve all tasks.
        Returns an empty list if no tasks exist.
        """
        return self.database_service.get_all_tasks()

    def get_tasks_by_status(self, completed: bool) -> List[Task]:
        """
        Retrieve tasks filtered by completion status.
        """
        all_tasks = self.database_service.get_all_tasks()
        return [task for task in all_tasks if task.completed == completed]