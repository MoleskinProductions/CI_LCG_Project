#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def _bootstrap_path() -> Path:
    repo = Path(__file__).resolve().parents[1]
    pkg_python = repo / "houdini_package" / "python"
    if str(pkg_python) not in sys.path:
        sys.path.insert(0, str(pkg_python))
    return repo


def _assert(cond: bool, msg: str) -> None:
    if not cond:
        raise AssertionError(msg)


def main() -> int:
    repo = _bootstrap_path()
    from ci import aggregate, graph, registry, suggest, trends

    fixture_dir = repo / "tests" / "fixtures" / "core_runs"
    run_a = str(fixture_dir / "PO-FIX-001.json")
    run_b = str(fixture_dir / "PO-FIX-002.json")
    run_c = str(fixture_dir / "PO-FIX-003.json")

    # Aggregate regression checks.
    stats = aggregate.aggregate_runs([run_a, run_b, run_c])
    n21 = stats["node_stats"]["Q000021"]
    _assert(n21["runs"] == 2, "Q000021 runs should be 2")
    _assert(n21["fails"] == 1, "Q000021 fails should be 1")
    _assert(n21["seam_hits"] == 1, "Q000021 seam_hits should be 1")
    _assert(n21["seam_kind_counts"].get("taxonomy_drift", 0) == 1, "taxonomy_drift count should be 1")
    _assert(stats["edge_stats"]["E000016"]["hits"] == 1, "E000016 hits should be 1")

    p006 = stats["probe_stats"]["P-PRB-006"]
    _assert(p006["runs"] == 2, "P-PRB-006 runs should be 2")
    _assert(p006["fails"] == 1, "P-PRB-006 fails should be 1")
    _assert(abs(p006["avg_seams"] - 0.5) < 1e-9, "P-PRB-006 avg_seams should be 0.5")

    # Trend regression checks.
    prev = trends.aggregate_window([run_a])
    recent = trends.aggregate_window([run_b, run_c])
    diff = trends.diff_stats(prev, recent)
    _assert(
        diff["node_deltas"]["Q000021"]["fail_rate_delta"] > 0.9,
        "Q000021 fail_rate delta should increase strongly from prev to recent",
    )
    _assert(
        diff["seam_kind_delta_total"].get("taxonomy_drift", 0) >= 1,
        "taxonomy_drift seam delta should be positive",
    )

    # Suggest regression checks.
    lcg = graph.load_lcg_graph()
    reg = registry.load_registry()
    chart_modes = registry.load_chart_modes()
    tasks = suggest.suggest_tasks(stats, lcg, reg, chart_modes)
    _assert(any(t["scope"] == "chart" for t in tasks), "Expected at least one chart coverage task")
    _assert(
        any("taxonomy-robustness" in t["title"] and t["target_id"] == "Q000021" for t in tasks),
        "Expected taxonomy robustness task for Q000021",
    )

    print("PASS: regression core checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
