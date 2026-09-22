from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock


@dataclass
class Permission:
    name: str
    description: str = ""
    granted: bool = False
    metadata: dict[str, str] = field(default_factory=dict)


class PermissionManager:
    def __init__(self) -> None:
        self._permissions: dict[str, Permission] = {}
        self._lock = Lock()

    def register(
        self,
        name: str,
        description: str = "",
        granted: bool = False,
        metadata: dict[str, str] | None = None,
    ) -> Permission:
        permission = Permission(
            name=name,
            description=description,
            granted=granted,
            metadata=metadata or {},
        )

        with self._lock:
            self._permissions[name] = permission

        return permission

    def grant(self, name: str) -> Permission:
        with self._lock:
            permission = self._permissions[name]
            permission.granted = True
            return permission

    def revoke(self, name: str) -> Permission:
        with self._lock:
            permission = self._permissions[name]
            permission.granted = False
            return permission

    def check(self, name: str) -> bool:
        with self._lock:
            permission = self._permissions.get(name)
            return bool(permission and permission.granted)

    def get(self, name: str) -> Permission | None:
        with self._lock:
            return self._permissions.get(name)

    def list(self) -> list[Permission]:
        with self._lock:
            return list(self._permissions.values())
