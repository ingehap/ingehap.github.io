# Homepage structure concepts

Three different structures for a new `ingehap.github.io` homepage, each built as a
working HTML prototype in `concepts/`. The goal in every case is the same — a window
into the publications and software projects you are currently working on, plus the
work you have already done — but each structure answers it differently.

All content in the prototypes is **placeholder** (marked "Example" or "placeholder"),
except *Project001 — SR learning*, which is seeded from the real notebook in this
repository. Every prototype is plain HTML/CSS with no build step or external
dependencies, works on GitHub Pages as-is, and supports light and dark mode.

Once this branch is merged, the prototypes are viewable at:

- `https://ingehap.github.io/concepts/structure-1-dashboard/`
- `https://ingehap.github.io/concepts/structure-2-timeline/`
- `https://ingehap.github.io/concepts/structure-3-classic/`

(Or open the `index.html` files locally in a browser.)

---

## Structure 1 — "The Dashboard" (single page, work-first)

```
┌────────────────────────────────────────┐
│ Name · one-line identity · profile     │
│ links (GitHub, ORCID, Scholar, email)  │
├────────────────────────────────────────┤
│ CURRENTLY WORKING ON                   │
│ [in-progress card] [in-progress card]  │
├────────────────────────────────────────┤
│ ALL WORK   (All | Papers | Software |  │
│             In progress)  ← filters    │
│ [card] [card] [card]                   │
│ [card] [card] [card]                   │
└────────────────────────────────────────┘
```

Publications and software are **equal citizens in one filterable card grid**, each
card carrying a type label, year, tags, and links (DOI/PDF/BibTeX for papers,
repo/docs for software). A pinned "Currently working on" strip at the top makes
in-flight work the first thing a visitor sees.

- **Best for:** emphasizing *current* activity; when code and papers deserve equal
  billing; visitors who scan rather than read.
- **Maintenance:** one flat list of items — adding work means copying one card block.
- **Trade-offs:** less narrative; with many items the grid needs the filters to stay
  scannable; citations aren't in a formal list format.

## Structure 2 — "The Timeline" (single page, chronological narrative)

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

A single **vertical stream ordered by year, newest first**, with a pinned "Now"
box above it. Papers (circles) and software releases (squares) interleave on the
same line of time, and a sticky year navigation rail lets visitors jump around.

- **Best for:** telling the *story* of a research trajectory; showing momentum;
  making the connection between projects and the papers they produced.
- **Maintenance:** append an entry under the right year — the structure enforces
  chronology for you.
- **Trade-offs:** harder to answer "show me just the software"; long careers make
  a long page; the weakest of the three at formal citation lists.

## Structure 3 — "The Classic Academic Hub" (multi-page)

```
┌────────────────────────────────────────┐
│ Name | Home  Publications  Software    │  ← real pages
├────────────────────────────────────────┤
│ HOME: portrait · bio · profile links   │
│ HIGHLIGHTS: 2–3 hand-picked items      │
│ NEWS: dated one-liners                 │
└────────────────────────────────────────┘
   publications.html: full citation list
   grouped by year (DOI/PDF/BibTeX)
   software.html: project cards with
   status badges and repo/docs links
```

The conventional academic site: a **compact home page** (bio, hand-picked
highlights, news one-liners) with **dedicated Publications and Software pages**
holding the complete lists. The prototype uses three real HTML pages sharing one
stylesheet.

- **Best for:** growth — it scales to many papers and projects, and to future
  pages (Teaching, CV, Talks); matches what academic visitors expect; proper
  hanging-indent citation formatting.
- **Maintenance:** slightly more — new work touches a list page and possibly the
  home-page highlights/news.
- **Trade-offs:** current work is least visible (one click away unless
  highlighted); three files to keep consistent; the home page can go stale if
  news isn't updated.

---

## Comparison

| | 1 · Dashboard | 2 · Timeline | 3 · Classic hub |
|---|---|---|---|
| Pages | 1 | 1 | 3+ |
| Organizing principle | type + status | time | content type |
| Current work visibility | highest (pinned strip + filter) | high (pinned "Now") | lowest (highlights only) |
| Formal citation list | no | no | yes |
| Scales to lots of content | with filters | page gets long | best |
| Effort per update | lowest | low | medium |

## Recommendation

For the stated goal — *a window into current and past work, publications and
software together* — **Structure 1 (Dashboard)** is the closest fit, with
Structure 2's "Now" box as its strongest rival. Structure 3 is the right choice
if you expect the publication list to grow long or want a conventional academic
presence.

The structures also hybridize well: e.g. Structure 1's dashboard as the home page
of Structure 3's multi-page hub, adding a formal publications page only when the
list outgrows the grid. Once a structure is chosen, the next step is to promote it
to the repository root as `index.html` and replace the placeholders with real
content.
