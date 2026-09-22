from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class MediaType(str, Enum):
    IMAGE = "image"
    AUDIO = "audio"
    VIDEO = "video"
    DOCUMENT = "document"


@dataclass
class MediaAsset:
    path: str
    media_type: MediaType
    mime_type: str = ""
    metadata: dict[str, str] = field(default_factory=dict)
