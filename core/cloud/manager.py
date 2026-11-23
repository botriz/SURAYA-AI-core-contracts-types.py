from __future__ import annotations

from typing import Any


class CloudStorageManager:
    def __init__(self, default_provider: str = "local") -> None:
        self.default_provider = default_provider
        self._providers: dict[str, Any] = {}

    def register(self, provider: Any) -> None:
        name = str(getattr(provider, "name", "")).strip()
        if not name:
            raise ValueError("Storage provider must define a non-empty name.")
        self._providers[name] = provider

    def list_providers(self) -> list[str]:
        return sorted(self._providers)

    def upload(self, local_path: str, remote_path: str, provider: str | None = None) -> str:
        selected = provider or self.default_provider
        storage = self._providers.get(selected)
        if storage is None:
            raise ValueError("Storage provider is not registered.")
        return storage.upload(local_path=local_path, remote_path=remote_path)
