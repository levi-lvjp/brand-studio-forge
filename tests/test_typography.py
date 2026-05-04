from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from forge.src.brand_profile import BrandProfile
from forge.src.typography import generate_typography

REFLEX_REJECT_FONTS = {
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


def _make_profile(**overrides) -> BrandProfile:
    defaults = {
        "name": "Test Brand",
        "industry": "coffee",
        "personality_words": ["warm", "artisanal", "craft"],
        "positioning_statement": "Handcrafted coffee for the mindful drinker",
        "target_audience": "Coffee enthusiasts 25-45",
        "competitors": ["Blue Bottle", "Stumptown"],
        "anti_references": ["Starbucks", "Dunkin"],
    }
    defaults.update(overrides)
    return BrandProfile(**defaults)


class TestGenerateTypographyOutputKeys:
    def test_has_display_font(self):
        result = generate_typography(_make_profile())
        assert "display_font" in result

    def test_has_body_font(self):
        result = generate_typography(_make_profile())
        assert "body_font" in result

    def test_has_display_weight(self):
        result = generate_typography(_make_profile())
        assert "display_weight" in result

    def test_has_body_weight(self):
        result = generate_typography(_make_profile())
        assert "body_weight" in result


class TestNoReflexRejectFonts:
    def test_no_reflex_reject_font_in_output(self):
        result = generate_typography(_make_profile())
        fonts_used = {result["display_font"], result["body_font"]}
        violators = fonts_used & REFLEX_REJECT_FONTS
        assert not violators, f"Reflex-reject fonts found: {violators}"


class TestFontContrast:
    def test_display_not_equal_body(self):
        result = generate_typography(_make_profile())
        assert result["display_font"] != result["body_font"], (
            "Display and body fonts must differ (contrast rule)"
        )


class TestDifferentProfilesDifferentPairs:
    def test_different_profiles_produce_different_pairs(self):
        coffee = _make_profile(
            name="Warm Roast",
            industry="coffee",
            personality_words=["warm", "artisanal", "craft"],
            mood="Warm",
        )
        tech = _make_profile(
            name="PreciseIO",
            industry="technology",
            personality_words=["precise", "minimal", "clean"],
            mood="Precise",
        )
        r1 = generate_typography(coffee)
        r2 = generate_typography(tech)
        pair1 = (r1["display_font"], r1["body_font"])
        pair2 = (r2["display_font"], r2["body_font"])
        assert pair1 != pair2, f"Same font pair {pair1} for different profiles"


class TestLineHeightBounds:
    def test_line_height_in_bounds(self):
        result = generate_typography(_make_profile())
        assert 1.4 <= result["line_height"] <= 1.8, (
            f"line_height {result['line_height']} outside [1.4, 1.8]"
        )
