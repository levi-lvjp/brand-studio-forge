#!/usr/bin/env python3
"""Brand interview CLI — guided brand discovery."""

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from forge.src.brand_profile import BrandProfile

MOODS = [
    "Warm",
    "Precise",
    "Rebellious",
    "Serene",
    "Playful",
    "Commanding",
    "Heritage",
    "Minimal",
    "Raw",
    "Lush",
]


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Brand interview CLI — guided brand discovery"
    )
    parser.add_argument(
        "--output-dir", default=".", help="Output directory for profile and PRODUCT.md"
    )
    args = parser.parse_args()

    output_dir = os.path.abspath(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    print("=== Brand Studio Forge — Interview ===\n")
    print(
        "Let's discover your brand. Answer each question to build your brand profile.\n"
    )

    name = input("Brand name: ").strip()
    industry = input("Industry / category: ").strip()
    what = input("What does the brand do? (one sentence): ").strip()
    audience = input("Who is the target audience? ").strip()

    print(
        "\nPick three personality words — use physical-object words, not 'modern' or 'elegant'."
    )
    personality_raw = input("Three personality words (comma-separated): ").strip()
    personality_words = [w.strip() for w in personality_raw.split(",") if w.strip()]

    anti_raw = input(
        "\nWhat is this brand NOT? (anti-references, comma-separated): "
    ).strip()
    anti_references = [a.strip() for a in anti_raw.split(",") if a.strip()]

    comp_raw = input("Top 3 competitors (comma-separated): ").strip()
    competitors = [c.strip() for c in comp_raw.split(",") if c.strip()]

    print(f"\nChoose a mood: {', '.join(MOODS)}")
    mood = input("Mood: ").strip()

    print("\n--- Logo Image Generation ---")
    print("1. gemini   — Google Gemini Imagen (requires GEMINI_API_KEY)")
    print("2. chatgpt  — OpenAI gpt-image-1 (requires OPENAI_API_KEY)")
    print("3. flux     — fal.ai FLUX/schnell (requires FAL_KEY)")
    print("4. custom   — OpenAI-compatible endpoint")
    print("5. skip     — No image generation (text placeholder)")
    choice = input("Select provider (1-5): ").strip()

    provider_map = {"1": "gemini", "2": "chatgpt", "3": "flux"}
    image_provider: str | None = None
    image_provider_config: dict | None = None

    if choice in provider_map:
        image_provider = provider_map[choice]
    elif choice == "4":
        image_provider = "custom"
        base_url = input("  base_url: ").strip()
        model = input("  model: ").strip()
        api_key = input("  api_key: ").strip()
        image_provider_config = {
            "base_url": base_url,
            "model": model,
            "api_key": api_key,
        }

    profile = BrandProfile(
        name=name,
        industry=industry,
        personality_words=personality_words,
        positioning_statement=what,
        target_audience=audience,
        competitors=competitors,
        anti_references=anti_references,
        mood=mood,
        image_provider=image_provider,
        image_provider_config=image_provider_config,
    )

    profile_path = os.path.join(output_dir, "brand_profile.json")
    profile.save(profile_path)
    print(f"\nBrandProfile saved to: {profile_path}")

    product_md = f"""# {name} — Brand Brief

## What it does
{what}

## Industry
{industry}

## Target audience
{audience}

## Personality
{", ".join(personality_words)}

## Mood
{mood}

## This is NOT
{", ".join(anti_references)}

## Competitors
{", ".join(competitors)}
"""
    product_path = os.path.join(output_dir, "PRODUCT.md")
    with open(product_path, "w") as f:
        f.write(product_md)
    print(f"PRODUCT.md saved to: {product_path}")

    print(f"\n=== Summary ===")
    print(f"Brand: {name}")
    print(f"Industry: {industry}")
    print(f"Personality: {', '.join(personality_words)}")
    print(f"Mood: {mood}")
    print(f"\nNext step: run forge/scripts/run_forge.py --profile {profile_path}")


if __name__ == "__main__":
    main()
