from __future__ import annotations

from typing import BinaryIO

from core.cloud.base import CloudFile, CloudStorageProvider


class CloudStorageManager:

    def __init__(self) -> None:
        self.providers: dict[
            str,
            CloudStorageProvider,
        ] = {}

        self.default_provider: str | None = None

    def register(
        self,
        provider: CloudStorageProvider,
        default: bool = False,
    ) -> None:

        self.providers[
            provider.name
        ] = provider

        if (
            default
            or self.default_provider is None
        ):
            self.default_provider = provider.name

    def get(
        self,
        provider_name: str | None = None,
    ) -> CloudStorageProvider:

        name = (
            provider_name
            or self.default_provider
        )

        if name is None:
            raise RuntimeError(
                "No cloud storage provider configured."
            )

        provider = self.providers.get(
            name
        )

        if provider is None:
            raise RuntimeError(
                f"Cloud provider '{name}' is not registered."
            )

        return provider

    def upload(
        self,
        source: BinaryIO,
        destination: str,
        provider_name: str | None = None,
    ) -> CloudFile:

        return self.get(
            provider_name
        ).upload(
            source,
            destination,
        )

    def download(
        self,
        path: str,
        provider_name: str | None = None,
    ) -> bytes:

        return self.get(
            provider_name
        ).download(
            path
        )

    def delete(
        self,
        path: str,
        provider_name: str | None = None,
    ) -> bool:

        return self.get(
            provider_name
        ).delete(
            path
        )

    def exists(
        self,
        path: str,
        provider_name: str | None = None,
    ) -> bool:

        return self.get(
            provider_name
        ).exists(
            path
        )

    def list(
        self,
        prefix: str = "",
        provider_name: str | None = None,
    ) -> list[CloudFile]:

        return self.get(
            provider_name
        ).list(
            prefix
        )
