#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    pkg_python = repo / "houdini_package" / "python"
    if str(pkg_python) not in sys.path:
        sys.path.insert(0, str(pkg_python))

    from ci import paths

    paths.ensure_runtime_dirs()

    checks = [
        ("repo_root", paths.repo_root(), True),
        ("houdini_package_root", paths.houdini_package_root(), True),
        ("lcg_graph_path", paths.lcg_graph_path(), False),
        ("registry_path", paths.registry_path(), False),
        ("chart_modes_path", paths.chart_modes_path(), False),
        ("probe_runs_dir", paths.probe_runs_dir(), True),
        ("ledger_dir", paths.ledger_dir(), True),
        ("task_suggestions_path(parent)", paths.task_suggestions_path().parent, True),
        ("patches_dir", paths.patches_dir(), True),
        ("reports_dir", paths.reports_dir(), True),
    ]

    fail = False
    for label, path, expect_dir in checks:
        exists = path.exists()
        kind_ok = path.is_dir() if expect_dir else exists
        status = "OK" if (exists and kind_ok) else "FAIL"
        print(f"{status:<4} {label}: {path}")
        if status != "OK":
            fail = True

    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
