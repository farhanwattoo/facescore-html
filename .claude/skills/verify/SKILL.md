---
name: verify
description: Build/launch/drive recipe to verify the face-score static site end-to-end (serve public/, drive the face-analysis tool with Playwright).
---

# Verify face-score site

## Launch
```bash
npx serve public -l 4173   # serve's cleanUrls default 301s *.html → extensionless; follow redirects (curl -L). Vercel does NOT do this (no cleanUrls in vercel.json).
```

## Drive the face tool (Playwright)
- Chromium: `/opt/pw-browsers/chromium-*/chrome-linux/chrome` (sandbox), `npm i playwright face-api.js@0.22.2` in scratchpad.
- Sandbox network policy blocks `cdn.jsdelivr.net` (403 CONNECT). Work around with `page.route('https://cdn.jsdelivr.net/**')` fulfilling the face-api request from `node_modules/face-api.js/dist/face-api.min.js`. Models load locally from `/models` — no other external deps.
- Test images: `public/photo-test-assets/` (`unsplash-baseline.jpg` = good face, `u-dark.jpg` = poor light; a flat-color PNG triggers the no-face error path).
- Upload via `input[type="file"]` (3 exist; `.first()` is the main tool).
- Result signal: wait until `[data-score-val]` text ≠ `-`, or `[data-error-message]` becomes visible. All metric elements: `[data-score-val] [data-age-val] [data-gender-val] [data-emotion-val] [data-symmetry-val] [data-smile-val]`. Analysis takes ~5-20s after model load.

## Site-level checks
```bash
node scripts/audit-site.mjs        # headings, thin content, sitemap coverage
node scripts/build-sitemap.mjs     # regenerate sitemap after adding pages
```

## Gotchas
- vercel.json redirects/rewrites do NOT apply under `npx serve` — clean JP URLs and 301s are Vercel-only; test `.html` paths locally.
- Chromium in the sandbox needs `proxy: { server: process.env.HTTPS_PROXY, bypass: 'localhost' }` only for external URLs; localhost works without proxy.
