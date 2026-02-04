# Agent Routing Plan

## A1_CI_Method_Specialist (for C1_CI_Method)
- Mission: tighten method-node discriminator specificity and reduce overlap between formalization and entry-point leakage tests.
- Input scope: Q000002, Q000007, Q000008; source pieces P0228, P0338, P0350.
- Output contract: update `reports/discriminator_atlas.md` and `lcg/edge_justifications.md`; acceptance = each node has non-overlapping observable/split criteria and E3/E4 justifications cite chart variables explicitly.
- Do not touch: C2_Ontology_Ground_Inversion, C3_Physics_Gauge_Detectability, C4_Time_Identity, C5_Mind_Intentionality.

## A2_Ontology_Ground_Specialist (for C2_Ontology_Ground_Inversion)
- Mission: strengthen ontology-ground invariants and clarify inversion/division claims without importing physics assumptions.
- Input scope: Q000001, Q000004, Q000011, Q000012, Q000013, Q000014, Q000016, Q000017, Q000018; source pieces P0148, P0284, P0023, P0065, P0103, P0118, P0146, P0184, P0198.
- Output contract: update `lcg/lcg_graph.json` node invariants/discriminators for these nodes and refresh `reports/discriminator_atlas.md`; acceptance = no boilerplate invariant labels and each discriminator remains node-specific.
- Do not touch: C1_CI_Method, C3_Physics_Gauge_Detectability, C4_Time_Identity, C5_Mind_Intentionality.

## A3_Physics_Gauge_Specialist (for C3_Physics_Gauge_Detectability)
- Mission: sharpen detectability logic (loop residue, gauge-invariant observables, rescaling limits) and reconcile E4 vs E3 role boundaries.
- Input scope: Q000003, Q000005, Q000006, Q000009, Q000010; source pieces P0280, P0289, P0294, P0254, P0263.
- Output contract: update `lcg/lcg_graph.json`, `lcg/edge_justifications.md`, and `reports/discriminator_atlas.md`; acceptance = top-weight edges have explicit shared invariant/discriminator rationale and no duplicate discriminator semantics.
- Do not touch: C1_CI_Method, C2_Ontology_Ground_Inversion, C4_Time_Identity, C5_Mind_Intentionality.

## A4_Time_Identity_Specialist (for C4_Time_Identity)
- Mission: expand and stabilize local-arrow/identity framing and justify chart-bridge links into ontology.
- Input scope: Q000015, Q000019; source pieces P0124, P0217.
- Output contract: update `lcg/lcg_graph.json` and `lcg/edge_justifications.md`; acceptance = E4 bridge justifications name interface variables and at least one additional discriminator transfer candidate is proposed.
- Do not touch: C1_CI_Method, C2_Ontology_Ground_Inversion, C3_Physics_Gauge_Detectability, C5_Mind_Intentionality.

## A5_Mind_Intentionality_Specialist (for C5_Mind_Intentionality)
- Mission: deepen intentionality-without-desire treatment and make its dependency on ontology explicit but non-circular.
- Input scope: Q000020; source piece P0158.
- Output contract: update `lcg/lcg_graph.json` and `reports/discriminator_atlas.md`; acceptance = intentionality discriminator is operationalized with at least one measurable split criterion reusable by other cognition nodes.
- Do not touch: C1_CI_Method, C2_Ontology_Ground_Inversion, C3_Physics_Gauge_Detectability, C4_Time_Identity.

## A0_Integrator (cross-constellation)
- Mission: merge cross-constellation edge decisions, enforce discriminator hygiene, and resolve conflicts between specialist edits.
- Input scope: all cross edges (currently E000008, E000017, E000018, E000019) plus all bridge nodes.
- Output contract: update `qa/findings.md`, `qa/decision_log.md`, and finalize `lcg/lcg_graph.json`; acceptance = cross-edge justifications are non-redundant, discriminator meanings are non-duplicative, and unresolved conflicts are logged with explicit decision rationale.
- Do not touch: source transcript segmentation artifacts in `pieces/` and `index/`.
