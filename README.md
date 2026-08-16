# Boming's Research Notes

Small experiments, visual explanations, and technical notes on geometric
intelligence, 3D AI, reinforcement learning, and AI agents.

> Researching how AI systems represent, reason about, and interact with
> structured physical and computational worlds.

This repository is my public research notebook. The focus is not on writing
complete papers, but on exploring interesting questions through small
experiments, mathematical intuition, visualization, and code.

Most notes follow the same arc:

**Question → Intuition → Method → Experiment → Result → Why It Matters**

---

## Research Areas

### Geometric AI &nbsp;·&nbsp; `GA`

Differentiable geometry, geometric optimization, topology, signed distance
fields, frame fields, discrete geometry, and structured representations.

→ [Browse Geometric AI notes](./geometric-ai/)

### 3D & Spatial AI &nbsp;·&nbsp; `3D`

3D reconstruction, neural scene representations, neural rendering, spatial
reasoning, and world models.

→ [Browse 3D AI notes](./3d-ai/)

### Reinforcement Learning &nbsp;·&nbsp; `RL`

GRPO, reward design, representation learning, and reinforcement learning for
structured and geometric reasoning.

→ [Browse Reinforcement Learning notes](./reinforcement-learning/)

### AI Agents &nbsp;·&nbsp; `AG`

Agent architectures, memory, planning, tool use, and multi-agent systems.

→ [Browse AI Agent notes](./ai-agents/)

---

## Recent Notes

### [GA-001 — When Is a Flat Drawing the Shadow of a Solid?](./geometric-ai/GA-001-maxwell-cremona-shadows/)

Your visual system rejects a Penrose triangle in a tenth of a second. Maxwell
worked out in 1864 what it is checking — and the answer is a rank test.

![Overview](./geometric-ai/GA-001-maxwell-cremona-shadows/figures/overview.png)

`Geometric AI` · `Concept` · `Complete` · 2026-08-16 ·
[interactive demo](https://claude.ai/code/artifact/ed5a605e-92a6-4b24-97d6-0c7ed142d9cb)

<!-- Template for each entry — newest first, keep roughly the last 5:

### [GA-001 — Differentiable SDF from Logits](./geometric-ai/GA-001-differentiable-sdf-from-logits/)

Can a discrete nearest-seed assignment coexist with gradient-based optimization?

![Overview](./geometric-ai/GA-001-differentiable-sdf-from-logits/figures/overview.png)

`Geometric AI` · `Experiment` · `Complete` · 2026-08-16

-->

---

## Notes Index

| ID | Title | Area | Type | Status | Date |
|----|-------|------|------|--------|------|
| [GA-001](./geometric-ai/GA-001-maxwell-cremona-shadows/) | When Is a Flat Drawing the Shadow of a Solid? | Geometric AI | Concept | Complete | 2026-08-16 |

**Type** — `Concept` · `Experiment` · `Research Idea`
**Status** — `Planned` · `Exploring` · `Complete` · `Open Question`

---

## Research Philosophy

Many interesting research questions do not require a full paper to explore. A
small synthetic experiment, a visualization, or a mathematical toy problem can
often reveal the core structure of a much larger problem.

A well-posed open question is worth publishing on its own. Notes marked
`Exploring` or `Open Question` are deliberately unfinished — publishing the
question is the point.

---

## Repository Layout

```
.
├── geometric-ai/            # GA-xxx notes
├── 3d-ai/                   # 3D-xxx notes
├── reinforcement-learning/  # RL-xxx notes
├── ai-agents/               # AG-xxx notes
├── assets/                  # repository-level images
├── NOTE_TEMPLATE.md         # the template every note starts from
├── LICENSE                  # CC BY 4.0 — notes, text, figures
├── LICENSE-CODE             # MIT — source code
└── CITATION.cff             # citation metadata
```

Each note is a self-contained folder named `<AREA>-<NNN>-<slug>`:

```
geometric-ai/GA-001-differentiable-sdf-from-logits/
├── README.md          # the note itself — the main artifact
├── figures/
│   └── overview.png   # every note has a main figure
├── src/
│   └── differentiable_sdf.py
└── experiment.ipynb
```

Subcategories are deliberately not pre-created. They get added when enough
notes exist to justify them.

### Adding a note

1. Pick the area and the next free number in that area (`GA-004`, `RL-002`, …).
2. Create `<area>/<AREA>-<NNN>-<slug>/` with `figures/` and `src/`.
3. Copy [`NOTE_TEMPLATE.md`](./NOTE_TEMPLATE.md) to that folder as `README.md`.
4. Produce `figures/overview.png` — the one image that carries the idea.
5. Add a row to the **Notes Index** above, an entry to **Recent Notes**, and a
   row to the area's own README.

---

## License & Citation

This repository is **dual-licensed**:

| Content | License | What it asks of you |
|---------|---------|---------------------|
| Notes, prose, figures, diagrams | [CC BY 4.0](./LICENSE) | Free to use, adapt, and share — including commercially — **provided you credit Boming Shi and link back to this repository**. |
| Source code (`src/`, `*.py`, `*.ipynb`) | [MIT](./LICENSE-CODE) | Free to use, with the copyright notice retained. |

If these notes or this code inform your work, please cite them. GitHub's
**Cite this repository** button in the sidebar generates APA and BibTeX from
[`CITATION.cff`](./CITATION.cff), or use:

```bibtex
@misc{shi_research_notes,
  author       = {Shi, Boming},
  title        = {Boming's Research Notes},
  year         = {2026},
  howpublished = {\url{https://github.com/MichaelBMS/Boming-Research-Notes}}
}
```

To cite a single note, name the note and its ID:

> Boming Shi, "Differentiable SDF from Logits", *Boming's Research Notes*,
> GA-001, 2026. <https://github.com/MichaelBMS/Boming-Research-Notes>

---

© 2026 Boming Shi
