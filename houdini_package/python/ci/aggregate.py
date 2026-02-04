from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, Iterable

from . import run_store


def aggregate_runs(run_paths: Iterable[str]) -> Dict[str, Any]:
    node_stats: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {"runs": 0, "fails": 0, "seam_hits": 0, "seam_kind_counts": defaultdict(int)}
    )
    edge_stats: Dict[str, Dict[str, Any]] = defaultdict(
        lambda: {"hits": 0, "seam_kind_counts": defaultdict(int)}
    )
    probe_stats: Dict[str, Dict[str, Any]] = defaultdict(lambda: {"runs": 0, "fails": 0, "seam_total": 0, "avg_seams": 0.0})
    errors = []
    timestamps = []
    observed_probe_ids = set()
    runs_considered = 0

    for path in run_paths:
        runs_considered += 1
        try:
            run = run_store.load_run(path)
        except Exception as exc:
            errors.append({"path": path, "error": str(exc)})
            continue

        node_id = run.get("node_id")
        probe_id = run.get("probe_id")
        if probe_id:
            observed_probe_ids.add(probe_id)
        split_result = str(run.get("split_result", "inconclusive")).lower()
        is_fail = split_result == "fail"
        ts = run.get("timestamp")
        if isinstance(ts, str) and ts:
            timestamps.append(ts)

        observable_values = run.get("observable_values", {})
        seam_flags = observable_values.get("seam_flags", []) if isinstance(observable_values, dict) else []
        seam_count = len(seam_flags)

        if node_id:
            ns = node_stats[node_id]
            ns["runs"] += 1
            ns["fails"] += 1 if is_fail else 0
            ns["seam_hits"] += seam_count
            for sf in seam_flags:
                ns["seam_kind_counts"][sf.get("kind", "unknown")] += 1

        if probe_id:
            ps = probe_stats[probe_id]
            ps["runs"] += 1
            ps["fails"] += 1 if is_fail else 0
            ps["seam_total"] += seam_count

        for sf in seam_flags:
            edge_id = sf.get("edge_id")
            if edge_id:
                es = edge_stats[edge_id]
                es["hits"] += 1
                es["seam_kind_counts"][sf.get("kind", "unknown")] += 1

    # finalize serialization-friendly dicts
    for ns in node_stats.values():
        ns["seam_kind_counts"] = dict(ns["seam_kind_counts"])
    for es in edge_stats.values():
        es["seam_kind_counts"] = dict(es["seam_kind_counts"])
    for ps in probe_stats.values():
        ps["avg_seams"] = ps["seam_total"] / ps["runs"] if ps["runs"] else 0.0
        del ps["seam_total"]

    window_start = min(timestamps) if timestamps else None
    window_end = max(timestamps) if timestamps else None
    return {
        "node_stats": dict(node_stats),
        "edge_stats": dict(edge_stats),
        "probe_stats": dict(probe_stats),
        "errors": errors,
        "meta": {
            "runs_considered": runs_considered,
            "window_start": window_start,
            "window_end": window_end,
            "probe_ids": sorted(observed_probe_ids),
        },
    }
