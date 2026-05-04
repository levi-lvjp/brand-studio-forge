from __future__ import annotations

import os
import sys
import tempfile
import textwrap
from pathlib import Path

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from forge.src.brand_profile import BrandProfile
from forge.src.skill_forge import forge_skill, forge_skill_preview


_ABSOLUTE_BANS = {
    "elevate",
    "empower",
    "seamless",
    "leverage",
    "innovative",
    "cutting-edge",
    "transform",
    "unlock",
}

_REQUIRED_BRAND_KEYS = {
    "name",
    "voice",
    "primary_color",
    "secondary_color",
    "display_font",
    "body_font",
    "tagline",
    "tone_rules",
    "content_types",
    "banned_words",
}


def _profile_fully_populated(**overrides) -> BrandProfile:
    kwargs = {
        "name": "ACME Coffee! Roasters",
        "industry": "Specialty Coffee",
        "personality_words": ["bold", "warm", "unpretentious"],
        "positioning_statement": "Coffee that wakes up the neighborhood.",
        "target_audience": "commuters and remote workers",
        "competitors": ["Blue Bottle", "Stumptown"],
        "anti_references": ["Starbucks", "pretentious third-wave"],
        "color_strategy": "committed",
        "primary_color": "#a44a22",
        "secondary_color": "#2d5a3f",
        "neutral_tone": "#f5e6d3",
        "display_font": "Obviously",
        "body_font": "Source Serif 4",
        "logo_type": "wordmark",
        "logo_strategy": "bold-typographic",
        "voice_tone": "direct and warm like a neighborhood barista",
        "voice_dos": [
            "short sentences",
            "concrete details",
            "local flavor references",
        ],
        "voice_donts": ["jargon", "wine-tasting descriptors", "hustle culture"],
        "tagline": "Roasted here. Brewed here. Shared here.",
        "mood": "early-morning-golden-hour",
    }
    kwargs.update(overrides)
    return BrandProfile(**kwargs)


def test_forge_skill_creates_file_at_expected_path(tmp_path):
    profile = _profile_fully_populated()
    result = forge_skill(profile, output_dir=str(tmp_path))

    assert os.path.isfile(result)
    expected_filename = "brand_acme_coffee_roasters_content.py"
    assert Path(result).name == expected_filename


def test_generated_file_compiles_without_syntax_error(tmp_path):
    profile = _profile_fully_populated()
    result = forge_skill(profile, output_dir=str(tmp_path))

    with open(result) as f:
        code = f.read()
    compile(code, result, "exec")


def test_generated_code_contains_brand_dict_with_required_keys(tmp_path):
    profile = _profile_fully_populated()
    result = forge_skill(profile, output_dir=str(tmp_path))

    with open(result) as f:
        code = f.read()

    namespace = {}
    exec(compile(code, result, "exec"), namespace)
    brand = namespace.get("BRAND")
    assert brand is not None, "BRAND dict not found in generated code"
    missing = _REQUIRED_BRAND_KEYS - set(brand.keys())
    assert not missing, f"Missing BRAND keys: {missing}"


def test_generate_content_function_exists_and_returns_prompt_with_brand_name(tmp_path):
    profile = _profile_fully_populated()
    result = forge_skill(profile, output_dir=str(tmp_path))

    namespace = {}
    exec(compile(open(result).read(), result, "exec"), namespace)

    func = namespace.get("generate_content")
    assert func is not None, "generate_content not found"
    prompt = func("instagram_caption", "Cold brew launch")
    assert isinstance(prompt, str)
    assert profile.name in prompt


def test_generate_weekly_calendar_returns_dict_with_7_day_keys(tmp_path):
    profile = _profile_fully_populated()
    result = forge_skill(profile, output_dir=str(tmp_path))

    namespace = {}
    exec(compile(open(result).read(), result, "exec"), namespace)

    func = namespace.get("generate_weekly_calendar")
    assert func is not None
    calendar = func()
    assert isinstance(calendar, dict)
    assert len(calendar) == 7
    days = {
        "monday",
        "tuesday",
        "wednesday",
        "thursday",
        "friday",
        "saturday",
        "sunday",
    }
    assert set(calendar.keys()) == days


def test_get_brand_info_returns_brand_dict(tmp_path):
    profile = _profile_fully_populated()
    result = forge_skill(profile, output_dir=str(tmp_path))

    namespace = {}
    exec(compile(open(result).read(), result, "exec"), namespace)

    func = namespace.get("get_brand_info")
    assert func is not None
    info = func()
    assert info is namespace["BRAND"]


@pytest.mark.parametrize(
    "name_input,expected_slug",
    [
        ("ACME Coffee! Roasters", "acme_coffee_roasters"),
        ("Müller & Sons", "muller_sons"),
        ("  Trim Me  ", "trim_me"),
        ("Hello---World", "hello_world"),
        ("Café 99!", "cafe_99"),
        ("simple", "simple"),
    ],
)
def test_slug_generation_handles_special_chars(name_input, expected_slug, tmp_path):
    profile = _profile_fully_populated(name=name_input)
    result = forge_skill(profile, output_dir=str(tmp_path))

    expected_filename = f"brand_{expected_slug}_content.py"
    assert Path(result).name == expected_filename


def test_forge_skill_preview_returns_string_without_creating_files(tmp_path):
    profile = _profile_fully_populated()
    before = set(os.listdir(tmp_path))

    result = forge_skill_preview(profile)

    assert isinstance(result, str)
    assert "BRAND" in result
    after = set(os.listdir(tmp_path))
    assert before == after, "forge_skill_preview created files on disk"


def test_banned_words_always_includes_absolute_bans(tmp_path):
    profile = _profile_fully_populated(
        voice_donts=["jargon", "wine-tasting descriptors"]
    )
    result = forge_skill(profile, output_dir=str(tmp_path))

    namespace = {}
    exec(compile(open(result).read(), result, "exec"), namespace)

    brand = namespace["BRAND"]
    banned = set(w.lower() for w in brand["banned_words"])
    for ban in _ABSOLUTE_BANS:
        assert ban in banned, f"Absolute ban '{ban}' missing from banned_words"


def test_brand_docstring_in_generated_file(tmp_path):
    profile = _profile_fully_populated()
    result = forge_skill(profile, output_dir=str(tmp_path))

    with open(result) as f:
        code = f.read()
    assert profile.name in code.splitlines()[0]
    assert "Auto-generated by Brand Studio Forge" in code


def test_generated_content_types_have_instructions(tmp_path):
    profile = _profile_fully_populated()
    result = forge_skill(profile, output_dir=str(tmp_path))

    namespace = {}
    exec(compile(open(result).read(), result, "exec"), namespace)

    ct = namespace["BRAND"]["content_types"]
    assert isinstance(ct, dict)
    for key in ct:
        assert isinstance(ct[key], str)
        assert len(ct[key]) > 0
