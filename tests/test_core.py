from core.guardian.approval import ApprovalManager
from core.runtime.container import create_container
from core.security.permissions import PermissionManager


def test_container_creation():
    container = create_container(
        data_dir="data/test",
        audit_path="data/test/audit.jsonl",
    )

    assert container.runtime.running is True
    assert "local" in container.cloud.list_providers()


def test_builtin_echo():
    container = create_container(
        data_dir="data/test_echo",
        audit_path="data/test_echo/audit.jsonl",
    )

    result = container.runtime.handle_command(
        "hello",
    )

    assert result["success"] is True


def test_permissions():
    permissions = PermissionManager()

    permissions.register(
        "test.permission",
    )

    assert permissions.check("test.permission") is False

    permissions.grant(
        "test.permission",
    )

    assert permissions.check("test.permission") is True

    permissions.revoke(
        "test.permission",
    )

    assert permissions.check("test.permission") is False


def test_approval_manager():
    container = create_container(
        data_dir="data/test_approval",
        audit_path="data/test_approval/audit.jsonl",
    )

    action = container.brain.create_plan(
        "test",
    ).actions[0]

    approvals = ApprovalManager()
    request = approvals.create(action)

    assert request.status.value == "pending"

    approvals.approve(request.id)

    assert request.status.value == "approved"
