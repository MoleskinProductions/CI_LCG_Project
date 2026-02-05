# Pathing Migration Notes (Phase 1)
Date: 2026-02-05

## What changed
- Added canonical path resolver: `houdini_package/python/ci/paths.py`.
- Migrated path resolution in:
  - `houdini_package/python/ci/registry.py`
  - `houdini_package/python/ci/schemas.py`
  - `houdini_package/python/ci/graph.py`
  - `houdini_package/python/ci/run_store.py`
  - `houdini_package/python/ci/runner.py`
  - `houdini_package/python/ci/ledger.py`
  - `houdini_package/python/ci_panels/CI_GraphOverlay_panel.py`
  - `tools/ci_patch_assistant.py`
- Aligned suggestions persistence path to canonical:
  - `houdini_package/output/ledger/task_suggestions.jsonl`
- Updated legacy panel copy (`houdini_package/ui/CI_GraphOverlay_panel.py`) to write/read the same suggestions path until duplicate-panel cleanup in Phase 2.

## Canonical directories now enforced
- Probe outputs: `houdini_package/output/probe_runs/`
- Ledger + suggestions: `houdini_package/output/ledger/`
- Patches: `patches/`
- Reports: `reports/`

## Environment overrides supported
- `CI_LCG_REPO_ROOT`
- `CI_LCG_GRAPH_PATH` (also accepts legacy `CI_LCG_GRAPH`)
- `CI_LCG_OUTPUT_DIR`
- `CI_LCG_PROBE_RUNS_DIR` (also accepts legacy `CI_OUTPUT_PROBE_DIR`)
- `CI_LCG_LEDGER_DIR` (also accepts legacy `CI_OUTPUT_LEDGER_DIR`)
- `CI_PROBE_REGISTRY`
- `CI_CHART_MODES`
- `CI_SCHEMA_PROBE_OUTPUT`
- `CI_SCHEMA_LEDGER_EVENT`
- `CI_SCHEMA_SEAM_FLAG`

## Quick verification
- Module import smoke succeeded for `ci.registry`, `ci.runner`, `ci.ledger`, `ci.graph`, `ci.run_store`.
- `ci.paths.task_suggestions_path()` resolves to `houdini_package/output/ledger/task_suggestions.jsonl`.
