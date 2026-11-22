# Faculty AI Hub (pilot)

## What this is

A pilot website. It is not official. It is the self-service training and one-stop hub for faculty AI at
Johns Hopkins, run by the DSAI Center for AI and Disciplinary Practice.

Live site: https://proflouishyman.github.io/dsai-ai-hub/

Designer: Louis Hyman (site designer).

## File layout

- `index.html`, `schedule.html`, `sign-up.html`: home, dates, and how to join.
- `entry.html`, `mid.html`, `advanced.html`: the three tier pages.
- `licenses.html`, `data-rules.html`, `locations.html`, `help.html`: access, rules, places, support.
- `ai-at-jhu.html`, `resources.html`: directories of outside links.
- `404.html`: the page-not-found page.
- `css/site.css`: the only stylesheet.
- `fonts/`: self-hosted Work Sans and Source Serif 4, with their licenses.
- `tools/`: `check_links.py` and `screenshots.py`.
- `DESIGN_NOTES.md`: colors, fonts and sources.
- `.nojekyll`: tells GitHub Pages to serve the files as they are.

There is no build step and no JavaScript. All links between pages are relative.

## How to update

1. Edit the HTML files directly.
2. The header, nav and footer are repeated in every page. Change all pages when you change one.
3. Keep "Coming soon" until a fact is settled. Never guess a room, time, form or address.
4. Before each term, run `python3 tools/check_links.py . link_check.csv` and fix any DEAD link.
5. To preview, run `python3 -m http.server 8765`. Then run `python3 tools/screenshots.py http://localhost:8765/ screenshots/`.

## Privacy rules

Do not put these on the site: names of people, email addresses, phone numbers, prices, or internal plans.
Check the diff and the commit message before every push.

## Moving to a JHU site later

1. Copy the files as they are. They are plain HTML, CSS and fonts, with relative links.
2. Switch the fonts to the University Communications-hosted files.
3. Add an official logo only with University Communications' approval.
4. Remove the pilot tag.
5. Keep `404.html`.

## Design notes

See `DESIGN_NOTES.md`.
