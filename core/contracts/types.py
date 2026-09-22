from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Decision(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"
    REQUIRE_APPROVAL = "require_approval"


class EventType(str, Enum):
    COMMAND_RECEIVED = "command_received"
    PLAN_CREATED = "plan_created"
    GUARDIAN_DECISION = "guardian_decision"
    ACTION_STARTED = "action_started"
    ACTION_COMPLETED = "action_completed"
    ACTION_BLOCKED = "action_blocked"
    ERROR = "error"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class CreatorCommand:
    command: str
    session_id: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=utc_now)


@dataclass
class ActionRequest:
    tool: str
    action: str
    parameters: dict[str, Any] = field(default_factory=dict)
    risk: RiskLevel = RiskLevel.LOW
    requires_approval: bool = False


@dataclass
class Plan:
    goal: str
    actions: list[ActionRequest] = field(default_factory=list)
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class GuardianDecision:
    decision: Decision
    reason: str
    approval_id: str | None = None


@dataclass
class ExecutionResult:
    success: bool
    output: Any = None
    error: str | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class AuditEvent:
    event_type: EventType
    payload: dict[str, Any]
    timestamp: str = field(default_factory=utc_now)
