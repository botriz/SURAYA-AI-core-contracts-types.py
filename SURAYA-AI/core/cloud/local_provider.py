from __future__ import annotations

import shutil
from pathlib import Path
from typing import BinaryIO

from core.cloud.base import CloudFile


class LocalStorageProvider:
    """
    Provider محلی برای تست معماری Cloud Storage.

    در مراحل بعد Providerهای واقعی ابری به همین قرارداد
    متصل می‌شوند.
    """

    name = "local"

    def __init__(
        self,
        root: str = "data/cloud",
    ) -> None:

        self.root = Path(root)

        self.root.mkdir(
            parents=True,
            exist_ok=True,
        )

    def _safe_path(
        self,
        path: str,
    ) -> Path:

        candidate = (
            self.root / path
        ).resolve()

        root = self.root.resolve()

        if root not in candidate.parents and candidate != root:
            raise ValueError(
                "Invalid storage path."
            )

        return candidate

    def upload(
        self,
        source: BinaryIO,
        destination: str,
    ) -> CloudFile:

        target = self._safe_path(
            destination
        )

        target.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        with target.open(
            "wb"
        ) as output:

            shutil.copyfileobj(
                source,
                output,
            )

        return CloudFile(
            path=destination,
            size=target.stat().st_size,
            provider=self.name,
            metadata={},
        )

    def download(
        self,
        path: str,
    ) -> bytes:

        target = self._safe_path(
            path
        )

        if not target.exists():
            raise FileNotFoundError(
                path
            )

        return target.read_bytes()

    def delete(
        self,
        path: str,
    ) -> bool:

        target = self._safe_path(
            path
        )

        if not target.exists():
            return False

        target.unlink()

        return True

    def exists(
        self,
        path: str,
    ) -> bool:

        return self._safe_path(
            path
        ).exists()

    def list(
        self,
        prefix: str = "",
    ) -> list[CloudFile]:

        base = self._safe_path(
            prefix
        )

        if not base.exists():
            return []

        if base.is_file():
            files = [base]
        else:
            files = [
                path
                for path in base.rglob("*")
                if path.is_file()
            ]

        result = []

        for path in files:

            relative = path.relative_to(
                self.root
            ).as_posix()

            result.append(
                CloudFile(
                    path=relative,
                    size=path.stat().st_size,
                    provider=self.name,
                    metadata={},
                )
            )

        return result
