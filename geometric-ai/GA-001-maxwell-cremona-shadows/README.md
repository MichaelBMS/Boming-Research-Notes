# `GA-001` — When Is a Flat Drawing the Shadow of a Solid?

**Area:** Geometric AI &nbsp;·&nbsp; **Type:** Concept &nbsp;·&nbsp; **Status:** Complete &nbsp;·&nbsp; **Date:** 2026-08-16

![Overview](./figures/overview.png)

> **Try it:** [Maxwell's Shadow Test](https://claude.ai/code/artifact/ed5a605e-92a6-4b24-97d6-0c7ed142d9cb)
> — drag the vertices and watch the verdict flip.
> First of four notes on the Maxwell–Cremona correspondence.

---

## Question

Given a planar graph drawn with straight edges, when is that drawing the
orthogonal projection of a polyhedral surface in three dimensions?

## Motivation

You already have an answer, and it runs in about a tenth of a second.

Show someone a Penrose triangle and they will tell you something is wrong with
it long before they can say what. Show them a wonky sketch of a cube and they
will accept the cube without comment. Whatever your visual system is doing, it
is plainly not searching the space of three-dimensional shapes — so what is it
computing?

The question is not only about perception. It shows up wherever flat data has
to stand for solid geometry:

- **Graph theory.** The answer turns out to be a statement about planar
  duality, and it is the first step toward Steinitz's theorem — every
  3-connected planar graph is the graph of a convex polyhedron.
- **Graphics.** Every sketch-to-3D system is fighting this constraint,
  usually without naming it. A stroke network that admits no lift admits no
  object, and no amount of optimisation will conjure one.
- **Computational geometry.** Delaunay triangulations, Voronoi diagrams and
  power diagrams are all defined by lifting flat things into one more
  dimension and looking at the result from below. Same machinery.

James Clerk Maxwell answered it in 1864, in a paper about trusses, and the
answer is far better than the question deserves.

## Intuition

Take the drawing and fold it, as if the edges were creases in a sheet of
paper. Every edge becomes a ridge or a valley, and each one has a number
attached: how sharply it folds. Call that number `ω_e`.

Now look at a single vertex. The creases meeting there have to agree with each
other — walk around the vertex, adding up the height changes, and you must
arrive back where you started. That is a purely geometric requirement, and it
is the only one there is: get every vertex to agree and the folds assemble
into a surface.

Maxwell's observation is that this closing-up condition, written out, is
**exactly** the condition that the vertex would sit still if you pulled its
edges with forces `ω_e`:

```
    Σ  ω_ij (p_j − p_i)  =  0        at every vertex i
   j~i
```

So the question "is this drawing a shadow?" becomes "can these edges be loaded
so that nothing moves?" — and that is a homogeneous linear system. Not a
search over shapes. Not an optimisation. A **rank test**.

The vocabulary is inherited from the truss problem, and it is worth keeping,
because the signs mean something: `ω > 0` is tension and corresponds to a fold
that bends one way; `ω < 0` is compression and bends the other. A drawing
whose interior edges are all the *same* sign is the projection of a **convex**
polyhedron.

## Method

A **planar framework** is a planar graph `G = (V, E)` with `n` vertices and
`m` edges, drawn with straight edges at positions `p : V → ℝ²`. A
**self-stress** is a vector `ω ∈ ℝ^m` satisfying the equilibrium equation
above at *every* vertex. Collecting those `2n` scalar equations gives the
`m × 2n` **rigidity matrix** `R(p)`, and the self-stresses are exactly
`ker(Rᵀ)`. So:

```
    dim (self-stress space)  =  m − rank R(p)
```

Note the `rank`. The familiar `m − 2n + 3` is what you get when the framework
is infinitesimally rigid, so that `rank R = 2n − 3` — the deficit of 3 being
the two translations and one rotation that no framework resists. It is a
special case, not the definition, and drawings that lift are precisely the
ones where the rank drops.

A **lift** is a continuous `z : ℝ² → ℝ` that is affine on each face,
`z(x) = ⟨a_f, x⟩ + b_f`. The correspondence is:

> **A drawing admits a non-trivial lift if and only if it carries a non-zero
> self-stress**, and the two determine each other.

<details>
<summary><strong>The proof, both directions</strong> — the whole note in twenty lines</summary>

Write `R₉₀` for the counterclockwise quarter turn `(x, y) ↦ (−y, x)`.

**Lift ⇒ stress.** Let `e = uv` be an edge with face `f` on its left and `g`
on its right. Continuity of `z` along `e` means `⟨a_f − a_g, x⟩ + (b_f − b_g)`
vanishes for every `x` on the line through `p_u` and `p_v`. So `a_f − a_g` is
normal to `e`, and since `R₉₀(p_v − p_u)` spans that normal line, there is a
scalar `ω_e` with

```
    a_f − a_g  =  ω_e · R₉₀(p_v − p_u)
```

Now walk once around a vertex `i`, through its neighbours `j_1, …, j_k` in
counterclockwise order. Each edge contributes one gradient jump, and the jumps
telescope: you end on the face you started from, so they sum to zero.

```
    0  =  Σ_t ω_{e_t} · R₉₀(p_{j_t} − p_i)  =  R₉₀ ( Σ_t ω_{e_t} (p_{j_t} − p_i) )
```

`R₉₀` is invertible, so the bracket vanishes. That bracket **is** the
equilibrium equation. The geometry closing up and the vertex standing still
are not analogous facts; they are the same equation, read through a rotation.

**Stress ⇒ lift.** Run it backwards: pick any face, set `a_f = 0`, and
integrate the same relation over the dual graph, one face at a time. The
result is well defined provided every closed walk in the dual returns the same
answer. The cycle space of the dual graph is generated by the vertex stars of
the primal — that is planar duality: cycles of `G*` correspond to cuts of `G`,
and the cut space is generated by the stars `δ(v)`. Each star closes by the
equilibrium equation at `v`. So consistency around the generators is exactly
the self-stress condition, and it propagates to every cycle.

The offsets follow from continuity at a shared endpoint:
`b_f − b_g = ⟨a_g − a_f, p_u⟩`.

**Signs and convexity.** Crossing `e` from `g` to `f` in the direction
`R₉₀(p_v − p_u)`, the slope of `z` changes by `⟨a_f − a_g, R₉₀(p_v − p_u)⟩ =
ω_e |e|²`. The slope increases exactly when `ω_e > 0`. So positive stress is a
convex crease, negative is concave, and a stress that is positive on every
interior edge makes `z` convex — the drawing is the projection of a convex
polyhedron. That equivalence, for 3-connected planar graphs, is the theorem of
Ash, Bolker, Crapo and Whiteley.

</details>

The one thing the argument needs and does not get for free is the duality
lemma. That is the seam where this becomes a graph-theory result rather than a
statics one, and it is where GA-002 picks up.

## Experiment

[`src/stress.py`](./src/stress.py) implements the correspondence directly:
build `R(p)`, take the nullspace of `Rᵀ` by SVD, integrate the resulting `ω`
over a spanning tree of the dual, and read off either heights (a polyhedron)
or gradients (a reciprocal diagram — GA-002's subject) from the same array.

The test that matters is a **falsifiable prediction about a specific picture**:
the Schlegel diagram of a cube — a square inside a square, corners joined —
should carry a self-stress, and moving one inner corner off its position
should destroy it. The graph is untouched; only geometry changes.

Everything the prose claims is pinned by
[`src/test_stress.py`](./src/test_stress.py), including the two hand-derived
numbers below and the sign conventions, so the note cannot drift away from the
code.

## Visualization

`figures/overview.png` is the experiment: top row a cube that lifts, bottom
row the same graph with one corner moved. The third column is the payoff —
where the good drawing closes into a frustum, the bad one is a roof whose
faces slide past each other, and the red bar marks the worst disagreement.

[`demo.html`](./demo.html) — also published as
[Maxwell's Shadow Test](https://claude.ai/code/artifact/ed5a605e-92a6-4b24-97d6-0c7ed142d9cb)
— does the same thing continuously. Drag a vertex and the rank test reruns on
every mouse move; the verdict flips the instant you leave the liftable set,
which is almost immediately, because that set has measure zero.

## Results

| | cube (Schlegel) | one corner moved |
|---|---|---|
| self-stress dimension | 1 | 0 |
| smallest singular value | 0 | 0.248 |
| lift | frustum, apex plane at 4 | none |
| worst gap between faces | 0 | 0.90 |

The stress on the intact cube comes out in clean integers: `+1` on the four
outer edges, `−2` on the inner square, `−4` on the connectors, lifting the
inner square to a constant height.

![The smallest liftable drawing](./figures/tetrahedron.png)

The four-vertex case is small enough to do entirely by hand. Symmetry makes
the centre's equilibrium free, corner equilibrium forces `ω_spoke =
−3 ω_boundary`, and integrating gives an apex at `√3/2` over a boundary at
zero — three compression spokes holding the peak up. The code agrees to nine
decimals. Rescale the same stress so the spokes carry `+1` instead and the
apex flips to `−√3/6`: interior edges positive, and the tent becomes a bowl,
which is the convex case.

Two things are worth noticing. First, the failed case fails *decisively*: the
smallest singular value is `0.248`, not a numerical whisker away from zero.
"Impossible" is not a near-miss. Second, the reciprocal-of-the-reciprocal
returns the original drawing exactly, which is a stronger check on the
orientation conventions than anything I could have argued.

## Discussion

What this shows: liftability is decidable by linear algebra, in the same
breath as computing a rank, with no search anywhere.

What it does **not** show, and should not be read as showing:

- **Nothing here is about generic behaviour.** Liftable drawings are a measure-
  zero set. The demo makes this visceral: nudge anything and the verdict dies.
  The interesting question is never "is this random drawing liftable" but "how
  far is it from being liftable", which is a different, non-linear question.
- **Rank tests are brittle near degeneracies.** Collinear vertices and
  coincident points move the rank around, and a tolerance decides the answer.
  The cube's `0.248` is comfortable; a drawing that is *nearly* liftable is
  genuinely ambiguous, and no threshold makes that go away.
- **"Lifts" is weaker than "lifts to something you would call an object."**
  This note asks only for a piecewise-linear surface. Convexity needs the
  uniform-sign condition, and strict convexity, self-intersection and
  realisability with sane coordinates are all separate questions — the last of
  which turns nasty, as GA-004 will show.
- Everything here fixes the outer face as the zero plane. That is a
  normalisation, not a result.

## Why It Matters

The correspondence is the door into three things this notebook cares about.

It makes polyhedral realisability **linear**, and therefore differentiable:
`ω` solves a linear system in the vertex positions, so a liftability residual
can be backpropagated through. A generative model over planar graphs can be
handed liftability as a hard constraint rather than a loss term it learns to
approximate.

It is the mechanism behind Steinitz's theorem, by way of Tutte's spring
embedding — where, in a coincidence that stops being one on inspection, the
spring constants *are* a positive self-stress.

And it is the honest version of what sketch-to-3D systems are up against. The
constraint is not soft, it is not learnable away, and it has been written down
since 1864.

**Next in this series —** *GA-002, Three Faces of Planar Duality* (in
progress): the same integration, read as points instead of heights, becomes
the reciprocal diagram — and the combinatorial dual and the Legendre transform
turn out to be one map.

## Code

- `src/stress.py` — rigidity matrix, self-stress basis, dual integration,
  reciprocal diagram, closure defect. Canonical copy for the series.
- `src/examples.py` — the drawings the note argues from.
- `src/test_stress.py` — 17 tests; the source of every number quoted above.
  Run with `python3 -m pytest src/test_stress.py` from this folder.
- `src/make_figures.py` — regenerates both figures deterministically.
- `demo.html` — the interactive version; single file, no dependencies.

## References

1. J. C. Maxwell, "On reciprocal figures and diagrams of forces",
   *Philosophical Magazine* **27** (182), 250–261, 1864. The 1870 sequel,
   "On reciprocal figures, frames, and diagrams of forces", won the Keith Prize.
2. P. Ash, E. Bolker, H. Crapo, W. Whiteley, "Convex Polyhedra, Dirichlet
   Tessellations, and Spider Webs", 1988 — positive interior stress ⟺ convex
   projection.
3. W. Whiteley, "Motions and stresses of projected polyhedra",
   *Structural Topology* **7**, 1982.
4. K. Sugihara, *Machine Interpretation of Line Drawings*, MIT Press, 1986 —
   the computational-vision reading, and the impossible objects that turn out
   to be buildable.
5. E. Steinitz, 1922 — 3-connected planar graphs are the graphs of convex
   polyhedra. Taken up in GA-004.

---

© 2026 Boming Shi &nbsp;·&nbsp; Notes: [CC BY 4.0](../../LICENSE) &nbsp;·&nbsp; Code: [MIT](../../LICENSE-CODE)

**Cite as:** Boming Shi, "When Is a Flat Drawing the Shadow of a Solid?",
*Boming's Research Notes*, `GA-001`, 2026.
<https://github.com/MichaelBMS/Boming-Research-Notes>
