from __future__ import annotations

from core.agents.base import Agent, AgentResult, AgentTask


class GuardianAgent(Agent):
    name = "guardian-agent"

    def __init__(self, guardian) -> None:
        self.guardian = guardian

    def execute(self, task: AgentTask) -> AgentResult:
        """
        Guardian agent is intentionally inspection-oriented.

        It does not execute arbitrary user tasks itself.
        """

        return AgentResult(
            success=True,
            output={
                "status": "inspection-ready",
                "goal": task.goal,
                "guardian": self.name,
            },
        )
