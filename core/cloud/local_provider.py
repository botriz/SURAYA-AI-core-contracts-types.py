from __future__ import annotations

import os
import shutil
from pathlib import Path


class LocalStorageProvider:
    name = "local"

    def __init__(self, root: str = "data/cloud") -> None:
        self.root = Path(root).resolve()
        self.root.mkdir(parents=True, exist_ok=True, mode=0o700)
        os.chmod(self.root, 0o700)

    def _safe_path(self, value: str) -> Path:
        candidate = Path(value)
        if candidate.is_absolute():
            raise ValueError("Storage paths must be relative.")
        resolved = (self.root / candidate).resolve()
        if resolved != self.root and self.root not in resolved.parents:
            raise ValueError("Storage path escapes the configured root.")
        return resolved

    def upload(self, local_path: str, remote_path: str) -> str:
        source = Path(local_path).resolve()
        if source != self.root and self.root not in source.parents:
            raise ValueError("Source must be inside the configured storage root.")
        if not source.is_file():
            raise FileNotFoundError("Source file does not exist.")
        destination = self._safe_path(remote_path)
        destination.parent.mkdir(parents=True, exist_ok=True)
        temporary = destination.with_name(destination.name + ".uploading")
        shutil.copyfile(source, temporary)
        os.chmod(temporary, 0o600)
        os.replace(temporary, destination)
        return str(destination.relative_to(self.root))
