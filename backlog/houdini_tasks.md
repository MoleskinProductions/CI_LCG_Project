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

## Production Alignment Trajectory (Integrated from production_spec.md, 2026-02-05)

## Phase 0 — Repo Reality Lock (Audit First)
1. Produce `reports/repo_audit.md` with verified file-path facts.
   - Done means audit lists panel locations, package file status, output paths, and risk list.

## Phase 1 — Path Centralization + Output Integrity
2. Add canonical resolver module `houdini_package/python/ci/paths.py`.
   - Done means panel + CLI + runner + ledger + patch assistant all resolve output/graph paths through one module.
3. Fix task suggestions path divergence.
   - Done means both UI and tools read/write `houdini_package/output/ledger/task_suggestions.jsonl` only.

## Phase 2 — Houdini 21 Packaging Hardening
4. Keep one canonical panel implementation (`houdini_package/python/ci_panels/CI_GraphOverlay_panel.py`) and retire duplicate under `houdini_package/ui/`.
   - Done means no duplicate runtime panel file is importable.
5. Normalize package wiring and panel discovery (`houdini_package/package.json`, `.pypanel`, install doc).
   - Done means panel is discoverable as "CI Graph Overlay" in Houdini 21.

## Phase 3 — Headless Workflow Completeness
6. Add `tools/ci_suggest_cli.py` for aggregate + task generation + optional JSONL append.
   - Done means probe -> ledger -> suggest -> patch assistant works without opening Houdini.

## Phase 4 — QA + Guardrails
7. Add smoke tests (`tools/smoke_test_imports.py`, `tools/smoke_test_paths.py`).
   - Done means import/path sanity checks pass in a clean shell.
8. Add `reports/repo_fix_summary.md` after migration.
   - Done means changed files, behavior impacts, and verification commands are documented.

## Phase 6 — Legacy Decommission Plan (Post-Stability)
9. Retire legacy package + panel shim after one stable window.
   - Done means `houdini_package/ci_package.json` and `houdini_package/ui/CI_GraphOverlay_panel.py` are removed no earlier than 2026-03-31, and Houdini discovery still passes via canonical files.
10. Keep deprecation checks green until removal date.
   - Done means `tools/check_legacy_shims.py` passes in CI and confirms shim remains a forwarder only.
