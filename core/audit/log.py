from __future__ import annotations

import json
import os
from pathlib import Path
from threading import Lock
from typing import Any

from core.contracts.types import EventType, utc_now


class AuditLog:
    """Append-only JSONL audit log with restrictive local file permissions."""

    def __init__(self, path: str = "data/audit.jsonl") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()
        if self.path.exists():
            os.chmod(self.path, 0o600)

    def append(self, event_type: EventType | str, payload: dict[str, Any]) -> dict[str, Any]:
        name = event_type.value if isinstance(event_type, EventType) else str(event_type)
        event = {"event_type": name, "payload": payload, "timestamp": utc_now()}
        encoded = json.dumps(event, ensure_ascii=False, separators=(",", ":"))
        with self._lock:
            descriptor = os.open(self.path, os.O_APPEND | os.O_CREAT | os.O_WRONLY, 0o600)
            try:
                os.write(descriptor, (encoded + "\n").encode("utf-8"))
            finally:
                os.close(descriptor)
        return event

    def read_all(self) -> list[dict[str, Any]]:
        if not self.path.exists():
            return []
        events: list[dict[str, Any]] = []
        with self._lock:
            for line in self.path.read_text(encoding="utf-8").splitlines():
                if not line.strip():
                    continue
                try:
                    value = json.loads(line)
                except json.JSONDecodeError:
                    continue
                if isinstance(value, dict):
                    events.append(value)
        return events
