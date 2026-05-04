---
name: brand-studio-forge
description: Use when the user wants to create, refine, or evolve a brand identity. Covers brand interviews, identity kit generation (logo, color, type, voice, guidelines), brand-specific content skills, and ongoing content via cron. Not for UI design or non-brand creative tasks.
version: 1.0.0
user-invocable: true
argument-hint: "[interview · forge · name · evolve · author | critique · audit | polish | content · schedule] [target]"
license: MIT
allowed-tools:
  - Bash(python3 forge/scripts/*.py *)
  - Bash(bash forge/scripts/setup.sh)
---

Generates and evolves brand identities, then authors brand-specific skills that produce ongoing content.

## Setup (non-optional)

Before any brand design or file edits, pass these gates. Skipping them produces generic output that ignores the brand.

| Gate | Required check | If fail |
|---|---|---|
| Context | BrandProfile JSON exists and was loaded | Run `/forge_interview` or `python3 forge/scripts/interview.py` |
| Brand | PRODUCT.md exists with personality words, positioning, anti-references | Run `/forge_interview`, then resume |
| Mode | One of: identity / content / evolve identified from task cue | Identify mode before continuing |
| Image | API key for at least one image provider exists in `~/.forge/keys.json` | Ask user for Gemini or OpenAI API key via keystore prompt |
| Mutation | All active gates above pass | Do not edit project files yet |

Codex-style agents must state this before editing files:

```text
FORGE_PREFLIGHT: context=pass brand=pass mode=identity|content|evolve image_gate=pass|skipped:<reason> mutation=open
```

### Context gathering

Two files, loaded from the project root under `forge/`.

- **PRODUCT.md** — required. Brand name, industry, personality, positioning, anti-references.
- **DESIGN.md** — optional, strongly recommended. Color tokens, typography, voice rules, logo specifications.

Both are produced by the `forge_interview` and `forge_forge` commands. Load PRODUCT.md directly. DESIGN.md is populated after `forge_forge` generates the identity kit.

```bash
python3 forge/scripts/interview.py
```

If PRODUCT.md is missing: run `/forge_interview`, then resume the user's original task with fresh context.

If DESIGN.md is missing: nudge once per session, then proceed.

### Mode selection

Three modes derived from the brand identity lifecycle. Priority: (1) task cue ("create a brand" → identity, "write a post" → content, "make this bolder" → evolve); (2) BrandProfile state (incomplete → identity, complete → content/evolve); (3) explicit user declaration. First match wins.

| Mode | When | Reference files loaded |
|---|---|---|
| **identity** | Creating brand from scratch | color-theory.md, typography-voice.md, voice.md, logo-and-mark.md, identity-system.md, strategy.md |
| **content** | Generating ongoing branded content | voice.md, tone-and-copy.md, mood-vocabulary.md |
| **evolve** | Refining existing identity | identity-system.md, anti-slop.md, touchpoints.md |

## Shared design laws

Apply to every brand identity the skill generates. Vary across brands. Never converge on the same choices.

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

Font selection follows a 4-step procedure:
1. Write three concrete brand-voice words (physical-object words, not "modern" or "elegant").
2. List the three fonts you'd reach for by reflex. If any are on the reflex-reject list, reject them.
3. Browse a real catalog with the three words in mind. Find the font as a physical object.
4. Cross-check. If the final pick lines up with the original reflex, start over.

Reflex-reject fonts (training-data defaults): Fraunces · Newsreader · Lora · Crimson · Crimson Pro · Playfair Display · Cormorant · Cormorant Garamond · Syne · IBM Plex Mono · IBM Plex Sans · Space Mono · Space Grotesk · Inter · DM Sans · DM Serif Display · Outfit · Plus Jakarta Sans · Instrument Sans · Instrument Serif.

Reflex-reject aesthetic lanes:
- **Tech-minimal blue.** Blue primary, white background, Inter/DM Sans, rounded corners, gradient accents.
- **Editorial-magazine.** Display serif italic + small mono labels + ruled separators + monochromatic restraint.
- **DTC pastel.** Soft pinks, lavender, mint, rounded everything, script accents.

### Voice

- Brand voice is constant. Tone shifts by context. Style is execution.
- Every generated copy must pass the voice-consistency check: remove the brand name — can you still tell which brand this belongs to?
- No "elevate", "empower", "seamless", "leverage", "innovative", "cutting-edge" — these are AI-branding tells.

### Absolute bans

Match-and-refuse. If generated output contains any of these, rewrite.

- **Side-stripe borders.** `border-left/right` > 1px as colored accent.
- **Gradient text.** `background-clip: text` with gradient.
- **Glassmorphism as default.** Blurs and glass cards used decoratively.
- **The hero-metric template.** Big number, small label, gradient accent.
- **Identical card grids.** Same-sized cards repeated endlessly.
- **Purple-blue gradients.** The single most common AI brand cliché.
- **"Empower" word family.** elevate, seamless, leverage, innovative, cutting-edge, transform, unlock.

### The AI slop test

If someone could look at this brand identity and say "AI made that" without doubt, it's failed.

**First-order check:** Can someone guess the color palette from the industry alone? "fintech → navy + gold", "wellness → sage + cream", "tech startup → blue + white" — rework until the answer isn't obvious from the category.

**Second-order check:** Can someone guess the aesthetic family from category-plus-anti-references? "coffee brand that's not brown → editorial-typographic cream", "SaaS that's not blue → terminal-dark mono" — the trap one tier deeper. Rework until both answers are not obvious.

## Commands

All commands use `forge_<subcommand>` format (underscore-delimited) for Telegram bot compatibility. Spaces are not supported in Telegram slash commands.

| Command | Category | Description | Reference |
|---|---|---|---|
| `forge_interview` | Create | Discover brand through multi-round questioning | [references/interview.md](references/interview.md) |
| `forge_forge` | Create | Generate identity kit from brand profile | [references/process.md](references/process.md) |
| `forge_name` | Create | Brand naming and tagline generation | [references/naming.md](references/naming.md) |
| `forge_evolve` | Create | Refine existing identity kit | [references/identity-system.md](references/identity-system.md) |
| `forge_author` | Create | Write brand-specific .py skill to disk | [references/skill-authoring.md](references/skill-authoring.md) |
| `forge_critique` | Evaluate | Brand identity review with heuristic scoring | [references/anti-slop.md](references/anti-slop.md) |
| `forge_audit` | Evaluate | Check identity kit completeness and consistency | [references/identity-system.md](references/identity-system.md) |
| `forge_polish` | Refine | Final quality pass on brand collateral | [references/grid-and-layout.md](references/grid-and-layout.md) |
| `forge_content` | Generate | Generate brand-voice social/marketing content | [references/tone-and-copy.md](references/tone-and-copy.md) |
| `forge_schedule` | Generate | Set up NL cron for brand content | [references/process.md](references/process.md) |

### Routing rules

1. **No argument** — render the table above as the user-facing command menu, grouped by category. Ask what they'd like to do.
2. **Argument starts with `forge_`** — strip the `forge_` prefix, extract the subcommand, and load its reference file. Everything after `forge_<subcommand>` is the target context. Only the underscore-delimited format is valid for routing; bare subcommand names are never matched to avoid collisions with other skills.
3. **No match** — general invocation. Apply the setup steps, shared design laws, and the loaded mode reference, using the full argument as context.

Setup (context gathering, mode selection) is already loaded by then; sub-commands don't re-run the skill.

## Hermes-specific

**delegate_task:** The `forge_forge` command fans out to 4 parallel children via `delegate_task` with `max_spawn_depth=2`. Child 1 loads `color-theory.md` and generates the palette. Child 2 loads `typography-voice.md` and selects fonts. Child 3 loads `voice.md` and defines the voice. Child 4 loads `logo-and-mark.md` and constructs logo prompts. Each child writes partial results to the shared filesystem. The parent merges and validates via `src/identity_kit.py`.

**FTS5 recall:** Cross-session brand memory via `python3 forge/scripts/recall.py --search "<query>"`. Example use: "make it more like the coffee brand from last month" searches FTS5 index, retrieves the previous brand profile as reference.

**NL cron:** Recurring content scheduling via `python3 forge/scripts/schedule.py`. Hermes' built-in scheduler runs the generated `brand_<name>_content.py` skill on the specified cadence. Example: "Post Instagram captions every Tuesday at 9am" registers the cron job.

**Self-evolving skills:** The centerpiece. After `forge_forge` completes an identity kit, `src/skill_forge.py` writes `brand_<name>_content.py` to `~/.hermes/skills/`. This file is a standalone Hermes skill containing baked brand constants, `generate_content()`, `generate_weekly_calendar()`, and `get_brand_info()`. The skill IS the deliverable. File tree shows a new .py appearing live. Next cron run uses that skill to generate authentic brand-voice content.

**API key persistence:** On first `forge_forge` invocation, if no image provider key is found in `~/.forge/keys.json`, the agent MUST ask the user for at least one key (Gemini or OpenAI). Store via `KeyStore.save()`. Keys are reused across sessions — never re-ask if keys already exist. Supported providers: `gemini` (Google Gemini 3.1 Flash Image / Nano Banana 2), `chatgpt` (OpenAI GPT Image 2).
