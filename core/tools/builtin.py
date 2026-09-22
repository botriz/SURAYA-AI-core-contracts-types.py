from __future__ import annotations

from typing import Any

from core.executor.runtime import Executor
from core.tools.registry import ToolDefinition, ToolRegistry


def echo_tool(value: Any = "") -> str:
    return str(value)


def register_builtin_tools(
    registry: ToolRegistry,
    executor: Executor,
) -> None:
    definition = ToolDefinition(
        name="echo",
        description="Returns the supplied value without modification.",
        risk="low",
        requires_approval=False,
        metadata={
            "builtin": True,
            "reversible": True,
        },
    )

    registry.register(definition)
    executor.register("echo", echo_tool)
