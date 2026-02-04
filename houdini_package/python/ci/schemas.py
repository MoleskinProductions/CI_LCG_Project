import json
import os
from pathlib import Path
from typing import Any, Dict


def _package_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _repo_root() -> Path:
    return _package_root().parent


def _schema_path(env_key: str, filename: str) -> Path:
    env_val = os.environ.get(env_key)
    if env_val:
        return Path(env_val)
    return _repo_root() / "companion" / "schemas" / filename


def load_probe_output_schema() -> Dict[str, Any]:
    with _schema_path("CI_SCHEMA_PROBE_OUTPUT", "probe_output.schema.json").open("r", encoding="utf-8") as f:
        return json.load(f)


def load_ledger_event_schema() -> Dict[str, Any]:
    with _schema_path("CI_SCHEMA_LEDGER_EVENT", "ledger_event.schema.json").open("r", encoding="utf-8") as f:
        return json.load(f)


def load_seam_flag_schema() -> Dict[str, Any]:
    with _schema_path("CI_SCHEMA_SEAM_FLAG", "seam_flag.schema.json").open("r", encoding="utf-8") as f:
        return json.load(f)
