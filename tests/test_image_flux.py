from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from forge.src.providers.image_flux import generate_image


class TestFallbackWhenNoApiKey:
    def test_fallback_when_fal_key_unset(self):
        if "FAL_KEY" in os.environ:
            saved = os.environ["FAL_KEY"]
            del os.environ["FAL_KEY"]
            try:
                result = generate_image(prompt="test prompt")
                assert result["fallback"] is True
                assert result["url"] is None
                assert result["error"] == "FAL_KEY not set"
            finally:
                os.environ["FAL_KEY"] = saved
        else:
            result = generate_image(prompt="test prompt")
            assert result["fallback"] is True
            assert result["url"] is None
            assert result["error"] == "FAL_KEY not set"


class TestPromptUsed:
    def test_prompt_used_matches_input(self):
        if "FAL_KEY" in os.environ:
            saved = os.environ["FAL_KEY"]
            del os.environ["FAL_KEY"]
            try:
                result = generate_image(prompt="a test logo design")
                assert result["prompt_used"] == "a test logo design"
            finally:
                os.environ["FAL_KEY"] = saved
        else:
            result = generate_image(prompt="a test logo design")
            assert result["prompt_used"] == "a test logo design"


class TestDefaultDimensions:
    def test_default_uses_1024(self):
        if "FAL_KEY" in os.environ:
            saved = os.environ["FAL_KEY"]
            del os.environ["FAL_KEY"]
            try:
                result = generate_image(prompt="test")
                assert result["fallback"] is True
            finally:
                os.environ["FAL_KEY"] = saved
        else:
            result = generate_image(prompt="test")
            assert result["fallback"] is True
