#!/usr/bin/env python3
"""Tests for check_email.py. Run: python3 scripts/test_check_email.py"""
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from check_email import check  # noqa: E402

GOOD = """<!doctype html><html lang="en" dir="ltr"><head><title>Your winter kit list</title></head>
<body><div style="display:none;font-size:1px;color:#ffffff">Three layers that matter</div>
<table role="presentation"><tr><td>
<h1>Winter kit</h1><p>Wind matters more than cold.</p>
<img src="https://cdn.example.com/a.jpg" alt="Runner on a ridge">
<a href="https://example.com/kit" style="display:inline-block;padding:16px">See the winter kit</a>
<p>Northbound, 120 Ridge Road, Bend, OR 97701</p>
<a href="{{unsubscribe_url}}">Unsubscribe</a>
</td></tr></table></body></html>"""

BAD = """<html><head></head><body style="background:#ffffff">
<table><tr><td>
<p>Big news \u2014 we launched.</p>
<img src="hero.webp">
<a href="https://example.com"><img src="https://cdn.example.com/b.png" alt=""></a>
<a href="https://example.com/1" style="display:inline-block;padding:10px">Click here</a>
<a href="https://example.com/2" style="display:inline-block;padding:10px">Buy one</a>
<a href="https://example.com/3" style="display:inline-block;padding:10px">Buy two</a>
<p style="font-size:10px">tiny</p>
</td></tr></table></body></html>"""


def run(html, **kw):
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, encoding="utf-8") as f:
        f.write(html)
        path = f.name
    try:
        return check(path, **kw)
    finally:
        os.unlink(path)


def rules(results, level):
    return {r["rule"] for r in results if r["level"] == level}


class CheckEmailTest(unittest.TestCase):
    def test_good_passes_clean(self):
        res = run(GOOD, transactional=False)
        self.assertEqual(rules(res, "FAIL"), set(), res)
        self.assertEqual(rules(res, "WARN"), set(), res)

    def test_bad_fails_every_gate(self):
        res = run(BAD, transactional=False)
        self.assertTrue({"lang", "title", "alt", "alt-linked", "image-format", "dashes", "unsubscribe"} <= rules(res, "FAIL"), res)
        self.assertTrue({"preheader", "link-text", "cta-count", "table-role", "h1", "pure-bw", "font-size", "address", "image-url"} <= rules(res, "WARN"), res)

    def test_transactional_skips_footer_gates(self):
        res = run(BAD, transactional=True)
        self.assertNotIn("unsubscribe", rules(res, "FAIL"))
        self.assertNotIn("address", rules(res, "WARN"))

    def test_hidden_preheader_white_not_flagged(self):
        res = run(GOOD, transactional=False)
        self.assertNotIn("pure-bw", rules(res, "WARN"))
        self.assertNotIn("font-size", rules(res, "WARN"))

    def test_size_clip(self):
        big = GOOD.replace("<p>Wind", "<p>" + "x" * (103 * 1024) + " Wind")
        self.assertIn("size", rules(run(big, transactional=False), "FAIL"))


if __name__ == "__main__":
    unittest.main(verbosity=2)
