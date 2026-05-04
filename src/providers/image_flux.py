from __future__ import annotations

import json
import os
import urllib.request
import urllib.error

from forge.src.providers.base import ImageProvider, ImageResult

FAL_FLUX_URL = "https://fal.run/fal-ai/flux/schnell"


class FluxProvider:
    name = "flux"

    def is_available(self) -> bool:
        return bool(os.environ.get("FAL_KEY"))

    def generate(
        self,
        prompt: str,
        negative_prompt: str = "",
        width: int = 1024,
        height: int = 1024,
        seed: int | None = None,
    ) -> ImageResult:
        fal_key = os.environ.get("FAL_KEY")
        if not fal_key:
            return {
                "url": None,
                "image_bytes": None,
                "prompt_used": prompt,
                "fallback": True,
                "error": "FAL_KEY not set",
            }

        request_body = {
            "prompt": prompt,
            "image_size": {"width": width, "height": height},
            "num_images": 1,
            "enable_safety_checker": True,
        }
        if seed is not None:
            request_body["seed"] = seed

        data = json.dumps(request_body).encode("utf-8")

        req = urllib.request.Request(
            FAL_FLUX_URL,
            data=data,
            headers={
                "Authorization": f"Key {fal_key}",
                "Content-Type": "application/json",
            },
            method="POST",
        )

        try:
            with urllib.request.urlopen(req, timeout=60) as response:
                response_data = json.loads(response.read().decode("utf-8"))
                image_url = None
                if (
                    "images" in response_data
                    and isinstance(response_data["images"], list)
                    and len(response_data["images"]) > 0
                ):
                    image = response_data["images"][0]
                    if isinstance(image, dict):
                        image_url = image.get("url")
                    else:
                        image_url = image
                return {
                    "url": image_url,
                    "image_bytes": None,
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


def generate_image(
    prompt: str,
    negative_prompt: str = "",
    width: int = 1024,
    height: int = 1024,
    seed: int | None = None,
) -> dict:
    provider = FluxProvider()
    return provider.generate(
        prompt=prompt,
        negative_prompt=negative_prompt,
        width=width,
        height=height,
        seed=seed,
    )
