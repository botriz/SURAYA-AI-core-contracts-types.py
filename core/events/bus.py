from __future__ import annotations

from collections import defaultdict
from threading import Lock
from typing import Any, Callable


EventHandler = Callable[[dict[str, Any]], None]


class EventBus:
    def __init__(self) -> None:
        self._handlers: dict[str, list[EventHandler]] = defaultdict(list)
        self._lock = Lock()

    def subscribe(
        self,
        event_name: str,
        handler: EventHandler,
    ) -> None:
        with self._lock:
            self._handlers[event_name].append(handler)

    def unsubscribe(
        self,
        event_name: str,
        handler: EventHandler,
    ) -> None:
        with self._lock:
            handlers = self._handlers.get(event_name, [])

            if handler in handlers:
                handlers.remove(handler)

    def publish(
        self,
        event_name: str,
        payload: dict[str, Any] | None = None,
    ) -> None:
        with self._lock:
            handlers = list(self._handlers.get(event_name, []))

        data = payload or {}

        for handler in handlers:
            handler(data)
