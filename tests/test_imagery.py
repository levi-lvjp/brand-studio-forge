import os
from unittest.mock import patch, MagicMock

from forge.src.brand_profile import BrandProfile
from forge.src.imagery import generate_brand_imagery, build_imagery_prompt


def _make_profile():
    return BrandProfile(
        name="Pencil",
        industry="stationery",
        personality_words=["precise", "quiet", "tactile"],
        mood="Minimal",
        primary_color="oklch(95% 0.02 215)",
    )


def test_build_imagery_prompt_photography():
    profile = _make_profile()
    prompt = build_imagery_prompt(profile, style="photography")
    assert "stationery" in prompt.lower() or "Pencil" in prompt
    assert "photo" in prompt.lower()


def test_build_imagery_prompt_illustration():
    profile = _make_profile()
    prompt = build_imagery_prompt(profile, style="illustration")
    assert "illustration" in prompt.lower()


def test_generate_brand_imagery_saves_files(tmp_path):
    profile = _make_profile()
    fake_bytes = b"\x89PNG\r\n\x1a\n" + b"\x00" * 100

    mock_result = {
        "url": None,
        "image_bytes": fake_bytes,
        "prompt_used": "test",
        "fallback": False,
        "error": None,
    }

    with patch("forge.src.imagery.get_provider") as mock_get:
        mock_provider = MagicMock()
        mock_provider.generate.return_value = mock_result
        mock_get.return_value = mock_provider

        paths = generate_brand_imagery(profile, output_dir=str(tmp_path), provider_name="gemini")

    assert "photography" in paths
    assert "illustration" in paths
    assert os.path.exists(paths["photography"])
    assert os.path.exists(paths["illustration"])


def test_generate_brand_imagery_fallback_returns_none(tmp_path):
    profile = _make_profile()

    mock_result = {
        "url": None,
        "image_bytes": None,
        "prompt_used": "test",
        "fallback": True,
        "error": "no key",
    }

    with patch("forge.src.imagery.get_provider") as mock_get:
        mock_provider = MagicMock()
        mock_provider.generate.return_value = mock_result
        mock_get.return_value = mock_provider

        paths = generate_brand_imagery(profile, output_dir=str(tmp_path), provider_name="gemini")

    assert paths["photography"] is None
    assert paths["illustration"] is None
