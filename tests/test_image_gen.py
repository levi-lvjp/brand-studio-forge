from __future__ import annotations

import base64
import os
import sys
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from forge.src.image_gen import generate_logo_images
from forge.src.providers.base import ImageResult


FAKE_IMAGE_BYTES = b"\x89PNG\r\n\x1a\nfake"


class _FakeFailingProvider:
    name = "fake"
    call_count = 0

    def is_available(self) -> bool:
        return False

    def generate(self, prompt: str, **kwargs) -> ImageResult:
        _FakeFailingProvider.call_count += 1
        return ImageResult(
            url=None,
            image_bytes=None,
            prompt_used=prompt,
            fallback=True,
            error="FAKE_KEY not set",
        )


class _FakeSuccessProvider:
    name = "fake"

    def is_available(self) -> bool:
        return True

    def generate(self, prompt: str, **kwargs) -> ImageResult:
        return ImageResult(
            url=None,
            image_bytes=FAKE_IMAGE_BYTES,
            prompt_used=prompt,
            fallback=False,
            error=None,
        )


class _FakeFlakyProvider:
    name = "fake"

    def is_available(self) -> bool:
        return True

    def generate(self, prompt: str, **kwargs) -> ImageResult:
        if "mono" in prompt.lower():
            return ImageResult(
                url=None,
                image_bytes=None,
                prompt_used=prompt,
                fallback=True,
                error="Simulated failure",
            )
        return ImageResult(
            url=None,
            image_bytes=FAKE_IMAGE_BYTES,
            prompt_used=prompt,
            fallback=False,
            error=None,
        )


class TestGenerateLogoImagesUnavailable:
    @mock.patch("forge.src.image_gen.get_provider")
    def test_returns_none_when_provider_unavailable(self, mock_get_provider):
        mock_get_provider.return_value = _FakeFailingProvider()
        logo_prompts = {
            "primary_prompt": "a logo",
            "icon_prompt": "an icon",
            "monochrome_prompt": "a mono logo",
        }
        result = generate_logo_images(
            logo_prompts=logo_prompts,
            provider_name="fake",
            output_dir="/tmp/test_output",
        )
        assert result is None


class TestGenerateLogoImagesDataUri:
    @mock.patch("forge.src.image_gen.os.makedirs")
    @mock.patch(
        "forge.src.image_gen.os.path.join", side_effect=lambda *args: "/".join(args)
    )
    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch("forge.src.image_gen.get_provider")
    def test_constructs_correct_img_tags(
        self, mock_get_provider, mock_open, mock_join, mock_makedirs
    ):
        mock_get_provider.return_value = _FakeSuccessProvider()

        logo_prompts = {
            "primary_prompt": "a logo",
            "icon_prompt": "an icon",
            "monochrome_prompt": "a mono logo",
            "negative_prompt": "no clipart",
        }
        result = generate_logo_images(
            logo_prompts=logo_prompts,
            provider_name="fake",
            output_dir="/tmp/test_output",
        )

        assert result is not None
        expected_b64 = base64.b64encode(FAKE_IMAGE_BYTES).decode("utf-8")
        for key in ("logo_img_tag", "logo_icon_img_tag", "logo_mono_img_tag"):
            assert key in result
            assert f"data:image/png;base64,{expected_b64}" in result[key]
            assert 'alt="logo"' in result[key]
            assert "max-width:100%;max-height:100%" in result[key]
            assert result[key].startswith("<img ")
            assert result[key].endswith(">")

    @mock.patch("forge.src.image_gen.os.makedirs")
    @mock.patch(
        "forge.src.image_gen.os.path.join", side_effect=lambda *args: "/".join(args)
    )
    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch("forge.src.image_gen.get_provider")
    def test_logo_files_contains_expected_paths(
        self, mock_get_provider, mock_open, mock_join, mock_makedirs
    ):
        mock_get_provider.return_value = _FakeSuccessProvider()

        logo_prompts = {
            "primary_prompt": "a logo",
            "icon_prompt": "an icon",
            "monochrome_prompt": "a mono logo",
        }
        result = generate_logo_images(
            logo_prompts=logo_prompts,
            provider_name="fake",
            output_dir="/tmp/test_output",
        )

        assert result is not None
        assert len(result["logo_files"]) == 3
        assert "/tmp/test_output/logo_primary.png" in result["logo_files"]
        assert "/tmp/test_output/logo_icon.png" in result["logo_files"]
        assert "/tmp/test_output/logo_mono.png" in result["logo_files"]


class TestGenerateLogoImagesPartialFailure:
    @mock.patch("forge.src.image_gen.os.makedirs")
    @mock.patch(
        "forge.src.image_gen.os.path.join", side_effect=lambda *args: "/".join(args)
    )
    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch("forge.src.image_gen.get_provider")
    def test_returns_none_when_one_prompt_fails(
        self, mock_get_provider, mock_open, mock_join, mock_makedirs
    ):
        mock_get_provider.return_value = _FakeFlakyProvider()

        logo_prompts = {
            "primary_prompt": "a logo",
            "icon_prompt": "an icon",
            "monochrome_prompt": "a mono logo",
        }
        result = generate_logo_images(
            logo_prompts=logo_prompts,
            provider_name="fake",
            output_dir="/tmp/test_output",
        )

        assert result is None

    @mock.patch("forge.src.image_gen.os.makedirs")
    @mock.patch(
        "forge.src.image_gen.os.path.join", side_effect=lambda *args: "/".join(args)
    )
    @mock.patch("builtins.open", new_callable=mock.mock_open)
    @mock.patch("forge.src.image_gen.get_provider")
    def test_empty_prompt_is_skipped_gracefully(
        self, mock_get_provider, mock_open, mock_join, mock_makedirs
    ):
        mock_get_provider.return_value = _FakeSuccessProvider()

        logo_prompts = {
            "primary_prompt": "a logo",
            "icon_prompt": "",
            "monochrome_prompt": "a mono logo",
        }
        result = generate_logo_images(
            logo_prompts=logo_prompts,
            provider_name="fake",
            output_dir="/tmp/test_output",
        )

        assert result is not None
        assert "logo_img_tag" in result
        assert result["logo_icon_img_tag"] == ""
        assert "logo_mono_img_tag" in result
        assert len(result["logo_files"]) == 2
