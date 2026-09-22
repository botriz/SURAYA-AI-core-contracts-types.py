from __future__ import annotations

from core.finance.models import (
    FinancialSnapshot,
    Transaction,
    TransactionType,
)


class FinanceEngine:
    def summarize(
        self,
        transactions: list[Transaction],
        currency: str,
    ) -> FinancialSnapshot:
        income = sum(
            item.amount
            for item in transactions
            if item.transaction_type == TransactionType.INCOME
        )

        expense = sum(
            item.amount
            for item in transactions
            if item.transaction_type == TransactionType.EXPENSE
        )

        return FinancialSnapshot(
            total_income=income,
            total_expense=expense,
            net_cash_flow=income - expense,
            currency=currency,
            transactions=transactions,
        )

    def opportunity_framework(
        self,
        capital: float,
        expected_return: float,
        risk_level: str,
    ) -> dict[str, object]:
        """
        Analytical framework only.

        This does not execute financial transactions and does not
        guarantee investment returns.
        """

        return {
            "capital": capital,
            "expected_return_assumption": expected_return,
            "risk_level": risk_level,
            "projected_value": capital * (1 + expected_return),
            "requires_human_approval": True,
        }
