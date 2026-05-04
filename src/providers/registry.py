from __future__ import annotations

from forge.src.providers.base import ImageProvider
from forge.src.providers.image_gemini import GeminiProvider
from forge.src.providers.image_openai import OpenAIProvider
from forge.src.providers.image_custom import CustomProvider

PRESET_PROVIDERS = {
    "gemini": GeminiProvider,
    "chatgpt": OpenAIProvider,
}


def get_provider(name: str, config: dict | None = None) -> ImageProvider:
    if name == "custom":
        return CustomProvider(**(config or {}))
    if name in PRESET_PROVIDERS:
        return PRESET_PROVIDERS[name]()
    raise ValueError(
        f"Unknown provider: {name}. Available: {', '.join(PRESET_PROVIDERS.keys())}"
    )


def available_providers() -> list[str]:
    return [name for name, cls in PRESET_PROVIDERS.items() if cls().is_available()]
