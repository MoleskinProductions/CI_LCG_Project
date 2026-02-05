#!/usr/bin/env python3
from __future__ import annotations

import importlib
import sys
from pathlib import Path


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    pkg_python = repo / "houdini_package" / "python"
    if str(pkg_python) not in sys.path:
        sys.path.insert(0, str(pkg_python))

    modules = [
        "ci.paths",
        "ci.registry",
        "ci.schemas",
        "ci.validate",
        "ci.runner",
        "ci.ledger",
        "ci.run_store",
        "ci.aggregate",
        "ci.trends",
        "ci.graph",
        "ci.suggest",
        "ci.provenance",
        "ci_panels.CI_GraphOverlay_panel",
    ]

    failed = []
    for name in modules:
        try:
            importlib.import_module(name)
            print(f"OK   {name}")
        except Exception as exc:
            failed.append((name, exc))
            print(f"FAIL {name}: {exc}")

    if failed:
        return 1
    print("ALL IMPORTS OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
