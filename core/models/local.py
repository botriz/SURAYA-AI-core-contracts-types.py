from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass
class LocalModel:
    name: str = "local-placeholder"

    def generate(
        self,
        prompt: str,
        **kwargs: Any,
    ) -> str:
        prompt = prompt.strip()

        if not prompt:
            raise ValueError("Prompt cannot be empty.")

        return (
            "SURAYA local model placeholder.\n\n"
            f"Prompt received:\n{prompt}"
        )
