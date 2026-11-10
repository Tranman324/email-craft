# Taste

Adapted from CosmoBlk/email-design (MIT, George Hartley). Condensed, ESP-neutral, with conflict resolutions from the other sources. See CREDITS.md.

The default AI email: hero icon, three-card grid, category palette, "Read more" button, moonscape padding, plain footer. Correct and forgettable. Every rule below exists to break one of those reflexes.

## Archetypes

Commit to one before writing a line. Minimal-lux is the safe reflex; it is right about 30% of the time.

- **Editorial.** Newsletters, brand stories, long-form. Serif heads, full-bleed photo, generous leading, voice-rich single column. Refs: Patagonia, Tracksmith, Lucy Folk.
- **Bold mono.** Launches, promos, statements. One saturated colour floods the surface, huge type, few words. Refs: Absolut, Liquid Death, Fly By Jing.
- **Minimal lux.** Premium, transactional, restraint as positioning. Tinted neutrals, content column 472–520px, one accent, never discount-led. Refs: Stripe, Aesop, Apple, MoMA.
- **Founder letter.** Welcome, win-back, milestones, reply-drivers. Plain-text feel, first person, short paragraphs, signed, no template chrome. Refs: Ugmonk, Superhuman.
- **Punk / character.** Voice carriers, retention. Mascot or character, irreverent copy, custom art. Refs: Frank Body, Duolingo, Chubbies.
- **Lookbook.** The product is the design: fashion, food, paint. Photo over copy, gallery rhythm, full-bleed hero. Refs: Dior, Clare Paint, Starbucks seasonal.

## Colour

- Pick a strategy before a colour:
  - **Restrained:** tinted neutrals plus one accent at 10% or less of the surface. Transactional and minimal-lux only.
  - **Committed:** one saturated colour carries 30–60% of the surface. Default for brand emails.
  - **Drenched:** the surface is the colour. Heroes and statements.
- Tint every neutral toward the brand hue. Never pure `#000` or `#fff`.
- Pull saturation back near black and white; high chroma at extreme lightness reads garish.
- **Category-reflex check.** If the palette is guessable from the industry (fintech navy + gold, wellness white + sage, AI black + neon, ecommerce blush + cream), rework it.
- Text pairs hit 4.5:1 contrast (3:1 for 18pt+ or 14pt bold). Preview the dark-mode inversion.

## Typography

- One family per email; a second only for a functional reason. Always a web-safe fallback stack.
- Body 15–16px (14 floor). Headline 22–34px; bold-mono may push to 48px+. Step ratio at least 1.25.
- Line length 50–65 characters.
- Emphasis through weight or size. No gradient text, no `background-clip: text`, no text baked into images.

## Layout

- Single column, 600px body. Mobile-first; anything side by side must survive stacking.
- Vary spacing for rhythm; uniform padding reads as a wireframe.
- Cards only when they are truly the best affordance. Nested cards are always wrong.
- Touch targets at least 44×44px. Buttons full-width on mobile.

## Whitespace (where most AI emails fail)

LLMs pad everything top and bottom and add spacer rows. The result is a moonscape.

- Default section padding: top 0, bottom 32. The next section owns the rhythm.
- No two spacers in a row. No empty text block as a spacer. No `<br><br>` between blocks. Never margin and padding on the same side.
- Hero sits flush to the header (8px gap at most); space goes below it.
- Last content section before the footer: 32–48px bottom, never more. The footer brings its own top padding.

## Imagery

- Every image is a product, person, place, or moment. Decoration alone does not earn a slot.
- Each image 200KB or less; total payload 800KB or less. PNG or JPG; no SVG or WEBP.
- Alt on every image: meaningful images get purpose plus detail; decorative ones get `alt=""`; linked images describe the destination.
- Dark mode: transparent PNG logos, off-white backgrounds, swap to a light logo where supported.

## Copy

- Inverted pyramid: the answer first.
- Short paragraphs. No restated headings, no intro that repeats the subject.
- No em or en dashes, no `--`. Use commas, colons, periods, parentheses.
- One CTA above the fold; a second at the bottom is fine; three or more is dilution. CTA text names the destination ("See the winter kit", never "Click here" or "Learn more").
- Subject 45 characters or less. Preheader 90 or less. Both add information.

## Footer, in order

1. **Mission line.** Why the company exists, one sentence, verbatim from the brand's own fields or site. If nothing verifiable exists, omit it. Never invent one.
2. **Socials.** Three to five, real URLs, 24–32px icons with alt text.
3. **Physical address.** One line. Required by CAN-SPAM.
4. **Unsubscribe.** The word "Unsubscribe", visible, not a buried "preferences" euphemism. Preferences may sit beside it, never replace it.
5. Optional: contact email, "you're getting this because..." line.

Style: 12–13px, tinted neutral at 60–70% of body contrast (still 4.5:1), its own padding, no spacer above.

## Pushback patterns

- **"Bolder"**: escalate colour (restrained → committed → drenched), raise type contrast, shorten lines, move toward bold-mono or punk.
- **"Quieter"**: de-escalate colour, add whitespace selectively (never uniformly), cut the second CTA, move toward minimal-lux or editorial.
- **"More personality"**: founder-letter or punk; rewrite in first person; add one unexpected element.
- **"Too plain"**: the archetype is wrong. If minimal-lux was the default, offer bold-mono or lookbook once.
- **"Looks like AI made it"**: diagnose which of reflex palette, stock-feeling imagery, or missing voice, and fix only that.

## Pre-handoff checklist

Three or more misses means redraft.

- [ ] Subject 45 or less and adds information; preheader 90 or less, not a restatement
- [ ] One archetype, applied throughout
- [ ] Colour strategy committed; no category-reflex palette; no pure black or white
- [ ] At least one real image, sourced or explicitly prompted (founder-letter exempt)
- [ ] One CTA above the fold, two at most, each naming its destination
- [ ] Footer: socials, address, unsubscribe; mission line only if verified
- [ ] No double spacers, no `<br><br>`, asymmetric padding
- [ ] No em or en dashes in copy
- [ ] 600px single column, 44px touch targets, 4.5:1 contrast
- [ ] Voice is recognisably this brand
