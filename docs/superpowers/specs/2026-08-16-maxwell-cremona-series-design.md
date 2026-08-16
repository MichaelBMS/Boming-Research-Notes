# Design — The Maxwell–Cremona Correspondence (GA-001 … GA-004)

**Date:** 2026-08-16 · **Area:** Geometric AI (`GA`) · **Status:** Approved, not yet implemented

A four-note series on the Maxwell–Cremona correspondence: one classical
theorem that is simultaneously a statement in graph theory, statics, and
computational geometry.

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

Then show what it buys you: Delaunay/Voronoi/power diagrams fall out of it,
Steinitz's theorem gets a proof through it, and the whole chain is linear —
therefore differentiable, therefore usable as a hard constraint layer in a
geometric learning pipeline.

### Voice

Accessible and funny, but dense. No padding, no throat-clearing. Every
paragraph either advances the argument or earns its place with a genuinely
good image. The humour is in the framing and the examples, never in filler
asides.

### Non-goals

Explicitly out of scope, to keep four notes from becoming twelve:

- Rigid origami / flat-foldability. Related, big, separate.
- 4-polytopes and Richter-Gebert's universality theorem beyond a one-line
  mention in GA-004.
- A history of graphic statics. Bow's notation gets a section in GA-002;
  the 150-year arc gets a paragraph, not a chapter.
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

The space of self-stresses is `ker(Rᵀ)` for the `m × 2n` rigidity matrix
`R(p)`. Its dimension is `m − rank R`, which equals `m − 2n + 3` **only when
the framework is infinitesimally rigid**. GA-001 states the general form and
the special case separately; it does not quote `m − 2n + 3` unconditionally.

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
  so corresponding edges are parallel. **This is the graphic-statics
  convention** (a force in a member acts along the member, so the force
  polygon's edges are parallel to the members). Bow's notation produces this
  one.

GA-002 derives the perpendicular one and then rotates, and says plainly that
Maxwell's and Cremona's own papers and the later literature disagree about
which name attaches to which — the series picks the descriptive names above
rather than the eponymous ones.

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
question.

- **Hook:** impossible figures — Penrose triangle, Escher, Sugihara's
  physically-buildable "impossible" objects. Your brain judges these in a
  second. On what evidence?
- **Question:** given a planar straight-line graph, when is it the orthogonal
  projection of a three-dimensional polyhedral surface?
- **Intuition:** fold a sheet of paper along the edges. Each edge becomes a
  ridge or a valley; how sharply it folds is `ω_e`. Vertex equilibrium reads
  "this hinge does not move on its own."
- **Method — the full two-way proof:**
  - continuity of `z` across `e` ⇒ `a_f − a_g ⟂ e` ⇒
    `a_f − a_g = λ_e R₉₀(p_v − p_u)`;
  - telescoping the gradient jumps around a vertex star closes to zero ⇒
    `Σ λ_e R₉₀(p_j − p_i) = 0` ⇒ apply `R₉₀⁻¹` ⇒ **literally the equilibrium
    equation**;
  - converse: given `ω`, integrate `a_f` over the dual graph; well-defined
    because the dual cycle space is generated by primal vertex stars, and
    each star closes exactly by equilibrium. State the planar-duality lemma
    explicitly.
- **Convexity:** uniform sign of `ω` ⟺ convex lift. Spider-web theorem.
- **Demo:** drag vertices; solve for the self-stress live; colour edges by
  tension/compression; a synchronized rotating 3D lift beside it. Load the
  Penrose triangle and watch the solver report no solution, with the
  non-closing height loop highlighted — a numeric gap, not a mystery.
- **Forward:** the third leg of the equivalence, the reciprocal diagram, gets
  its own note.

### GA-002 — `GA-002-reciprocal-figures`

**Title:** Reciprocal Figures — Maxwell's Third Leg
**Takeaway:** the duality is not a coincidence; it is the Legendre transform
wearing different clothes.

- Construction of the reciprocal, and uniqueness up to translation.
- **Legendre derivation:** `z*(y) = sup_x (⟨y,x⟩ − z(x))`. For piecewise-
  linear `z`, faces of `z*` correspond to vertices of `z` and vertices of
  `z*` to faces of `z`; the reciprocal is the projection of `z*`.
- Perpendicular vs parallel conventions per §2.3, including why engineers
  want the parallel one.
- **Bow's notation:** nineteenth-century truss hand-calculation is freehand
  dual-graph drawing. Worked example on a small truss.
- One paragraph on the arc from Culmann and Rankine through to Thrust Network
  Analysis (Block & Ochsendorf 2007).
- **Demo:** a triptych — form diagram ↔ force diagram ↔ 3D lift. Drag any
  one panel, the other two update live.

### GA-003 — `GA-003-lifted-paraboloid`

**Title:** Delaunay, Voronoi, and Power Diagrams Were the Same Theorem
**Takeaway:** half the classic structures in computational geometry are
slices of one lift.

- Why these four things always turn out to be the same piece of code.
- Paraboloid lift `|x|²` + lower convex hull = Delaunay; Voronoi as its
  Legendre dual.
- Weights = sliding points along the paraboloid = **power diagrams**.
- **Aurenhammer 1987:** a convex subdivision is a power diagram ⟺ it is
  liftable ⟺ it carries a positive self-stress. Those three clauses are
  Maxwell–Cremona. (Exact statement and theorem number to be checked against
  the source — see §7.)
- Regular vs non-regular triangulations; pointer to the secondary polytope
  (GKZ), no more than a pointer.
- **Contrast case:** the straight-skeleton roof model is also a piecewise-
  linear lift, but generally non-convex and generally *not* a regular
  subdivision — so it sits outside this framework. Saying precisely where the
  analogy breaks is the point of including it.
- **Demo:** drag points, watch the paraboloid lift and lower hull, see
  Delaunay fall out of the projection; slide weights to morph into a power
  diagram; load a non-regular triangulation and watch the solver refuse to
  lift it.

### GA-004 — `GA-004-algorithms-and-their-price`

**Title:** Algorithms, and What They Cost
**Takeaway:** "computable" and "computable accurately" are different claims.

- Six algorithms, each with pseudocode and a complexity argument:
  1. find a self-stress — sparse nullspace of `Rᵀ`;
  2. decide liftability — a rank test;
  3. decide liftability to a *convex* polyhedron — LP feasibility, strict
     uniform sign;
  4. build the lift from `ω` — dual-graph BFS integration, `O(n)`;
  5. build the reciprocal from `ω` — the same BFS, rotating each step;
  6. the reverse direction — construct a drawing with a prescribed stress.
- **Tutte's spring embedding**, and the one-line observation that makes the
  whole series click: the spring constants *are* a positive self-stress, so
  Tutte's equilibrium condition is literally the self-stress condition.
- **Tutte → Maxwell → Steinitz:** a proof of Steinitz's theorem by way of two
  Laplacian solves.
- **The hard side:** exponential coordinate bits for some 3-polytopes
  (Richter-Gebert), Mnëv universality and ∃R-completeness for the adjacent
  realizability problems, degeneracies, and what "almost liftable" means in
  floating point. Precise statements, checked (§7) — this section is where
  vagueness would do the most damage.
- **Geometric AI:** the chain is linear, so `ω` is differentiable in the
  vertex positions — differentiable graphic statics; Maxwell–Cremona as a
  hard constraint layer so a generated planar graph is liftable by
  construction.
- **Open question to close the series:** can a learned prior predict a good
  self-stress directly? Can a network spot a Sugihara-style impossible
  figure — or does it get fooled the same way we do?
- **Demo:** Tutte convergence animation (random start → relaxation → one-click
  lift to a convex polyhedron), plus a miniature roof designer driven by a
  positive stress field.

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
  - the reciprocal of the reciprocal returns the original up to similarity.
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
else reuses. Then GA-002 (needs the conventions), then GA-003 (largely
independent code — hulls and weights — but cites GA-001's theorem), then
GA-004 (depends on all three).

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
3. Whether Maxwell's and Cremona's original papers use the perpendicular or
   the parallel convention — the series describes both, so this only affects
   the historical sentence, but it should be right.
4. Richter-Gebert on coordinate size for 3-polytopes: the exact statement of
   the exponential bound, and whether it is an upper bound, a lower bound, or
   both.
5. Mnëv universality and what exactly is ∃R-complete — realizability of
   oriented matroids and order types, *not* Steinitz realizability, which is
   always possible for 3-polytopes.
6. That straight skeletons are in general not regular subdivisions.
7. The dimension formula `m − 2n + 3` and its infinitesimal-rigidity
   hypothesis (§2.1).

Where a source cannot be confirmed, the claim is stated as the weaker version
that *is* confirmed. This series is a public research note under the author's
name; an unverified crisp claim is worse than a verified hedged one.

---

## 8. References to work from

Maxwell 1864, 1870 · Cremona 1872 · Tutte 1963 · Steinitz 1922 ·
Aurenhammer 1987 · Whiteley 1982 · Crapo–Whiteley 1993 · Sugihara 1986 ·
Richter-Gebert 1996 · Mnëv 1988 · Gelfand–Kapranov–Zelevinsky ·
Aichholzer–Aurenhammer 1996 · Block–Ochsendorf 2007

---

© 2026 Boming Shi · Notes: [CC BY 4.0](../../../LICENSE) · Code: [MIT](../../../LICENSE-CODE)
