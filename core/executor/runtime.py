from __future__ import annotations

from typing import Any, Callable

from core.contracts.types import ExecutionResult


ToolHandler = Callable[..., Any]


class Executor:
    def __init__(self) -> None:
        self._handlers: dict[str, ToolHandler] = {}

    def register(
        self,
        name: str,
        handler: ToolHandler,
    ) -> None:
        if not name.strip():
            raise ValueError("Tool name cannot be empty.")

        self._handlers[name] = handler

    def unregister(self, name: str) -> bool:
        return self._handlers.pop(name, None) is not None

    def has_tool(self, name: str) -> bool:
        return name in self._handlers

    def execute(
        self,
        tool: str,
        parameters: dict[str, Any] | None = None,
    ) -> ExecutionResult:
        handler = self._handlers.get(tool)

        if handler is None:
            return ExecutionResult(
                success=False,
                error=f"Tool '{tool}' is not registered.",
            )

        try:
            output = handler(**(parameters or {}))

            return ExecutionResult(
                success=True,
                output=output,
            )

        except Exception as exc:
            return ExecutionResult(
                success=False,
                error=str(exc),
            )
