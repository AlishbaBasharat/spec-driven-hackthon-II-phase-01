# Quickstart Guide: Interactive CLI To-Do Application

## Prerequisites
- Python 3.13+
- UV package manager

## Setup

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. **Install dependencies using UV**
   ```bash
   uv sync
   # Or if starting fresh:
   uv pip install rich simple-term-menu pydantic pytest
   ```

3. **Install in development mode**
   ```bash
   uv build
   uv pip install -e .
   ```

## Running the Application

1. **Start the interactive CLI**
   ```bash
   python -m src.cli.app
   # Or if installed as package:
   todo-app
   ```

2. **Using the Interactive Menu**
   - Use arrow keys (↑/↓) or number keys to navigate options
   - Press Enter to select an option
   - Follow on-screen prompts for additional input

## Available Features

### 1. View All Tasks
- Displays all tasks with completion status indicators
- Shows pending tasks in one color and completed tasks in another
- Includes task titles, descriptions (truncated if long), and creation timestamps

### 2. Add New Task
- Prompts for task title (required)
- Optionally prompts for task description
- Creates new task with pending status
- Assigns unique ID automatically

### 3. Update Task
- Select existing task from list
- Update title and/or description
- Changes reflected immediately

### 4. Mark Complete/Incomplete
- Toggle completion status of any task
- Visual indicators update immediately
- Tracks completion statistics

### 5. Delete Task
- Select task to remove from list
- Confirmation prompt to prevent accidental deletion
- Removes task permanently

## Development

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_task_service.py
```

### Project Structure
```
src/
├── models/           # Data models (Task, etc.)
├── services/         # Business logic (TaskService, etc.)
├── cli/             # CLI interface (App, UI components)
└── __init__.py

tests/
├── unit/            # Unit tests for individual components
├── integration/     # Integration tests
└── conftest.py      # Test configuration
```

### Adding New Features
1. Update data models in `src/models/`
2. Implement business logic in `src/services/`
3. Add CLI interface in `src/cli/`
4. Write tests in `tests/`
5. Update documentation as needed

## Architecture Notes
- Clean architecture with separation of concerns
- Storage abstraction layer allows switching between in-memory and persistent storage
- All business logic is in services, presentation in CLI layer
- Data validation through Pydantic models