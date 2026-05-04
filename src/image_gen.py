from __future__ import annotations

import base64
import os
import urllib.request
import urllib.error

from forge.src.providers.registry import get_provider


def generate_logo_images(
    logo_prompts: dict,
    provider_name: str,
    provider_config: dict | None = None,
    output_dir: str = "./output",
) -> dict | None:
    try:
        provider = get_provider(provider_name, provider_config)

        negative_prompt = logo_prompts.get("negative_prompt", "")
        prompt_keys = [
            ("primary_prompt", "logo_primary"),
            ("icon_prompt", "logo_icon"),
            ("monochrome_prompt", "logo_mono"),
        ]

        img_tags = {}
        logo_files = []

        os.makedirs(output_dir, exist_ok=True)

        for prompt_key, file_stem in prompt_keys:
            prompt_text = logo_prompts.get(prompt_key, "")
            if not prompt_text:
                continue

            result = provider.generate(
                prompt=prompt_text,
                negative_prompt=negative_prompt,
                width=512,
                height=512,
            )

            if result.get("fallback"):
                return None
            if result.get("error"):
                return None

            image_bytes = result.get("image_bytes")
            if image_bytes is None and result.get("url"):
                url = result["url"]
                req = urllib.request.Request(url)
                with urllib.request.urlopen(req, timeout=60) as response:
                    image_bytes = response.read()

            if image_bytes is None:
                return None

            filename = f"{file_stem}.png"
            filepath = os.path.join(output_dir, filename)
            with open(filepath, "wb") as f:
                f.write(image_bytes)
            logo_files.append(filepath)

            b64 = base64.b64encode(image_bytes).decode("utf-8")
            img_tag = (
                f'<img src="data:image/png;base64,{b64}" alt="logo"'
                f' style="max-width:100%;max-height:100%">'
            )
            img_tags[f"{file_stem}_img_tag"] = img_tag

        return {
            "logo_img_tag": img_tags.get("logo_primary_img_tag", ""),
            "logo_icon_img_tag": img_tags.get("logo_icon_img_tag", ""),
            "logo_mono_img_tag": img_tags.get("logo_mono_img_tag", ""),
            "logo_files": logo_files,
        }
    except Exception:
        return None
