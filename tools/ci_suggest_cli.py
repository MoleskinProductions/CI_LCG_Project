#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def _bootstrap_path() -> None:
    repo = Path(__file__).resolve().parents[1]
    pkg_python = repo / "houdini_package" / "python"
    if str(pkg_python) not in sys.path:
        sys.path.insert(0, str(pkg_python))


def _task_to_markdown(task: dict) -> str:
    lines = [
        f"- [ ] ({task['priority']}) {task['scope'].capitalize()} {task['target_id']}: {task['title']}",
        f"  - Rationale: {task['rationale']}",
        f"  - Acceptance: {task['acceptance_criteria']}",
        f"  - Suggested agent: {task['suggested_agent']}",
    ]
    return "\n".join(lines)


def main() -> int:
    _bootstrap_path()
    from ci import aggregate, graph, io_utils, paths, registry, run_store, suggest

    parser = argparse.ArgumentParser(description="Generate hotspot-driven CI task suggestions from recent probe runs.")
    parser.add_argument("--last-n", type=int, default=25, help="Number of most recent run files to aggregate.")
    parser.add_argument("--append", action="store_true", help="Append top suggestions to task_suggestions.jsonl.")
    parser.add_argument("--limit", type=int, default=10, help="Max tasks to print/save.")
    parser.add_argument("--json", action="store_true", help="Print suggestions as JSON instead of markdown.")
    args = parser.parse_args()

    if args.last_n < 1:
        print("ERROR: --last-n must be >= 1", file=sys.stderr)
        return 2
    if args.limit < 1:
        print("ERROR: --limit must be >= 1", file=sys.stderr)
        return 2

    paths.ensure_runtime_dirs()
    run_paths = run_store.list_recent_runs(limit=args.last_n)
    if not run_paths:
        print("ERROR: no probe runs found in output directory.", file=sys.stderr)
        return 3

    stats = aggregate.aggregate_runs(run_paths)
    if stats.get("errors"):
        print(f"WARN: skipped malformed run files: {len(stats['errors'])}", file=sys.stderr)

    try:
        lcg_graph = graph.load_lcg_graph()
        reg = registry.load_registry()
        chart_modes = registry.load_chart_modes()
    except FileNotFoundError as exc:
        print(f"ERROR: missing required file: {exc}", file=sys.stderr)
        return 4
    except Exception as exc:
        print(f"ERROR: failed to load graph/registry/chart modes: {exc}", file=sys.stderr)
        return 4

    tasks = suggest.suggest_tasks(stats, lcg_graph, reg, chart_modes)
    out_tasks = tasks[: args.limit]
    if not out_tasks:
        print("No task suggestions generated for the selected run window.")
        return 0

    if args.json:
        print(json.dumps(out_tasks, indent=2))
    else:
        for task in out_tasks:
            print(_task_to_markdown(task))
            print("")

    if args.append:
        target = paths.task_suggestions_path()
        target.parent.mkdir(parents=True, exist_ok=True)
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        for task in out_tasks:
            io_utils.append_jsonl_record(target, {"timestamp": now, **task})
        print(f"Appended {len(out_tasks)} suggestions to {target}")

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
