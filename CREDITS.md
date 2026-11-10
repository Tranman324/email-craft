# Credits

email-craft is an amalgamation. It cherry-picks the design-taste layer from one skill, the cross-client build layer from two others, and the accessibility and compliance floor from a fourth, then resolves where they disagree and adds a lint gate and tested starters.

Every adapted source below is MIT licensed. Their copyright and permission notices are reproduced in `LICENSES/`, as MIT requires. Text was condensed and rewritten, not copied wholesale; the ideas and much of the structure are theirs.

## Adapted (MIT)

- **CosmoBlk/email-design** by George Hartley. https://github.com/CosmoBlk/email-design
  - Taken: the six archetypes, colour strategies (restrained / committed / drenched), category-reflex check, whitespace and "moonscape" rules, imagery sourcing order, footer order with the never-invent-a-mission rule, the JSON brief, pushback patterns, pre-handoff checklist.
  - Lives in: `email-craft/references/taste.md`, brief schema and workflow steps 1–4 in `email-craft/SKILL.md`.
  - License: `LICENSES/CosmoBlk-email-design.txt`

- **framix-team/skill-email-html-mjml** by Framix. https://github.com/framix-team/skill-email-html-mjml
  - Taken: MJML 5 engineering rules, Outlook/Gmail/stacking gotchas, the silent `mj-include` trap, templating-tag protection, heading roles via `mj-html-attributes`, the dark-mode pattern, compile flags and exit-code discipline.
  - Lives in: `email-craft/references/mjml.md`
  - License: `LICENSES/framix-skill-email-html-mjml.txt`

- **resend/resend-skills**, `react-email` skill, by Resend. https://github.com/resend/resend-skills/tree/main/skills/react-email
  - Taken: React Email structure, `pixelBasedPreset`, no flex/grid/`dark:`, `box-border` and border-style rules, static asset pattern, render and plain-text commands.
  - Lives in: `email-craft/references/react-email.md`
  - License: `LICENSES/resend-resend-skills.txt`
  - Upstream project: React Email, https://github.com/resend/react-email (MIT, Plus Five Five, Inc.)

- **resend/resend-skills**, `email-best-practices` skill, by Resend. https://github.com/resend/resend-skills/tree/main/skills/email-best-practices
  - Taken: accessibility severity order and checklist, CAN-SPAM / GDPR / CASL requirements, `List-Unsubscribe` one-click headers, marketing consent rules.
  - Lives in: `email-craft/references/accessibility-compliance.md`
  - License: `LICENSES/resend-resend-skills.txt` (the standalone https://github.com/resend/email-best-practices repo carries no license file; we used the MIT copy bundled in resend-skills)

## Referenced, not copied

- **CosmoBlk/bestemaildesigns**, "47 Best Email Designs of 2026". https://github.com/CosmoBlk/bestemaildesigns (no license file, so linked only; recommended as a reference when picking an archetype)
- **MJML** https://mjml.io and **React Email** https://react.email, the frameworks this skill drives
- **Can I email** https://www.caniemail.com, client CSS support data
- **Good Email Code** by Mark Robbins, https://www.goodemailcode.com, accessible email patterns
- Inspiration galleries: Really Good Emails https://reallygoodemails.com, Email Love https://emaillove.com, Milled https://milled.com

## Original to email-craft

- Conflict resolutions between the sources (questions cap, no pure black/white, dark-mode split by build path, dash rule)
- `scripts/check_email.py` lint gate and its tests
- `assets/editorial.mjml` and `assets/bold-mono.mjml` starters, compile-tested on MJML 5.4.1 and render-checked at 600px, 375px, and dark mode
- The MJML 5 dark-mode body-background gotcha (`.dm-bg > div`), found by rendering
