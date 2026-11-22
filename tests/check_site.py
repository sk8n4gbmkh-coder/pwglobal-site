"""Control gate for the site: build dist/ and check that all language versions are consistent.

Run: python3 tests/check_site.py   (exit code 0 = pass)
"""
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DIST = os.path.join(ROOT, "dist")
PAGES = {"en": "index.html", "uk": "ua/index.html", "et": "et/index.html"}
errors = []


def check(cond, msg):
    if not cond:
        errors.append(msg)


# Gate 1: build succeeds (build.py itself fails on a missing translation or ET/UA count mismatch)
r = subprocess.run([sys.executable, os.path.join(ROOT, "build.py")], cwd=ROOT, capture_output=True, text=True)
check(r.returncode == 0, f"build failed: {r.stdout}{r.stderr}".strip())

if not errors:
    html = {}
    for lang, path in PAGES.items():
        full = os.path.join(DIST, path)
        check(os.path.exists(full), f"missing page {path}")
        if os.path.exists(full):
            html[lang] = open(full, encoding="utf-8").read()

    sections = {}
    for lang, h in html.items():
        # Gate 2: correct html lang
        check(f'<html lang="{lang}">' in h, f"{PAGES[lang]}: wrong <html lang>")
        # Gate 3: every in-page link points to an existing id (no dead menu links)
        ids = set(re.findall(r'id="([^"]+)"', h))
        for target in set(re.findall(r'href="#([^"]+)"', h)):
            check(target in ids, f"{PAGES[lang]}: link #{target} has no matching section")
        # Gate 4: quote form still wired to Netlify Forms
        check('data-netlify="true"' in h and 'name="quote"' in h, f"{PAGES[lang]}: quote form missing Netlify attributes")
        # Gate 5: language switch links to the other versions
        others = [l for l in PAGES if l != lang]
        for o in others:
            check(f'hreflang="{o}"' in h, f"{PAGES[lang]}: no link to {o} version")
        sections[lang] = re.findall(r'<section[^>]*id="([^"]+)"', h)
        # Gate 5b: every local image exists in dist/ (absolute /img/... paths, UA/ET live in subfolders)
        for src in re.findall(r'<img[^>]+src="([^"]+)"', h):
            if not src.startswith("http"):
                check(src.startswith("/"), f"{PAGES[lang]}: image {src} must use an absolute path")
                check(os.path.exists(os.path.join(DIST, src.lstrip("/"))), f"{PAGES[lang]}: image {src} missing in dist/")
        # Gate 5c (negative): old SVG line-up gone, hero has 3 photos
        check('id="lineup"' not in h, f"{PAGES[lang]}: old SVG line-up still present")
        check(len(re.findall(r'<img[^>]+data-cap=', h)) == 3, f"{PAGES[lang]}: hero should have 3 photos")
        # Gate 5d: stock table = 15 rows (spec 002), every colour key has a label; no old "black/white matt"
        m = re.search(r"const cans=\[(.*?)\n  \];", h, re.S)
        rows = re.findall(r'\["[^"]+","([a-z]+)"', m.group(1)) if m else []
        check(len(rows) == 15, f"{PAGES[lang]}: stock table has {len(rows)} rows, expected 15")
        for key in set(rows):
            check(re.search(rf'const T=\{{[^}}]*\b{key}:"', h) is not None, f"{PAGES[lang]}: colour '{key}' has no label in T")
        check("bwmatt" not in h, f"{PAGES[lang]}: old bwmatt colour still present")

    # Gate 6: all languages have the same sections in the same order
    if "en" in sections:
        for lang, s in sections.items():
            check(s == sections["en"], f"{PAGES[lang]}: sections {s} differ from EN {sections['en']}")

    # Gate 7: every sitemap URL has a built file
    sm = open(os.path.join(DIST, "sitemap.xml"), encoding="utf-8").read()
    for loc in re.findall(r"<loc>https://[^/]+(/[^<]*)</loc>", sm):
        f = loc.lstrip("/") or "index.html"
        if f.endswith("/"):
            f += "index.html"
        check(os.path.exists(os.path.join(DIST, f)), f"sitemap entry {loc} has no file")

if errors:
    print("FAIL")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print("PASS: build, 3 languages, links, form, language switch, sections, sitemap")
