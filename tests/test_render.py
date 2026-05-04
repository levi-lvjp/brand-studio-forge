from __future__ import annotations

import os
import sys
import tempfile
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from forge.src.brand_profile import BrandProfile
from forge.src.render import render_pdf, render_png, _substitute_template


def _make_profile(**overrides) -> BrandProfile:
    defaults = {
        "name": "Test Brand",
        "industry": "coffee",
        "personality_words": ["warm", "artisanal", "craft"],
        "positioning_statement": "Handcrafted coffee for the mindful drinker",
        "target_audience": "Coffee enthusiasts 25-45",
        "competitors": ["Blue Bottle", "Stumptown"],
        "anti_references": ["Starbucks", "Dunkin"],
        "primary_color": "oklch(70% 0.15 45)",
        "secondary_color": "oklch(80% 0.08 165)",
        "neutral_tone": "oklch(95% 0.02 45)",
        "display_font": "Bitter",
        "body_font": "Work Sans",
        "voice_tone": "authoritative, declarative, measured",
        "voice_dos": ["Write clearly", "Be direct", "Use data"],
        "voice_donts": ["Never use jargon", "Avoid fluff"],
        "tagline": "Made right. Told true.",
        "color_strategy": "Committed",
    }
    defaults.update(overrides)
    return BrandProfile(**defaults)


def _make_mock_pw_chain():
    mock_page = mock.MagicMock()
    mock_context = mock.MagicMock()
    mock_browser = mock.MagicMock()
    mock_playwright = mock.MagicMock()

    mock_page.pdf.return_value = b"fake pdf"
    mock_context.new_page.return_value = mock_page
    mock_browser.new_context.return_value = mock_context
    mock_playwright.chromium.launch.return_value = mock_browser

    mock_pw = mock.MagicMock()
    mock_pw.start.return_value = mock_playwright
    mock_playwright.start.return_value = mock_playwright
    mock_playwright.__enter__.return_value = mock_playwright
    mock_playwright.__exit__.return_value = None

    return mock_pw, mock_playwright, mock_page, mock_context, mock_browser


class TestSubstituteTemplate:
    TEMPLATE_CONTENT = (
        "<html><head><title>{{BRAND_NAME}}</title></head>"
        "<body><h1>{{BRAND_NAME}} — {{TAGLINE}}</h1>"
        "<div style='background: {{PRIMARY_COLOR}};'></div>"
        "<ul>{{VOICE_DOS}}</ul><ul>{{VOICE_DONTS}}</ul></body></html>"
    )

    def test_substitutes_simple_variables(self):
        variables = {
            "BRAND_NAME": "Test Co",
            "TAGLINE": "Best coffee",
            "PRIMARY_COLOR": "oklch(50% 0.2 30)",
            "VOICE_DOS": ["Be kind", "Be honest"],
            "VOICE_DONTS": ["Don't lie", "Don't shout"],
        }
        result = _substitute_template(self.TEMPLATE_CONTENT, variables)
        assert "Test Co" in result
        assert "Best coffee" in result
        assert "oklch(50% 0.2 30)" in result
        assert "{{BRAND_NAME}}" not in result
        assert "{{TAGLINE}}" not in result
        assert "{{PRIMARY_COLOR}}" not in result

    def test_removes_all_placeholders(self):
        variables = {
            "BRAND_NAME": "X",
            "TAGLINE": "Y",
            "PRIMARY_COLOR": "red",
            "VOICE_DOS": [],
            "VOICE_DONTS": [],
        }
        result = _substitute_template(self.TEMPLATE_CONTENT, variables)
        assert "{{" not in result
        assert "}}" not in result

    def test_list_values_rendered_as_html_li(self):
        variables = {
            "BRAND_NAME": "Test",
            "TAGLINE": "Tag",
            "PRIMARY_COLOR": "red",
            "VOICE_DOS": ["Do thing A", "Do thing B"],
            "VOICE_DONTS": ["Don't thing C"],
        }
        result = _substitute_template(self.TEMPLATE_CONTENT, variables)
        assert "<li>Do thing A</li>" in result
        assert "<li>Do thing B</li>" in result
        assert "<li>Don't thing C</li>" in result

    def test_empty_list_produces_empty_string(self):
        variables = {
            "BRAND_NAME": "Test",
            "TAGLINE": "Tag",
            "PRIMARY_COLOR": "red",
            "VOICE_DOS": [],
            "VOICE_DONTS": [],
        }
        result = _substitute_template(self.TEMPLATE_CONTENT, variables)
        assert "<li>" not in result


class TestRenderPdf:
    def test_missing_template_file_raises_file_not_found(self):
        with tempfile.NamedTemporaryFile(suffix=".pdf") as tmp:
            with mock.patch("forge.src.render.sync_playwright"):
                import pytest

                with pytest.raises(FileNotFoundError):
                    render_pdf("/nonexistent/template.html", {}, tmp.name)

    def test_substitutes_variables_in_html_before_pdf_render(self):
        content = "<html><body><h1>{{TITLE}}</h1></body></html>"
        with tempfile.NamedTemporaryFile(
            suffix=".html", mode="w", delete=False
        ) as tmpl:
            tmpl.write(content)
            tmpl_path = tmpl.name

        try:
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as out:
                output_path = out.name

            mock_pw, mock_playwright, mock_page, mock_context, mock_browser = (
                _make_mock_pw_chain()
            )
            mock_pw.return_value = mock_playwright

            with mock.patch("forge.src.render.sync_playwright", mock_pw):
                render_pdf(tmpl_path, {"TITLE": "Hello World"}, output_path)

            mock_page.set_content.assert_called_once()
            called_html = mock_page.set_content.call_args[0][0]
            assert "Hello World" in called_html
            assert "{{TITLE}}" not in called_html

            mock_page.pdf.assert_called_once()
            call_kwargs = mock_page.pdf.call_args.kwargs
            assert call_kwargs["format"] == "A4"
            assert call_kwargs["print_background"] is True

            os.unlink(output_path)
        finally:
            os.unlink(tmpl_path)

    def test_multiple_variable_substitution(self):
        content = "<html><body>{{BRAND_NAME}} | {{PRIMARY_COLOR}}</body></html>"
        with tempfile.NamedTemporaryFile(
            suffix=".html", mode="w", delete=False
        ) as tmpl:
            tmpl.write(content)
            tmpl_path = tmpl.name

        try:
            with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as out:
                output_path = out.name

            mock_pw, mock_playwright, mock_page, _, _ = _make_mock_pw_chain()
            mock_pw.return_value = mock_playwright

            with mock.patch("forge.src.render.sync_playwright", mock_pw):
                render_pdf(
                    tmpl_path,
                    {"BRAND_NAME": "Acme", "PRIMARY_COLOR": "oklch(50% 0.2 30)"},
                    output_path,
                )

            called_html = mock_page.set_content.call_args[0][0]
            assert "Acme" in called_html
            assert "oklch(50% 0.2 30)" in called_html
            assert "{{BRAND_NAME}}" not in called_html

            os.unlink(output_path)
        finally:
            os.unlink(tmpl_path)


class TestRenderPng:
    def test_uses_correct_viewport_dimensions(self):
        content = "<html><body>test</body></html>"
        with tempfile.NamedTemporaryFile(
            suffix=".html", mode="w", delete=False
        ) as tmpl:
            tmpl.write(content)
            tmpl_path = tmpl.name

        try:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as out:
                output_path = out.name

            mock_pw, mock_playwright, mock_page, _, _ = _make_mock_pw_chain()
            mock_pw.return_value = mock_playwright

            with mock.patch("forge.src.render.sync_playwright", mock_pw):
                render_png(tmpl_path, {}, output_path, width=1200, height=630)

            mock_page.set_viewport_size.assert_called_once_with(
                {"width": 1200, "height": 630}
            )
            mock_page.screenshot.assert_called_once_with(
                path=output_path,
                full_page=False,
                clip={"x": 0, "y": 0, "width": 1200, "height": 630},
            )

            os.unlink(output_path)
        finally:
            os.unlink(tmpl_path)

    def test_default_dimensions_are_1080(self):
        content = "<html><body>test</body></html>"
        with tempfile.NamedTemporaryFile(
            suffix=".html", mode="w", delete=False
        ) as tmpl:
            tmpl.write(content)
            tmpl_path = tmpl.name

        try:
            with tempfile.NamedTemporaryFile(suffix=".png", delete=False) as out:
                output_path = out.name

            mock_pw, mock_playwright, mock_page, _, _ = _make_mock_pw_chain()
            mock_pw.return_value = mock_playwright

            with mock.patch("forge.src.render.sync_playwright", mock_pw):
                render_png(tmpl_path, {}, output_path)

            mock_page.set_viewport_size.assert_called_once_with(
                {"width": 1080, "height": 1080}
            )

            os.unlink(output_path)
        finally:
            os.unlink(tmpl_path)
