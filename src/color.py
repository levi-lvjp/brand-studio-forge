from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from forge.src.brand_profile import BrandProfile
from forge.src.mood import PERSONALITY_TO_MOOD, infer_mood

MOOD_OKLCH_RANGES: dict[str, dict] = {
    "Commanding": {
        "primary": (15, 35, 0.08, 0.16),
        "secondary": (35, 55, 0.06, 0.14),
        "neutral_l": (90, 97),
    },
    "Warm": {
        "primary": (55, 80, 0.10, 0.20),
        "secondary": (75, 90, 0.06, 0.14),
        "neutral_l": (90, 96),
        "hue_range": (40, 90),
    },
    "Precise": {
        "primary": (85, 97, 0.02, 0.08),
        "secondary": (40, 60, 0.06, 0.14),
        "neutral_l": (92, 98),
    },
    "Rebellious": {
        "primary": (10, 25, 0.08, 0.15),
        "secondary": (80, 95, 0.04, 0.10),
        "neutral_l": (94, 98),
    },
    "Serene": {
        "primary": (80, 95, 0.04, 0.12),
        "secondary": (65, 80, 0.05, 0.13),
        "neutral_l": (93, 98),
        "hue_range": (180, 240),
    },
    "Playful": {
        "primary": (55, 75, 0.12, 0.22),
        "secondary": (70, 85, 0.08, 0.16),
        "neutral_l": (92, 97),
    },
    "Heritage": {
        "primary": (25, 55, 0.08, 0.18),
        "secondary": (50, 70, 0.06, 0.14),
        "neutral_l": (88, 95),
        "hue_range": (20, 60),
    },
    "Minimal": {
        "primary": (92, 98, 0.00, 0.04),
        "secondary": (60, 80, 0.04, 0.12),
        "neutral_l": (94, 99),
    },
    "Raw": {
        "primary": (85, 97, 0.00, 0.04),
        "secondary": (5, 20, 0.00, 0.04),
        "neutral_l": (93, 98),
    },
    "Lush": {
        "primary": (25, 50, 0.10, 0.20),
        "secondary": (50, 65, 0.08, 0.18),
        "neutral_l": (90, 96),
    },
}

INDUSTRY_DEFAULTS: dict[str, tuple[int, int, float, float]] = {
    "fintech": (240, 260, 0.08, 0.16),
    "wellness": (110, 140, 0.06, 0.14),
    "coffee": (30, 50, 0.08, 0.14),
    "legal": (240, 260, 0.04, 0.10),
    "food": (0, 30, 0.15, 0.25),
    "technology": (220, 250, 0.10, 0.20),
    "fashion": (290, 330, 0.12, 0.22),
    "healthcare": (190, 220, 0.06, 0.14),
    "education": (240, 270, 0.08, 0.16),
}

INDUSTRY_DEFAULT_STRATEGIES: dict[str, str] = {
    "fintech": "Committed",
    "wellness": "Restrained",
    "coffee": "Committed",
    "legal": "Restrained",
    "food": "Full palette",
    "technology": "Committed",
    "fashion": "Full palette",
    "healthcare": "Committed",
    "education": "Committed",
}

PERSONALITY_STRATEGY_SHIFTS: dict[str, int] = {
    "bold": +1,
    "disruptive": +2,
    "minimal": -1,
    "precise": -1,
    "playful": +1,
    "lush": +1,
    "raw": -1,
    "serene": -1,
}

STRATEGY_LEVELS = ["Restrained", "Committed", "Full palette", "Drenched"]

BANNED_PATTERNS = ["#000", "#fff"]


def _fmt_oklch(l: float, c: float, h: float) -> str:
    return f"oklch({l:.1f}% {c:.4f} {h:.0f})"


def _infer_strategy(profile: BrandProfile, mood: str) -> str:
    if profile.color_strategy:
        return profile.color_strategy
    base_idx = 1
    industry = profile.industry.lower().strip()
    for key, strat in INDUSTRY_DEFAULT_STRATEGIES.items():
        if key in industry:
            base_idx = STRATEGY_LEVELS.index(strat)
            break
    for word in profile.personality_words:
        lower = word.lower().strip()
        if lower in PERSONALITY_STRATEGY_SHIFTS:
            base_idx += PERSONALITY_STRATEGY_SHIFTS[lower]
    base_idx = max(0, min(base_idx, len(STRATEGY_LEVELS) - 1))
    return STRATEGY_LEVELS[base_idx]


def _apply_chroma_decay(l: float, c: float) -> float:
    l_rel = l / 100.0
    if l_rel < 0.30:
        factor = l_rel / 0.30
    elif l_rel > 0.80:
        factor = (1.0 - l_rel) / 0.20
    else:
        factor = 1.0
    return c * max(0.3, factor)


def _competitor_dodge(hue: float, industry: str) -> float:
    lower_industry = industry.lower().strip()
    for key, (bad_lo, bad_hi, _, _) in INDUSTRY_DEFAULTS.items():
        if key in lower_industry and bad_lo <= hue <= bad_hi:
            shift = 35 if hue > (bad_lo + bad_hi) / 2 else -35
            return (hue + shift) % 360
    return hue


def _pick_hue(mood: str, industry: str) -> float:
    ranges = MOOD_OKLCH_RANGES.get(mood, MOOD_OKLCH_RANGES["Warm"])
    mood_hues = ranges.get("hue_range", None)
    if mood_hues:
        lo, hi = mood_hues
        hue = (lo + hi) / 2
    elif mood == "Commanding":
        hue = 255
    elif mood == "Precise":
        hue = 210
    elif mood == "Rebellious":
        hue = 350
    elif mood == "Playful":
        hue = 45
    elif mood == "Minimal":
        hue = 215
    elif mood == "Raw":
        hue = 230
    elif mood == "Lush":
        hue = 290
    elif mood == "Serene":
        hue = 200
    elif mood == "Heritage":
        hue = 35
    else:
        hue = 55
    hue = _competitor_dodge(hue, industry)
    return hue


def generate_palette(profile: BrandProfile) -> dict:
    mood = infer_mood(profile)
    strategy = _infer_strategy(profile, mood)
    ranges = MOOD_OKLCH_RANGES.get(mood, MOOD_OKLCH_RANGES["Warm"])
    hue = _pick_hue(mood, profile.industry)

    p_lo, p_hi, c_lo, c_hi = ranges["primary"]
    s_lo, s_hi, sc_lo, sc_hi = ranges["secondary"]
    nl_lo, nl_hi = ranges["neutral_l"]

    primary_l = (p_lo + p_hi) / 2
    raw_primary_c = (c_lo + c_hi) / 2
    primary_c = _apply_chroma_decay(primary_l, raw_primary_c)

    secondary_l = (s_lo + s_hi) / 2
    raw_secondary_c = (sc_lo + sc_hi) / 2
    secondary_c = _apply_chroma_decay(secondary_l, raw_secondary_c)
    secondary_hue = (hue + 120) % 360

    neutral_l = (nl_lo + nl_hi) / 2
    neutral_c = min(max(raw_primary_c * 0.10, 0.01), 0.06)

    accent_hue = (hue + 200) % 360
    accent_l = (p_lo + p_hi + s_lo + s_hi) / 4
    accent_c = _apply_chroma_decay(accent_l, raw_primary_c * 0.9)

    primary_color = _fmt_oklch(primary_l, primary_c, hue)
    secondary_color = _fmt_oklch(secondary_l, secondary_c, secondary_hue)
    neutral_color = _fmt_oklch(neutral_l, neutral_c, hue)
    accent_color = _fmt_oklch(accent_l, accent_c, accent_hue)

    reasoning = (
        f"Derived from mood archetype '{mood}' with OKLCH primary at hue {hue:.0f} deg. "
        f"Strategy '{strategy}' balances the brand's personality with its {profile.industry} industry context."
    )

    result = {
        "primary": primary_color,
        "secondary": secondary_color,
        "neutral": neutral_color,
        "accent": accent_color,
        "strategy": strategy,
        "mood": mood,
        "reasoning": reasoning,
    }

    _palette_guard(result)
    return result


def _palette_guard(result: dict) -> None:
    for key in ("primary", "secondary", "neutral", "accent"):
        val = str(result[key]).lower()
        for banned in BANNED_PATTERNS:
            if banned in val:
                import sys

                print(
                    f"WARNING: {key} color '{result[key]}' matched banned pattern '{banned}', replaced with fallback",
                    file=sys.stderr,
                )
                result[key] = "oklch(50% 0.15 55)"


def oklch_to_name(oklch_str: str) -> str:
    """Convert oklch string to approximate human-readable color name."""
    if not oklch_str:
        return oklch_str
    match_ = re.match(
        r"oklch\(\s*([\d.]+)%?\s+([\d.]+)\s+([\d.]+)\s*\)", str(oklch_str).strip()
    )
    if not match_:
        return oklch_str

    lightness = float(match_.group(1))
    chroma = float(match_.group(2))
    hue = float(match_.group(3))

    hue = hue % 360

    if 0 <= hue < 30:
        base = "red"
    elif 30 <= hue < 60:
        base = "amber"
    elif 60 <= hue < 90:
        base = "gold"
    elif 90 <= hue < 150:
        base = "green"
    elif 150 <= hue < 210:
        base = "teal"
    elif 210 <= hue < 270:
        base = "blue"
    elif 270 <= hue < 330:
        base = "purple"
    else:
        base = "rose"

    modifiers: list[str] = []

    if chroma < 0.06:
        modifiers.append("muted")
    elif chroma > 0.18:
        modifiers.append("vivid")

    if lightness < 35:
        modifiers.append("deep")
    elif lightness > 85:
        modifiers.append("pale")

    if 30 <= hue < 60 and chroma <= 0.06:
        base = "olive"

    if modifiers:
        return f"{' '.join(modifiers)} {base}"
    return base
