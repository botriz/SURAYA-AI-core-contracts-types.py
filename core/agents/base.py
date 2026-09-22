from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class AgentTask:
    goal: str
    context: dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentResult:
    success: bool
    output: Any = None
    error: str | None = None


class Agent:
    name = "base-agent"

    def execute(self, task: AgentTask) -> AgentResult:
        raise NotImplementedError
