from __future__ import annotations

from dataclasses import dataclass, field
from threading import Lock
from typing import Any


@dataclass
class ToolDefinition:
    name: str
    description: str
    risk: str = "low"
    requires_approval: bool = False
    permissions: list[str] = field(default_factory=list)
    reversible: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}
        self._lock = Lock()

    def register(self, tool: ToolDefinition) -> ToolDefinition:
        if not tool.name.strip():
            raise ValueError("Tool name cannot be empty.")

        with self._lock:
            self._tools[tool.name] = tool

        return tool

    def remove(self, name: str) -> bool:
        with self._lock:
            return self._tools.pop(name, None) is not None

    def get(self, name: str) -> ToolDefinition | None:
        with self._lock:
            return self._tools.get(name)

    def exists(self, name: str) -> bool:
        return self.get(name) is not None

    def list(self) -> list[ToolDefinition]:
        with self._lock:
            return list(self._tools.values())
