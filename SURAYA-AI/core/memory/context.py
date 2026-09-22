from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from core.memory.store import MemoryStore


@dataclass
class ContextMemory:
    store: MemoryStore
    session: dict[str, Any] = field(default_factory=dict)

    def remember(
        self,
        key: str,
        value: Any,
    ) -> None:

        self.session[key] = value

        self.store.put(
            key,
            value,
        )

    def recall(
        self,
        key: str,
        default: Any = None,
    ) -> Any:

        if key in self.session:
            return self.session[key]

        value = self.store.get(
            key,
            default,
        )

        if value is not default:
            self.session[key] = value

        return value

    def forget(
        self,
        key: str,
    ) -> bool:

        self.session.pop(
            key,
            None,
        )

        return self.store.delete(
            key
        )

    def clear_session(self) -> None:
        self.session.clear()
