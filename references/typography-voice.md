# Typography & Voice Reference

The skill's typography pipeline reads this file to avoid training-data defaults.

---

## 4-Step Font Selection Procedure

From ARCHITECTURE.md. Every brand identity follows this sequence.

**Named rule — The Reflex-Reject Rule:** If your first font instinct is on the reflex-reject list, reject it and start the catalog search. These are training-data defaults — the typographic equivalent of clip art. See the list below.

**Named rule — The Physical Object Rule:** Describe the font as a physical object, not an adjective. "Worn leather" not "premium." "Glass tower" not "modern." "Hand-printed zine" not "creative." These words are spatial, textural, material — they point at a typeface's visual weight and rhythm.

**Named rule — The Cross-Check Rule:** If the final pick matches the original reflex from step 2, start over. The point is to escape the gravity well of defaults. If a genuine catalog search lands on a reflex-reject font after honest rejection, that's different — but the reflex must be broken first.

---

## Reflex-Reject Font List

These 20 fonts are training-data defaults. The AI reaches for them because they dominate its training corpus, not because they're right. Each has a reason:

| Font | Why It's a Default |
|---|---|
| **Inter** | Most popular Google Font. The Helvetica of AI output — technically fine, zero personality. |
| **DM Sans** | Google Fonts' second-most-popular geometric sans. Clean, safe, forgettable. |
| **DM Serif Display** | DM Sans's serif companion. AI pairs them reflexively. |
| **Space Grotesk** | "Techy but friendly." Every AI-generated startup brand since 2022. |
| **Space Mono** | Space Grotesk's mono sibling. AI's go-to "developer" font. |
| **IBM Plex Sans** | Open-source, well-made, but AI defaults to it for "professional but not boring." |
| **IBM Plex Mono** | Same gravity as Plex Sans. AI's "terminal aesthetic" reflex. |
| **Plus Jakarta Sans** | Rounded geometric that became AI's "approachable SaaS" default. |
| **Instrument Sans** | Recent Google Fonts addition that AI latched onto for "modern editorial." |
| **Instrument Serif** | Instrument Sans's serif pair. AI reaches for the set. |
| **Outfit** | Geometric sans with friendly curves. AI's "startup but warm" pick. |
| **Syne** | Distinctive, but AI overuses it for "bold creative studio" vibes. |
| **Playfair Display** | The display serif AI reaches for whenever "elegant" is mentioned. |
| **Lora** | "Literary" serif default. AI picks it for any content-heavy brand. |
| **Crimson / Crimson Pro** | AI's "book typography" reflex. Reaches for it on "editorial" prompts. |
| **Cormorant / Cormorant Garamond** | AI's "luxury serif" default. Fine typeface, but the choice reveals no thought. |
| **Fraunces** | Variable serif that AI defaults to for "artisan/craft" brands. |
| **Newsreader** | AI's "news/media" serif. The name itself triggers the association. |

Not banned from existence — banned from being the first answer. If a genuine catalog search lands on one of these after rejecting the reflex, that's different. But the reflex must be broken first.

---

## Type Classification

Know what you're choosing:

### Serif

| Class | Characteristics | Reads As | Canonical Examples |
|---|---|---|---|
| **Humanist / Old Style** | Angled stress, low contrast, bracketed serifs | Warm, readable, scholarly | Garamond, Sabon, Caslon |
| **Transitional** | Vertical stress, moderate contrast | Authoritative, balanced, institutional | Baskerville, Times, Century |
| **Modern / Didone** | Extreme contrast, hairline serifs, vertical stress | Dramatic, elegant, luxurious | Bodoni, Didot |
| **Slab / Egyptian** | Thick rectangular serifs, low contrast | Sturdy, mechanical, bold | Clarendon, Rockwell, Sentinel |

### Sans Serif

| Class | Characteristics | Reads As | Canonical Examples |
|---|---|---|---|
| **Humanist** | Calligraphic bone structure, open counters | Friendly, organic, readable | Gill Sans, Fira Sans, Lucida |
| **Transitional / Grotesque** | Even stroke width, neutral, large x-height | Professional, contemporary, clear | Helvetica, Univers, Aktiv Grotesk |
| **Geometric** | Built from circles and lines, uniform strokes | Precise, systematic, engineered | Futura, Avenir, Century Gothic |

### What The Classification Tells You

The classification maps to a temperature axis: Humanist (warm) → Transitional (neutral) → Geometric/Modern (cool). Match this to the brand-voice words from step 1. "Worn leather" is humanist territory. "Glass tower" is geometric/modern.

---

## Brand Personality → Font Family Mapping

| Personality | Serif Direction | Sans Direction | Avoid |
|---|---|---|---|
| Authoritative, established | Transitional (Baskerville, Caslon) | Grotesque (Univers, Aktiv) | Geometric — too cold for trust |
| Elegant, luxurious | Modern (Bodoni, Didot) | — (serif preferred) | Slab — too blunt for luxury |
| Warm, approachable | Humanist (Sabon, Garamond) | Humanist (Gill Sans, Fira) | Modern — too sharp for warmth |
| Technical, precise | — (sans preferred) | Geometric (Futura, Avenir) | Humanist — too organic for precision |
| Bold, disruptive | Slab (Clarendon, Sentinel) | Geometric bold weights | Transitional — too safe for disruption |
| Artisan, handmade | Humanist with irregularity | — (serif preferred) | Geometric — contradicts the hand |
| Corporate, neutral | Transitional (Century) | Transitional (Helvetica, Univers) | Display faces — too loud for neutral |

"It is not the type but what you do with it that counts." The family gets you in the neighborhood; weight, size, spacing, and color do the actual work.

---

## Pairing Rules

### When to Use Two Families

Use two families when the brand needs to distinguish **two voices** — e.g., headlines that shout vs. body that explains, or a display personality vs. a functional interface. If both voices could be served by weight contrast within one family, use one family.

### When One Family Suffices

Superfamilies (serif + sans sharing a common skeleton) solve most pairing needs: Scala/Scala Sans, Thesis, Source Serif/Source Sans. One purchase, guaranteed harmony.

### The Cardinal Rule: Contrast, Not Harmony

Two similar typefaces fight. Two different typefaces converse.

- **TYPE CRIME:** Two serif bolds side by side. They're close enough to look like a mistake.
- **TYPE CRIME:** Weights too close — regular next to book, or medium next to semibold. If you can't tell them apart at arm's length, the contrast is too low.
- **Minimum weight contrast:** Skip at least two weight steps. Regular (400) pairs with Bold (700), not Medium (500).

### Practical Pairing Formula

1. One serif + one sans from different classification temperatures (e.g., Humanist serif + Geometric sans = high contrast).
2. Assign clear roles: one for display (headlines, pull quotes), one for text (body, UI labels).
3. Never let both families appear at the same size and weight on the same page.

---

## Type Scale

Hand-crafted steps, not mathematical ratios:

```
12 / 14 / 16 / 18 / 20 / 24 / 30 / 36 / 48 / 60 / 72
```

- Use `px` or `rem`, not `em`. Compound `em` values create unpredictable sizing.
- Body: 16–18px. Below 16 strains reading on screens.
- Line length: 45–75 characters (20–35em). Wider loses the reader's eye.
- Line height: narrow columns → 1.5×, wide columns → up to 2.0×.
- Limit to 3–4 sizes per view. If you need more, the hierarchy is unclear.

---

## Reflex-Reject Aesthetic Lanes (Typography-Specific)

From ARCHITECTURE.md, expanded with typographic tells:

### Tech-Minimal Blue
**Type tell:** Geometric sans (Inter, DM Sans, Space Grotesk) at one weight, all-caps micro labels, generous letter-spacing on headings. The typography says nothing — it's a vessel for the blue.

### Editorial-Magazine
**Type tell:** Display serif italic for headlines + small monospace for labels + ruled separators. Looks like a Substack template. The serif is always high-contrast (Playfair, Cormorant). The mono is always Space Mono or IBM Plex Mono.

### DTC Pastel
**Type tell:** Rounded sans-serif (Plus Jakarta, Outfit) or a script accent for the wordmark. Everything is medium weight — no bold, no light, no tension. The typography is as soft as the palette.

### How to Escape

The lanes aren't wrong in isolation — they're wrong as defaults. Escape by:
1. Running the 4-step procedure honestly (step 2 catches the reflex)
2. Mixing classification temperatures (a humanist serif in a "tech" brand breaks the lane)
3. Using weight contrast aggressively (bold/light pairing creates energy that soft defaults lack)
4. Choosing a typeface with genuine character — irregular terminals, distinctive letterforms, an actual g

---

## Bans

Match-and-refuse. If the type pipeline outputs any of these, reject and rework.

| Ban | Why |
|---|---|
| Any font on the reflex-reject list as first instinct (see list above) | Training-data defaults. The 4-step procedure must break the reflex before any of these are reconsidered. |
| More than 2 font families in one brand system | Two voices (display + text) is the ceiling. A third family signals indecision. |
| Display fonts for body text | Display faces are sized for headlines. At body sizes they fatigue the reader within two paragraphs. |
| Weights too close together (regular/medium, medium/semibold) | If you can't tell them apart at arm's length, the contrast is too low. Skip at least two weight steps (400 → 700, not 400 → 500). |
| Serif + serif or sans + sans from the same classification temperature | Two similar typefaces fight. Two different typefaces converse. Mix classification temperatures for contrast. |
| Overspecified type scale (12+ named styles) | A brand identity is not a UI design system. Four to six named roles: display, heading, body, caption. See anti-slop.md #8. |
| Font-weight-only hierarchy | Weight is one axis. Real hierarchy uses size, weight, case, spacing, and color together. See anti-slop.md #7. |
| Type specimens using "The quick brown fox" | Show real brand copy in the actual typeface. Lorem ipsum hides that the chosen font doesn't work with the brand's vocabulary. |

---

## Type Slop Test

If the type selection was driven by training-data gravity rather than brand-voice words, it failed.

**Check 1 — The Reflex Audit:** Was step 2 of the 4-step procedure actually performed? If the font selection skipped the reflex-rejection step, the result is unverified.

**Check 2 — The Voice-Word Match:** Read the three brand-voice words aloud. Does the chosen typeface physically feel like those words? If "worn leather" is met with a geometric sans, the words and the font live in different worlds.

**Check 3 — The One-Family Test:** Remove the secondary typeface. Can the brand survive with one family and weight contrast alone? If yes, the second family is decoration. If no, the pairing is justified.

**Check 4 — The Aesthetic Lane Check:** Does the type selection (family + pairing + weight usage) map to one of the three reflex-reject aesthetic lanes (tech-minimal blue, editorial-magazine, DTC pastel)? If yes, see anti-slop.md #24.

---

## Calibration Typefaces

Not a shopping list — a calibration set. These are typefaces whose quality is beyond question. Use them to train your eye, then find contemporary equivalents with the same structural integrity:

- **Garamond** (1532) — the humanist serif benchmark
- **Caslon** — English text standard for two centuries
- **Baskerville** (1757) — the transitional benchmark
- **Bodoni** (1788) — the modern serif benchmark
- **Century Expanded** (1900) — wide, readable, American
- **Futura** (1930) — the geometric sans benchmark
- **Helvetica** (1957) — the grotesque benchmark
- **Univers** (1957) — systematic grotesque; 21 versions, 5 weights, 5 widths
- **Optima** — a sans with calligraphic stress; neither serif nor sans

Quality heuristic: 5+ weights, tall x-height, available on major platforms. Popular fonts are popular partly because they're well-made.
