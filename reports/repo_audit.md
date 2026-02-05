# Repo Audit (Trajectory Integration)
Date: 2026-02-05

## Verified current-state findings
- Canonical panel exists at `houdini_package/python/ci_panels/CI_GraphOverlay_panel.py` (PySide6-first with PySide2 fallback).
- Duplicate/obsolete panel still exists at `houdini_package/ui/CI_GraphOverlay_panel.py` (duplication risk).
- Houdini package file is currently `houdini_package/ci_package.json`; `houdini_package/package.json` is missing.
- Panel suggestion persistence currently resolves to `houdini_package/python/output/ledger/task_suggestions.jsonl` (from `parents[1]` pathing in panel), while other tools target `houdini_package/output/ledger/task_suggestions.jsonl`.
- Headless tooling gap remains: `tools/ci_suggest_cli.py` missing.
- Smoke test gaps remain: `tools/smoke_test_imports.py` and `tools/smoke_test_paths.py` missing.

## Glaring issues
1. Panel duplication can cause accidental imports and drift.
2. Task suggestion path mismatch can split provenance history across two files.
3. Missing canonical path module means path logic is scattered and fragile.
4. Missing headless suggestion CLI blocks full non-UI automation loop.

## Safe fixes (next trajectory phases)
1. Add `houdini_package/python/ci/paths.py` and migrate all path resolution to it.
2. Standardize task suggestions on `houdini_package/output/ledger/task_suggestions.jsonl`.
3. Keep only `houdini_package/python/ci_panels/CI_GraphOverlay_panel.py` as runtime panel source.
4. Add `tools/ci_suggest_cli.py` and smoke scripts to lock workflow quality.

## Risks / unknowns
- Houdini package discovery may depend on current `ci_package.json` behavior in user installs; migration to `package.json` should be tested in Houdini 21 before removing compatibility files.
- Existing persisted suggestions under `houdini_package/python/output/ledger/` may need one-time migration.
