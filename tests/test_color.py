from __future__ import annotations

import os
import re
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from forge.src.brand_profile import BrandProfile
from forge.src.color import generate_palette

OKLCH_REGEX = re.compile(r"oklch\((\d+\.?\d*)%\s+(\d+\.?\d*)\s+(\d+\.?\d*)\)")


def _parse_oklch(value: str) -> tuple[float, float, float] | None:
    m = OKLCH_REGEX.match(value)
    if not m:
        return None
    return float(m.group(1)), float(m.group(2)), float(m.group(3))


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


class TestGeneratePaletteOutputKeys:
    def test_has_required_keys(self):
        profile = _make_profile()
        result = generate_palette(profile)
        assert "primary" in result
        assert "secondary" in result
        assert "neutral" in result
        assert "strategy" in result


class TestOklchStringValidity:
    def test_primary_is_valid_oklch(self):
        result = generate_palette(_make_profile())
        assert _parse_oklch(result["primary"]) is not None

    def test_secondary_is_valid_oklch(self):
        result = generate_palette(_make_profile())
        assert _parse_oklch(result["secondary"]) is not None

    def test_neutral_is_valid_oklch(self):
        result = generate_palette(_make_profile())
        assert _parse_oklch(result["neutral"]) is not None


class TestNeutralTinted:
    def test_neutral_has_chroma_above_zero(self):
        result = generate_palette(_make_profile())
        parsed = _parse_oklch(result["neutral"])
        assert parsed is not None
        l, c, h = parsed
        assert c > 0, f"Neutral chroma {c} should be > 0 (tinted toward primary hue)"


class TestNoHexDefaults:
    def test_no_black_hash(self):
        result = generate_palette(_make_profile())
        combined = " ".join(str(v) for v in result.values())
        assert "#000" not in combined

    def test_no_white_hash(self):
        result = generate_palette(_make_profile())
        combined = " ".join(str(v) for v in result.values())
        assert "#fff" not in combined


class TestDifferentProfilesDifferentPalettes:
    def test_warm_coffee_vs_cold_fintech(self):
        coffee = _make_profile(
            name="Warm Roast",
            industry="coffee",
            personality_words=["warm", "artisanal", "craft"],
            mood="Warm",
        )
        fintech = _make_profile(
            name="Cold Ledger",
            industry="fintech",
            personality_words=["precise", "secure", "reliable"],
            mood="Precise",
            competitors=["Stripe", "Plaid"],
        )
        result_coffee = generate_palette(coffee)
        result_fintech = generate_palette(fintech)
        assert result_coffee["primary"] != result_fintech["primary"]


class TestReflexRejectFintechNavy:
    def test_fintech_does_not_get_navy_primary(self):
        fintech = _make_profile(
            name="FinanceApp",
            industry="fintech",
            personality_words=["precise", "secure", "reliable"],
            mood="Precise",
            competitors=["Stripe", "Plaid", "Revolut"],
        )
        result = generate_palette(fintech)
        parsed = _parse_oklch(result["primary"])
        assert parsed is not None
        l, c, h = parsed
        assert not (240 <= h <= 260), (
            f"Fintech brand got navy hue {h}. Must avoid hue 240-260."
        )
