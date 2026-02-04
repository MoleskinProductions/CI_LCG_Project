import json
import os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from . import schemas
from .validate import validate_json


def _package_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _default_ledger_dir() -> Path:
    return _package_root() / "output" / "ledger"


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def build_ledger_event(
    run_id: str,
    node_id: str,
    probe_record_id: str,
    seam_flag_ids: list[str],
    interface_variables: list[str],
    edge_id: str | None = None,
    invariant_ids: list[str] | None = None,
    notes: str | None = None,
) -> Dict[str, Any]:
    event_num = probe_record_id.split("-")[-1]
    event: Dict[str, Any] = {
        "schema_version": "0.1.0",
        "event_id": f"LE-{event_num}",
        "run_id": run_id,
        "timestamp": _now_iso(),
        "node_id": node_id,
        "invariant_ids": invariant_ids or ["I-000-000"],
        "probe_refs": [probe_record_id],
        "channel_drift": {iv: 0.0 for iv in interface_variables},
        "seam_flags": seam_flag_ids,
        "decision": "retain" if not seam_flag_ids else "review",
    }
    if edge_id:
        event["edge_id"] = edge_id
    if notes:
        event["notes"] = notes
    return event


def write_ledger_event(event: Dict[str, Any], ledger_dir: str | None = None) -> Dict[str, str]:
    out_dir = Path(ledger_dir or os.environ.get("CI_OUTPUT_LEDGER_DIR", _default_ledger_dir()))
    out_dir.mkdir(parents=True, exist_ok=True)

    validate_json(event, schemas.load_ledger_event_schema(), label="ledger_event")

    event_id = event["event_id"]
    json_path = out_dir / f"{event_id}.json"
    jsonl_path = out_dir / "ledger.jsonl"

    json_path.write_text(json.dumps(event, indent=2) + "\n", encoding="utf-8")
    with jsonl_path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(event) + "\n")

    return {
        "ledger_event_json": str(json_path),
        "ledger_jsonl": str(jsonl_path),
    }
