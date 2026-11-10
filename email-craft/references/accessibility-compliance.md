# Accessibility and compliance

Adapted from the `email-best-practices` skill in resend/resend-skills (MIT, Resend): accessibility.md, compliance.md, marketing-emails.md. Condensed. Not legal advice. See CREDITS.md.

## Accessibility, fix in this order

1. **Critical: alt text.** Every `<img>` has `alt`. Meaningful images: purpose plus key detail. Decorative: `alt=""` (omitting it is not the same; some readers announce the filename). Linked images are never decorative: alt names the destination.
2. **Serious:**
   - `lang` and `dir` on `<html>` and on the direct children of `<body>` (clients strip the `<html>` copy). MJML does this from the `<mjml>` tag.
   - Layout tables carry `role="presentation"`. Real data tables keep table semantics and use `<th scope="col">`.
   - Every link has discernible text.
   - `<title>` set and specific to this email (subject-like), not the brand name.
   - Contrast 4.5:1 for body and links, 3:1 for large text. Never colour alone for meaning.
3. **Moderate:** link text names the destination. Never "click here", "learn more", "read more", or a bare URL.
4. **Mild:** one `<h1>`, subheadings nested in order. One- or two-sentence notices may skip headings.

Also: send a plain-text alternative; no text inside images; footer text no smaller than 12px.

Testing: automated checks are a floor (Parcel accessibility checker, WebAIM contrast checker), then a dark-mode preview in Apple Mail, Outlook, and Gmail mobile. Visually hidden link text pattern: https://www.goodemailcode.com/email-accessibility/visually-hidden-text

## Compliance, every marketing email

- Accurate From / Reply-To; subject line not deceptive.
- Physical mailing address in the footer (CAN-SPAM).
- Visible unsubscribe in the body. Preferences may sit beside it, never replace it.
- Bulk senders (Gmail, Yahoo, Microsoft requirement) also send headers:
  - `List-Unsubscribe: <https://example.com/unsubscribe?u=...>`
  - `List-Unsubscribe-Post: List-Unsubscribe=One-Click`
  - The endpoint accepts POST (returns 200/202) and stops mail within 48 hours.
- Opt-out timing: CAN-SPAM 10 business days; GDPR immediately; CASL 10 business days and the link must work 60 days after send.
- Consent: explicit opt-in for GDPR/CASL; no pre-checked boxes, no bought lists. Double opt-in recommended (required in practice in Germany).
- Transactional emails (receipts, resets) can go without marketing consent if they stay non-promotional.
