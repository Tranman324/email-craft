# MJML 5 build path

Adapted from framix-team/skill-email-html-mjml (MIT, Framix). Condensed; behaviours re-checked against MJML 5.4.1 where noted. See CREDITS.md. Full component docs: https://documentation.mjml.io

## Setup

- Node 20+. Install per project: `npm install -D mjml` (pin `^5.4.0`). Never `npm install -g`.
- Run with `npx mjml` or `./node_modules/.bin/mjml`.

## Compile

```bash
npx mjml in.mjml -o out.html --config.minify=true --config.validationLevel=strict
```

- `minify` is mandatory: Gmail clips anything over 102KB.
- The output directory must already exist.
- **Exit code is the only proof.** A failed recompile leaves the previous good `.html` in place, so a stale file looks like success. Check `$?`.
- On error: read the reported line, fix, recompile once, then report.

## Engineering rules

1. All visible content lives in `mj-column` inside `mj-section`. Sections never nest (use `mj-wrapper` to group them).
2. Body width 600px. `mj-group` keeps side-by-side items (social rows, logo rows) from stacking on mobile. Use `gutter` on `mj-section` for column spacing, not padding tricks.
3. Web fonts via `mj-font` (MJML hides `@font-face` from Outlook), always with a fallback stack.
4. Critical styles as component attributes (`color`, `font-size`, `padding`), not classes; Gmail can strip classes. Custom CSS that must survive goes in `<mj-style inline="inline">`.
5. Global defaults in `<mj-attributes>` (`mj-all`, per-component defaults, `mj-class`) instead of repeating inline styles. This is also where the brief's tokens live.
6. Full-bleed heroes: `mj-hero`, or `mj-section` with `background-url` plus `background-size` and a fallback `background-color`. Outlook gets VML backgrounds only on these two.
7. Skip `mj-accordion` and `mj-carousel`; client support is too thin. No JavaScript anywhere; it is blocked in every client.
8. Always set `<mj-title>`, `<mj-preview>`, and `lang` + `dir` on `<mjml>`. MJML copies them onto the body wrapper div (`role="article"`, `aria-label`).

## Gotchas

- **Vertical align:** if one column in a section sets `vertical-align`, every column in that section must set it.
- **Outlook backgrounds:** keyword positions only (`top`, `center`, `bottom`). Pair `background-repeat="no-repeat"` with an explicit `background-size`.
- **Heading roles:** `role` / `aria-level` directly on `mj-text` fail strict validation. Use `mj-html-attributes`:

```xml
<mj-html-attributes>
  <mj-selector path=".email-h1 div">
    <mj-html-attribute name="role">heading</mj-html-attribute>
    <mj-html-attribute name="aria-level">1</mj-html-attribute>
  </mj-selector>
</mj-html-attributes>
<!-- then -->
<mj-text css-class="email-h1">Headline</mj-text>
```

- **Includes are off by default in MJML 5.** `mj-include` is silently dropped unless you pass `--config.allowIncludes true` (plus `--config.includePath <dir>` for partials outside the template folder). Strict validation still exits 0 when an include drops. After compiling, grep the HTML for a plain-text string from the partial.
- **Templating tags:** plain `{{name}}` passes through text, attributes, `mj-title`, and `mj-preview` untouched. Block tags containing `<` or `>` (`{% if x < 5 %}`) need `<!-- htmlmin:ignore -->` around them or minify mangles them silently. Keep templating tags out of `<mj-style>`; inside CSS they fail the minified build. Put `mj-raw` between sections, never between content components in a column.
- **`mj-hero`** rejects `container-background-color` under strict validation in MJML 5.
- **Stacking:** MJML 5's minifier leaves single spaces between inline-block columns; the `font-size:0px` MJML puts on the parent cell is what prevents gaps. For v4-style stripping: `--config.minifyOptions '{"collapseWhitespace":"all"}'` (JSON string form only).
- **Random IDs:** `mj-navbar`, `mj-accordion`, `mj-carousel` emit new IDs each compile; don't diff them as real changes.

## Dark mode pattern

```xml
<mj-head>
  <mj-raw>
    <meta name="color-scheme" content="light dark">
    <meta name="supported-color-schemes" content="light dark">
  </mj-raw>
  <mj-style inline="inline">.logo-dark { display: none !important; }</mj-style>
  <mj-style>
    @media (prefers-color-scheme: dark) {
      .logo-light { display: none !important; }
      .logo-dark { display: block !important; }
      .dm-bg, .dm-bg > div { background-color: #121212 !important; }
      .dm-text div { color: #F1F1F1 !important; }
    }
  </mj-style>
</mj-head>
```

- **MJML 5 paints `mj-body background-color` twice:** on `<body>` (where `mj-body css-class="dm-bg"` lands) and on the inner wrapper `<div>`. Override both (`.dm-bg, .dm-bg > div`) or the page stays light while the text turns light. Verified on MJML 5.4.1 by rendering with `prefers-color-scheme: dark`.
- Inline link colours need their own class (`<a class="dm-link" style="color:...">`) plus a dark override, or footer links vanish on the dark ground.

Apple Mail and Outlook for Mac/iOS honour it. Gmail ignores it and may force-invert; healthy light-mode contrast is the real defence.

## Translating the brief

- Colour strategy → `mj-body background-color` and section backgrounds. Drenched: the section and wrapper share `primary_color`. Restrained: tinted neutral body, accent on CTA and one rule line only.
- Type scale → `mj-class` entries (`h1`, `h2`, `body`, `meta`) in `mj-attributes`.
- Padding rule → `mj-section padding="0"`, content `padding="0 32px 32px"`; hero `padding="0"`.
- Footer → its own `mj-section` with a smaller `mj-class`; `mj-social` renders as one horizontal row by default, so it needs no `mj-group`.
- Deliver `<type>.mjml` and `<type>.html`, named for the email type.
