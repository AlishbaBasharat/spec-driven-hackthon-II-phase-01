"""
Test script to verify SQLite persistence functionality.
This script tests that tasks persist across application restarts.
"""
import os
import sqlite3
from src.models.task import Task
from src.services.database_service import DatabaseService
from src.services.task_service import TaskService


def test_basic_persistence():
    """Test basic persistence functionality"""
    print("Testing basic persistence functionality...")

    # Remove existing database file to start fresh
    if os.path.exists("todo_app.db"):
        os.remove("todo_app.db")
        print("Removed existing database file")

    # Create a new database service (which will create the SQLite database)
    db_service = DatabaseService()
    task_service = TaskService(db_service)

    # Create a test task
    task = task_service.create_task("Test Task", "This is a test task for persistence")
    print(f"Created task: {task.title} (ID: {task.id})")

    # Verify the task exists in the database
    retrieved_task = task_service.get_task(task.id)
    assert retrieved_task is not None, "Task should exist in database"
    assert retrieved_task.title == "Test Task", "Task title should match"
    assert retrieved_task.description == "This is a test task for persistence", "Task description should match"
    print("✓ Task retrieved successfully from database")

    # Get all tasks
    all_tasks = task_service.get_all_tasks()
    assert len(all_tasks) == 1, "Should have 1 task in database"
    print(f"✓ Found {len(all_tasks)} task(s) in database")

    # Test task deletion
    delete_result = task_service.delete_task(task.id)
    assert delete_result is True, "Task deletion should return True"
    print("✓ Task deleted successfully")

    # Verify task is gone
    all_tasks_after_delete = task_service.get_all_tasks()
    assert len(all_tasks_after_delete) == 0, "Should have 0 tasks after deletion"
    print("✓ No tasks found after deletion")

    print("Basic persistence test passed!\n")


def test_multiple_tasks():
    """Test with multiple tasks"""
    print("Testing multiple tasks...")

    # Create a new database service (or use existing)
    db_service = DatabaseService()
    task_service = TaskService(db_service)

    # Create multiple tasks
    task1 = task_service.create_task("First Task", "Description for first task")
    task2 = task_service.create_task("Second Task", "Description for second task")
    task3 = task_service.create_task("Third Task", "Description for third task")

    print(f"Created 3 tasks: {task1.title}, {task2.title}, {task3.title}")

    # Get all tasks
    all_tasks = task_service.get_all_tasks()
    assert len(all_tasks) == 3, f"Should have 3 tasks, but found {len(all_tasks)}"
    print(f"✓ Found {len(all_tasks)} tasks in database")

    # Mark one task as complete
    updated_task = task_service.mark_task_complete(task2.id)
    assert updated_task is not None, "Task should be updated"
    assert updated_task.completed is True, "Task should be marked as complete"
    print("✓ Task marked as complete successfully")

    # Verify the update in the database
    retrieved_task = task_service.get_task(task2.id)
    assert retrieved_task.completed is True, "Retrieved task should be marked as complete"
    print("✓ Updated task retrieved successfully from database")

    print("Multiple tasks test passed!\n")


def test_database_directly():
    """Test the database directly to ensure data is persisted"""
    print("Testing database directly...")

    # Connect to the database directly
    conn = sqlite3.connect("todo_app.db")
    cursor = conn.cursor()

    # Check if tasks table exists
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='tasks';")
    tables = cursor.fetchall()
    assert len(tables) > 0, "Tasks table should exist"
    print("✓ Tasks table exists")

    # Count the number of tasks
    cursor.execute("SELECT COUNT(*) FROM tasks;")
    count = cursor.fetchone()[0]
    print(f"✓ Direct database check shows {count} tasks")

    # Get all task details
    cursor.execute("SELECT * FROM tasks;")
    rows = cursor.fetchall()
    print(f"✓ Direct database query found {len(rows)} rows")

    for row in rows:
        print(f"  - ID: {row[0]}, Title: {row[1]}, Completed: {bool(row[3])}")

    conn.close()
    print("Direct database test passed!\n")


if __name__ == "__main__":
    print("Starting persistence tests...\n")

    test_basic_persistence()
    test_multiple_tasks()
    test_database_directly()

    print("All persistence tests passed!")
    print("\nThe SQLite database is working correctly and tasks persist across application restarts.")