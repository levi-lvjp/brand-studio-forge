# Anti-Slop Checklist

AI-generated brand identities fail in predictable ways. This checklist catches them before the user sees them. Run every identity kit through these checks before delivery. Any single failure is a rework trigger.

---

## Color Slop

### 1. Industry-Predictable Palette
**What it looks like:** Fintech → navy + gold. Wellness → sage + cream. Food → warm red + kraft brown. Tech → blue + white.
**Why it's bad:** The user could have typed their industry into any generator and gotten this. Zero brand differentiation.
**What to do instead:** Run the first-order AI slop test. If someone can guess the palette from the industry name alone, rework. Pick a color strategy (restrained/committed/full/drenched) first, then select colors that serve the strategy rather than the category.

### 2. Purple-Blue Gradient Default
**What it looks like:** Linear gradient from purple to blue as the primary brand expression. Sometimes with a pink third stop.
**Why it's bad:** The single most common AI brand cliche. Signals "I asked a model to make something modern."
**What to do instead:** If the brand genuinely needs a gradient, use a single-hue gradient (light-to-dark within one OKLCH hue). Multi-hue gradients are earned by editorial context, not slapped on as identity.

### 3. The Five-Swatch Grid
**What it looks like:** Primary, secondary, accent, dark, light — five swatches in a neat row, each with a hex code. Looks complete. Means nothing.
**Why it's bad:** A palette is a system of relationships, not a list. Five disconnected swatches don't explain how colors interact, which surfaces they live on, or what ratio they appear in.
**What to do instead:** Define color roles: surface, text, accent, emphasis. Show them in context — on a mock page, a card, a header — not in a swatch row.

### 4. Pure Black and Pure White
**What it looks like:** `#000000` for text, `#ffffff` for backgrounds.
**Why it's bad:** Pure black on pure white is harsh. Real brand design tints neutrals toward the brand hue. Pure black reads as "no decision was made."
**What to do instead:** Tint all neutrals. A warm brand gets warm greys (OKLCH hue ~60–80). A cool brand gets cool greys (OKLCH hue ~240–260). The darkest dark should be ~L:15, not L:0.

---

## Typography Slop

### 5. Reflex-Reach Font
**What it looks like:** Inter for sans, Playfair Display for serif, Space Mono for mono. Any font on the reflex-reject list.
**Why it's bad:** These are training-data defaults. The model reaches for them because they appear most often in its training set, not because they're right for this brand.
**What to do instead:** Follow the 4-step font procedure. Write three brand-voice words. List your reflex picks. Reject them. Browse a real catalog with the words in mind.

### 6. The Serif-Sans "Pairing"
**What it looks like:** One display serif + one geometric sans. Always. Regardless of brand personality.
**Why it's bad:** This is the only pairing structure most models know. A rugged outdoor brand and a luxury skincare brand get the same structural answer.
**What to do instead:** Consider serif+serif, sans+sans, slab+humanist, monospace+grotesque. The pairing should emerge from the brand voice words, not from a formula.

### 7. Font-Weight-as-Hierarchy
**What it looks like:** Bold for headings, regular for body, light for captions. Type hierarchy expressed entirely through weight.
**Why it's bad:** Weight is one axis. Real hierarchy uses size, weight, case, spacing, and color together. Weight-only hierarchy is flat and monotonous across a full guidelines document.
**What to do instead:** Define a type scale with at least 4 roles: display, heading, body, caption. Vary size and tracking between levels. Use weight sparingly — two weights per family is usually enough.

### 8. Overspecified Type Scale
**What it looks like:** Heading 1 through Heading 6, body large, body, body small, caption large, caption, caption small, overline, label — twelve or more named styles.
**Why it's bad:** No brand collateral uses twelve text styles. This is a UI design system, not a brand identity. It makes the guidelines look thorough while providing no real guidance.
**What to do instead:** Four to six named styles. Display, heading, body, caption. Maybe a pull-quote style. Each one with a specific, demonstrated use case.

---

## Voice Slop

### 9. "Empower" and Family
**What it looks like:** "We empower brands to elevate their presence and unlock seamless growth through innovative solutions."
**Why it's bad:** Every word in that sentence is an AI brand-copy tell. "Empower," "elevate," "unlock," "seamless," "innovative" — these are filler words that sound meaningful and say nothing.
**What to do instead:** State what the brand does in concrete terms. "We roast coffee and ship it to your door on Tuesdays" says more than "We empower coffee lovers to elevate their morning ritual."

### 10. The Three-Pillar Mission
**What it looks like:** "Quality. Innovation. Community." — three abstract nouns presented as brand values.
**Why it's bad:** These could belong to any company in any industry. They differentiate nothing. No employee will change a decision because "quality" is listed as a value.
**What to do instead:** Brand values should be specific enough to be actionable and unusual enough to be memorable. "We'd rather ship late than ship ugly" is a real value. "Quality" is not.

### 11. Voice-Tone Conflation
**What it looks like:** "Our brand voice is friendly, professional, and approachable" — with no distinction between what stays constant and what shifts by context.
**Why it's bad:** Voice is constant. Tone shifts. If the guide says the voice is "playful" but doesn't address how that works in a crisis email or a legal notice, it will be ignored.
**What to do instead:** Define voice as 3–4 constant traits. Then show tone variation across contexts: social post, support reply, investor update, error message. Same voice, different tone.

### 12. Generic Tagline
**What it looks like:** "Your partner in [industry]." "Where [abstract noun] meets [abstract noun]." "Redefining [industry] for the modern era."
**Why it's bad:** Template sentence. The user paid for a brand identity and got a Mad Lib.
**What to do instead:** A tagline should be ownable — if you can replace the brand name with a competitor's and the tagline still works, it's generic. Write something that only this brand could say.

---

## Layout Slop

### 13. Side-Stripe Borders
**What it looks like:** A colored `border-left: 4px solid` on a card, callout, or section. Usually the brand accent color.
**Why it's bad:** This is a UI pattern (used in alerts and code blocks) that migrated into brand design through AI generation. It signals "component library" not "brand identity."
**What to do instead:** Use white space, background color, or typographic hierarchy to distinguish sections. If you need a rule, make it a full-width horizontal one.

### 14. Identical Card Grids
**What it looks like:** Three or four cards, same size, same structure, evenly spaced in a row. Often: icon, heading, short paragraph.
**Why it's bad:** This is a landing page pattern, not a brand expression. It makes every brand look like every SaaS marketing site.
**What to do instead:** Vary the layout. One large element + two small. An asymmetric grid. A single full-width panel with internal structure. The card grid is earned by content that genuinely has equal-weight items — most content does not.

### 15. The Hero-Metric Template
**What it looks like:** Large number, small label underneath, optional gradient accent. "500+ Clients Served."
**Why it's bad:** This is a pitch-deck pattern. It communicates "we have a template" not "we have a brand."
**What to do instead:** If metrics matter, integrate them into the narrative. A case study with a number in context beats a floating statistic.

### 16. Glassmorphism as Default
**What it looks like:** Blurred glass cards, backdrop-filter, translucent panels with frosted edges.
**Why it's bad:** Glassmorphism is a specific aesthetic choice (Apple circa 2020). Using it as the default surface treatment for any brand is style without substance.
**What to do instead:** Surface treatment should come from the brand mood. Matte for understated brands. Textured for craft brands. Clean flat for modern brands. Frosted glass only if the brand world is literally translucent.

### 17. Gradient Text
**What it looks like:** `background-clip: text` with a gradient fill on headings.
**Why it's bad:** Reduces legibility. Looks like a tech product landing page. Dates the brand to 2021–2023.
**What to do instead:** Solid color for text. Always. If you want color impact, put it on the surface behind the text or in a graphic element.

---

## Logo Slop

### 18. The Initial-Mark Default
**What it looks like:** Brand name's first letter in a circle, square, or rounded square. Sometimes with a gradient.
**Why it's bad:** This is the lowest-effort logo concept. It says nothing about the brand beyond its first letter. Every brand gets the same structural answer.
**What to do instead:** A logo mark should emerge from the brand's world — what it does, makes, or stands for. If the best concept genuinely is a lettermark, it needs distinctive typography or a conceptual twist that makes it ownable.

### 19. Thin-Line Geometric Icon
**What it looks like:** An abstract geometric shape made of thin, uniform-weight strokes. Usually symmetrical. Often looks like a tech startup logo generator output.
**Why it's bad:** Thin-line geometric marks are undifferentiated. They scale poorly at small sizes (the lines disappear). They have no texture, weight, or personality.
**What to do instead:** Consider filled shapes, varied stroke weights, organic forms, or typographic solutions. Not every brand needs an icon mark — a well-set wordmark is often stronger.

### 20. Unearned Complexity
**What it looks like:** A logo that tries to encode three brand concepts in overlapping shapes. "The three circles represent our values of innovation, community, and sustainability."
**Why it's bad:** Logos don't work as puzzles. If you need a legend to explain the mark, the mark has failed. This is narrative retrofitting — the explanation was written after the shapes were generated.
**What to do instead:** One concept. One shape. If the mark needs explaining, simplify until it doesn't.

---

## Naming Slop

### 21. The Portmanteau Default
**What it looks like:** Two relevant words mashed together: "CafeFlow," "BrandForge," "StyleVault."
**Why it's bad:** Reads as generated. Lacks personality. Usually one "meaning" word + one "tech/action" word.
**What to do instead:** Consider real words, obscure words, metaphors, place names, invented words with phonetic texture. A name should be pronounceable, memorable, and not immediately decode-able into its component parts.

### 22. The -ly / -ify Suffix
**What it looks like:** "Brandify." "Designly." "Craftio."
**Why it's bad:** Dates to the 2010s startup naming wave. Reads as generic SaaS. No brand personality.
**What to do instead:** Drop the suffix. If the root word is good enough, it can stand alone. If it can't, find a better root.

---

## Meta Slop

### 23. The Second-Order Trap
**What it looks like:** A coffee brand that avoids brown (good instinct) but lands on editorial-typographic cream with a display serif (the predictable anti-reference).
**Why it's bad:** Avoiding the obvious and landing on the next-most-obvious is not differentiation. AI models are now trained on enough anti-pattern content to generate the "sophisticated alternative" as reliably as the original cliché.
**What to do instead:** Run both slop tests. First-order: could someone guess this from the industry? Second-order: could someone guess this from the industry + "but make it premium"? If either answer is yes, keep pushing.

### 24. Aesthetic-Lane Collapse
**What it looks like:** The brand identity falls cleanly into one of three AI aesthetic lanes: tech-minimal-blue, editorial-magazine, or DTC-pastel.
**Why it's bad:** These lanes are so overrepresented in AI training data that they're the new "default." Landing in one means the brand looks like everything else that tried to look distinctive.
**What to do instead:** If the mood board or initial direction maps to a recognized lane, deliberately introduce one element from outside it. A tech brand with hand-drawn typography. An editorial brand with saturated color. The disruption should be small enough to feel intentional, large enough to break the pattern.

### 25. Completeness Theater
**What it looks like:** A guidelines document with every possible section filled in — brand story, mission, vision, values, personality traits, voice attributes, color psychology, icon library, pattern library, motion principles — but each section is two sentences of boilerplate.
**Why it's bad:** Volume is not quality. A thin treatment of everything is worse than a deep treatment of the things that matter. The user needed three strong pages, not twenty weak ones.
**What to do instead:** Go deep on: color system, typography, voice, and logo usage. Leave out sections the brand doesn't need yet. A one-page-per-topic guide that says something real beats a 40-page template that says nothing.
