from __future__ import annotations

from dataclasses import dataclass, field

from core.brain.intent import Intent, IntentType
from core.contracts.types import ActionRequest, Plan, RiskLevel


@dataclass
class PlanningContext:
    session_id: str | None = None
    metadata: dict[str, str] = field(default_factory=dict)


class Planner:
    def create_plan(
        self,
        command: str,
        intent: Intent,
        context: PlanningContext | None = None,
    ) -> Plan:
        actions: list[ActionRequest] = []

        if intent.type in {
            IntentType.CHAT,
            IntentType.QUESTION,
            IntentType.UNKNOWN,
        }:
            actions.append(
                ActionRequest(
                    tool="echo",
                    action="respond",
                    parameters={
                        "value": command,
                    },
                    risk=RiskLevel.LOW,
                    requires_approval=False,
                )
            )

        elif intent.type == IntentType.MEMORY:
            actions.append(
                ActionRequest(
                    tool="echo",
                    action="memory_request",
                    parameters={
                        "value": command,
                    },
                    risk=RiskLevel.LOW,
                    requires_approval=False,
                )
            )

        else:
            actions.append(
                ActionRequest(
                    tool="echo",
                    action="planned_task",
                    parameters={
                        "value": command,
                        "intent": intent.type.value,
                    },
                    risk=RiskLevel.LOW,
                    requires_approval=False,
                )
            )

        return Plan(
            goal=command,
            actions=actions,
            metadata={
                "intent": intent.type.value,
                "confidence": str(intent.confidence),
                "session_id": (
                    context.session_id
                    if context and context.session_id
                    else ""
                ),
            },
        )
