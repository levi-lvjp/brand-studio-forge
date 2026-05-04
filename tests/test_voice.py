from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from forge.src.brand_profile import BrandProfile
from forge.src.voice import generate_voice

ABSOLUTE_BANNED_WORDS = {
    "elevate",
    "empower",
    "seamless",
    "leverage",
    "innovative",
    "cutting-edge",
    "transform",
    "unlock",
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


class TestGenerateVoiceOutputKeys:
    def test_has_tone(self):
        result = generate_voice(_make_profile())
        assert "tone" in result

    def test_has_dos(self):
        result = generate_voice(_make_profile())
        assert "dos" in result

    def test_has_donts(self):
        result = generate_voice(_make_profile())
        assert "donts" in result

    def test_has_banned_words(self):
        result = generate_voice(_make_profile())
        assert "banned_words" in result


class TestAbsoluteBannedWords:
    def test_banned_words_includes_all_eight_absolute(self):
        result = generate_voice(_make_profile())
        missing = ABSOLUTE_BANNED_WORDS - set(result["banned_words"])
        assert not missing, f"Missing absolute banned words: {missing}"


class TestDosAndDonts:
    def test_dos_has_at_least_three_items(self):
        result = generate_voice(_make_profile())
        assert len(result["dos"]) >= 3, (
            f"dos list has {len(result['dos'])} items, needs ≥3"
        )

    def test_donts_has_at_least_three_items(self):
        result = generate_voice(_make_profile())
        assert len(result["donts"]) >= 3, (
            f"donts list has {len(result['donts'])} items, needs ≥3"
        )


class TestSampleTagline:
    def test_sample_tagline_is_non_empty(self):
        result = generate_voice(_make_profile())
        assert result["sample_tagline"], "sample_tagline is empty"

    def test_sample_tagline_has_no_banned_words(self):
        result = generate_voice(_make_profile())
        tagline_lower = result["sample_tagline"].lower()
        for word in result["banned_words"]:
            assert word.lower() not in tagline_lower, (
                f"Tagline contains banned word '{word}': {result['sample_tagline']}"
            )


class TestDifferentProfilesDifferentVoice:
    def test_different_profiles_produce_different_voice(self):
        coffee = _make_profile(
            name="Warm Roast",
            industry="coffee",
            personality_words=["warm", "artisanal", "craft"],
            mood="Warm",
        )
        fintech = _make_profile(
            name="Precise Capital",
            industry="fintech",
            personality_words=["precise", "secure", "authoritative"],
            mood="Precise",
        )
        r1 = generate_voice(coffee)
        r2 = generate_voice(fintech)
        assert r1["tone"] != r2["tone"], "Tone should differ for different brands"
        assert r1["dos"] != r2["dos"], "dos should differ for different brands"
