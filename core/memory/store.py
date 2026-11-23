from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from threading import RLock
from typing import Any


class MemoryStore:
    """Small SQLite-backed key/value memory store for local single-instance use."""

    def __init__(self, path: str = "data/memory.db") -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = RLock()
        self._connection = sqlite3.connect(self.path, check_same_thread=False)
        self._connection.execute("PRAGMA journal_mode=WAL")
        self._connection.execute("PRAGMA synchronous=FULL")
        self._connection.execute(
            """
            CREATE TABLE IF NOT EXISTS memory (
                key TEXT PRIMARY KEY,
                value_json TEXT NOT NULL,
                updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        self._connection.commit()

    def put(self, key: str, value: Any) -> None:
        normalized = str(key).strip()
        if not normalized:
            raise ValueError("Memory key cannot be empty.")
        encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":"))
        with self._lock:
            self._connection.execute(
                """
                INSERT INTO memory(key, value_json, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(key) DO UPDATE SET
                    value_json=excluded.value_json,
                    updated_at=CURRENT_TIMESTAMP
                """,
                (normalized, encoded),
            )
            self._connection.commit()

    def get(self, key: str) -> Any | None:
        with self._lock:
            row = self._connection.execute(
                "SELECT value_json FROM memory WHERE key = ?", (str(key),)
            ).fetchone()
        return json.loads(row[0]) if row else None

    def delete(self, key: str) -> bool:
        with self._lock:
            cursor = self._connection.execute("DELETE FROM memory WHERE key = ?", (str(key),))
            self._connection.commit()
            return cursor.rowcount > 0

    def close(self) -> None:
        with self._lock:
            self._connection.close()
