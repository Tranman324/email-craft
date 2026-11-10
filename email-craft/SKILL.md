---
name: email-craft
description: "Use when designing or building an HTML email template. Commits to a design brief, then ships cross-client MJML or React Email HTML that passes a lint gate."
version: 1.0.0
author: Jeremy Tran (Athena)
license: MIT
platforms: [linux, macos, windows]
metadata:
  hermes:
    tags: [email, email-design, mjml, react-email, html-email, templates]
    related_skills: [no-ai-design-slop, audit-ai-design-slop]
---

# Email Craft

Taste first, code second, proof last. One email = one brief = one build = one check.
Triggers: draft, design, redesign, build, or critique an email template (newsletter, launch, promo, welcome, win-back, transactional, announcement).
Skip: strategy-only, deliverability-only, ESP selection, copy with no design.

## Workflow

1. **Context, silent.** Read the brand file, prior templates, and the brand site before asking anything. Fill this profile and mark each field known / inferable / missing:
   - company, from-name, mission line (verbatim from a real source only)
   - primary colour hex, secondary hex, logo URL (PNG or JPG)
   - voice descriptors
   - footer: physical address, socials, unsubscribe mechanism
   - production host for images (absolute URLs only)
2. **Ask at most three questions**, one numbered message, only when three or more fields that matter for *this* email are missing. Priority: purpose, archetype/tone, brand colour, mission line, address and socials. Otherwise default and list the defaults in the brief.
3. **Commit.** Read `references/taste.md`. Pick one archetype and one colour strategy, then write the brief (schema below). The brief is the contract; the build follows it.
4. **Resolve image slots.** Order: supplied brand assets, brand site (`og:image`, homepage hero, /about, /press), brand socials, then one explicit placeholder with a concrete prompt to the user. Real photography or commissioned illustration only; a marked placeholder beats stock or AI imagery.
5. **Pick the build path.**
   - **MJML (default):** HTML pasted into an ESP (Klaviyo, Mailchimp, Benchmark, Postmark), standalone files, Handlebars/Liquid templates. Read `references/mjml.md`. Start from `assets/<archetype>.mjml` when one matches.
   - **React Email:** the codebase already runs React/TypeScript and sends from code (Resend, Nodemailer, SES). Read `references/react-email.md`.
6. **Build to the brief.** Carry its tokens into code: colour strategy, type scale, padding rule (top 0, bottom 32), at most two CTAs, footer order.
7. **Verify. Every gate passes or the email is not done.**
   - Compile exits 0. MJML: `npx mjml in.mjml -o out.html --config.minify=true --config.validationLevel=strict`. Judge by exit code, never by the file existing.
   - `python3 scripts/check_email.py out.html` reports zero FAIL. Fix each WARN or name why it stays.
   - Screenshot the HTML at 600px and 375px wide and look at it. Fix moonscape gaps, broken stacking, unreadable contrast.
   - Plain-text version exists (React Email `render(..., { plainText: true })`; MJML: write it from the brief).
   - Pre-handoff checklist in `references/taste.md` has two or fewer misses; three or more means redraft.
8. **Deliver** source, compiled HTML, plain text, the brief, the checker output, and the screenshots. Sending, test sends, and ESP uploads wait for an explicit go.

## Brief schema

```json
{
  "name": "Campaign or template name",
  "subject": "<=45 chars, adds information",
  "preheader": "<=90 chars, never restates the subject",
  "archetype": "editorial | bold-mono | minimal-lux | founder-letter | punk-character | lookbook",
  "color_strategy": "restrained | committed | drenched",
  "primary_color": "#hex",
  "secondary_color": "#hex or null",
  "voice": ["concrete descriptors"],
  "build_path": "mjml | react-email",
  "structure": [
    { "kind": "header", "logo": true },
    { "kind": "hero", "image_slot": "hero" },
    { "kind": "headline", "content": "..." },
    { "kind": "body", "content": "..." },
    { "kind": "cta", "label": "names the destination", "url": "..." },
    { "kind": "footer" }
  ],
  "image_slots": [
    { "slot_id": "hero", "purpose": "what it must convey", "candidate_url": "url or null", "user_prompt": "ask if null" }
  ],
  "footer": {
    "mission_line": "verbatim from a real source, else null",
    "socials": [{ "name": "instagram", "url": "..." }],
    "physical_address": "one line",
    "unsubscribe": "{{unsubscribe_url}}"
  },
  "defaults_assumed": ["fields filled without user input"],
  "anti_slop_checks": ["what makes this one not generic"]
}
```

## Where the sources disagree (resolved)

- **Questions:** three at most, only for blocking gaps. Overrides React Email's ask-first list.
- **Black and white:** never pure `#000`/`#fff`. Tint neutrals toward the brand hue; dark-mode neutrals near `#121212` / `#F1F1F1`.
- **Dark mode:** MJML path ships `color-scheme` meta plus `prefers-color-scheme` overrides (Apple Mail and Outlook for Mac/iOS honour them; Gmail ignores them). React Email path skips `dark:` variants and relies on contrast that survives forced inversion.
- **Width:** 600px body. Minimal-lux narrows the content column to 472–520px inside it.
- **Dashes:** no em or en dashes in copy. The checker enforces it.

## Files

- `references/taste.md`: archetypes, visual laws, whitespace, copy, footer, pushback, checklist
- `references/mjml.md`: MJML 5 rules, gotchas, dark mode, compile and error recovery
- `references/react-email.md`: React Email rules and render commands
- `references/accessibility-compliance.md`: a11y priority list, CAN-SPAM/GDPR/CASL footer and header rules
- `assets/editorial.mjml`, `assets/bold-mono.mjml`: compile-clean starters
- `scripts/check_email.py`: stdlib lint for compiled HTML (`--json` for machine output)

Upstream sources and licenses: `CREDITS.md` at the repository root.
