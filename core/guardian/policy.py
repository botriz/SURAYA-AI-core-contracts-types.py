from __future__ import annotations

from core.contracts.types import (
    ActionRequest,
    Decision,
    Plan,
    RiskLevel,
)


class GuardianPolicy:
    def __init__(
        self,
        max_risk_without_approval: RiskLevel = RiskLevel.MEDIUM,
        blocked_tools: set[str] | None = None,
        blocked_actions: set[str] | None = None,
    ) -> None:
        self.max_risk_without_approval = max_risk_without_approval
        self.blocked_tools = blocked_tools or set()
        self.blocked_actions = blocked_actions or set()

    def check_plan(
        self,
        plan: Plan,
    ) -> tuple[Decision, str]:
        if not plan.goal.strip():
            return Decision.BLOCK, "Plan goal is empty."

        if not plan.actions:
            return Decision.BLOCK, "Plan contains no actions."

        for action in plan.actions:
            decision, reason = self.check_action(action)

            if decision == Decision.BLOCK:
                return decision, reason

        return Decision.ALLOW, "Plan passed Guardian policy."

    def check_action(
        self,
        action: ActionRequest,
    ) -> tuple[Decision, str]:
        if action.tool in self.blocked_tools:
            return (
                Decision.BLOCK,
                f"Tool '{action.tool}' is blocked.",
            )

        if action.action in self.blocked_actions:
            return (
                Decision.BLOCK,
                f"Action '{action.action}' is blocked.",
            )

        if action.requires_approval:
            return (
                Decision.REQUIRE_APPROVAL,
                "Action explicitly requires Creator approval.",
            )

        if self._risk_value(action.risk) > self._risk_value(
            self.max_risk_without_approval
        ):
            return (
                Decision.REQUIRE_APPROVAL,
                f"Risk level '{action.risk.value}' requires approval.",
            )

        return Decision.ALLOW, "Action passed Guardian policy."

    @staticmethod
    def _risk_value(risk: RiskLevel) -> int:
        return {
            RiskLevel.LOW: 1,
            RiskLevel.MEDIUM: 2,
            RiskLevel.HIGH: 3,
            RiskLevel.CRITICAL: 4,
        }[risk]
