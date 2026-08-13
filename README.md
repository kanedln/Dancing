# Hot Maid Cleaning — website

A single-page marketing site for the cleaning business, built to match the branding on the
business-card artwork: black ground, hot pink, gold crown accents, Playfair Display headlines.

The card artwork is embedded as the hero "billboard" — it's the first thing on the page.

**Stack:** static HTML, CSS and vanilla JS. No build step, no dependencies, no framework.
Drop the folder on any host (Netlify, Vercel, Cloudflare Pages, GitHub Pages, cPanel) and it runs.

```
index.html
robots.txt / sitemap.xml
assets/
  css/styles.css      all styling + self-hosted @font-face rules
  js/main.js          nav, reveals, counters, before/after gallery, form
  img/                banner (webp ×4 + jpg), room artwork (svg ×6), social card, favicon
  fonts/              Inter + Playfair Display (woff2, latin & latin-ext)
tools/
  generate-room-art.py   regenerates the before/after room artwork
```

---

## What's on the page

| Section | Purpose |
| --- | --- |
| Announcement bar | Offer + phone, visible before anything else |
| Sticky header | Nav with scroll-spy, gold "Get a Free Quote" CTA |
| **Hero** | The card artwork as a framed billboard, plus H1, CTAs and trust badges |
| Stats | Animated count-up figures |
| Services | The four specialties from the card: Airbnb, Homes, Rentals, Home Sales |
| Why us | Differentiators + 24-hour guarantee stamp |
| How it works | Three steps |
| Pricing | Three tiers, middle one featured |
| Results | Before/after comparison slider with a kitchen / living room / bathroom switcher |
| Service area | Sheboygan &amp; Manitowoc county town lists |
| Reviews | Three testimonial slots |
| Quote form | Validated, with honeypot spam trap |
| FAQ | Native `<details>` accordion |
| Final CTA + footer | Last conversion push, sitemap, contact |
| Mobile bar | Sticky Call / Free Quote buttons under 880px |

---

## Before you go live

Everything below is a placeholder. Search `index.html` for each string and replace it.

| Placeholder | Where | Replace with |
| --- | --- | --- |
| ~~`(555) 214-8899`~~ | header, hero, footer, form fallback, JSON-LD | Done — set to `(920) 377-9509` |
| ~~`hello@hotmaidcleaning.com`~~ | footer, form, `main.js` → `FALLBACK_EMAIL` | Done — set to `myhotmaidcleaning@gmail.com` |
| ~~Contact name~~ | quote section, footer | Done — set to "Ask for Laurie" |
| ~~`[Your City]`, `[ST]`~~ | footer, contact list, JSON-LD | Done — Sheboygan &amp; Manitowoc, WI |
| `https://www.hotmaidcleaning.com/` | `<link rel="canonical">`, `og:url` | Real domain |
| `og:image` path | `<head>` | Change to the **absolute** URL (`https://yourdomain.com/assets/img/og-cover.jpg`) — some platforms won't resolve a relative one |
| `[Client name]` quotes | Reviews section | **Real reviews only.** Pull them from Google/Airbnb — don't invent testimonials |
| `$149 / $189 / $289` | Pricing | Your actual starting prices |
| Stat numbers | `data-count` attributes in the Stats section | Your real figures |
| `2026` in footer | Auto-filled by JS from the system clock | — |

### Wire up the quote form

The form has no backend. Open `assets/js/main.js` and set:

```js
const FORM_ENDPOINT = 'https://formspree.io/f/XXXXXXX';   // or Basin, Netlify, your own API
```

It POSTs `FormData` and expects a 2xx response. Leave `FORM_ENDPOINT` empty and the form falls
back to opening the visitor's mail client with the request pre-filled — usable, but you'll lose
submissions from people without a mail client configured, so set a real endpoint before launch.

On Netlify you can skip the JS entirely: add `netlify` and `name="quote"` to the `<form>` tag.

### Swap in photos from real jobs

The Results slider ships with **illustrated** room scenes, not photographs — they show the finish
standard without claiming to be any particular customer's home, and the section says so on the
page. Replace them with photos from your own jobs as soon as you have a good pair.

Drop the files in `assets/img/` and edit the `ROOMS` map near the top of the slider block in
`assets/js/main.js`:

```js
const ROOMS = {
  kitchen: ['assets/img/kitchen-before.jpg', 'assets/img/kitchen-after.jpg'],
  living:  ['assets/img/living-before.jpg',  'assets/img/living-after.jpg'],
  bath:    ['assets/img/bath-before.jpg',    'assets/img/bath-after.jpg']
};
```

The keys must match the `data-room` attributes on the `.ba-tab` buttons. Two rules for the photos:
shoot **before and after from the exact same spot** (tripod or a taped floor mark) or the wipe
won't line up, and use 16:9 — anything else gets cropped by `background-size: cover`. Once you use
real photos, delete the "Illustrated examples…" line under the slider.

### Regenerating the illustrated artwork

```bash
python3 tools/generate-room-art.py
```

Each room is drawn once and rendered twice (before/after) from the same geometry, which is what
keeps the two frames aligned. Edit the palettes or clutter in that script and re-run.

---

## Notes

- **Images.** The source artwork was 1.9 MB; the hero ships at 137 KB (webp, four widths via
  `srcset`) with a jpg fallback, preloaded with `fetchpriority="high"`.
- **Fonts are self-hosted** in `assets/fonts` — no Google Fonts request, so nothing leaks visitor
  IPs to a third party and there's no render-blocking round trip.
- **Accessibility.** Skip link, visible focus rings, labelled form fields with `aria-invalid` and
  live error messages, `aria-expanded` on the menu button, Escape closes the drawer, and
  `prefers-reduced-motion` disables all animation.
- **SEO.** `HouseCleaningService` JSON-LD with an `areaServed` list of every town covered, plus
  Open Graph and Twitter card tags, semantic headings, `robots.txt` and `sitemap.xml`. The title
  and meta description lead with Sheboygan and Manitowoc, which is what local searches key on.
  Update the JSON-LD block whenever you change the phone, address or service list.
- **Brand colours** were sampled directly from the artwork and live as CSS custom properties at
  the top of `styles.css` — `--pink: #DB044C`, `--gold: #C89439`, `--ink: #050505`.

## Running it locally

```bash
python3 -m http.server 8000
# then open http://localhost:8000
```

Opening `index.html` directly with `file://` mostly works, but a server is needed for the webfonts
and the form fetch to behave the same as in production.
