from __future__ import annotations

from typing import Any, Dict, List, Tuple


def build_task_provenance(
    stats: Dict[str, Any],
    target_id: str,
    scope: str,
    n_runs: int,
    time_range: Tuple[str | None, str | None] | None,
    seam_kind_counts: Dict[str, int] | None,
    probe_ids: List[str] | None,
) -> Dict[str, Any]:
    prov: Dict[str, Any] = {
        "scope": scope,
        "target_id": target_id,
        "runs": n_runs,
        "seam_kinds": seam_kind_counts or {},
        "probes": probe_ids or [],
    }

    if time_range:
        start, end = time_range
        if start:
            prov["window_start"] = start
        if end:
            prov["window_end"] = end

    if scope == "node":
        runs = stats.get("runs", 0) or 0
        fails = stats.get("fails", 0) or 0
        prov["fail_rate"] = (fails / runs) if runs else 0.0
        prov["seam_hits"] = stats.get("seam_hits", 0)
    elif scope == "edge":
        prov["edge_hits"] = stats.get("hits", 0)
    elif scope == "probe":
        runs = stats.get("runs", 0) or 0
        fails = stats.get("fails", 0) or 0
        prov["fail_rate"] = (fails / runs) if runs else 0.0
        prov["avg_seams"] = stats.get("avg_seams", 0.0)

    return prov

