from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class ToolDefinition:
    name: str
    description: str
    handler: Callable[..., Any]


class ToolRegistry:
    """
    سیستم افزونه و ابزار SURAYA.

    ابزارها بدون تغییر در Core قابل اضافه شدن هستند.
    """

    def __init__(self) -> None:
        self._tools: dict[str, ToolDefinition] = {}

    def register(
        self,
        name: str,
        description: str,
        handler: Callable[..., Any],
    ) -> None:

        if not name:
            raise ValueError(
                "Tool name cannot be empty."
            )

        if not callable(handler):
            raise TypeError(
                "Tool handler must be callable."
            )

        if name in self._tools:
            raise ValueError(
                f"Tool '{name}' is already registered."
            )

        self._tools[name] = ToolDefinition(
            name=name,
            description=description,
            handler=handler,
        )

    def remove(
        self,
        name: str,
    ) -> None:

        self._tools.pop(name, None)

    def get(
        self,
        name: str,
    ) -> ToolDefinition:

        if name not in self._tools:
            raise KeyError(
                f"Tool '{name}' is not registered."
            )

        return self._tools[name]

    def exists(
        self,
        name: str,
    ) -> bool:

        return name in self._tools

    def list(
        self,
    ) -> list[ToolDefinition]:

        return list(
            self._tools.values()
        )
