# Homepage structure: The Timeline

The structure of the `ingehap.github.io` homepage, live at the repository root
as `index.html`. (Two alternative structures — a filterable dashboard grid and
a classic multi-page academic hub — were prototyped and rejected in favor of
this one.)

The page is a single chronological narrative — a window into current work and
everything that led to it:

```
┌────────────────────────────────────────┐
│ Name (large) · short bio · links       │
├──────┬─────────────────────────────────┤
│ Year │ ▌NOW: ongoing work (pinned)     │
│ nav  │                                 │
│ Now  │ 2026 ●─ paper entry             │
│ 2026 │ 2025 ●─ paper entry             │
│ 2025 │ 2024 ■─ software release        │
│ 2024 │      ●─ paper entry             │
│ 2023 │ 2023 ■─ Project001 started      │
└──────┴─────────────────────────────────┘
```

## How it works

- **Pinned "Now" box** — ongoing work sits above the stream, so the page always
  opens on what's happening currently.
- **One stream, ordered by year, newest first** — publications (circle markers),
  software releases (square markers) and courses (diamond markers) interleave
  on the same line of time.
- **Sticky year navigation** (desktop) — jump to any year; hidden on small screens.
- **Entry anatomy** — title, venue or release line, one plain-language sentence,
  then links (DOI / PDF / BibTeX for papers, repository / docs for software).
- **Mathematics** — entry text can contain LaTeX (`$$…$$` for display math,
  `\(…\)` inline), rendered by [KaTeX](https://katex.org/). KaTeX 0.17.0 is
  vendored in `assets/katex/` (CSS, JS, auto-render extension, woff2 fonts),
  so the site has no CDN dependency and works offline. The 2025 example
  publication shows a display equation.
- **Animations from Python** — entries can embed animations rendered by Python
  scripts. The pipeline is: script in `scripts/` (matplotlib's `FuncAnimation`
  + the Pillow GIF writer, no external encoder) → looping GIF in `assets/anim/`
  → plain `<img>` in the entry. The 2026 example software item shows the
  anisotropy energy surface morphing between easy-axis, easy-cone and
  easy-plane regimes; regenerate it with
  `python scripts/anisotropy_animation.py assets/anim/anisotropy-energy.gif`.
- Plain HTML/CSS, no build step or external dependencies, light and dark mode.
  Works on GitHub Pages as-is.

Step-by-step instructions for both the math and the animation pipeline are in
[`help.md`](help.md).

## Maintenance model

- New paper or release: copy an `<article class="entry …">` block under the right
  year (add the year `<section>` and its nav link each January).
- Work starts or finishes: add or remove a line in the "Now" list.

## Next steps

1. Replace the placeholder entries (marked "Example"/"placeholder") with real
   publications and projects — only *Project001 — SR learning* is real today.
2. Optional later: split entries into a small JSON data file rendered by a few
   lines of JS, if hand-editing HTML becomes tedious.
