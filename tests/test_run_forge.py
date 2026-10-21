from __future__ import annotations

import os
import sys
from unittest import mock

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from scripts.run_forge import _pick_provider, _validate_profile
from forge.src.brand_profile import BrandProfile


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


class TestValidateProfile:
    def test_accepts_valid_profile(self):
        _validate_profile(_make_profile())

    def test_rejects_empty_name(self):
        with pytest.raises(ValueError):
            _validate_profile(_make_profile(name=""))

    def test_rejects_empty_industry(self):
        with pytest.raises(ValueError):
            _validate_profile(_make_profile(industry=""))

    def test_rejects_missing_personality_words(self):
        with pytest.raises(ValueError):
            _validate_profile(_make_profile(personality_words=[]))


class TestPickProvider:
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_returns_none_when_nothing_available(self):
        assert _pick_provider(_make_profile()) is None

    @mock.patch.dict(os.environ, {"OPENAI_API_KEY": "x"}, clear=True)
    def test_falls_back_to_available_preset(self):
        profile = _make_profile(image_provider="gemini")
        assert _pick_provider(profile) == "chatgpt"

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_uses_custom_when_config_present(self):
        profile = _make_profile(
            image_provider="custom",
            image_provider_config={"base_url": "https://example.com", "model": "x"},
        )
        assert _pick_provider(profile) == "custom"
