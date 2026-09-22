from __future__ import annotations

from core.audit.log import AuditLog
from core.brain.brain import Brain
from core.contracts.types import Decision, EventType
from core.executor.runtime import Executor
from core.guardian.guardian import Guardian
from core.runtime.state import RuntimeState
from core.tools.registry import ToolRegistry


class SurayaRuntime:
    def __init__(
        self,
        brain: Brain,
        guardian: Guardian,
        executor: Executor,
        tools: ToolRegistry,
        audit: AuditLog,
    ) -> None:
        self.brain = brain
        self.guardian = guardian
        self.executor = executor
        self.tools = tools
        self.audit = audit
        self.state = RuntimeState()

    @property
    def running(self) -> bool:
        return self.state.running and not self.state.emergency_stop

    def handle_command(
        self,
        command: str,
        session_id: str | None = None,
    ) -> dict:
        if not self.running:
            raise RuntimeError("SURAYA runtime is stopped.")

        self.state.last_command = command
        self.state.update()

        response = self.brain.process(
            command,
            session_id=session_id,
        )

        plan = response.plan

        self.audit.append(
            EventType.PLAN_CREATED,
            {
                "goal": plan.goal,
                "actions": len(plan.actions),
            },
        )

        plan_report = self.guardian.inspect_plan(plan)

        self.audit.append(
            EventType.GUARDIAN_DECISION,
            {
                "decision": plan_report.decision.value,
                "reason": plan_report.reason,
            },
        )

        if plan_report.decision == Decision.BLOCK:
            return {
                "success": False,
                "status": "blocked",
                "reason": plan_report.reason,
            }

        results = []

        for action in plan.actions:
            if not self.running:
                return {
                    "success": False,
                    "status": "stopped",
                    "results": results,
                }

            action_report = self.guardian.inspect_action(action)

            if action_report.decision == Decision.BLOCK:
                results.append(
                    {
                        "tool": action.tool,
                        "status": "blocked",
                        "reason": action_report.reason,
                    }
                )
                continue

            if action_report.decision == Decision.REQUIRE_APPROVAL:
                results.append(
                    {
                        "tool": action.tool,
                        "status": "approval_required",
                        "reason": action_report.reason,
                        "approval_id": (
                            action_report.approval_request.id
                            if action_report.approval_request
                            else None
                        ),
                    }
                )
                continue

            try:
                execution = self.executor.execute(
                    action.tool,
                    action.parameters,
                )

                verification = self.guardian.verify_result(execution)

                results.append(
                    {
                        "tool": action.tool,
                        "success": execution.success,
                        "output": execution.output,
                        "error": execution.error,
                        "guardian": verification.decision.value,
                    }
                )

            except Exception as exc:
                results.append(
                    {
                        "tool": action.tool,
                        "success": False,
                        "error": str(exc),
                    }
                )

        self.state.last_result = "completed"
        self.state.update()

        return {
            "success": True,
            "status": "completed",
            "goal": plan.goal,
            "results": results,
        }

    def stop(self) -> None:
        self.state.stop()

    def start(self) -> None:
        self.state.start()

    def emergency_stop(self) -> None:
        self.state.emergency_stop_now()
