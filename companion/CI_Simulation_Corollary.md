# CI Simulation Corollary

## Purpose
This document specifies how the current CI/LCG argument scaffold can be executed as a simulation-oriented workflow without making domain-truth claims. Everything here is framed as model-family comparison, chart translation, probe execution, and seam detection.

## Core Translation Rules

### 1) Discriminators -> Probes
Each discriminator becomes a probe contract:
- **Observable** in discriminator `how_to` becomes a measurable probe channel.
- **Split criterion** becomes probe pass/fail logic.
- **Transferable flag** becomes probe portability scope:
  - `true`: eligible for cross-node reuse (E3 candidates).
  - `false`: local diagnostic only.

### 2) Interface Variables -> Measurement Channels
Interface variables define cross-chart channel names. They are not outcomes; they are translation axes used when comparing charts.

Current channel vocabulary:
- `primitive budget / silent premise`
- `ledger stability / taxonomy drift`
- `observability equivalence class`
- `dimensionless drift`
- `orientation residue`
- `constraint-order coupling`
- `local arrow persistence`
- `loop/closure residue`

### 3) Edge Semantics in Simulation Terms
- **E3 (DiscriminatorTransfer)** -> *transfer*: same probe logic can be reused with bounded adaptation.
- **E4 (ChartBridge)** -> *reparameterize*: translate data between chart spaces along one interface variable.
- **E1 (SharedLeak)** -> *soft adjacency*: exploratory relation; do not treat as reusable transfer proof.

### 4) Seams -> Failure Modes
A seam is a repeatable failure signature where chart comparison or probe transfer breaks. In simulation terms, seam flags are first-class outputs, not debugging leftovers.

## Execution Model
A single simulation run is an iteration over:
1. Select node + chart mode.
2. Load associated probes (discriminator-bound).
3. Execute probe batch and write structured outputs.
4. Translate/compare against target node chart where an E3 or E4 edge exists.
5. Emit seam flags and ledger deltas.

## Evidence Discipline
- Probe outputs are evidence artifacts, not conclusions.
- Conclusions are limited to what invariants + discriminator splits support.
- Chart translation success does not imply transfer success.

## Mapping Table

| Discriminator pattern | Probe type | Expected outputs | Failure signatures |
|---|---|---|---|
| `interface_scatter` | Cross-chart scatter comparison | channel scatter matrix, stability score, admissibility tag | instability under chart shifts; channel mismatch; non-portable split |
| `orthogonal_probe` | Counterfactual axis isolation | axis contribution, primitive delta, branch outcomes | hidden assumption injection; axis collapse; role-swapping artifacts |
| `ensemble_split` | Model-family split test | family scores, split boundary, confidence spread | taxonomy explosion; unstable boundary; split inversion across runs |

## Worked Corollary by Spine Segment

### Method Spine (C1)
- `D-CI-001`, `D-CI-002`, `D-LCG-001`, `D-LCG-002` become procedural integrity probes.
- `E000023` and `E000024` are explicit reparameterization links for method->ontology handoff.
- Primary seam: **silent upgrade** (procedural validity incorrectly treated as ontic admissibility).

### Ontology Spine (C2)
- Orthogonal probes enforce regime-marker stability under re-description.
- E3 edges (`E000013`, `E000014`, `E000015`) become transfer candidates only when split criteria remain invariant.
- Primary seam: **reification drift** (relation-level claims turning into substance claims).

### Gauge/Detectability Spine (C3)
- Interface-scatter probes test chart-invariant channel behavior (`loop/closure residue`, `dimensionless drift`, `observability equivalence class`, `orientation residue`).
- E3 transfers (`E000010`, `E000012`) are valid only if admissibility channels remain stable.
- Primary seam: **chart-dependent observables masquerading as stable outputs**.

### Time/Identity Stress (C4)
- `D-TIM-002` evaluates local asymmetry persistence across chart shifts.
- E4 links (`E000016`, `E000019`) remain translation edges; they should not be reinterpreted as identity proofs.
- Primary seam: **global-orientation injection** that invalidates local persistence framing.

### Cognition Bridge (C5)
- `D-020-001` contributes a transfer hypothesis into differentiation behavior (`E000017`).
- Primary seam: **overclosure** (jumping from directional bias tests to full cognitive ontology).

## Operational Guardrails
- Every run logs interface-variable channel values, not only pass/fail labels.
- Every transfer claim must cite probe lineage (source probe -> adapted probe).
- Any E1-based move is marked “soft adjacency” in UI and reports.
- Any method->ontology move must pass `D-BRID-021` channel checks before publication-grade synthesis.

## Minimal Test Program
1. Run C1 probe batch over two chart modes and verify stable seam typing.
2. Execute handoff probes (`Q000008 -> Q000021 -> Q000011`) and validate no silent upgrade.
3. Run one C2 E3 transfer chain and one C3 E3 transfer chain.
4. Run C4 local-arrow persistence scatter with at least two chart modes.
5. Confirm ledger captures seam flags, failure signatures, and interface-variable drift trends.
