# Miles & Mountains — Alfred's travel website

Static site hosted free on GitHub Pages (repo `alfredligo09-wq.github.io`). No build step: plain HTML, CSS and JS.

- `index.html` home; `blog/`, `tips/`, `moments/`, `gallery/`, `about/` each have an `index.html`.
- `assets/style.css` all styles (palette: pine #17332b, mist #e4ece8, snow #f6f8f5, sun #e8a33d; fonts Gloock + Hanken Grotesk).
- `assets/site.js` mobile menu, region tabs, footer year. `assets/topo.svg` contour-line texture.
- `tools/generate.py` produced the original pages but is now OUTDATED (home hero is a photo: `assets/hero*.jpg/webp`). Do not run it; edit HTML directly.
- The owner is new to coding: explain changes simply, keep the site fast and mobile-first.
- Before design work, use the skills in `.claude/skills/` (frontend-design, ui-ux-pro-max).
- New posts: put each in its own folder, e.g. `blog/bali-2027/index.html`, resize photos (max ~1600px wide, WebP/JPEG) into that folder, then replace the empty state on the section page and home page with a card linking to it.
- Instagram link placeholder: `https://www.instagram.com/` — replace with the owner's profile URL once known.
- After changing `assets/style.css` or `assets/site.js`, bump the `?v=` number on their links in EVERY html file, or browsers keep the old cached file.
