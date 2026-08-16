# Design — The Maxwell–Cremona Correspondence (GA-001 … GA-004)

**Date:** 2026-08-16 · **Area:** Geometric AI (`GA`) · **Status:** Approved, not yet implemented

A four-note series on the Maxwell–Cremona correspondence: one classical
theorem that turns out to be a statement about **planar graphs**, and that
quietly underwrites a surprising amount of **computer graphics**.

---

## 1. Goal

Explain, from scratch and with full derivations, why these three things are
the same thing for a planar straight-line graph:

1. a **self-stress** — edge weights that hold every interior vertex in
   equilibrium,
2. a **polyhedral lift** — a piecewise-linear function whose graph projects
   back to the drawing,
3. a **reciprocal diagram** — a drawing of the dual graph with corresponding
   edges at a fixed angle.

Then show what it buys you: planar duality gets a geometric realization,
Steinitz's theorem gets a proof, Delaunay/Voronoi/power diagrams turn out to
be one construction seen from different angles, Tutte's embedding turns out to
be both a graph-drawing algorithm and the standard mesh-parametrization method
in graphics — and the whole chain is linear, therefore differentiable,
therefore usable as a hard constraint layer in a geometric learning pipeline.

### Emphasis

**Graph theory and computer graphics are the two load-bearing directions.**
Statics is where the theorem came from and where half the vocabulary
("stress", "equilibrium", "force diagram") comes from, so it gets honest
historical treatment — but it does not drive a single note's structure.
Structural/civil engineering *applications* (thrust networks, funicular form
finding, masonry analysis) are **out of scope**. The one place statics gets
more than a sentence is GA-002's Bow's-notation box — and that box exists to
land a graph-theory punchline, not a structural one.

Concretely, the graph-theory line runs: planar duality, cycle space vs cut
space, Whitney's uniqueness of embedding and why the dual is well defined,
3-connectivity, Steinitz, Tutte's spring embedding, Laman/sparsity counts,
Schnyder woods and grid drawings. The graphics line runs: single-view line-
drawing interpretation and sketch-to-3D, mesh parametrization and UV
unwrapping, Delaunay meshing, power diagrams for blue-noise sampling and
optimal transport, straight skeletons for procedural building generation.

### Voice

Accessible and funny, but dense. No padding, no throat-clearing. Every
paragraph either advances the argument or earns its place with a genuinely
good image. The humour is in the framing and the examples, never in filler
asides.

### Non-goals

Explicitly out of scope, to keep four notes from becoming twelve:

- **Structural engineering applications.** Thrust Network Analysis, funicular
  design, masonry vaults, Bow's-notation truss workflows. One historical
  aside in GA-002, nothing more.
- Rigid origami / flat-foldability. Related, big, separate.
- 4-polytopes and Richter-Gebert's universality theorem beyond a one-line
  mention in GA-004.
- Any trained model. The Geometric AI connection in GA-004 is analysis plus
  an open question — there is no ML experiment in this series. If the open
  question turns out to be worth testing, it becomes its own note.
- Secondary polytopes beyond a pointer in GA-003.

---

## 2. Shared conventions

These are fixed here so the four notes cannot contradict each other. Every
note links back to this section's definitions as stated in GA-001.

### 2.1 Self-stress

For a planar framework `(G, p)` with `G = (V, E)` and `p: V → ℝ²`, a
self-stress is `ω: E → ℝ` satisfying, at every **interior** vertex `i`:

```
Σ_{j ~ i} ω_ij (p_j − p_i) = 0
```

Sign convention: `ω_ij > 0` is **tension**, `ω_ij < 0` is **compression**.
This is the rigidity-theory convention and the series uses it everywhere.
The names are inherited from statics; the object is a vector in the kernel of
a graph-derived matrix, and the notes read it that way.

The space of self-stresses is `ker(Rᵀ)` for the `m × 2n` rigidity matrix
`R(p)`. Its dimension is `m − rank R`, which equals `m − 2n + 3` **only when
the framework is infinitesimally rigid**. GA-001 states the general form and
the special case separately; it does not quote `m − 2n + 3` unconditionally.
Laman's condition and the sparsity count `m ≤ 2n − 3` are the graph-theoretic
side of the same statement and are mentioned in GA-001, developed in GA-004.

### 2.2 Lift

`z: ℝ² → ℝ` is continuous and affine on each face: `z(x) = ⟨a_f, x⟩ + b_f`
on face `f`. Let `R₉₀` be counterclockwise rotation by 90°.

For an edge `e = uv` with face `f` on its left and `g` on its right:

```
a_f − a_g = ω_e · R₉₀(p_v − p_u)
```

**Orientation and sign are pinned by test, not by assertion.** `src/stress.py`
asserts the convention against a known convex example (the Schlegel diagram
of a tetrahedron, or a pyramid over a convex polygon): a convex lift must
come out with all interior `ω_e` of one fixed sign, and the note states which.
Whichever sign the test yields is the sign the prose uses, in all four notes.

### 2.3 Reciprocal diagram

Two conventions, and the series names both explicitly because the literature
is inconsistent:

- **Perpendicular reciprocal** — the direct gradient/Legendre construction:
  dual vertex `f* = a_f`, so `f* − g* = ω_e · R₉₀(p_v − p_u)`, which is
  perpendicular to `e`. This is what the mathematics hands you.
- **Parallel reciprocal** — the whole perpendicular diagram rotated by 90°,
  so corresponding edges are parallel. This is the convention used in
  graphic statics, for the physical reason that a force in a member acts
  along the member.

GA-002 derives the perpendicular one and then rotates, and says plainly that
the historical papers and the later literature disagree about which name
attaches to which — the series picks the descriptive names above rather than
the eponymous ones.

### 2.4 Length and depth budget

Per note: **1200–1500 words of main text**, one demo, one `overview.png`.

Full derivations are required (that was an explicit decision), but the heavy
algebra lives in `<details>` blocks or a trailing Appendix section so the main
line stays fast. A reader who skips every `<details>` must still get a
complete, honest argument — the folded content is verification, not the load-
bearing idea.

If a note exceeds the budget, that is evidence it should split, not evidence
the budget should stretch.

### 2.5 Cross-linking

Each note opens with one sentence of back-reference and closes with one
sentence of forward-tease. Each is independently readable: a reader landing
on GA-003 from a search engine gets a self-contained note, with links for the
background rather than a dependency on it.

---

## 3. The four notes

All four are `Type: Concept`, `Status: Complete`, `Date: 2026-08-16`.
Template mapping for a Concept note: the template's **Experiment** section
holds the numerical verification plus the interactive demo; **Results** holds
what the verification actually showed.

### GA-001 — `GA-001-maxwell-cremona-shadows`

**Title:** When Is a Flat Drawing the Shadow of a Solid?
**Takeaway:** whether a drawing is three-dimensional is a linear algebra
question on a planar graph.

- **Hook:** impossible figures — the Penrose triangle, Escher, and Sugihara's
  physically-buildable "impossible" objects. Your visual system judges these
  in a second. On what evidence? Frame it as the graphics problem it is:
  single-view interpretation of a line drawing, the thing every sketch-to-3D
  system has to solve.
- **Question:** given a planar straight-line graph, when is it the orthogonal
  projection of a three-dimensional polyhedral surface?
- **Intuition:** fold a sheet of paper along the edges. Each edge becomes a
  ridge or a valley; how sharply it folds is `ω_e`. The vertex condition says
  the folds around a vertex have to agree with each other.
- **Method — the full two-way proof:**
  - continuity of `z` across `e` ⇒ `a_f − a_g ⟂ e` ⇒
    `a_f − a_g = λ_e R₉₀(p_v − p_u)`;
  - telescoping the gradient jumps around a vertex star closes to zero ⇒
    `Σ λ_e R₉₀(p_j − p_i) = 0` ⇒ apply `R₉₀⁻¹` ⇒ **literally the equilibrium
    equation**;
  - converse: given `ω`, integrate `a_f` over the dual graph; well-defined
    because the dual cycle space is generated by primal vertex stars, and
    each star closes exactly by equilibrium. State the planar-duality lemma
    explicitly — this is the note's first real graph-theory move, and GA-002
    is built on it.
- **Reading it as a graph invariant:** the lift is a potential on the dual
  graph, and the obstruction to defining it is a class in the dual cycle
  space. Half a paragraph, no homology machinery, but it names the shape of
  the argument.
- **Convexity:** uniform sign of `ω` ⟺ convex lift. Spider-web theorem.
- **Where the words came from:** one honest paragraph on Maxwell 1864 and why
  a theorem about planar graphs is phrased in the vocabulary of forces.
- **Demo:** drag vertices; solve for the self-stress live; colour edges by
  sign; a synchronized rotating 3D lift beside it. Load the Penrose triangle
  and watch the solver report no solution, with the non-closing dual loop
  highlighted — a numeric gap, not a mystery.
- **Forward:** the third leg of the equivalence is a drawing of the dual
  graph, which needs its own note.

### GA-002 — `GA-002-planar-duality-three-ways`

**Title:** Three Faces of Planar Duality
**Takeaway:** the duality is not a coincidence; combinatorial duality and the
Legendre transform are the same map, and the reciprocal diagram is where you
can see it.

- **The three faces:**
  1. **Combinatorial** — `G ↔ G*`, cycle space ↔ cut space, and why that
     exchange is exactly what makes the GA-001 integration argument work.
  2. **Geometric** — polarity and the Legendre transform.
  3. **The reciprocal diagram** — the concrete drawing that pins the other
     two together.
- **When is the dual even well defined?** Whitney: a 3-connected planar graph
  has an essentially unique embedding, so `G*` is a property of the graph and
  not of the drawing. This is why 3-connectivity keeps appearing, and it sets
  up Steinitz in GA-004.
- Construction of the reciprocal, and uniqueness up to translation.
- **Legendre derivation:** `z*(y) = sup_x (⟨y,x⟩ − z(x))`. For piecewise-
  linear `z`, faces of `z*` correspond to vertices of `z` and vertices of
  `z*` to faces of `z` — the face/vertex swap of combinatorial duality,
  falling out of a convex-analysis operation. That coincidence is the note.
- Perpendicular vs parallel conventions per §2.3.
- **Historical aside (a box, not a section):** nineteenth-century engineers
  drew force diagrams by hand with Bow's notation. They were drawing dual
  graphs, decades before graph theory had a name for them. Two paragraphs
  maximum; the punchline is graph-theoretic, not structural.
- **Demo:** a triptych — primal graph ↔ reciprocal (dual) diagram ↔ 3D lift.
  Drag any one panel, the other two update live. Toggle between the
  perpendicular and parallel conventions to see the 90° rotation.

### GA-003 — `GA-003-lifted-paraboloid`

**Title:** Delaunay, Voronoi, and Power Diagrams Were the Same Theorem
**Takeaway:** half the classic structures in computational geometry and
graphics are slices of one lift.

- Why these four things always turn out to be the same piece of code.
- Paraboloid lift `|x|²` + lower convex hull = Delaunay; Voronoi as its
  Legendre dual — reusing GA-002's transform verbatim.
- Weights = sliding points along the paraboloid = **power diagrams**.
- **Aurenhammer 1987:** a convex subdivision is a power diagram ⟺ it is
  liftable ⟺ it carries a positive self-stress. Those three clauses are
  Maxwell–Cremona. (Exact statement and theorem number to be checked against
  the source — see §7.)
- Regular vs non-regular triangulations; pointer to the secondary polytope
  (GKZ), no more than a pointer.
- **Where graphics actually uses this:** Delaunay meshing and remeshing;
  power diagrams behind capacity-constrained and blue-noise sampling and the
  optimal-transport formulations built on them; Lloyd relaxation and CVTs as
  the practical workhorse.
- **Contrast case:** the straight-skeleton roof model is also a piecewise-
  linear lift, but generally non-convex and generally *not* a regular
  subdivision — so it sits outside this framework, which is precisely why
  procedural building generators that use it cannot borrow these guarantees.
  Saying where the analogy breaks is the point of including it.
- **Demo:** drag points, watch the paraboloid lift and lower hull, see
  Delaunay fall out of the projection; slide weights to morph into a power
  diagram; load a non-regular triangulation and watch the solver refuse to
  lift it.

### GA-004 — `GA-004-algorithms-and-their-price`

**Title:** Algorithms, and What They Cost
**Takeaway:** "computable" and "computable accurately" are different claims —
and the gap sits exactly in the third dimension.

- Six algorithms, each with pseudocode and a complexity argument:
  1. find a self-stress — sparse nullspace of `Rᵀ`;
  2. decide liftability — a rank test;
  3. decide liftability to a *convex* polyhedron — LP feasibility, strict
     uniform sign;
  4. build the lift from `ω` — dual-graph BFS integration, `O(n)`;
  5. build the reciprocal from `ω` — the same BFS, rotating each step;
  6. the reverse direction — construct a drawing with a prescribed stress.
- **Tutte's spring embedding**, given real weight, with the one-line
  observation that makes the whole series click: the spring constants *are* a
  positive self-stress, so Tutte's equilibrium condition is literally the
  self-stress condition. Two Laplacian solves.
- **Tutte → Maxwell → Steinitz:** a proof that every 3-connected planar graph
  is the graph of a convex polyhedron. This is the series' graph-theory
  payoff and gets the space it deserves.
- **The same algorithm, in graphics:** Tutte's embedding is the standard mesh
  parametrization method — fix the boundary to a convex polygon, solve a
  linear system, get a UV map with no flipped triangles, guaranteed. Tutte
  1963 → Floater's weight schemes → what a modern unwrapper does. One
  algorithm, two fields, forty years apart.
- **The hard side:** exponential coordinate bits for some 3-polytopes
  (Richter-Gebert); Mnëv universality and ∃R-completeness for the adjacent
  realizability problems; degeneracies; what "almost liftable" means in
  floating point. Precise statements, checked (§7) — this section is where
  vagueness would do the most damage.
- **The contrast that frames the note:** in the plane, Schnyder gives every
  planar graph a straight-line drawing on an `(n−2) × (n−2)` integer grid. One
  dimension up, some polyhedra need exponentially many bits. **Drawable
  cheaply, liftable expensively** — and the whole series has been about that
  one extra dimension.
- **Geometric AI:** the chain is linear, so `ω` is differentiable in the
  vertex positions; Maxwell–Cremona as a hard constraint layer so a generated
  planar graph is liftable by construction; the connection to learned mesh
  parametrization and to sketch-to-3D reconstruction, where liftability is
  the constraint every method is implicitly fighting.
- **Open question to close the series:** can a learned prior predict a good
  self-stress directly? Can a network spot a Sugihara-style impossible figure
  — or does it get fooled the same way we do?
- **Demo:** Tutte convergence animation (random start → relaxation → one-click
  lift to a convex polyhedron), plus a second panel running the same solver as
  a UV unwrapper on a small mesh, to show they are one algorithm.

---

## 4. Deliverables per note

```
geometric-ai/GA-00N-<slug>/
├── README.md            # the note; English; NOTE_TEMPLATE arc
├── demo.html            # single file, zero dependencies
├── figures/
│   ├── overview.png     # the one image; reused for LinkedIn
│   └── *.png / *.gif    # supporting stills exported from the demo
└── src/
    ├── stress.py        # solver (see §5.2 on duplication)
    └── make_figures.py  # deterministic; regenerates every figure
```

Plus, per note: publish `demo.html` as a Claude Artifact and link it from the
README; add an index row to the root `README.md` **Notes Index**, a Recent
Notes entry, and a row to `geometric-ai/README.md`.

Repository-wide, once: GitHub Pages must be enabled in repository Settings so
the `demo.html` files are reachable as web pages. **This is a manual step for
Boming — it cannot be done from here.** Until it is on, the READMEs link to
the Artifact URLs and the raw file.

---

## 5. Technical contracts

### 5.1 `demo.html`

- **Single file, zero external requests.** No CDN, no external fonts, no
  remote images. This is required both for offline use from the repo and for
  the Artifact CSP.
- Vanilla JS. 2D in SVG. 3D via a hand-rolled orthographic projection with
  painter's-algorithm face sorting — roughly a hundred lines, and it avoids a
  3D library we are not allowed to fetch anyway.
- Linear algebra in JS: dense nullspace via QR or SVD with explicit rank
  tolerance. Demo sizes stay under ~200 vertices, so dense is fine and honest
  about its limits.
- Theme-aware: full light palette on bare `:root`, dark overrides under both
  `prefers-color-scheme: dark` and `[data-theme="dark"]`. Explicit `body`
  background.
- Responsive; wide content scrolls inside its own container, never the body.
- Deterministic. Any randomness is seeded, so figures regenerate identically.
- Respects `prefers-reduced-motion`; animations are pausable.

### 5.2 `src/`

- Python 3, `numpy` + `scipy` + `matplotlib` only.
- `stress.py`: build `R(p)`, nullspace via `scipy.linalg.svd` with an explicit
  rank tolerance, lift by dual BFS integration, reciprocal by the same walk.
- **Tests come first** (TDD), and they are what pins §2.2's sign convention:
  - a convex example (tetrahedron Schlegel diagram) lifts, with all interior
    `ω` of one sign — the test records which;
  - the Penrose-triangle drawing admits no self-stress;
  - lift-then-recover round-trips: recomputing `ω` from the lift returns the
    input;
  - the reciprocal of the reciprocal returns the original up to similarity;
  - (GA-004) a Tutte embedding of a 3-connected planar graph produces a
    positive self-stress and lifts to a convex polyhedron.
- `make_figures.py` is deterministic and regenerates every figure in the note
  from scratch.

**On duplicating `stress.py`:** the repository's stated value is that each
note folder is self-contained. Rather than break that with a cross-folder
import through a dash-named directory, `stress.py` is copied into each note
that needs it, with a header comment naming GA-001 as the canonical copy. If
this drifts painfully, the fix is a top-level shared module — but that is a
later decision, made when the pain is real, in the spirit of the repository's
"subcategories get added when enough notes justify them."

---

## 6. Build order

GA-001 first: it fixes the conventions and produces the solver everything
else reuses. Then GA-002 (needs the conventions and the duality lemma), then
GA-003 (largely independent code — hulls and weights — but cites GA-001's
theorem and GA-002's transform), then GA-004 (depends on all three).

Each note ships complete — README, demo, figures, src, tests, index rows,
Artifact — before the next one starts. No parallel half-finished notes.

### Definition of done, per note

- [ ] `figures/overview.png` exists and is referenced
- [ ] metadata line filled in
- [ ] main text within the 1200–1500 word budget
- [ ] every `src/` test passes; conventions in prose match what the tests assert
- [ ] `demo.html` opens correctly from `file://`, in both themes
- [ ] Artifact published and linked
- [ ] rows added to the root README (index + Recent Notes) and to
      `geometric-ai/README.md`
- [ ] citation line at the bottom names the real title and ID
- [ ] CC BY 4.0 / MIT footer intact

---

## 7. Claims requiring source verification before publication

These are load-bearing and easy to get subtly wrong. Each must be checked
against the primary source and cited precisely, or softened until it is:

1. Aurenhammer 1987 — the exact form of the power-diagram ⟺ liftability
   equivalence, and its theorem number.
2. The precise "spider web" statement, and correct attribution among
   Maxwell, Whiteley, and Ash–Bolker.
3. Whether the historical papers use the perpendicular or the parallel
   convention — the series describes both, so this only affects the
   historical sentence, but it should be right.
4. Richter-Gebert on coordinate size for 3-polytopes: the exact statement of
   the exponential bound, and whether it is an upper bound, a lower bound, or
   both. The GA-004 framing contrast depends on this being a *lower* bound —
   if it is not, the contrast must be reworded.
5. Mnëv universality and what exactly is ∃R-complete — realizability of
   oriented matroids and order types, *not* Steinitz realizability, which is
   always possible for 3-polytopes.
6. That straight skeletons are in general not regular subdivisions.
7. The dimension formula `m − 2n + 3` and its infinitesimal-rigidity
   hypothesis (§2.1), and the exact statement of Laman's condition.
8. Whitney's uniqueness-of-embedding theorem — the exact hypothesis
   (3-connected, and what "unique" means: unique up to reflection and choice
   of outer face).
9. Schnyder's grid bound — confirm `(n−2) × (n−2)`, and confirm it applies to
   all planar graphs (via triangulation) and not only to maximal ones.
10. Tutte 1963 — the exact hypotheses of the spring-embedding theorem
    (3-connected, boundary fixed to a convex polygon) and what is actually
    guaranteed (no flipped faces / convex faces).
11. The graphics-side attributions: Floater's parametrization weights, and
    the power-diagram-based blue-noise / optimal-transport sampling line of
    work. Get authors and years right or drop the specific citation and
    describe the technique generically.
12. That procedural building generators use the straight skeleton for roof
    generation — state it generically unless a specific system can be cited.

Where a source cannot be confirmed, the claim is stated as the weaker version
that *is* confirmed. This series is a public research note under the author's
name; an unverified crisp claim is worse than a verified hedged one.

---

## 8. References to work from

**Core:** Maxwell 1864, 1870 · Cremona 1872 · Whiteley 1982 ·
Crapo–Whiteley 1993 · Richter-Gebert 1996

**Graph theory:** Tutte 1963 · Steinitz 1922 · Whitney 1932 · Laman 1970 ·
Schnyder 1990 · de Fraysseix–Pach–Pollack 1990 · Mnëv 1988

**Computational geometry:** Aurenhammer 1987 ·
Gelfand–Kapranov–Zelevinsky · Aichholzer–Aurenhammer 1996

**Graphics and vision:** Sugihara 1986 · Floater · Lipson–Shpitalni 1996 ·
the power-diagram sampling line of work (§7.11)

---

© 2026 Boming Shi · Notes: [CC BY 4.0](../../../LICENSE) · Code: [MIT](../../../LICENSE-CODE)
