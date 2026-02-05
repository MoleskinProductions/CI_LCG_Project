#!/usr/bin/env bash
set -euo pipefail

echo "[1/4] Smoke checks"
bash tools/precommit_smoke.sh
python tools/smoke_test_panel_import.py

echo "[2/4] Probe runs"
python houdini_package/tools/ci_probe_cli.py --probe-id P-PRB-006 --chart-mode-id CHART-003 --seed 1
python houdini_package/tools/ci_probe_cli.py --probe-id P-PRB-004 --chart-mode-id CHART-002 --seed 9
python houdini_package/tools/ci_probe_cli.py --probe-id P-PRB-010 --chart-mode-id CHART-004 --seed 21

echo "[3/4] Suggest + patch draft"
python tools/ci_suggest_cli.py --last-n 25 --append --limit 10
python tools/ci_patch_assistant.py --list --last-n 20
python tools/ci_patch_assistant.py --index 1

echo "[4/4] Done"
echo "Check reports/patch_verify_report.md before any --apply."
