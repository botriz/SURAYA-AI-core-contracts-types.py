from __future__ import annotations

from dataclasses import asdict
from typing import Any

from core.audit.log import AuditLog
from core.brain.brain import Brain
from core.contracts.types import (
    AuditEvent,
    CreatorCommand,
    EventType,
)
from core.executor.runtime import Executor
from core.guardian.guardian import Guardian
from core.tools.registry import ToolRegistry


class SurayaRuntime:
    """
    هسته اجرایی اصلی SURAYA.

    مسیر اصلی:

    Creator
        ↓
    Brain
        ↓
    Guardian Precheck
        ↓
    Executor
        ↓
    Guardian Verification
        ↓
    Result
    """

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

        self._running = True

    def stop(self) -> None:
        """
        توقف اضطراری Runtime.
        """

        self._running = False

    def start(self) -> None:
        """
        فعال‌سازی مجدد Runtime.
        """

        self._running = True

    @property
    def running(self) -> bool:
        return self._running

    def handle_command(
        self,
        text: str,
    ) -> dict[str, Any]:

        if not self._running:
            return {
                "status": "stopped",
                "reason": "SURAYA runtime is stopped by Guardian.",
            }

        command = CreatorCommand(
            text=text,
        )

        self.audit.append(
            AuditEvent(
                event_type=EventType.COMMAND,
                actor="creator",
                payload={
                    "command_id": command.command_id,
                    "text": command.text,
                },
            )
        )

        response = self.brain.process(
            command
        )

        plan = response.plan

        self.audit.append(
            AuditEvent(
                event_type=EventType.PLAN,
                actor="brain",
                payload={
                    "plan_id": plan.plan_id,
                    "goal": plan.goal,
                    "actions": [
                        {
                            "name": action.name,
                            "tool": action.tool,
                            "risk": action.risk.value,
                        }
                        for action in plan.actions
                    ],
                },
            )
        )

        guardian_report = self.guardian.inspect_plan(
            plan
        )

        self.audit.append(
            AuditEvent(
                event_type=EventType.GUARDIAN_PRECHECK,
                actor="guardian",
                payload=asdict(
                    guardian_report
                ),
            )
        )

        if not guardian_report.allowed:

            return {
                "status": "blocked",
                "stage": "guardian_precheck",
                "reason": guardian_report.reason,
                "plan_id": plan.plan_id,
            }

        results = []

        for action in plan.actions:

            if not self._running:

                return {
                    "status": "stopped",
                    "stage": "execution",
                    "reason": (
                        "Runtime was stopped by Guardian "
                        "before action execution."
                    ),
                    "plan_id": plan.plan_id,
                }

            decision = self.guardian.inspect_action(
                action=action,
                plan_id=plan.plan_id,
            )

            if decision.decision.value != "allow":

                self.audit.append(
                    AuditEvent(
                        event_type=EventType.GUARDIAN_MONITOR,
                        actor="guardian",
                        payload=asdict(
                            decision
                        ),
                    )
                )

                return {
                    "status": decision.decision.value,
                    "stage": "guardian_action_check",
                    "reason": decision.reason,
                    "plan_id": plan.plan_id,
                    "action": action.name,
                }

            result = self.executor.execute(
                action
            )

            self.audit.append(
                AuditEvent(
                    event_type=EventType.ACTION,
                    actor="executor",
                    payload={
                        "action": action.name,
                        "success": result.success,
                        "output": result.output,
                        "error": result.error,
                    },
                )
            )

            verification = self.guardian.verify_result(
                result
            )

            self.audit.append(
                AuditEvent(
                    event_type=EventType.VERIFICATION,
                    actor="guardian",
                    payload=asdict(
                        verification
                    ),
                )
            )

            if not verification.execution_verified:

                return {
                    "status": "blocked",
                    "stage": "guardian_verification",
                    "reason": verification.reason,
                    "plan_id": plan.plan_id,
                    "action": action.name,
                    "error": result.error,
                }

            results.append(
                {
                    "action": action.name,
                    "output": result.output,
                }
            )

        final_result = {
            "status": "completed",
            "plan_id": plan.plan_id,
            "goal": plan.goal,
            "results": results,
            "guardian": {
                "precheck": "passed",
                "verification": "passed",
            },
        }

        self.audit.append(
            AuditEvent(
                event_type=EventType.REPORT,
                actor="guardian",
                payload=final_result,
            )
        )

        return final_result
