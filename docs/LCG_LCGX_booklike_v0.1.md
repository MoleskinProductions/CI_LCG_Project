# The Leak Constellation Graph (LCG) & LCG‑X Web App
**A CI/IOB navigation instrument for open questions across science, philosophy, and computation**  
Version: **v0.1**  
Generated: **2026-01-29T00:00:00Z**

---

## Preface

This is a *book-like* markdown artifact intended for **version control** (Git) and iterative refinement.

- **LCG** = the graph artifact (data + semantics).
- **LCG‑X** = the local‑first web app for exploring/editing/validating LCGs.
- **Complexical Induction (CI)** = the method focus: organize inquiry by *structural seams* (“leaks”) rather than by topic alone.

This draft is deliberately actionable: it contains a coherent spec, strict schemas, and a seed dataset you can load immediately.

---

## Abstract

The **Leak Constellation Graph (LCG)** is a graph-structured atlas of open questions where connections are defined not by topical similarity, but by shared **structural seams (“leaks”)**—recurring failure modes in explanation, inference, and representation.

The companion **LCG‑X** web app operationalizes this by providing (1) strict schema validation, (2) high-friction editing guardrails, (3) analytics for cluster/centrality/motif discovery, and (4) exports that turn the graph into dossiers for serious writing and research workflows.

---

## Table of Contents

1. Conceptual Overview  
2. LCG Specification v0.1  
3. LCG‑X Web App Specification v0.1  
4. JSON Schemas (Draft 2020‑12)  
5. Seed Dataset (25 nodes / 40 edges)

---

# 1. Conceptual Overview

## 1.1 What LCG is

An **LCG** is a directed, typed graph:

- **Nodes** represent *open questions* (scientific tensions, philosophical paradoxes, explanatory gaps, disputed inferences).
- **Edges** represent *structural relations* between those questions: shared leak types, complementary seams, transferable discriminators, and chart bridges.

The key discipline is **explicit justification**: every edge must say *why* it exists.

## 1.2 What “structure” means here

LCG treats “interdisciplinary” as *structural adjacency*, not topical adjacency.

Examples of structural adjacency:
- underdetermination under distribution shift,
- chart mismatch (two incompatible descriptions of the same object),
- proof/knowledge barriers,
- robustness via coarse-graining,
- observer included in the system being described.

These are portable. “What kind of failure mode is this?” is often a better connector than “What is this about?”

---

# 2. LCG Specification v0.1

## 2.1 Core objects

### QuestionNode (minimum fields)
- `id`: Q000123  
- `title`: short, sharp  
- `domains`: tags  
- `summary`: 2–6 sentences  
- `status`: open / contested / partially_resolved / obsolete  
- `leak_profile`: weights for L1..L6 (recommended normalized)  
- `chart_tags`: representation/frame tags  
- `interface_variables`: optional, but encouraged  
- `claim_temptations`: A/M/I/P flags (what this node *seduces* people into claiming)  
- `invariants`: candidate glue keys / budgets / regime markers  
- `discriminators`: tests that split hypotheses or charts  

### RelationEdge (minimum fields)
- `id`: E000123  
- `source`, `target`: Q-ids  
- `type`: E1..E4  
- `weight`: 0–1  
- `justification`: explicit rationale  
- `evidence_refs`: optional pointers (seed can be empty)  

## 2.2 Edge types (E1–E4)

- **E1_SharedLeak (homology):** same seam, different domain clothing.  
- **E2_ComplementaryLeak (duality):** seam in one is glue in another.  
- **E3_DiscriminatorTransfer:** a test strategy in one domain transfers to another.  
- **E4_ChartBridge:** shared interface variable / translation layer between descriptions.

## 2.3 Guardrails (editorial, not metaphysical)

- `weight > 0.6` ⇒ `justification` must be nontrivial (recommend ≥ 120 chars).
- Nodes with strong metaphysical temptation should not have *zero* discriminators (warn, don’t block).
- Leak profiles should be normalized (warn if not).

## 2.4 Analytics (LCG‑X must support)

- Clustering (Louvain or similar)
- Centralities (degree, betweenness)
- “Discriminator hub” score (out-degree along E3 edges)
- Motif detection (small subgraph patterns worth reusing in writing)

## 2.5 Exports

- Full bundle: `lcg_graph.json`
- Node dossiers: `reports/node_Q000123.md`
- Cluster dossiers: `reports/cluster_C01.md`
- Discriminator atlas: `reports/discriminator_atlas.md`
- Snapshots: PNG/SVG

---

# 3. LCG‑X Web App Specification v0.1

## 3.1 Product stance

LCG‑X is an **epistemic instrument**:
- no feeds, no engagement mechanics,
- no “AI declares truth,”
- explicit justifications and discriminators are the center of gravity.

MVP is **local-first**: file import/export, runs as a static site.

## 3.2 Recommended stack

- **Frontend:** TypeScript + React (Vite)
- **Graph UI:** Cytoscape.js
- **Validation:** AJV
- **State:** Zustand (or Redux Toolkit)
- **Analytics:** Graphology + Louvain + centrality modules

## 3.3 Core user stories

1. **Load/Validate:** import `lcg_graph.json`, validate, show precise errors.  
2. **Explore:** pan/zoom, search, filters by domain/leak/status/metrics.  
3. **Edit Nodes:** create/edit nodes; leak normalization helper.  
4. **Edit Edges:** create/edit edges; guardrails on weight/justification.  
5. **Analytics:** compute clusters + centrality + hubs + suspicious edges.  
6. **Export:** save bundle + export dossiers + snapshots.

## 3.4 UI layout

- Left: graph canvas  
- Right: inspector (tabs: Node | Edge | Analytics | Export | Validation)  
- Top bar: Import/Save, Undo/Redo, Search, Layout selector.

Visual encoding:
- Node color = dominant leak
- Node size = chosen metric (default betweenness)
- Edge style by type (E1 solid, E2 dashed, E3 bold arrow, E4 dotted)
- Edge thickness = weight

## 3.5 Milestones

- **M1** import/export + validation + graph render + basic editors  
- **M2** guardrails + search/filter + undo/redo  
- **M3** analytics dashboard + metric styling  
- **M4** exports (markdown dossiers + snapshots)  
- **M5** motif suggestions + deterministic “Next Moves” routing

---

# 4. JSON Schemas (Draft 2020‑12)

> These are strict schemas designed to keep the artifact clean under version control.

## 4.1 `schemas/node.schema.json`
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.org/lcg/node.schema.json",
  "title": "LCG QuestionNode",
  "type": "object",
  "additionalProperties": false,
  "required": ["id", "title", "domains", "summary", "status", "leak_profile", "chart_tags", "claim_temptations", "invariants", "discriminators"],
  "properties": {
    "id": { "type": "string", "pattern": "^Q\\d{6}$" },
    "title": { "type": "string", "minLength": 3 },
    "domains": { "type": "array", "items": { "type": "string" }, "minItems": 1 },
    "summary": { "type": "string", "minLength": 20 },
    "status": { "type": "string", "enum": ["open", "contested", "partially_resolved", "obsolete"] },
    "leak_profile": {
      "type": "object",
      "additionalProperties": false,
      "required": ["L1","L2","L3","L4","L5","L6"],
      "properties": {
        "L1": { "type": "number", "minimum": 0, "maximum": 1 },
        "L2": { "type": "number", "minimum": 0, "maximum": 1 },
        "L3": { "type": "number", "minimum": 0, "maximum": 1 },
        "L4": { "type": "number", "minimum": 0, "maximum": 1 },
        "L5": { "type": "number", "minimum": 0, "maximum": 1 },
        "L6": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    },
    "chart_tags": { "type": "array", "items": { "type": "string" }, "minItems": 1 },
    "interface_variables": { "type": "array", "items": { "type": "string" } },
    "claim_temptations": {
      "type": "array",
      "items": { "type": "string", "enum": ["A","M","I","P"] },
      "minItems": 1
    },
    "invariants": {
      "type": "array",
      "items": { "$ref": "invariant_ref.schema.json" },
      "minItems": 1
    },
    "discriminators": {
      "type": "array",
      "items": { "$ref": "discriminator_ref.schema.json" }
    },
    "sources": { "type": "array", "items": { "type": "string" } },
    "notes": { "type": "string" }
  }
}
```

## 4.2 `schemas/edge.schema.json`
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.org/lcg/edge.schema.json",
  "title": "LCG RelationEdge",
  "type": "object",
  "additionalProperties": false,
  "required": ["id", "source", "target", "type", "weight", "justification"],
  "properties": {
    "id": { "type": "string", "pattern": "^E\\d{6}$" },
    "source": { "type": "string", "pattern": "^Q\\d{6}$" },
    "target": { "type": "string", "pattern": "^Q\\d{6}$" },
    "type": { "type": "string", "enum": ["E1_SharedLeak","E2_ComplementaryLeak","E3_DiscriminatorTransfer","E4_ChartBridge"] },
    "weight": { "type": "number", "minimum": 0, "maximum": 1 },
    "justification": { "type": "string", "minLength": 40 },
    "evidence_refs": { "type": "array", "items": { "type": "string" } },
    "tags": { "type": "array", "items": { "type": "string" } }
  }
}
```

## 4.3 `schemas/invariant_ref.schema.json`
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.org/lcg/invariant_ref.schema.json",
  "title": "InvariantRef",
  "type": "object",
  "additionalProperties": false,
  "required": ["id", "name"],
  "properties": {
    "id": { "type": "string", "pattern": "^I-[A-Z]{2,5}-\\d{3}$" },
    "name": { "type": "string" },
    "definition": { "type": "string" },
    "role": { "type": "string", "enum": ["glue_key","discriminator","regime_marker","budget","summary"] }
  }
}
```

## 4.4 `schemas/discriminator_ref.schema.json`
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.org/lcg/discriminator_ref.schema.json",
  "title": "DiscriminatorRef",
  "type": "object",
  "additionalProperties": false,
  "required": ["id", "name", "pattern"],
  "properties": {
    "id": { "type": "string", "pattern": "^D-[A-Z]{2,5}-\\d{3}$" },
    "name": { "type": "string" },
    "pattern": {
      "type": "string",
      "enum": ["hysteresis","ablation","intervention","orthogonal_probe","interface_scatter","ensemble_split","stress_ramp"]
    },
    "how_to": { "type": "string" },
    "transferable": { "type": "boolean", "default": true }
  }
}
```

## 4.5 `schemas/lcg.schema.json`
```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://example.org/lcg/lcg.schema.json",
  "title": "Leak Constellation Graph Bundle",
  "type": "object",
  "additionalProperties": false,
  "required": ["version", "generated_at", "nodes", "edges"],
  "properties": {
    "version": { "type": "string", "const": "0.1" },
    "generated_at": { "type": "string", "format": "date-time" },
    "nodes": { "type": "array", "items": { "$ref": "node.schema.json" }, "minItems": 1 },
    "edges": { "type": "array", "items": { "$ref": "edge.schema.json" } }
  }
}
```

---

# 5. Seed Dataset (self-contained)

Save this into `public/seeds/lcg_graph.seed.json` (or load it directly into the app).

```json
{
  "version": "0.1",
  "generated_at": "2026-01-30T05:00:00Z",
  "nodes": [
    {
      "id": "Q000001",
      "title": "Cosmological constant problem",
      "domains": ["cosmology", "qft", "gravity", "philosophy"],
      "summary": "Why is the observed vacuum energy (Λ) so small compared to naive quantum field theory expectations, and why is it comparable to matter density today?",
      "status": "open",
      "leak_profile": { "L1": 0.02, "L2": 0.05, "L3": 0.10, "L4": 0.15, "L5": 0.30, "L6": 0.38 },
      "chart_tags": ["EFT", "vacuum_energy", "GR_background", "parameter_naturalness"],
      "interface_variables": ["Lambda", "vacuum_energy_density", "curvature_scale"],
      "claim_temptations": ["P", "M"],
      "invariants": [
        {
          "id": "I-COS-001",
          "name": "late_time_expansion_rate",
          "definition": "Observed acceleration signature in the expansion history.",
          "role": "glue_key"
        }
      ],
      "discriminators": [
        {
          "id": "D-COS-001",
          "name": "Dynamic equation-of-state tests",
          "pattern": "orthogonal_probe",
          "how_to": "Use BAO+SN+CMB joint constraints to test w(z) vs w=-1 across redshift.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "LCG seed: treat as L5/L6 seam between EFT expectations, GR coupling, and empirical acceleration."
    },
    {
      "id": "Q000002",
      "title": "Hubble tension",
      "domains": ["cosmology", "gravity", "statistics"],
      "summary": "Early-universe inferences and late-universe measurements disagree on H0, challenging ΛCDM glue assumptions and/or measurement systematics.",
      "status": "contested",
      "leak_profile": { "L1": 0.03, "L2": 0.06, "L3": 0.20, "L4": 0.18, "L5": 0.10, "L6": 0.43 },
      "chart_tags": ["CMB_inference", "distance_ladder", "BAO", "sound_horizon_glue"],
      "interface_variables": ["H0", "rd", "Omega_m"],
      "claim_temptations": ["I", "P"],
      "invariants": [
        {
          "id": "I-COS-002",
          "name": "acoustic_scale_consistency",
          "definition": "Consistency of the CMB acoustic scale with inferred late-time distances.",
          "role": "glue_key"
        }
      ],
      "discriminators": [
        {
          "id": "D-COS-002",
          "name": "Orthogonal H0 probes",
          "pattern": "orthogonal_probe",
          "how_to": "Compare standard sirens, time-delay lenses, TRGB/Cepheid ladders, and CMB-inferred H0 with shared priors minimized.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "Classic L6 seam: underdetermined split between systematics vs new physics; interface variable rd is a key bridge."
    },
    {
      "id": "Q000003",
      "title": "Is dark energy dynamical or a constant?",
      "domains": ["cosmology", "gravity"],
      "summary": "Does dark energy evolve in time (w(z) ≠ -1), or is Λ truly constant across cosmic history?",
      "status": "open",
      "leak_profile": { "L1": 0.03, "L2": 0.06, "L3": 0.18, "L4": 0.18, "L5": 0.12, "L6": 0.43 },
      "chart_tags": ["w0_wa", "expansion_history", "BAO_geometry", "SN_distances"],
      "interface_variables": ["w(z)", "H(z)"],
      "claim_temptations": ["I", "P"],
      "invariants": [
        {
          "id": "I-COS-003",
          "name": "distance_redshift_relation",
          "definition": "Geometric distance measures across redshift must cohere under a chosen DE model.",
          "role": "glue_key"
        }
      ],
      "discriminators": [
        {
          "id": "D-COS-003",
          "name": "Model comparison with penalty",
          "pattern": "ablation",
          "how_to": "Compare ΛCDM vs w0-wa vs early dark energy variants under equalized priors and complexity penalties.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "Serves as a ChartBridge between cosmological constant problem and Hubble tension narratives."
    },
    {
      "id": "Q000004",
      "title": "Quantum gravity: consistent unification of GR and QFT",
      "domains": ["gravity", "qft", "quantum_foundations", "math"],
      "summary": "How can a quantum theory recover classical spacetime geometry while remaining consistent with quantum field theory and observed locality/causality?",
      "status": "open",
      "leak_profile": { "L1": 0.05, "L2": 0.10, "L3": 0.12, "L4": 0.18, "L5": 0.25, "L6": 0.30 },
      "chart_tags": ["spacetime_emergence", "UV_completion", "locality", "holography"],
      "interface_variables": ["Planck_scale", "entropy_area", "causal_structure"],
      "claim_temptations": ["P", "M"],
      "invariants": [
        {
          "id": "I-GRV-001",
          "name": "recover_GR_limit",
          "definition": "Any candidate must recover classical GR in appropriate regimes.",
          "role": "regime_marker"
        }
      ],
      "discriminators": [
        {
          "id": "D-GRV-001",
          "name": "Consistency under dual descriptions",
          "pattern": "interface_scatter",
          "how_to": "Test whether candidate frameworks give consistent predictions when translated across duality/interface maps (where available).",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "A major L5/L6 hub; interacts strongly with black holes, measurement, and information."
    },
    {
      "id": "Q000005",
      "title": "Measurement problem in quantum mechanics",
      "domains": ["quantum_foundations", "philosophy", "physics"],
      "summary": "How do definite outcomes arise from unitary quantum evolution, and what exactly counts as a measurement or observer interaction?",
      "status": "open",
      "leak_profile": { "L1": 0.05, "L2": 0.08, "L3": 0.10, "L4": 0.12, "L5": 0.30, "L6": 0.35 },
      "chart_tags": ["unitarity", "collapse", "decoherence", "observer_interface"],
      "interface_variables": ["Born_rule", "pointer_basis"],
      "claim_temptations": ["P", "M"],
      "invariants": [
        {
          "id": "I-QM-001",
          "name": "empirical_equivalence_class",
          "definition": "Different interpretations often match standard predictions over typical experiments.",
          "role": "regime_marker"
        }
      ],
      "discriminators": [
        {
          "id": "D-QM-001",
          "name": "Intervention beyond decoherence",
          "pattern": "intervention",
          "how_to": "Identify experiments that would differ between collapse models, Many-Worlds, and hidden-variable approaches, if any.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "Canonical L5 seam: the chart includes the observer; beware category errors between interpretation and new physics."
    },
    {
      "id": "Q000006",
      "title": "Arrow of time and low-entropy initial conditions",
      "domains": ["physics", "cosmology", "philosophy"],
      "summary": "Why does time appear directional and why did the universe begin in an extraordinarily low-entropy state enabling thermodynamic irreversibility?",
      "status": "open",
      "leak_profile": { "L1": 0.03, "L2": 0.06, "L3": 0.10, "L4": 0.20, "L5": 0.28, "L6": 0.33 },
      "chart_tags": ["entropy", "initial_conditions", "coarse_graining", "time_asymmetry"],
      "interface_variables": ["entropy", "phase_space_volume"],
      "claim_temptations": ["M", "P"],
      "invariants": [
        {
          "id": "I-TIME-001",
          "name": "second_law_regime",
          "definition": "Entropy increase holds robustly under coarse-grained macroscopic descriptions.",
          "role": "regime_marker"
        }
      ],
      "discriminators": [
        {
          "id": "D-TIME-001",
          "name": "Coarse-graining sensitivity tests",
          "pattern": "ablation",
          "how_to": "Vary coarse-graining schemes and track which asymmetries remain invariant vs which are artifacts.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "Strong L4/L5 mix: many paradoxes arise from confusing micro-reversibility with macro irreversibility."
    },
    {
      "id": "Q000007",
      "title": "Black hole information paradox",
      "domains": ["gravity", "qft", "cosmology", "quantum_foundations"],
      "summary": "Does black hole evaporation destroy information, and if not, where is it encoded without violating locality or unitarity?",
      "status": "open",
      "leak_profile": { "L1": 0.04, "L2": 0.10, "L3": 0.18, "L4": 0.14, "L5": 0.22, "L6": 0.32 },
      "chart_tags": ["unitarity_vs_locality", "horizon", "entropy_area", "evaporation"],
      "interface_variables": ["Page_curve", "horizon_structure"],
      "claim_temptations": ["P", "I"],
      "invariants": [
        {
          "id": "I-BH-001",
          "name": "unitarity_constraint",
          "definition": "Quantum evolution is assumed unitary in standard QFT; violations imply new physics.",
          "role": "budget"
        }
      ],
      "discriminators": [
        {
          "id": "D-BH-001",
          "name": "Consistency across descriptions",
          "pattern": "interface_scatter",
          "how_to": "Check whether proposed resolutions preserve unitarity while matching semiclassical limits and entropy constraints.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "A tight ChartBridge among GR, QFT, and quantum information; good motif generator."
    },
    {
      "id": "Q000008",
      "title": "Inflation and initial conditions",
      "domains": ["cosmology", "physics"],
      "summary": "What mechanism (if any) drove inflation, and what initial conditions are required to start inflation without fine-tuning?",
      "status": "contested",
      "leak_profile": { "L1": 0.05, "L2": 0.07, "L3": 0.12, "L4": 0.20, "L5": 0.18, "L6": 0.38 },
      "chart_tags": ["inflation_model_space", "fine_tuning", "primordial_perturbations"],
      "interface_variables": ["scalar_spectral_index", "tensor_to_scalar_ratio"],
      "claim_temptations": ["I", "P"],
      "invariants": [
        {
          "id": "I-INF-001",
          "name": "primordial_spectrum_fit",
          "definition": "Observed primordial perturbation statistics must be reproduced.",
          "role": "glue_key"
        }
      ],
      "discriminators": [
        {
          "id": "D-INF-001",
          "name": "Tensor-mode search",
          "pattern": "orthogonal_probe",
          "how_to": "Use CMB polarization constraints to separate inflation classes (or challenge inflation generically).",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "Often drifts into L5 (what counts as explanation for initial conditions). Keep interface variables explicit."
    },
    {
      "id": "Q000009",
      "title": "Baryogenesis: matter–antimatter asymmetry",
      "domains": ["physics", "cosmology", "qft"],
      "summary": "Why is there more matter than antimatter, and what mechanism generated the observed baryon asymmetry in the early universe?",
      "status": "open",
      "leak_profile": { "L1": 0.04, "L2": 0.06, "L3": 0.18, "L4": 0.18, "L5": 0.12, "L6": 0.42 },
      "chart_tags": ["CP_violation", "out_of_equilibrium", "early_universe"],
      "interface_variables": ["baryon_to_photon_ratio"],
      "claim_temptations": ["P", "I"],
      "invariants": [
        {
          "id": "I-COS-004",
          "name": "observed_asymmetry_value",
          "definition": "The baryon-to-photon ratio is tightly constrained by cosmological observations.",
          "role": "glue_key"
        }
      ],
      "discriminators": [
        {
          "id": "D-COS-004",
          "name": "Collider/EDM constraints",
          "pattern": "orthogonal_probe",
          "how_to": "Use EDM bounds and collider searches to prune baryogenesis mechanisms via CP-violation signatures.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "Nice example of discriminator transfer: 'orthogonal probes' outside the original inference channel."
    },
    {
      "id": "Q000010",
      "title": "Origin of life (abiogenesis)",
      "domains": ["bio", "chemistry", "complex_systems", "philosophy"],
      "summary": "How did self-sustaining, evolving chemical systems arise from prebiotic chemistry, and what were the necessary steps to reach heredity and metabolism?",
      "status": "open",
      "leak_profile": { "L1": 0.06, "L2": 0.10, "L3": 0.18, "L4": 0.22, "L5": 0.12, "L6": 0.32 },
      "chart_tags": ["prebiotic_networks", "autocatalysis", "compartmentalization", "information_to_function"],
      "interface_variables": ["replication_fidelity", "energy_flux"],
      "claim_temptations": ["M", "I"],
      "invariants": [
        {
          "id": "I-BIO-001",
          "name": "heredity_threshold",
          "definition": "A minimal fidelity/selection regime enabling cumulative evolution.",
          "role": "regime_marker"
        }
      ],
      "discriminators": [
        {
          "id": "D-BIO-001",
          "name": "Network autocatalysis tests",
          "pattern": "intervention",
          "how_to": "Construct/perturb chemical networks to test emergence of self-maintenance and replication-like dynamics.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "Huge L4/L6 zone: avoid naive 'random search' framing; focus on landscapes, constraints, compartments."
    },
    {
      "id": "Q000011",
      "title": "Protein folding speed vs astronomical conformations (Levinthal-style)",
      "domains": ["bio", "biophysics", "complex_systems"],
      "summary": "Proteins fold quickly despite enormous possible conformations, implying biased dynamics on structured landscapes rather than blind search.",
      "status": "partially_resolved",
      "leak_profile": { "L1": 0.04, "L2": 0.08, "L3": 0.22, "L4": 0.32, "L5": 0.06, "L6": 0.28 },
      "chart_tags": ["energy_landscape", "funnel", "coarse_graining", "traps"],
      "interface_variables": ["free_energy", "fold_time"],
      "claim_temptations": ["I", "M"],
      "invariants": [
        {
          "id": "I-BIO-002",
          "name": "fold_time_distribution",
          "definition": "Across seeds/conditions, folding times cluster within regimes; traps are structured.",
          "role": "summary"
        }
      ],
      "discriminators": [
        {
          "id": "D-BIO-002",
          "name": "Annealing/hysteresis perturbations",
          "pattern": "stress_ramp",
          "how_to": "Vary temperature/noise schedules to separate funnel dynamics from trap-dominated regimes.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "Anchor for CI demonstration: paradox dissolves under correct chart (landscape)."
    },
    {
      "id": "Q000012",
      "title": "Morphogenesis: robust form from noisy components",
      "domains": ["bio", "complex_systems", "math"],
      "summary": "How do organisms reliably develop consistent structures despite stochastic gene expression, variable environments, and noisy cellular dynamics?",
      "status": "open",
      "leak_profile": { "L1": 0.05, "L2": 0.12, "L3": 0.20, "L4": 0.30, "L5": 0.08, "L6": 0.25 },
      "chart_tags": ["pattern_formation", "reaction_diffusion", "control", "robustness"],
      "interface_variables": ["morphogen_gradients", "boundary_conditions"],
      "claim_temptations": ["I", "M"],
      "invariants": [
        {
          "id": "I-BIO-003",
          "name": "shape_robustness",
          "definition": "Pattern outcomes remain stable under perturbations within a regime of parameters.",
          "role": "glue_key"
        }
      ],
      "discriminators": [
        {
          "id": "D-BIO-003",
          "name": "Ablate pathway / perturbation response",
          "pattern": "ablation",
          "how_to": "Remove or weaken a control pathway and quantify which invariants break vs persist.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "Strong L4/L3: defects localize; interfaces/boundaries often dominate outcomes."
    },
    {
      "id": "Q000013",
      "title": "Consciousness: the hard problem / what-it’s-like",
      "domains": ["cog_sci", "neuroscience", "philosophy"],
      "summary": "How do subjective experiences arise from physical processes, and what would count as a satisfying explanation across first- and third-person charts?",
      "status": "open",
      "leak_profile": { "L1": 0.03, "L2": 0.06, "L3": 0.06, "L4": 0.10, "L5": 0.40, "L6": 0.35 },
      "chart_tags": ["first_person", "third_person", "phenomenology", "mechanism_gap"],
      "interface_variables": ["report", "access", "integration"],
      "claim_temptations": ["M", "P"],
      "invariants": [
        {
          "id": "I-COG-001",
          "name": "chart_interface_constraint",
          "definition": "Any account must map between first-person structure and third-person interventions without collapsing one into the other.",
          "role": "budget"
        }
      ],
      "discriminators": [
        {
          "id": "D-COG-001",
          "name": "Intervention vs report dissociation",
          "pattern": "intervention",
          "how_to": "Use dissociations (e.g., unconscious processing, blindsight-like cases) to separate reportability from experience claims.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "High L5/L6: many positions are empirically equivalent at current resolution; emphasize interface variables."
    },
    {
      "id": "Q000014",
      "title": "Binding problem: unity of perception and representation",
      "domains": ["cog_sci", "neuroscience", "complex_systems"],
      "summary": "How does the brain bind distributed features into unified percepts and maintain coherent representations over time and context?",
      "status": "open",
      "leak_profile": { "L1": 0.04, "L2": 0.10, "L3": 0.18, "L4": 0.22, "L5": 0.16, "L6": 0.30 },
      "chart_tags": ["integration", "synchrony", "attention", "global_workspace"],
      "interface_variables": ["attention", "temporal_binding_window"],
      "claim_temptations": ["I", "M"],
      "invariants": [
        {
          "id": "I-COG-002",
          "name": "perceptual_coherence",
          "definition": "Percepts remain stable under noise and changing sensory input within limits.",
          "role": "glue_key"
        }
      ],
      "discriminators": [
        {
          "id": "D-COG-002",
          "name": "Ablation of integration pathways",
          "pattern": "ablation",
          "how_to": "Perturb candidate binding mechanisms and measure breakdown modes as structured residuals.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "Naturally connects to morphogenesis via shared robustness + interface seams."
    },
    {
      "id": "Q000015",
      "title": "Personal identity over time",
      "domains": ["philosophy", "cog_sci", "ethics"],
      "summary": "What makes a person the same individual over time: memory, body, continuity of values, narrative, or something else entirely?",
      "status": "contested",
      "leak_profile": { "L1": 0.02, "L2": 0.06, "L3": 0.05, "L4": 0.18, "L5": 0.38, "L6": 0.31 },
      "chart_tags": ["narrative_self", "continuity", "copy_branching", "normative_constraints"],
      "interface_variables": ["memory_continuity", "policy_stability", "accountability"],
      "claim_temptations": ["M", "A"],
      "invariants": [
        {
          "id": "I-PHI-001",
          "name": "accountability_continuity",
          "definition": "Practices of responsibility and commitment persist even when metaphysical identity is disputed.",
          "role": "regime_marker"
        }
      ],
      "discriminators": [
        {
          "id": "D-PHI-001",
          "name": "Branching/copy thought experiments",
          "pattern": "stress_ramp",
          "how_to": "Vary degrees of copying, replacement, and memory editing; track which identity invariants you refuse to give up.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "CI framing: identity as invariants under transformations + social interface constraints."
    },
    {
      "id": "Q000016",
      "title": "Agency and free will under physical law",
      "domains": ["philosophy", "cog_sci", "physics", "ethics"],
      "summary": "How can agency be a real causal locus if physical dynamics are deterministic or stochastic, and what role do levels of description play?",
      "status": "open",
      "leak_profile": { "L1": 0.03, "L2": 0.08, "L3": 0.08, "L4": 0.25, "L5": 0.28, "L6": 0.28 },
      "chart_tags": ["levels_of_description", "control", "counterfactuals", "responsibility"],
      "interface_variables": ["counterfactual_control", "policy_constraints"],
      "claim_temptations": ["M", "A"],
      "invariants": [
        {
          "id": "I-PHI-002",
          "name": "counterfactual_sensitivity",
          "definition": "Agency claims hinge on counterfactual dependence of outcomes on internal policies.",
          "role": "glue_key"
        }
      ],
      "discriminators": [
        {
          "id": "D-PHI-002",
          "name": "Interventionist causality tests",
          "pattern": "intervention",
          "how_to": "Use causal models: vary internal state/policy and test outcome dependence while holding environment fixed.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "Bridges causality theory and identity; avoid collapsing normative and descriptive layers."
    },
    {
      "id": "Q000017",
      "title": "Emergence and reduction: when higher-level laws are real",
      "domains": ["philosophy", "complex_systems", "physics", "math"],
      "summary": "When do higher-level patterns warrant their own explanatory status, and how do they relate to underlying microdynamics without being epiphenomenal?",
      "status": "open",
      "leak_profile": { "L1": 0.03, "L2": 0.10, "L3": 0.12, "L4": 0.32, "L5": 0.20, "L6": 0.23 },
      "chart_tags": ["coarse_graining", "universality", "effective_theories", "levels"],
      "interface_variables": ["renormalization_group", "order_parameters"],
      "claim_temptations": ["M", "I"],
      "invariants": [
        {
          "id": "I-CS-001",
          "name": "universality_class",
          "definition": "Many microdetails wash out; macro behavior is governed by a smaller set of parameters.",
          "role": "glue_key"
        }
      ],
      "discriminators": [
        {
          "id": "D-CS-001",
          "name": "Ensemble + coarse-grain invariance checks",
          "pattern": "ensemble_split",
          "how_to": "Vary micro-implementations and coarse-graining schemes; see which macro laws persist.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "A structural keystone for CI; links folding, morphogenesis, and time’s arrow."
    },
    {
      "id": "Q000018",
      "title": "P vs NP and the limits of efficient computation",
      "domains": ["comp_sci", "math", "logic"],
      "summary": "Are problems whose solutions can be verified efficiently also solvable efficiently, and what does that imply for complexity and cryptography?",
      "status": "open",
      "leak_profile": { "L1": 0.02, "L2": 0.06, "L3": 0.06, "L4": 0.14, "L5": 0.20, "L6": 0.52 },
      "chart_tags": ["worst_case", "reductions", "proof_complexity", "computational_limits"],
      "interface_variables": ["polynomial_time", "verification_vs_search"],
      "claim_temptations": ["I", "M"],
      "invariants": [
        {
          "id": "I-CS-002",
          "name": "reduction_invariance",
          "definition": "Complexity classes are stable under polynomial-time reductions.",
          "role": "glue_key"
        }
      ],
      "discriminators": [
        {
          "id": "D-CS-002",
          "name": "Lower bound strategy transfer",
          "pattern": "interface_scatter",
          "how_to": "Compare proof techniques across models of computation; identify barriers (relativization, natural proofs, algebrization).",
          "transferable": false
        }
      ],
      "sources": [],
      "notes": "A pure L6 magnet: proof barriers function like structural seams."
    },
    {
      "id": "Q000019",
      "title": "Generalization and out-of-distribution robustness in machine learning",
      "domains": ["ml", "comp_sci", "statistics"],
      "summary": "Why do modern models generalize, when do they fail under distribution shift, and what invariants should training enforce to resist spurious correlations?",
      "status": "open",
      "leak_profile": { "L1": 0.04, "L2": 0.10, "L3": 0.22, "L4": 0.28, "L5": 0.06, "L6": 0.30 },
      "chart_tags": ["inductive_bias", "OOD_shift", "spurious_features", "scaling"],
      "interface_variables": ["loss_surface", "data_distribution"],
      "claim_temptations": ["I", "M"],
      "invariants": [
        {
          "id": "I-ML-001",
          "name": "robust_feature_invariance",
          "definition": "Performance should depend on causal/robust features rather than dataset-specific artifacts.",
          "role": "glue_key"
        }
      ],
      "discriminators": [
        {
          "id": "D-ML-001",
          "name": "Stress tests and dataset ablations",
          "pattern": "stress_ramp",
          "how_to": "Systematically shift distributions and ablate feature sets; track where failures localize as seams.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "Nice E3 transfer hub: discriminator patterns are portable to many scientific inference disputes."
    },
    {
      "id": "Q000020",
      "title": "Interpretability and alignment: understanding model behavior",
      "domains": ["ml", "philosophy", "ethics", "comp_sci"],
      "summary": "How can we reliably explain and control complex learned systems when their internal representations are opaque and their goals may diverge from ours?",
      "status": "open",
      "leak_profile": { "L1": 0.04, "L2": 0.10, "L3": 0.22, "L4": 0.20, "L5": 0.14, "L6": 0.30 },
      "chart_tags": ["mechanistic_interpretability", "objective_misalignment", "evaluation_gaps"],
      "interface_variables": ["objective", "capability", "interpretation"],
      "claim_temptations": ["A", "M"],
      "invariants": [
        {
          "id": "I-ML-002",
          "name": "behavioral_reliability",
          "definition": "Model behavior should remain stable under expected deployment conditions and adversarial perturbations.",
          "role": "budget"
        }
      ],
      "discriminators": [
        {
          "id": "D-ML-002",
          "name": "Intervention + interpretability cross-check",
          "pattern": "intervention",
          "how_to": "Manipulate internal circuits/features and test whether explanations predict behavioral changes.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "Strong L3/L6: failure modes are structured residuals; interpretability is an interface-variable project."
    },
    {
      "id": "Q000021",
      "title": "Causality: inferring interventions from observations",
      "domains": ["statistics", "ml", "philosophy", "comp_sci"],
      "summary": "When can causal structure be identified from data, and what assumptions are necessary to infer intervention effects from purely observational distributions?",
      "status": "open",
      "leak_profile": { "L1": 0.04, "L2": 0.12, "L3": 0.18, "L4": 0.18, "L5": 0.14, "L6": 0.34 },
      "chart_tags": ["causal_graphs", "identifiability", "counterfactuals", "confounding"],
      "interface_variables": ["do_operator", "confounders"],
      "claim_temptations": ["I", "M"],
      "invariants": [
        {
          "id": "I-STAT-001",
          "name": "identifiability_conditions",
          "definition": "Causal effects are only identifiable under explicit assumptions about graph structure and confounding.",
          "role": "budget"
        }
      ],
      "discriminators": [
        {
          "id": "D-STAT-001",
          "name": "Interventions / natural experiments",
          "pattern": "intervention",
          "how_to": "Use randomized interventions or quasi-experimental variation to separate causal from correlational hypotheses.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "A direct methodological keystone for CI routing: it formalizes ‘discriminator’ logic."
    },
    {
      "id": "Q000022",
      "title": "Gödel incompleteness and the limits of formal systems",
      "domains": ["logic", "math", "philosophy", "comp_sci"],
      "summary": "In sufficiently expressive systems, some truths are unprovable within the system; what does this imply for foundations and mechanized reasoning?",
      "status": "partially_resolved",
      "leak_profile": { "L1": 0.02, "L2": 0.06, "L3": 0.06, "L4": 0.10, "L5": 0.34, "L6": 0.42 },
      "chart_tags": ["self_reference", "provability", "meta_theory", "consistency"],
      "interface_variables": ["provability_predicate", "meta_system"],
      "claim_temptations": ["M", "I"],
      "invariants": [
        {
          "id": "I-LOG-001",
          "name": "meta_level_escape",
          "definition": "Proving consistency/completeness generally requires stepping to a stronger meta-system.",
          "role": "regime_marker"
        }
      ],
      "discriminators": [
        {
          "id": "D-LOG-001",
          "name": "Strength comparison across systems",
          "pattern": "interface_scatter",
          "how_to": "Compare what becomes provable when moving between formal systems; track costs of added axioms.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "An explicit L5 engine: self-reference forces interface thinking; resonates with your ‘ground’ discussions."
    },
    {
      "id": "Q000023",
      "title": "Physical Church–Turing and computation in nature",
      "domains": ["physics", "comp_sci", "philosophy"],
      "summary": "What are the true limits of computation in physical reality, and can physical processes exceed classical computability assumptions?",
      "status": "open",
      "leak_profile": { "L1": 0.03, "L2": 0.08, "L3": 0.10, "L4": 0.16, "L5": 0.24, "L6": 0.39 },
      "chart_tags": ["computability", "physical_limits", "hypercomputation", "resource_bounds"],
      "interface_variables": ["energy_time_tradeoffs", "noise_limits"],
      "claim_temptations": ["M", "P"],
      "invariants": [
        {
          "id": "I-CS-003",
          "name": "resource_boundedness",
          "definition": "Physical computation is limited by resources (energy, time, noise, precision).",
          "role": "budget"
        }
      ],
      "discriminators": [
        {
          "id": "D-CS-003",
          "name": "Noise/precision stress tests",
          "pattern": "stress_ramp",
          "how_to": "Analyze whether proposed super-Turing schemes survive realistic noise, finite precision, and resource scaling.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "ChartBridge between logic/computation limits and physics constraints; high risk of P-temptation."
    },
    {
      "id": "Q000024",
      "title": "Value grounding and metaethics",
      "domains": ["ethics", "philosophy", "cog_sci"],
      "summary": "Are moral truths objective, constructed, or instrumental, and what grounds normativity without collapsing into preference or mere social convention?",
      "status": "contested",
      "leak_profile": { "L1": 0.02, "L2": 0.05, "L3": 0.04, "L4": 0.12, "L5": 0.45, "L6": 0.32 },
      "chart_tags": ["normativity", "objectivity", "constructivism", "social_contracts"],
      "interface_variables": ["reasons", "commitments"],
      "claim_temptations": ["A", "M"],
      "invariants": [
        {
          "id": "I-ETH-001",
          "name": "coordination_pressure",
          "definition": "Human communities face stable coordination constraints regardless of metaethical stance.",
          "role": "regime_marker"
        }
      ],
      "discriminators": [
        {
          "id": "D-ETH-001",
          "name": "Reflective equilibrium under stress",
          "pattern": "stress_ramp",
          "how_to": "Vary scenarios and constraints; track which normative commitments remain invariant vs collapse.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "Keep descriptive vs normative layers explicit; expect L5 to dominate."
    },
    {
      "id": "Q000025",
      "title": "Meaning and reference in language",
      "domains": ["philosophy", "cog_sci", "logic", "linguistics"],
      "summary": "How do words and concepts latch onto the world, and how do meaning, use, and reference relate across individual minds and social practice?",
      "status": "open",
      "leak_profile": { "L1": 0.02, "L2": 0.08, "L3": 0.06, "L4": 0.18, "L5": 0.36, "L6": 0.30 },
      "chart_tags": ["semantics_pragmatics", "reference", "social_language_games", "concepts"],
      "interface_variables": ["use", "truth_conditions"],
      "claim_temptations": ["M", "I"],
      "invariants": [
        {
          "id": "I-LANG-001",
          "name": "communication_success",
          "definition": "Meaning must support reliable coordination and prediction in communicative practice.",
          "role": "glue_key"
        }
      ],
      "discriminators": [
        {
          "id": "D-LANG-001",
          "name": "Ablation of context vs truth conditions",
          "pattern": "ablation",
          "how_to": "Test which meaning phenomena require context/pragmatics vs which behave like stable truth-conditional content.",
          "transferable": true
        }
      ],
      "sources": [],
      "notes": "Strong CI relevance: meaning is an interface variable across minds, world, and social norms."
    }
  ],
  "edges": [
    {
      "id": "E000001",
      "source": "Q000001",
      "target": "Q000003",
      "type": "E4_ChartBridge",
      "weight": 0.85,
      "justification": "Both questions share the interface variable w(z)/Λ and the expansion-history glue; treating Λ as constant vs dynamical is a direct chart-bridge that reframes the ‘smallness’ issue into observational discriminators.",
      "evidence_refs": [],
      "tags": ["Lambda", "w(z)"]
    },
    {
      "id": "E000002",
      "source": "Q000002",
      "target": "Q000003",
      "type": "E4_ChartBridge",
      "weight": 0.78,
      "justification": "Hubble tension often localizes at the early/late glue via rd and H(z); dynamical dark energy or early-time modifications can shift inferred distances, making these questions adjacent via shared interface variables.",
      "evidence_refs": [],
      "tags": ["H0", "rd"]
    },
    {
      "id": "E000003",
      "source": "Q000002",
      "target": "Q000019",
      "type": "E3_DiscriminatorTransfer",
      "weight": 0.62,
      "justification": "The structural problem is underdetermination under distribution shift: different modeling assumptions fit training data (CMB) but diverge when tested on shifted regimes (late-time probes). ML stress tests and ablations transfer as discriminator patterns.",
      "evidence_refs": [],
      "tags": ["OOD", "stress_tests"]
    },
    {
      "id": "E000004",
      "source": "Q000001",
      "target": "Q000017",
      "type": "E1_SharedLeak",
      "weight": 0.66,
      "justification": "Both express an effective-theory seam: macro behavior is stable while micro-level ‘naturalness’ expectations do not map cleanly to observed parameters, highlighting L4/L5 issues around coarse-graining and what counts as explanation.",
      "evidence_refs": [],
      "tags": ["EFT", "coarse_graining"]
    },
    {
      "id": "E000005",
      "source": "Q000004",
      "target": "Q000007",
      "type": "E4_ChartBridge",
      "weight": 0.86,
      "justification": "Black hole information is a forcing function for quantum gravity: any UV-complete framework must reconcile horizon thermodynamics, unitarity, and semiclassical limits; BH paradox is an interface testbed.",
      "evidence_refs": [],
      "tags": ["unitarity", "horizon"]
    },
    {
      "id": "E000006",
      "source": "Q000005",
      "target": "Q000007",
      "type": "E2_ComplementaryLeak",
      "weight": 0.70,
      "justification": "Measurement outcomes and black hole evaporation both press on unitarity vs definiteness/locality; ‘where does information go’ and ‘where do outcomes come from’ are dual-looking seams across different physical interfaces.",
      "evidence_refs": [],
      "tags": ["unitarity", "information"]
    },
    {
      "id": "E000007",
      "source": "Q000006",
      "target": "Q000008",
      "type": "E4_ChartBridge",
      "weight": 0.64,
      "justification": "Arrow-of-time questions hinge on initial conditions; inflation is often invoked as an explanatory bridge but also inherits its own initial-condition/fine-tuning seams, linking them via the ‘initial state’ interface.",
      "evidence_refs": [],
      "tags": ["initial_conditions"]
    },
    {
      "id": "E000008",
      "source": "Q000006",
      "target": "Q000017",
      "type": "E1_SharedLeak",
      "weight": 0.72,
      "justification": "Both are dominated by coarse-graining: macro asymmetry and macro laws emerge despite micro reversibility or micro diversity; the paradoxes dissolve only when the correct invariants under coarse-grain are specified.",
      "evidence_refs": [],
      "tags": ["L4", "coarse_graining"]
    },
    {
      "id": "E000009",
      "source": "Q000010",
      "target": "Q000011",
      "type": "E1_SharedLeak",
      "weight": 0.67,
      "justification": "Both are often misframed as blind search in astronomical spaces; both become tractable when posed as biased dynamics on structured landscapes with constraints and compartmentalization (L4/L6 chart correction).",
      "evidence_refs": [],
      "tags": ["landscape", "search_space"]
    },
    {
      "id": "E000010",
      "source": "Q000011",
      "target": "Q000019",
      "type": "E3_DiscriminatorTransfer",
      "weight": 0.73,
      "justification": "Folding funnels and ML generalization both support discriminator patterns: stress ramps, ablations, and ensemble splits reveal whether success is robust invariance or brittle overfitting to a narrow regime.",
      "evidence_refs": [],
      "tags": ["stress_ramp", "ensemble"]
    },
    {
      "id": "E000011",
      "source": "Q000011",
      "target": "Q000017",
      "type": "E4_ChartBridge",
      "weight": 0.69,
      "justification": "Protein folding is a concrete case of emergence: macro structure is governed by a reduced set of landscape features despite huge micro possibilities; it bridges ‘emergent law’ discussions via explicit invariants and traps.",
      "evidence_refs": [],
      "tags": ["emergence", "invariants"]
    },
    {
      "id": "E000012",
      "source": "Q000012",
      "target": "Q000017",
      "type": "E4_ChartBridge",
      "weight": 0.74,
      "justification": "Morphogenesis provides a worked example of universality and boundary-driven outcomes; it is a chart-bridge for emergence by supplying measurable invariants (robust pattern outcomes) and structured defect modes.",
      "evidence_refs": [],
      "tags": ["pattern_formation", "robustness"]
    },
    {
      "id": "E000013",
      "source": "Q000012",
      "target": "Q000014",
      "type": "E1_SharedLeak",
      "weight": 0.63,
      "justification": "Both concern binding/integration across distributed components: cells into tissues, features into percepts. In each case, coherence is an emergent invariant and defects localize at interfaces (L3/L4).",
      "evidence_refs": [],
      "tags": ["integration", "interfaces"]
    },
    {
      "id": "E000014",
      "source": "Q000013",
      "target": "Q000014",
      "type": "E4_ChartBridge",
      "weight": 0.71,
      "justification": "Binding is a mechanistic bridge problem for consciousness accounts: if global unity fails, ‘what-it’s-like’ narratives lose coherence. The interface variable is integration/access.",
      "evidence_refs": [],
      "tags": ["integration", "access"]
    },
    {
      "id": "E000015",
      "source": "Q000013",
      "target": "Q000015",
      "type": "E2_ComplementaryLeak",
      "weight": 0.68,
      "justification": "Consciousness asks what grounds first-person experience; identity asks what grounds continuity of the subject. They are complementary seams across the same first/third-person interface (L5/L6).",
      "evidence_refs": [],
      "tags": ["first_person", "continuity"]
    },
    {
      "id": "E000016",
      "source": "Q000015",
      "target": "Q000024",
      "type": "E4_ChartBridge",
      "weight": 0.66,
      "justification": "Personal identity connects to value grounding via accountability and commitment invariants; both are partly constituted by social practices and normativity, making the interface variable ‘reasons/commitments’.",
      "evidence_refs": [],
      "tags": ["normativity", "commitments"]
    },
    {
      "id": "E000017",
      "source": "Q000016",
      "target": "Q000021",
      "type": "E4_ChartBridge",
      "weight": 0.80,
      "justification": "Agency claims can be made precise via interventionist causality: the interface variable is counterfactual dependence under do-operations. Causal identifiability is the glue discipline for free-will debates.",
      "evidence_refs": [],
      "tags": ["do_operator", "counterfactuals"]
    },
    {
      "id": "E000018",
      "source": "Q000021",
      "target": "Q000019",
      "type": "E3_DiscriminatorTransfer",
      "weight": 0.70,
      "justification": "Causal inference provides discriminator templates for ML generalization: ablate confounders, test interventions, and separate spurious correlations from robust features under distribution shift.",
      "evidence_refs": [],
      "tags": ["causality", "spurious"]
    },
    {
      "id": "E000019",
      "source": "Q000020",
      "target": "Q000019",
      "type": "E4_ChartBridge",
      "weight": 0.62,
      "justification": "Interpretability and generalization share the interface variable of ‘what internal representations track’; failures in either show up as structured residuals under stress tests and targeted interventions.",
      "evidence_refs": [],
      "tags": ["representations", "stress_tests"]
    },
    {
      "id": "E000020",
      "source": "Q000022",
      "target": "Q000018",
      "type": "E1_SharedLeak",
      "weight": 0.65,
      "justification": "Both exhibit proof/knowledge barriers: you can formalize problems sharply, yet face structural limits on what can be proven within a given system or technique set (L5/L6).",
      "evidence_refs": [],
      "tags": ["proof_limits", "barriers"]
    },
    {
      "id": "E000021",
      "source": "Q000022",
      "target": "Q000025",
      "type": "E2_ComplementaryLeak",
      "weight": 0.60,
      "justification": "Self-reference and meta-level shifts haunt both provability and meaning: language about language and proofs about proofs force interface discipline and can generate apparent paradoxes (L5).",
      "evidence_refs": [],
      "tags": ["self_reference", "meta"]
    },
    {
      "id": "E000022",
      "source": "Q000023",
      "target": "Q000018",
      "type": "E4_ChartBridge",
      "weight": 0.63,
      "justification": "Computational complexity classes are charted abstractly, but physical computation introduces resource constraints (noise, precision, energy). The bridge is ‘what computation is physically realizable’.",
      "evidence_refs": [],
      "tags": ["resources", "computability"]
    },
    {
      "id": "E000023",
      "source": "Q000023",
      "target": "Q000006",
      "type": "E1_SharedLeak",
      "weight": 0.58,
      "justification": "Both raise coarse-graining and resource questions: time direction and computation limits depend on macroscopic constraints and available resources; naive microscopic pictures mislead (L4/L5).",
      "evidence_refs": [],
      "tags": ["resources", "coarse_graining"]
    },
    {
      "id": "E000024",
      "source": "Q000009",
      "target": "Q000004",
      "type": "E4_ChartBridge",
      "weight": 0.60,
      "justification": "Baryogenesis mechanisms may rely on beyond-Standard-Model physics that interfaces with quantum gravity-scale assumptions; while not directly dependent, both are pruned by consistency and UV completion constraints.",
      "evidence_refs": [],
      "tags": ["UV_completion"]
    },
    {
      "id": "E000025",
      "source": "Q000008",
      "target": "Q000001",
      "type": "E2_ComplementaryLeak",
      "weight": 0.57,
      "justification": "Inflation and Λ both function as ‘cosmic explanatory patches’ that succeed observationally yet raise naturalness/initial-condition questions; they are complementary seams about what counts as explanation in cosmology.",
      "evidence_refs": [],
      "tags": ["patch", "naturalness"]
    },
    {
      "id": "E000026",
      "source": "Q000007",
      "target": "Q000006",
      "type": "E4_ChartBridge",
      "weight": 0.61,
      "justification": "Black hole thermodynamics connects entropy, information, and time asymmetry through horizon dynamics; it bridges arrow-of-time discussions via entropy accounting under extreme conditions.",
      "evidence_refs": [],
      "tags": ["entropy", "information"]
    },
    {
      "id": "E000027",
      "source": "Q000005",
      "target": "Q000013",
      "type": "E1_SharedLeak",
      "weight": 0.64,
      "justification": "Both are observer-interface problems: measurement and consciousness each place the observer inside the chart, amplifying L5 seams about what can be explained within the system describing itself.",
      "evidence_refs": [],
      "tags": ["observer", "interface"]
    },
    {
      "id": "E000028",
      "source": "Q000016",
      "target": "Q000015",
      "type": "E4_ChartBridge",
      "weight": 0.59,
      "justification": "Agency over time depends on identity invariants (policy stability, commitments). Identity debates set the domain of validity for responsibility claims in agency discussions.",
      "evidence_refs": [],
      "tags": ["responsibility", "continuity"]
    },
    {
      "id": "E000029",
      "source": "Q000024",
      "target": "Q000020",
      "type": "E3_DiscriminatorTransfer",
      "weight": 0.60,
      "justification": "Alignment work imports metaethical seam structure: ‘what should the system do’ requires explicit normativity handling; reflective-equilibrium stress tests transfer as discriminator patterns.",
      "evidence_refs": [],
      "tags": ["normativity", "stress_tests"]
    },
    {
      "id": "E000030",
      "source": "Q000025",
      "target": "Q000020",
      "type": "E4_ChartBridge",
      "weight": 0.58,
      "justification": "Interpretability relies on meaning-like mappings from internal states to external descriptions; semantics/pragmatics is a chart bridge for how explanations latch onto behavior.",
      "evidence_refs": [],
      "tags": ["explanations", "meaning"]
    },
    {
      "id": "E000031",
      "source": "Q000010",
      "target": "Q000012",
      "type": "E1_SharedLeak",
      "weight": 0.59,
      "justification": "Both require robust organization from noisy components and rely on constraints/compartments. ‘Random search’ framings fail; landscape + interface constraints dominate (L4/L3).",
      "evidence_refs": [],
      "tags": ["robustness", "compartments"]
    },
    {
      "id": "E000032",
      "source": "Q000014",
      "target": "Q000017",
      "type": "E1_SharedLeak",
      "weight": 0.61,
      "justification": "Binding is an emergence problem: macro unity arises from micro distributed activity, with order parameters and integration constraints acting as invariants under coarse-graining (L4).",
      "evidence_refs": [],
      "tags": ["emergence", "integration"]
    },
    {
      "id": "E000033",
      "source": "Q000019",
      "target": "Q000017",
      "type": "E4_ChartBridge",
      "weight": 0.62,
      "justification": "Generalization questions are modern emergence problems: macro competence arises despite many micro parameterizations, suggesting universality-like behavior under training dynamics and data constraints.",
      "evidence_refs": [],
      "tags": ["universality", "training_dynamics"]
    },
    {
      "id": "E000034",
      "source": "Q000006",
      "target": "Q000022",
      "type": "E2_ComplementaryLeak",
      "weight": 0.55,
      "justification": "The arrow of time asks for a ground of asymmetry; incompleteness shows that grounds often require stepping outside the system. Both cultivate L5 humility about ‘final explanations’.",
      "evidence_refs": [],
      "tags": ["ground", "meta_level"]
    },
    {
      "id": "E000035",
      "source": "Q000001",
      "target": "Q000007",
      "type": "E1_SharedLeak",
      "weight": 0.57,
      "justification": "Both involve deep tension between gravitational coupling and quantum information/energy accounting; vacuum energy and horizon entropy each stress how ‘stuff’ contributes to curvature and information flow.",
      "evidence_refs": [],
      "tags": ["gravity_quantum_seam"]
    },
    {
      "id": "E000036",
      "source": "Q000003",
      "target": "Q000006",
      "type": "E4_ChartBridge",
      "weight": 0.54,
      "justification": "Dark energy dynamics can affect late-time structure and may interact with time-asymmetry narratives via horizon thermodynamics and entropy accounting, providing a weak but meaningful chart bridge.",
      "evidence_refs": [],
      "tags": ["horizons", "entropy"]
    },
    {
      "id": "E000037",
      "source": "Q000023",
      "target": "Q000019",
      "type": "E1_SharedLeak",
      "weight": 0.56,
      "justification": "Both are about limits under noise/resources: ML generalization collapses under certain shifts; physical computation proposals collapse under precision/noise scaling, highlighting similar stress-ramp seams.",
      "evidence_refs": [],
      "tags": ["noise", "resources"]
    },
    {
      "id": "E000038",
      "source": "Q000021",
      "target": "Q000020",
      "type": "E3_DiscriminatorTransfer",
      "weight": 0.66,
      "justification": "Alignment and interpretability can borrow causal-discovery discriminators: interventions and counterfactual tests separate ‘mere correlation explanations’ from mechanisms that genuinely control outcomes.",
      "evidence_refs": [],
      "tags": ["interventions", "mechanisms"]
    },
    {
      "id": "E000039",
      "source": "Q000015",
      "target": "Q000025",
      "type": "E4_ChartBridge",
      "weight": 0.55,
      "justification": "Identity is stabilized by narrative and language; meaning/reference supplies the interface machinery by which selves are described, negotiated, and made accountable in social space.",
      "evidence_refs": [],
      "tags": ["narrative", "social_interface"]
    },
    {
      "id": "E000040",
      "source": "Q000013",
      "target": "Q000020",
      "type": "E2_ComplementaryLeak",
      "weight": 0.52,
      "justification": "Consciousness and interpretability both face a mapping seam between internal states and external descriptions; explanations can be behaviorally adequate yet fail the ‘what is it like’ or ‘what is it doing’ demands.",
      "evidence_refs": [],
      "tags": ["explanation_gap"]
    }
  ]
}
```
