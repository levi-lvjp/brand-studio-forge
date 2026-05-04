# Brand Studio Forge — Architecture

## Design Source

Architecture for the brand identity domain.

---

## Skill Architecture

### YAML Frontmatter (SKILL.md)

```yaml
---
name: brand-studio-forge
description: Use when the user wants to create, refine, or evolve a brand identity. Covers brand interviews, identity kit generation (logo, color, type, voice, guidelines), brand-specific content skills, and ongoing content via cron. Not for UI design or non-brand creative tasks.
version: 1.0.0
license: MIT
allowed-tools:
  - Bash(python3 forge/scripts/*.py *)
  - Bash(bash forge/scripts/setup.sh)
---
```

### Setup Gates

Before any creative output, the agent must resolve all gates:

| Gate | Required Check | If Fail |
|---|---|---|
| Context | BrandProfile JSON exists and was loaded by loader script | Run `/forge_interview` first, then resume |
| Brand | PRODUCT.md exists with personality words, positioning, anti-references | Run `/forge_interview`, refresh context, then resume |
| Mode | One of: identity / content / evolve is selected based on task cue | Identify mode before continuing |
| Image | Required visual probes generated or skipped with reason | Resolve in `forge_forge` step before code |
| Mutation | All active gates above pass | Do not edit project files yet |

**PREFLIGHT assertion (Codex-compatible):**
```
FORGE_PREFLIGHT: context=pass brand=pass mode=identity|content|evolve image_gate=pass|skipped:<reason> mutation=open
```

### Mode System

Brand Studio Forge has three modes:

| Mode | When | Behavioral Difference |
|---|---|---|
| **identity** | Creating a brand identity kit from scratch | Generates full identity: color, type, voice, logo, guidelines. Loads: color-theory.md, typography-voice.md, voice.md, logo-and-mark.md, identity-system.md |
| **content** | Generating ongoing branded content | Uses existing BrandProfile to produce social posts, email copy, blog intros. Loads: voice.md, tone-and-copy.md, mood-vocabulary.md |
| **evolve** | Refining or evolving an existing identity | Audit + incremental changes. Loads: identity-system.md, anti-slop.md, touchpoints.md |

Mode is inferred from:
1. Task cue in the request ("create a brand" → identity, "write a post" → content, "make this bolder" → evolve)
2. State of BrandProfile (incomplete → identity, complete → content/evolve)
3. Explicit user declaration

---

## Command Router

| Command | Category | Description | Reference |
|---|---|---|---|
| `forge_interview` | Create | Discover a brand through multi-round questioning | references/interview.md |
| `forge_forge` | Create | Generate identity kit from brand profile | references/process.md |
| `forge_name` | Create | Brand naming and tagline generation | references/naming.md |
| `forge_evolve` | Create | Refine an existing identity kit | references/identity-system.md |
| `forge_author` | Create | Write brand-specific .py skill to disk | references/skill-authoring.md |
| `forge_critique` | Evaluate | Brand identity review with heuristic scoring | references/anti-slop.md |
| `forge_audit` | Evaluate | Check identity kit completeness and consistency | references/identity-system.md |
| `forge_polish` | Refine | Final quality pass on brand collateral | references/grid-and-layout.md |
| `forge_content` | Generate | Generate brand-voice social/marketing content | references/tone-and-copy.md |
| `forge_schedule` | Generate | Set up NL cron for brand content | references/process.md |

All commands use `forge_<subcommand>` underscore-delimited format for Telegram bot compatibility. Spaces are not supported in Telegram slash commands. Only the underscore-delimited format is valid for routing; bare subcommand names are never matched to avoid collisions with other skills.

### Routing rules

1. **No argument** — render command menu, ask what they want
2. **Input starts with `forge_`** — strip prefix, extract subcommand, load reference, follow instructions
3. **No match** — general invocation with shared design laws + loaded mode reference

---

## Shared Design Laws

Apply to every brand identity the skill generates.

### Color

- Use OKLCH. Reduce chroma as lightness approaches 0 or 100.
- Never use `#000` or `#fff`. Tint every neutral toward the brand hue.
- Pick a **color strategy** before picking colors. Four steps on the commitment axis:
  - **Restrained** — tinted neutrals + one accent ≤10%. Corporate, professional services.
  - **Committed** — one saturated color carries 30–60% of the surface. Most consumer brands.
  - **Full palette** — 3–4 named roles, each used deliberately. Fashion, lifestyle, food.
  - **Drenched** — the surface IS the color. Entertainment, youth, disruptive brands.
- Category-aware: never pick the same primary color as the brand's top 3 competitors.

### Typography

- Font selection follows the 4-step procedure:
  1. Write three concrete brand-voice words (physical-object words, not "modern" or "elegant")
  2. List the three fonts you'd reach for by reflex. If any are on the reflex-reject list, reject them.
  3. Browse a real catalog with the three words in mind. Find the font as a physical object.
  4. Cross-check. If the final pick lines up with the original reflex, start over.

### Reflex-Reject Font List

Training-data defaults. The AI must look further:

Fraunces · Newsreader · Lora · Crimson · Crimson Pro · Playfair Display · Cormorant · Cormorant Garamond · Syne · IBM Plex Mono · IBM Plex Sans · Space Mono · Space Grotesk · Inter · DM Sans · DM Serif Display · Outfit · Plus Jakarta Sans · Instrument Sans · Instrument Serif

### Reflex-Reject Aesthetic Lanes

Saturated brand identity families that AI defaults to:

- **Tech-minimal blue.** Blue primary, white background, Inter/DM Sans, rounded corners, gradient accents. Every SaaS startup since 2019.
- **Editorial-magazine.** Display serif italic + small mono labels + ruled separators + monochromatic restraint. Every Notion-adjacent brand since 2024.
- **DTC pastel.** Soft pinks, lavender, mint, rounded everything, script accents. Every DTC brand since Glossier.

### Voice

- Brand voice is constant. Tone shifts by context. Style is execution.
- Every generated piece of copy must pass the voice-consistency check: if you removed the brand name, could you still tell which brand this belongs to?
- No "elevate", "empower", "seamless", "leverage", "innovative", "cutting-edge" — these are AI-branding tells.

### Absolute Bans

Match-and-refuse:

- **Side-stripe borders** — `border-left/right` > 1px as colored accent
- **Gradient text** — `background-clip: text` with gradient
- **Glassmorphism as default** — blurs and glass cards used decoratively
- **The hero-metric template** — big number, small label, gradient accent
- **Identical card grids** — same-sized cards repeated endlessly
- **Purple-blue gradients** — the single most common AI brand cliché
- **"Empower" and family** — elevate, seamless, leverage, innovative, cutting-edge, transform, unlock

### The AI Slop Test (brand-specific)

If someone could look at this brand identity and say "AI made that" without doubt, it's failed.

**First-order check:** If someone could guess the color palette from the industry alone — "fintech → navy + gold", "wellness → sage + cream", "tech startup → blue + white" — it's the training-data reflex. Rework until the answer isn't obvious from the category.

**Second-order check:** If someone could guess the aesthetic family from category-plus-anti-references — "coffee brand that's not brown → editorial-typographic cream", "SaaS that's not blue → terminal-dark mono" — it's the trap one tier deeper. Rework until both answers are not obvious.

---

## Module Architecture

```
forge/
├── SKILL.md                          # Hermes skill definition (command router + design laws)
├── PRODUCT.md                        # Brand brief (filled by forge_interview command)
├── DESIGN.md                          # Design token system (filled by forge_forge command)
├── references/                        # 15 domain reference .md files
│   ├── process.md                     # Brand identity process
│   ├── strategy.md                    # Strategy + positioning
│   ├── interview.md                   # Interview methodology
│   ├── naming.md                      # Naming principles
│   ├── voice.md                       # Voice development
│   ├── tone-and-copy.md              # Tone + copywriting guidelines
│   ├── color-theory.md               # Brand color strategy (OKLCH)
│   ├── typography-voice.md           # Typography as brand voice
│   ├── logo-and-mark.md             # Logo design principles
│   ├── identity-system.md           # What a complete kit contains
│   ├── touchpoints.md              # Brand across surfaces
│   ├── grid-and-layout.md          # Grid systems for collateral
│   ├── anti-slop.md                # AI brand clichés to avoid
│   ├── mood-vocabulary.md          # Mood → palette/type/voice mapping
│   └── skill-authoring.md         # How to write .py skill from profile
├── scripts/                          # CLI entry points
│   ├── interview.py                  # Brand interview chatbot
│   ├── run_forge.py                 # Generate identity kit
│   ├── content.py                   # Generate branded content
│   ├── deliver.py                   # Telegram delivery
│   ├── recall.py                    # FTS5 memory search
│   ├── schedule.py                  # NL cron setup
│   └── setup.sh                    # Dependency checker
├── src/                              # Python engine
│   ├── brand_profile.py             # BrandProfile data model
│   ├── color.py                     # OKLCH palette generation
│   ├── typography.py                # Font pairing + voice
│   ├── voice.py                     # Copy voice/tone
│   ├── logo.py                      # Logo prompt generation
│   ├── identity_kit.py             # Identity kit orchestration
│   ├── render.py                    # HTML→PDF/PNG via Playwright
│   ├── skill_forge.py              # Write .py skill to disk (Beat 5)
│   └── providers/
│       └── image_flux.py            # FLUX via fal.ai
├── assets/
│   └── templates/
│       ├── brand_guidelines.html    # Primary deliverable template
│       ├── business_card.html       # Supporting template
│       ├── social_post.html         # Supporting template
│       └── logo_sheet.html          # Supporting template
└── tests/
    ├── test_brand_profile.py
    ├── test_color.py
    ├── test_typography.py
    ├── test_voice.py
    ├── test_identity_kit.py
    ├── test_render.py
    ├── test_skill_forge.py
    └── test_e2e.py
```

---

## Data Flow

```
USER (Telegram/chat)
  ↓ "I want to create a brand for my coffee roastery"
  ↓
INTERVIEW (scripts/interview.py)
  → Reads: references/interview.md
  → Produces: PRODUCT.md + partial BrandProfile JSON
  ↓
FORGE (scripts/run_forge.py)
  ↓
  delegate_task spawns 4 children:
  ├── Child 1: COLOR (src/color.py)     → reads color-theory.md → partial profile
  ├── Child 2: TYPE (src/typography.py) → reads typography-voice.md → partial profile
  ├── Child 3: VOICE (src/voice.py)     → reads voice.md → partial profile
  └── Child 4: LOGO (src/logo.py)      → reads logo-and-mark.md → logo prompt
  ↓ (merge)
  identity_kit.py → complete BrandProfile JSON
  ↓
  RENDER (src/render.py) → brand_guidelines.pdf + brand card pdf
  ↓
  SKILL FORGE (src/skill_forge.py) → writes brand_<name>_content.py to disk
  ↓
  DELIVER (scripts/deliver.py) → sends PDF + .py via Telegram
  ↓
  SCHEDULE (scripts/schedule.py) → sets cron for weekly content
  ↓
  CONTENT (brand_<name>_content.py) → generates brand-voice posts on schedule
```

---

## 5 Hermes-Only Demo Beats

| Beat | Time | What | Why Hermes-only |
|---|---|---|---|
| 1: Multi-channel ingestion | 0:15–0:25 | User sends mood board + competitor links via Telegram | 17-channel gateway, no platform-specific code |
| 2: Parallel delegate_task | 0:25–0:40 | Terminal split: 4 parallel workers log + write files | Shared filesystem, max_spawn_depth |
| 3: FTS5 recall | 0:40–0:50 | "make it like the coffee brand from last month" → cross-session recall | FTS5 full-text search across sessions |
| 4: NL cron | 0:50–1:00 | "post weekly in our voice" → scheduled content generation | Built-in NL cron + multi-platform delivery |
| 5: Self-evolving skills | 1:00–1:15 | File tree: .py skill APPEARS. Cron fires. Content generates. | Agent writes executable code to disk |

---

## Key Decisions (locked)

1. **Brand Profile = JSON** (data) **+ .py skill** (executable). Both outputs, not one.
2. **OKLCH color system** — no hex for new brand colors.
3. **HTML+Playwright rendering** — HTML/CSS templates rendered to PDF/PNG via Playwright.
4. **Flat-file storage** — BrandProfile as JSON, identity as DESIGN.md, skills as .py. No database.
5. **12-15 reference files** — enough depth without overbuilding.
6. **Hermes + CLI** — skill works in Hermes, scripts work standalone for testing/demo fallback.