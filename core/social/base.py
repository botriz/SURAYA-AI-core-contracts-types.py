from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol


@dataclass
class SocialAccount:
    platform: str
    account_id: str
    display_name: str = ""
    connected: bool = False
    metadata: dict[str, str] = field(default_factory=dict)


@dataclass
class SocialPost:
    text: str
    media: list[str] = field(default_factory=list)
    scheduled_at: str | None = None


class SocialProvider(Protocol):
    name: str

    def connect(self) -> SocialAccount:
        ...

    def publish(self, post: SocialPost) -> dict[str, object]:
        ...

    def analytics(self) -> dict[str, object]:
        ...
