#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path


def _bootstrap_path() -> None:
    repo = Path(__file__).resolve().parents[1]
    pkg_python = repo / "houdini_package" / "python"
    if str(pkg_python) not in sys.path:
        sys.path.insert(0, str(pkg_python))


def _check(name: str, fn):
    try:
        detail = fn()
        return True, name, detail
    except Exception as exc:
        return False, name, str(exc)


def main() -> int:
    _bootstrap_path()
    from ci import paths, registry, schemas

    checks = []

    checks.append(_check("repo_root exists", lambda: str(paths.repo_root())))
    checks.append(_check("lcg graph exists", lambda: str(paths.lcg_graph_path()) if paths.lcg_graph_path().exists() else (_ for _ in ()).throw(FileNotFoundError(paths.lcg_graph_path()))))
    checks.append(_check("registry load", lambda: f"probes={len(registry.load_registry()['probes'])}"))
    checks.append(_check("chart modes load", lambda: f"chart_modes={len(registry.load_chart_modes()['chart_modes'])}"))
    checks.append(_check("probe schema load", lambda: f"id={schemas.load_probe_output_schema().get('schema_id')}"))
    checks.append(_check("ledger schema load", lambda: f"id={schemas.load_ledger_event_schema().get('schema_id')}"))
    checks.append(_check("seam schema load", lambda: f"id={schemas.load_seam_flag_schema().get('schema_id')}"))

    def _task_suggestions_status() -> str:
        p = paths.task_suggestions_path()
        if not p.exists():
            return f"missing (ok): {p}"
        with p.open("r", encoding="utf-8") as f:
            lines = [ln.strip() for ln in f if ln.strip()]
        parsed = 0
        for ln in lines[-20:]:
            json.loads(ln)
            parsed += 1
        return f"exists: {p} (parsed_last={parsed})"

    checks.append(_check("task suggestions jsonl parse", _task_suggestions_status))

    paths.ensure_runtime_dirs()
    checks.append(_check("runtime dirs writable", lambda: f"{paths.probe_runs_dir()} | {paths.ledger_dir()}"))

    failed = [c for c in checks if not c[0]]
    for ok, name, detail in checks:
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {name}: {detail}")

    if failed:
        print("\nSuggested fixes:")
        print("- Verify env overrides (CI_LCG_* / CI_SCHEMA_* / CI_PROBE_REGISTRY / CI_CHART_MODES).")
        print("- Confirm expected files exist under companion/, lcg/, and reports/.")
        print("- Run tools/smoke_test_paths.py for detailed path output.")
        return 1

    print("\nOverall: PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
