from __future__ import annotations

import json
import sqlite3
from pathlib import Path
from typing import Any


class MemoryStore:
    """
    حافظه پایدار اولیه SURAYA.

    در نسخه‌های بعدی این لایه به حافظه بلندمدت،
    Vector Store، Knowledge Graph و Cloud Memory
    متصل خواهد شد.
    """

    def __init__(
        self,
        database_path: str = "data/suraya_memory.db",
    ) -> None:

        self.path = Path(database_path)

        self.path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        self._initialize()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(
            self.path
        )

        connection.row_factory = sqlite3.Row

        return connection

    def _initialize(self) -> None:

        with self._connect() as db:

            db.execute(
                """
                CREATE TABLE IF NOT EXISTS memories (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    key TEXT NOT NULL UNIQUE,
                    value TEXT NOT NULL,
                    created_at TEXT NOT NULL
                        DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL
                        DEFAULT CURRENT_TIMESTAMP
                )
                """
            )

            db.commit()

    def put(
        self,
        key: str,
        value: Any,
    ) -> None:

        encoded = json.dumps(
            value,
            ensure_ascii=False,
        )

        with self._connect() as db:

            db.execute(
                """
                INSERT INTO memories (
                    key,
                    value
                )
                VALUES (?, ?)

                ON CONFLICT(key)
                DO UPDATE SET
                    value = excluded.value,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    key,
                    encoded,
                ),
            )

            db.commit()

    def get(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        with self._connect() as db:

            row = db.execute(
                """
                SELECT value
                FROM memories
                WHERE key = ?
                """,
                (key,),
            ).fetchone()

        if row is None:
            return default

        return json.loads(
            row["value"]
        )

    def delete(
        self,
        key: str,
    ) -> bool:

        with self._connect() as db:

            cursor = db.execute(
                """
                DELETE FROM memories
                WHERE key = ?
                """,
                (key,),
            )

            db.commit()

            return cursor.rowcount > 0

    def exists(
        self,
        key: str,
    ) -> bool:

        with self._connect() as db:

            row = db.execute(
                """
                SELECT 1
                FROM memories
                WHERE key = ?
                LIMIT 1
                """,
                (key,),
            ).fetchone()

        return row is not None
