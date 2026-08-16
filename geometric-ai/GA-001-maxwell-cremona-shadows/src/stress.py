"""Maxwell-Cremona: self-stresses of a planar framework.

Canonical copy. GA-002 and later notes carry verbatim copies of this file;
edit this one and re-copy rather than editing a copy in place.

Conventions (see docs/superpowers/specs/2026-08-16-maxwell-cremona-series-design.md):

    A self-stress on a framework (G, p) is omega: E -> R with

        sum_{j ~ i} omega_ij (p_j - p_i) = 0

    at *every* vertex i. Positive omega is tension, negative is compression.
"""

from __future__ import annotations

from typing import List, NamedTuple

import numpy as np


class NotLiftable(Exception):
    """Raised when the supplied edge weights are not a self-stress, and so
    define no lift."""


class PlanarStructure(NamedTuple):
    """The faces of a straight-line planar drawing.

    `faces` are vertex cycles, counterclockwise for bounded faces and
    clockwise for the single unbounded one, whose index is `outer`.
    `edge_face_pairs[k]` is `[left, right]` for the directed edge u -> v,
    where `edges[k] == (u, v)`.
    """

    faces: List[List[int]]
    edge_face_pairs: np.ndarray
    outer: int


class Attempt(NamedTuple):
    """One affine piece per face, integrated over a spanning tree of the dual
    graph without checking that the pieces agree where they meet.

    For a genuine self-stress they always agree. For anything else the faces
    tear apart, and `closure_defect` measures the tear.
    """

    structure: PlanarStructure
    gradients: np.ndarray
    offsets: np.ndarray


class Lift(NamedTuple):
    """A piecewise-linear lift, which is also a reciprocal diagram.

    `gradients[f]` is the gradient of the lift on face `f`. Read as heights
    it is a polyhedron; read as points it is the reciprocal diagram, one
    vertex per face of the primal. That those are the same array is the whole
    Maxwell-Cremona correspondence, so they are not stored separately.
    """

    structure: PlanarStructure
    gradients: np.ndarray
    offsets: np.ndarray
    heights: np.ndarray


def rotate90(vectors: np.ndarray) -> np.ndarray:
    """Counterclockwise quarter turn: (x, y) -> (-y, x)."""
    vectors = np.asarray(vectors, dtype=float)
    return np.stack([-vectors[..., 1], vectors[..., 0]], axis=-1)


def signed_area(points: np.ndarray, face: List[int]) -> float:
    """Shoelace area of a face; negative exactly for the outer face."""
    loop = np.asarray(points, dtype=float)[list(face)]
    following = np.roll(loop, -1, axis=0)
    return 0.5 * float(
        np.sum(loop[:, 0] * following[:, 1] - following[:, 0] * loop[:, 1])
    )


def rigidity_matrix(points: np.ndarray, edges: np.ndarray) -> np.ndarray:
    """The m x 2n rigidity matrix R(p).

    Row `k` for edge (u, v) holds p_u - p_v in u's slot and p_v - p_u in v's.
    A self-stress is then exactly a vector omega with R.T @ omega == 0: the
    2i-th and (2i+1)-th entries of R.T @ omega are the two components of
    sum_j omega_ij (p_i - p_j).
    """
    points = np.asarray(points, dtype=float)
    edges = np.asarray(edges, dtype=int)
    n, m = len(points), len(edges)

    matrix = np.zeros((m, 2 * n))
    for k, (u, v) in enumerate(edges):
        delta = points[u] - points[v]
        matrix[k, 2 * u : 2 * u + 2] = delta
        matrix[k, 2 * v : 2 * v + 2] = -delta
    return matrix


def self_stress_basis(
    points: np.ndarray, edges: np.ndarray, rcond: float = 1e-10
) -> np.ndarray:
    """An orthonormal basis for the space of self-stresses, as an m x k array.

    k == 0 means the drawing carries no self-stress, and so lifts only to the
    trivial flat "polyhedron".
    """
    transposed = rigidity_matrix(points, edges).T
    _, singular_values, right_vectors = np.linalg.svd(transposed)

    largest = singular_values[0] if singular_values.size else 0.0
    tol = max(transposed.shape) * largest * rcond
    rank = int((singular_values > tol).sum())

    return right_vectors[rank:].T


def planar_faces(points: np.ndarray, edges: np.ndarray) -> PlanarStructure:
    """Trace the faces of a straight-line planar drawing.

    Standard rotation-system walk: sort each vertex's neighbours by angle,
    then step from the directed edge u -> v to v -> w, where w is the
    neighbour just *before* u going counterclockwise around v. That rule
    keeps each traced face on the left of its own directed edges, which is
    what makes bounded faces come out counterclockwise.
    """
    points = np.asarray(points, dtype=float)
    edges = np.asarray(edges, dtype=int)
    n = len(points)

    neighbours: List[List[int]] = [[] for _ in range(n)]
    for u, v in edges:
        neighbours[u].append(int(v))
        neighbours[v].append(int(u))
    for v in range(n):
        offsets = points[neighbours[v]] - points[v]
        order = np.argsort(np.arctan2(offsets[:, 1], offsets[:, 0]))
        neighbours[v] = [neighbours[v][i] for i in order]
    rank_at = [{w: i for i, w in enumerate(nb)} for nb in neighbours]

    faces: List[List[int]] = []
    face_of: dict = {}
    starts = [(int(u), int(v)) for u, v in edges] + [(int(v), int(u)) for u, v in edges]
    for start in starts:
        if start in face_of:
            continue
        cycle: List[int] = []
        u, v = start
        while (u, v) not in face_of:
            face_of[(u, v)] = len(faces)
            cycle.append(u)
            around = neighbours[v]
            u, v = v, around[(rank_at[v][u] - 1) % len(around)]
        faces.append(cycle)

    pairs = np.array(
        [[face_of[(int(u), int(v))], face_of[(int(v), int(u))]] for u, v in edges],
        dtype=int,
    )

    unbounded = [i for i, f in enumerate(faces) if signed_area(points, f) < 0]
    if len(unbounded) != 1:
        raise ValueError(
            "expected exactly one unbounded face, found %d -- is the drawing "
            "connected and free of crossings?" % len(unbounded)
        )

    return PlanarStructure(faces=faces, edge_face_pairs=pairs, outer=unbounded[0])


def nearest_stress(points: np.ndarray, edges: np.ndarray) -> np.ndarray:
    """The unit-norm edge weighting that comes closest to being a self-stress.

    When a self-stress exists this returns one. When none does, it returns the
    best available near-miss, which is what you want to draw when showing *how*
    a drawing fails to be a shadow.
    """
    transposed = rigidity_matrix(points, edges).T
    _, _, right_vectors = np.linalg.svd(transposed)
    return right_vectors[-1]


def spanning_lift(
    points: np.ndarray, edges: np.ndarray, omega: np.ndarray
) -> Attempt:
    """Integrate `omega` over a spanning tree of the dual graph.

    Crossing an edge adds the gradient jump `omega_e * R90(e)`; the offset
    follows from continuity along that edge. Rooted at the outer face with the
    zero plane, so the result is normalised without any extra step.

    No consistency check -- that is `closure_defect`'s job.
    """
    points = np.asarray(points, dtype=float)
    edges = np.asarray(edges, dtype=int)
    omega = np.asarray(omega, dtype=float)

    structure = planar_faces(points, edges)
    jumps = omega[:, None] * rotate90(points[edges[:, 1]] - points[edges[:, 0]])

    incident: List[List[int]] = [[] for _ in structure.faces]
    for k, (left, right) in enumerate(structure.edge_face_pairs):
        incident[left].append(k)
        incident[right].append(k)

    gradients = np.full((len(structure.faces), 2), np.nan)
    offsets = np.full(len(structure.faces), np.nan)
    gradients[structure.outer] = 0.0
    offsets[structure.outer] = 0.0

    queue = [structure.outer]
    while queue:
        here = queue.pop()
        for k in incident[here]:
            left, right = structure.edge_face_pairs[k]
            there = right if here == left else left
            if not np.isnan(gradients[there, 0]):
                continue
            sign = -1.0 if here == left else 1.0
            gradients[there] = gradients[here] + sign * jumps[k]
            offsets[there] = offsets[here] - sign * np.dot(
                jumps[k], points[edges[k, 0]]
            )
            queue.append(there)

    return Attempt(structure=structure, gradients=gradients, offsets=offsets)


def heights_on_face(points: np.ndarray, attempt, index: int) -> np.ndarray:
    """Where face `index` puts each of its own corners."""
    face = attempt.structure.faces[index]
    return np.asarray(points, dtype=float)[face] @ attempt.gradients[index] + (
        attempt.offsets[index]
    )


def closure_defect(points: np.ndarray, attempt) -> float:
    """How far apart the faces meeting at a vertex are, at worst.

    Zero exactly when the weights were a self-stress. Anything else is the
    width of the crack in the roof.
    """
    spread = np.zeros(len(points))
    lowest = np.full(len(points), np.inf)
    highest = np.full(len(points), -np.inf)
    for index, face in enumerate(attempt.structure.faces):
        for vertex, height in zip(face, heights_on_face(points, attempt, index)):
            lowest[vertex] = min(lowest[vertex], height)
            highest[vertex] = max(highest[vertex], height)
    seen = np.isfinite(lowest)
    spread[seen] = highest[seen] - lowest[seen]
    return float(spread.max())


def lift(points: np.ndarray, edges: np.ndarray, omega: np.ndarray,
         tol: float = 1e-8) -> Lift:
    """Integrate a self-stress into a piecewise-linear lift.

    The walk over the dual is path-independent precisely because every vertex
    is in equilibrium, so weights that are not a self-stress raise
    `NotLiftable` rather than returning quiet nonsense.

    The result is normalised so the outer face lies in the plane z = 0.
    """
    points = np.asarray(points, dtype=float)
    edges = np.asarray(edges, dtype=int)
    omega = np.asarray(omega, dtype=float)

    scale = max(1.0, float(np.abs(points).max()) * float(np.abs(omega).max()))
    residual = np.linalg.norm(rigidity_matrix(points, edges).T @ omega)
    if residual > tol * scale:
        raise NotLiftable(
            "these weights are not a self-stress: vertex equilibrium is off by "
            "%.3g" % (residual / scale)
        )

    attempt = spanning_lift(points, edges, omega)
    defect = closure_defect(points, attempt)
    if defect > tol * scale:
        raise NotLiftable("the lift does not close up; worst gap %.3g" % defect)

    # One height per vertex; the faces already agree, so take the first.
    heights = np.full(len(points), np.nan)
    for index, face in enumerate(attempt.structure.faces):
        for vertex, height in zip(face, heights_on_face(points, attempt, index)):
            if np.isnan(heights[vertex]):
                heights[vertex] = height

    return Lift(
        structure=attempt.structure,
        gradients=attempt.gradients,
        offsets=attempt.offsets,
        heights=heights,
    )


def stress_from_gradients(
    points: np.ndarray, edges: np.ndarray, lifted: Lift
) -> np.ndarray:
    """Read the self-stress back off a lift -- the correspondence, backwards.

    Each edge's gradient jump is `omega_e * R90(e)`, so projecting the jump
    onto `R90(e)` and dividing by `|e|^2` returns `omega_e`.
    """
    points = np.asarray(points, dtype=float)
    edges = np.asarray(edges, dtype=int)

    spans = points[edges[:, 1]] - points[edges[:, 0]]
    left, right = lifted.structure.edge_face_pairs.T
    jumps = lifted.gradients[left] - lifted.gradients[right]

    return np.sum(jumps * rotate90(spans), axis=1) / np.sum(spans * spans, axis=1)
