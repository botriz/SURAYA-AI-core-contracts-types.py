from __future__ import annotations

from dataclasses import dataclass
from typing import FrozenSet

from core.contracts.types import (
    ActionRequest,
    Decision,
    GuardianDecision,
    Plan,
    RiskLevel,
)


@dataclass(frozen=True)
class GuardianPolicy:
    """
    سیاست پایه Guardian.

    Guardian از Executor بالاتر است و Executor نمی‌تواند
    این سیاست‌ها را در زمان اجرا تغییر دهد.
    """

    max_risk_without_approval: RiskLevel = RiskLevel.MEDIUM

    blocked_tools: FrozenSet[str] = frozenset()

    blocked_actions: FrozenSet[str] = frozenset()

    def check_plan(self, plan: Plan) -> GuardianDecision:
        if not plan.actions:
            return GuardianDecision(
                decision=Decision.BLOCK,
                reason="Plan contains no executable actions.",
                plan_id=plan.plan_id,
            )

        for action in plan.actions:
            decision = self.check_action(
                action=action,
                plan_id=plan.plan_id,
            )

            if decision.decision != Decision.ALLOW:
                return decision

        return GuardianDecision(
            decision=Decision.ALLOW,
            reason="Plan passed Guardian precheck.",
            plan_id=plan.plan_id,
        )

    def check_action(
        self,
        action: ActionRequest,
        plan_id: str | None = None,
    ) -> GuardianDecision:

        if action.tool in self.blocked_tools:
            return GuardianDecision(
                decision=Decision.BLOCK,
                reason=f"Tool '{action.tool}' is blocked by Guardian policy.",
                plan_id=plan_id,
                action_name=action.name,
                risk=action.risk,
            )

        if action.name in self.blocked_actions:
            return GuardianDecision(
                decision=Decision.BLOCK,
                reason=f"Action '{action.name}' is blocked by Guardian policy.",
                plan_id=plan_id,
                action_name=action.name,
                risk=action.risk,
            )

        if action.requires_approval:
            return GuardianDecision(
                decision=Decision.APPROVAL_REQUIRED,
                reason="Creator approval is required for this action.",
                plan_id=plan_id,
                action_name=action.name,
                risk=action.risk,
            )

        if self._risk_value(action.risk) > self._risk_value(
            self.max_risk_without_approval
        ):
            return GuardianDecision(
                decision=Decision.APPROVAL_REQUIRED,
                reason=(
                    f"Risk level '{action.risk.value}' exceeds "
                    "the automatic execution threshold."
                ),
                plan_id=plan_id,
                action_name=action.name,
                risk=action.risk,
            )

        return GuardianDecision(
            decision=Decision.ALLOW,
            reason="Action passed Guardian policy.",
            plan_id=plan_id,
            action_name=action.name,
            risk=action.risk,
        )

    @staticmethod
    def _risk_value(level: RiskLevel) -> int:
        return {
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.HIGH: 3,
            RiskLevel.CRITICAL: 4,
        }[level]
