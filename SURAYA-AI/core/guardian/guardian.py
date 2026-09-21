from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from core.contracts.types import (
    ActionRequest,
    Decision,
    ExecutionResult,
    GuardianDecision,
    Plan,
    RiskLevel,
)
from core.guardian.policy import GuardianPolicy


@dataclass(frozen=True)
class GuardianReport:
    allowed: bool
    decision: Decision
    reason: str
    plan_id: str
    checked_actions: int
    blocked_actions: int
    execution_verified: bool = False


class Guardian:
    """
    لایه مستقل نظارت و کنترل SURAYA.

    Guardian:
    - Plan را قبل از اجرا بررسی می‌کند.
    - هر Action را بررسی می‌کند.
    - نتیجه Executor را بررسی می‌کند.
    - در صورت مشاهده خطا، نتیجه را تأیید نمی‌کند.
    """

    def __init__(
        self,
        policy: GuardianPolicy | None = None,
    ) -> None:
        self.policy = policy or GuardianPolicy()

    def inspect_plan(
        self,
        plan: Plan,
    ) -> GuardianReport:

        decision = self.policy.check_plan(plan)

        blocked = 0

        if decision.decision != Decision.ALLOW:
            blocked = 1

        return GuardianReport(
            allowed=decision.decision == Decision.ALLOW,
            decision=decision.decision,
            reason=decision.reason,
            plan_id=plan.plan_id,
            checked_actions=len(plan.actions),
            blocked_actions=blocked,
        )

    def inspect_action(
        self,
        action: ActionRequest,
        plan_id: str,
    ) -> GuardianDecision:

        return self.policy.check_action(
            action=action,
            plan_id=plan_id,
        )

    def verify_result(
        self,
        result: ExecutionResult,
    ) -> GuardianReport:

        if not result.success:

            return GuardianReport(
                allowed=False,
                decision=Decision.BLOCK,
                reason=(
                    "Executor reported an execution failure. "
                    "Guardian did not approve the result."
                ),
                plan_id="",
                checked_actions=1,
                blocked_actions=1,
                execution_verified=False,
            )

        return GuardianReport(
            allowed=True,
            decision=Decision.ALLOW,
            reason="Execution result passed basic Guardian verification.",
            plan_id="",
            checked_actions=1,
            blocked_actions=0,
            execution_verified=True,
        )
