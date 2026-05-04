from __future__ import annotations

import base64
import json
import urllib.request
import urllib.error

from forge.src.providers.base import ImageResult


class CustomProvider:
    name = "custom"

    def __init__(
        self,
        base_url: str = "",
        model: str = "",
        api_key: str | None = None,
    ) -> None:
        self.base_url = base_url
        self.model = model
        self.api_key = api_key

    def is_available(self) -> bool:
        return bool(self.base_url and self.model)

    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        seed: int | None = None,
    ) -> ImageResult:
        if not self.is_available():
            return {
                "url": None,
                "image_bytes": None,
                "prompt_used": prompt,
                "fallback": True,
                "error": "base_url or model not set",
            }

        request_body = {
            "model": self.model,
            "prompt": prompt,
            "n": 1,
            "size": "1024x1024",
            "response_format": "b64_json",
        }

        data = json.dumps(request_body).encode("utf-8")
        url = f"{self.base_url}/v1/images/generations"

        headers = {"Content-Type": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"

        req = urllib.request.Request(
            url,
            data=data,
            headers=headers,
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=90) as response:
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
                return {
                    "url": None,
                    "image_bytes": image_bytes,
                    "prompt_used": prompt,
                    "fallback": False,
                    "error": None,
                }
        except urllib.error.URLError as e:
            return {
                "url": None,
                "image_bytes": None,
                "prompt_used": prompt,
                "fallback": True,
                "error": str(e),
            }
        except Exception as e:
            return {
                "url": None,
                "image_bytes": None,
                "prompt_used": prompt,
                "fallback": True,
                "error": str(e),
            }
