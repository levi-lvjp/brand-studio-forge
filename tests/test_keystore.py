import json
import os
import tempfile

from forge.src.providers.keystore import KeyStore


def test_save_and_load_key(tmp_path):
    store = KeyStore(path=str(tmp_path / "keys.json"))
    store.set("gemini", "test-key-123")
    store.save()

    store2 = KeyStore(path=str(tmp_path / "keys.json"))
    assert store2.get("gemini") == "test-key-123"


def test_get_missing_key_returns_none(tmp_path):
    store = KeyStore(path=str(tmp_path / "keys.json"))
    assert store.get("nonexistent") is None


def test_has_any_provider(tmp_path):
    store = KeyStore(path=str(tmp_path / "keys.json"))
    assert store.has_any_provider() is False
    store.set("chatgpt", "sk-abc")
    assert store.has_any_provider() is True


def test_available_providers(tmp_path):
    store = KeyStore(path=str(tmp_path / "keys.json"))
    store.set("gemini", "key1")
    store.set("chatgpt", "key2")
    assert sorted(store.available_providers()) == ["chatgpt", "gemini"]


def test_set_injects_to_env(tmp_path):
    store = KeyStore(path=str(tmp_path / "keys.json"))
    store.set("gemini", "env-test-key")
    assert os.environ.get("GEMINI_API_KEY") == "env-test-key"
    del os.environ["GEMINI_API_KEY"]
