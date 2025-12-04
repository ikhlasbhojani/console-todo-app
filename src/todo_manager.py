"""TodoManager class for task CRUD operations with SQLite persistence.

This module provides the TodoManager class which handles all database
interactions for task management.
"""

import sqlite3
from datetime import date, datetime
from pathlib import Path

from src.models import Task, TaskStats


def get_default_db_path() -> str:
    """Get the default database path for global installation.

    Returns:
        Path to ~/.todo-app/todo.db for global installs,
        or data/todo.db for local development.
    """
    # Use ~/.todo-app/todo.db for global installation
    home = Path.home()
    todo_app_dir = home / ".todo-app"
    return str(todo_app_dir / "todo.db")


class TodoManager:
    """Manages todo tasks with SQLite persistence.

    This class provides CRUD operations for tasks and handles
    all database interactions. It creates the database and
    table if they don't exist.

    Attributes:
        db_path: Path to the SQLite database file.
    """

    def __init__(self, db_path: str | None = None) -> None:
        """Initialize the TodoManager.

        Creates parent directories and database if they don't exist,
        and initializes the tasks table.

        Args:
            db_path: Path to SQLite database file. Creates parent
                     directories and database if they don't exist.
                     Defaults to ~/.todo-app/todo.db for global installation.

        Example:
            >>> manager = TodoManager()
            >>> manager = TodoManager("/path/to/test.db")
        """
        if db_path is None:
            db_path = get_default_db_path()
        self.db_path = db_path

        # Create parent directories if they don't exist
        db_file = Path(db_path)
        db_file.parent.mkdir(parents=True, exist_ok=True)

        # Initialize database and create table if needed
        self._init_db()

        # Ensure Phase 2 columns exist (migration)
        self._ensure_columns_exist()

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with row factory configured.

        Returns:
            SQLite connection with Row factory enabled.

        Example:
            >>> conn = self._get_connection()
            >>> cursor = conn.execute("SELECT * FROM tasks")
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self) -> None:
        """Create tasks table if it doesn't exist.

        Creates the tasks table with the following schema:
        - id: INTEGER PRIMARY KEY AUTOINCREMENT
        - title: TEXT NOT NULL
        - description: TEXT DEFAULT ''
        - status: TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'done'))
        - created_at: TEXT NOT NULL
        - updated_at: TEXT NOT NULL

        Also creates an index on the status column for query optimization.

        Example:
            >>> manager = TodoManager()
            >>> # Table is automatically created during initialization
        """
        with self._get_connection() as conn:
            # Create tasks table
            conn.execute("""
                CREATE TABLE IF NOT EXISTS tasks (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    title TEXT NOT NULL,
                    description TEXT DEFAULT '',
                    status TEXT DEFAULT 'pending' CHECK(status IN ('pending', 'done')),
                    created_at TEXT NOT NULL,
                    updated_at TEXT NOT NULL
                )
            """)

            # Create index for performance on status queries
            conn.execute("""
                CREATE INDEX IF NOT EXISTS idx_tasks_status ON tasks(status)
            """)

            # Create projects table for Phase 2
            conn.execute("""
                CREATE TABLE IF NOT EXISTS projects (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL UNIQUE COLLATE NOCASE,
                    description TEXT,
                    created_at TEXT NOT NULL
                )
            """)

            conn.commit()

    def _ensure_columns_exist(self) -> None:
        """Ensure Phase 2 columns exist in tasks table.

        Uses PRAGMA table_info to check for columns and adds them if missing.
        This is a safe migration that preserves existing data.
        """
        with self._get_connection() as conn:
            cursor = conn.execute("PRAGMA table_info(tasks)")
            columns = [row[1] for row in cursor.fetchall()]

            # Add due_date column if missing
            if "due_date" not in columns:
                conn.execute("ALTER TABLE tasks ADD COLUMN due_date TEXT")

            # Add project_id column if missing
            if "project_id" not in columns:
                conn.execute("ALTER TABLE tasks ADD COLUMN project_id INTEGER")

            conn.commit()

    def add_task(
        self,
        title: str,
        description: str = "",
        due_date: date | None = None,
        project_id: int | None = None,
    ) -> Task:
        """Create a new task.

        Args:
            title: Task title (required, non-empty after strip)
            description: Optional task description (default: empty string)
            due_date: Optional due date for the task
            project_id: Optional project ID to assign task to

        Returns:
            The newly created Task with generated ID and timestamps.

        Raises:
            ValueError: If title is empty or whitespace-only.

        Example:
            >>> manager.add_task("Buy milk", "2 liters from store")
            Task(id=1, title="Buy milk", description="2 liters from store",
                 status="pending", created_at=..., updated_at=...)
        """
        # Strip and validate title
        stripped_title = title.strip()
        if not stripped_title:
            raise ValueError("Title cannot be empty")

        # Create timestamps
        now = datetime.now()
        created_at = now.isoformat()
        updated_at = now.isoformat()

        # Format due_date for storage
        due_date_str = due_date.isoformat() if due_date else None

        # Insert task into database
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO tasks (
                    title, description, status, created_at, updated_at,
                    due_date, project_id
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    stripped_title,
                    description,
                    "pending",
                    created_at,
                    updated_at,
                    due_date_str,
                    project_id,
                ),
            )
            task_id = cursor.lastrowid
            conn.commit()

        # Return newly created Task object
        return Task(
            id=task_id,
            title=stripped_title,
            description=description,
            status="pending",
            created_at=now,
            updated_at=now,
            due_date=due_date,
            project_id=project_id,
        )

    def list_tasks(self) -> list[Task]:
        """Retrieve all tasks ordered by ID.

        Returns:
            List of all Task objects, empty list if no tasks exist.
            Tasks are ordered by id ascending.

        Example:
            >>> manager.list_tasks()
            [Task(id=1, ...), Task(id=2, ...)]
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT id, title, description, status, created_at, updated_at, due_date, project_id
                FROM tasks
                ORDER BY id ASC
                """
            )
            rows = cursor.fetchall()

        # Convert rows to Task objects
        tasks = [Task.from_row(row) for row in rows]
        return tasks

    def get_task(self, task_id: int) -> Task | None:
        """Retrieve a single task by ID.

        Args:
            task_id: The unique identifier of the task.

        Returns:
            The Task if found, None if no task with that ID exists.

        Example:
            >>> manager.get_task(1)
            Task(id=1, title="Buy milk", ...)
            >>> manager.get_task(999)
            None
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT id, title, description, status, created_at, updated_at, due_date, project_id
                FROM tasks
                WHERE id = ?
                """,
                (task_id,),
            )
            row = cursor.fetchone()

        if row is None:
            return None

        return Task.from_row(row)

    def update_task(
        self,
        task_id: int,
        title: str | None = None,
        description: str | None = None,
    ) -> bool:
        """Update an existing task's title and/or description.

        Args:
            task_id: The unique identifier of the task to update.
            title: New title (None = keep current). Empty string not allowed.
            description: New description (None = keep current).

        Returns:
            True if task was found and updated, False if task not found.

        Raises:
            ValueError: If title is provided but empty/whitespace-only.

        Note:
            - If both title and description are None, no update occurs but
              returns True if task exists.
            - Always updates updated_at timestamp on success.

        Example:
            >>> manager.update_task(1, title="Buy milk and eggs")
            True
            >>> manager.update_task(999, title="New title")
            False
        """
        # Check if task exists
        task = self.get_task(task_id)

        if task is None:
            return False

        # Validate title if provided
        if title is not None:
            stripped_title = title.strip()
            if not stripped_title:
                raise ValueError("Title cannot be empty")
            title = stripped_title

        # Build update query dynamically based on provided fields
        update_fields: list[str] = []
        params: list[str | int] = []

        if title is not None:
            update_fields.append("title = ?")
            params.append(title)

        if description is not None:
            update_fields.append("description = ?")
            params.append(description)

        # Always update updated_at timestamp
        now = datetime.now()
        updated_at = now.isoformat()
        update_fields.append("updated_at = ?")
        params.append(updated_at)

        # Add task_id for WHERE clause
        params.append(task_id)

        # Execute update query
        query = f"""
            UPDATE tasks
            SET {", ".join(update_fields)}
            WHERE id = ?
        """

        with self._get_connection() as conn:
            conn.execute(query, tuple(params))
            conn.commit()

        return True

    def complete_task(self, task_id: int) -> tuple[bool, str]:
        """Mark a task as completed.

        Args:
            task_id: The unique identifier of the task to complete.

        Returns:
            Tuple of (success: bool, message: str):
            - (True, "[OK] Task {id} marked as completed.") on success
            - (False, "[ERROR] Task not found") if task doesn't exist
            - (False, "Task is already complete.") if already done

        Example:
            >>> manager.complete_task(1)
            (True, "[OK] Task 1 marked as completed.")
            >>> manager.complete_task(999)
            (False, "[ERROR] Task not found")
        """
        # Retrieve the task to check if it exists
        task = self.get_task(task_id)

        if task is None:
            return (False, "[ERROR] Task not found")

        # Check if task is already completed
        if task.is_completed():
            return (False, "Task is already complete.")

        # Update task status to "done" and update timestamp
        now = datetime.now()
        updated_at = now.isoformat()

        with self._get_connection() as conn:
            conn.execute(
                """
                UPDATE tasks
                SET status = ?, updated_at = ?
                WHERE id = ?
                """,
                ("done", updated_at, task_id),
            )
            conn.commit()

        return (True, f"[OK] Task {task_id} marked as completed.")

    def delete_task(self, task_id: int) -> bool:
        """Delete a task.

        Args:
            task_id: The unique identifier of the task to delete.

        Returns:
            True if task was found and deleted, False if task not found.

        Note:
            Confirmation is handled by the CLI layer, not this method.

        Example:
            >>> manager.delete_task(1)
            True
            >>> manager.delete_task(999)
            False
        """
        # Check if task exists first
        task = self.get_task(task_id)

        if task is None:
            return False

        # Delete the task from database
        with self._get_connection() as conn:
            conn.execute(
                """
                DELETE FROM tasks
                WHERE id = ?
                """,
                (task_id,),
            )
            conn.commit()

        return True

    # =========================================================================
    # Phase 2: Filter Methods for Due Dates
    # =========================================================================

    def list_tasks_today(self) -> list[Task]:
        """Retrieve all tasks due today.

        Returns:
            List of Task objects due on the current date.
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT id, title, description, status, created_at, updated_at, due_date, project_id
                FROM tasks
                WHERE due_date = DATE('now', 'localtime')
                ORDER BY id ASC
                """
            )
            rows = cursor.fetchall()

        return [Task.from_row(row) for row in rows]

    def list_tasks_overdue(self) -> list[Task]:
        """Retrieve all overdue pending tasks.

        Returns:
            List of pending Task objects with past due dates.
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT id, title, description, status, created_at, updated_at, due_date, project_id
                FROM tasks
                WHERE due_date < DATE('now', 'localtime') AND status = 'pending'
                ORDER BY due_date ASC, id ASC
                """
            )
            rows = cursor.fetchall()

        return [Task.from_row(row) for row in rows]

    def list_tasks_upcoming(self) -> list[Task]:
        """Retrieve all tasks due within the next 7 days.

        Returns:
            List of Task objects due within the next 7 days (including today).
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT
                    id, title, description, status, created_at, updated_at,
                    due_date, project_id
                FROM tasks
                WHERE due_date BETWEEN DATE('now', 'localtime')
                    AND DATE('now', 'localtime', '+7 days')
                ORDER BY due_date ASC, id ASC
                """
            )
            rows = cursor.fetchall()

        return [Task.from_row(row) for row in rows]

    def list_tasks_by_project(self, project_id: int) -> list[Task]:
        """Retrieve all tasks in a specific project.

        Args:
            project_id: The project ID to filter by.

        Returns:
            List of Task objects in the specified project.
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT id, title, description, status, created_at, updated_at, due_date, project_id
                FROM tasks
                WHERE project_id = ?
                ORDER BY id ASC
                """,
                (project_id,),
            )
            rows = cursor.fetchall()

        return [Task.from_row(row) for row in rows]

    def get_stats(self) -> TaskStats:
        """Get task statistics.

        Returns:
            TaskStats object with all metrics calculated.
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT
                    COUNT(*) as total,
                    SUM(CASE WHEN status = 'pending' THEN 1 ELSE 0 END)
                        as pending,
                    SUM(CASE WHEN status = 'done' THEN 1 ELSE 0 END)
                        as completed,
                    SUM(CASE WHEN due_date = DATE('now', 'localtime')
                        THEN 1 ELSE 0 END) as due_today,
                    SUM(CASE WHEN due_date < DATE('now', 'localtime')
                        AND status = 'pending' THEN 1 ELSE 0 END)
                        as overdue
                FROM tasks
                """
            )
            row = cursor.fetchone()

        return TaskStats(
            total=row["total"] or 0,
            pending=row["pending"] or 0,
            completed=row["completed"] or 0,
            due_today=row["due_today"] or 0,
            overdue=row["overdue"] or 0,
        )
