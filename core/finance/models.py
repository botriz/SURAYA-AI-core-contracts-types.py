from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class TransactionType(str, Enum):
    INCOME = "income"
    EXPENSE = "expense"


@dataclass
class Transaction:
    amount: float
    currency: str
    transaction_type: TransactionType
    category: str = ""
    description: str = ""
    date: str = ""


@dataclass
class FinancialSnapshot:
    total_income: float
    total_expense: float
    net_cash_flow: float
    currency: str
    transactions: list[Transaction] = field(default_factory=list)
