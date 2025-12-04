"""Pytest configuration and shared fixtures for testing.

This module provides reusable fixtures for TodoManager testing,
including temporary database creation and sample task data.
"""

import tempfile
from datetime import datetime
from pathlib import Path

import pytest

from src.models import Task
from src.todo_manager import TodoManager


@pytest.fixture
def temp_db() -> str:
    """Create a temporary database file for testing.

    Yields:
        Path to temporary database file.

    Example:
        >>> def test_something(temp_db):
        ...     manager = TodoManager(temp_db)
    """
    with tempfile.NamedTemporaryFile(mode="w", suffix=".db", delete=False) as f:
        db_path = f.name

    yield db_path

    # Cleanup: remove temp database file after test
    Path(db_path).unlink(missing_ok=True)


@pytest.fixture
def todo_manager(temp_db: str) -> TodoManager:
    """Create a TodoManager instance with temporary database.

    Args:
        temp_db: Temporary database path from temp_db fixture.

    Returns:
        TodoManager instance configured with temporary database.

    Example:
        >>> def test_add_task(todo_manager):
        ...     task = todo_manager.add_task("Test task")
        ...     assert task.id == 1
    """
    return TodoManager(db_path=temp_db)


@pytest.fixture
def sample_task() -> Task:
    """Create a sample Task instance for testing.

    Returns:
        Task instance with predefined test data.

    Example:
        >>> def test_task_format(sample_task):
        ...     assert sample_task.title == "Buy milk"
    """
    return Task(
        id=1,
        title="Buy milk",
        description="Get 2 liters from the store",
        status="pending",
        created_at=datetime(2025, 12, 4, 10, 15, 0),
        updated_at=datetime(2025, 12, 4, 10, 15, 0),
    )
