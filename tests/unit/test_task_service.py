"""
Unit tests for the TaskService to verify error handling and edge cases.
"""
import pytest
from src.models.task import Task
from src.models.errors import ValidationError, NotFoundError
from src.services.database_service import DatabaseService
from src.services.task_service import TaskService


class TestTaskService:
    def setup_method(self):
        """Set up a fresh TaskService for each test"""
        self.database_service = DatabaseService()
        self.task_service = TaskService(self.database_service)

    def test_create_task_with_valid_title_and_description(self):
        """Test that a task can be created with valid title and description"""
        task = self.task_service.create_task("Test Title", "Test Description")

        assert task.title == "Test Title"
        assert task.description == "Test Description"
        assert task.completed is False
        assert task.id is not None

    def test_create_task_with_valid_title_no_description(self):
        """Test that a task can be created with just a title"""
        task = self.task_service.create_task("Test Title")

        assert task.title == "Test Title"
        assert task.description is None
        assert task.completed is False

    def test_create_task_empty_title_raises_validation_error(self):
        """Test that creating a task with empty title raises ValidationError"""
        with pytest.raises(ValidationError):
            self.task_service.create_task("")

    def test_create_task_whitespace_only_title_raises_validation_error(self):
        """Test that creating a task with whitespace-only title raises ValidationError"""
        with pytest.raises(ValidationError):
            self.task_service.create_task("   ")

    def test_create_task_title_too_long_raises_validation_error(self):
        """Test that creating a task with title > 200 chars raises ValidationError"""
        long_title = "x" * 201
        with pytest.raises(ValidationError):
            self.task_service.create_task(long_title)

    def test_create_task_description_too_long_raises_validation_error(self):
        """Test that creating a task with description > 1000 chars raises ValidationError"""
        long_description = "x" * 1001
        with pytest.raises(ValidationError):
            self.task_service.create_task("Valid Title", long_description)

    def test_update_task_with_valid_data(self):
        """Test that a task can be updated with valid data"""
        original_task = self.task_service.create_task("Original Title", "Original Description")

        updated_task = self.task_service.update_task(
            original_task.id,
            title="Updated Title",
            description="Updated Description"
        )

        assert updated_task.title == "Updated Title"
        assert updated_task.description == "Updated Description"

    def test_update_task_with_invalid_title_raises_validation_error(self):
        """Test that updating a task with invalid title raises ValidationError"""
        task = self.task_service.create_task("Original Title")

        with pytest.raises(ValidationError):
            self.task_service.update_task(task.id, title="")

    def test_update_nonexistent_task_raises_not_found_error(self):
        """Test that updating a non-existent task raises NotFoundError"""
        with pytest.raises(NotFoundError):
            self.task_service.update_task("nonexistent-id", title="New Title")

    def test_get_nonexistent_task_returns_none(self):
        """Test that getting a non-existent task returns None"""
        result = self.task_service.get_task("nonexistent-id")
        assert result is None

    def test_delete_nonexistent_task_returns_false(self):
        """Test that deleting a non-existent task returns False"""
        result = self.task_service.delete_task("nonexistent-id")
        assert result is False

    def test_mark_complete_nonexistent_task_raises_not_found_error(self):
        """Test that marking a non-existent task as complete raises NotFoundError"""
        with pytest.raises(NotFoundError):
            self.task_service.mark_task_complete("nonexistent-id")

    def test_mark_incomplete_nonexistent_task_raises_not_found_error(self):
        """Test that marking a non-existent task as incomplete raises NotFoundError"""
        with pytest.raises(NotFoundError):
            self.task_service.mark_task_incomplete("nonexistent-id")

    def test_update_task_with_long_description_raises_validation_error(self):
        """Test that updating a task with a long description raises ValidationError"""
        task = self.task_service.create_task("Original Title")

        with pytest.raises(ValidationError):
            self.task_service.update_task(task.id, description="x" * 1001)

    def test_get_tasks_by_status_filters_correctly(self):
        """Test that get_tasks_by_status returns correctly filtered tasks"""
        # Create some tasks
        task1 = self.task_service.create_task("Task 1")
        task2 = self.task_service.create_task("Task 2")

        # Mark one as complete
        self.task_service.mark_task_complete(task2.id)

        # Get pending tasks
        pending_tasks = self.task_service.get_tasks_by_status(completed=False)
        assert len(pending_tasks) == 1
        assert pending_tasks[0].id == task1.id

        # Get completed tasks
        completed_tasks = self.task_service.get_tasks_by_status(completed=True)
        assert len(completed_tasks) == 1
        assert completed_tasks[0].id == task2.id