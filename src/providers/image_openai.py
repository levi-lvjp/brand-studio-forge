from __future__ import annotations

import base64
import json
import os
import ssl
import time
import urllib.request
import urllib.error

import certifi

from forge.src.providers.base import ImageResult

_SSL_CTX = ssl.create_default_context(cafile=certifi.where())

OPENAI_IMAGE_URL = "https://api.openai.com/v1/images/generations"


class OpenAIProvider:
    name = "chatgpt"

    def is_available(self) -> bool:
        return bool(os.environ.get("OPENAI_API_KEY"))

    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        seed: int | None = None,
    ) -> ImageResult:
        api_key = os.environ.get("OPENAI_API_KEY")
        if not api_key:
            return ImageResult(
                url=None,
                image_bytes=None,
                prompt_used=prompt,
                fallback=True,
                error="OPENAI_API_KEY not set",
            )

        request_body = {
            "model": "gpt-image-2",
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
            "quality": "medium",
            "response_format": "b64_json",
        }

        data = json.dumps(request_body).encode("utf-8")

        req = urllib.request.Request(
            OPENAI_IMAGE_URL,
            data=data,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        last_error: str | None = None
        for attempt in range(4):
            if attempt > 0:
                time.sleep(2**attempt)
                req = urllib.request.Request(
                    OPENAI_IMAGE_URL,
                    data=data,
                    headers={
                        "Authorization": f"Bearer {api_key}",
                        "Content-Type": "application/json",
                    },
                    method="POST",
                )
            try:
                with urllib.request.urlopen(
                    req, timeout=90, context=_SSL_CTX
                ) as response:
                    response_data = json.loads(response.read().decode("utf-8"))
                    image_bytes = None
                    if (
                        "data" in response_data
                        and isinstance(response_data["data"], list)
                        and len(response_data["data"]) > 0
                    ):
                        b64 = response_data["data"][0].get("b64_json")
                        if b64:
                            image_bytes = base64.b64decode(b64)
                    return ImageResult(
                        url=None,
                        image_bytes=image_bytes,
                        prompt_used=prompt,
                        fallback=image_bytes is None,
                        error=None if image_bytes else "No image in response",
                    )
            except urllib.error.HTTPError as e:
                last_error = str(e)
                if e.code != 429:
                    break
            except (urllib.error.URLError, Exception) as e:
                last_error = str(e)
                break

        return ImageResult(
            url=None,
            image_bytes=None,
            prompt_used=prompt,
            fallback=True,
            error=last_error,
        )
