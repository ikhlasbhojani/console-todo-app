"""ProjectManager class for project CRUD operations with SQLite persistence.

This module provides the ProjectManager class which handles all database
interactions for project management.
"""

import sqlite3
from datetime import datetime
from pathlib import Path

from src.models import Project, Task


def get_default_db_path() -> str:
    """Get the default database path for global installation.

    Returns:
        Path to ~/.todo-app/todo.db for global installs.
    """
    home = Path.home()
    todo_app_dir = home / ".todo-app"
    return str(todo_app_dir / "todo.db")


class ProjectManager:
    """Manages projects with SQLite persistence.

    This class provides CRUD operations for projects and handles
    all database interactions.

    Attributes:
        db_path: Path to the SQLite database file.
    """

    def __init__(self, db_path: str | None = None) -> None:
        """Initialize the ProjectManager.

        Args:
            db_path: Path to SQLite database file.
                     Defaults to ~/.todo-app/todo.db for global installation.
        """
        if db_path is None:
            db_path = get_default_db_path()
        self.db_path = db_path

    def _get_connection(self) -> sqlite3.Connection:
        """Get a database connection with row factory configured.

        Returns:
            SQLite connection with Row factory enabled.
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def create_project(self, name: str, description: str = "") -> Project:
        """Create a new project.

        Args:
            name: Project name (required, unique, case-insensitive)
            description: Optional project description

        Returns:
            The newly created Project.

        Raises:
            ValueError: If name is empty or already exists.
        """
        stripped_name = name.strip()
        if not stripped_name:
            raise ValueError("Project name cannot be empty.")

        now = datetime.now()
        created_at = now.isoformat()

        with self._get_connection() as conn:
            try:
                cursor = conn.execute(
                    """
                    INSERT INTO projects (name, description, created_at)
                    VALUES (?, ?, ?)
                    """,
                    (stripped_name, description, created_at),
                )
                project_id = cursor.lastrowid
                conn.commit()
            except sqlite3.IntegrityError:
                raise ValueError("Project name already exists.")

        return Project(
            id=project_id,
            name=stripped_name,
            description=description,
            created_at=now,
        )

    def list_projects(self) -> list[Project]:
        """Retrieve all projects with task counts.

        Returns:
            List of all Project objects with task_count populated.
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT p.id, p.name, p.description, p.created_at,
                       COUNT(t.id) as task_count
                FROM projects p
                LEFT JOIN tasks t ON p.id = t.project_id
                GROUP BY p.id
                ORDER BY p.id ASC
                """
            )
            rows = cursor.fetchall()

        projects = [Project.from_row(row) for row in rows]
        return projects

    def get_project(self, name: str) -> Project | None:
        """Retrieve a project by name (case-insensitive).

        Args:
            name: The project name to look up.

        Returns:
            The Project if found, None otherwise.
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT p.id, p.name, p.description, p.created_at,
                       COUNT(t.id) as task_count
                FROM projects p
                LEFT JOIN tasks t ON p.id = t.project_id
                WHERE p.name = ? COLLATE NOCASE
                GROUP BY p.id
                """,
                (name.strip(),),
            )
            row = cursor.fetchone()

        if row is None:
            return None

        return Project.from_row(row)

    def get_project_by_id(self, project_id: int) -> Project | None:
        """Retrieve a project by ID.

        Args:
            project_id: The unique identifier of the project.

        Returns:
            The Project if found, None otherwise.
        """
        with self._get_connection() as conn:
            cursor = conn.execute(
                """
                SELECT p.id, p.name, p.description, p.created_at,
                       COUNT(t.id) as task_count
                FROM projects p
                LEFT JOIN tasks t ON p.id = t.project_id
                WHERE p.id = ?
                GROUP BY p.id
                """,
                (project_id,),
            )
            row = cursor.fetchone()

        if row is None:
            return None

        return Project.from_row(row)

    def delete_project(self, name: str, cascade: bool = False) -> tuple[bool, int]:
        """Delete a project.

        Args:
            name: The project name to delete.
            cascade: If True, delete all associated tasks.

        Returns:
            Tuple of (success, deleted_task_count).
            Returns (False, 0) if project not found.
        """
        project = self.get_project(name)
        if project is None:
            return (False, 0)

        task_count = project.task_count

        with self._get_connection() as conn:
            if cascade and task_count > 0:
                # Delete associated tasks first
                conn.execute(
                    "DELETE FROM tasks WHERE project_id = ?",
                    (project.id,),
                )

            # Delete the project
            conn.execute(
                "DELETE FROM projects WHERE id = ?",
                (project.id,),
            )
            conn.commit()

        return (True, task_count if cascade else 0)

    def get_tasks_by_project(self, project_id: int) -> list[Task]:
        """Retrieve all tasks in a project.

        Args:
            project_id: The project ID to filter by.

        Returns:
            List of Task objects in the project.
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

        tasks = [Task.from_row(row) for row in rows]
        return tasks
