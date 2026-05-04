from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from forge.src.brand_profile import BrandProfile
from forge.src.logo import generate_logo_prompts

VALID_LOGO_TYPES = {
    "wordmark",
    "lettermark",
    "pictorial",
    "abstract",
    "emblem",
    "combination",
    "dynamic",
    "signature",
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
        "primary_color": "#c17a3a",
        "secondary_color": "#e8d5b7",
        "tagline": "Brewed with patience",
    }
    defaults.update(overrides)
    return BrandProfile(**defaults)


class TestOutputRequiredKeys:
    def test_has_all_required_keys(self):
        profile = _make_profile()
        result = generate_logo_prompts(profile)
        required_keys = {
            "primary_prompt",
            "icon_prompt",
            "monochrome_prompt",
            "negative_prompt",
            "logo_type",
            "strategy",
            "reasoning",
        }
        assert set(result.keys()) == required_keys


class TestPromptValuesNonEmpty:
    def test_primary_prompt_non_empty(self):
        result = generate_logo_prompts(_make_profile())
        assert isinstance(result["primary_prompt"], str)
        assert len(result["primary_prompt"]) > 0

    def test_icon_prompt_non_empty(self):
        result = generate_logo_prompts(_make_profile())
        assert isinstance(result["icon_prompt"], str)
        assert len(result["icon_prompt"]) > 0

    def test_monochrome_prompt_non_empty(self):
        result = generate_logo_prompts(_make_profile())
        assert isinstance(result["monochrome_prompt"], str)
        assert len(result["monochrome_prompt"]) > 0

    def test_negative_prompt_non_empty(self):
        result = generate_logo_prompts(_make_profile())
        assert isinstance(result["negative_prompt"], str)
        assert len(result["negative_prompt"]) > 0

    def test_reasoning_non_empty(self):
        result = generate_logo_prompts(_make_profile())
        assert isinstance(result["reasoning"], str)
        assert len(result["reasoning"]) > 0


class TestNegativePromptAntiSlop:
    def test_negative_prompt_contains_clipart(self):
        result = generate_logo_prompts(_make_profile())
        assert "clipart" in result["negative_prompt"].lower()

    def test_negative_prompt_contains_generic(self):
        result = generate_logo_prompts(_make_profile())
        assert "generic" in result["negative_prompt"].lower()

    def test_negative_prompt_contains_glossy(self):
        result = generate_logo_prompts(_make_profile())
        assert "glossy" in result["negative_prompt"].lower()


class TestBrandNameInPrimaryPrompt:
    def test_brand_name_appears_in_primary_prompt(self):
        profile = _make_profile(name="Roast & Reverie")
        result = generate_logo_prompts(profile)
        assert "Roast & Reverie" in result["primary_prompt"]


class TestDifferentProfilesDifferentPrompts:
    def test_coffee_and_tech_produce_different_prompts(self):
        coffee = _make_profile(
            name="Warm Roast",
            industry="coffee",
            personality_words=["warm", "artisanal", "craft"],
        )
        tech = _make_profile(
            name="DataPulse",
            industry="technology",
            personality_words=["precise", "innovative", "fast"],
            primary_color="#2d3436",
            secondary_color="#6c5ce7",
            tagline="Analyze everything",
        )
        coffee_result = generate_logo_prompts(coffee)
        tech_result = generate_logo_prompts(tech)
        assert coffee_result["primary_prompt"] != tech_result["primary_prompt"]


class TestLogoTypeValid:
    def test_logo_type_is_valid(self):
        result = generate_logo_prompts(_make_profile())
        assert result["logo_type"] in VALID_LOGO_TYPES


class TestStrategyNonEmpty:
    def test_strategy_is_non_empty_string(self):
        result = generate_logo_prompts(_make_profile())
        assert isinstance(result["strategy"], str)
        assert len(result["strategy"]) > 0
