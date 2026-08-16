"""Tests for stress.py — the Maxwell-Cremona solver behind GA-001.

These tests are the reason the note can state its numbers and its sign
conventions as facts rather than as hopes. Two in particular are quoted
directly by README.md: `test_tetrahedron_lifts_to_a_tent_with_apex_at_...`
fixes the lift orientation, and
`test_convex_schlegel_puts_every_interior_edge_in_compression` fixes which
sign a convex lift produces on interior edges.
"""

import numpy as np
import pytest

import stress
from examples import IMPOSSIBLE_CORNER, cube_schlegel, tetrahedron_schlegel


def test_tetrahedron_schlegel_stress_space_is_one_dimensional():
    points, edges = tetrahedron_schlegel()

    basis = stress.self_stress_basis(points, edges)

    assert basis.shape == (6, 1)


def test_tetrahedron_schlegel_stress_ratio_is_minus_three():
    """Hand-computable: centre equilibrium is free by symmetry, and corner
    equilibrium forces omega_spoke = -3 * omega_boundary."""
    points, edges = tetrahedron_schlegel()

    omega = stress.self_stress_basis(points, edges)[:, 0]
    omega = omega / omega[3]  # normalise so the outer triangle carries +1

    np.testing.assert_allclose(omega[:3], [-3.0, -3.0, -3.0], atol=1e-9)
    np.testing.assert_allclose(omega[3:], [1.0, 1.0, 1.0], atol=1e-9)


def test_cube_schlegel_carries_a_self_stress():
    points, edges = cube_schlegel()

    basis = stress.self_stress_basis(points, edges)

    assert basis.shape[1] == 1


def test_impossible_cube_carries_no_self_stress():
    """The whole point of the note: moving one corner destroys liftability,
    and the linear algebra sees it even though the graph is unchanged."""
    points, edges = cube_schlegel(IMPOSSIBLE_CORNER)

    basis = stress.self_stress_basis(points, edges)

    assert basis.shape[1] == 0


# --- the planar structure ------------------------------------------------


def test_planar_faces_finds_three_triangles_and_one_outer_face():
    points, edges = tetrahedron_schlegel()

    structure = stress.planar_faces(points, edges)

    bounded = [
        frozenset(f) for i, f in enumerate(structure.faces) if i != structure.outer
    ]
    assert len(structure.faces) == 4
    assert sorted(bounded, key=sorted) == sorted(
        [frozenset({0, 1, 2}), frozenset({0, 2, 3}), frozenset({0, 1, 3})], key=sorted
    )


def test_outer_face_is_the_one_with_negative_signed_area():
    points, edges = tetrahedron_schlegel()

    structure = stress.planar_faces(points, edges)

    areas = [stress.signed_area(points, f) for f in structure.faces]
    negative = [i for i, a in enumerate(areas) if a < 0]
    assert negative == [structure.outer]


# --- lift and reciprocal, which are one computation ----------------------


def tetrahedron_stress_normalised_to_unit_boundary():
    points, edges = tetrahedron_schlegel()
    omega = stress.self_stress_basis(points, edges)[:, 0]
    return points, edges, omega / omega[3]


def test_tetrahedron_lifts_to_a_tent_with_apex_at_sqrt_three_over_two():
    """Hand-derived. With the outer triangle in tension at +1 and the outer
    face taken as the zero plane, the centre rises to sqrt(3)/2 -- the three
    spokes are in compression and hold the peak up."""
    points, edges, omega = tetrahedron_stress_normalised_to_unit_boundary()

    lift = stress.lift(points, edges, omega)

    np.testing.assert_allclose(
        lift.heights, [np.sqrt(3.0) / 2.0, 0.0, 0.0, 0.0], atol=1e-9
    )


def test_gradient_jump_across_an_edge_is_perpendicular_to_that_edge():
    """The whole Maxwell-Cremona construction in one assertion: the dual
    diagram's edges are the gradient jumps, and they are perpendicular."""
    points, edges, omega = tetrahedron_stress_normalised_to_unit_boundary()

    lift = stress.lift(points, edges, omega)

    for k, (u, v) in enumerate(edges):
        left, right = lift.structure.edge_face_pairs[k]
        jump = lift.gradients[left] - lift.gradients[right]
        assert abs(np.dot(jump, points[v] - points[u])) < 1e-9


def test_lift_recovers_the_stress_it_was_built_from():
    points, edges, omega = tetrahedron_stress_normalised_to_unit_boundary()

    lift = stress.lift(points, edges, omega)
    recovered = stress.stress_from_gradients(points, edges, lift)

    np.testing.assert_allclose(recovered, omega, atol=1e-9)


def test_cube_lift_is_recovered_too():
    points, edges = cube_schlegel()
    omega = stress.self_stress_basis(points, edges)[:, 0]

    lift = stress.lift(points, edges, omega)
    recovered = stress.stress_from_gradients(points, edges, lift)

    np.testing.assert_allclose(recovered, omega, atol=1e-9)


def test_reciprocal_of_the_reciprocal_returns_the_original_drawing():
    """Duality is an involution. Reciprocating again means dual stress 1/omega
    and another quarter turn, which lands exactly back on the primal edges."""
    points, edges, omega = tetrahedron_stress_normalised_to_unit_boundary()

    lifted = stress.lift(points, edges, omega)
    left, right = lifted.structure.edge_face_pairs.T
    dual_spans = lifted.gradients[left] - lifted.gradients[right]
    reciprocated_again = stress.rotate90(dual_spans) / omega[:, None]

    np.testing.assert_allclose(
        reciprocated_again, points[edges[:, 0]] - points[edges[:, 1]], atol=1e-9
    )


def test_convex_schlegel_puts_every_interior_edge_in_compression():
    """The sign convention the prose quotes. Normalise the outer boundary to
    tension +1; every edge not on the outer face then comes out negative."""
    points, edges = cube_schlegel()
    omega = stress.self_stress_basis(points, edges)[:, 0]
    omega = omega / omega[0]

    outer_edges, interior_edges = omega[:4], omega[4:]

    np.testing.assert_allclose(outer_edges, 1.0, atol=1e-9)
    assert np.all(interior_edges < -1e-9)


# --- what failure actually looks like ------------------------------------


def test_spanning_lift_matches_the_real_lift_when_one_exists():
    points, edges = cube_schlegel()
    omega = stress.self_stress_basis(points, edges)[:, 0]

    attempt = stress.spanning_lift(points, edges, omega)
    exact = stress.lift(points, edges, omega)

    np.testing.assert_allclose(attempt.gradients, exact.gradients, atol=1e-9)
    assert stress.closure_defect(points, attempt) < 1e-9


def test_impossible_cube_leaves_a_visible_crack():
    """Integrate the best available weights over a spanning tree of the dual
    and the roof does not close: faces meeting at a vertex disagree about how
    high that vertex is. That gap is what "impossible" looks like."""
    points, edges = cube_schlegel(IMPOSSIBLE_CORNER)
    omega = stress.nearest_stress(points, edges)

    attempt = stress.spanning_lift(points, edges, omega)

    assert stress.closure_defect(points, attempt) > 1e-2


def test_nearest_stress_is_an_actual_stress_when_one_exists():
    points, edges = cube_schlegel()

    omega = stress.nearest_stress(points, edges)

    residual = stress.rigidity_matrix(points, edges).T @ omega
    assert np.linalg.norm(residual) < 1e-9


def test_positive_interior_stress_gives_a_convex_lift():
    """Ash, Bolker, Crapo & Whiteley (1988): a 3-connected planar drawing is
    the projection of a *convex* polyhedron exactly when it carries an
    equilibrium stress positive on the interior edges.

    Same stress as the tent test, rescaled so the spokes carry +1 instead of
    -3. The apex flips to sqrt(3)/6 *below* the outer plane -- a bowl, which
    is what convex means here.
    """
    points, edges = tetrahedron_schlegel()
    omega = stress.self_stress_basis(points, edges)[:, 0]
    omega = omega / omega[0]  # normalise the spokes to +1

    lifted = stress.lift(points, edges, omega)

    np.testing.assert_allclose(omega[:3], 1.0, atol=1e-9)
    np.testing.assert_allclose(
        lifted.heights, [-np.sqrt(3.0) / 6.0, 0.0, 0.0, 0.0], atol=1e-9
    )


def test_lifting_an_impossible_cube_raises():
    """A drawing with no self-stress has no non-flat lift, and asking for one
    should fail loudly rather than return quiet nonsense."""
    points, edges = cube_schlegel(IMPOSSIBLE_CORNER)
    not_a_stress = np.ones(len(edges))

    with pytest.raises(stress.NotLiftable):
        stress.lift(points, edges, not_a_stress)
