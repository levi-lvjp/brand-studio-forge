from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from forge.src.brand_profile import BrandProfile
from forge.src.mood import infer_mood

REFLEX_REJECT_FONTS: set[str] = {
    "Fraunces",
    "Newsreader",
    "Lora",
    "Crimson",
    "Crimson Pro",
    "Playfair Display",
    "Cormorant",
    "Cormorant Garamond",
    "Syne",
    "IBM Plex Mono",
    "IBM Plex Sans",
    "Space Mono",
    "Space Grotesk",
    "Inter",
    "DM Sans",
    "DM Serif Display",
    "Outfit",
    "Plus Jakarta Sans",
    "Instrument Sans",
    "Instrument Serif",
}

FONT_CATALOG: list[dict] = [
    {
        "name": "Bitter",
        "category": "humanist_serif",
        "temp": "warm",
        "object": "worn leather",
    },
    {
        "name": "Merriweather",
        "category": "humanist_serif",
        "temp": "warm",
        "object": "dog-eared paperback",
    },
    {
        "name": "Libre Baskerville",
        "category": "transitional_serif",
        "temp": "neutral",
        "object": "marble column",
    },
    {
        "name": "PT Serif",
        "category": "transitional_serif",
        "temp": "neutral",
        "object": "typewriter page",
    },
    {
        "name": "Alice",
        "category": "transitional_serif",
        "temp": "warm",
        "object": "vellum page",
    },
    {
        "name": "Jost",
        "category": "geometric_sans",
        "temp": "cool",
        "object": "glass tower",
    },
    {
        "name": "Barlow",
        "category": "geometric_sans",
        "temp": "cool",
        "object": "highway signage",
    },
    {
        "name": "Manrope",
        "category": "geometric_sans",
        "temp": "neutral",
        "object": "cast metal type",
    },
    {
        "name": "Sora",
        "category": "geometric_sans",
        "temp": "cool",
        "object": "architectural grid",
    },
    {
        "name": "Public Sans",
        "category": "grotesque_sans",
        "temp": "neutral",
        "object": "government form",
    },
    {
        "name": "Atkinson Hyperlegible",
        "category": "grotesque_sans",
        "temp": "neutral",
        "object": "braille signage",
    },
    {
        "name": "Work Sans",
        "category": "grotesque_sans",
        "temp": "neutral",
        "object": "shop window decal",
    },
    {
        "name": "Figtree",
        "category": "geometric_sans",
        "temp": "warm",
        "object": "rounded pebble",
    },
    {
        "name": "Spectral",
        "category": "humanist_serif",
        "temp": "warm",
        "object": "letterpress print",
    },
    {
        "name": "Source Sans 3",
        "category": "humanist_sans",
        "temp": "warm",
        "object": "pencil draft",
    },
    {
        "name": "Source Serif 4",
        "category": "transitional_serif",
        "temp": "neutral",
        "object": "library binding",
    },
    {
        "name": "Fira Sans",
        "category": "humanist_sans",
        "temp": "warm",
        "object": "handwritten note",
    },
    {
        "name": "Fira Mono",
        "category": "monospace",
        "temp": "cool",
        "object": "punch card",
    },
    {
        "name": "Hind",
        "category": "humanist_sans",
        "temp": "warm",
        "object": "woven textile",
    },
    {
        "name": "Gelasio",
        "category": "transitional_serif",
        "temp": "warm",
        "object": "illuminated manuscript",
    },
    {
        "name": "Overpass",
        "category": "grotesque_sans",
        "temp": "neutral",
        "object": "highway sign",
    },
    {
        "name": "Asap",
        "category": "humanist_sans",
        "temp": "neutral",
        "object": "rounded button",
    },
    {
        "name": "Vollkorn",
        "category": "humanist_serif",
        "temp": "warm",
        "object": "inkwell page",
    },
    {
        "name": "Raleway",
        "category": "geometric_sans",
        "temp": "cool",
        "object": "steel cable",
    },
    {
        "name": "Cabin",
        "category": "humanist_sans",
        "temp": "warm",
        "object": "wooden beam",
    },
    {
        "name": "Noto Sans",
        "category": "grotesque_sans",
        "temp": "neutral",
        "object": "UN translation",
    },
    {
        "name": "Nunito",
        "category": "geometric_sans",
        "temp": "warm",
        "object": "soft pillow",
    },
    {
        "name": "Archivo",
        "category": "grotesque_sans",
        "temp": "cool",
        "object": "steel filing cabinet",
    },
    {
        "name": "Zilla Slab",
        "category": "slab_serif",
        "temp": "warm",
        "object": "carpenter's bench",
    },
    {
        "name": "Alegreya",
        "category": "humanist_serif",
        "temp": "warm",
        "object": "vellum scroll",
    },
    {
        "name": "Alegreya Sans",
        "category": "humanist_sans",
        "temp": "warm",
        "object": "vellum scroll",
    },
    {
        "name": "Bricolage Grotesque",
        "category": "grotesque_sans",
        "temp": "warm",
        "object": "stamp collection",
    },
    {
        "name": "Nunito Sans",
        "category": "geometric_sans",
        "temp": "warm",
        "object": "soft pillow",
    },
    {
        "name": "Exo 2",
        "category": "geometric_sans",
        "temp": "cool",
        "object": "carbon fiber panel",
    },
    {
        "name": "Rubik",
        "category": "geometric_sans",
        "temp": "warm",
        "object": "rounded cube",
    },
    {
        "name": "Teko",
        "category": "geometric_sans",
        "temp": "cool",
        "object": "stencil plate",
    },
    {
        "name": "Chivo",
        "category": "grotesque_sans",
        "temp": "neutral",
        "object": "brass plate",
    },
    {
        "name": "Spline Sans",
        "category": "grotesque_sans",
        "temp": "cool",
        "object": "graph paper",
    },
    {
        "name": "Lato",
        "category": "humanist_sans",
        "temp": "warm",
        "object": "summer linen",
    },
    {
        "name": "Noto Serif",
        "category": "transitional_serif",
        "temp": "neutral",
        "object": "UN translation",
    },
    {
        "name": "Taviraj",
        "category": "transitional_serif",
        "temp": "warm",
        "object": "copper engraving",
    },
    {
        "name": "Grenze",
        "category": "humanist_serif",
        "temp": "warm",
        "object": "gothic arch",
    },
]

MOOD_FONT_TEMPS: dict[str, tuple[str, str]] = {
    "Commanding": ("cool", "neutral"),
    "Warm": ("warm", "warm"),
    "Precise": ("cool", "neutral"),
    "Rebellious": ("cool", "neutral"),
    "Serene": ("warm", "warm"),
    "Playful": ("warm", "warm"),
    "Heritage": ("warm", "neutral"),
    "Minimal": ("cool", "cool"),
    "Raw": ("neutral", "neutral"),
    "Lush": ("warm", "warm"),
}

MOOD_FONT_CATEGORIES: dict[str, tuple[list[str], list[str]]] = {
    "Commanding": (
        ["transitional_serif", "grotesque_sans"],
        ["grotesque_sans", "humanist_sans"],
    ),
    "Warm": (["humanist_serif", "transitional_serif"], ["humanist_sans"]),
    "Precise": (
        ["grotesque_sans", "geometric_sans"],
        ["grotesque_sans", "humanist_sans"],
    ),
    "Rebellious": (
        ["grotesque_sans", "geometric_sans"],
        ["monospace", "grotesque_sans"],
    ),
    "Serene": (["humanist_serif", "transitional_serif"], ["humanist_sans"]),
    "Playful": (
        ["humanist_serif", "geometric_sans"],
        ["humanist_sans", "geometric_sans"],
    ),
    "Heritage": (
        ["humanist_serif", "transitional_serif"],
        ["humanist_sans", "transitional_serif"],
    ),
    "Minimal": (["grotesque_sans", "geometric_sans"], ["grotesque_sans"]),
    "Raw": (["grotesque_sans", "monospace"], ["monospace", "grotesque_sans"]),
    "Lush": (["transitional_serif", "humanist_serif"], ["humanist_sans"]),
}

INDUSTRY_OBVIOUS_FONTS: dict[str, list[str]] = {
    "fintech": ["Bitter", "Libre Baskerville", "Fira Sans"],
    "wellness": ["Alegreya", "Spectral", "Gelasio"],
    "coffee": ["Bitter", "Vollkorn", "Alegreya"],
    "technology": ["Jost", "Public Sans", "Manrope"],
    "legal": ["Libre Baskerville", "PT Serif", "Archivo"],
    "food": ["Bitter", "Alegreya", "Nunito"],
    "fashion": ["Jost", "Raleway", "Overpass"],
    "healthcare": ["Fira Sans", "Hind", "Nunito"],
}


def _get_valid_catalog() -> list[dict]:
    return [f for f in FONT_CATALOG if f["name"] not in REFLEX_REJECT_FONTS]


def _filter_by_category(candidates: list[dict], categories: list[str]) -> list[dict]:
    return [f for f in candidates if f["category"] in categories]


def _filter_by_temp(candidates: list[dict], temps: tuple[str, str]) -> list[dict]:
    display_temp, body_temp = temps
    display_candidates = [f for f in candidates if f["temp"] == display_temp]
    if not display_candidates:
        display_candidates = candidates
    return display_candidates


def _cross_check_reject(candidates: list[dict], profile: BrandProfile) -> list[dict]:
    industry = profile.industry.lower().strip()
    obvious = []
    for key, fonts in INDUSTRY_OBVIOUS_FONTS.items():
        if key in industry:
            obvious = fonts
            break
    if not obvious:
        return candidates
    non_obvious = [f for f in candidates if f["name"] not in obvious]
    if non_obvious:
        return non_obvious
    return candidates


def _select_pair(
    display_candidates: list[dict],
    body_candidates: list[dict],
) -> tuple[dict, dict]:
    for d in display_candidates:
        for b in body_candidates:
            if d["name"] == b["name"]:
                continue
            if d["category"] == b["category"]:
                continue
            if d["name"] in ("Alegreya",) and b["name"] == "Alegreya Sans":
                continue
            if d["name"] == "Source Serif 4" and b["name"] == "Source Sans 3":
                continue
            if d["name"] in ("Noto Serif",) and b["name"] == "Noto Sans":
                continue
            return d, b
    return display_candidates[0], body_candidates[0]


def _body_weight_for_font(name: str) -> int:
    bold_sans = {"Overpass", "Archivo", "Exo 2", "Teko", "Spline Sans"}
    if name in bold_sans:
        return 600
    return 400


def generate_typography(profile: BrandProfile) -> dict:
    mood = infer_mood(profile)
    catalog = _get_valid_catalog()

    display_cats, body_cats = MOOD_FONT_CATEGORIES.get(
        mood, (["humanist_serif"], ["humanist_sans"])
    )
    temps = MOOD_FONT_TEMPS.get(mood, ("warm", "warm"))

    display_pool = _filter_by_category(catalog, display_cats)
    body_pool = _filter_by_category(catalog, body_cats)

    display_pool = _cross_check_reject(display_pool, profile)
    body_pool = _cross_check_reject(body_pool, profile)

    if not display_pool:
        display_pool = [
            f
            for f in catalog
            if f["category"] in display_cats or f["category"] == "humanist_serif"
        ]
    if not body_pool:
        body_pool = [
            f
            for f in catalog
            if f["category"] in body_cats or f["category"] == "humanist_sans"
        ]

    display_font, body_font = _select_pair(display_pool, body_pool)

    display_weight = (
        700
        if display_font["category"]
        in ("humanist_serif", "transitional_serif", "slab_serif")
        else 600
    )
    body_weight = _body_weight_for_font(body_font["name"])

    line_height = 1.6
    if mood in ("Serene", "Lush"):
        line_height = 1.75
    elif mood in ("Precise", "Minimal"):
        line_height = 1.5

    reasoning = (
        f"Mood '{mood}' maps to '{display_font['object']}' (display) and "
        f"'{body_font['object']}' (body). Fonts are from {display_font['category']} "
        f"and {body_font['category']} categories with temperature contrast."
    )

    return {
        "display_font": display_font["name"],
        "body_font": body_font["name"],
        "display_weight": display_weight,
        "body_weight": body_weight,
        "display_size": "clamp(2.5rem, 7vw, 4.5rem)",
        "body_size": "1rem",
        "line_height": line_height,
        "reasoning": reasoning,
    }
