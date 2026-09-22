from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class RuntimeState:
    running: bool = True
    emergency_stop: bool = False
    active_task_id: str | None = None
    last_command: str | None = None
    last_result: str | None = None
    updated_at: str = field(default_factory=utc_now)

    def update(self) -> None:
        self.updated_at = utc_now()

    def stop(self) -> None:
        self.running = False
        self.update()

    def start(self) -> None:
        self.running = True
        self.emergency_stop = False
        self.update()

    def emergency_stop_now(self) -> None:
        self.emergency_stop = True
        self.running = False
        self.update()
