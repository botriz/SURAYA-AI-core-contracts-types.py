from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


class ModelProvider(Protocol):
    name: str

    def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        ...


@dataclass
class ModelRouter:
    """
    دروازه مرکزی مدل‌های هوش مصنوعی.

    هیچ بخش دیگری از سیستم نباید مستقیماً به یک
    مدل خاص وابسته باشد.
    """

    providers: dict[str, ModelProvider] = field(
        default_factory=dict
    )

    default_provider: str | None = None

    def register(
        self,
        provider: ModelProvider,
        default: bool = False,
    ) -> None:

        if not provider.name:
            raise ValueError("Model provider must have a name.")

        self.providers[provider.name] = provider

        if default or self.default_provider is None:
            self.default_provider = provider.name

    def remove(
        self,
        provider_name: str,
    ) -> None:

        self.providers.pop(provider_name, None)

        if self.default_provider == provider_name:
            self.default_provider = (
                next(iter(self.providers), None)
            )

    def list_providers(self) -> list[str]:
        return list(self.providers.keys())

    def generate(
        self,
        prompt: str,
        provider: str | None = None,
        **kwargs: Any,
    ) -> str:

        selected_provider = (
            provider
            or self.default_provider
        )

        if selected_provider is None:
            raise RuntimeError(
                "No model provider is configured."
            )

        model = self.providers.get(
            selected_provider
        )

        if model is None:
            raise RuntimeError(
                f"Model provider '{selected_provider}' "
                "is not registered."
            )

        return model.generate(
            prompt,
            **kwargs,
      )
