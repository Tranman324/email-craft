#!/usr/bin/env python3
"""Lint a compiled HTML email against email-craft's gates. Stdlib only.

Usage: check_email.py FILE.html [--json] [--transactional]
Exit 0 when no FAIL, 1 when any FAIL, 2 on usage or read error.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from html.parser import HTMLParser

GMAIL_CLIP = 102 * 1024
SIZE_WARN = 90 * 1024
VAGUE_LINKS = {"click here", "here", "learn more", "read more", "more", "click", "this link"}
DASHES = re.compile("[\u2014\u2013]")
PURE_BW = re.compile(r"#(?:000000|ffffff|000|fff)\b", re.I)
VOID = {"area", "base", "br", "col", "embed", "hr", "img", "input", "link", "meta", "source", "track", "wbr"}


class Email(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.html_attrs: dict = {}
        self.title = ""
        self.in_title = False
        self.stack: list[tuple[str, dict]] = []
        self.skip_depth = 0  # inside <style>/<script>/<head> text
        self.imgs: list[dict] = []
        self.links: list[dict] = []
        self.link_stack: list[dict] = []
        self.tables: list[dict] = []
        self.table_stack: list[dict] = []
        self.text_chunks: list[str] = []
        self.hidden_text: list[str] = []
        self.hidden_depth = 0
        self.h1 = 0
        self.headings: list[int] = []
        self.style_blobs: list[str] = []
        self.in_style = False
        self.small_fonts: set[str] = set()

    def handle_starttag(self, tag, attrs_list):
        a = {k.lower(): (v or "") for k, v in attrs_list}
        style = a.get("style", "")
        hidden = bool(re.search(r"display\s*:\s*none", style, re.I))
        # Hidden preheader blocks use 1px white text by design; skip their styles.
        fs = None
        if style and not (hidden or self.hidden_depth):
            self.style_blobs.append(style)
            m = re.search(r"font-size\s*:\s*(\d+(?:\.\d+)?)px", style)
            if m:
                fs = float(m.group(1))
        for k in ("bgcolor", "color"):
            if a.get(k):
                self.style_blobs.append(f"{k}:{a[k]}")
        if tag == "html":
            self.html_attrs = a
        elif tag == "title":
            self.in_title = True
        elif tag in ("style", "script"):
            self.in_style = tag == "style"
            self.skip_depth += 1
        elif tag == "img":
            a["_linked"] = bool(self.link_stack)
            self.imgs.append(a)
            for lk in self.link_stack:
                lk["imgs"].append(a)
        elif tag == "a":
            lk = {"href": a.get("href", ""), "text": "", "imgs": [], "style": style}
            self.links.append(lk)
            self.link_stack.append(lk)
        elif tag == "table":
            t = {"role": a.get("role", ""), "th": False}
            self.tables.append(t)
            self.table_stack.append(t)
        elif tag == "th" and self.table_stack:
            self.table_stack[-1]["th"] = True
        elif re.fullmatch(r"h[1-6]", tag):
            lvl = int(tag[1])
            self.headings.append(lvl)
            self.h1 += lvl == 1
        if a.get("role") == "heading" and a.get("aria-level", "").isdigit():
            lvl = int(a["aria-level"])
            self.headings.append(lvl)
            self.h1 += lvl == 1
        if tag not in VOID:
            self.stack.append((tag, {"hidden": hidden, "fs": fs}))
            if hidden:
                self.hidden_depth += 1

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False
        elif tag in ("style", "script"):
            self.skip_depth = max(0, self.skip_depth - 1)
            self.in_style = False
        elif tag == "a" and self.link_stack:
            self.link_stack.pop()
        elif tag == "table" and self.table_stack:
            self.table_stack.pop()
        # pop to the matching tag (tolerate sloppy markup)
        for i in range(len(self.stack) - 1, -1, -1):
            if self.stack[i][0] == tag:
                for _, meta in self.stack[i:]:
                    if meta["hidden"]:
                        self.hidden_depth -= 1
                del self.stack[i:]
                break

    def handle_data(self, data):
        if self.in_title:
            self.title += data
            return
        if self.skip_depth:
            if self.in_style:
                self.style_blobs.append(data)
            return
        for lk in self.link_stack:
            lk["text"] += data
        if self.hidden_depth:
            self.hidden_text.append(data)
        else:
            self.text_chunks.append(data)
            if data.strip():
                # Nearest ancestor font-size governs this text (dividers carry 1px with no text).
                fs = next((m["fs"] for _, m in reversed(self.stack) if m["fs"] is not None), None)
                if fs is not None and 0 < fs < 12:
                    self.small_fonts.add(f"{fs:g}px")

    def handle_comment(self, data):
        pass  # MSO conditionals hold VML duplicates; ignore


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def check(path: str, transactional: bool) -> list[dict]:
    with open(path, "rb") as fh:
        raw = fh.read()
    html = raw.decode("utf-8", errors="replace")
    p = Email()
    p.feed(html)
    out: list[dict] = []

    def add(level: str, rule: str, msg: str):
        out.append({"level": level, "rule": rule, "msg": msg})

    size = len(raw)
    if size > GMAIL_CLIP:
        add("FAIL", "size", f"{size/1024:.1f}KB exceeds Gmail's 102KB clip; minify or cut content")
    elif size > SIZE_WARN:
        add("WARN", "size", f"{size/1024:.1f}KB is close to Gmail's 102KB clip")

    if not p.html_attrs.get("lang"):
        add("FAIL", "lang", "<html> has no lang attribute")
    if not p.html_attrs.get("dir"):
        add("WARN", "dir", "<html> has no dir attribute")
    if not norm(p.title):
        add("FAIL", "title", "<title> missing or empty")

    if not norm(" ".join(p.hidden_text)):
        add("WARN", "preheader", "no hidden preheader text found (mj-preview / <Preview>)")

    for img in p.imgs:
        src = img.get("src", "")
        short = src[-60:] or "(no src)"
        if "alt" not in img:
            add("FAIL", "alt", f"image without alt attribute: {short}")
        elif img["_linked"] and not img["alt"].strip():
            add("FAIL", "alt-linked", f"linked image has empty alt; name the destination: {short}")
        if re.search(r"\.(svg|webp)(\?|#|$)", src, re.I):
            add("FAIL", "image-format", f"SVG/WEBP renders poorly in email clients: {short}")
        if src and not re.match(r"(https?:)?//|cid:|\{\{|\[\[|%%|\*\|", src):
            add("WARN", "image-url", f"image src is not an absolute URL: {short}")

    ctas = 0
    for lk in p.links:
        text = norm(lk["text"]).lower().rstrip(".!→> ")
        has_img_name = any(i.get("alt", "").strip() for i in lk["imgs"])
        if not text and not has_img_name:
            add("FAIL", "link-name", f"link has no discernible text: {lk['href'][:60]}")
        elif text in VAGUE_LINKS:
            add("WARN", "link-text", f'vague link text "{text}"; name the destination')
        elif re.fullmatch(r"(https?://|www\.)\S+", text):
            add("WARN", "link-text", f"bare URL as link text: {text[:60]}")
        st = lk["style"].lower()
        if "display:inline-block" in st.replace(" ", "") and "padding" in st and "unsubscribe" not in text:
            ctas += 1
    if ctas > 2:
        add("WARN", "cta-count", f"{ctas} button-style CTAs; two is the ceiling")

    layout_no_role = sum(1 for t in p.tables if not t["th"] and t["role"] not in ("presentation", "none"))
    if layout_no_role:
        add("WARN", "table-role", f'{layout_no_role} layout table(s) without role="presentation"')

    if p.h1 == 0:
        add("WARN", "h1", "no h1 (fine only for one- or two-sentence notices)")
    elif p.h1 > 1:
        add("WARN", "h1", f"{p.h1} h1 headings; use one")
    for prev, cur in zip(p.headings, p.headings[1:]):
        if cur > prev + 1:
            add("WARN", "heading-order", f"heading jumps from h{prev} to h{cur}")
            break

    visible = norm(" ".join(p.text_chunks + p.hidden_text + [p.title]))
    dashes = DASHES.findall(visible)
    if dashes:
        i = DASHES.search(visible).start()
        add("FAIL", "dashes", f'{len(dashes)} em/en dash(es) in copy, e.g. "...{visible[max(0,i-30):i+30]}..."')
    if re.search(r"\s--\s", visible):
        add("FAIL", "dashes", "double-hyphen used as a dash in copy")

    styles = " ".join(p.style_blobs)
    bw = sorted({m.group(0).lower() for m in PURE_BW.finditer(styles)})
    if bw:
        add("WARN", "pure-bw", f"pure black/white in styles ({', '.join(bw)}); tint toward the brand hue")
    if re.search(r"display\s*:\s*(flex|grid)", styles, re.I):
        add("WARN", "layout-css", "flex/grid in styles; most clients ignore it, use tables/columns")
    widths = [int(w) for w in re.findall(r"max-width\s*:\s*(\d+)px", styles)]
    if widths and max(widths) > 640:
        add("WARN", "width", f"container max-width {max(widths)}px; keep the body at 600px")
    if p.small_fonts:
        add("WARN", "font-size", f"text below 12px: {', '.join(sorted(p.small_fonts))}")

    if not transactional:
        has_unsub = any("unsubscribe" in (norm(l["text"]).lower() + l["href"].lower()) for l in p.links)
        if not has_unsub:
            add("FAIL", "unsubscribe", 'no visible "Unsubscribe" link (pass --transactional for receipts/resets)')
        if not re.search(r"\d{3,}.*\b(st|street|ave|avenue|rd|road|blvd|suite|ste|po box|lane|ln|dr|drive|way)\b|\b\d{5}(-\d{4})?\b",
                         visible, re.I):
            add("WARN", "address", "no physical mailing address detected in copy (CAN-SPAM)")

    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("file")
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--transactional", action="store_true", help="skip marketing footer checks")
    args = ap.parse_args()
    try:
        results = check(args.file, args.transactional)
    except OSError as e:
        print(f"error: {e}", file=sys.stderr)
        return 2
    fails = sum(r["level"] == "FAIL" for r in results)
    warns = sum(r["level"] == "WARN" for r in results)
    if args.json:
        print(json.dumps({"file": args.file, "fail": fails, "warn": warns, "results": results}, indent=2))
    else:
        for r in results:
            print(f"{r['level']:4}  {r['rule']:<14} {r['msg']}")
        print(f"\n{fails} FAIL, {warns} WARN  ({'PASS' if not fails else 'NOT READY'})")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
