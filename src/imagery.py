from __future__ import annotations

import json
import os
import ssl
import sys
import urllib.request
import urllib.error

import certifi

from PIL import Image

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from forge.src.brand_profile import BrandProfile
from forge.src.color import oklch_to_name
from forge.src.providers.registry import get_provider

_SSL_CTX = ssl.create_default_context(cafile=certifi.where())

TEXT_MODEL_URL = (
    "https://generativelanguage.googleapis.com/v1beta/models/"
    "gemini-2.5-flash:generateContent"
)

_SYSTEM_INSTRUCTION = (
    "You are an expert art director writing prompts for AI image generation. "
    "Given a raw brief, expand it into a detailed, evocative prompt that will "
    "produce high-quality results. Keep it under 200 words. Include specific "
    "details about composition, lighting, texture, color treatment, and mood. "
    "Do not include any explanation — output only the refined prompt."
)


def build_imagery_prompt(profile: BrandProfile, style: str) -> str:
    mood = profile.mood or "Warm"
    personality = ", ".join(profile.personality_words[:3])
    color_hint = oklch_to_name(profile.primary_color or "")

    if style == "photography":
        return (
            f"Brand photography style reference for '{profile.name}', "
            f"a {profile.industry} brand. Mood: {mood}. "
            f"Personality: {personality}. "
            f"Natural light, editorial composition, unstaged feel. "
            f"Color palette leans toward {color_hint}. "
            f"No text, no logos, no people's faces. "
            f"High-end commercial photography, lifestyle context. "
            f"Square 1:1 aspect ratio."
        )
    else:
        return (
            f"Brand illustration style reference for '{profile.name}', "
            f"a {profile.industry} brand. Mood: {mood}. "
            f"Personality: {personality}. "
            f"Minimal line art or geometric shapes. "
            f"Color palette: {color_hint}. "
            f"Abstract, non-literal, suitable as brand pattern or texture. "
            f"No text, no logos. "
            f"Square 1:1 aspect ratio."
        )


def refine_imagery_prompt(raw_prompt: str, style: str) -> str:
    """Use Gemini text model to refine a raw imagery brief into a detailed image generation prompt."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        return raw_prompt

    request_body = {
        "systemInstruction": {"parts": [{"text": _SYSTEM_INSTRUCTION}]},
        "contents": [{"parts": [{"text": raw_prompt}]}],
    }

    data = json.dumps(request_body).encode("utf-8")
    url = f"{TEXT_MODEL_URL}?key={api_key}"

    req = urllib.request.Request(
        url,
        data=data,
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


def generate_brand_imagery(
    profile: BrandProfile,
    output_dir: str,
    provider_name: str = "gemini",
) -> dict[str, str | None]:
    provider = get_provider(provider_name)
    results: dict[str, str | None] = {}

    for style in ("photography", "illustration"):
        prompt = build_imagery_prompt(profile, style)
        prompt = refine_imagery_prompt(prompt, style)
        result = provider.generate(prompt=prompt, width=1024, height=1024)

        if result["image_bytes"]:
            filename = f"imagery_{style}.png"
            out_path = os.path.join(output_dir, filename)
            with open(out_path, "wb") as f:
                f.write(result["image_bytes"])
            img = Image.open(out_path)
            iw, ih = img.size
            side = min(iw, ih)
            left = (iw - side) // 2
            top = (ih - side) // 2
            img = img.crop((left, top, left + side, top + side))
            img = img.resize((1024, 1024), Image.LANCZOS)
            if img.mode == "RGBA":
                bg = Image.new("RGB", img.size, (255, 255, 255))
                bg.paste(img, mask=img.split()[3])
                img = bg
            img.save(out_path, "PNG")
            results[style] = out_path
        elif result["url"]:
            results[style] = result["url"]
        else:
            results[style] = None
            print(
                f"WARNING: imagery generation failed for {style}: {result.get('error')}",
                file=sys.stderr,
            )

    return results
