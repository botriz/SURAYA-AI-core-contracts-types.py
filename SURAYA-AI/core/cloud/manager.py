from __future__ import annotations

from core.cloud.base import CloudFile, CloudStorageProvider


class CloudStorageManager:
    def __init__(self, default_provider: str = "local") -> None:
        self._providers: dict[str, CloudStorageProvider] = {}
        self._default_provider = default_provider

    def register(self, provider: CloudStorageProvider) -> None:
        self._providers[provider.name] = provider

    def remove(self, name: str) -> bool:
        return self._providers.pop(name, None) is not None

    def get(self, name: str | None = None) -> CloudStorageProvider:
        provider_name = name or self._default_provider

        if provider_name not in self._providers:
            raise KeyError(
                f"Cloud provider '{provider_name}' is not registered."
            )

        return self._providers[provider_name]

    def set_default(self, name: str) -> None:
        self.get(name)
        self._default_provider = name

    def list_providers(self) -> list[str]:
        return sorted(self._providers.keys())

    def upload(
        self,
        local_path: str,
        remote_path: str,
        provider: str | None = None,
    ) -> CloudFile:
        return self.get(provider).upload(
            local_path,
            remote_path,
        )

    def download(
        self,
        remote_path: str,
        local_path: str,
        provider: str | None = None,
    ) -> str:
        return self.get(provider).download(
            remote_path,
            local_path,
        )

    def delete(
        self,
        remote_path: str,
        provider: str | None = None,
    ) -> bool:
        return self.get(provider).delete(remote_path)

    def exists(
        self,
        remote_path: str,
        provider: str | None = None,
    ) -> bool:
        return self.get(provider).exists(remote_path)

    def list(
        self,
        prefix: str = "",
        provider: str | None = None,
    ) -> list[CloudFile]:
        return self.get(provider).list(prefix)
