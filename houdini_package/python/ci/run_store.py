import json
from pathlib import Path
from typing import Any, Dict, List

from . import paths

def list_recent_runs(run_dir: str | None = None, limit: int = 50) -> List[str]:
    path = Path(run_dir) if run_dir else paths.probe_runs_dir()
    if not path.exists():
        return []
    files = [p for p in path.glob("PO-*.json") if p.is_file()]
    files.sort(key=lambda p: p.stat().st_mtime, reverse=True)
    return [str(p) for p in files[:limit]]


def load_run(path: str) -> Dict[str, Any]:
    p = Path(path)
    with p.open("r", encoding="utf-8") as f:
        return json.load(f)


def summarize_run(path: str) -> Dict[str, Any]:
    run = load_run(path)
    observable_values = run.get("observable_values", {})
    seam_flags = observable_values.get("seam_flags", []) if isinstance(observable_values, dict) else []
    edge_ids = sorted({sf.get("edge_id") for sf in seam_flags if sf.get("edge_id")})
    return {
        "path": path,
        "record_id": run.get("record_id"),
        "run_id": run.get("run_id"),
        "probe_id": run.get("probe_id"),
        "chart_mode": run.get("chart_mode"),
        "node_id": run.get("node_id"),
        "pass_fail": str(run.get("split_result", "inconclusive")).upper(),
        "seam_count": len(seam_flags),
        "edge_ids": edge_ids,
        "seam_flags": seam_flags,
    }
