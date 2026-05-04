# Grid and Layout

Rules for composing brand collateral — guidelines pages, business cards, social posts, logo sheets. Every HTML template in `assets/templates/` must follow these.

---

## The Grid Is a Tool, Not a Religion

Choose a grid that fits the content. A page with no grid is chaos. A page with a grid too fine for its content is the same thing — infinite options is no constraint. A grid too coarse starves the layout of alternatives. Match the grid density to the information density.

**Named rule — The Fixed-Width Exception:** Do not outsource every layout decision to a column grid. Elements that have an ideal fixed width — sidebars, logo lockups, stat blocks — get a fixed width. Only the main content area flexes.

---

## Spacing System

**Named rule — The Scale-Pick Rule:** Define a spacing scale before placing anything. Never eyeball spacing. Pick from the scale. Base on 16px with geometric steps:

```
4 · 8 · 12 · 16 · 24 · 32 · 48 · 64 · 96 · 128 · 192 · 256
```

No two adjacent values closer than 25% apart. At small sizes (icon padding, input insets) a couple of pixels changes everything. At large sizes (card widths, hero spacing) 20px is invisible. The scale accounts for this — tight steps at the bottom, wide jumps at the top.

---

## Margins and Edges

Outside margins create tension between the edge and the content. Tight margins feel urgent, editorial. Generous margins feel luxurious, restrained.

**Named rule — The Margin-First Rule:** Set margins before columns. The margin is the first brand signal — it says how the brand breathes. For brand guidelines documents, default to generous (≥48px on a standard page). For social cards, tighter is fine (24–32px). Never use zero margins on any brand collateral. Even full-bleed images need the surrounding layout to declare a margin zone.

---

## Column Structure

Divide the content area into columns after setting margins. Standard column counts by format:

| Format | Columns | Use |
|---|---|---|
| Business card | 2 | Name block + contact block |
| Social post (square) | 1–2 | Headline + supporting text |
| Brand guidelines page | 3–4 | Body text + callouts + swatches |
| Logo sheet | 2–3 | Logo variants + clearspace diagrams |
| Letterhead | 3 | Asymmetric: 1 narrow (logo) + 2 text |

For asymmetric layouts, leave one column blank or narrower. Symmetry reads as default; asymmetry reads as intentional.

Column gutters should be tight — ideally the width of one line of body text. Wider gutters fragment the page. Tighter gutters blur the columns.

---

## Baseline Grid

**Named rule — The Baseline Lock Rule:** Anchor all text to a baseline grid founded on the body type size. If body copy is set at 16px/24px (size/leading), the baseline grid is 24px. Every other type size must sit on a leading that is a multiple of 24. This keeps text blocks from drifting when placed in adjacent columns.

When type and images share the same module grid, the page gains a level of refinement that reads as professional rather than templated.

---

## Horizontal Modules

Columns handle vertical rhythm. Horizontal modules handle where things sit top-to-bottom.

Divide the page height into modules — 4 to 8 depending on content density. Place content at module intersections. The logo goes at a module line. The body text starts at a module line. Contact info anchors to a module line.

This gives horizontal continuity across multi-page documents. Page 1 and page 12 feel related because elements land on the same horizontal rails.

---

## White Space

**Named rule — The Don't Fill Rule:** White space is a design element, not leftover space. Start with too much white space, then remove until it feels right. The reverse approach — adding space when things look cramped — produces layouts where every element has the minimum breathing room to not look bad. Minimum is not the goal.

A brand guidelines page with generous white space says "we are confident enough to leave room." A cramped page says "we are afraid you'll miss something." Dense layouts have their place — dashboards, data tables, spec sheets. Brand identity collateral is not that place.

---

## Ambiguous Spacing

**Named rule — The Ambiguous Spacing Rule:** If two spacings are close but not identical, one is a mistake — pick one. When two elements have equal space above and below, the eye cannot tell which group they belong to. This is the most common layout failure in generated brand collateral.

The fix: space within a group must always be less than space between groups. A label sits 8px above its swatch. The gap between swatch groups is 32px. The relationship is now unambiguous.

This applies everywhere:
- Section headings get more space above than below (they belong to what follows, not what precedes)
- Related items in a list get tighter spacing than the gap between lists
- Caption-to-image is tighter than image-to-next-section

---

## Don't Fill the Canvas

**Named rule — The Content-Width Rule:** A brand guidelines PDF does not need to fill every page edge to edge. If the content wants 600px of width, use 600px. Give each element the space it needs. Do not widen something to match something else. A narrow text block beside a wide image is fine — it creates visual hierarchy. Stretching a narrow layout to fill 1200px makes it harder to read and looks like a template.

---

## Format-Specific Rules

### Brand Guidelines (A4/Letter, multi-page)
- 3-column grid, 48px margins
- Table of contents on page 2
- Color swatches: full-width band, not tiny squares
- Typography specimens: show real brand copy, not "The quick brown fox"
- Minimum 1 full page of white space (inside cover or divider) per 6 pages of content

### Business Card (90×55mm / 3.5×2in)
- 2-column grid
- Logo: top-left or centered, never bottom
- Contact info: smaller type, aligned to grid
- Back of card: one strong brand element (color, pattern, logo mark)
- Never cram — if it doesn't fit, cut copy, don't shrink type

### Social Post (1080×1080 or 1080×1350)
- 1- or 2-column grid
- 24–32px margins
- Body text no smaller than 32px (mobile readability)
- One focal element per card — headline, stat, or image. Not all three.

### Logo Sheet
- Show: primary lockup, reversed, monochrome, mark only, minimum size
- Each variant in its own clearspace box
- Clearspace: minimum equals the height of the logo mark
- Include one "don't do this" row: stretched, recolored, rotated, cropped

---

## CSS Grid Implementation

All templates use CSS Grid, not flexbox-for-layout. Map the conceptual grid directly:

```css
.guidelines-page {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  padding: 48px;
}
```

Span elements across columns with `grid-column: span 2` or `grid-column: 1 / -1` for full-width. Do not nest grids more than one level deep in brand collateral — it creates alignment drift.

Use `max-width` on the outer container. Do not let guidelines pages stretch beyond 1200px on screen or 210mm in print. The content has an ideal width; honor it.

---

## The Layout Integrity Check

Before finalizing any template, verify:

1. Every text block aligns to the baseline grid
2. No two spacing values are within 4px of each other unless they are the same value
3. White space between sections exceeds white space within sections
4. The page reads correctly with all images replaced by grey rectangles
5. The layout holds if any single text block doubles in length

---

## Bans

Match-and-refuse. If any layout contains these, rework.

| Ban | Why |
|---|---|
| Asymmetric margins without explicit rationale | Margins must be set intentionally. A 48px left / 24px right margin is fine if the reason is documented. Random asymmetry looks like a mistake. |
| Mixing spacing scales within one document | Pick one scale. If the document uses the geometric scale (4·8·12·16·24·32...), every spacing value comes from it. No exceptions. |
| Side-stripe borders (`border-left` > 1px as colored accent) | This is a UI pattern that migrated into brand design. See anti-slop.md #13. |
| Identical card grids (same size, same structure, evenly spaced) | A landing page pattern, not a brand expression. Vary the layout. See anti-slop.md #14. |
| Gradient text (`background-clip: text`) | Reduces legibility. Dates the brand to 2021–2023. See anti-slop.md #17. |
| Nested grids more than one level deep | Nesting creates alignment drift. CSS Grid subgrid or manual column tracking is the fix. |
| Zero margins on any brand collateral | Even full-bleed elements need a declared margin zone. |
| Layout tested only at ideal content length | Content doubles, halves, or is replaced with a grey rectangle — the layout must hold. |

---

## Grid Slop Test

If you can't identify the grid by overlaying lines on the final output, there is no grid.

**Check 1 — The Grid Overlay Test:** Overlay column lines and baseline grid lines on the final output. Does every element snap to the intersection of a column and a baseline rail? If not, the grid exists on paper but not in practice.

**Check 2 — The Spacing Audit:** List every spacing value in the layout. Are they all from the declared scale? If any value is ad-hoc, the Scale-Pick Rule was violated.

**Check 3 — The Grouping Check:** For every pair of adjacent regions, is the between-group space greater than the within-group space? If any region is ambiguous about what it belongs to, see the Ambiguous Spacing Rule.

**Check 4 — The Content-Resize Test:** Double the length of the longest text block. Halve the length of the shortest. Replace all images with grey rectangles. Does the layout hold without breaking? If elements start to overlap or float, the grid has weak joints.

**Check 5 — The CSS Grid Audit:** Inspect the CSS. Is the layout using CSS Grid (not flexbox-for-layout)? Are there any `margin-top: Xpx` values that should be `gap`? Ad-hoc margins signal the grid was abandoned.
