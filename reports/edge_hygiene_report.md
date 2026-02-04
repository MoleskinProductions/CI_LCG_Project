# Edge Hygiene Report

## Edge changes in this pass
- Added edges: none.
- Removed edges: none.
- Type changes: none.
- Weight changes: none.
- Justification hardened (non-generic): E000002, E000003, E000004, E000005, E000006, E000007, E000010, E000011, E000012, E000013, E000014, E000015, E000016, E000017, E000018, E000019.

## E-rule compliance checks
- E3 steel-beam rule: all E3 justifications now explicitly include shared pattern, shared observable axis, and transfer rationale.
- E4 chart-translation rule: all E4 justifications now explicitly name one interface variable.
- E1 weak-similarity rule: all E1 edges remain at weight 0.4; no E1 pair duplicates an E3 pair.
- Edge budget rule: total edges remain 20 (<=40).

## Discriminator canonicalization actions
- Duplicate cluster addressed: formerly generic `orthogonal_probe` entries.
- Canonical anchor retained: D-CI-001.
- Rewrites: all discriminators now include node-specific `how_to` text with explicit observable and split criterion.
- Transferability flags tightened: node-local probes marked `transferable=false` (Q000005, Q000012, Q000016, Q000017, Q000018, Q000019).
- Pattern refinement: D-PHY-004 (Q000009) moved to `interface_scatter` to align with E000012 transfer semantics.

## Invariant hygiene actions
- Deduped repeated invariant name+definition within each node (no residual duplicates).
- Kept 1–2 invariants per node.
- Added role suffix to each invariant definition: `(glue_key | discriminator | regime_marker | budget | summary)`.

## PROVISIONAL nodes (need next discriminator work)
- Q000005: needs a second discriminator that links geometry/force framing to a measurable interface variable shared with C2/C4 bridge work.
- Q000008: needs an intervention-style discriminator for ledger robustness under adversarial taxonomy edits.
- Q000019: needs an interface-scatter companion discriminator tying local arrow persistence to concrete observability classes.


## C1_Method_Specialist update (2026-02-04)
- Edge justifications updated with concrete counterexamples: `E000002`, `E000003`, `E000004`, `E000011`.
- Discriminator split-criterion orthogonality tightened: `Q000002/D-CI-001` (primitive-budget formalization test), `Q000007/D-CI-002` (seam-visibility entry-framing test).
- New robustness discriminator added: `Q000008/D-LCG-002` (`ensemble_split`, transferable=true) for adversarial taxonomy relabeling stress.
- No node additions; no edge additions/removals/type changes.


## C4_Time_Identity_Specialist update (2026-02-04)
- Added discriminator `Q000019/D-TIM-002` (`Local-arrow persistence scatter test`, pattern=`interface_scatter`, transferable=true) with explicit cross-context observable and local-vs-global split criterion.
- Normalized `Q000018` existing discriminator id to `D-TIM-001` and sharpened its split criterion to keep it non-duplicate with Q000019 arrow-persistence tests.
- Added one relation edge `E000022` (`E3_DiscriminatorTransfer`, `Q000018 -> Q000019`, weight `0.6`) with explicit shared pattern, observable axis, and transfer rationale.
- Verified E4 bridge coverage for `E000019`: both endpoints (`Q000019`, `Q000017`) include interface variable `local arrow persistence`.


## C3_Physics_Gauge_Specialist update (2026-02-04)
- Hardened spine justifications: `E000010` now explicitly ties loop/closure residue to gauge-invariant operators and admissible observable class; `E000012` now includes an explicit unit-scaling failure case template.
- Confirmed/filled interface-variable coverage on E4 endpoints: `E000005` (`observability equivalence class`), `E000006` (`dimensionless drift`), `E000007` (`orientation residue`).
- Tightened discriminator orthogonality in C3 nodes: `D-PHY-001`, `D-PHY-003`, `D-PHY-004`, `D-PHY-005` now include one-sentence non-overlap clarifiers.
- Added schema hygiene fields on edited edges: `tags` and `evidence_refs` for `E000005`, `E000006`, `E000007`, `E000010`, `E000012`.


## A0.1 micro-hygiene update (2026-02-04)
- `E000022` schema fields added: `evidence_refs=["P0198","P0217"]`, `tags=["e3"]`.
- `E000016` resolved as `E4_ChartBridge` (not E3) because Q000015 and Q000019 do not expose a single explicit shared discriminator observable axis; updated type/weight/justification and set `tags=["e4"]` while preserving `evidence_refs`.


## C2_Ontology_Ground_Inversion_Specialist update (2026-02-04)
- Edited nodes: `Q000001`, `Q000004`, `Q000011`, `Q000012`, `Q000013`, `Q000014`, `Q000016`, `Q000017`, `Q000018`.
- Edited edges: `E000013`, `E000014`, `E000015` (internal spine justifications), `E000018`, `E000019` (interface-variable compliance check on C2 endpoints).
- Changes made: rewrote C2 invariant definitions into regime-marker form; sharpened C2 discriminator `how_to` axes to ontology-native observables/splits; hardened three E3 spine justifications with explicit shared axis, transfer logic, and one failure counterexample sentence each; verified/filled required interface variables on C2 endpoints for touching E4 bridges.
