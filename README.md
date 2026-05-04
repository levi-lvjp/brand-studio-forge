# Brand Studio Forge

A Hermes skill that builds complete brand identities from a conversation — then writes itself to disk as a living content engine.

Give it a name, an industry, and three personality words. It returns a full identity kit: perceptually uniform color palette, curated typography, a defined voice system, AI-generated logo variants, and print-ready PDF guidelines. Then it goes further — it writes a standalone Python skill that generates on-brand content on a schedule, without the original agent.

---

## What it produces

| Deliverable | Format | Description |
|---|---|---|
| Brand Guidelines | PDF | 8-page document with color, type, voice, logo, imagery, and usage rules |
| Logo Sheet | PDF | Primary logo, icon variant, and monochrome variant |
| Business Card | PDF | Front and back, ready for print |
| Social Post | PNG | Branded social media template |
| Brand Profile | JSON | Machine-readable identity tokens |
| Content Skill | `.py` | Self-contained script that generates brand-voice content on cron |

## How it works

```
Interview → Identity Assembly → Render → Skill Forge
```

1. **Interview** — structured brand discovery through multi-round questioning. Produces a BrandProfile with personality words, positioning, anti-references, and mood.

2. **Identity Assembly** — four parallel workers, each loading domain-specific reference documents:
   - **Color** — OKLCH-based palette with chroma decay, competitor dodge, and a 4-level commitment strategy (Restrained → Committed → Full palette → Drenched)
   - **Typography** — font pairing with a reflex-reject filter that blocks 20 overused AI-default fonts
   - **Voice** — tone spectrum, dos/don'ts, and a sample tagline. Every piece of copy passes a voice-consistency check
   - **Logo** — 22 design strategies matched to personality, with industry anti-cliche rules that ban literal symbols (no coffee cups for coffee brands, no teeth for dental)

3. **Render** — HTML templates populated with design tokens, rendered to PDF/PNG via Playwright. Images embedded as base64 data URIs for portable output.

4. **Skill Forge** — writes a standalone `.py` file to `~/.hermes/skills/` containing baked brand constants and content generation functions. This skill runs on cron without the original agent.

## The anti-slop philosophy

Most AI-generated brands look like AI-generated brands. Forge is built to avoid that.

**Reflex-reject system.** The 20 most common AI-default fonts are banned. Three overused aesthetic lanes (tech-minimal blue, editorial-magazine, DTC pastel) are flagged and rejected.

**Two-tier slop test.** First: can someone guess the palette from the industry alone? ("fintech = navy + gold") If yes, rework. Second: can someone guess the aesthetic from the industry + anti-references? ("coffee brand that's not brown = editorial cream") If yes, rework again.

**Absolute bans.** No gradient text, no glassmorphism, no purple-blue gradients, no side-stripe borders, no "empower/elevate/seamless/leverage" copy.

**Industry anti-cliches.** 13 industries mapped to their most tired visual symbols, with instructions to find the underlying concept instead. Coffee: "No coffee cups, coffee beans, steam wisps, or mugs. Find the ritual, not the object."

## Commands

| Command | What it does |
|---|---|
| `forge_interview` | Multi-round brand discovery conversation |
| `forge_forge` | Generate the full identity kit |
| `forge_name` | Brand naming and tagline generation |
| `forge_evolve` | Refine an existing identity |
| `forge_author` | Write a content skill to disk |
| `forge_critique` | Score an identity against heuristics |
| `forge_audit` | Check kit completeness and consistency |
| `forge_polish` | Final quality pass on collateral |
| `forge_content` | Generate brand-voice content |
| `forge_schedule` | Set up recurring content via cron |

## Image generation

Forge generates logos and brand imagery (photography style, illustration style) using AI image providers. Two providers are supported out of the box:

| Provider | Model | Env variable |
|---|---|---|
| Gemini | Gemini 2.0 Flash Preview Image Generation | `GEMINI_API_KEY` |
| OpenAI | GPT Image 2 | `OPENAI_API_KEY` |

API keys are stored persistently in `~/.forge/keys.json` after first use. The skill prompts for a key if none is found.

Raw image prompts are refined through an LLM layer (Gemini 2.5 Flash) that expands brief descriptions into detailed art-direction prompts with composition, lighting, texture, and mood specifics.

## Quick start

```bash
# Install dependencies
bash scripts/setup.sh

# Run the brand interview
python3 scripts/interview.py

# Generate the identity kit
python3 scripts/run_forge.py --profile brand_profile.json
```

### As a Hermes skill

Drop the `forge/` directory into your Hermes skills path. The `SKILL.md` frontmatter handles routing and tool permissions.

```
~/.hermes/skills/brand-studio-forge/
├── SKILL.md
├── src/
├── scripts/
├── assets/
├── references/
└── ...
```

## Project structure

```
forge/
├── SKILL.md                # Hermes skill definition + design laws
├── PRODUCT.md              # Brand brief template
├── DESIGN.md               # Design token template
├── src/                    # Python engine
│   ├── brand_profile.py    # BrandProfile data model
│   ├── color.py            # OKLCH palette generation
│   ├── typography.py       # Font pairing engine
│   ├── voice.py            # Voice and tone system
│   ├── logo.py             # Logo strategy + prompt generation
│   ├── imagery.py          # Brand imagery generation
│   ├── identity_kit.py     # Orchestrator
│   ├── mood.py             # Personality → mood mapping
│   ├── image_gen.py        # Logo image generation
│   ├── render.py           # HTML → PDF/PNG via Playwright
│   ├── skill_forge.py      # Write content skill to disk
│   └── providers/          # Image generation backends
│       ├── image_gemini.py
│       ├── image_openai.py
│       ├── image_custom.py
│       ├── keystore.py
│       └── registry.py
├── scripts/                # CLI entry points
│   ├── run_forge.py
│   ├── interview.py
│   ├── content.py
│   ├── deliver.py
│   ├── recall.py
│   ├── schedule.py
│   └── setup.sh
├── assets/
│   └── templates/          # HTML render templates
│       ├── brand_guidelines.html
│       ├── business_card.html
│       ├── logo_sheet.html
│       └── social_post.html
├── references/             # Domain knowledge (15 files)
│   ├── color-theory.md
│   ├── typography-voice.md
│   ├── voice.md
│   ├── logo-and-mark.md
│   ├── identity-system.md
│   ├── anti-slop.md
│   ├── mood-vocabulary.md
│   └── ...
└── tests/                  # Test suite
```

## Requirements

- Python 3.10+
- Playwright + Chromium (for PDF/PNG rendering)
- Pillow (for image post-processing)
- At least one image provider API key (Gemini or OpenAI)

## License

MIT
