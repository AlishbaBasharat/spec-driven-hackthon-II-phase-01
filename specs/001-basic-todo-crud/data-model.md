# Data Model: Interactive CLI To-Do Application

## Task Entity

### Attributes
- **id** (str): Unique identifier for the task (UUID string format)
- **title** (str): Required title of the task (min length: 1, max length: 200)
- **description** (str): Optional detailed description of the task (max length: 1000)
- **completed** (bool): Status indicator showing if task is completed (default: False)
- **created_at** (datetime): Timestamp when task was created (auto-generated)
- **updated_at** (datetime): Timestamp when task was last modified (auto-updated)

### Validation Rules
- Title must not be empty or contain only whitespace
- Title length must be between 1 and 200 characters
- Description length must not exceed 1000 characters
- ID must be unique within the system
- created_at and updated_at must be valid ISO 8601 datetime strings

### State Transitions
- **Pending → Completed**: When user marks task as complete
- **Completed → Pending**: When user marks task as incomplete

## TaskList Collection

### Attributes
- **tasks** (List[Task]): Collection of Task entities
- **total_count** (int): Total number of tasks in the collection
- **completed_count** (int): Number of completed tasks
- **pending_count** (int): Number of pending tasks

### Operations
- **add_task(task: Task)**: Add a new task to the collection
- **get_task(task_id: str)**: Retrieve a specific task by ID
- **update_task(task_id: str, updates: dict)**: Update task properties
- **delete_task(task_id: str)**: Remove a task from the collection
- **mark_complete(task_id: str)**: Mark a task as complete
- **mark_incomplete(task_id: str)**: Mark a task as incomplete
- **get_all_tasks()**: Retrieve all tasks
- **get_pending_tasks()**: Retrieve only pending tasks
- **get_completed_tasks()**: Retrieve only completed tasks

## Storage Interface

### Abstract Methods
- **save_task(task: Task) -> Task**: Persist a task and return the saved task
- **get_task(task_id: str) -> Optional[Task]**: Retrieve a task by ID
- **get_all_tasks() -> List[Task]**: Retrieve all tasks
- **update_task(task_id: str, updates: dict) -> Optional[Task]**: Update a task
- **delete_task(task_id: str) -> bool**: Delete a task by ID (returns success status)
- **clear_all_tasks() -> bool**: Remove all tasks (returns success status)

## In-Memory Implementation (Phase I)
- Tasks stored in a Python dictionary with task ID as key
- Data is volatile and lost when application exits
- Satisfies Phase I constitution requirement for in-memory storage

## SQLite Implementation (Future Enhancement)
- Tasks stored in SQLite database table
- Data persists across application restarts
- Can be enabled by switching storage implementation