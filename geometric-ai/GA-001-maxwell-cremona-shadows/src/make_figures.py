"""Regenerate every figure in GA-001.

Deterministic -- no randomness anywhere, so re-running reproduces the committed
PNGs byte-for-similar. Run from this directory:

    python3 make_figures.py

Colour carries the sign of the stress (the diverging pair red/blue with a
neutral grey zero) and line width carries its magnitude, so the encoding
survives colour-vision deficiency and greyscale printing.
"""

from __future__ import annotations

import pathlib

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402
from mpl_toolkits.mplot3d.art3d import Poly3DCollection  # noqa: E402

import stress  # noqa: E402
from examples import (  # noqa: E402
    IMPOSSIBLE_CORNER,
    IRREGULAR_QUAD,
    cube_schlegel,
    cube_with_vanishing_point,
    tetrahedron_schlegel,
)

FIGURES = pathlib.Path(__file__).resolve().parent.parent / "figures"

SURFACE = "#fcfcfb"
INK = "#0b0b0b"
SECONDARY = "#52514e"
MUTED = "#898781"
HAIRLINE = "#e1e0d9"
TENSION = "#e34948"       # diverging warm pole: omega > 0
COMPRESSION = "#2a78d6"   # diverging cool pole: omega < 0
NEUTRAL = "#c3c2b7"       # the zero midpoint

plt.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Helvetica Neue", "Helvetica", "Arial", "DejaVu Sans"],
        "figure.facecolor": SURFACE,
        "savefig.facecolor": SURFACE,
        "axes.facecolor": SURFACE,
    }
)


def edge_style(weight, largest):
    """Colour by sign, width by magnitude."""
    if abs(weight) < 1e-9:
        return NEUTRAL, 1.6
    colour = TENSION if weight > 0 else COMPRESSION
    return colour, 1.4 + 2.6 * abs(weight) / largest


def draw_graph(ax, points, edges, omega=None, highlight=None, faded=False):
    ax.set_aspect("equal")
    ax.set_axis_off()

    largest = float(np.abs(omega).max()) if omega is not None else 1.0
    for k, (u, v) in enumerate(edges):
        if omega is None:
            colour, width = (MUTED if faded else INK), 1.8
        else:
            colour, width = edge_style(omega[k], largest)
        ax.plot(
            points[[u, v], 0], points[[u, v], 1],
            color=colour, linewidth=width, solid_capstyle="round", zorder=2,
        )

    ax.scatter(
        points[:, 0], points[:, 1],
        s=42, color=(MUTED if faded else INK),
        edgecolors=SURFACE, linewidths=2.0, zorder=3,
    )
    if highlight is not None:
        ax.scatter(
            points[highlight, 0], points[highlight, 1],
            s=190, facecolors="none", edgecolors=TENSION,
            linewidths=2.2, zorder=4,
        )

    span = points.max(axis=0) - points.min(axis=0)
    pad = 0.14 * span.max()
    ax.set_xlim(points[:, 0].min() - pad, points[:, 0].max() + pad)
    ax.set_ylim(points[:, 1].min() - pad, points[:, 1].max() + pad)


def draw_lift(ax, points, edges, lifted, omega, shadow=True):
    """The lifted surface, with the original drawing lying underneath it."""
    ax.set_axis_off()
    ax.view_init(elev=24, azim=-62)
    ax.set_box_aspect((1.0, 1.0, 0.62))

    base = lifted.heights.min()
    polygons = [
        [(points[i, 0], points[i, 1], lifted.heights[i]) for i in face]
        for index, face in enumerate(lifted.structure.faces)
        if index != lifted.structure.outer
    ]
    ax.add_collection3d(
        Poly3DCollection(
            polygons, facecolors="#dfe8f5", edgecolors="none", alpha=0.72, zorder=1
        )
    )

    largest = float(np.abs(omega).max())
    for k, (u, v) in enumerate(edges):
        colour, width = edge_style(omega[k], largest)
        ax.plot(
            points[[u, v], 0], points[[u, v], 1], lifted.heights[[u, v]],
            color=colour, linewidth=width, solid_capstyle="round", zorder=3,
        )

    if shadow:
        for u, v in edges:
            ax.plot(
                points[[u, v], 0], points[[u, v], 1], [base, base],
                color=HAIRLINE, linewidth=1.4, zorder=0,
            )
        for i, height in enumerate(lifted.heights):
            if height - base > 1e-9:
                ax.plot(
                    [points[i, 0]] * 2, [points[i, 1]] * 2, [base, height],
                    color=MUTED, linewidth=0.9, linestyle=(0, (2, 3)), zorder=0,
                )


def draw_cracked_lift(ax, points, attempt):
    """Each face put where the spanning-tree walk says it goes -- so the faces
    visibly fail to meet. This is what an unliftable drawing looks like when
    you insist on lifting it anyway.
    """
    ax.set_axis_off()
    ax.view_init(elev=24, azim=-62)
    ax.set_box_aspect((1.0, 1.0, 0.62))

    lowest = np.full(len(points), np.inf)
    highest = np.full(len(points), -np.inf)
    for index, face in enumerate(attempt.structure.faces):
        if index == attempt.structure.outer:
            continue
        corners = stress.heights_on_face(points, attempt, index)
        ax.add_collection3d(
            Poly3DCollection(
                [[(points[i, 0], points[i, 1], z) for i, z in zip(face, corners)]],
                facecolors="#efeeea", edgecolors=MUTED, linewidths=1.5, alpha=0.9,
            )
        )
        for vertex, height in zip(face, corners):
            lowest[vertex] = min(lowest[vertex], height)
            highest[vertex] = max(highest[vertex], height)

    worst = int(np.nanargmax(np.where(np.isfinite(lowest), highest - lowest, -np.inf)))
    ax.plot(
        [points[worst, 0]] * 2, [points[worst, 1]] * 2,
        [lowest[worst], highest[worst]],
        color=TENSION, linewidth=3.4, solid_capstyle="round", zorder=10,
    )
    return highest[worst] - lowest[worst]


def panel_title(ax, text, tone=SECONDARY):
    ax.set_title(text, fontsize=11.5, color=tone, pad=9)


def make_overview():
    figure = plt.figure(figsize=(12.4, 7.4))
    grid = figure.add_gridspec(
        2, 3, hspace=0.30, wspace=0.06, left=0.055, right=0.985, top=0.86, bottom=0.05
    )

    # --- top row: a drawing that lifts ---
    points, edges = cube_schlegel()
    omega = stress.self_stress_basis(points, edges)[:, 0]
    omega = omega / omega[0]
    lifted = stress.lift(points, edges, omega)

    ax = figure.add_subplot(grid[0, 0])
    draw_graph(ax, points, edges)
    panel_title(ax, "The drawing")

    ax = figure.add_subplot(grid[0, 1])
    draw_graph(ax, points, edges, omega=omega)
    panel_title(ax, "Its self-stress")

    ax = figure.add_subplot(grid[0, 2], projection="3d")
    draw_lift(ax, points, edges, lifted, omega)
    panel_title(ax, "The lift")

    # --- bottom row: move one corner and it stops ---
    broken_points, broken_edges = cube_schlegel(IMPOSSIBLE_CORNER)
    dimension = stress.self_stress_basis(broken_points, broken_edges).shape[1]
    assert dimension == 0, "the impossible cube should carry no self-stress"

    ax = figure.add_subplot(grid[1, 0])
    draw_graph(ax, broken_points, broken_edges, highlight=[6])
    panel_title(ax, "One corner moved")

    ax = figure.add_subplot(grid[1, 1])
    draw_graph(ax, broken_points, broken_edges, faded=True)
    panel_title(ax, "No self-stress exists")
    ax.text(
        0.5, -0.02, "stress space: dimension 0",
        transform=ax.transAxes, ha="center", va="top",
        fontsize=10.5, color=MUTED,
    )

    # Insist on lifting it anyway: integrate the closest thing to a stress
    # over a spanning tree of the dual, scaled to the height the real cube
    # reached, so the two 3D panels are directly comparable.
    best_effort = stress.nearest_stress(broken_points, broken_edges)
    trial = stress.spanning_lift(broken_points, broken_edges, best_effort)
    reached = max(
        stress.heights_on_face(broken_points, trial, i).max()
        for i in range(len(trial.structure.faces))
    )
    trial = stress.spanning_lift(
        broken_points, broken_edges, best_effort * lifted.heights.max() / reached
    )

    ax = figure.add_subplot(grid[1, 2], projection="3d")
    gap = draw_cracked_lift(ax, broken_points, trial)
    panel_title(ax, "The attempted lift")
    ax.text2D(
        0.5, -0.04, "faces disagree by %.2f at the worst vertex" % gap,
        transform=ax.transAxes, ha="center", va="top", fontsize=10.5, color=MUTED,
    )

    figure.suptitle(
        "Maxwell–Cremona: a drawing lifts to a polyhedron exactly when its "
        "edges can hold every vertex in equilibrium",
        fontsize=14.5, color=INK, y=0.965,
    )
    figure.text(
        0.5, 0.915,
        "red = tension   ·   blue = compression   ·   width = magnitude",
        ha="center", fontsize=11, color=MUTED,
    )

    figure.savefig(FIGURES / "overview.png", dpi=190)
    plt.close(figure)


def make_tolerance():
    """Four drawings you cannot tell apart, and the cliff underneath them."""
    offsets = [0.0, 0.01, 0.08, 0.24]
    figure = plt.figure(figsize=(12.4, 4.3))
    grid = figure.add_gridspec(
        1, 4, wspace=0.05, left=0.02, right=0.98, top=0.82, bottom=0.24
    )

    for column, offset in enumerate(offsets):
        points, edges = cube_schlegel(inner_corner=(1.0 + offset, 1.0 + offset))
        dimension = stress.self_stress_basis(points, edges).shape[1]
        width = points[:, 0].max() - points[:, 0].min()
        displacement = 100.0 * offset * np.sqrt(2.0) / width

        ax = figure.add_subplot(grid[0, column])
        draw_graph(ax, points, edges)
        panel_title(ax, "corner moved %.2f%%" % displacement, MUTED)
        # Neutral, not alarm-red: an unliftable drawing is an absence of an
        # answer, not an error -- and red already means tension here.
        ax.text(
            0.5, -0.03,
            "lifts" if dimension else "does not lift",
            transform=ax.transAxes, ha="center", va="top", fontsize=12.5,
            color=INK if dimension else MUTED,
        )
        ax.text(
            0.5, -0.15, "stress dimension %d" % dimension,
            transform=ax.transAxes, ha="center", va="top",
            fontsize=10.5, color=MUTED,
        )

    figure.suptitle(
        "One corner, four positions. Only the first drawing is a projection.",
        fontsize=14.5, color=INK, y=0.945,
    )
    figure.savefig(FIGURES / "tolerance.png", dpi=190)
    plt.close(figure)


def _bare_3d(ax, elev=28, azim=-135):
    ax.set_axis_off()
    ax.view_init(elev=elev, azim=azim)


def make_crease():
    """Why the slope difference across an edge is perpendicular to that edge.

    Both faces contain the crease, so walking along it they must agree on the
    rate of climb. Their slopes therefore share their along-edge part and can
    differ only across the edge, which leaves exactly one number per edge.
    """
    above, below = np.array([0.7, -1.0]), np.array([0.7, 0.5])
    half = 1.0

    def quad(slope, y_from, y_to):
        corners = [(-half, y_from), (half, y_from), (half, y_to), (-half, y_to)]
        return [(x, y, slope[0] * x + slope[1] * y) for x, y in corners]

    figure = plt.figure(figsize=(13.2, 4.6))
    grid = figure.add_gridspec(
        1, 3, wspace=0.10, left=0.02, right=0.98, top=0.80, bottom=0.10
    )

    # --- 1. the setup ----------------------------------------------------
    ax = figure.add_subplot(grid[0, 0], projection="3d")
    _bare_3d(ax)
    for slope, lo, hi, tone in [
        (above, 0.0, 1.0, "#dbe4f0"), (below, -1.0, 0.0, "#efece6")
    ]:
        ax.add_collection3d(
            Poly3DCollection([quad(slope, lo, hi)], facecolors=tone,
                             edgecolors=MUTED, linewidths=1.2)
        )
    ax.plot([-half, half], [0, 0], [-0.7 * half, 0.7 * half],
            color=INK, linewidth=3.2, zorder=8)
    # Floated just above the ridge, or the crease line hides it.
    ax.quiver(-0.55, 0, -0.285, 1.05, 0, 0.735, color=INK,
              arrow_length_ratio=0.16, linewidth=2.0, zorder=9)
    # text2D, so the surface cannot paint over the label
    ax.text2D(0.46, 0.88, "walk along the crease", transform=ax.transAxes,
              ha="center", color=INK, fontsize=10.5)
    ax.set_box_aspect((2.0, 2.0, 1.5))
    panel_title(ax, "Two faces, one crease")

    # --- 2. what would go wrong ------------------------------------------
    ax = figure.add_subplot(grid[0, 1])
    ax.set_axis_off()
    xs = np.linspace(-1, 1, 60)
    ax.fill_between(xs, 0.7 * xs, 0.2 * xs, color=TENSION, alpha=0.16, zorder=1)
    ax.plot(xs, 0.7 * xs, color=INK, linewidth=2.4, zorder=3)
    ax.plot(xs, 0.2 * xs, color=TENSION, linewidth=2.4, zorder=3)
    ax.text(1.04, 0.70, "the face below\nsays this", color=INK,
            fontsize=10, va="center")
    ax.text(1.04, 0.20, "the face above\nwould say this", color=TENSION,
            fontsize=10, va="center")
    ax.annotate("", xy=(0.72, 0.72 * 0.7), xytext=(0.72, 0.72 * 0.2),
                arrowprops=dict(arrowstyle="<->", color=TENSION, lw=1.5))
    ax.text(0.80, 0.72 * 0.45, "a gap", color=TENSION, fontsize=10,
            ha="left", va="center")
    ax.set_xlim(-1.15, 2.05); ax.set_ylim(-1.0, 1.0)
    ax.text(-1.15, -0.88,
            "height along the crease, if the slopes disagreed in the\n"
            "along-edge direction: the faces would need two heights at once",
            color=MUTED, fontsize=10)
    panel_title(ax, "So they must agree along it")

    # --- 3. hence perpendicular ------------------------------------------
    ax = figure.add_subplot(grid[0, 2])
    ax.set_aspect("equal"); ax.set_axis_off()
    ax.plot([-1.15, 1.15], [0, 0], color=INK, linewidth=2.4,
            solid_capstyle="round", zorder=2)
    ax.text(1.2, 0, "edge", color=INK, fontsize=10.5, va="center")
    ax.plot([above[0], above[0]], [above[1] - 0.12, below[1] + 0.12],
            color=MUTED, linewidth=1.1, linestyle=(0, (3, 3)), zorder=1)
    for vector, label, va in [
        (below, "slope below", "bottom"), (above, "slope above", "top"),
    ]:
        ax.annotate("", xy=tuple(vector), xytext=(0, 0),
                    arrowprops=dict(arrowstyle="-|>", color=SECONDARY, lw=1.9))
        ax.text(vector[0] - 0.08, vector[1] + (0.1 if va == "bottom" else -0.1),
                label, color=SECONDARY, fontsize=10, ha="right", va=va)
    ax.annotate("", xy=tuple(above), xytext=tuple(below),
                arrowprops=dict(arrowstyle="-|>", color=COMPRESSION, lw=3.0))
    ax.text(above[0] + 0.1, -0.25, "their difference", color=COMPRESSION,
            fontsize=10.5)
    ax.add_patch(plt.Rectangle((above[0] - 0.16, 0), 0.16, -0.16, fill=False,
                               edgecolor=MUTED, linewidth=1.2, zorder=4))
    ax.text(-1.15, -1.55,
            "same along-edge part, so the difference is\n"
            "perpendicular — one number per edge",
            color=MUTED, fontsize=10)
    ax.set_xlim(-1.25, 1.75); ax.set_ylim(-1.75, 1.05)
    panel_title(ax, "Leaving one number per edge")

    figure.suptitle(
        "Continuity along an edge leaves exactly one free number per edge",
        fontsize=14, color=INK, y=0.955,
    )
    figure.savefig(FIGURES / "crease.png", dpi=190)
    plt.close(figure)


def make_vanishing_point():
    """Concurrency is necessary and nowhere near sufficient."""
    apex = (0.2, 0.1)
    cases = [
        ("all four corners slid equally", [0.48] * 4),
        ("three slid the same, one moved", [0.40, 0.55, 0.50, 0.62]),
    ]

    figure = plt.figure(figsize=(9.6, 5.2))
    grid = figure.add_gridspec(
        1, 2, wspace=0.06, left=0.03, right=0.97, top=0.80, bottom=0.17
    )

    for column, (label, slides) in enumerate(cases):
        points, edges = cube_with_vanishing_point(IRREGULAR_QUAD, apex, slides)
        dimension = stress.self_stress_basis(points, edges).shape[1]

        ax = figure.add_subplot(grid[0, column])
        for corner in range(4):
            ax.plot(
                [points[corner, 0], apex[0]], [points[corner, 1], apex[1]],
                color=HAIRLINE, linewidth=1.2, linestyle=(0, (3, 3)), zorder=0,
            )
        draw_graph(ax, points, edges)
        ax.scatter(
            [apex[0]], [apex[1]], s=120, facecolors=SURFACE,
            edgecolors=MUTED, linewidths=1.6, zorder=5,
        )
        ax.annotate(
            "vanishing point", apex, textcoords="offset points", xytext=(16, -32),
            fontsize=9.5, color=MUTED,
        )
        panel_title(ax, label, MUTED)
        ax.text(
            0.5, -0.04,
            "lifts" if dimension else "does not lift",
            transform=ax.transAxes, ha="center", va="top", fontsize=12.5,
            color=INK if dimension else MUTED,
        )

    figure.suptitle(
        "Both drawings have a vanishing point. Only the left one lifts.",
        fontsize=13.5, color=INK, y=0.935,
    )
    figure.savefig(FIGURES / "vanishing-point.png", dpi=190)
    plt.close(figure)


def make_tetrahedron():
    """The smallest interesting case, worked end to end."""
    points, edges = tetrahedron_schlegel()
    omega = stress.self_stress_basis(points, edges)[:, 0]
    omega = omega / omega[3]
    lifted = stress.lift(points, edges, omega)

    figure = plt.figure(figsize=(11.4, 3.9))
    grid = figure.add_gridspec(
        1, 3, wspace=0.05, left=0.03, right=0.97, top=0.83, bottom=0.04
    )

    ax = figure.add_subplot(grid[0, 0])
    draw_graph(ax, points, edges)
    panel_title(ax, "Four vertices, six edges")

    ax = figure.add_subplot(grid[0, 1])
    draw_graph(ax, points, edges, omega=omega)
    panel_title(ax, "boundary +1, spokes −3")

    ax = figure.add_subplot(grid[0, 2], projection="3d")
    draw_lift(ax, points, edges, lifted, omega)
    panel_title(ax, "apex at √3⁄2")

    figure.suptitle(
        "The smallest liftable drawing: three compression spokes carry the peak",
        fontsize=13, color=INK, y=0.95,
    )
    figure.savefig(FIGURES / "tetrahedron.png", dpi=190)
    plt.close(figure)


if __name__ == "__main__":
    FIGURES.mkdir(exist_ok=True)
    make_overview()
    make_crease()
    make_tolerance()
    make_vanishing_point()
    make_tetrahedron()
    for name in (
        "overview.png", "crease.png", "tolerance.png",
        "vanishing-point.png", "tetrahedron.png"
    ):
        print("wrote", FIGURES / name)
