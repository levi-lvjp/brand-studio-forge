from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from forge.src.brand_profile import BrandProfile

PERSONALITY_TO_MOOD: dict[str, str] = {
    "warm": "Warm",
    "artisanal": "Warm",
    "craft": "Warm",
    "approachable": "Warm",
    "friendly": "Warm",
    "cozy": "Warm",
    "bold": "Commanding",
    "authoritative": "Commanding",
    "confident": "Commanding",
    "precise": "Precise",
    "minimal": "Minimal",
    "clean": "Minimal",
    "technical": "Precise",
    "premium": "Lush",
    "luscious": "Lush",
    "rich": "Lush",
    "playful": "Playful",
    "fun": "Playful",
    "energetic": "Playful",
    "calm": "Serene",
    "peaceful": "Serene",
    "serene": "Serene",
    "rebellious": "Rebellious",
    "edgy": "Rebellious",
    "disruptive": "Rebellious",
    "heritage": "Heritage",
    "traditional": "Heritage",
    "classic": "Heritage",
    "raw": "Raw",
    "unpolished": "Raw",
    "industrial": "Raw",
    "reliable": "Commanding",
    "secure": "Precise",
    "trusted": "Commanding",
}


def infer_mood(profile: BrandProfile) -> str:
    if profile.mood:
        return profile.mood
    for word in profile.personality_words:
        lower = word.lower().strip()
        if lower in PERSONALITY_TO_MOOD:
            return PERSONALITY_TO_MOOD[lower]
    return "Warm"
