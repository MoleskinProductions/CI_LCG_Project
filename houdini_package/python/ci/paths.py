from __future__ import annotations

import os
from pathlib import Path


def repo_root() -> Path:
    env_root = os.environ.get("CI_LCG_REPO_ROOT")
    if env_root:
        return Path(env_root).expanduser().resolve()
    return Path(__file__).resolve().parents[3]


def houdini_package_root() -> Path:
    default = repo_root() / "houdini_package"
    if default.exists():
        return default
    return Path(__file__).resolve().parents[2]


def companion_config_dir() -> Path:
    return repo_root() / "companion" / "config"


def companion_schema_dir() -> Path:
    return repo_root() / "companion" / "schemas"


def registry_path() -> Path:
    env = os.environ.get("CI_PROBE_REGISTRY")
    if env:
        return Path(env).expanduser().resolve()
    return companion_config_dir() / "probe_registry.json"


def chart_modes_path() -> Path:
    env = os.environ.get("CI_CHART_MODES")
    if env:
        return Path(env).expanduser().resolve()
    return companion_config_dir() / "chart_modes.json"


def schema_path(filename: str, env_key: str | None = None) -> Path:
    if env_key and os.environ.get(env_key):
        return Path(os.environ[env_key]).expanduser().resolve()
    return companion_schema_dir() / filename


def lcg_graph_path() -> Path:
    env = os.environ.get("CI_LCG_GRAPH_PATH") or os.environ.get("CI_LCG_GRAPH")
    if env:
        return Path(env).expanduser().resolve()
    return repo_root() / "lcg" / "lcg_graph.json"


def reports_dir() -> Path:
    return repo_root() / "reports"


def constellations_report_path() -> Path:
    return reports_dir() / "constellations.md"


def output_base_dir() -> Path:
    env = os.environ.get("CI_LCG_OUTPUT_DIR")
    if env:
        return Path(env).expanduser().resolve()
    return houdini_package_root() / "output"


def probe_runs_dir() -> Path:
    env = os.environ.get("CI_LCG_PROBE_RUNS_DIR") or os.environ.get("CI_OUTPUT_PROBE_DIR")
    if env:
        return Path(env).expanduser().resolve()
    return output_base_dir() / "probe_runs"


def ledger_dir() -> Path:
    env = os.environ.get("CI_LCG_LEDGER_DIR") or os.environ.get("CI_OUTPUT_LEDGER_DIR")
    if env:
        return Path(env).expanduser().resolve()
    return output_base_dir() / "ledger"


def task_suggestions_path() -> Path:
    return ledger_dir() / "task_suggestions.jsonl"


def patches_dir() -> Path:
    return repo_root() / "patches"


def ensure_runtime_dirs() -> None:
    probe_runs_dir().mkdir(parents=True, exist_ok=True)
    ledger_dir().mkdir(parents=True, exist_ok=True)
    patches_dir().mkdir(parents=True, exist_ok=True)
    reports_dir().mkdir(parents=True, exist_ok=True)
