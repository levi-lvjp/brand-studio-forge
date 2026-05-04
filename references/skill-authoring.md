# Skill Authoring

Technical spec for writing brand-specific `.py` Hermes skills from a BrandProfile JSON. This is the centerpiece of Brand Studio Forge — the agent writes executable code to disk that generates ongoing brand-voice content.

---

## What Gets Written

After `forge` produces a complete BrandProfile JSON and identity kit, the `author` command writes a Python file to `~/.hermes/skills/` (or a specified path). This file is a standalone Hermes skill that:

1. Loads the brand's profile from a known JSON path
2. Generates content (social posts, email subject lines, blog intros) in the brand's voice
3. Renders output via the HTML+Playwright pipeline
4. Delivers via Telegram (or whichever platform the user configured)

The authored skill is not a template with blanks filled in. It is generated code that encodes the brand's specific constraints — color values, font choices, voice rules, banned words — as constants and validation logic.

---

## Named Rules

**Named rule — The Single-Brand Principle:** Each authored `.py` skill serves exactly one brand. A skill that can generate content for multiple brands by swapping a config value has failed. Brand constants are baked, not passed.

**Named rule — The Constant Snapshot Rule:** Bake brand values (colors, type, voice traits, banned words) directly into the skill as Python constants. The JSON is the source of truth for updates; the skill is a snapshot that works even if the JSON moves. See `src/brand_profile.py` for the full schema.

**Named rule — The Self-Contained Delivery Rule:** The authored skill must work with zero additional file reads beyond its own constants and the profile JSON refresh path. Templates are embedded as string constants, fonts are verified at startup, and delivery uses only subprocess calls to Hermes. No external asset dependencies.

**Named rule — The Voice Hard Gate:** Every generated piece of copy must pass `validate_copy()` — banned-word scanning (case-insensitive, including morphological variants), sentence-length enforcement by style, and the Blind Attribution Test from voice.md. If validation fails, re-generate. Never deliver unvalidated copy.

---

## Code Generation Rules

### Constants, Not Config

Bake brand values directly into the skill as Python constants. Do not read from the JSON at generation time — the JSON is the source of truth for updates, but the skill should work even if the JSON is moved. Constants are the snapshot; `load_profile()` is the refresh.

### Voice Enforcement

The `generate_prompt()` function must include:

1. The brand's voice traits as system-level instructions
2. The banned words list as a hard constraint ("never use these words")
3. The sentence style directive
4. Tone context for the specific content type being generated
5. A word-count target appropriate to the content type

The `validate_copy()` function must:

1. Scan for any banned word (case-insensitive, including morphological variants: "empower" catches "empowering," "empowered," "empowerment")
2. Check sentence length against style (short_declarative → flag sentences over 20 words)
3. Return a pass/fail with specific violations listed

### Color in Templates

All color values in generated HTML use OKLCH:

```css
color: oklch(0.45 0.12 250);
background: oklch(0.95 0.02 250);
```

Never convert to hex in the authored skill. The HTML+Playwright pipeline handles OKLCH natively.

### Template Selection

The skill includes 3 HTML template strings for common content types:

| Template | Dimensions | Use |
|---|---|---|
| `social_square` | 1080×1080 | Instagram, Telegram, general social |
| `social_story` | 1080×1920 | Stories, vertical short-form |
| `email_header` | 600×200 | Email hero banner |

Templates are embedded as Python string constants, not read from external files. This keeps the skill self-contained and portable.

### Font Loading

Templates load fonts via Google Fonts `@import` or from local paths. The authored skill must verify font availability at generation time:

```python
def check_fonts():
    """Verify brand fonts are accessible."""
    for font in [TYPOGRAPHY["display"]["family"], TYPOGRAPHY["body"]["family"]]:
        # Check Google Fonts availability or local file existence
        ...
```

If a font is unavailable, the skill falls back to the closest system font and logs a warning. It does not silently substitute.

---

## Bans

Match-and-refuse when authoring skills. If generated code contains any of these, rewrite before writing to disk.

| Ban | Why |
|---|---|
| Hardcoded API keys, tokens, or credentials | Authentication is Hermes' responsibility. The skill never touches secrets. |
| Imports outside stdlib + coloraide + Jinja2 | The skill's dependency surface is deliberately narrow for portability and auditability. |
| `eval()`, `exec()`, or dynamic code generation | The authored file is human-readable Python with zero obfuscation. Generated code that generates code is a security boundary violation. |
| Network calls beyond `hermes send` and font verification | All content generation is local. The skill talks to Hermes for delivery and to font APIs for availability checks — nothing else. |
| File writes outside `~/.hermes/output/brand_{name}/` | Output is sandboxed to a single directory. No scatter. |
| Silent font substitution | If a brand font is unavailable, log a warning and choose the closest system font explicitly. Never swap without telling the user. |
| Leaving a broken `.py` file on disk | If the skill fails import verification, delete it. Either the file works or it doesn't exist. |
| Content generation without `validate_copy()` | Unvalidated copy is untested copy. Every output goes through the voice hard gate. |

---

## Skill Slop Test

If the authored skill could serve any brand by changing the `BRAND_NAME` constant, it failed.

**Check 1 — The Name-Swap Test:** Change `BRAND_NAME` to a different brand in the same industry. Does the skill still produce output that sounds like it belongs to the *original* brand? If so, the voice encoding is generic.

**Check 2 — The Standalone Test:** Copy the skill file to a machine without the original BrandProfile JSON. Run `main(task='weekly_social')`. Does it produce brand-voice output from its baked constants alone? If it crashes, the Constant Snapshot Rule was violated.

**Check 3 — The Dependency Audit:** Count the `import` statements. Are they all stdlib + coloraide + Jinja2? If any other library appears, the dependency surface has crept.

**Check 4 — The Security Scan:** Does the file contain `eval`, `exec`, `__import__`, or any string of API-key length? If yes, the security constraints were violated.

**Check 5 — The Import Verification:** Run `python -c "import brand_{name}_content"`. Exit code 0? If not, the file is broken and must not exist on disk.

---

## Hermes Integration

### Cron and Delivery

After writing the skill, `schedule` registers a NL cron: `"Every Monday at 9am, run brand_{name}_content.py with task='weekly_social' and deliver to Telegram"`. The skill calls Hermes delivery via subprocess (`hermes send --file ...`). See demo beat 5 for the full end-to-end flow.

### Discovery

Hermes discovers skills in `~/.hermes/skills/`. Requirements: filename `brand_{sanitized_name}_content.py`, docstring describing the skill, `main()` entry point, `chmod +x`.

---

## Authoring Process

The `skill_forge.py` module follows this sequence:

1. **Validate** — confirm BrandProfile JSON is complete (all required fields populated)
2. **Sanitize** — convert brand name to a valid Python identifier (`The Roastery` → `the_roastery`)
3. **Extract constants** — pull color, type, voice values from the profile
4. **Generate code** — build the skill source as a string, injecting constants
5. **Write** — save to `~/.hermes/skills/brand_{name}_content.py`
6. **Verify** — run `python -c "import brand_{name}_content"` to confirm the file is syntactically valid
7. **Set permissions** — `chmod +x` the file
8. **Report** — return the file path and a summary of what was authored

### Error Handling

If any step fails:

- Validation failure → return error listing missing fields, do not write
- Syntax error in generated code → log the error, attempt one regeneration pass, then fail with the error exposed
- Write failure (permissions, path) → return error with the attempted path
- Import failure → delete the broken file, return error

Never leave a broken `.py` file on disk. Either the file works or it doesn't exist.

---

## Demo Beat 5 Integration

Centerpiece demo moment: the file tree shows a new `.py` file appearing. The authored skill must work on first run with no manual intervention. For the demo, cron fires on a 30-second interval (not weekly). The user's journey: brand interview → identity kit → executable code → live content arriving in Telegram.

---

## Security Constraints

The authored skill is agent-generated code that runs on the user's machine. All constraints are enforced by the Bans section above. Key principles: no network calls except Hermes delivery + font verification, no writes outside `~/.hermes/output/brand_{name}/`, no credentials, human-readable code with zero obfuscation.
