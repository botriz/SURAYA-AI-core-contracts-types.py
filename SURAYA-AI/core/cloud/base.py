from __future__ import annotations

from dataclasses import dataclass
from typing import BinaryIO, Protocol


@dataclass(frozen=True)
class CloudFile:
    path: str
    size: int
    provider: str
    metadata: dict[str, str]


class CloudStorageProvider(Protocol):

    name: str

    def upload(
        self,
        source: BinaryIO,
        destination: str,
    ) -> CloudFile:
        ...

    def download(
        self,
        path: str,
    ) -> bytes:
        ...

    def delete(
        self,
        path: str,
    ) -> bool:
        ...

    def exists(
        self,
        path: str,
    ) -> bool:
        ...

    def list(
        self,
        prefix: str = "",
    ) -> list[CloudFile]:
        ...
