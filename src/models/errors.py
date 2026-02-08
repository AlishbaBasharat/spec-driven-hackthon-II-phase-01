"""
Custom exception classes for the todo application
"""

class ValidationError(Exception):
    """
    Raised when input data doesn't meet validation requirements
    Contains specific error message about what validation failed
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


class NotFoundError(Exception):
    """
    Raised when attempting to access a non-existent task
    Contains information about the requested task ID
    """
    def __init__(self, task_id: str, message: str = None):
        self.task_id = task_id
        self.message = message or f"Task with ID {task_id} not found"
        super().__init__(self.message)


class StorageError(Exception):
    """
    Raised when storage operations fail
    Contains information about the specific failure
    """
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)