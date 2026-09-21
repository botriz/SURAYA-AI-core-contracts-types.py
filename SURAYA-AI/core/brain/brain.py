from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from core.contracts.types import (
    ActionRequest,
    CreatorCommand,
    Plan,
    RiskLevel,
)
from core.memory.store import MemoryStore
from core.models.router import ModelRouter


@dataclass
class BrainResponse:
    goal: str
    plan: Plan
    explanation: str


class Brain:
    """
    مغز مرکزی SURAYA.

    وظایف:
    - دریافت فرمان Creator
    - درک هدف
    - استفاده از Memory
    - ساخت Plan
    - آماده‌سازی Plan برای Guardian

    Brain مستقیماً اجازه اجرای ابزار را ندارد.
    اجرای واقعی فقط بعد از عبور از Guardian انجام می‌شود.
    """

    def __init__(
        self,
        memory: Optional[MemoryStore] = None,
        model_router: Optional[ModelRouter] = None,
    ) -> None:

        self.memory = memory or MemoryStore()
        self.model_router = model_router or ModelRouter()

    def understand(
        self,
        command: CreatorCommand,
    ) -> str:

        text = command.text.strip()

        if not text:
            raise ValueError(
                "Creator command cannot be empty."
            )

        return text

    def create_plan(
        self,
        command: CreatorCommand,
    ) -> Plan:

        goal = self.understand(command)

        action = ActionRequest(
            name="echo_command",
            tool="echo",
            arguments={
                "text": goal,
            },
            risk=RiskLevel.LOW,
            requires_approval=False,
        )

        return Plan(
            goal=goal,
            actions=[action],
        )

    def process(
        self,
        command: CreatorCommand,
    ) -> BrainResponse:

        goal = self.understand(command)

        self.memory.put(
            "last_creator_command",
            {
                "command_id": command.command_id,
                "text": goal,
            },
        )

        plan = self.create_plan(
            command
        )

        return BrainResponse(
            goal=goal,
            plan=plan,
            explanation=(
                "Command understood and converted "
                "into an executable plan."
            ),
        )
