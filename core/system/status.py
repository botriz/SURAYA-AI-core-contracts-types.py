from __future__ import annotations

from dataclasses import dataclass


@dataclass
class SystemStatus:
    name: str
    version: str
    runtime_running: bool
    emergency_stop: bool
    tool_count: int
    cloud_provider_count: int
    pending_approvals: int


def build_status(container) -> SystemStatus:
    return SystemStatus(
        name="SURAYA AI",
        version="0.4.0",
        runtime_running=container.runtime.running,
        emergency_stop=container.runtime.state.emergency_stop,
        tool_count=len(container.tools.list()),
        cloud_provider_count=len(
            container.cloud.list_providers()
        ),
        pending_approvals=len(
            container.guardian.approvals.pending()
        ),
    )
