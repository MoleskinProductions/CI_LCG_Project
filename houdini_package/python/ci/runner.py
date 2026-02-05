import json
import random
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict

from . import ledger, paths, registry, schemas
from .validate import validate_json


DEFAULT_PROBE_ID = "P-PRB-006"
# Example reproducible fail seed:
#   P-PRB-010 with seed=21 yields seam_count > 0.


def _now_iso() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def _id_suffix() -> str:
    return datetime.now(timezone.utc).strftime("%H%M%S")


def _pick_chart_mode(probe_id: str, chart_mode_id: str | None, chart_modes: Dict[str, Any]) -> Dict[str, Any]:
    if chart_mode_id:
        return registry.get_chart_mode(chart_mode_id, chart_modes)
    for mode in chart_modes["chart_modes"]:
        if probe_id in mode.get("default_probes", []):
            return mode
    return chart_modes["chart_modes"][0]


def _stub_node_for_probe(probe_id: str) -> str:
    defaults = {
        "P-PRB-006": "Q000011",
        "P-PRB-005": "Q000021",
        "P-PRB-012": "Q000019",
    }
    return defaults.get(probe_id, "Q000002")


def _make_seam_flag(
    run_id: str,
    probe_id: str,
    record_id: str,
    idx: int,
    *,
    kind: str,
    scope: str,
    severity: str,
    description: str,
    edge_id: str | None = None,
) -> Dict[str, Any]:
    flag: Dict[str, Any] = {
        "schema_version": "0.1.0",
        "flag_id": f"SF-{record_id.split('-')[-1]}",
        "run_id": run_id,
        "timestamp": _now_iso(),
        "severity": severity,
        "scope": scope,
        "kind": kind,
        "trigger_probe_ids": [probe_id],
        "evidence_refs": [record_id],
        "description": description,
    }
    if edge_id:
        flag["edge_id"] = edge_id
    return flag


def _execute_probe(
    probe_id: str,
    run_id: str,
    record_id: str,
    inputs: Dict[str, Any],
    seed: int | None,
) -> Dict[str, Any]:
    rng = random.Random(seed if seed is not None else datetime.now(timezone.utc).timestamp())

    if probe_id == "P-PRB-004":
        labels = [
            "scope_boundary",
            "constraint_gap",
            "chart_mismatch",
            "taxonomy_conflict",
            "role_swap",
            "silent_upgrade",
            "regress_loop",
            "admissibility_gap",
        ]
        base_labels = labels[:]
        rng.shuffle(labels)
        merge_count = rng.randint(0, 2)
        merged = labels[:-merge_count] if merge_count else labels
        overlap = len(set(base_labels) & set(merged)) / max(1, len(base_labels))
        drift_score = max(0.0, min(1.0, (1.0 - overlap) + 0.2 * merge_count))
        pass_fail = "fail" if drift_score > 0.35 else "pass"
        seam_flags = []
        if pass_fail == "fail":
            severity = "high" if drift_score > 0.7 else "medium"
            seam_flags.append(
                _make_seam_flag(
                    run_id,
                    probe_id,
                    record_id,
                    1,
                    kind="taxonomy_drift",
                    scope="node",
                    severity=severity,
                    description=f"seam_type=taxonomy_drift drift_score={drift_score:.3f}",
                )
            )
        outputs = {
            "drift_score": round(drift_score, 4),
            "base_count": len(base_labels),
            "post_perturb_count": len(merged),
            "merge_count": merge_count,
            "pass_fail": pass_fail,
        }
        return {"pass_fail": pass_fail, "seam_flags": seam_flags, "outputs": outputs}

    if probe_id == "P-PRB-008":
        signal = [rng.uniform(-1.0, 1.0) for _ in range(12)]
        first_half = signal[:6]
        second_half = signal[6:]
        asym_a = (sum(second_half) / len(second_half)) - (sum(first_half) / len(first_half))
        reversed_signal = list(reversed(signal))
        coarse = [(reversed_signal[i] + reversed_signal[i + 1]) / 2.0 for i in range(0, 12, 2)]
        coarse_first = coarse[:3]
        coarse_second = coarse[3:]
        asym_b = (sum(coarse_second) / len(coarse_second)) - (sum(coarse_first) / len(coarse_first))
        sign_flip = (asym_a > 0 and asym_b < 0) or (asym_a < 0 and asym_b > 0)
        collapse = abs(asym_b) < 0.05
        pass_fail = "fail" if (sign_flip or collapse) else "pass"
        seam_flags = []
        if pass_fail == "fail":
            seam_type = "arrow_instability" if sign_flip else "chart_dependence"
            seam_flags.append(
                _make_seam_flag(
                    run_id,
                    probe_id,
                    record_id,
                    1,
                    kind="axis_collapse",
                    scope="node",
                    severity="medium",
                    description=f"seam_type={seam_type} asym_a={asym_a:.4f} asym_b={asym_b:.4f}",
                )
            )
        outputs = {
            "asymmetry_chart_a": round(asym_a, 6),
            "asymmetry_chart_b": round(asym_b, 6),
            "sign_flip": sign_flip,
            "collapse": collapse,
            "pass_fail": pass_fail,
        }
        return {"pass_fail": pass_fail, "seam_flags": seam_flags, "outputs": outputs}

    if probe_id == "P-PRB-010":
        edge_id = str(inputs.get("edge_id") or "E000024")
        procedure_valid = {
            "claim": "translation admissible",
            "interface_variables": ["primitive budget / silent premise", "ledger stability / taxonomy drift"],
            "primitive_budget": 3,
        }
        translated_visible = {
            "ontology_admissible": True,
            "interface_variables": list(procedure_valid["interface_variables"]),
            "primitive_budget": procedure_valid["primitive_budget"],
        }
        hide_interface = bool(inputs.get("force_reify", rng.random() < 0.65))
        translated_reified = {
            "ontology_admissible": True,
            "interface_variables": [] if hide_interface else list(procedure_valid["interface_variables"]),
            "primitive_budget": None if hide_interface else procedure_valid["primitive_budget"],
        }
        reification_detected = (not translated_reified["interface_variables"]) or (
            translated_reified["primitive_budget"] is None
        )
        pass_fail = "fail" if reification_detected else "pass"
        seam_flags = []
        if pass_fail == "fail":
            seam_flags.append(
                _make_seam_flag(
                    run_id,
                    probe_id,
                    record_id,
                    1,
                    kind="silent_upgrade",
                    scope="edge",
                    severity="high",
                    edge_id=edge_id,
                    description="seam_type=silent_upgrade interface variable dropped during handoff translation",
                )
            )
        outputs = {
            "visible_translation_has_interfaces": bool(translated_visible["interface_variables"]),
            "reified_translation_has_interfaces": bool(translated_reified["interface_variables"]),
            "reification_detected": reification_detected,
            "pass_fail": pass_fail,
        }
        return {"pass_fail": pass_fail, "seam_flags": seam_flags, "outputs": outputs}

    # Default A9.3 stub behavior (kept for P-PRB-006 and any other probes).
    return {
        "pass_fail": "pass",
        "seam_flags": [],
        "outputs": {"score": 0.9, "pass_fail": "pass"},
    }


def run_probe(
    probe_id: str = DEFAULT_PROBE_ID,
    chart_mode_id: str | None = None,
    inputs: Dict[str, Any] | None = None,
    stub_mode: bool = True,
    output_dir: str | None = None,
    seed: int | None = None,
) -> Dict[str, Any]:
    if not stub_mode:
        raise NotImplementedError("Only stub_mode is implemented in A9.3 vertical slice.")

    reg = registry.load_registry()
    chart_modes = registry.load_chart_modes()
    probe = registry.get_probe(probe_id, reg)
    chart_mode = _pick_chart_mode(probe_id, chart_mode_id, chart_modes)

    suffix = _id_suffix()
    run_id = f"RUN-{suffix}"
    record_id = f"PO-{suffix}"
    node_id = _stub_node_for_probe(probe_id)

    run_inputs = inputs or {}
    execution = _execute_probe(probe_id, run_id, record_id, run_inputs, seed)
    pass_fail = execution["pass_fail"]
    seam_flags = execution["seam_flags"]
    outputs = execution["outputs"]

    # Validate seam flags against schema.
    seam_schema = schemas.load_seam_flag_schema()
    for i, sf in enumerate(seam_flags):
        validate_json(sf, seam_schema, label=f"seam_flag[{i}]")

    inputs_summary = {
        "probe_id": probe_id,
        "chart_mode_id": chart_mode["id"],
        "stub_mode": True,
        "input_fields": probe.get("input_fields", []),
        "seed": seed,
        "inputs": run_inputs,
    }
    outputs["seam_count"] = len(seam_flags)

    probe_output: Dict[str, Any] = {
        "schema_version": "0.1.0",
        "record_id": record_id,
        "run_id": run_id,
        "timestamp": _now_iso(),
        "node_id": node_id,
        "probe_id": probe_id,
        "discriminator_ids": probe["discriminator_ids"],
        "interface_variables": probe["interface_variables"],
        "chart_mode": chart_mode["id"],
        "observable_values": {
            "chart_mode_id": chart_mode["id"],
            "inputs_summary": inputs_summary,
            "outputs": outputs,
            "seam_flags": seam_flags,
            "pass_fail": pass_fail,
        },
        "split_result": pass_fail,
        "confidence": 0.9,
        "failure_signatures": [sf["kind"] for sf in seam_flags],
        "notes": "A9.3 stub execution",
    }

    validate_json(probe_output, schemas.load_probe_output_schema(), label="probe_output")

    out_dir = Path(output_dir) if output_dir else paths.probe_runs_dir()
    out_dir.mkdir(parents=True, exist_ok=True)
    probe_output_path = out_dir / f"{record_id}.json"
    probe_output_path.write_text(json.dumps(probe_output, indent=2) + "\n", encoding="utf-8")

    ledger_event = ledger.build_ledger_event(
        run_id=run_id,
        node_id=node_id,
        probe_record_id=record_id,
        seam_flag_ids=[sf["flag_id"] for sf in seam_flags],
        interface_variables=probe["interface_variables"],
        invariant_ids=["I-000-000"],
        notes=f"probe_output_path={probe_output_path}",
    )
    ledger_paths = ledger.write_ledger_event(ledger_event)

    return {
        "probe_output": probe_output,
        "probe_output_path": str(probe_output_path),
        "ledger_event": ledger_event,
        "ledger_paths": ledger_paths,
        "pass_fail": pass_fail.upper(),
        "seam_count": len(seam_flags),
    }
