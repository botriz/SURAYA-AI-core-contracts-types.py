from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from threading import Lock
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class KnowledgeItem:
    id: str
    title: str
    content: str
    source: str = ""
    tags: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)
    updated_at: str = field(default_factory=utc_now)


class KnowledgeBase:
    def __init__(self) -> None:
        self._items: dict[str, KnowledgeItem] = {}
        self._lock = Lock()

    def add(
        self,
        title: str,
        content: str,
        source: str = "",
        tags: list[str] | None = None,
    ) -> KnowledgeItem:
        item = KnowledgeItem(
            id=str(uuid4()),
            title=title,
            content=content,
            source=source,
            tags=tags or [],
        )

        with self._lock:
            self._items[item.id] = item

        return item

    def get(self, item_id: str) -> KnowledgeItem | None:
        with self._lock:
            return self._items.get(item_id)

    def delete(self, item_id: str) -> bool:
        with self._lock:
            if item_id not in self._items:
                return False

            del self._items[item_id]
            return True

    def search(self, query: str) -> list[KnowledgeItem]:
        normalized = query.strip().lower()

        if not normalized:
            return []

        with self._lock:
            results = []

            for item in self._items.values():
                haystack = " ".join(
                    [
                        item.title,
                        item.content,
                        item.source,
                        " ".join(item.tags),
                    ]
                ).lower()

                if normalized in haystack:
                    results.append(item)

            return results

    def list(self) -> list[KnowledgeItem]:
        with self._lock:
            return list(self._items.values())
