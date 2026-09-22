from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime, timezone
from uuid import uuid4


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class ResearchSource:
    title: str
    url: str = ""
    content: str = ""
    credibility: float | None = None


@dataclass
class ResearchResult:
    id: str
    question: str
    findings: list[str] = field(default_factory=list)
    sources: list[ResearchSource] = field(default_factory=list)
    limitations: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)


class ResearchEngine:
    """
    Research orchestration layer.

    External search and scientific tooling will be connected later.
    """

    def create_result(
        self,
        question: str,
        findings: list[str] | None = None,
        sources: list[ResearchSource] | None = None,
        limitations: list[str] | None = None,
    ) -> ResearchResult:
        return ResearchResult(
            id=str(uuid4()),
            question=question,
            findings=findings or [],
            sources=sources or [],
            limitations=limitations or [],
        )

    def build_hypotheses(
        self,
        question: str,
        count: int = 3,
    ) -> list[str]:
        count = max(1, min(count, 10))

        return [
            f"Hypothesis {index}: investigate a plausible explanation for: {question}"
            for index in range(1, count + 1)
        ]
