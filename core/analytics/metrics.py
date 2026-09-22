from __future__ import annotations

from dataclasses import dataclass
from threading import Lock


@dataclass
class Metric:
    name: str
    value: float
    count: int = 1


class Metrics:
    def __init__(self) -> None:
        self._values: dict[str, Metric] = {}
        self._lock = Lock()

    def increment(
        self,
        name: str,
        value: float = 1.0,
    ) -> Metric:
        with self._lock:
            metric = self._values.get(name)

            if metric is None:
                metric = Metric(
                    name=name,
                    value=value,
                    count=1,
                )
                self._values[name] = metric
            else:
                metric.value += value
                metric.count += 1

            return metric

    def set(
        self,
        name: str,
        value: float,
    ) -> Metric:
        with self._lock:
            metric = Metric(
                name=name,
                value=value,
                count=1,
            )
            self._values[name] = metric
            return metric

    def get(self, name: str) -> Metric | None:
        with self._lock:
            return self._values.get(name)

    def all(self) -> list[Metric]:
        with self._lock:
            return list(self._values.values())
