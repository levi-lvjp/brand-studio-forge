from __future__ import annotations

import base64
import json
import os
import ssl
import urllib.request
import urllib.error

import certifi

from forge.src.providers.registry import get_provider

_SSL_CTX = ssl.create_default_context(cafile=certifi.where())

_TEXT_MODEL_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)

_LOGO_SYSTEM_INSTRUCTION = (
    "You are an expert logo designer writing prompts for AI image generation. "
    "Given a raw logo brief, rewrite it into a vivid visual prompt under 120 words. "
    "Focus on shape, form, negative space, weight, texture, and composition. "
    "Describe what the logo LOOKS like, not what it means. "
    "Keep 'flat vector on white background' and any 'Avoid:' lines intact. "
    "Do not include any explanation — output only the refined prompt."
)


def _refine_logo_prompt(raw_prompt: str) -> str:
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return raw_prompt

    request_body = {
        "systemInstruction": {"parts": [{"text": _LOGO_SYSTEM_INSTRUCTION}]},
        "contents": [{"parts": [{"text": raw_prompt}]}],
    }

    data = json.dumps(request_body).encode("utf-8")
    url = f"{_TEXT_MODEL_URL}?key={api_key}"

    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(req, timeout=60, context=_SSL_CTX) as response:
            response_data = json.loads(response.read().decode("utf-8"))
            candidates = response_data.get("candidates", [])
            if candidates:
                parts = candidates[0].get("content", {}).get("parts", [])
                if parts and "text" in parts[0]:
                    return parts[0]["text"].strip()
    except Exception:
        pass

    return raw_prompt


def generate_logo_images(
    logo_prompts: dict,
    provider_name: str,
    provider_config: dict | None = None,
    output_dir: str = "./output",
) -> dict | None:
    try:
        provider = get_provider(provider_name, provider_config)

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

            prompt_text = _refine_logo_prompt(prompt_text)

            result = provider.generate(
                prompt=prompt_text,
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
