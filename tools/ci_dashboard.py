#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys
from pathlib import Path


def _bootstrap_path() -> None:
    repo = Path(__file__).resolve().parents[1]
    pkg_python = repo / "houdini_package" / "python"
    if str(pkg_python) not in sys.path:
        sys.path.insert(0, str(pkg_python))


def _fail_rate(d: dict) -> float:
    runs = d.get("runs", 0) or 0
    fails = d.get("fails", 0) or 0
    return (fails / runs) if runs else 0.0


def main() -> int:
    _bootstrap_path()
    from ci import aggregate, run_store

    parser = argparse.ArgumentParser(description="Quick terminal dashboard for recent CI probe activity.")
    parser.add_argument("--last-n", type=int, default=25, help="Number of recent probe runs to include.")
    parser.add_argument("--top", type=int, default=5, help="Top N hotspot rows for nodes/edges/probes.")
    args = parser.parse_args()

    if args.last_n < 1 or args.top < 1:
        print("ERROR: --last-n and --top must be >= 1", file=sys.stderr)
        return 2

    run_paths = run_store.list_recent_runs(limit=args.last_n)
    if not run_paths:
        print("No probe runs found.")
        return 0

    stats = aggregate.aggregate_runs(run_paths)
    meta = stats.get("meta", {})
    node_stats = stats.get("node_stats", {})
    edge_stats = stats.get("edge_stats", {})
    probe_stats = stats.get("probe_stats", {})
    errors = stats.get("errors", [])

    print("== CI Dashboard ==")
    print(f"runs_considered={meta.get('runs_considered', 0)}")
    print(f"window={meta.get('window_start')} -> {meta.get('window_end')}")
    print(f"malformed_runs_skipped={len(errors)}")
    print("")

    print(f"-- Top {args.top} Hot Nodes (fail_rate, seam_hits) --")
    hot_nodes = sorted(
        node_stats.items(),
        key=lambda kv: (_fail_rate(kv[1]), kv[1].get("seam_hits", 0), kv[1].get("runs", 0)),
        reverse=True,
    )[: args.top]
    if not hot_nodes:
        print("(none)")
    for nid, d in hot_nodes:
        print(
            f"{nid}: runs={d.get('runs',0)} fails={d.get('fails',0)} "
            f"fail_rate={_fail_rate(d):.2f} seams={d.get('seam_hits',0)} kinds={d.get('seam_kind_counts',{})}"
        )
    print("")

    print(f"-- Top {args.top} Hot Edges (seam hits) --")
    hot_edges = sorted(edge_stats.items(), key=lambda kv: kv[1].get("hits", 0), reverse=True)[: args.top]
    if not hot_edges:
        print("(none)")
    for eid, d in hot_edges:
        print(f"{eid}: hits={d.get('hits',0)} kinds={d.get('seam_kind_counts',{})}")
    print("")

    print(f"-- Top {args.top} Probe Failure Rates --")
    hot_probes = sorted(
        probe_stats.items(),
        key=lambda kv: (
            (kv[1].get("fails", 0) / kv[1].get("runs", 1)) if kv[1].get("runs", 0) else 0.0,
            kv[1].get("avg_seams", 0.0),
            kv[1].get("runs", 0),
        ),
        reverse=True,
    )[: args.top]
    if not hot_probes:
        print("(none)")
    for pid, d in hot_probes:
        runs = d.get("runs", 0)
        fails = d.get("fails", 0)
        rate = (fails / runs) if runs else 0.0
        print(f"{pid}: runs={runs} fails={fails} fail_rate={rate:.2f} avg_seams={d.get('avg_seams',0.0):.2f}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
