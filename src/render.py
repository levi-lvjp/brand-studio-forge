from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from playwright.sync_api import sync_playwright

from forge.src.brand_profile import BrandProfile
from forge.src.identity_kit import assemble_identity_dict


def _substitute_template(template: str, variables: dict) -> str:
    result = template
    for key, value in variables.items():
        placeholder = "{{" + key + "}}"
        if isinstance(value, list):
            if not value:
                rendered = ""
            else:
                rendered = "\n".join(f"        <li>{item}</li>" for item in value)
        elif isinstance(value, dict):
            rendered = ""
        else:
            rendered = str(value)
        result = result.replace(placeholder, rendered)
    return result


def _launch_browser():
    try:
        p = sync_playwright().start()
        browser = p.chromium.launch()
        return p, browser
    except Exception as exc:
        raise RuntimeError(
            "Playwright Chromium failed to launch. "
            "Run: pip install playwright && playwright install chromium"
        ) from exc


def render_pdf(template_path: str, variables: dict, output_path: str) -> str:
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found: {template_path}")

    with open(template_path) as f:
        template = f.read()

    html = _substitute_template(template, variables)

    p, browser = _launch_browser()
    try:
        context = browser.new_context()
        page = context.new_page()
        page.set_content(html)
        page.pdf(
            path=output_path,
            format="A4",
            print_background=True,
            margin={"top": "0", "bottom": "0", "left": "0", "right": "0"},
        )
    finally:
        browser.close()
        p.stop()

    return output_path


def render_png(
    template_path: str,
    variables: dict,
    output_path: str,
    width: int = 1080,
    height: int = 1080,
) -> str:
    if not os.path.exists(template_path):
        raise FileNotFoundError(f"Template not found: {template_path}")

    with open(template_path) as f:
        template = f.read()

    html = _substitute_template(template, variables)

    p, browser = _launch_browser()
    try:
        context = browser.new_context()
        page = context.new_page()
        page.set_viewport_size({"width": width, "height": height})
        page.set_content(html)
        page.screenshot(
            path=output_path,
            full_page=False,
            clip={"x": 0, "y": 0, "width": width, "height": height},
        )
    finally:
        browser.close()
        p.stop()

    return output_path


def render_brand_kit(profile: BrandProfile, output_dir: str = "./output") -> dict:
    os.makedirs(output_dir, exist_ok=True)
    variables = assemble_identity_dict(profile)

    base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    templates_dir = os.path.join(base, "assets", "templates")

    template_map = {
        "guidelines": ("brand_guidelines.html", "brand_guidelines.pdf", render_pdf),
        "business_card": ("business_card.html", "business_card.pdf", render_pdf),
        "logo_sheet": ("logo_sheet.html", "logo_sheet.pdf", render_pdf),
        "social_post": ("social_post.html", "social_post.png", render_png),
    }

    results = {}
    for key, (tmpl_file, out_file, render_fn) in template_map.items():
        tmpl_path = os.path.join(templates_dir, tmpl_file)
        out_path = os.path.join(output_dir, out_file)
        if key == "social_post":
            results[key] = render_fn(
                tmpl_path, variables, out_path, width=1080, height=1080
            )
        else:
            results[key] = render_fn(tmpl_path, variables, out_path)

    return results
