#!/usr/bin/env python3
"""Check every outbound link in the site (or a candidate CSV) and write link_check.csv.

Contract (output CSV columns, all required):
  url, status (int HTTP code, or 0 on network error), final_url, verdict (OK|DEAD|FLAGGED),
  method (http|browser), note, checked_at (ISO date), pages (semicolon list of site pages using it)
Verdicts: OK = 2xx/3xx resolving to a real page; DEAD = 404/410/network error after one retry;
FLAGGED = anything else (403/429/999 bot blocks that a real browser also could not open,
sign-in walls, campus-only hosts). Loud failure: exits 1 and prints a FAILED banner if any
link is DEAD; FLAGGED links are listed at the top of the output but do not fail the run.
Usage: check_links.py SITE_DIR OUT_CSV
"""
import csv, datetime, re, sys, time, pathlib, urllib.request, urllib.error, urllib.parse, ssl

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/130.0.0.0 Safari/537.36")
# Hosts reachable only on the JHU network or VPN. The site labels these links "On campus or JH VPN only";
# the checker cannot reach them from outside, so they are FLAGGED (counted and listed), never OK or DEAD.
NETWORK_ONLY = {"portal.ai.jh.edu"}
WALL = ["just a moment...", "attention required! | cloudflare", "cf-browser-verification",
        "checking your browser before accessing", "id=\"challenge-form\""]

def collect(site):
    """Map each external URL to the site pages that link to it."""
    links = {}
    for f in sorted(pathlib.Path(site).glob("*.html")):
        for u in re.findall(r'href="(https?://[^"]+)"', f.read_text()):
            links.setdefault(u.replace("&amp;", "&"), set()).add(f.name)
    return links

def http_check(u):
    """Plain GET with a browser UA. Returns (status, final_url, body_snippet)."""
    req = urllib.request.Request(u, headers={"User-Agent": UA, "Accept": "text/html,*/*"})
    try:
        with urllib.request.urlopen(req, timeout=20, context=ssl.create_default_context()) as r:
            return r.status, r.geturl(), r.read(4000).decode("utf-8", "ignore")
    except urllib.error.HTTPError as e:
        return e.code, u, ""
    except Exception as e:
        return 0, u, f"ERR {type(e).__name__}: {e}"

def browser_check(urls):
    """Real-Chrome fallback for links a plain GET could not confirm."""
    out = {}
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        return {u: (None, u, "playwright not available") for u in urls}
    with sync_playwright() as pw:
        b = pw.chromium.launch(channel="chrome", headless=True,
                               args=["--disable-blink-features=AutomationControlled"])
        c = b.new_context(user_agent=UA)
        c.add_init_script("Object.defineProperty(navigator,'webdriver',{get:()=>undefined});")
        for u in urls:
            p = c.new_page()  # fresh tab per URL so one failed navigation cannot poison the next
            try:
                r = p.goto(u, wait_until="load", timeout=30000)
                p.wait_for_timeout(2000)
                html = p.content().lower()
                title = p.title()
                wall = any(m in html for m in WALL)
                out[u] = (r.status if r else None, p.url, ("BOT WALL " if wall else "") + "title=" + title[:80])
            except Exception as e:
                out[u] = (0, u, f"browser ERR {str(e).splitlines()[0][:120]}")
            finally:
                p.close()
        b.close()
    return out

def main():
    site, out_csv = sys.argv[1], sys.argv[2]
    links = collect(site)
    today = datetime.date.today().isoformat()
    rows, retry = {}, []
    for u in sorted(links):
        if urllib.parse.urlparse(u).hostname in NETWORK_ONLY:
            rows[u] = [u, 0, u, "FLAGGED", "skipped", "JHU network only (by design)", today]
            continue
        s, final, body = http_check(u)
        if s == 0:  # one retry on network error
            time.sleep(2); s, final, body = http_check(u)
        if 200 <= s < 400 and not any(m in body.lower() for m in WALL):
            rows[u] = [u, s, final, "OK", "http", "", today]
        else:
            retry.append(u); rows[u] = [u, s, final, "", "http", body[:80] if s == 0 else "", today]
    for u, (s, final, note) in browser_check(retry).items():
        s = s or 0
        title = note.split("title=")[-1].lower()
        if s and 200 <= s < 400 and "BOT WALL" not in note and "not found" not in title and "404" not in title:
            v = "OK"
        elif s in (404, 410) or "not found" in title or "404" in title or (s == 0 and rows[u][1] in (0, 404, 410)):
            v = "DEAD"
        else:
            v = "FLAGGED"
        rows[u] = [u, s, final, v, "browser", f"plain GET {rows[u][1]}; {note}", today]
    with open(out_csv, "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["url", "status", "final_url", "verdict", "method", "note", "checked_at", "pages"])
        for u in sorted(rows):
            w.writerow(rows[u] + [";".join(sorted(links[u]))])
    counts = {k: sum(1 for r in rows.values() if r[3] == k) for k in ("OK", "DEAD", "FLAGGED")}
    for k in ("DEAD", "FLAGGED"):
        for r in rows.values():
            if r[3] == k:
                print(f"{k}: {r[0]} status={r[1]} {r[5]} on {';'.join(sorted(links[r[0]]))}")
    print(f"TOTAL {len(rows)} OK {counts['OK']} DEAD {counts['DEAD']} FLAGGED {counts['FLAGGED']}")
    if counts["DEAD"]:
        print("=== FAILED: dead links present (see above) ===")
        sys.exit(1)

if __name__ == "__main__":
    main()
