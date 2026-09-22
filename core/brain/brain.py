from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.brain.intent import detect_intent
from core.brain.planner import Planner, PlanningContext
from core.contracts.types import Plan
from core.memory.store import MemoryStore
from core.models.router import ModelRouter


@dataclass
class BrainResponse:
    command: str
    answer: str
    plan: Plan
    metadata: dict[str, Any]


class Brain:
    def __init__(
        self,
        memory: MemoryStore,
        model_router: ModelRouter,
        planner: Planner | None = None,
    ) -> None:
        self.memory = memory
        self.model_router = model_router
        self.planner = planner or Planner()

    def understand(self, command: str):
        return detect_intent(command)

    def create_plan(
        self,
        command: str,
        session_id: str | None = None,
    ) -> Plan:
        intent = self.understand(command)

        return self.planner.create_plan(
            command=command,
            intent=intent,
            context=PlanningContext(
                session_id=session_id,
            ),
        )

    def process(
        self,
        command: str,
        session_id: str | None = None,
    ) -> BrainResponse:
        if not command.strip():
            raise ValueError("Command cannot be empty.")

        plan = self.create_plan(
            command,
            session_id=session_id,
        )

        intent = self.understand(command)

        return BrainResponse(
            command=command,
            answer=command,
            plan=plan,
            metadata={
                "intent": intent.type.value,
                "confidence": intent.confidence,
                "session_id": session_id,
            },
      )
