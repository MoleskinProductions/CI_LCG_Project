import json
from typing import Any, Dict

from . import paths


def load_probe_output_schema() -> Dict[str, Any]:
    with paths.schema_path("probe_output.schema.json", "CI_SCHEMA_PROBE_OUTPUT").open("r", encoding="utf-8") as f:
        return json.load(f)


def load_ledger_event_schema() -> Dict[str, Any]:
    with paths.schema_path("ledger_event.schema.json", "CI_SCHEMA_LEDGER_EVENT").open("r", encoding="utf-8") as f:
        return json.load(f)


def load_seam_flag_schema() -> Dict[str, Any]:
    with paths.schema_path("seam_flag.schema.json", "CI_SCHEMA_SEAM_FLAG").open("r", encoding="utf-8") as f:
        return json.load(f)
