from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Optional
from uuid import uuid4
from datetime import datetime, timezone


class RiskLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class Decision(str, Enum):
    ALLOW = "allow"
    BLOCK = "block"
    APPROVAL_REQUIRED = "approval_required"


class EventType(str, Enum):
    COMMAND = "command"
    PLAN = "plan"
    GUARDIAN_PRECHECK = "guardian_precheck"
    ACTION = "action"
    GUARDIAN_MONITOR = "guardian_monitor"
    VERIFICATION = "verification"
    REPORT = "report"
    ERROR = "error"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass(frozen=True)
class CreatorCommand:
    text: str
    command_id: str = field(default_factory=lambda: str(uuid4()))
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ActionRequest:
    name: str
    tool: str
    arguments: Dict[str, Any] = field(default_factory=dict)
    risk: RiskLevel = RiskLevel.LOW
    requires_approval: bool = False


@dataclass(frozen=True)
class Plan:
    goal: str
    actions: List[ActionRequest]
    plan_id: str = field(default_factory=lambda: str(uuid4()))


@dataclass(frozen=True)
class GuardianDecision:
    decision: Decision
    reason: str
    plan_id: Optional[str] = None
    action_name: Optional[str] = None
    risk: RiskLevel = RiskLevel.LOW


@dataclass(frozen=True)
class ExecutionResult:
    success: bool
    action_name: str
    output: Any = None
    error: Optional[str] = None


@dataclass(frozen=True)
class AuditEvent:
    event_type: EventType
    actor: str
    payload: Dict[str, Any]
    event_id: str = field(default_factory=lambda: str(uuid4()))
    timestamp: str = field(default_factory=utc_now)
