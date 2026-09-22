from __future__ import annotations

from core.agents.base import Agent, AgentResult, AgentTask


class ExecutorAgent(Agent):
    name = "executor-agent"

    def __init__(self, runtime) -> None:
        self.runtime = runtime

    def execute(self, task: AgentTask) -> AgentResult:
        try:
            result = self.runtime.handle_command(
                task.goal,
                session_id=task.context.get("session_id"),
            )

            return AgentResult(
                success=True,
                output=result,
            )

        except Exception as exc:
            return AgentResult(
                success=False,
                error=str(exc),
            )
