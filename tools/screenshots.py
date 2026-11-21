#!/usr/bin/env python3
"""Screenshot every page at desktop (1280px) and phone (390px) widths, full page.
Also reports horizontal overflow (scrollWidth > viewport) per page, which fails the phone-width rule.
Usage: screenshots.py BASE_URL OUT_DIR   (e.g. http://localhost:8765/ screenshots/)"""
import sys, pathlib
from playwright.sync_api import sync_playwright
PAGES = ["index","schedule","sign-up","entry","mid","advanced","licenses","data-rules",
         "locations","help","ai-at-jhu","resources","404"]
base, out = sys.argv[1], pathlib.Path(sys.argv[2]); out.mkdir(exist_ok=True)
bad = []
with sync_playwright() as pw:
    b = pw.chromium.launch()
    for label, w, h in (("desktop", 1280, 900), ("phone", 390, 844)):
        p = b.new_page(viewport={"width": w, "height": h})
        for name in PAGES:
            r = p.goto(f"{base}{name}.html", wait_until="load")
            if not r or r.status != 200:
                bad.append(f"{name} HTTP {r.status if r else None}"); continue
            sw = p.evaluate("()=>document.documentElement.scrollWidth")
            if sw > w: bad.append(f"{label} {name}: horizontal overflow {sw}px > {w}px")
            p.screenshot(path=str(out / f"{name}-{label}.png"), full_page=True)
    b.close()
print("\n".join(bad) if bad else "no overflow, all pages 200")
sys.exit(1 if bad else 0)
