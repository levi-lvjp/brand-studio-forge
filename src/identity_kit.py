from __future__ import annotations

import base64
import copy
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from forge.src.brand_profile import BrandProfile
from forge.src.color import generate_palette
from forge.src.imagery import generate_brand_imagery
from forge.src.providers.registry import available_providers
from forge.src.typography import generate_typography
from forge.src.voice import generate_voice


def assemble_identity(profile: BrandProfile) -> BrandProfile:
    result = copy.copy(profile)

    palette = generate_palette(result)
    if not result.primary_color:
        result.primary_color = palette["primary"]
    if not result.secondary_color:
        result.secondary_color = palette["secondary"]
    if not result.accent_color:
        result.accent_color = palette["accent"]
    if not result.neutral_tone:
        result.neutral_tone = palette["neutral"]
    if not result.color_strategy:
        result.color_strategy = palette["strategy"]
    if not result.mood:
        result.mood = palette.get("mood")

    typo = generate_typography(result)
    if not result.display_font:
        result.display_font = typo["display_font"]
    if not result.body_font:
        result.body_font = typo["body_font"]

    voice = generate_voice(result)
    if not result.voice_tone:
        result.voice_tone = voice["tone"]
    if not result.voice_dos:
        result.voice_dos = voice["dos"]
    if not result.voice_donts:
        result.voice_donts = voice["donts"]
    if not result.tagline:
        result.tagline = voice["sample_tagline"]

    try:
        from forge.src.logo import generate_logo_prompts

        logo = generate_logo_prompts(result)
        if not result.logo_type:
            result.logo_type = logo["logo_type"]
        if not result.logo_strategy:
            result.logo_strategy = logo["strategy"]
    except ImportError:
        logo = None

    if result.image_provider:
        try:
            import base64

            output_dir = os.path.join(
                os.path.dirname(os.path.abspath(__file__)), "..", "output"
            )
            os.makedirs(output_dir, exist_ok=True)
            logo_primary_path = os.path.join(output_dir, "logo_primary.png")
            logo_icon_path = os.path.join(output_dir, "logo_icon.png")
            logo_mono_path = os.path.join(output_dir, "logo_mono.png")

            all_exist = (
                os.path.isfile(logo_primary_path)
                and os.path.isfile(logo_icon_path)
                and os.path.isfile(logo_mono_path)
            )

            if all_exist:

                def _read_logo_img_tag(filepath):
                    with open(filepath, "rb") as f:
                        b64 = base64.b64encode(f.read()).decode("utf-8")
                    return (
                        f'<img src="data:image/png;base64,{b64}" alt="logo"'
                        f' style="max-width:100%;max-height:100%">'
                    )

                result._logo_images = {
                    "logo_img_tag": _read_logo_img_tag(logo_primary_path),
                    "logo_icon_img_tag": _read_logo_img_tag(logo_icon_path),
                    "logo_mono_img_tag": _read_logo_img_tag(logo_mono_path),
                    "logo_files": [
                        logo_primary_path,
                        logo_icon_path,
                        logo_mono_path,
                    ],
                }
            else:
                from forge.src.image_gen import generate_logo_images

                result._logo_images = generate_logo_images(
                    logo_prompts=logo or {},
                    provider_name=result.image_provider,
                    provider_config=result.image_provider_config,
                    output_dir=output_dir,
                )
        except ImportError:
            result._logo_images = None
    else:
        result._logo_images = None

    return result


def assemble_identity_dict(profile: BrandProfile) -> dict:
    assembled = assemble_identity(profile)

    color_palette = [
        {
            "name": "Primary",
            "value": assembled.primary_color,
            "role": "Primary brand color",
        },
        {
            "name": "Secondary",
            "value": assembled.secondary_color,
            "role": "Secondary brand color",
        },
        {
            "name": "Neutral",
            "value": assembled.neutral_tone,
            "role": "Backgrounds and body text",
        },
        {
            "name": "Accent",
            "value": assembled.accent_color or assembled.secondary_color,
            "role": "Accents and highlights",
        },
    ]

    typography_hierarchy = (
        f'<div class="type-specimen">'
        f'<div class="type-specimen__sample t-display">Display — {assembled.display_font} 300</div>'
        f'<div class="type-specimen__meta">'
        f'<span class="type-specimen__detail">Family: <span>{assembled.display_font}</span></span>'
        f'<span class="type-specimen__detail">Weight: <span>300</span></span>'
        f'<span class="type-specimen__detail">Size: <span>clamp(2.5rem, 7vw, 4.5rem)</span></span>'
        f"</div></div>"
        f'<div class="type-specimen">'
        f'<div class="type-specimen__sample t-h1">Heading 1 — {assembled.display_font} 400</div>'
        f'<div class="type-specimen__meta">'
        f'<span class="type-specimen__detail">Family: <span>{assembled.display_font}</span></span>'
        f'<span class="type-specimen__detail">Weight: <span>400</span></span>'
        f'<span class="type-specimen__detail">Size: <span>1.8rem</span></span>'
        f"</div></div>"
        f'<div class="type-specimen">'
        f'<div class="type-specimen__sample t-h2">Heading 2 — {assembled.display_font} 400</div>'
        f'<div class="type-specimen__meta">'
        f'<span class="type-specimen__detail">Family: <span>{assembled.display_font}</span></span>'
        f'<span class="type-specimen__detail">Weight: <span>400</span></span>'
        f'<span class="type-specimen__detail">Size: <span>1.25rem</span></span>'
        f"</div></div>"
        f'<div class="type-specimen">'
        f'<div class="type-specimen__sample t-h3">Heading 3 — {assembled.body_font} 600</div>'
        f'<div class="type-specimen__meta">'
        f'<span class="type-specimen__detail">Family: <span>{assembled.body_font}</span></span>'
        f'<span class="type-specimen__detail">Weight: <span>600</span></span>'
        f'<span class="type-specimen__detail">Size: <span>0.85rem</span></span>'
        f"</div></div>"
        f'<div class="type-specimen">'
        f'<div class="type-specimen__sample t-body">Body — {assembled.body_font}. '
        f"The quick brown fox jumps over the lazy dog. Pack my box with five dozen liquor jugs.</div>"
        f'<div class="type-specimen__meta">'
        f'<span class="type-specimen__detail">Family: <span>{assembled.body_font}</span></span>'
        f'<span class="type-specimen__detail">Weight: <span>400</span></span>'
        f'<span class="type-specimen__detail">Size: <span>0.92rem</span></span>'
        f"</div></div>"
        f'<div class="type-specimen">'
        f'<div class="type-specimen__sample t-caption">Caption — {assembled.body_font} 400</div>'
        f'<div class="type-specimen__meta">'
        f'<span class="type-specimen__detail">Family: <span>{assembled.body_font}</span></span>'
        f'<span class="type-specimen__detail">Weight: <span>400</span></span>'
        f'<span class="type-specimen__detail">Size: <span>0.72rem</span></span>'
        f"</div></div>"
    )

    voice_description = (
        f"{assembled.name} speaks with a {assembled.voice_tone} voice. "
        f"Its language is grounded in {assembled.industry} — specific, earned, and unmistakably itself."
    )

    color_palette_html_parts = []
    for idx, swatch in enumerate(color_palette):
        size_class = " swatch__color--large" if idx == 0 else ""
        color_palette_html_parts.append(
            '<div class="swatch">'
            f'<div class="swatch__color{size_class}" style="background: {swatch["value"]}"></div>'
            f'<div class="swatch__name">{swatch["name"]}</div>'
            f'<div class="swatch__value">{swatch["value"]}</div>'
            f'<div class="swatch__role">{swatch["role"]}</div>'
            "</div>"
        )
    color_palette_html = "\n".join(color_palette_html_parts)

    primary = assembled.primary_color or "oklch(50% 0.15 250)"
    logo_svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 60">'
        f'<text x="100" y="38" text-anchor="middle" '
        f'font-family="{assembled.display_font or "sans-serif"}" '
        f'font-size="28" font-weight="600" fill="{primary}">'
        f"{assembled.name}</text></svg>"
    )
    logo_icon_svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 60">'
        f'<text x="30" y="40" text-anchor="middle" '
        f'font-family="{assembled.display_font or "sans-serif"}" '
        f'font-size="36" font-weight="700" fill="{primary}">'
        f"{assembled.name[:1]}</text></svg>"
    )
    logo_mono_svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 60">'
        f'<text x="100" y="38" text-anchor="middle" '
        f'font-family="{assembled.display_font or "sans-serif"}" '
        f'font-size="28" font-weight="600" fill="oklch(25% 0 0)">'
        f"{assembled.name}</text></svg>"
    )

    logo_images = getattr(assembled, "_logo_images", None)
    if logo_images is not None:
        logo_svg = logo_images.get("logo_img_tag", logo_svg)
        logo_icon_svg = logo_images.get("logo_icon_img_tag", logo_icon_svg)
        logo_mono_svg = logo_images.get("logo_mono_img_tag", logo_mono_svg)

    display_font_param = (assembled.display_font or "Inter").replace(" ", "+")
    body_font_param = (assembled.body_font or "Inter").replace(" ", "+")
    font_link = (
        '<link rel="preconnect" href="https://fonts.googleapis.com">'
        '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
        '<link rel="stylesheet" href="https://fonts.googleapis.com/css2?'
        f"family={display_font_param}:wght@300;400;600;700"
        f'&family={body_font_param}:wght@400;600&display=swap">'
    )

    imagery_paths: dict[str, str | None] = {"photography": None, "illustration": None}
    output_dir = os.path.join(
        os.path.dirname(os.path.abspath(__file__)), "..", "output"
    )
    os.makedirs(output_dir, exist_ok=True)
    photo_path = os.path.join(output_dir, "imagery_photography.png")
    illust_path = os.path.join(output_dir, "imagery_illustration.png")

    if os.path.isfile(photo_path) and os.path.isfile(illust_path):
        imagery_paths = {"photography": photo_path, "illustration": illust_path}
    else:
        providers = available_providers()
        if providers:
            preferred = (
                assembled.image_provider
                if assembled.image_provider in providers
                else providers[0]
            )
            try:
                imagery_paths = generate_brand_imagery(
                    assembled, output_dir, provider_name=preferred
                )
            except Exception as e:
                print(f"WARNING: imagery generation failed: {e}", file=sys.stderr)

    def _img_tag_from_path(path: str | None, alt: str) -> str:
        if path and os.path.isfile(path):
            with open(path, "rb") as f:
                b64 = base64.b64encode(f.read()).decode("utf-8")
            return (
                f'<img src="data:image/png;base64,{b64}" alt="{alt}" '
                f'style="width:100%;height:100%;object-fit:cover;" />'
            )
        return f'<span class="imagery-placeholder__label">{alt}</span>'

    photography_tag = _img_tag_from_path(imagery_paths.get("photography"), "Photography style")
    illustration_tag = _img_tag_from_path(imagery_paths.get("illustration"), "Illustration style")

    return {
        "FONT_LINK": font_link,
        "BRAND_NAME": assembled.name,
        "PRIMARY_COLOR": assembled.primary_color,
        "SECONDARY_COLOR": assembled.secondary_color,
        "NEUTRAL_TONE": assembled.neutral_tone,
        "DISPLAY_FONT": assembled.display_font,
        "BODY_FONT": assembled.body_font,
        "LOGO_SVG": logo_svg,
        "LOGO_ICON_SVG": logo_icon_svg,
        "LOGO_MONO_SVG": logo_mono_svg,
        "VOICE_DESCRIPTION": voice_description,
        "VOICE_DOS": assembled.voice_dos or [],
        "VOICE_DONTS": assembled.voice_donts or [],
        "COLOR_PALETTE": color_palette_html,
        "TYPOGRAPHY_HIERARCHY": typography_hierarchy,
        "TAGLINE": assembled.tagline or "",
        "CONTACT_NAME": assembled.name,
        "CONTACT_TITLE": "Founder",
        "CONTACT_EMAIL": f"hello@{assembled.name.lower().replace(' ', '')}.com",
        "CONTACT_PHONE": "",
        "CONTACT_URL": f"{assembled.name.lower().replace(' ', '')}.com",
        "MIN_SIZE": "24px",
        "CLEAR_SPACE": "1x cap height",
        "POST_TYPE": "quote",
        "HEADLINE": assembled.tagline or assembled.name,
        "BODY_TEXT": voice_description,
        "IMAGERY_PHOTOGRAPHY_TAG": photography_tag,
        "IMAGERY_ILLUSTRATION_TAG": illustration_tag,
    }
