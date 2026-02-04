# Houdini Implementation Backlog (A9.1 Bootstrap)

## Phase 1 — Configuration Baseline
1. Validate `companion/config/probe_registry.json` against markdown probe definitions.
   - Done means all probes `P-PRB-001`..`P-PRB-012` have discriminator IDs and interface variables matching `companion/Probe_Library.md`.
2. Validate `companion/config/chart_modes.json` for channel coverage.
   - Done means every interface variable used by any probe appears in at least one chart mode.

## Phase 2 — Schema Contract Lock
3. Review and lock `companion/schemas/probe_output.schema.json`.
   - Done means sample probe outputs for one C1, one C2, one C3/C4 probe validate successfully.
4. Review and lock `companion/schemas/ledger_event.schema.json`.
   - Done means ledger events can reference node-only and edge-linked decisions.
5. Review and lock `companion/schemas/seam_flag.schema.json`.
   - Done means seam flags can represent node, edge, and path scope with severity.

## Phase 3 — Data Flow Wiring (Spec-Only)
6. Define run artifact naming and ID policy (`RUN-######`, `PO-######`, `LE-######`, `SF-######`).
   - Done means one-page convention doc exists and is referenced by all schema examples.
7. Define probe execution order templates per chart mode.
   - Done means each chart mode has an ordered probe list and required input field checklist.

## Phase 4 — Path-Level Sanity Scenarios
8. Scenario A: Method stability path (`Q000002 -> Q000007 -> Q000008`).
   - Done means probe outputs show stable seam typing and no silent premise inflation.
9. Scenario B: Handoff path (`Q000008 -> Q000021 -> Q000011`).
   - Done means handoff fails when ontic claims are introduced without interface-variable accounting.
10. Scenario C: Detectability path (`Q000006 -> Q000003 -> Q000009 -> Q000010`).
   - Done means scaling drift and closure residue checks are both represented in seam flags.
11. Scenario D: Time persistence path (`Q000015 -> Q000019`).
   - Done means local arrow persistence can be evaluated without requiring global orientation constraint.

## Phase 5 — Sanity Checks (Release Gate)
12. Registry consistency check.
   - Done means every probe in registry maps to valid discriminator IDs present in `lcg/lcg_graph.json`.
13. Interface-variable consistency check.
   - Done means each probe’s interface variables exist in `reports/interface_variables.md`.
14. Schema version lock check.
   - Done means all generated artifacts declare `schema_version: 0.1.0` and pass schema validation.
15. Soft-edge handling check.
   - Done means any E1-driven scenario is explicitly labeled “soft adjacency” in reports.
