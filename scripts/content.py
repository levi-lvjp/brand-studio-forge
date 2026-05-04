#!/usr/bin/env python3
"""Branded content generation CLI."""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from forge.src.brand_profile import BrandProfile

CONTENT_TYPES = [
    "instagram_caption",
    "email_subject",
    "blog_intro",
    "tweet",
    "linkedin_post",
]


def _make_profile_path_module(path: str) -> str:
    abs_path = os.path.abspath(path)
    return f'r"{abs_path}"'


def main() -> None:
    parser = argparse.ArgumentParser(description="Branded content generation CLI")
    parser.add_argument("--profile", required=True, help="Path to brand_profile.json")
    parser.add_argument(
        "--type",
        default="instagram_caption",
        choices=CONTENT_TYPES,
        help="Content type",
    )
    parser.add_argument("--topic", default="brand update", help="Content topic")
    parser.add_argument(
        "--calendar",
        action="store_true",
        help="Generate weekly calendar instead of single content",
    )
    args = parser.parse_args()

    profile_path = os.path.abspath(args.profile)
    if not os.path.exists(profile_path):
        print(f"ERROR: Profile not found: {profile_path}", file=sys.stderr)
        sys.exit(1)

    profile = BrandProfile.load(profile_path)

    try:
        from forge.src.skill_forge import forge_skill_preview
    except ImportError:
        print("ERROR: forge.src.skill_forge module not available", file=sys.stderr)
        sys.exit(1)

    skill_code = forge_skill_preview(profile)

    brand_dict = {
        "name": profile.name,
        "voice": profile.voice_tone or "professional",
        "primary_color": profile.primary_color or "#000000",
        "secondary_color": profile.secondary_color or "#ffffff",
        "display_font": profile.display_font or "Inter",
        "body_font": profile.body_font or "Inter",
        "tagline": profile.tagline or "",
        "tone_rules": profile.voice_dos or [],
        "banned_words": profile.voice_donts or [],
    }

    if args.calendar:
        prompt = (
            f"You are the voice of {brand_dict['name']}. "
            f"Voice: {brand_dict['voice']}\n\n"
            f"Tone: {', '.join(brand_dict['tone_rules'])}\n\n"
            f"Create a 7-day content calendar for {brand_dict['name']}. "
            f"For each day, provide a content type and topic idea."
        )
    else:
        prompt = (
            f"You are the voice of {brand_dict['name']}. "
            f"Voice: {brand_dict['voice']}\n\n"
            f"Tone: {', '.join(brand_dict['tone_rules'])}\n"
            f"Banned words: {', '.join(brand_dict['banned_words'])}\n\n"
            f"Generate {args.type} content about: {args.topic}"
        )

    print(prompt)


if __name__ == "__main__":
    main()
