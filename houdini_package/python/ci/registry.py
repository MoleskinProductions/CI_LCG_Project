import json
import os
from pathlib import Path
from typing import Any, Dict, List


def _package_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _repo_root() -> Path:
    return _package_root().parent


def _default_registry_path() -> Path:
    return _repo_root() / "companion" / "config" / "probe_registry.json"


def _default_chart_modes_path() -> Path:
    return _repo_root() / "companion" / "config" / "chart_modes.json"


def load_registry(registry_path: str | None = None) -> Dict[str, Any]:
    path = Path(registry_path or os.environ.get("CI_PROBE_REGISTRY", _default_registry_path()))
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if "probes" not in data or not isinstance(data["probes"], list):
        raise ValueError(f"Invalid registry format in {path}: missing probes list")
    return data


def load_chart_modes(chart_modes_path: str | None = None) -> Dict[str, Any]:
    path = Path(chart_modes_path or os.environ.get("CI_CHART_MODES", _default_chart_modes_path()))
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
    if "chart_modes" not in data or not isinstance(data["chart_modes"], list):
        raise ValueError(f"Invalid chart modes format in {path}: missing chart_modes list")
    return data


def list_probes(registry: Dict[str, Any] | None = None) -> List[Dict[str, Any]]:
    reg = registry or load_registry()
    return reg["probes"]


def get_probe(probe_id: str, registry: Dict[str, Any] | None = None) -> Dict[str, Any]:
    reg = registry or load_registry()
    for probe in reg["probes"]:
        if probe.get("id") == probe_id:
            return probe
    raise KeyError(f"Probe not found: {probe_id}")


def get_chart_mode(chart_mode_id: str, chart_modes: Dict[str, Any] | None = None) -> Dict[str, Any]:
    cm = chart_modes or load_chart_modes()
    for mode in cm["chart_modes"]:
        if mode.get("id") == chart_mode_id:
            return mode
    raise KeyError(f"Chart mode not found: {chart_mode_id}")
