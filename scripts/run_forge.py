#!/usr/bin/env python3
"""Brand Studio Forge — identity generation pipeline."""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from forge.src.brand_profile import BrandProfile
from forge.src.identity_kit import assemble_identity
from forge.src.providers.keystore import KeyStore
from forge.src.providers.registry import available_providers


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Brand Studio Forge — identity generation pipeline"
    )
    parser.add_argument("--profile", required=True, help="Path to brand_profile.json")
    parser.add_argument(
        "--output-dir", default="./output", help="Output directory (default: ./output)"
    )
    parser.add_argument(
        "--skip-render", action="store_true", help="Skip PDF/PNG generation"
    )
    parser.add_argument(
        "--skip-skill", action="store_true", help="Skip .py skill generation"
    )
    args = parser.parse_args()

    profile_path = os.path.abspath(args.profile)
    if not os.path.exists(profile_path):
        print(f"ERROR: Profile not found: {profile_path}", file=sys.stderr)
        sys.exit(1)

    profile = BrandProfile.load(profile_path)

    keystore = KeyStore()

    if not keystore.has_any_provider():
        print("\n=== Image Generation Setup ===")
        print("To generate brand imagery, you need at least one API key.")
        print("Keys are saved to ~/.forge/keys.json (only asked once).\n")
        print("Supported providers:")
        print("  1. gemini  — Google Gemini 3.1 Flash Image (Nano Banana 2)")
        print("  2. chatgpt — OpenAI GPT Image 2")
        print("")

        gemini_key = input("Google Gemini API key (Enter to skip): ").strip()
        if gemini_key:
            keystore.set("gemini", gemini_key)

        openai_key = input("OpenAI API key (Enter to skip): ").strip()
        if openai_key:
            keystore.set("chatgpt", openai_key)

        if keystore.has_any_provider():
            keystore.save()
            print(f"\nKeys saved. Available providers: {', '.join(keystore.available_providers())}")
        else:
            print("\nNo keys provided. Imagery section will use placeholders.")
    else:
        print(f"[+] Image providers loaded: {', '.join(keystore.available_providers())}")

    assembled = assemble_identity(profile)

    output_dir = os.path.abspath(args.output_dir)
    os.makedirs(output_dir, exist_ok=True)

    output_profile_path = os.path.join(output_dir, "brand_profile.json")
    assembled.save(output_profile_path)
    print(f"[+] Updated profile: {output_profile_path}")

    generated_files: list[str] = [output_profile_path]

    if not args.skip_render:
        try:
            from forge.src.render import render_brand_kit

            render_results = render_brand_kit(assembled, output_dir)
            for key, path_val in render_results.items():
                print(f"[+] Rendered {key}: {path_val}")
                generated_files.append(path_val)
        except ImportError as e:
            print(
                f"WARNING: Playwright not available — skipping render ({e})",
                file=sys.stderr,
            )
            print(
                "Install with: pip install playwright && playwright install chromium",
                file=sys.stderr,
            )

    if not args.skip_skill:
        try:
            from forge.src.skill_forge import forge_skill

            skill_path = forge_skill(assembled)
            print(f"[+] Skill forged: {skill_path}")
            generated_files.append(skill_path)
        except ImportError as e:
            print(f"WARNING: Could not import skill_forge ({e})", file=sys.stderr)

    print(f"\n=== Generated {len(generated_files)} files ===")
    for f in generated_files:
        print(f"  {f}")


if __name__ == "__main__":
    main()
