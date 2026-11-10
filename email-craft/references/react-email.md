# React Email build path

Adapted from the `react-email` skill in resend/resend-skills (MIT, Resend). Condensed. See CREDITS.md. Docs: https://react.email/docs/llms.txt

Use when the app is already React/TypeScript and sends from code. Otherwise use MJML.

## Setup

- `npm i react-email` (components, `render`, `Tailwind`, `pixelBasedPreset` all import from `react-email`).
- New project: `npx create-email@latest`. Existing: add `"email": "email dev --dir emails --port 3000"` to scripts.
- Local images in `emails/static/`. Production images need an absolute CDN URL: `const base = process.env.NODE_ENV === "production" ? "https://cdn.example.com" : ""`. Ask for the host; never hardcode localhost.

## Structure

```tsx
<Html lang="en" dir="ltr">
  <Tailwind config={brandConfig}>
    <Head />
    <Body className="bg-[#F4F1EC] font-sans">
      <Preview>Preheader text, first inside Body</Preview>
      <Container className="mx-auto max-w-[600px]">
        {/* Sections, Row/Column, Heading as="h1", Text, Button, Img, Hr */}
      </Container>
    </Body>
  </Tailwind>
</Html>
```

- `<Head />` sits inside `<Tailwind>`. `<Preview>` is the first child of `<Body>` (it also emits `<title>`).
- `Container` once per email; `Section` for blocks; `Row`/`Column` for columns.
- Brand tokens in one shared `emails/tailwind.config.ts` (`satisfies TailwindConfig`, `presets: [pixelBasedPreset]`). Templates use semantic names (`bg-brand-primary`), never hardcoded hex.
- Typed props interface plus `.PreviewProps` containing only props the component uses.

## Hard rules

- `pixelBasedPreset` always; clients don't support `rem`.
- No flexbox or grid; use `Row`/`Column`.
- No responsive prefixes (`sm:`, `md:`) and no `dark:` / `light:` variants; they don't inline.
- PNG or JPG only. Never generate SVG.
- `Button` always carries `box-border`. Every border names its style (`border-solid`); single-side borders reset first (`border-none border-l border-solid`).
- Known-size images (logos, icons) get fixed width/height; content images `w-full h-auto`.
- Never write `{{var}}` in JSX. If an ESP needs mustache placeholders, put them only in `PreviewProps` values.
- When iterating, change only what was asked.

## Render

```tsx
import { render } from "react-email";
const html = await render(<Welcome {...props} />);
const text = await render(<Welcome {...props} />, { plainText: true });
```

Static export for the checker: `npx email export --dir emails --outDir out`. Then run `scripts/check_email.py out/<name>.html`.

## Accessibility defaults it gives you

`<Html>` sets `lang`/`dir`; `<Img>` defaults `alt=""`; `<Preview>` emits `<title>`. You still own: one `<Heading as="h1">`, ordered subheadings, descriptive alt on meaningful and linked images, destination-naming link text, contrast. See `accessibility-compliance.md`.
