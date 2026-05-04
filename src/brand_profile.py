from __future__ import annotations

import json
from dataclasses import dataclass, field


@dataclass
class BrandProfile:
    name: str
    industry: str
    personality_words: list[str]
    positioning_statement: str = ""
    target_audience: str = ""
    competitors: list[str] = field(default_factory=list)
    anti_references: list[str] = field(default_factory=list)
    color_strategy: str | None = None
    primary_color: str | None = None
    secondary_color: str | None = None
    accent_color: str | None = None
    neutral_tone: str | None = None
    display_font: str | None = None
    body_font: str | None = None
    logo_type: str | None = None
    logo_strategy: str | None = None
    voice_tone: str | None = None
    voice_dos: list[str] | None = None
    voice_donts: list[str] | None = None
    tagline: str | None = None
    mood: str | None = None
    image_provider: str | None = None
    image_provider_config: dict | None = None

    _IDENTITY_FIELDS: tuple[str, ...] = field(
        default=(
            "color_strategy",
            "primary_color",
            "secondary_color",
            "accent_color",
            "neutral_tone",
            "display_font",
            "body_font",
            "logo_type",
            "logo_strategy",
            "voice_tone",
            "voice_dos",
            "voice_donts",
            "tagline",
            "mood",
        ),
        init=False,
        repr=False,
        compare=False,
    )

    def to_json(self) -> dict:
        return {
            "name": self.name,
            "industry": self.industry,
            "personality_words": self.personality_words,
            "positioning_statement": self.positioning_statement,
            "target_audience": self.target_audience,
            "competitors": self.competitors,
            "anti_references": self.anti_references,
            "color_strategy": self.color_strategy,
            "primary_color": self.primary_color,
            "secondary_color": self.secondary_color,
            "accent_color": self.accent_color,
            "neutral_tone": self.neutral_tone,
            "display_font": self.display_font,
            "body_font": self.body_font,
            "logo_type": self.logo_type,
            "logo_strategy": self.logo_strategy,
            "voice_tone": self.voice_tone,
            "voice_dos": self.voice_dos,
            "voice_donts": self.voice_donts,
            "tagline": self.tagline,
            "mood": self.mood,
            "image_provider": self.image_provider,
            "image_provider_config": self.image_provider_config,
        }

    @classmethod
    def from_json(cls, data: dict) -> BrandProfile:
        return cls(
            name=data["name"],
            industry=data["industry"],
            personality_words=data["personality_words"],
            positioning_statement=data["positioning_statement"],
            target_audience=data["target_audience"],
            competitors=data["competitors"],
            anti_references=data["anti_references"],
            color_strategy=data.get("color_strategy"),
            primary_color=data.get("primary_color"),
            secondary_color=data.get("secondary_color"),
            accent_color=data.get("accent_color"),
            neutral_tone=data.get("neutral_tone"),
            display_font=data.get("display_font"),
            body_font=data.get("body_font"),
            logo_type=data.get("logo_type"),
            logo_strategy=data.get("logo_strategy"),
            voice_tone=data.get("voice_tone"),
            voice_dos=data.get("voice_dos"),
            voice_donts=data.get("voice_donts"),
            tagline=data.get("tagline"),
            mood=data.get("mood"),
            image_provider=data.get("image_provider"),
            image_provider_config=data.get("image_provider_config"),
        )

    def save(self, path: str) -> None:
        try:
            with open(path, "w") as f:
                json.dump(self.to_json(), f, indent=2)
        except OSError as exc:
            raise OSError(f"Failed to save brand profile to {path}: {exc}") from exc

    @classmethod
    def load(cls, path: str) -> BrandProfile:
        try:
            with open(path) as f:
                data = json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Brand profile not found: {path}")
        except json.JSONDecodeError as exc:
            raise ValueError(f"Invalid JSON in brand profile {path}: {exc}") from exc
        return cls.from_json(data)

    def is_complete(self) -> bool:
        return all(getattr(self, f) is not None for f in self._IDENTITY_FIELDS)
