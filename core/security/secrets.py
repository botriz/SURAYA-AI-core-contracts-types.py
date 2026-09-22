from __future__ import annotations

import json
import os
from pathlib import Path
from threading import Lock
from typing import Any


class SecretStore:
    """
    Minimal local secret store abstraction.

    Production deployments should replace or extend this with
    Android Keystore / OS keychain / encrypted vault storage.
    """

    def __init__(self, path: str = "data/secrets.json") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = Lock()

    def _read(self) -> dict[str, str]:
        if not self.path.exists():
            return {}

        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError):
            return {}

    def _write(self, data: dict[str, str]) -> None:
        temporary = self.path.with_suffix(".tmp")
        temporary.write_text(
            json.dumps(data, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )
        os.replace(temporary, self.path)

    def set(self, key: str, value: str) -> None:
        if not key.strip():
            raise ValueError("Secret key cannot be empty.")

        with self._lock:
            data = self._read()
            data[key] = value
            self._write(data)

    def get(self, key: str) -> str | None:
        with self._lock:
            return self._read().get(key)

    def delete(self, key: str) -> bool:
        with self._lock:
            data = self._read()

            if key not in data:
                return False

            del data[key]
            self._write(data)
            return True

    def exists(self, key: str) -> bool:
        return self.get(key) is not None

    def list_keys(self) -> list[str]:
        with self._lock:
            return sorted(self._read().keys())
