from typing import List, Optional, Dict
import sqlite3
import json
from datetime import datetime
from ..models.storage import Storage
from ..models.task import Task


class SQLiteStorage(Storage):
    """
    SQLite storage implementation for tasks.
    Tasks are stored in an SQLite database file with persistence across app restarts.
    """

    def __init__(self, db_path: str = "todo_app.db"):
        self.db_path = db_path
        self.init_database()

    def init_database(self):
        """Initialize the database and create the tasks table if it doesn't exist."""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id TEXT PRIMARY KEY,
                    title TEXT NOT NULL,
                    description TEXT,
                    completed BOOLEAN DEFAULT 0,
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)
            conn.commit()

    def save_task(self, task: Task) -> Task:
        """Persist a task and return the saved task"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT OR REPLACE INTO tasks (id, title, description, completed, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                task.id,
                task.title,
                task.description,
                task.completed,
                task.created_at.isoformat(),
                task.updated_at.isoformat()
            ))
            conn.commit()
        return task

    def get_task(self, task_id: str) -> Optional[Task]:
        """Retrieve a task by ID"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks WHERE id = ?", (task_id,))
            row = cursor.fetchone()

            if row:
                return Task(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    completed=bool(row[3]),
                    created_at=datetime.fromisoformat(row[4]),
                    updated_at=datetime.fromisoformat(row[5])
                )
            return None

    def get_all_tasks(self) -> List[Task]:
        """Retrieve all tasks"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM tasks ORDER BY created_at DESC")
            rows = cursor.fetchall()

            tasks = []
            for row in rows:
                task = Task(
                    id=row[0],
                    title=row[1],
                    description=row[2],
                    completed=bool(row[3]),
                    created_at=datetime.fromisoformat(row[4]),
                    updated_at=datetime.fromisoformat(row[5])
                )
                tasks.append(task)
            return tasks

    def update_task(self, task_id: str, updates: dict) -> Optional[Task]:
        """Update a task"""
        task = self.get_task(task_id)
        if not task:
            return None

        # Apply updates to the task object
        for key, value in updates.items():
            if hasattr(task, key):
                setattr(task, key, value)

        # Update the timestamp
        task.updated_at = datetime.now()

        # Save the updated task back to the database
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE tasks
                SET title = ?, description = ?, completed = ?, updated_at = ?
                WHERE id = ?
            """, (
                task.title,
                task.description,
                task.completed,
                task.updated_at.isoformat(),
                task.id
            ))
            conn.commit()

        return task

    def delete_task(self, task_id: str) -> bool:
        """Delete a task by ID (returns success status)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            conn.commit()
            return cursor.rowcount > 0

    def clear_all_tasks(self) -> bool:
        """Remove all tasks (returns success status)"""
        with sqlite3.connect(self.db_path) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM tasks")
            conn.commit()
            return cursor.rowcount > 0