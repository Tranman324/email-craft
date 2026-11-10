# email-craft

An agent skill for email templates that look like a brand made them and render like an engineer built them.

Most email skills do one half. Design skills write a nice brief and hand off to whatever the ESP spits out. HTML skills produce bulletproof tables with a generic look. email-craft does both in one pass: commit to a design brief, build it in MJML or React Email, then prove it with a compile, a lint gate, and a render.

## What it does

1. **Brief first.** Reads the brand, asks at most three questions, commits to one of six archetypes (editorial, bold mono, minimal lux, founder letter, punk/character, lookbook) and a colour strategy.
2. **Build second.** MJML 5 for ESP-pasted HTML, React Email for apps that send from code.
3. **Proof last.** Strict compile, `check_email.py` (size clip, alt text, lang, title, preheader, link text, CTA count, dashes, pure black/white, unsubscribe, address), and screenshots at desktop, mobile, and dark mode.

## Install

Claude Code:

```bash
git clone https://github.com/Tranman324/email-craft.git
cp -r email-craft/email-craft ~/.claude/skills/email-craft
```

Anything that reads `SKILL.md` folders (Hermes, Codex, Cursor) works the same way: point it at the `email-craft/` subfolder.

## Use the checker on any email

```bash
python3 email-craft/scripts/check_email.py path/to/email.html          # human output
python3 email-craft/scripts/check_email.py path/to/email.html --json   # machine output
python3 email-craft/scripts/check_email.py receipt.html --transactional
python3 email-craft/scripts/test_check_email.py                        # tests
```

Exit code 0 = no FAIL, 1 = at least one FAIL.

## Starters

```bash
npm install -D mjml
npx mjml email-craft/assets/editorial.mjml -o editorial.html --config.minify=true --config.validationLevel=strict
```

Both starters compile clean on MJML 5.4.1 and pass the checker with zero warnings. All copy, brands, and image URLs in them are placeholders.

## Credits

Built from four MIT-licensed skills by George Hartley (CosmoBlk), Framix, and Resend. Full attribution, what came from where, and the license texts: [CREDITS.md](CREDITS.md) and [LICENSES/](LICENSES/).

## License

MIT. See [LICENSE](LICENSE).
