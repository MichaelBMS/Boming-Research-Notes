"""The small drawings GA-001 argues from.

Shared by the tests and the figure script so that the note, the figures and
the assertions are all talking about the same picture.
"""

from __future__ import annotations

import numpy as np


def tetrahedron_schlegel():
    """A triangle with a vertex at its centre: the Schlegel diagram of a
    tetrahedron, and the smallest interesting liftable drawing.

    Vertex 0 is the centre; 1, 2, 3 are the corners of a unit equilateral
    triangle centred on the origin, so their positions sum to zero.
    """
    root3_over_2 = np.sqrt(3.0) / 2.0
    points = np.array(
        [[0.0, 0.0], [0.0, 1.0], [-root3_over_2, -0.5], [root3_over_2, -0.5]]
    )
    #                 spokes                outer triangle
    edges = np.array([[0, 1], [0, 2], [0, 3], [1, 2], [2, 3], [1, 3]])
    return points, edges


def cube_schlegel(inner_corner=(1.0, 1.0)):
    """A square inside a square, corners joined: the Schlegel diagram of a
    cube, i.e. what a cube looks like seen through one of its faces.

    `inner_corner` moves vertex 6. At (1, 1) the drawing is a genuine
    projection of a cube. Move it anywhere generic and the drawing becomes an
    "impossible cube": still a perfectly good planar graph, no longer the
    shadow of anything.
    """
    points = np.array(
        [
            [-2.0, -2.0], [2.0, -2.0], [2.0, 2.0], [-2.0, 2.0],           # outer
            [-1.0, -1.0], [1.0, -1.0], list(inner_corner), [-1.0, 1.0],   # inner
        ]
    )
    edges = np.array(
        [
            [0, 1], [1, 2], [2, 3], [3, 0],   # outer square
            [4, 5], [5, 6], [6, 7], [7, 4],   # inner square
            [0, 4], [1, 5], [2, 6], [3, 7],   # connectors
        ]
    )
    return points, edges


#: The corner displacement that turns the cube drawing into an impossible one.
IMPOSSIBLE_CORNER = (1.4, 0.7)


def cube_with_vanishing_point(outer, apex, slides):
    """A cube drawing built so its four connecting edges are concurrent.

    The connectors are the images of four parallel edges of the solid, so they
    have to meet at a common point -- the vanishing point `apex`. Each inner
    corner then sits somewhere along its own ray, at fraction `slides[i]`.

    This is the parametrisation the degrees-of-freedom count uses: eight
    numbers for the outer quad, two for the apex, four slides. Concurrency is
    baked in, which is exactly what makes it useful for showing that
    concurrency is *not* sufficient.
    """
    outer = np.asarray(outer, dtype=float)
    apex = np.asarray(apex, dtype=float)
    inner = outer + np.asarray(slides, dtype=float)[:, None] * (apex - outer)
    return np.vstack([outer, inner]), cube_schlegel()[1]


#: An irregular outer quad, used so results cannot lean on symmetry.
IRREGULAR_QUAD = [[-2.3, -1.8], [2.1, -2.4], [1.7, 2.2], [-2.6, 1.5]]
