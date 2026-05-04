import json
import os
import sys
import tempfile

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

import pytest

from forge.src.brand_profile import BrandProfile


def _minimal_profile() -> BrandProfile:
    return BrandProfile(
        name="Roast & Co",
        industry="Coffee",
        personality_words=["rugged", "aromatic", "unhurried"],
        positioning_statement="The only coffee roastery that ages beans in whiskey barrels",
        target_audience="Urban professionals who grind their own beans",
        competitors=["Blue Bottle", "Stumptown"],
        anti_references=["Starbucks green siren", "generic latte art"],
    )


def _complete_profile() -> BrandProfile:
    p = _minimal_profile()
    p.color_strategy = "Committed"
    p.primary_color = "oklch(45% 0.15 30)"
    p.secondary_color = "oklch(70% 0.08 60)"
    p.accent_color = "oklch(55% 0.12 230)"
    p.neutral_tone = "oklch(92% 0.02 30)"
    p.display_font = "Eczar"
    p.body_font = "Source Serif 4"
    p.logo_type = "wordmark"
    p.logo_strategy = "Typographic with ligature"
    p.voice_tone = "warm, artisanal, unhurried"
    p.voice_dos = ["Use sensory language", "Reference craft process"]
    p.voice_donts = ["Use corporate jargon", "Mention 'premium'"]
    p.tagline = "Barrel-aged patience"
    p.mood = "Craft Heritage"
    return p


class TestBrandProfileSerialization:
    def test_roundtrip_minimal(self):
        original = _minimal_profile()
        data = original.to_json()
        restored = BrandProfile.from_json(data)
        assert restored.name == original.name
        assert restored.industry == original.industry
        assert restored.personality_words == original.personality_words
        assert restored.positioning_statement == original.positioning_statement
        assert restored.target_audience == original.target_audience
        assert restored.competitors == original.competitors
        assert restored.anti_references == original.anti_references
        assert restored.color_strategy is None
        assert restored.voice_dos is None

    def test_roundtrip_complete(self):
        original = _complete_profile()
        data = original.to_json()
        restored = BrandProfile.from_json(data)
        assert restored.name == original.name
        assert restored.color_strategy == original.color_strategy
        assert restored.primary_color == original.primary_color
        assert restored.secondary_color == original.secondary_color
        assert restored.neutral_tone == original.neutral_tone
        assert restored.display_font == original.display_font
        assert restored.body_font == original.body_font
        assert restored.logo_type == original.logo_type
        assert restored.logo_strategy == original.logo_strategy
        assert restored.voice_tone == original.voice_tone
        assert restored.voice_dos == original.voice_dos
        assert restored.voice_donts == original.voice_donts
        assert restored.tagline == original.tagline
        assert restored.mood == original.mood

    def test_to_json_returns_dict(self):
        p = _minimal_profile()
        data = p.to_json()
        assert isinstance(data, dict)
        assert data["name"] == "Roast & Co"

    def test_to_json_is_json_serializable(self):
        p = _complete_profile()
        raw = json.dumps(p.to_json())
        assert isinstance(raw, str)


class TestBrandProfilePersistence:
    def test_save_load_roundtrip(self, tmp_path):
        original = _complete_profile()
        path = str(tmp_path / "profile.json")
        original.save(path)
        assert os.path.exists(path)
        restored = BrandProfile.load(path)
        assert restored.name == original.name
        assert restored.color_strategy == original.color_strategy
        assert restored.voice_dos == original.voice_dos
        assert restored.mood == original.mood

    def test_save_creates_valid_json(self, tmp_path):
        p = _minimal_profile()
        path = str(tmp_path / "profile.json")
        p.save(path)
        with open(path) as f:
            data = json.load(f)
        assert data["name"] == "Roast & Co"


class TestIsComplete:
    def test_partial_profile_is_not_complete(self):
        p = _minimal_profile()
        assert p.is_complete() is False

    def test_complete_profile_is_complete(self):
        p = _complete_profile()
        assert p.is_complete() is True

    def test_missing_single_field_is_not_complete(self):
        p = _complete_profile()
        p.tagline = None
        assert p.is_complete() is False

    def test_missing_list_field_is_not_complete(self):
        p = _complete_profile()
        p.voice_dos = None
        assert p.is_complete() is False
