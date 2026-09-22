from __future__ import annotations

from dataclasses import dataclass

from core.contracts.types import (
    ActionRequest,
    Decision,
    ExecutionResult,
    Plan,
)
from core.guardian.approval import ApprovalManager, ApprovalRequest
from core.guardian.policy import GuardianPolicy


@dataclass
class GuardianReport:
    decision: Decision
    reason: str
    approval_request: ApprovalRequest | None = None


class Guardian:
    def __init__(
        self,
        policy: GuardianPolicy | None = None,
        approvals: ApprovalManager | None = None,
    ) -> None:
        self.policy = policy or GuardianPolicy()
        self.approvals = approvals or ApprovalManager()

    def inspect_plan(self, plan: Plan) -> GuardianReport:
        decision, reason = self.policy.check_plan(plan)

        return GuardianReport(
            decision=decision,
            reason=reason,
        )

    def inspect_action(
        self,
        action: ActionRequest,
    ) -> GuardianReport:
        decision, reason = self.policy.check_action(action)

        if decision == Decision.REQUIRE_APPROVAL:
            approval = self.approvals.create(
                action,
                reason=reason,
            )

            return GuardianReport(
                decision=decision,
                reason=reason,
                approval_request=approval,
            )

        return GuardianReport(
            decision=decision,
            reason=reason,
        )

    def verify_result(
        self,
        result: ExecutionResult,
    ) -> GuardianReport:
        if not result.success:
            return GuardianReport(
                decision=Decision.BLOCK,
                reason=result.error or "Execution failed.",
            )

        return GuardianReport(
            decision=Decision.ALLOW,
            reason="Execution result verified.",
        )
