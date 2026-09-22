from __future__ import annotations

from typing import Any, Protocol


class ModelProvider(Protocol):
    name: str

    def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        ...


class ModelRouter:
    def __init__(
        self,
        default_provider: str | None = None,
    ) -> None:
        self.providers: dict[str, ModelProvider] = {}
        self.default_provider = default_provider

    def register(
        self,
        provider: ModelProvider,
        *,
        default: bool = False,
    ) -> None:
        self.providers[provider.name] = provider

        if default or self.default_provider is None:
            self.default_provider = provider.name

    def remove(self, name: str) -> bool:
        removed = self.providers.pop(name, None) is not None

        if removed and self.default_provider == name:
            self.default_provider = (
                next(iter(self.providers), None)
            )

        return removed

    def list_providers(self) -> list[str]:
        return sorted(self.providers.keys())

    def get(self, name: str | None = None) -> ModelProvider:
        provider_name = name or self.default_provider

        if provider_name is None:
            raise RuntimeError("No model provider is configured.")

        provider = self.providers.get(provider_name)

        if provider is None:
            raise KeyError(
                f"Model provider '{provider_name}' is not registered."
            )

        return provider

    def generate(
        self,
        prompt: str,
        provider: str | None = None,
        **kwargs: Any,
    ) -> str:
        return self.get(provider).generate(
            prompt,
            **kwargs,
              )
