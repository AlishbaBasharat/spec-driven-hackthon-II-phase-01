# Todo In-Memory Python Console App

A visually clean, modern interactive CLI To-Do application with 5 basic CRUD operations for managing tasks. The application allows users to manage their tasks through an interactive menu system with arrow key navigation.

## Features

- View all tasks with clear completion status indicators
- Add new tasks with title and optional description
- Update existing task details
- Delete tasks from the list
- Mark tasks as complete/incomplete
- Interactive menu with arrow key navigation
- Color-coded task display for better visibility
- Persistent storage (SQLite database)

## Prerequisites

- Python 3.13+
- UV package manager (optional, but recommended)

## Installation

### Using UV (recommended)
```bash
uv sync
uv run todo-app
```

### Using pip
```bash
pip install -r requirements.txt
python -m src.cli.app
```

## Usage

The application provides an interactive menu where you can:
- View all tasks
- Add new tasks
- Update existing tasks
- Delete tasks
- Mark tasks as complete/incomplete

Navigate using arrow keys or number selection as prompted.

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test file
pytest tests/unit/test_task.py
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

## Architecture Notes
- Clean architecture with separation of concerns
- Storage abstraction layer allows switching between implementations
- All business logic is in services, presentation in CLI layer
- Data validation through Pydantic models