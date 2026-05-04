from __future__ import annotations

import os
import sys
from unittest import mock

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from forge.src.providers.base import ImageResult
from forge.src.providers.image_gemini import GeminiProvider
from forge.src.providers.image_openai import OpenAIProvider
from forge.src.providers.registry import get_provider, available_providers


class TestGeminiProviderFallback:
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_is_available_false_when_no_key(self):
        provider = GeminiProvider()
        assert provider.is_available() is False

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_generate_returns_fallback_when_no_key(self):
        provider = GeminiProvider()
        result = provider.generate(prompt="test prompt")
        assert result["fallback"] is True
        assert result["url"] is None
        assert result["image_bytes"] is None
        assert result["prompt_used"] == "test prompt"
        assert result["error"] == "GEMINI_API_KEY not set"


class TestOpenAIProviderFallback:
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_is_available_false_when_no_key(self):
        provider = OpenAIProvider()
        assert provider.is_available() is False

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_generate_returns_fallback_when_no_key(self):
        provider = OpenAIProvider()
        result = provider.generate(prompt="test prompt")
        assert result["fallback"] is True
        assert result["url"] is None
        assert result["prompt_used"] == "test prompt"
        assert result["error"] == "OPENAI_API_KEY not set"


class TestProviderImageResultShape:
    def _assert_valid_imageresult(self, result: ImageResult, expected_prompt: str):
        assert isinstance(result, dict)
        assert "url" in result
        assert "image_bytes" in result
        assert "prompt_used" in result
        assert "fallback" in result
        assert "error" in result
        assert result["prompt_used"] == expected_prompt

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_gemini_returns_correct_shape(self):
        provider = GeminiProvider()
        result = provider.generate(prompt="gemini test")
        self._assert_valid_imageresult(result, "gemini test")

    @mock.patch.dict(os.environ, {}, clear=True)
    def test_openai_returns_correct_shape(self):
        provider = OpenAIProvider()
        result = provider.generate(prompt="openai test")
        self._assert_valid_imageresult(result, "openai test")


class TestRegistryGetProvider:
    def test_returns_gemini_provider(self):
        provider = get_provider("gemini")
        assert isinstance(provider, GeminiProvider)
        assert provider.name == "gemini"

    def test_returns_openai_provider(self):
        provider = get_provider("chatgpt")
        assert isinstance(provider, OpenAIProvider)
        assert provider.name == "chatgpt"

    def test_raises_value_error_for_unknown(self):
        try:
            get_provider("nonexistent")
            assert False, "Expected ValueError"
        except ValueError as e:
            assert "Unknown provider" in str(e)


class TestRegistryAvailableProviders:
    @mock.patch.dict(os.environ, {}, clear=True)
    def test_returns_empty_list_when_no_env_vars(self):
        providers = available_providers()
        assert providers == []
