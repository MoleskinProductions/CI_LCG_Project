# Dev Workflow (CI_LCG Houdini Toolchain)

## 1) Run smoke checks
```bash
python tools/smoke_test_imports.py
python tools/smoke_test_paths.py
python tools/smoke_test_panel_import.py
```

## 2) Generate probe runs
```bash
python houdini_package/tools/ci_probe_cli.py --probe-id P-PRB-006 --chart-mode-id CHART-003 --seed 1
python houdini_package/tools/ci_probe_cli.py --probe-id P-PRB-004 --chart-mode-id CHART-002 --seed 9
python houdini_package/tools/ci_probe_cli.py --probe-id P-PRB-010 --chart-mode-id CHART-004 --seed 21
```

## 3) Generate suggestions headlessly
```bash
python tools/ci_suggest_cli.py --last-n 25 --append --limit 10
```

Outputs append to:
- `houdini_package/output/ledger/task_suggestions.jsonl`

## 4) Generate candidate patch (safe mode)
```bash
python tools/ci_patch_assistant.py --list --last-n 20
python tools/ci_patch_assistant.py --index 1
```

Outputs:
- `patches/PATCH-*.json`
- `patches/PATCH-*.md`
- `lcg/lcg_graph.patched.json`
- `reports/patch_verify_report.md`

## 5) Apply patch only when verification passes
```bash
python tools/ci_patch_assistant.py --index 1 --apply
```

If verify fails, apply is blocked unless `--force` is provided.

## 6) Houdini panel workflow
- Install package using `docs/INSTALL_HOUDINI_PANEL.md`.
- Open: **Python Panel -> CI Graph Overlay**.
- Use:
  - Single run mode for one run overlay
  - Aggregate mode for heatmap + task generation
  - Trend tab for recent-vs-previous window deltas
