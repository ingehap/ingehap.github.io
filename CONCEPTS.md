# Homepage structure: The Timeline

The chosen structure for the new `ingehap.github.io` homepage, built as a working
prototype in `concepts/structure-2-timeline/index.html`. (Two alternative
structures — a filterable dashboard grid and a classic multi-page academic hub —
were prototyped and rejected in favor of this one.)

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
- **One stream, ordered by year, newest first** — publications (circle markers)
  and software releases (square markers) interleave on the same line of time.
- **Sticky year navigation** (desktop) — jump to any year; hidden on small screens.
- **Entry anatomy** — title, venue or release line, one plain-language sentence,
  then links (DOI / PDF / BibTeX for papers, repository / docs for software).
- Plain HTML/CSS, no build step or external dependencies, light and dark mode.
  Works on GitHub Pages as-is.

## Maintenance model

- New paper or release: copy an `<article class="entry …">` block under the right
  year (add the year `<section>` and its nav link each January).
- Work starts or finishes: add or remove a line in the "Now" list.

## Next steps

1. Replace the placeholder entries (marked "Example"/"placeholder") with real
   publications and projects — only *Project001 — SR learning* is real today.
2. Promote the page to the site root as `index.html` and remove the concept
   banner, making it the live homepage.
3. Optional later: split entries into a small JSON data file rendered by a few
   lines of JS, if hand-editing HTML becomes tedious.
