from pathlib import Path

from core.contracts.types import (
    ActionRequest,
    Decision,
    RiskLevel,
)
from core.guardian.guardian import Guardian
from core.guardian.policy import GuardianPolicy
from core.runtime.container import create_container
from core.security.permissions import PermissionManager


def test_container_creation(tmp_path: Path):
    container = create_container(
        data_dir=str(tmp_path / "data"),
        audit_path=str(tmp_path / "audit.jsonl"),
    )

    assert container.runtime.running is True
    assert "local" in container.cloud.list_providers()
    assert container.tools.exists("echo")


def test_builtin_echo(tmp_path: Path):
    container = create_container(
        data_dir=str(tmp_path / "data"),
        audit_path=str(tmp_path / "audit.jsonl"),
    )

    result = container.runtime.handle_command(
        "hello",
    )

    assert result["success"] is True
    assert result["status"] == "completed"


def test_permissions():
    permissions = PermissionManager()

    permissions.register(
        "test.permission",
    )

    assert permissions.check(
        "test.permission"
    ) is False

    permissions.grant(
        "test.permission",
    )

    assert permissions.check(
        "test.permission"
    ) is True

    permissions.revoke(
        "test.permission",
    )

    assert permissions.check(
        "test.permission"
    ) is False


def test_guardian_blocks_tool():
    guardian = Guardian(
        GuardianPolicy(
            blocked_tools={"dangerous"},
        )
    )

    action = ActionRequest(
        tool="dangerous",
        action="execute",
        risk=RiskLevel.LOW,
    )

    report = guardian.inspect_action(action)

    assert report.decision == Decision.BLOCK


def test_guardian_requires_approval():
    guardian = Guardian(
        GuardianPolicy(
            max_risk_without_approval=RiskLevel.MEDIUM,
        )
    )

    action = ActionRequest(
        tool="test",
        action="execute",
        risk=RiskLevel.HIGH,
    )

    report = guardian.inspect_action(action)

    assert report.decision == Decision.REQUIRE_APPROVAL
    assert report.approval_request is not None


def test_approval_manager(tmp_path: Path):
    container = create_container(
        data_dir=str(tmp_path / "data"),
        audit_path=str(tmp_path / "audit.jsonl"),
    )

    action = container.brain.create_plan(
        "test",
    ).actions[0]

    request = container.guardian.approvals.create(
        action,
    )

    assert request.status.value == "pending"

    container.guardian.approvals.approve(
        request.id,
    )

    assert request.status.value == "approved"
