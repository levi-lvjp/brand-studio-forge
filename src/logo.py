from __future__ import annotations

import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", ".."))
from forge.src.brand_profile import BrandProfile
from forge.src.color import oklch_to_name

LOGO_STRATEGIES: dict[str, str] = {
    "negative_space": "Counter-form between or within letters/shapes carries a second image — dual reading on second glance",
    "overlapping_geometry": "Two or more simple shapes overlap to create a third emergent form at the intersection",
    "visual_rhythm": "Repeated elements create pattern and movement — repetition suggests energy and system",
    "geometric_substitution": "A letter or element is replaced by a geometric shape that carries meaning",
    "silhouette_extraction": "Reduce a complex object to its most recognizable outline — minimal strokes, maximal recognition",
    "diagonal_cut": "Angled lines or sliced forms suggest motion or energy — implied direction through form",
    "container_badge": "A custom-shaped boundary encloses and unifies mark elements — badge framing for craft authority",
    "symmetrical_construction": "Mirror-image halves create stability, formality, and trust through bilateral symmetry",
    "letterform_ligature": "Two or more letters share a stroke or connect organically — typographic fusion",
    "monogram_integration": "Multiple initials interlocked into a single unified glyph — woven identity",
    "custom_letter_anatomy": "Specific letter features (bowl, ascender, terminal) are modified to carry meaning",
    "object_as_letterform": "A recognizable object stands in for a letter it resembles — silhouette substitution",
    "wordmark_with_action": "The word itself implies action or a verb — typography suggests movement",
    "bespoke_type_design": "Entirely custom letterforms designed for the brand — one-of-a-kind type treatment",
    "dual_imagery": "A single form reads as two different things simultaneously — visual pun or optical illusion",
    "hidden_meaning": "A secondary message or image is embedded but not immediately obvious — discovery on second look",
    "visual_metaphor": "An object symbolizes an abstract brand quality — concrete stands for conceptual",
    "pattern_from_dna": "A repeating pattern is derived from the mark's core geometry — systematic extension",
    "multi_mark_system": "Several variations of the mark serve different contexts — primary, compact, icon, pattern tile",
    "letterform_dissolve": "Letters partially dissolve, fragment, or fade — suggestion over declaration",
    "tension_between_elements": "Two forms pull apart or press together — unresolved spacing creates energy",
    "single_line_continuous": "The entire mark drawn in one unbroken line — flow and economy of gesture",
}

STRATEGY_PERSONALITY_MAP: dict[str, list[str]] = {
    "negative_space": ["clever", "witty", "subtle", "sophisticated", "layered"],
    "overlapping_geometry": [
        "structural",
        "layered",
        "complex",
        "interconnected",
        "precision",
    ],
    "visual_rhythm": ["energetic", "systematic", "dynamic", "patterned", "methodical"],
    "geometric_substitution": ["playful", "clever", "minimal", "bold", "abstract"],
    "silhouette_extraction": [
        "minimal",
        "distinctive",
        "confident",
        "graphic",
        "assertive",
    ],
    "diagonal_cut": ["fast", "progressive", "dynamic", "sharp", "forward"],
    "container_badge": [
        "heritage",
        "craft",
        "authoritative",
        "established",
        "traditional",
    ],
    "symmetrical_construction": [
        "stable",
        "trustworthy",
        "balanced",
        "formal",
        "reliable",
    ],
    "letterform_ligature": ["crafted", "bespoke", "artisanal", "connected", "flowing"],
    "monogram_integration": [
        "concise",
        "prestigious",
        "institutional",
        "established",
        "formal",
    ],
    "custom_letter_anatomy": ["detailed", "bespoke", "unique", "precise", "expressive"],
    "object_as_letterform": ["playful", "literal", "direct", "memorable", "whimsical"],
    "wordmark_with_action": ["active", "bold", "kinetic", "verb-driven", "energetic"],
    "bespoke_type_design": [
        "one-of-a-kind",
        "artisanal",
        "craft",
        "distinctive",
        "expressive",
    ],
    "dual_imagery": ["clever", "witty", "intellectual", "surprising", "layered"],
    "hidden_meaning": [
        "mysterious",
        "intellectual",
        "nuanced",
        "discovery",
        "quietly_clever",
    ],
    "visual_metaphor": ["poetic", "abstract", "conceptual", "artistic", "evocative"],
    "pattern_from_dna": [
        "systematic",
        "complete",
        "versatile",
        "rhythmic",
        "methodical",
    ],
    "multi_mark_system": [
        "versatile",
        "thorough",
        "adaptive",
        "systematic",
        "complete",
    ],
    "letterform_dissolve": [
        "atmospheric",
        "mysterious",
        "poetic",
        "subtle",
        "ethereal",
    ],
    "tension_between_elements": [
        "tense",
        "edgy",
        "confrontational",
        "bold",
        "unresolved",
    ],
    "single_line_continuous": ["fluid", "graceful", "effortless", "flowing", "organic"],
}

LOGO_TYPE_PERSONALITY_MAP: dict[str, list[str]] = {
    "wordmark": ["bold", "confident", "distinctive"],
    "lettermark": ["formal", "institutional", "prestigious"],
    "pictorial": ["approachable", "literal", "memorable"],
    "abstract": ["innovative", "unique", "conceptual"],
    "emblem": ["heritage", "authoritative", "traditional"],
    "combination": ["balanced", "versatile", "comprehensive"],
    "dynamic": ["playful", "adaptable", "digital-native"],
    "signature": ["personal", "artisanal", "intimate"],
}

INDUSTRY_ANTI_CLICHES: dict[str, str] = {
    "coffee": "No coffee cups, coffee beans, steam wisps, or mugs. Find the ritual, not the object.",
    "dental": "No teeth, toothbrushes, or molar shapes. Find care, not anatomy.",
    "technology": "No circuit boards, network nodes, gears, or code brackets. Find the human outcome.",
    "fintech": "No dollar signs, upward arrows, graphs, or coins. Find the transaction moment.",
    "healthcare": "No crosses, hearts, stethoscopes, or pulse lines. Find the relief point.",
    "fitness": "No dumbbells, running figures, or biceps. Find the transformation moment.",
    "real_estate": "No houses, roofs, keys, or buildings. Find the threshold — arrival or leaving.",
    "food": "No forks, spoons, plates, or chef hats. Find the ingredient or the shared table.",
    "travel": "No globes, airplanes, compasses, or suitcases. Find the unfamiliar moment.",
    "education": "No books, graduation caps, lightbulbs, or owls. Find the question being asked.",
    "music": "No notes, clefs, headphones, or microphones. Find a specific sound moment.",
    "fashion": "No hangers, needles, thread spools, or dress forms. Find the garment's character.",
    "sustainability": "No leaves, sprouts, globes, or recycling arrows. Find the specific material or practice.",
}

ANTI_SLOP_TERMS: list[str] = [
    "clipart",
    "generic icons",
    "glossy 3D",
    "purple-blue gradients",
    "stock imagery",
    "generic industry symbols",
    "over-detailed illustration",
    "trendy geometric low-poly",
    "gradient-dependent",
    "swoosh",
    "generic globe",
    "letter inside a circle",
]

_MOOD_COLOR_MAP: dict[str, dict[str, str]] = {
    "Warm": {"hue": "40-60 amber/terracotta", "surface": "warm paper, natural fiber"},
    "Precise": {"hue": "220-240 cool slate", "surface": "clean white, studio-lit"},
    "Rebellious": {
        "hue": "80-130 acid, 330-360 magenta",
        "surface": "raw concrete, newsprint",
    },
    "Serene": {"hue": "180-220 cool blue/sage", "surface": "watercolor wash, linen"},
    "Playful": {
        "hue": "multi-hue separation 60°+",
        "surface": "flat bold, sticker aesthetic",
    },
    "Commanding": {
        "hue": "anchored single dominant",
        "surface": "matte dense, solid fields",
    },
    "Heritage": {
        "hue": "20-60 oxblood/forest/navy",
        "surface": "leather, embossed, foil",
    },
    "Minimal": {"hue": "near-achromatic", "surface": "flat, no texture"},
    "Raw": {
        "hue": "paper white + black",
        "surface": "exposed materials, process shots",
    },
    "Lush": {
        "hue": "jewel tones 0-20/140-170/260-340",
        "surface": "velvet, lacquer, gloss",
    },
}


def _best_strategy_match(personality_words: list[str]) -> str:
    scores: dict[str, int] = {}
    for strategy, traits in STRATEGY_PERSONALITY_MAP.items():
        scores[strategy] = sum(
            1
            for pw in personality_words
            for t in traits
            if pw.lower() in t.lower() or t.lower() in pw.lower()
        )
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "negative_space"
    return best


def _best_logo_type(personality_words: list[str]) -> str:
    scores: dict[str, int] = {}
    for ltype, traits in LOGO_TYPE_PERSONALITY_MAP.items():
        scores[ltype] = sum(
            1
            for pw in personality_words
            for t in traits
            if pw.lower() in t.lower() or t.lower() in pw.lower()
        )
    best = max(scores, key=scores.get)
    if scores[best] == 0:
        return "combination"
    return best


def _format_colors(profile: BrandProfile) -> str:
    parts: list[str] = []
    if profile.primary_color:
        parts.append(f"primary color {oklch_to_name(profile.primary_color)}")
    if profile.secondary_color:
        parts.append(f"secondary color {oklch_to_name(profile.secondary_color)}")
    return ", ".join(parts) if parts else ""


def _get_mood_context(profile: BrandProfile) -> str:
    mood = getattr(profile, "mood", None)
    if not mood or mood not in _MOOD_COLOR_MAP:
        return ""
    cfg = _MOOD_COLOR_MAP[mood]
    return (
        f" — mood is {mood}: hue range {cfg['hue']}, surface quality {cfg['surface']}"
    )


def _get_anti_cliche(profile: BrandProfile) -> str:
    industry_lower = profile.industry.lower()
    for key, guidance in INDUSTRY_ANTI_CLICHES.items():
        if key in industry_lower:
            return f" CRITICAL: {guidance}"
    return ""


def _build_primary_prompt(
    profile: BrandProfile,
    logo_type: str,
    strategy: str,
    strategy_desc: str,
    anti_cliche: str,
    mood_ctx: str,
) -> str:
    colors = _format_colors(profile)
    mood = getattr(profile, "mood", None) or "Warm"
    mood_surface = _MOOD_COLOR_MAP.get(mood, {}).get("surface", "clean matte")
    personality = ", ".join(profile.personality_words[:3])
    avoid = ", ".join(ANTI_SLOP_TERMS[:6])

    prompt = (
        f"Logo for '{profile.name}'. {logo_type} mark. "
        f"Visual feel: {personality}. "
        f"The form uses {strategy_desc}. "
        f"{f'Colors: {colors}. ' if colors else ''}"
        f"Surface quality: {mood_surface}. "
        f"Flat vector, solid shapes, no gradients, high contrast, centered on white background. "
        f"Avoid: {avoid}.{anti_cliche}"
    )
    return prompt


def _build_icon_prompt(profile: BrandProfile, logo_type: str, anti_cliche: str) -> str:
    colors = _format_colors(profile)
    personality = ", ".join(profile.personality_words[:3])
    avoid = ", ".join(ANTI_SLOP_TERMS[:6])

    prompt = (
        f"Minimal icon mark for '{profile.name}'. "
        f"Single symbol, no text, no letters. "
        f"Visual feel: {personality}. "
        f"{f'Colors: {colors}. ' if colors else ''}"
        f"Bold geometric silhouette, works at 32px. "
        f"Flat vector on white background, no gradients, no shadows. "
        f"Avoid: {avoid}.{anti_cliche}"
    )
    return prompt


def _build_monochrome_prompt(
    profile: BrandProfile, logo_type: str, anti_cliche: str
) -> str:
    personality = ", ".join(profile.personality_words[:3])
    avoid = ", ".join(ANTI_SLOP_TERMS[:6])

    prompt = (
        f"Monochrome logo for '{profile.name}'. "
        f"Pure black on white. Single weight, no gradients, no gray tones. "
        f"Visual feel: {personality}. "
        f"Strong silhouette that reads at stamp size. "
        f"Flat vector, centered on white background. "
        f"Avoid: {avoid}.{anti_cliche}"
    )
    return prompt


def _build_negative_prompt() -> str:
    return ", ".join(ANTI_SLOP_TERMS)


def _build_reasoning(profile: BrandProfile, logo_type: str, strategy: str) -> str:
    return (
        f"For a {profile.industry} brand with personality words '{', '.join(profile.personality_words)}', "
        f"the {logo_type} approach best fits its positioning, "
        f"using a {strategy} strategy to create a mark that avoids industry clichés "
        f"while communicating the brand's core character."
    )


def generate_logo_prompts(profile: BrandProfile) -> dict:
    strategy = _best_strategy_match(profile.personality_words)
    strategy_desc = LOGO_STRATEGIES.get(strategy, "A distinctive visual approach")
    logo_type = _best_logo_type(profile.personality_words)
    anti_cliche = _get_anti_cliche(profile)
    mood_ctx = _get_mood_context(profile)

    return {
        "primary_prompt": _build_primary_prompt(
            profile, logo_type, strategy, strategy_desc, anti_cliche, mood_ctx
        ),
        "icon_prompt": _build_icon_prompt(profile, logo_type, anti_cliche),
        "monochrome_prompt": _build_monochrome_prompt(profile, logo_type, anti_cliche),
        "negative_prompt": _build_negative_prompt(),
        "logo_type": logo_type,
        "strategy": strategy,
        "reasoning": _build_reasoning(profile, logo_type, strategy),
    }
