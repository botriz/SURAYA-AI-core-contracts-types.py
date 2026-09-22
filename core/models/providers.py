from __future__ import annotations

from typing import Any

from core.models.local import LocalModel
from core.models.router import ModelRouter


def create_default_model_router() -> ModelRouter:
    router = ModelRouter()

    router.register(
        LocalModel(),
        default=True,
    )

    return router


def generate(
    router: ModelRouter,
    prompt: str,
    provider: str | None = None,
    **kwargs: Any,
) -> str:
    return router.generate(
        prompt,
        provider=provider,
        **kwargs,
    )
