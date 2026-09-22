from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Project:
    id: str
    name: str
    description: str = ""
    status: str = "active"
    metadata: dict[str, str] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


class ProjectManager:
    def __init__(self) -> None:
        self._projects: dict[str, Project] = {}
        self._lock = Lock()

    def create(
        self,
        name: str,
        description: str = "",
        metadata: dict[str, str] | None = None,
    ) -> Project:
        project = Project(
            id=str(uuid4()),
            name=name,
            description=description,
            metadata=metadata or {},
        )

        with self._lock:
            self._projects[project.id] = project

        return project

    def get(self, project_id: str) -> Project | None:
        with self._lock:
            return self._projects.get(project_id)

    def update(
        self,
        project_id: str,
        *,
        name: str | None = None,
        description: str | None = None,
        status: str | None = None,
    ) -> Project:
        with self._lock:
            project = self._projects[project_id]

            if name is not None:
                project.name = name

            if description is not None:
                project.description = description

            if status is not None:
                project.status = status

            project.updated_at = utc_now()

            return project

    def delete(self, project_id: str) -> bool:
        with self._lock:
            if project_id not in self._projects:
                return False

            del self._projects[project_id]
            return True

    def list(self) -> list[Project]:
        with self._lock:
            return list(self._projects.values())
