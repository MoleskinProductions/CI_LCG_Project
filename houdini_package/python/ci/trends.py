from __future__ import annotations

from collections import defaultdict
from typing import Any, Dict, Iterable

from . import aggregate


def aggregate_window(run_paths: Iterable[str]) -> Dict[str, Any]:
    stats = aggregate.aggregate_runs(run_paths)
    meta = stats.get("meta", {})
    return {
        "node_stats": stats.get("node_stats", {}),
        "edge_stats": stats.get("edge_stats", {}),
        "probe_stats": stats.get("probe_stats", {}),
        "errors": stats.get("errors", []),
        "window_start": meta.get("window_start"),
        "window_end": meta.get("window_end"),
        "runs_considered": int(meta.get("runs_considered", 0)),
    }


def _node_fail_rate(node_stats: Dict[str, Any], node_id: str) -> float:
    d = node_stats.get(node_id, {})
    runs = d.get("runs", 0) or 0
    fails = d.get("fails", 0) or 0
    return (fails / runs) if runs else 0.0


def diff_stats(stats_a: Dict[str, Any], stats_b: Dict[str, Any]) -> Dict[str, Any]:
    # Delta convention: b - a (positive = worsening for fail/hits)
    nodes_a = stats_a.get("node_stats", {})
    nodes_b = stats_b.get("node_stats", {})
    edges_a = stats_a.get("edge_stats", {})
    edges_b = stats_b.get("edge_stats", {})

    node_ids = set(nodes_a) | set(nodes_b)
    edge_ids = set(edges_a) | set(edges_b)

    node_deltas: Dict[str, Dict[str, Any]] = {}
    for nid in node_ids:
        runs_a = (nodes_a.get(nid, {}) or {}).get("runs", 0)
        runs_b = (nodes_b.get(nid, {}) or {}).get("runs", 0)
        fr_a = _node_fail_rate(nodes_a, nid)
        fr_b = _node_fail_rate(nodes_b, nid)
        sh_a = (nodes_a.get(nid, {}) or {}).get("seam_hits", 0)
        sh_b = (nodes_b.get(nid, {}) or {}).get("seam_hits", 0)
        seam_kind_delta: Dict[str, int] = {}
        kinds = set((nodes_a.get(nid, {}) or {}).get("seam_kind_counts", {})) | set(
            (nodes_b.get(nid, {}) or {}).get("seam_kind_counts", {})
        )
        for k in kinds:
            seam_kind_delta[k] = (nodes_b.get(nid, {}).get("seam_kind_counts", {}).get(k, 0) -
                                  nodes_a.get(nid, {}).get("seam_kind_counts", {}).get(k, 0))

        node_deltas[nid] = {
            "fail_rate_delta": fr_b - fr_a,
            "seam_hits_delta": sh_b - sh_a,
            "runs_a": runs_a,
            "runs_b": runs_b,
            "seam_kind_delta": seam_kind_delta,
        }

    edge_deltas: Dict[str, Dict[str, Any]] = {}
    for eid in edge_ids:
        hits_a = (edges_a.get(eid, {}) or {}).get("hits", 0)
        hits_b = (edges_b.get(eid, {}) or {}).get("hits", 0)
        seam_kind_delta: Dict[str, int] = {}
        kinds = set((edges_a.get(eid, {}) or {}).get("seam_kind_counts", {})) | set(
            (edges_b.get(eid, {}) or {}).get("seam_kind_counts", {})
        )
        for k in kinds:
            seam_kind_delta[k] = (edges_b.get(eid, {}).get("seam_kind_counts", {}).get(k, 0) -
                                  edges_a.get(eid, {}).get("seam_kind_counts", {}).get(k, 0))
        edge_deltas[eid] = {
            "hit_delta": hits_b - hits_a,
            "hits_a": hits_a,
            "hits_b": hits_b,
            "seam_kind_delta": seam_kind_delta,
        }

    seam_kind_delta_total: Dict[str, int] = defaultdict(int)
    for d in node_deltas.values():
        for k, v in d.get("seam_kind_delta", {}).items():
            seam_kind_delta_total[k] += v

    return {
        "node_deltas": node_deltas,
        "edge_deltas": edge_deltas,
        "seam_kind_delta_total": dict(seam_kind_delta_total),
        "window_a": {
            "runs_considered": int(stats_a.get("runs_considered", 0)),
            "window_start": stats_a.get("window_start"),
            "window_end": stats_a.get("window_end"),
        },
        "window_b": {
            "runs_considered": int(stats_b.get("runs_considered", 0)),
            "window_start": stats_b.get("window_start"),
            "window_end": stats_b.get("window_end"),
        },
    }
