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
        with self._lock:
            existing = self._permissions.get(name)

            if existing is not None:
                return existing

            permission = Permission(
                name=name,
                description=description,
                granted=granted,
                metadata=metadata or {},
            )

            self._permissions[name] = permission
            return permission

    def grant(self, name: str) -> Permission:
        with self._lock:
            if name not in self._permissions:
                self.register(name)

            self._permissions[name].granted = True
            return self._permissions[name]

    def revoke(self, name: str) -> Permission:
        with self._lock:
            if name not in self._permissions:
                self.register(name)

            self._permissions[name].granted = False
            return self._permissions[name]

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
