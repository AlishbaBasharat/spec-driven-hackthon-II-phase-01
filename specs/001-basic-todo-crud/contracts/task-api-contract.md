# Task API Contract

## Overview
This contract defines the interface for task management operations in the CLI To-Do application. The contract separates the interface from the implementation, allowing for different storage backends (in-memory, SQLite) while maintaining consistent behavior.

## Task Operations

### Add Task
- **Method**: `create_task(title: str, description: str = None) -> Task`
- **Input**:
  - title (required): Task title (string, 1-200 chars)
  - description (optional): Task description (string, 0-1000 chars)
- **Output**: Task object with all attributes including unique ID
- **Success**: Returns created Task object
- **Errors**:
  - ValidationError if title is invalid
  - StorageError if operation fails

### Get Task
- **Method**: `get_task(task_id: str) -> Optional[Task]`
- **Input**: task_id (string identifier)
- **Output**: Task object or None if not found
- **Success**: Returns Task object if found
- **Errors**: None (returns None for missing tasks)

### Update Task
- **Method**: `update_task(task_id: str, title: str = None, description: str = None) -> Optional[Task]`
- **Input**:
  - task_id (string identifier)
  - title (optional new title)
  - description (optional new description)
- **Output**: Updated Task object or None if task doesn't exist
- **Success**: Returns updated Task object
- **Errors**:
  - ValidationError if new values are invalid
  - NotFoundError if task_id doesn't exist

### Delete Task
- **Method**: `delete_task(task_id: str) -> bool`
- **Input**: task_id (string identifier)
- **Output**: Boolean indicating success
- **Success**: Returns True if task was deleted
- **Errors**: None (returns False if task doesn't exist)

### Mark Complete
- **Method**: `mark_task_complete(task_id: str) -> Optional[Task]`
- **Input**: task_id (string identifier)
- **Output**: Updated Task object or None if task doesn't exist
- **Success**: Returns Task object with completed = True
- **Errors**: NotFoundError if task_id doesn't exist

### Mark Incomplete
- **Method**: `mark_task_incomplete(task_id: str) -> Optional[Task]`
- **Input**: task_id (string identifier)
- **Output**: Updated Task object or None if task doesn't exist
- **Success**: Returns Task object with completed = False
- **Errors**: NotFoundError if task_id doesn't exist

### List All Tasks
- **Method**: `get_all_tasks() -> List[Task]`
- **Input**: None
- **Output**: List of all Task objects (empty list if none)
- **Success**: Returns list of all tasks
- **Errors**: None

### List Filtered Tasks
- **Method**: `get_tasks_by_status(completed: bool) -> List[Task]`
- **Input**: completed (boolean to filter by status)
- **Output**: List of matching Task objects
- **Success**: Returns list of tasks matching the status
- **Errors**: None

## Error Types

### ValidationError
- Raised when input data doesn't meet validation requirements
- Contains specific error message about what validation failed

### NotFoundError
- Raised when attempting to access a non-existent task
- Contains information about the requested task ID

### StorageError
- Raised when storage operations fail
- Contains information about the specific failure