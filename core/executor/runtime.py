from __future__ import annotations

from typing import Any, Callable, Dict

from core.contracts.types import (
    ActionRequest,
    ExecutionResult,
)


class Executor:
    """
    موتور اجرای SURAYA.

    Executor فقط عملیاتی را اجرا می‌کند که Guardian
    قبلاً اجازه اجرای آن را داده باشد.
    """

    def __init__(self) -> None:
        self._handlers: Dict[str, Callable[..., Any]] = {}

    def register(
        self,
        tool_name: str,
        handler: Callable[..., Any],
    ) -> None:

        if not tool_name:
            raise ValueError("Tool name cannot be empty.")

        if not callable(handler):
            raise TypeError("Handler must be callable.")

        self._handlers[tool_name] = handler

    def unregister(self, tool_name: str) -> None:
        self._handlers.pop(tool_name, None)

    def has_tool(self, tool_name: str) -> bool:
        return tool_name in self._handlers

    def execute(
        self,
        action: ActionRequest,
    ) -> ExecutionResult:

        handler = self._handlers.get(action.tool)

        if handler is None:
            return ExecutionResult(
                success=False,
                action_name=action.name,
                error=f"Tool '{action.tool}' is not registered.",
            )

        try:
            output = handler(**action.arguments)

            return ExecutionResult(
                success=True,
                action_name=action.name,
                output=output,
            )

        except Exception as exc:
            return ExecutionResult(
                success=False,
                action_name=action.name,
                error=str(exc),
            )
