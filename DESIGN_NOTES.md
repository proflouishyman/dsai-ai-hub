# Design notes

Sources read 2026-11-21 (pages fetched with a real browser; the site blocks plain fetches):

- https://brand.jhu.edu/visual-identity/colors/ — Primary: Heritage Blue #002D72 (RGB 0,45,114; PMS 288 C);
  Spirit Blue #68ACE5 (RGB 104,172,229; PMS 284 C). Quote: "At least one primary color, preferably Heritage Blue,
  should appear frequently and prominently". Secondary used here: none, except Double Black #000000 and White
  #FFFFFF from the grayscale palette. Not used (on purpose): Medium Blue #0077D8, Harbor Blue #4E97E0, the greens,
  Lavender/Plum/Purple, reds — so that no meaning depends on telling similar hues apart (color-blind-safe).
  Accessibility quote: JHU follows WCAG 2.1 Level AA; 4.5:1 normal text, 3:1 large text ("at least 19px tall and
  bold, or 21px tall"). "Spirit Blue is not accessible when combined with white text or background."
- https://brand.jhu.edu/visual-identity/typography/ — open-source faces Work Sans, Oswald, Source Serif 4 (Google
  Fonts) and proprietary Hopkins Slab (affiliates only, JHU-related materials, download library). Pairing used:
  "Source Serif 4 and Work Sans" ("For professional or formal communications"). System defaults: Tahoma and
  Georgia. Rule followed: "Do not load Google Fonts directly from external Google Fonts services" — fonts are
  self-hosted in /fonts (SIL OFL 1.1; licenses included). Hopkins Slab not used (proprietary; not needed).
  "Adobe Garamond is strictly reserved for use in the Johns Hopkins University logo system" — not used.
- https://brand.jhu.edu/visual-identity/primary-logo/ — "Individuals cannot create their own logos or shields for any
  reason." "It's best practice for the primary logo ... to appear on the initial view of a communication as a signal
  of official affiliation." This pilot is NOT official, so it shows no logo, shield or wordmark, and says so in the
  header tag and footer.
- https://brand.jhu.edu/visual-identity/enterprise-branding/ — Work Sans is the enterprise primary typeface; Gold
  #F1C400 and Spirit Blue are preferred accents (Gold not used here: it is too close to the time-scale yellow).

## Specs used on this site

| Token | Hex | Where used |
|---|---|---|
| Heritage Blue | #002D72 | Header band, headings, links, card borders |
| Spirit Blue | #68ACE5 | The 4px rule under the header only (decorative; never text, never meaning) |
| Near-black | #111111 | Body text, table borders, footer top border, box borders |
| Double Black | #000000 | Focus outline (3px, 2px offset), text on yellow and orange pills |
| White | #FFFFFF | Page background everywhere; text on the blue header |
| Time: before winter break | #FFE000 (text #000) | Schedule key: Nov 23 – Dec 17, 2026 |
| Time: January build | #808080 (text #FFF, bold, 19px) | Schedule key: Jan 4 – 29, 2027 |
| Time: Launch | #0047FF (text #FFF) | Schedule: Feb 1, 2027 |
| Time: Spring after launch | #FF7A00 (text #000) | Schedule: Feb 2 – May 2027 |
| Time: Fall 2027 and later | #111111 (text #FFF) | Schedule: from Aug 30, 2027 |

The five time colors are the color-blind-safe time scale used in the planning documents. Color means time, and it is always
paired with a text label (the phase word on each pill).

Fonts: Work Sans 400/600/700 for body and interface; Source Serif 4 600/700 for h1 and h2 only. Fallbacks:
Tahoma and Georgia. Body is 18px with a 1.6 line height and a line length of about 70 characters.

## When the site moves to a JHU host

- Add the official logo only with University Communications' approval.
- Switch fonts to the University Communications-hosted files, following the JHU webfonts guide (JHED login).
- Remove the pilot tag (and the "Not an official university page" footer line once the page is official).
- Check the JHU URL and domain guidelines.
