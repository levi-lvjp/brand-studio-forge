from __future__ import annotations

from typing import Protocol, TypedDict


class ImageResult(TypedDict):
    url: str | None
    image_bytes: bytes | None
    prompt_used: str
    fallback: bool
    error: str | None


class ImageProvider(Protocol):
    name: str

    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        seed: int | None = None,
    ) -> ImageResult: ...

    def is_available(self) -> bool: ...
