# Color Theory Reference

The skill's color pipeline reads this file to avoid training-data defaults.

---

## OKLCH System

All colors specified in OKLCH(lightness, chroma, hue).

- **Lightness** (L): 0–100%. 0 = black, 100 = white.
- **Chroma** (C): 0–0.4. Distance from grey. Higher = more saturated.
- **Hue** (H): 0–360° angle on the color wheel.

### Named Rules

**Named rule — The Chroma Decay Rule:** Reduce chroma as lightness approaches 0 or 100. High-chroma darks clip to black; high-chroma lights read as neon. Peak chroma belongs near the middle of the lightness range (L:40–60).

**Named rule — The Tint Everything Rule:** Never use `#000` or `#fff`. Tint every neutral toward the brand hue. A warm brand gets warm greys (H:60–80). A cool brand gets cool greys (H:240–260). The darkest dark is L:15, not L:0.

**Named rule — The Commitment Axis:** Choose a color strategy before picking colors. Start at Restrained (tinted neutrals + one accent ≤10%). Move right only if the brand personality demands it. Most brands overestimate how far right they belong. The four positions: Restrained → Committed → Full palette → Drenched.

**Named rule — The Competitor Dodge Rule:** Never pick the same primary color as the brand's top 3 competitors. Map competitor primaries first. Differentiate within the category — a fintech brand can avoid navy without choosing hot pink. Teal or deep green says "financial" without saying "me too."

**Named rule — The Perceptual Brightness Rule:** Perceived brightness varies by hue at the same OKLCH lightness. Yellow (H ≈ 90°) reads bright; blue (H ≈ 260°) reads dark. Compensate when building tints and shades. When making tints: rotate hue toward 90°/180°/300° (yellow/cyan/magenta). When making shades: rotate toward 0°/120°/240° (red/green/blue).

### 9-Shade Palette Construction

Build each color role as a 9-step scale (100–900):

1. Pick the base color (500). This is the color you'd use on a white background.
2. Pick the edges: 100 (barely tinted white) and 900 (nearly black with hue).
3. Fill 200, 300, 400 between 100 and 500. Fill 600, 700, 800 between 500 and 900.
4. Increase chroma as lightness moves away from the extremes. Peak chroma near 400–600.
5. Rotate hue slightly at each step (lighter → warm shift, darker → cool shift).

Three palette categories minimum: greys (tinted neutral), primary (brand color), accent (supporting).

---

## Color Strategy Selection

Choose before picking any colors. From ARCHITECTURE.md:

| Strategy | Surface Coverage | Fits | Example Signal |
|---|---|---|---|
| **Restrained** | Tinted neutrals + one accent ≤10% | Corporate, law, finance, consulting | "We want to look serious" |
| **Committed** | One saturated color carries 30–60% | Most consumer brands, SaaS | "We have a color" |
| **Full palette** | 3–4 named roles, each deliberate | Fashion, lifestyle, food, media | "We're expressive" |
| **Drenched** | The surface IS the color | Entertainment, youth, disruptors | "We want to own a feeling" |

Selection heuristic: start Restrained. Move right only if the brand personality demands it. Most brands overestimate how far right they belong.

---

## Emotion-to-Color Mapping

OKLCH ranges are approximate anchors — use them as starting points, not gospel.

| Emotion | Color Family | OKLCH Anchor | Notes |
|---|---|---|---|
| Trust, reliability | Deep blue | L:35–45 C:0.10–0.18 H:250–265 | Credible, authoritative, professional |
| Calm, patience | Light blue | L:70–85 C:0.06–0.12 H:230–250 | Sky blue reads tranquil, faithful |
| Energy, urgency | Bright red | L:50–60 C:0.20–0.28 H:20–30 | Energizing, passionate; also signals danger |
| Warmth, comfort | Golden yellow | L:75–85 C:0.12–0.20 H:85–100 | Nourishing, buttery; amber for mellow richness |
| Luxury, prestige | Deep purple | L:25–40 C:0.12–0.20 H:290–310 | Visionary, royal; also deep red (L:30–40 H:15–25) |
| Play, fun | Vibrant orange | L:65–75 C:0.18–0.25 H:55–70 | Whimsical, energetic; tangerine for juicy vitality |
| Growth, health | Foliage green | L:45–60 C:0.10–0.18 H:145–165 | Natural, balanced, restorative |
| Sophistication | Charcoal | L:25–35 C:0.02–0.06 H:(brand) | Steadfast, professional; tint toward brand hue |
| Freshness, youth | Lime/aqua | L:70–80 C:0.14–0.22 H:155–185 | Citrusy, dreamy, youthful |
| Romance, softness | Dusty pink | L:70–80 C:0.06–0.12 H:0–15 | Subtle, cozy; light pink for romantic |
| Earthiness, craft | Terra cotta/brown | L:40–55 C:0.08–0.14 H:50–65 | Wholesome, grounded, artisan |
| Creativity, drama | Red-purple | L:40–55 C:0.16–0.24 H:320–345 | Sensual, thrilling, expressive |
| Serenity, taste | Teal | L:50–65 C:0.08–0.16 H:190–210 | Cool, sophisticated, confident |
| Classic, timeless | Neutral grey | L:40–70 C:0.01–0.04 H:(brand) | Corporate, practical; always tint |

### Colors That Carry Negative Associations

Be aware, not afraid. Context determines reading:

- Bright yellow at high chroma: cowardice, hazard, caution tape
- Olive green: military, drab (deliberate in outdoor brands, risky elsewhere)
- Chartreuse: gaudy, tacky if poorly paired (but bold and trendy when owned)
- Deep black at high coverage: oppressive, funereal (but powerful and elegant in fashion)
- Clinical white: sterile, cold (but pure and clean in wellness)

---

## Category-Aware Color Selection

Category-aware color selection principles:

1. **Map competitor primaries.** List the top 3 competitors' dominant colors. Never match them.
2. **Check industry gravity.** Every industry has a default color pull: fintech → navy, wellness → sage, food → red/orange. Knowing the pull lets you resist it deliberately.
3. **Five steps:** (a) shop the competition, (b) research the category, (c) prioritize color psychology, (d) know the audience, (e) remember 95% of consumer response is subconscious — color is the first thing noticed and the last thing forgotten.
4. **Differentiate, don't alienate.** The goal is to stand out within the category, not outside it. A fintech brand can avoid navy without choosing hot pink — teal or deep green says "financial" without saying "me too."

---

## Color Combination Schemes

Color combination schemes:

- **Monochromatic**: One hue, vary lightness and chroma. Safe, always harmonious. Risk: monotony.
- **Analogous**: Adjacent hues (±30°). Comfortable, natural. Risk: low contrast.
- **Complementary**: Opposite hues (±180°). High energy, high contrast. Risk: vibrating/garish if both high-chroma.
- **Split complementary**: One hue + two flanking its complement (±150° and ±210°). Contrast without collision.
- **Triadic**: Three hues at 120° intervals. Rich, balanced. Risk: circus if all high-chroma — mute at least one.

Rule: the more hues, the more you must vary chroma and lightness to avoid chaos.

---

## Color Relativity

Color deceives continually. These are not opinions — they are perceptual facts:

1. **One color appears as two.** Place the same swatch on dark and light grounds. It looks lighter on dark, darker on light. The skill must never assume a color "is" a fixed value — it is always relative to its surround.
2. **Two colors appear as one.** A ground subtracts its own hue from what sits on it. Red-orange on red ground looks orange. Blue-green on blue ground looks green. Different starting colors can converge.
3. **Simultaneous contrast.** The eye generates the complement of any color it stares at. Grey on yellow ground picks up a violet cast. This means adjacent colors shift each other's apparent hue.
4. **Quantity changes quality.** A small accent reads differently from a large field of the same color. Test every palette color at both chip size and surface size.
**Named rule — The Relativity Truth:** 60% of trained designers misjudge lighter/darker. Do not trust your eye for lightness comparison. Use the L value. Always test palette colors in context — on the actual background, at the actual size, next to the actual neighbors. Swatches lie.

---

## Bans

Match-and-refuse. If the color pipeline outputs any of these, reject and rework.

| Ban | Why |
|---|---|
| `#000000` or `#ffffff` as any palette color | Pure black reads as "no decision was made." Pure white is clinical. Tint every neutral. See anti-slop.md #4. |
| Purple-blue gradients as default brand expression | The single most common AI brand cliché. If a multi-hue gradient appears, it must be earned by editorial context. See anti-slop.md #2. |
| Industry-alone palette selection (fintech → navy, wellness → sage, food → red/orange) | This is the training-data reflex. Run the first-order AI slop test before finalizing. See anti-slop.md #1. |
| The five-swatch disconnected grid (primary, secondary, accent, dark, light) | A palette is a system of relationships, not a list. Define color roles with surface assignments and usage ratios. See anti-slop.md #3. |
| Palette colors tested only at swatch size | Color relativity means a small chip and a full surface read differently. Test at both scales. |
| Exceeding the commitment axis for the brand's actual needs | Most brands overestimate how far right they belong. A corporate law firm does not need a Drenched palette. |

---

## AI Palette Slop Test

From ARCHITECTURE.md, expanded:

### First-Order Check
Could someone guess this palette from the industry alone?
- Fintech → navy + gold
- Wellness → sage + cream
- Tech startup → blue + white
- Coffee → brown + cream
- Legal → dark blue + grey

If yes: it's the training-data reflex. Rework.

### Second-Order Check
Could someone guess the palette from category-plus-anti-reference?
- "Coffee brand that's not brown" → editorial cream + black
- "SaaS that's not blue" → terminal-dark mono
- "Wellness that's not sage" → warm terracotta earth tones

If yes: it's the trap one tier deeper. The contrarian choice has also become a cliche. Rework until neither the obvious nor the obvious-opposite is the answer.

### Purple-Blue Gradient Ban
The single most common AI brand cliche. If the palette trends toward purple-blue gradients at any point, reject it immediately. This is non-negotiable.
