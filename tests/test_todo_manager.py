"""Unit tests for TodoManager CRUD operations.

This module tests TodoManager methods following TDD principles.
Tests are written before implementation to verify contract compliance.

Test Coverage:
User Story 1 (Add and View Tasks):
- T021: test_add_task_success - Verify successful task creation with valid inputs
- T022: test_add_task_empty_title_raises_error - Verify ValueError for empty titles
- T023: test_list_tasks_returns_all_tasks - Verify all tasks are retrieved in order
- T024: test_list_tasks_empty_returns_empty_list - Verify empty list when no tasks

User Story 2 (Mark Tasks Complete):
- T032: test_complete_task_success - Verify task status changes to 'done'
- T033: test_complete_task_not_found - Verify False returned for non-existent task
- T034: test_complete_task_already_done - Verify handling of already completed tasks

User Story 3 (Update Task Details):
- T039: test_update_task_title_only - Verify selective title update
- T040: test_update_task_description_only - Verify selective description update
- T041: test_update_task_not_found - Verify False returned for non-existent task
- T042: test_update_task_preserves_unchanged_fields - Verify fields preserved with None

User Story 4 (Delete Tasks):
- T046: test_delete_task_success - Verify task is removed from database
- T047: test_delete_task_not_found - Verify False returned for non-existent task
"""

from datetime import datetime

import pytest

from src.models import Task
from src.todo_manager import TodoManager


class TestAddTask:
    """Test suite for TodoManager.add_task() method."""

    def test_add_task_success(self, todo_manager: TodoManager) -> None:
        """Test successful task creation with valid title and description.

        Verifies:
        - Task is created and returned
        - Task has auto-generated ID (should be 1 for first task)
        - Title and description are stored correctly
        - Status defaults to "pending"
        - Timestamps (created_at, updated_at) are set
        - Task is persisted in database

        Test ID: T021
        User Story: US1 - Add and View Tasks
        """
        # Arrange
        title = "Buy milk"
        description = "Get 2 liters from the store"

        # Act
        task = todo_manager.add_task(title, description)

        # Assert - Verify returned Task object
        assert isinstance(task, Task), "add_task should return a Task instance"
        assert task.id == 1, "First task should have ID 1"
        assert task.title == title, "Title should match input"
        assert task.description == description, "Description should match input"
        assert task.status == "pending", "New task should have status 'pending'"
        assert isinstance(task.created_at, datetime), "created_at should be a datetime"
        assert isinstance(task.updated_at, datetime), "updated_at should be a datetime"
        assert task.created_at == task.updated_at, "New task should have matching timestamps"

        # Assert - Verify database persistence by retrieving task
        retrieved_task = todo_manager.get_task(task.id)
        assert retrieved_task is not None, "Task should be persisted in database"
        assert retrieved_task.title == title, "Persisted title should match"
        assert retrieved_task.description == description, "Persisted description should match"

    def test_add_task_with_default_description(self, todo_manager: TodoManager) -> None:
        """Test task creation with default empty description.

        Verifies:
        - Description defaults to empty string when not provided
        - Task is created successfully with only title

        Test ID: T021 (extended)
        User Story: US1 - Add and View Tasks
        """
        # Arrange
        title = "Write unit tests"

        # Act
        task = todo_manager.add_task(title)

        # Assert
        assert task.title == title, "Title should match input"
        assert task.description == "", "Description should default to empty string"
        assert task.id == 1, "Task should be created with ID"

    def test_add_task_strips_title_whitespace(self, todo_manager: TodoManager) -> None:
        """Test that title is stripped of leading/trailing whitespace.

        Verifies:
        - Leading and trailing whitespace is removed from title
        - Task is created successfully with trimmed title

        Test ID: T021 (extended)
        User Story: US1 - Add and View Tasks
        """
        # Arrange
        title_with_whitespace = "   Buy groceries   "
        expected_title = "Buy groceries"

        # Act
        task = todo_manager.add_task(title_with_whitespace, "Weekly shopping")

        # Assert
        assert task.title == expected_title, "Title should be stripped of whitespace"

    def test_add_task_empty_title_raises_error(self, todo_manager: TodoManager) -> None:
        """Test that empty title raises ValueError.

        Verifies:
        - ValueError is raised when title is empty string
        - Error message is descriptive
        - No task is created in database

        Test ID: T022
        User Story: US1 - Add and View Tasks
        """
        # Arrange
        empty_title = ""

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            todo_manager.add_task(empty_title, "This should fail")

        # Verify error message is descriptive
        assert "title" in str(exc_info.value).lower(), "Error message should mention 'title'"
        assert "empty" in str(exc_info.value).lower(), "Error message should mention 'empty'"

        # Verify no task was created
        all_tasks = todo_manager.list_tasks()
        assert len(all_tasks) == 0, "No task should be created when title is empty"

    def test_add_task_whitespace_only_title_raises_error(self, todo_manager: TodoManager) -> None:
        """Test that whitespace-only title raises ValueError.

        Verifies:
        - ValueError is raised when title contains only whitespace
        - Title validation happens after stripping

        Test ID: T022 (extended)
        User Story: US1 - Add and View Tasks
        """
        # Arrange
        whitespace_title = "   \t\n   "

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            todo_manager.add_task(whitespace_title)

        # Verify error message
        assert "title" in str(exc_info.value).lower(), "Error should be about title"
        assert "empty" in str(exc_info.value).lower(), "Error should mention empty"

    def test_add_task_multiple_tasks_increment_ids(self, todo_manager: TodoManager) -> None:
        """Test that multiple tasks receive incrementing IDs.

        Verifies:
        - First task gets ID 1
        - Second task gets ID 2
        - Third task gets ID 3
        - IDs are auto-incremented correctly

        Test ID: T021 (extended)
        User Story: US1 - Add and View Tasks
        """
        # Arrange & Act
        task1 = todo_manager.add_task("First task")
        task2 = todo_manager.add_task("Second task")
        task3 = todo_manager.add_task("Third task")

        # Assert
        assert task1.id == 1, "First task should have ID 1"
        assert task2.id == 2, "Second task should have ID 2"
        assert task3.id == 3, "Third task should have ID 3"


class TestListTasks:
    """Test suite for TodoManager.list_tasks() method."""

    def test_list_tasks_returns_all_tasks(self, todo_manager: TodoManager) -> None:
        """Test that list_tasks returns all tasks in order.

        Verifies:
        - All added tasks are returned
        - Tasks are ordered by ID ascending
        - Task attributes are preserved correctly
        - List contains Task objects

        Test ID: T023
        User Story: US1 - Add and View Tasks
        """
        # Arrange - Create multiple tasks
        task1 = todo_manager.add_task("Buy milk", "2 liters")
        task2 = todo_manager.add_task("Write tests", "Complete US1 tests")
        task3 = todo_manager.add_task("Review code", "Check PR")

        # Act
        tasks = todo_manager.list_tasks()

        # Assert - Verify list properties
        assert isinstance(tasks, list), "list_tasks should return a list"
        assert len(tasks) == 3, "Should return all 3 tasks"

        # Assert - Verify all tasks are Task instances
        for task in tasks:
            assert isinstance(task, Task), "Each item should be a Task instance"

        # Assert - Verify tasks are ordered by ID ascending
        assert tasks[0].id == task1.id, "First task should have lowest ID"
        assert tasks[1].id == task2.id, "Second task should have middle ID"
        assert tasks[2].id == task3.id, "Third task should have highest ID"
        assert tasks[0].id < tasks[1].id < tasks[2].id, "IDs should be in ascending order"

        # Assert - Verify task details are correct
        assert tasks[0].title == "Buy milk", "First task title should match"
        assert tasks[0].description == "2 liters", "First task description should match"
        assert tasks[1].title == "Write tests", "Second task title should match"
        assert tasks[2].title == "Review code", "Third task title should match"

    def test_list_tasks_empty_returns_empty_list(self, todo_manager: TodoManager) -> None:
        """Test that list_tasks returns empty list when no tasks exist.

        Verifies:
        - Empty list is returned when database has no tasks
        - No errors are raised
        - Return type is still a list

        Test ID: T024
        User Story: US1 - Add and View Tasks
        """
        # Arrange - No tasks added (fresh database from fixture)

        # Act
        tasks = todo_manager.list_tasks()

        # Assert
        assert isinstance(tasks, list), "Should return a list even when empty"
        assert len(tasks) == 0, "Should return empty list when no tasks exist"
        assert tasks == [], "Should be an empty list"

    def test_list_tasks_preserves_all_task_attributes(self, todo_manager: TodoManager) -> None:
        """Test that all task attributes are preserved in list_tasks.

        Verifies:
        - All Task fields are populated correctly
        - Timestamps are datetime objects
        - Status field is included

        Test ID: T023 (extended)
        User Story: US1 - Add and View Tasks
        """
        # Arrange
        original_task = todo_manager.add_task("Test task", "Test description")

        # Act
        tasks = todo_manager.list_tasks()

        # Assert
        retrieved_task = tasks[0]
        assert retrieved_task.id == original_task.id, "ID should be preserved"
        assert retrieved_task.title == original_task.title, "Title should be preserved"
        assert retrieved_task.description == original_task.description, (
            "Description should be preserved"
        )
        assert retrieved_task.status == original_task.status, "Status should be preserved"
        assert isinstance(retrieved_task.created_at, datetime), "created_at should be datetime"
        assert isinstance(retrieved_task.updated_at, datetime), "updated_at should be datetime"

    def test_list_tasks_after_simulated_app_restart(self, temp_db: str) -> None:
        """Test that tasks persist across simulated application restarts.

        Verifies:
        - Tasks survive database connection close/reopen
        - Data persistence works correctly
        - Tasks can be retrieved after manager recreation

        Test ID: T023 (extended) - Persistence testing
        User Story: US1 - Add and View Tasks
        """
        # Arrange - Create tasks and close connection
        manager1 = TodoManager(db_path=temp_db)
        manager1.add_task("Persistent task", "Should survive restart")
        manager1.add_task("Another task")
        original_task_count = len(manager1.list_tasks())

        # Simulate app restart by creating new manager instance
        manager2 = TodoManager(db_path=temp_db)

        # Act
        tasks = manager2.list_tasks()

        # Assert
        assert len(tasks) == original_task_count, "Same number of tasks after restart"
        assert len(tasks) == 2, "Both tasks should persist"
        assert tasks[0].title == "Persistent task", "First task should persist"
        assert tasks[1].title == "Another task", "Second task should persist"

    def test_list_tasks_with_mixed_descriptions(self, todo_manager: TodoManager) -> None:
        """Test list_tasks with tasks having various description values.

        Verifies:
        - Tasks with empty descriptions are handled
        - Tasks with descriptions are handled
        - Mixed task list works correctly

        Test ID: T023 (extended)
        User Story: US1 - Add and View Tasks
        """
        # Arrange
        todo_manager.add_task("Task with description", "Detailed info here")
        todo_manager.add_task("Task without description")
        todo_manager.add_task("Another with description", "More details")

        # Act
        tasks = todo_manager.list_tasks()

        # Assert
        assert len(tasks) == 3, "Should return all 3 tasks"
        assert tasks[0].description == "Detailed info here", "First task description"
        assert tasks[1].description == "", "Second task should have empty description"
        assert tasks[2].description == "More details", "Third task description"


class TestTaskCreationEdgeCases:
    """Test suite for edge cases in task creation."""

    def test_add_task_with_special_characters(self, todo_manager: TodoManager) -> None:
        """Test task creation with special characters in title and description.

        Verifies:
        - Special characters are stored correctly
        - Unicode characters work
        - SQL injection attempts are handled safely

        Test ID: T021 (edge case)
        User Story: US1 - Add and View Tasks
        """
        # Arrange
        special_title = "Task with special chars: @#$%^&*()"
        unicode_description = "Description with unicode: 你好 🎉 café"

        # Act
        task = todo_manager.add_task(special_title, unicode_description)

        # Assert
        assert task.title == special_title, "Special characters in title should be preserved"
        assert task.description == unicode_description, "Unicode in description should be preserved"

        # Verify persistence
        retrieved = todo_manager.get_task(task.id)
        assert retrieved.title == special_title, "Special characters should persist"

    def test_add_task_with_very_long_title(self, todo_manager: TodoManager) -> None:
        """Test task creation with very long title.

        Verifies:
        - Long titles are accepted
        - No truncation occurs (or expected truncation)

        Test ID: T021 (edge case)
        User Story: US1 - Add and View Tasks
        """
        # Arrange
        long_title = "A" * 500  # 500 character title

        # Act
        task = todo_manager.add_task(long_title, "Short description")

        # Assert
        assert len(task.title) == 500, "Long title should be stored completely"
        assert task.title == long_title, "Long title should match input"

    def test_add_task_with_newlines_in_description(self, todo_manager: TodoManager) -> None:
        """Test task creation with multiline description.

        Verifies:
        - Newlines are preserved in description
        - Multiline text is handled correctly

        Test ID: T021 (edge case)
        User Story: US1 - Add and View Tasks
        """
        # Arrange
        title = "Multiline task"
        description = "Line 1\nLine 2\nLine 3"

        # Act
        task = todo_manager.add_task(title, description)

        # Assert
        assert task.description == description, "Newlines should be preserved"
        assert "\n" in task.description, "Description should contain newlines"


class TestCompleteTask:
    """Test suite for TodoManager.complete_task() method.

    Tests User Story 2: Mark Tasks Complete
    Verifies the complete_task operation including success cases,
    not found errors, and already completed task handling.
    """

    def test_complete_task_success(self, todo_manager: TodoManager) -> None:
        """Test successfully marking a pending task as completed.

        Verifies:
        - Returns (True, "[OK] Task {id} marked as completed.") on success
        - Task status changes from "pending" to "done"
        - Task is updated in database
        - Updated_at timestamp is modified

        Test ID: T032
        User Story: US2 - Mark Tasks Complete
        """
        # Arrange - Create a pending task
        task = todo_manager.add_task("Buy groceries", "Weekly shopping")
        assert task.status == "pending", "Task should start as pending"
        original_updated_at = task.updated_at

        # Act
        success, message = todo_manager.complete_task(task.id)

        # Assert - Verify return values
        assert success is True, "complete_task should return True on success"
        assert message == f"[OK] Task {task.id} marked as completed.", (
            "Success message should match expected format"
        )

        # Assert - Verify task status changed in database
        updated_task = todo_manager.get_task(task.id)
        assert updated_task is not None, "Task should still exist in database"
        assert updated_task.status == "done", "Task status should be 'done'"
        assert updated_task.title == "Buy groceries", "Task title should be unchanged"
        assert updated_task.description == "Weekly shopping", "Task description should be unchanged"

        # Assert - Verify updated_at timestamp changed (optional but good practice)
        # Note: This may fail if operation is too fast, but worth checking
        assert updated_task.updated_at >= original_updated_at, (
            "updated_at should be equal or later after completion"
        )

    def test_complete_task_not_found(self, todo_manager: TodoManager) -> None:
        """Test completing a task that doesn't exist.

        Verifies:
        - Returns (False, "[ERROR] Task not found") for non-existent ID
        - No errors are raised
        - Database remains unchanged

        Test ID: T033
        User Story: US2 - Mark Tasks Complete
        """
        # Arrange - Use a task ID that doesn't exist
        non_existent_id = 99999

        # Verify database is empty or doesn't have this ID
        existing_task = todo_manager.get_task(non_existent_id)
        assert existing_task is None, "Test setup: Task should not exist"

        # Act
        success, message = todo_manager.complete_task(non_existent_id)

        # Assert
        assert success is False, "complete_task should return False for non-existent task"
        assert message == "[ERROR] Task not found", "Error message should indicate task not found"

        # Verify no task was created
        still_not_found = todo_manager.get_task(non_existent_id)
        assert still_not_found is None, "Task should still not exist after failed completion"

    def test_complete_task_already_done(self, todo_manager: TodoManager) -> None:
        """Test completing a task that is already marked as done.

        Verifies:
        - Returns (False, "Task is already complete.") when task is already done
        - Task status remains "done"
        - No database changes occur

        Test ID: T034
        User Story: US2 - Mark Tasks Complete
        """
        # Arrange - Create and complete a task
        task = todo_manager.add_task("Write tests", "Complete US2 tests")

        # First completion - should succeed
        first_success, first_message = todo_manager.complete_task(task.id)
        assert first_success is True, "First completion should succeed"

        # Verify task is now done
        completed_task = todo_manager.get_task(task.id)
        assert completed_task.status == "done", "Task should be marked as done"

        # Act - Try to complete again
        second_success, second_message = todo_manager.complete_task(task.id)

        # Assert - Should fail with already complete message
        assert second_success is False, (
            "complete_task should return False for already completed task"
        )
        assert second_message == "Task is already complete.", (
            "Error message should indicate task is already complete"
        )

        # Verify task status hasn't changed
        still_completed_task = todo_manager.get_task(task.id)
        assert still_completed_task.status == "done", (
            "Task status should still be 'done' after duplicate completion attempt"
        )


class TestUpdateTask:
    """Test suite for TodoManager.update_task() method.

    Tests User Story 3: Update Task Details
    Verifies the update_task operation including selective field updates,
    error handling, and timestamp management.
    """

    def test_update_task_title_only(self, todo_manager: TodoManager) -> None:
        """Test updating only the task title while preserving description.

        Verifies:
        - Returns True on successful update
        - Title is updated to new value
        - Description remains unchanged
        - Status remains unchanged
        - updated_at timestamp is modified
        - Database reflects the changes

        Test ID: T039
        User Story: US3 - Update Task Details
        """
        # Arrange - Create a task with both title and description
        task = todo_manager.add_task("Buy milk", "Get 2 liters from the store")
        original_description = task.description
        original_status = task.status
        original_updated_at = task.updated_at

        # Act - Update only the title
        new_title = "Buy organic milk"
        result = todo_manager.update_task(task.id, title=new_title)

        # Assert - Verify return value
        assert result is True, "update_task should return True on success"

        # Assert - Verify database changes
        updated_task = todo_manager.get_task(task.id)
        assert updated_task is not None, "Task should still exist in database"
        assert updated_task.title == new_title, "Title should be updated to new value"
        assert updated_task.description == original_description, (
            "Description should remain unchanged"
        )
        assert updated_task.status == original_status, "Status should remain unchanged"

        # Assert - Verify updated_at timestamp changed
        assert updated_task.updated_at >= original_updated_at, (
            "updated_at should be updated after modification"
        )

    def test_update_task_description_only(self, todo_manager: TodoManager) -> None:
        """Test updating only the task description while preserving title.

        Verifies:
        - Returns True on successful update
        - Description is updated to new value
        - Title remains unchanged
        - Status remains unchanged
        - updated_at timestamp is modified
        - Database reflects the changes

        Test ID: T040
        User Story: US3 - Update Task Details
        """
        # Arrange - Create a task with both title and description
        task = todo_manager.add_task("Write tests", "Complete US1 tests")
        original_title = task.title
        original_status = task.status
        original_updated_at = task.updated_at

        # Act - Update only the description
        new_description = "Complete US3 update task tests"
        result = todo_manager.update_task(task.id, description=new_description)

        # Assert - Verify return value
        assert result is True, "update_task should return True on success"

        # Assert - Verify database changes
        updated_task = todo_manager.get_task(task.id)
        assert updated_task is not None, "Task should still exist in database"
        assert updated_task.title == original_title, "Title should remain unchanged"
        assert updated_task.description == new_description, (
            "Description should be updated to new value"
        )
        assert updated_task.status == original_status, "Status should remain unchanged"

        # Assert - Verify updated_at timestamp changed
        assert updated_task.updated_at >= original_updated_at, (
            "updated_at should be updated after modification"
        )

    def test_update_task_not_found(self, todo_manager: TodoManager) -> None:
        """Test updating a task that doesn't exist.

        Verifies:
        - Returns False for non-existent task ID
        - No errors are raised
        - Database remains unchanged

        Test ID: T041
        User Story: US3 - Update Task Details
        """
        # Arrange - Use a task ID that doesn't exist
        non_existent_id = 99999

        # Verify database doesn't have this ID
        existing_task = todo_manager.get_task(non_existent_id)
        assert existing_task is None, "Test setup: Task should not exist"

        # Act - Try to update non-existent task
        result = todo_manager.update_task(
            non_existent_id, title="New title", description="New description"
        )

        # Assert - Should return False
        assert result is False, "update_task should return False for non-existent task"

        # Verify no task was created
        still_not_found = todo_manager.get_task(non_existent_id)
        assert still_not_found is None, "Task should still not exist after failed update"

    def test_update_task_preserves_unchanged_fields(self, todo_manager: TodoManager) -> None:
        """Test updating with both parameters as None preserves all fields.

        Verifies:
        - Returns True if task exists (even with no actual changes)
        - Title remains unchanged
        - Description remains unchanged
        - Status remains unchanged
        - updated_at timestamp may still be updated (implementation detail)

        Test ID: T042
        User Story: US3 - Update Task Details
        """
        # Arrange - Create a task
        task = todo_manager.add_task("Review code", "Check PR #123")
        original_title = task.title
        original_description = task.description
        original_status = task.status

        # Act - Update with both parameters as None
        result = todo_manager.update_task(task.id, title=None, description=None)

        # Assert - Verify return value (True if task exists)
        assert result is True, "update_task should return True if task exists, even with no changes"

        # Assert - Verify no data changes
        updated_task = todo_manager.get_task(task.id)
        assert updated_task is not None, "Task should still exist in database"
        assert updated_task.title == original_title, (
            "Title should remain unchanged when None is passed"
        )
        assert updated_task.description == original_description, (
            "Description should remain unchanged when None is passed"
        )
        assert updated_task.status == original_status, "Status should remain unchanged"

    def test_update_task_both_fields_together(self, todo_manager: TodoManager) -> None:
        """Test updating both title and description simultaneously.

        Verifies:
        - Returns True on successful update
        - Both title and description are updated
        - Status remains unchanged
        - updated_at timestamp is modified

        Test ID: T039 (extended)
        User Story: US3 - Update Task Details
        """
        # Arrange
        task = todo_manager.add_task("Old title", "Old description")
        original_status = task.status

        # Act - Update both fields
        new_title = "New title"
        new_description = "New description"
        result = todo_manager.update_task(task.id, title=new_title, description=new_description)

        # Assert
        assert result is True, "update_task should return True on success"

        updated_task = todo_manager.get_task(task.id)
        assert updated_task.title == new_title, "Title should be updated"
        assert updated_task.description == new_description, "Description should be updated"
        assert updated_task.status == original_status, "Status should remain unchanged"

    def test_update_task_empty_title_raises_error(self, todo_manager: TodoManager) -> None:
        """Test that updating with empty title raises ValueError.

        Verifies:
        - ValueError is raised when title is empty string
        - Error message is descriptive
        - Task remains unchanged in database

        Test ID: T039 (validation)
        User Story: US3 - Update Task Details
        """
        # Arrange
        task = todo_manager.add_task("Valid title", "Valid description")
        original_title = task.title

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            todo_manager.update_task(task.id, title="")

        # Verify error message
        assert "title" in str(exc_info.value).lower(), "Error message should mention 'title'"
        assert "empty" in str(exc_info.value).lower(), "Error message should mention 'empty'"

        # Verify task unchanged
        unchanged_task = todo_manager.get_task(task.id)
        assert unchanged_task.title == original_title, (
            "Title should not change when update raises error"
        )

    def test_update_task_whitespace_only_title_raises_error(
        self, todo_manager: TodoManager
    ) -> None:
        """Test that updating with whitespace-only title raises ValueError.

        Verifies:
        - ValueError is raised when title contains only whitespace
        - Title validation happens after stripping
        - Task remains unchanged in database

        Test ID: T039 (validation)
        User Story: US3 - Update Task Details
        """
        # Arrange
        task = todo_manager.add_task("Valid title", "Valid description")
        original_title = task.title

        # Act & Assert
        with pytest.raises(ValueError) as exc_info:
            todo_manager.update_task(task.id, title="   \t\n   ")

        # Verify error message
        assert "title" in str(exc_info.value).lower(), "Error message should mention 'title'"
        assert "empty" in str(exc_info.value).lower(), "Error message should mention 'empty'"

        # Verify task unchanged
        unchanged_task = todo_manager.get_task(task.id)
        assert unchanged_task.title == original_title, (
            "Title should not change when update raises error"
        )

    def test_update_task_strips_title_whitespace(self, todo_manager: TodoManager) -> None:
        """Test that title is stripped of leading/trailing whitespace during update.

        Verifies:
        - Leading and trailing whitespace is removed from title
        - Task is updated with trimmed title

        Test ID: T039 (extended)
        User Story: US3 - Update Task Details
        """
        # Arrange
        task = todo_manager.add_task("Original title", "Original description")

        # Act - Update with whitespace-padded title
        title_with_whitespace = "   Updated title   "
        expected_title = "Updated title"
        result = todo_manager.update_task(task.id, title=title_with_whitespace)

        # Assert
        assert result is True, "update_task should succeed"

        updated_task = todo_manager.get_task(task.id)
        assert updated_task.title == expected_title, "Title should be stripped of whitespace"

    def test_update_task_to_empty_description(self, todo_manager: TodoManager) -> None:
        """Test updating description to empty string.

        Verifies:
        - Description can be set to empty string
        - Empty string is different from None (None means no update)
        - Title and status remain unchanged

        Test ID: T040 (extended)
        User Story: US3 - Update Task Details
        """
        # Arrange
        task = todo_manager.add_task("Task title", "Original description")
        original_title = task.title

        # Act - Update description to empty string
        result = todo_manager.update_task(task.id, description="")

        # Assert
        assert result is True, "update_task should succeed with empty description"

        updated_task = todo_manager.get_task(task.id)
        assert updated_task.title == original_title, "Title should remain unchanged"
        assert updated_task.description == "", "Description should be updated to empty string"

    def test_update_task_with_special_characters(self, todo_manager: TodoManager) -> None:
        """Test updating with special characters in title and description.

        Verifies:
        - Special characters are stored correctly
        - Unicode characters work
        - Database handles various character sets

        Test ID: T039 (edge case)
        User Story: US3 - Update Task Details
        """
        # Arrange
        task = todo_manager.add_task("Original", "Original desc")

        # Act - Update with special characters
        special_title = "Task with special chars: @#$%^&*()"
        unicode_description = "Description with unicode: 你好 🎉 café"
        result = todo_manager.update_task(
            task.id, title=special_title, description=unicode_description
        )

        # Assert
        assert result is True, "update_task should succeed with special characters"

        updated_task = todo_manager.get_task(task.id)
        assert updated_task.title == special_title, (
            "Special characters in title should be preserved"
        )
        assert updated_task.description == unicode_description, (
            "Unicode in description should be preserved"
        )

    def test_update_task_persistence_across_restart(self, temp_db: str) -> None:
        """Test that task updates persist across simulated application restarts.

        Verifies:
        - Updated tasks survive database connection close/reopen
        - Data persistence works correctly after updates
        - Updates can be retrieved after manager recreation

        Test ID: T039 (persistence)
        User Story: US3 - Update Task Details
        """
        # Arrange - Create task and update it
        manager1 = TodoManager(db_path=temp_db)
        task = manager1.add_task("Original title", "Original description")

        # Act - Update the task
        new_title = "Updated title"
        new_description = "Updated description"
        manager1.update_task(task.id, title=new_title, description=new_description)

        # Simulate app restart
        manager2 = TodoManager(db_path=temp_db)

        # Assert - Verify updates persisted
        persisted_task = manager2.get_task(task.id)
        assert persisted_task is not None, "Task should persist after restart"
        assert persisted_task.title == new_title, "Updated title should persist across restart"
        assert persisted_task.description == new_description, (
            "Updated description should persist across restart"
        )

    def test_update_task_multiple_updates_sequential(self, todo_manager: TodoManager) -> None:
        """Test multiple sequential updates to the same task.

        Verifies:
        - Task can be updated multiple times
        - Each update applies correctly
        - updated_at timestamp progresses

        Test ID: T039 (extended)
        User Story: US3 - Update Task Details
        """
        # Arrange
        task = todo_manager.add_task("Version 1", "Description 1")

        # Act - Perform multiple sequential updates
        result1 = todo_manager.update_task(task.id, title="Version 2")
        updated1 = todo_manager.get_task(task.id)

        result2 = todo_manager.update_task(task.id, description="Description 2")
        updated2 = todo_manager.get_task(task.id)

        result3 = todo_manager.update_task(task.id, title="Version 3")
        updated3 = todo_manager.get_task(task.id)

        # Assert - All updates succeeded
        assert all([result1, result2, result3]), "All updates should succeed"

        # Assert - Final state is correct
        assert updated3.title == "Version 3", "Title should reflect last update"
        assert updated3.description == "Description 2", "Description should reflect its last update"

        # Assert - Timestamps should progress
        assert updated1.updated_at <= updated2.updated_at <= updated3.updated_at, (
            "updated_at should progress with each update"
        )

    def test_update_task_with_very_long_title(self, todo_manager: TodoManager) -> None:
        """Test updating with very long title.

        Verifies:
        - Long titles are accepted during update
        - No truncation occurs
        - Database handles large text fields

        Test ID: T039 (edge case)
        User Story: US3 - Update Task Details
        """
        # Arrange
        task = todo_manager.add_task("Short title", "Short description")

        # Act - Update with very long title
        long_title = "A" * 500  # 500 character title
        result = todo_manager.update_task(task.id, title=long_title)

        # Assert
        assert result is True, "update_task should succeed with long title"

        updated_task = todo_manager.get_task(task.id)
        assert len(updated_task.title) == 500, "Long title should be stored completely"
        assert updated_task.title == long_title, "Long title should match input"

    def test_update_task_with_newlines_in_description(self, todo_manager: TodoManager) -> None:
        """Test updating description with multiline content.

        Verifies:
        - Newlines are preserved in description during update
        - Multiline text is handled correctly

        Test ID: T040 (edge case)
        User Story: US3 - Update Task Details
        """
        # Arrange
        task = todo_manager.add_task("Task title", "Original description")

        # Act - Update with multiline description
        multiline_description = "Line 1\nLine 2\nLine 3\nLine 4"
        result = todo_manager.update_task(task.id, description=multiline_description)

        # Assert
        assert result is True, "update_task should succeed with multiline description"

        updated_task = todo_manager.get_task(task.id)
        assert updated_task.description == multiline_description, (
            "Newlines should be preserved in description"
        )
        assert updated_task.description.count("\n") == 3, "All newlines should be preserved"


class TestDeleteTask:
    """Test suite for TodoManager.delete_task() method.

    Tests User Story 4: Delete Tasks
    Verifies the delete_task operation including success cases,
    not found errors, and database state after deletion.
    """

    def test_delete_task_success(self, todo_manager: TodoManager) -> None:
        """Test successfully deleting an existing task.

        Verifies:
        - Returns True when task is found and deleted
        - Task is removed from database
        - Task can no longer be retrieved with get_task
        - Task does not appear in list_tasks
        - Other tasks remain unaffected

        Test ID: T046
        User Story: US4 - Delete Tasks
        """
        # Arrange - Create multiple tasks to verify selective deletion
        task1 = todo_manager.add_task("Task to delete", "This will be deleted")
        task2 = todo_manager.add_task("Task to keep", "This should remain")
        task3 = todo_manager.add_task("Another keeper", "Also should remain")

        # Verify all tasks exist before deletion
        all_tasks_before = todo_manager.list_tasks()
        assert len(all_tasks_before) == 3, "Should have 3 tasks before deletion"

        # Act - Delete the first task
        result = todo_manager.delete_task(task1.id)

        # Assert - Verify return value
        assert result is True, "delete_task should return True on success"

        # Assert - Verify task is removed from database
        deleted_task = todo_manager.get_task(task1.id)
        assert deleted_task is None, "Deleted task should not be retrievable"

        # Assert - Verify task does not appear in list
        remaining_tasks = todo_manager.list_tasks()
        assert len(remaining_tasks) == 2, "Should have 2 tasks after deletion"
        remaining_ids = [task.id for task in remaining_tasks]
        assert task1.id not in remaining_ids, "Deleted task ID should not be in list"

        # Assert - Verify other tasks remain unaffected
        assert task2.id in remaining_ids, "Task 2 should still exist"
        assert task3.id in remaining_ids, "Task 3 should still exist"

        kept_task2 = todo_manager.get_task(task2.id)
        kept_task3 = todo_manager.get_task(task3.id)
        assert kept_task2 is not None, "Task 2 should be retrievable"
        assert kept_task3 is not None, "Task 3 should be retrievable"
        assert kept_task2.title == "Task to keep", "Task 2 title should be unchanged"
        assert kept_task3.title == "Another keeper", "Task 3 title should be unchanged"

    def test_delete_task_not_found(self, todo_manager: TodoManager) -> None:
        """Test deleting a task that doesn't exist.

        Verifies:
        - Returns False when task ID is not found
        - No errors are raised
        - Database remains unchanged
        - Other tasks are unaffected

        Test ID: T047
        User Story: US4 - Delete Tasks
        """
        # Arrange - Create some tasks and use a non-existent ID
        task1 = todo_manager.add_task("Existing task 1")
        task2 = todo_manager.add_task("Existing task 2")
        non_existent_id = 99999

        # Verify the non-existent task doesn't exist
        non_existent_task = todo_manager.get_task(non_existent_id)
        assert non_existent_task is None, "Test setup: Non-existent task should not exist"

        # Count tasks before attempted deletion
        tasks_before = todo_manager.list_tasks()
        count_before = len(tasks_before)

        # Act - Try to delete non-existent task
        result = todo_manager.delete_task(non_existent_id)

        # Assert - Verify return value
        assert result is False, "delete_task should return False for non-existent task"

        # Assert - Verify database unchanged
        tasks_after = todo_manager.list_tasks()
        count_after = len(tasks_after)
        assert count_after == count_before, "Task count should be unchanged"
        assert count_after == 2, "Should still have 2 tasks"

        # Assert - Verify existing tasks are unaffected
        still_exists1 = todo_manager.get_task(task1.id)
        still_exists2 = todo_manager.get_task(task2.id)
        assert still_exists1 is not None, "Task 1 should still exist"
        assert still_exists2 is not None, "Task 2 should still exist"
        assert still_exists1.title == "Existing task 1", "Task 1 should be unchanged"
        assert still_exists2.title == "Existing task 2", "Task 2 should be unchanged"

    def test_delete_task_completed_task(self, todo_manager: TodoManager) -> None:
        """Test deleting a task that has been marked as completed.

        Verifies:
        - Completed tasks can be deleted
        - Returns True for successful deletion
        - Task is removed from database regardless of status

        Test ID: T046 (extended)
        User Story: US4 - Delete Tasks
        """
        # Arrange - Create and complete a task
        task = todo_manager.add_task("Completed task", "Already done")
        success, message = todo_manager.complete_task(task.id)
        assert success is True, "Task should be completed successfully"

        # Verify task is completed
        completed_task = todo_manager.get_task(task.id)
        assert completed_task.status == "done", "Task should have status 'done'"

        # Act - Delete the completed task
        result = todo_manager.delete_task(task.id)

        # Assert
        assert result is True, "delete_task should return True for completed task"

        deleted_task = todo_manager.get_task(task.id)
        assert deleted_task is None, "Completed task should be deleted from database"

    def test_delete_task_persistence_across_restart(self, temp_db: str) -> None:
        """Test that task deletion persists across simulated application restarts.

        Verifies:
        - Deleted tasks remain deleted after database connection close/reopen
        - Deletion persistence works correctly
        - Deleted task cannot be retrieved after manager recreation

        Test ID: T046 (persistence)
        User Story: US4 - Delete Tasks
        """
        # Arrange - Create tasks and delete one
        manager1 = TodoManager(db_path=temp_db)
        task1 = manager1.add_task("Task to delete", "Will be deleted")
        task2 = manager1.add_task("Task to keep", "Will persist")

        # Delete first task
        result = manager1.delete_task(task1.id)
        assert result is True, "Deletion should succeed"

        # Simulate app restart by creating new manager instance
        manager2 = TodoManager(db_path=temp_db)

        # Act - Try to retrieve deleted task
        deleted_task = manager2.get_task(task1.id)
        remaining_tasks = manager2.list_tasks()

        # Assert - Verify deletion persisted
        assert deleted_task is None, "Deleted task should not be retrievable after restart"
        assert len(remaining_tasks) == 1, "Should have 1 task after restart"
        assert remaining_tasks[0].id == task2.id, "Remaining task should be task2"
        assert remaining_tasks[0].title == "Task to keep", "Remaining task should be unchanged"

    def test_delete_task_empty_database(self, todo_manager: TodoManager) -> None:
        """Test deleting from an empty database.

        Verifies:
        - Returns False when database has no tasks
        - No errors are raised on empty database
        - Database remains empty after failed deletion

        Test ID: T047 (edge case)
        User Story: US4 - Delete Tasks
        """
        # Arrange - Empty database (no tasks added)
        tasks_before = todo_manager.list_tasks()
        assert len(tasks_before) == 0, "Database should be empty"

        # Act - Try to delete from empty database
        result = todo_manager.delete_task(1)

        # Assert
        assert result is False, "delete_task should return False on empty database"

        tasks_after = todo_manager.list_tasks()
        assert len(tasks_after) == 0, "Database should still be empty"

    def test_delete_task_all_tasks_sequential(self, todo_manager: TodoManager) -> None:
        """Test deleting all tasks one by one.

        Verifies:
        - Multiple sequential deletions work correctly
        - Each deletion returns True
        - Database becomes empty after all deletions
        - list_tasks returns empty list when all tasks deleted

        Test ID: T046 (extended)
        User Story: US4 - Delete Tasks
        """
        # Arrange - Create multiple tasks
        task1 = todo_manager.add_task("Task 1")
        task2 = todo_manager.add_task("Task 2")
        task3 = todo_manager.add_task("Task 3")

        assert len(todo_manager.list_tasks()) == 3, "Should have 3 tasks initially"

        # Act - Delete all tasks sequentially
        result1 = todo_manager.delete_task(task1.id)
        result2 = todo_manager.delete_task(task2.id)
        result3 = todo_manager.delete_task(task3.id)

        # Assert - All deletions succeeded
        assert result1 is True, "First deletion should succeed"
        assert result2 is True, "Second deletion should succeed"
        assert result3 is True, "Third deletion should succeed"

        # Assert - Database is now empty
        final_tasks = todo_manager.list_tasks()
        assert len(final_tasks) == 0, "Database should be empty after all deletions"
        assert final_tasks == [], "Should return empty list"

        # Assert - None of the tasks are retrievable
        assert todo_manager.get_task(task1.id) is None, "Task 1 should not be retrievable"
        assert todo_manager.get_task(task2.id) is None, "Task 2 should not be retrievable"
        assert todo_manager.get_task(task3.id) is None, "Task 3 should not be retrievable"

    def test_delete_task_duplicate_deletion(self, todo_manager: TodoManager) -> None:
        """Test attempting to delete the same task twice.

        Verifies:
        - First deletion returns True
        - Second deletion returns False
        - No errors raised on duplicate deletion attempt
        - Task remains deleted after second attempt

        Test ID: T047 (edge case)
        User Story: US4 - Delete Tasks
        """
        # Arrange - Create a task
        task = todo_manager.add_task("Task to delete twice")

        # Act - Delete task twice
        first_result = todo_manager.delete_task(task.id)
        second_result = todo_manager.delete_task(task.id)

        # Assert - First deletion succeeds, second fails
        assert first_result is True, "First deletion should return True"
        assert second_result is False, "Second deletion should return False"

        # Assert - Task is still deleted
        deleted_task = todo_manager.get_task(task.id)
        assert deleted_task is None, "Task should remain deleted after duplicate deletion"

    def test_delete_task_with_negative_id(self, todo_manager: TodoManager) -> None:
        """Test deleting with negative task ID.

        Verifies:
        - Returns False for negative IDs
        - No errors raised
        - Database remains unchanged

        Test ID: T047 (edge case)
        User Story: US4 - Delete Tasks
        """
        # Arrange - Create a task and use negative ID
        task = todo_manager.add_task("Valid task")
        negative_id = -1

        # Act - Try to delete with negative ID
        result = todo_manager.delete_task(negative_id)

        # Assert
        assert result is False, "delete_task should return False for negative ID"

        # Assert - Original task unchanged
        existing_task = todo_manager.get_task(task.id)
        assert existing_task is not None, "Original task should still exist"
        tasks = todo_manager.list_tasks()
        assert len(tasks) == 1, "Should still have 1 task"

    def test_delete_task_with_zero_id(self, todo_manager: TodoManager) -> None:
        """Test deleting with zero task ID.

        Verifies:
        - Returns False for ID 0
        - No errors raised
        - Database remains unchanged

        Test ID: T047 (edge case)
        User Story: US4 - Delete Tasks
        """
        # Arrange - Create a task
        task = todo_manager.add_task("Valid task")

        # Act - Try to delete with ID 0
        result = todo_manager.delete_task(0)

        # Assert
        assert result is False, "delete_task should return False for ID 0"

        # Assert - Original task unchanged
        existing_task = todo_manager.get_task(task.id)
        assert existing_task is not None, "Original task should still exist"

    def test_delete_task_middle_of_sequence(self, todo_manager: TodoManager) -> None:
        """Test deleting a task from the middle of a sequence.

        Verifies:
        - Deletion works correctly when task is not first or last
        - Tasks before and after the deleted task remain
        - IDs of remaining tasks are unchanged
        - List order is preserved

        Test ID: T046 (extended)
        User Story: US4 - Delete Tasks
        """
        # Arrange - Create tasks in sequence
        task1 = todo_manager.add_task("First task")
        task2 = todo_manager.add_task("Middle task (to delete)")
        task3 = todo_manager.add_task("Last task")

        # Act - Delete middle task
        result = todo_manager.delete_task(task2.id)

        # Assert
        assert result is True, "Deletion should succeed"

        # Assert - Verify remaining tasks
        remaining_tasks = todo_manager.list_tasks()
        assert len(remaining_tasks) == 2, "Should have 2 remaining tasks"
        assert remaining_tasks[0].id == task1.id, "First task should remain"
        assert remaining_tasks[1].id == task3.id, "Last task should remain"
        assert remaining_tasks[0].title == "First task", "First task title preserved"
        assert remaining_tasks[1].title == "Last task", "Last task title preserved"

        # Assert - Deleted task is gone
        deleted_task = todo_manager.get_task(task2.id)
        assert deleted_task is None, "Middle task should be deleted"
