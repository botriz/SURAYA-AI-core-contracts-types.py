from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass
class CodeInspection:
    path: str
    exists: bool
    is_file: bool
    size: int
    extension: str


class CodeEngine:
    """
    Safe code-workspace abstraction.

    Arbitrary code execution is intentionally not implemented here.
    A sandboxed runner will be added as a separate controlled tool.
    """

    def inspect_file(self, path: str) -> CodeInspection:
        target = Path(path)

        return CodeInspection(
            path=str(target),
            exists=target.exists(),
            is_file=target.is_file(),
            size=target.stat().st_size if target.is_file() else 0,
            extension=target.suffix,
        )

    def list_files(
        self,
        root: str,
        extensions: Iterable[str] | None = None,
    ) -> list[str]:
        base = Path(root)

        if not base.exists():
            return []

        allowed = None

        if extensions is not None:
            allowed = {
                ext if ext.startswith(".") else f".{ext}"
                for ext in extensions
            }

        results: list[str] = []

        for item in base.rglob("*"):
            if not item.is_file():
                continue

            if allowed is not None and item.suffix not in allowed:
                continue

            results.append(str(item))

        return sorted(results)
