from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from forge.src.brand_profile import BrandProfile
from forge.src.identity_kit import assemble_identity, assemble_identity_dict


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


class TestAssembleIdentityColor:
    def test_fills_primary_color(self):
        profile = _make_profile()
        result = assemble_identity(profile)
        assert result.primary_color is not None

    def test_fills_secondary_color(self):
        profile = _make_profile()
        result = assemble_identity(profile)
        assert result.secondary_color is not None

    def test_fills_neutral_tone(self):
        profile = _make_profile()
        result = assemble_identity(profile)
        assert result.neutral_tone is not None


class TestAssembleIdentityTypography:
    def test_fills_display_font(self):
        profile = _make_profile()
        result = assemble_identity(profile)
        assert result.display_font is not None

    def test_fills_body_font(self):
        profile = _make_profile()
        result = assemble_identity(profile)
        assert result.body_font is not None


class TestAssembleIdentityVoice:
    def test_fills_voice_tone(self):
        profile = _make_profile()
        result = assemble_identity(profile)
        assert result.voice_tone is not None

    def test_fills_voice_dos(self):
        profile = _make_profile()
        result = assemble_identity(profile)
        assert result.voice_dos is not None

    def test_fills_voice_donts(self):
        profile = _make_profile()
        result = assemble_identity(profile)
        assert result.voice_donts is not None

    def test_fills_tagline(self):
        profile = _make_profile()
        result = assemble_identity(profile)
        assert result.tagline is not None


class TestAssembleIdentityDict:
    REQUIRED_KEYS = {
        "BRAND_NAME",
        "PRIMARY_COLOR",
        "SECONDARY_COLOR",
        "NEUTRAL_TONE",
        "DISPLAY_FONT",
        "BODY_FONT",
        "LOGO_SVG",
        "VOICE_DESCRIPTION",
        "VOICE_DOS",
        "VOICE_DONTS",
        "COLOR_PALETTE",
        "TYPOGRAPHY_HIERARCHY",
        "TAGLINE",
    }

    def test_returns_dict_with_all_template_keys(self):
        profile = _make_profile()
        assembled = assemble_identity(profile)
        result = assemble_identity_dict(assembled)
        missing = self.REQUIRED_KEYS - set(result.keys())
        assert not missing, f"Missing keys: {missing}"

    def test_color_palette_is_html_string_with_swatch(self):
        profile = _make_profile()
        assembled = assemble_identity(profile)
        result = assemble_identity_dict(assembled)
        assert isinstance(result["COLOR_PALETTE"], str)
        assert "swatch" in result["COLOR_PALETTE"]
        assert "swatch__color" in result["COLOR_PALETTE"]

    def test_typography_hierarchy_is_string(self):
        profile = _make_profile()
        assembled = assemble_identity(profile)
        result = assemble_identity_dict(assembled)
        assert isinstance(result["TYPOGRAPHY_HIERARCHY"], str)
        assert len(result["TYPOGRAPHY_HIERARCHY"]) > 0


class TestAssembleIdentityDictLogoImages:
    def test_img_tags_replace_svg_when_logo_images_set(self):
        from unittest import mock

        fake_img_tag = '<img src="data:image/png;base64,Zm9v" alt="logo" style="max-width:100%;max-height:100%">'
        fake_logo_images = {
            "logo_img_tag": fake_img_tag,
            "logo_icon_img_tag": fake_img_tag,
            "logo_mono_img_tag": fake_img_tag,
            "logo_files": [],
        }

        profile = _make_profile()
        profile.image_provider = "gemini"
        profile.image_provider_config = None

        with mock.patch("forge.src.identity_kit.assemble_identity") as mock_assemble:
            assembled = _make_profile()
            assembled.primary_color = "oklch(50% 0.15 250)"
            assembled.secondary_color = "oklch(70% 0.08 180)"
            assembled.neutral_tone = "oklch(92% 0.02 50)"
            assembled.display_font = "Bitter"
            assembled.body_font = "Work Sans"
            assembled.voice_tone = "warm"
            assembled.voice_dos = ["a"]
            assembled.voice_donts = ["b"]
            assembled.tagline = "test"
            assembled._logo_images = fake_logo_images
            mock_assemble.return_value = assembled

            result = assemble_identity_dict(profile)

            assert "LOGO_SVG" in result
            assert "data:image/png;base64,Zm9v" in result["LOGO_SVG"], (
                f"Expected img tag in LOGO_SVG, got: {result['LOGO_SVG']}"
            )
            assert not result["LOGO_SVG"].startswith("<svg"), (
                f"LOGO_SVG should be img tag, got SVG: {result['LOGO_SVG']}"
            )

            assert "data:image/png;base64,Zm9v" in result["LOGO_ICON_SVG"]
            assert not result["LOGO_ICON_SVG"].startswith("<svg")

            assert "data:image/png;base64,Zm9v" in result["LOGO_MONO_SVG"]
            assert not result["LOGO_MONO_SVG"].startswith("<svg")


class TestAssembledProfileCompleteness:
    def test_assembled_profile_is_nearly_complete(self):
        profile = _make_profile()
        result = assemble_identity(profile)
        assert result.primary_color is not None
        assert result.secondary_color is not None
        assert result.neutral_tone is not None
        assert result.display_font is not None
        assert result.body_font is not None
        assert result.voice_tone is not None
        assert result.voice_dos is not None
        assert result.voice_donts is not None
        assert result.tagline is not None
        assert result.color_strategy is not None
