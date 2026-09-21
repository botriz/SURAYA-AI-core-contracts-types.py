from __future__ import annotations

import json
from pathlib import Path
from threading import Lock

from core.contracts.types import AuditEvent


class AuditLog:
    """
    ثبت غیرقابل‌حذف جریان عملیاتی اصلی SURAYA.

    در نسخه‌های بعدی امکان ارسال Audit به فضای ابری
    نیز اضافه خواهد شد.
    """

    def __init__(
        self,
        path: str = "data/audit.jsonl",
    ) -> None:

        self.path = Path(path)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._lock = Lock()

    def append(
        self,
        event: AuditEvent,
    ) -> None:

        record = {
            "event_id": event.event_id,
            "timestamp": event.timestamp,
            "event_type": event.event_type.value,
            "actor": event.actor,
            "payload": event.payload,
        }

        line = json.dumps(
            record,
            ensure_ascii=False,
        )

        with self._lock:

            with self.path.open(
                "a",
                encoding="utf-8",
            ) as file:

                file.write(
                    line + "\n"
                )

    def read_all(self) -> list[dict]:

        if not self.path.exists():
            return []

        records = []

        with self.path.open(
            "r",
            encoding="utf-8",
        ) as file:

            for line in file:

                line = line.strip()

                if not line:
                    continue

                records.append(
                    json.loads(line)
                )

        return records
