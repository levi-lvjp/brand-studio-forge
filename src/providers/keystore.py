from __future__ import annotations

import json
import os

DEFAULT_PATH = os.path.expanduser("~/.forge/keys.json")

ENV_MAP = {
    "gemini": "GEMINI_API_KEY",
    "chatgpt": "OPENAI_API_KEY",
}


class KeyStore:
    def __init__(self, path: str = DEFAULT_PATH) -> None:
        self._path = path
        self._keys: dict[str, str] = {}
        self._load()

    def _load(self) -> None:
        if os.path.exists(self._path):
            with open(self._path) as f:
                self._keys = json.load(f)
        for provider, key in self._keys.items():
            env_var = ENV_MAP.get(provider)
            if env_var and key:
                os.environ[env_var] = key

    def get(self, provider: str) -> str | None:
        return self._keys.get(provider)

    def set(self, provider: str, key: str) -> None:
        self._keys[provider] = key
        env_var = ENV_MAP.get(provider)
        if env_var:
            os.environ[env_var] = key

    def save(self) -> None:
        os.makedirs(os.path.dirname(self._path), exist_ok=True)
        with open(self._path, "w") as f:
            json.dump(self._keys, f, indent=2)
        os.chmod(self._path, 0o600)

    def has_any_provider(self) -> bool:
        return any(bool(v) for v in self._keys.values())

    def available_providers(self) -> list[str]:
        return [k for k, v in self._keys.items() if v]
