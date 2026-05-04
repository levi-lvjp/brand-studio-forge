from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))

from forge.src.brand_profile import BrandProfile
from forge.src.mood import infer_mood

ABSOLUTE_BANNED_WORDS: list[str] = [
    "elevate",
    "empower",
    "seamless",
    "leverage",
    "innovative",
    "cutting-edge",
    "transform",
    "unlock",
]

MOOD_VOICE_TRAITS: dict[str, dict] = {
    "Commanding": {
        "tone": "authoritative, declarative, measured",
        "dos": [
            "Use short declarative sentences",
            "State facts directly without hedging",
            "Address the reader with earned confidence",
            "Let data and precision do the convincing",
            "Use specific numbers over vague claims",
            "Write headings that stand alone as statements",
        ],
        "donts": [
            "Never use exclamation marks",
            "Never begin with 'We believe' — just state the thing",
            "Never use the word 'journey'",
            "Never say 'excited' or 'thrilled'",
            "Never pad a sentence with 'very' or 'really'",
            "Never ask rhetorical questions",
        ],
        "extra_banned": ["excited", "thrilled", "fun", "journey"],
    },
    "Warm": {
        "tone": "warm, artisanal, unhurried",
        "dos": [
            "Address reader as 'you'",
            "Use sensory detail — scent, texture, warmth",
            "Let sentence length vary for rhythm",
            "Use contractions naturally",
            "Write the way a friend explains their craft",
            "Make the customer the subject of most sentences",
        ],
        "donts": [
            "Never say 'innovative'",
            "Never use passive voice",
            "Never stack three adjectives when one precise one works",
            "Never use jargon the customer wouldn't say aloud",
            "Never begin with 'At [Brand], we...'",
            "Never use corporate filler like 'solutions' or 'offerings'",
        ],
        "extra_banned": ["leverage", "optimize", "synergy", "stakeholder"],
    },
    "Precise": {
        "tone": "precise, technical, restrained",
        "dos": [
            "Use active voice exclusively",
            "Lead with specific numbers and measurements",
            "Name the component, material, or method directly",
            "Let clarity carry confidence",
            "Write single-sentence paragraphs for emphasis",
            "Use technical terms accurately and unapologetically",
        ],
        "donts": [
            "Never use superlatives ('best', 'fastest', 'greatest')",
            "Never say 'revolutionary' or 'game-changing'",
            "Never use the word 'magic'",
            "Never promise more than the data supports",
            "Never use vague intensifiers like 'incredibly'",
            "Never describe the product — describe what it enables",
        ],
        "extra_banned": [
            "revolutionary",
            "game-changing",
            "best-in-class",
            "world-class",
        ],
    },
    "Rebellious": {
        "tone": "confrontational, urgent, sharp",
        "dos": [
            "Use fragments for impact",
            "Address the establishment directly by name",
            "Write in imperative mood: 'Do this. Skip that.'",
            "Break one grammar rule per paragraph — intentionally",
            "Let anger or urgency show through word choice",
            "End on a strong, unqualified declarative",
        ],
        "donts": [
            "Never say 'premium' or 'luxury'",
            "Never use the word 'bespoke'",
            "Never soften a confrontation with 'perhaps' or 'maybe'",
            "Never explain the joke",
            "Never write a sentence longer than 20 words",
            "Never use 'we're excited to announce'",
        ],
        "extra_banned": ["premium", "luxury", "curated", "bespoke"],
    },
    "Serene": {
        "tone": "calm, sensory, unhurried",
        "dos": [
            "Let long sentences breathe and flow",
            "Use sensory language — weight, light, texture",
            "Address the reader's sense of well-being",
            "Name specific materials and their qualities",
            "Allow space between statements",
            "Write in a rhythm that readers can exhale to",
        ],
        "donts": [
            "Never say 'disrupt' or 'hack'",
            "Never use the word 'grind'",
            "Never create false urgency",
            "Never use all-caps or exclamation marks",
            "Never write a heading that demands attention — invite it",
            "Never use aggressive action words",
        ],
        "extra_banned": ["disrupt", "hack", "crush", "dominate", "grind"],
    },
    "Playful": {
        "tone": "witty, energetic, conversational",
        "dos": [
            "Use contractions always",
            "Ask the reader questions directly",
            "Reference pop culture when it earns the laugh",
            "Punctuate expressively — em dashes, ellipses",
            "Break the fourth wall: 'we know you noticed'",
            "Vary paragraph length dramatically for rhythm",
        ],
        "donts": [
            "Never say 'solutions' or 'enterprise'",
            "Never use the word 'robust' or 'scalable'",
            "Never explain the joke twice",
            "Never write a punchline without a setup",
            "Never be funny at the reader's expense",
            "Never use 'we're thrilled to share'",
        ],
        "extra_banned": ["solutions", "enterprise", "robust", "scalable"],
    },
    "Heritage": {
        "tone": "editorial, rooted, earnest",
        "dos": [
            "Use the editorial 'we' when appropriate",
            "Reference historical context and lineage",
            "Let sentences carry weight and deliberation",
            "Honor the tradition before inviting the future",
            "Write with the care of a letterpress setting type",
            "Proper nouns deserve full formal treatment",
        ],
        "donts": [
            "Never say 'disrupt' or 'pivot'",
            "Never use startup vocabulary",
            "Never say 'growth hack'",
            "Never describe 200 years of history in one sentence",
            "Never abbreviate what should be spelled out fully",
            "Never sound urgent about things that have waited decades",
        ],
        "extra_banned": ["disrupt", "pivot", "startup", "hustle", "growth hack"],
    },
    "Minimal": {
        "tone": "sharp, essential, quiet",
        "dos": [
            "Write the shortest sentence that works",
            "Remove every word you can remove — then remove one more",
            "Let white space on the page do the breathing",
            "Use one adjective max per noun",
            "State the thing. Full stop.",
            "Earn every word by its specific contribution",
        ],
        "donts": [
            "Never use filler phrases — period",
            "Never say 'passionate' or 'dedicated' or 'committed'",
            "Never stack adverbs",
            "Never say 'it goes without saying' — then don't say it",
            "Never write a paragraph that could be one sentence",
            "Never use 'holistic' or 'excellence'",
        ],
        "extra_banned": [
            "passionate",
            "dedicated",
            "committed",
            "excellence",
            "holistic",
            "it goes without saying",
        ],
    },
    "Raw": {
        "tone": "direct, unpolished, transparent",
        "dos": [
            "Write in first person",
            "Name the tool, the material, the process directly",
            "Leave the construction marks visible",
            "Use technical language unglossed — your reader can handle it",
            "Write like field notes, not press releases",
            "Show your working — what failed, what you learned",
        ],
        "donts": [
            "Never say 'luxury' or 'premium'",
            "Never use the word 'elegant' or 'refined'",
            "Never polish what should stay rough",
            "Never hide a mistake in corporate language",
            "Never use 'curated' when you mean 'picked'",
            "Never pretend the process was smooth if it wasn't",
        ],
        "extra_banned": ["luxury", "premium", "elegant", "refined", "curated"],
    },
    "Lush": {
        "tone": "sensual, immersive, indulgent",
        "dos": [
            "Earn every sensory adjective with specificity",
            "Use second person to address the reader's senses",
            "Let subordinate clauses build texture",
            "Name ingredients, materials, origins specifically",
            "Write with the pace of a slowly poured drink",
            "Allow a sentence to be beautiful for its own sake",
        ],
        "donts": [
            "Never say 'innovative' or 'solutions'",
            "Never use tech jargon",
            "Never use the word 'optimize'",
            "Never rush a description — this is not a spec sheet",
            "Never say 'high-quality' — show what quality means here",
            "Never describe the price before describing the experience",
        ],
        "extra_banned": ["innovative", "solutions", "optimize", "scalable", "leverage"],
    },
}

INDUSTRY_BANNED_WORDS: dict[str, list[str]] = {
    "coffee": ["artisanal", "craft", "hand-crafted"],
    "fintech": ["disrupt", "democratize", "frictionless"],
    "wellness": ["holistic", "wellness journey", "self-care ritual"],
    "technology": ["revolutionary", "game-changer", "next-gen"],
    "legal": ["aggressive", "pit bull", "hard-hitting"],
    "food": ["farm-to-table", "artisanal", "curated"],
    "fashion": ["curated", "curation", "timeless classic"],
    "healthcare": ["patient-centric", "holistic", "integrated"],
}

TAGLINES_BY_INDUSTRY: dict[str, list[str]] = {
    "coffee": [
        "Slow-roasted stories, one cup at a time",
        "Beans with backbone, brewed without rush",
        "Morning happens here, one pour at a time",
        "Real roast, real people, real early mornings",
    ],
    "fintech": [
        "Your money moves. You just move faster.",
        "Numbers that work for people, not the other way.",
        "Finance without the finery.",
        "Where your dollars go to grow.",
    ],
    "wellness": [
        "Feel better. Not different. Better.",
        "Good days start with what you put in.",
        "Rest like you mean it.",
    ],
    "technology": [
        "Code that speaks your language.",
        "Build like you mean it. Ship like you're done.",
        "Tools that stay out of your way.",
    ],
    "food": [
        "Flavors that don't need explaining.",
        "Ingredients first. Recipes second.",
        "Good food remembers where it came from.",
    ],
    "fashion": [
        "Wear what you already are.",
        "Clothes that answer fewer questions.",
    ],
    "healthcare": [
        "Care before cure.",
        "Your health. Your terms. Our science.",
    ],
    "legal": [
        "Clarity in the courtroom.",
        "Law that speaks plain English.",
    ],
}

DEFAULT_TAGLINES = [
    "Made right. Told true.",
    "Built for people who pay attention.",
    "Less talk. More proof.",
    "Something worth noticing.",
]


def _pick_tagline(profile: BrandProfile) -> str:
    industry = profile.industry.lower().strip()
    for key, taglines in TAGLINES_BY_INDUSTRY.items():
        if key in industry:
            idx = hash(profile.name) % len(taglines)
            return taglines[idx]
    idx = hash(profile.name) % len(DEFAULT_TAGLINES)
    return DEFAULT_TAGLINES[idx]


def _voice_description(profile: BrandProfile, mood: str, traits: dict) -> str:
    tone = traits["tone"]
    return (
        f"{profile.name} speaks with a {tone} voice. "
        f"Its language is grounded in {profile.industry} — specific, earned, and "
        f"unmistakably itself. Every sentence carries the weight of its values: "
        f"{', '.join(profile.personality_words[:3])}."
    )


def generate_voice(profile: BrandProfile) -> dict:
    mood = infer_mood(profile)
    traits = MOOD_VOICE_TRAITS.get(mood, MOOD_VOICE_TRAITS["Warm"])

    banned_words = list(ABSOLUTE_BANNED_WORDS)
    for word in traits.get("extra_banned", []):
        if word not in banned_words:
            banned_words.append(word)

    industry_lower = profile.industry.lower().strip()
    for key, words in INDUSTRY_BANNED_WORDS.items():
        if key in industry_lower:
            for w in words:
                if w not in banned_words:
                    banned_words.append(w)

    sample_tagline = _pick_tagline(profile)

    return {
        "tone": traits["tone"],
        "dos": traits["dos"],
        "donts": traits["donts"],
        "sample_tagline": sample_tagline,
        "banned_words": banned_words,
        "voice_description": _voice_description(profile, mood, traits),
        "reasoning": (
            f"Mood archetype '{mood}' derived from personality words "
            f"{profile.personality_words}. Voice traits follow The Constant "
            f"Voice Principle: tone adapts, voice is fixed."
        ),
    }
