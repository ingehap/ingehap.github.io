#!/usr/bin/env python3
"""Animate the uniaxial magnetocrystalline anisotropy energy surface.

Renders E_a(theta) = K1 sin^2(theta) + K2 sin^4(theta) as a polar plot
while K1/K2 sweeps from +1 down to -2.4 and back, passing through the
three anisotropy regimes:

    K1 > 0            easy axis   (minima along theta = 0, pi)
    -2 K2 < K1 < 0    easy cone   (minima on a cone, sin^2 = -K1/2K2)
    K1 < -2 K2        easy plane  (minima in the basal plane)

Output is an animated GIF written with matplotlib.animation.FuncAnimation
and the Pillow writer — no external encoder needed.

Usage:
    python scripts/anisotropy_animation.py [outfile.gif]
"""

import sys

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.animation import FuncAnimation, PillowWriter

# palette matching the site's light theme
BG = "#f7f6f2"
INK = "#26291f"
ACCENT = "#3d6b4f"
GOLD = "#a8862c"
FAINT = "#8e9287"

K2 = 1.0
THETA = np.linspace(0.0, 2.0 * np.pi, 721)
R_PAD = 0.35  # radial offset so the curve never collapses onto the origin

# sweep there and back so the GIF loops seamlessly
_forward = np.linspace(1.0, -2.4, 36)
K1_SWEEP = np.concatenate([_forward, _forward[::-1]])

FPS = 12
FIGSIZE_IN = 4.2
DPI = 100


def energy(theta, k1, k2=K2):
    s2 = np.sin(theta) ** 2
    return k1 * s2 + k2 * s2**2


def regime(k1, k2=K2):
    if k1 > 0:
        return "easy axis"
    if k1 > -2.0 * k2:
        return "easy cone"
    return "easy plane"


def easy_directions(k1, k2=K2):
    """Polar angles of the energy minima."""
    if k1 > 0:
        angles = [0.0, np.pi]
    elif k1 > -2.0 * k2:
        cone = np.arcsin(np.sqrt(-k1 / (2.0 * k2)))
        angles = [cone, np.pi - cone, np.pi + cone, 2.0 * np.pi - cone]
    else:
        angles = [np.pi / 2.0, 3.0 * np.pi / 2.0]
    return np.array(angles)


def main(outfile="anisotropy-energy.gif"):
    fig = plt.figure(figsize=(FIGSIZE_IN, FIGSIZE_IN), dpi=DPI)
    fig.patch.set_facecolor(BG)
    ax = fig.add_subplot(projection="polar", facecolor=BG)
    fig.subplots_adjust(left=0.06, right=0.94, top=0.76, bottom=0.05)
    ax.set_theta_zero_location("N")  # theta measured from the symmetry axis
    ax.set_rticks([])
    ax.set_xticks(np.deg2rad([0, 90, 180, 270]))
    ax.set_xticklabels(["θ = 0", "90°", "180°", "270°"], color=FAINT, size=8)
    ax.grid(color=FAINT, alpha=0.25, linewidth=0.6)
    ax.spines["polar"].set_color(FAINT)
    ax.spines["polar"].set_alpha(0.4)
    ax.set_rlim(0, np.ptp(energy(THETA, 1.0)) + R_PAD + 0.6)

    (line,) = ax.plot([], [], color=ACCENT, linewidth=2.0)
    fill = [ax.fill_between([], [])]  # replaced each frame
    minima = ax.scatter([], [], s=28, color=GOLD, zorder=3)
    title = ax.set_title("", color=INK, size=10, pad=14)

    def update(i):
        k1 = K1_SWEEP[i]
        e = energy(THETA, k1)
        r = e - e.min() + R_PAD
        line.set_data(THETA, r)
        fill[0].remove()
        fill[0] = ax.fill_between(THETA, R_PAD * 0, r, color=ACCENT, alpha=0.12)
        easy = easy_directions(k1)
        minima.set_offsets(np.column_stack([easy, np.full_like(easy, R_PAD)]))
        title.set_text(
            f"$E_a(\\theta) = K_1\\sin^2\\theta + K_2\\sin^4\\theta$\n"
            f"$K_1/K_2 = {k1:+.2f}$  ·  {regime(k1)}"
        )
        return line, fill[0], minima, title

    anim = FuncAnimation(fig, update, frames=len(K1_SWEEP), blit=False)
    anim.save(outfile, writer=PillowWriter(fps=FPS))
    print(f"wrote {outfile} ({len(K1_SWEEP)} frames @ {FPS} fps)")


if __name__ == "__main__":
    main(*sys.argv[1:2])
