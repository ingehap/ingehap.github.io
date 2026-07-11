# Site help: LaTeX math and Python animations

How to put mathematics and script-generated animations on this site. Both
features are already wired up on the homepage (`index.html` at the repository
root); this document explains how they work and how to use them on any page.

- [1. LaTeX math with KaTeX](#1-latex-math-with-katex)
- [2. Python animations with matplotlib → GIF](#2-python-animations-with-matplotlib--gif)

---

## 1. LaTeX math with KaTeX

You write LaTeX directly in the page's HTML; [KaTeX](https://katex.org/)
typesets it in the browser when the page loads. KaTeX **0.17.0 is vendored in
this repository** under `assets/katex/` (CSS, JS, the auto-render extension,
and woff2 fonts), so pages depend on no CDN and work offline. GitHub Pages
serves the files as-is — there is no build step.

### 1.1 Enabling math on a page

Add these lines inside `<head>`:

```html
<link rel="stylesheet" href="assets/katex/katex.min.css">
<script defer src="assets/katex/katex.min.js"></script>
<script defer src="assets/katex/contrib/auto-render.min.js"
  onload="renderMathInElement(document.body, {delimiters: [
    {left: '$$', right: '$$', display: true},
    {left: '\\(', right: '\\)', display: false}
  ]});"></script>
```

**Adjust the relative path to where your page lives:**

| Page location | Path prefix |
|---|---|
| repository root (`index.html`) | `assets/katex/…` |
| one level deep (`concepts/…`) | `../assets/katex/…` |
| two levels deep (`concepts/<page>/…`) | `../../assets/katex/…` |

The `defer` attributes keep the scripts from blocking the page; `auto-render`
scans the document once it loads and typesets everything between the
configured delimiters.

### 1.2 Writing math

Two delimiter pairs are configured:

- **Inline math** — `\( … \)`, flows with the sentence:

  ```html
  <p>with anisotropy constants \(K_1\), \(K_2\) fitted per material.</p>
  ```

- **Display math** — `$$ … $$`, centered on its own line:

  ```html
  <div class="formula">$$E_{\mathrm{a}}(\theta) = K_1 \sin^2\theta + K_2 \sin^4\theta$$</div>
  ```

Any LaTeX math-mode notation KaTeX supports works: `\frac{a}{b}`, `\sqrt{x}`,
`\sum_{i=1}^{N}`, `\partial`, Greek letters, `\mathrm{}`, matrices via
`\begin{pmatrix}…\end{pmatrix}`, and so on. See the
[KaTeX supported functions list](https://katex.org/docs/supported.html).

The timeline page wraps display math in `<div class="formula">`, whose CSS
adds `overflow-x: auto` — a long equation scrolls inside its box instead of
stretching the page on small screens. Reuse that pattern:

```css
.formula { max-width: 38rem; overflow-x: auto; }
```

### 1.3 Things that bite

- **Backslashes are literal in HTML.** Write `\theta`, `\sin`, `\;` exactly —
  no doubling. Doubling is only needed when LaTeX passes through a
  *programming-language string* first, where `\t` or `\;` get eaten as escape
  sequences. (This once turned `\;` into literal semicolons on this very
  site.) In Python use raw strings: `r"K_1 \sin^2\theta"`; in JavaScript
  double the backslashes: `"K_1 \\sin^2\\theta"`.
- **Math renders once, on page load.** Content inserted later by JavaScript
  is not typeset automatically — call `renderMathInElement(theNewElement, …)`
  on it yourself.
- **Raw LaTeX showing on the page** almost always means the three `<head>`
  lines are missing, the relative path prefix is wrong for the page's depth,
  or the delimiters don't match the configured ones.
- **Dollar-sign text** like "costs $5 and $10" would be misread as math if
  single `$…$` delimiters were configured — that's why this site uses `\(…\)`
  for inline math and only double `$$` for display.

### 1.4 Upgrading KaTeX

Grab a newer dist and overwrite the vendored files (woff2 fonts are enough
for all modern browsers):

```bash
npm pack katex@<version>
tar -xzf katex-<version>.tgz
cp package/dist/katex.min.{css,js} assets/katex/
cp package/dist/contrib/auto-render.min.js assets/katex/contrib/
cp package/dist/fonts/*.woff2 assets/katex/fonts/
```

---

## 2. Python animations with matplotlib → GIF

The pipeline: **a Python script renders an animated GIF, the GIF is committed
to the repository, and the page embeds it with a plain `<img>` tag.** The
site stays static — visitors never run Python, and GitHub Pages just serves
a file. Everything uses generic, pip-installable libraries: matplotlib's
`FuncAnimation` for the animation and Pillow as the GIF encoder (no ffmpeg
or other system tools).

```
scripts/your_animation.py  ──runs──▶  assets/anim/your-animation.gif  ──embedded by──▶  page <img>
```

A complete working example lives at `scripts/anisotropy_animation.py`
(the animated anisotropy energy surface on the timeline). Regenerate its GIF
with:

```bash
python scripts/anisotropy_animation.py assets/anim/anisotropy-energy.gif
```

### 2.1 Requirements

```bash
pip install matplotlib pillow numpy
```

### 2.2 Minimal script

A copy-paste starting point — a traveling sine wave:

```python
#!/usr/bin/env python3
"""Minimal matplotlib -> GIF animation."""
import matplotlib
matplotlib.use("Agg")                      # render off-screen, no display needed

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter

FRAMES, FPS = 60, 15
x = np.linspace(0, 4 * np.pi, 400)

fig, ax = plt.subplots(figsize=(4.2, 2.6), dpi=100)   # 420 x 260 px
ax.set_xlim(x[0], x[-1])
ax.set_ylim(-1.2, 1.2)
(line,) = ax.plot([], [], color="#3d6b4f", linewidth=2)

def update(i):
    phase = 2 * np.pi * i / FRAMES         # one full period over the sweep -> seamless loop
    line.set_data(x, np.sin(x - phase))
    return (line,)

anim = FuncAnimation(fig, update, frames=FRAMES)
anim.save("assets/anim/sine-wave.gif", writer=PillowWriter(fps=FPS))
```

The moving parts:

- **`matplotlib.use("Agg")`** — selects the off-screen renderer, so the
  script runs anywhere (CI, ssh, no display server) *(must come before
  `import matplotlib.pyplot`)*.
- **`update(i)`** — called once per frame; mutate the artists (line data,
  titles, markers) rather than recreating the figure.
- **`FuncAnimation(fig, update, frames=N)`** — drives the frame loop.
- **`PillowWriter(fps=…)`** — encodes the GIF; Pillow ships as a plain
  Python dependency.
- **Seamless looping** — end the sweep where it began. Either animate a
  quantity that is periodic over the frame count (like `phase` above), or
  sweep a parameter *there and back*, as `anisotropy_animation.py` does:

  ```python
  forward = np.linspace(1.0, -2.4, 36)
  sweep = np.concatenate([forward, forward[::-1]])
  ```

### 2.3 Embedding the GIF in a page

```html
<figure class="media">
  <img src="assets/anim/sine-wave.gif" width="420" height="260"
       loading="lazy"
       alt="Traveling sine wave animation">
</figure>
```

- `width`/`height` = the GIF's pixel size (figsize × dpi). Setting them
  prevents the page from jumping while the GIF loads.
- `loading="lazy"` defers the download until the entry scrolls into view.
- Always write meaningful `alt` text.
- The timeline page already has the matching CSS (`.entry .media img`):
  block display, `max-width: 100%`, a hairline border, and a light
  background so the figure reads as a framed panel in both color themes.

### 2.4 Keeping GIFs small

GIF size grows with pixels × frames × visual complexity. Rules of thumb:

- **Dimensions**: `figsize=(4.2, 4.2), dpi=100` → 420 px, plenty for an
  inline figure. Prefer more inches × fewer dpi over the reverse only if you
  want larger text.
- **Frames**: 40–80 frames at 12–15 fps reads smoothly; the anisotropy GIF
  is 72 frames / 12 fps ≈ 6 s and ~340 KB.
- **Style**: flat colors and clean lines compress dramatically better than
  gradients, shading, or image backgrounds — GIF is palette-based.
- Sanity-check the result: `ls -lh assets/anim/`. A few hundred KB is fine;
  multiple MB deserves fewer frames or smaller dimensions.
- If a clip really needs to be long or high-resolution, an `<video>` tag with
  an mp4 beats GIF by ~10× — but GIF stays the zero-dependency default here.

### 2.5 Checklist for a new animation

1. Write `scripts/<name>.py` (start from the minimal script or
   `scripts/anisotropy_animation.py`).
2. Run it: `python scripts/<name>.py` → commit the GIF under `assets/anim/`.
3. Add the `<figure class="media">…</figure>` block to the page entry.
4. Open the page locally in a browser and watch the loop once — check the
   title isn't clipped, the loop doesn't jump, and the file size is sane.
5. Commit the script *and* the GIF together, so the output can always be
   regenerated.
