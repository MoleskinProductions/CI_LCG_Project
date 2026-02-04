from __future__ import annotations

from typing import Any, Dict, List

from .provenance import build_task_provenance

C1_NODES = {"Q000002", "Q000007", "Q000008", "Q000021"}
C2_NODES = {"Q000001", "Q000004", "Q000011", "Q000012", "Q000013", "Q000014", "Q000016", "Q000017", "Q000018"}
C3_NODES = {"Q000003", "Q000005", "Q000006", "Q000009", "Q000010"}
C4_NODES = {"Q000015", "Q000019"}
C5_NODES = {"Q000020"}


def _suggested_agent_for_node(node_id: str) -> str:
    if node_id in C1_NODES:
        return "C1_Method_Specialist"
    if node_id in C2_NODES:
        return "C2_Ontology_Ground_Inversion_Specialist"
    if node_id in C3_NODES:
        return "C3_Physics_Gauge_Specialist"
    if node_id in C4_NODES:
        return "C4_Time_Identity_Specialist"
    if node_id in C5_NODES:
        return "C5_Mind_Intentionality_Specialist"
    return "A0_Integrator"


def _priority_for_fail_rate(fail_rate: float) -> str:
    if fail_rate >= 0.66:
        return "P1"
    if fail_rate >= 0.33:
        return "P2"
    return "P3"


def _top_kind(kind_counts: Dict[str, int]) -> str | None:
    if not kind_counts:
        return None
    return max(kind_counts.items(), key=lambda kv: kv[1])[0]


def _mk_task(
    task_id: str,
    priority: str,
    scope: str,
    target_id: str,
    title: str,
    rationale: str,
    acceptance: str,
    agent: str,
    provenance: Dict[str, Any] | None = None,
) -> Dict[str, Any]:
    task = {
        "id": task_id,
        "priority": priority,
        "scope": scope,
        "target_id": target_id,
        "title": title,
        "rationale": rationale,
        "acceptance_criteria": acceptance,
        "suggested_agent": agent,
    }
    if provenance is not None:
        task["provenance"] = provenance
    return task


def suggest_tasks(
    aggregate_stats: Dict[str, Any],
    lcg_graph: Dict[str, Any],
    registry: Dict[str, Any],
    chart_modes: Dict[str, Any],
) -> List[Dict[str, Any]]:
    tasks: List[Dict[str, Any]] = []

    node_map = {n["id"]: n for n in lcg_graph.get("nodes", [])}
    edge_map = {e["id"]: e for e in lcg_graph.get("edges", [])}

    node_stats = aggregate_stats.get("node_stats", {})
    edge_stats = aggregate_stats.get("edge_stats", {})
    probe_stats = aggregate_stats.get("probe_stats", {})
    meta = aggregate_stats.get("meta", {})
    n_runs = int(meta.get("runs_considered", 0))
    time_range = (meta.get("window_start"), meta.get("window_end"))
    all_probe_ids = list(meta.get("probe_ids", []))

    tid = 1

    # 1) Hot nodes
    for node_id, stats in sorted(node_stats.items(), key=lambda kv: (kv[1].get("fails", 0), kv[1].get("seam_hits", 0)), reverse=True):
        runs = stats.get("runs", 0)
        if runs <= 0:
            continue
        fail_rate = stats.get("fails", 0) / runs
        seam_kind_counts = stats.get("seam_kind_counts", {})
        dominant = _top_kind(seam_kind_counts)
        discrim_count = len(node_map.get(node_id, {}).get("discriminators", []))

        # Gate: focus on genuinely hot nodes
        if fail_rate < 0.25 and stats.get("seam_hits", 0) < 2:
            continue

        if discrim_count < 2:
            axis = "seam visibility under re-description"
            title = f"Node {node_id}: Add orthogonal_probe discriminator for {axis}"
            rationale = (
                f"Node has {discrim_count} discriminator(s), fail_rate={fail_rate:.2f}, "
                f"seam_hits={stats.get('seam_hits',0)}. Additional probe coverage can reduce ambiguity."
            )
            acceptance = "Node has >=2 discriminators with non-overlapping split criteria and one recent rerun reduces fail_rate."
            tasks.append(
                _mk_task(
                    f"TASK-{tid:03d}",
                    _priority_for_fail_rate(fail_rate),
                    "node",
                    node_id,
                    title,
                    rationale,
                    acceptance,
                    _suggested_agent_for_node(node_id),
                    build_task_provenance(
                        stats,
                        node_id,
                        "node",
                        n_runs,
                        time_range,
                        seam_kind_counts,
                        all_probe_ids,
                    ),
                )
            )
            tid += 1

        if dominant == "taxonomy_drift":
            title = f"Node {node_id}: Strengthen taxonomy-robustness discriminator"
            rationale = f"Dominant seam kind is taxonomy_drift ({seam_kind_counts.get('taxonomy_drift',0)} hits)."
            acceptance = "D-LCG-002-style robustness split is explicit and seeded reruns show reduced taxonomy_drift seams."
            tasks.append(
                _mk_task(
                    f"TASK-{tid:03d}",
                    "P1",
                    "node",
                    node_id,
                    title,
                    rationale,
                    acceptance,
                    _suggested_agent_for_node(node_id),
                    build_task_provenance(
                        stats,
                        node_id,
                        "node",
                        n_runs,
                        time_range,
                        seam_kind_counts,
                        all_probe_ids,
                    ),
                )
            )
            tid += 1

        if dominant == "silent_upgrade":
            title = f"Node {node_id}: Strengthen admissibility handoff discriminator"
            rationale = f"Dominant seam kind is silent_upgrade ({seam_kind_counts.get('silent_upgrade',0)} hits)."
            acceptance = "D-BRID-021-style handoff checks block ontic upgrade without interface-variable accounting."
            tasks.append(
                _mk_task(
                    f"TASK-{tid:03d}",
                    "P1",
                    "node",
                    node_id,
                    title,
                    rationale,
                    acceptance,
                    "C1_Method_Specialist",
                    build_task_provenance(
                        stats,
                        node_id,
                        "node",
                        n_runs,
                        time_range,
                        seam_kind_counts,
                        all_probe_ids,
                    ),
                )
            )
            tid += 1

    # 2) Hot edges
    for edge_id, stats in sorted(edge_stats.items(), key=lambda kv: kv[1].get("hits", 0), reverse=True):
        hits = stats.get("hits", 0)
        if hits < 1:
            continue
        edge = edge_map.get(edge_id)
        if not edge:
            continue
        kind_counts = stats.get("seam_kind_counts", {})

        if edge.get("type", "").startswith("E3") and ("chart_dependence" in kind_counts or "axis_collapse" in kind_counts):
            title = f"Edge {edge_id}: Review E3 transfer for chart dependence"
            rationale = f"E3 edge has {hits} seam hits with chart dependence/axis collapse signals ({kind_counts})."
            acceptance = "Either add interface-variable bridge rationale or downgrade to E4 with explicit translation variable."
            tasks.append(
                _mk_task(
                    f"TASK-{tid:03d}",
                    "P1",
                    "edge",
                    edge_id,
                    title,
                    rationale,
                    acceptance,
                    "A0_Integrator",
                    build_task_provenance(
                        stats,
                        edge_id,
                        "edge",
                        n_runs,
                        time_range,
                        kind_counts,
                        all_probe_ids,
                    ),
                )
            )
            tid += 1

        if edge.get("type", "").startswith("E4") and ("silent_upgrade" in kind_counts or "nonportable_transfer" in kind_counts):
            title = f"Edge {edge_id}: Review E4 bridge for transfer readiness"
            rationale = f"E4 edge has admissibility/transfer seam hits ({kind_counts})."
            acceptance = "Confirm bridge remains E4 with guardrails or promote to E3 only with explicit shared discriminator axis."
            tasks.append(
                _mk_task(
                    f"TASK-{tid:03d}",
                    "P2",
                    "edge",
                    edge_id,
                    title,
                    rationale,
                    acceptance,
                    "A0_Integrator",
                    build_task_provenance(
                        stats,
                        edge_id,
                        "edge",
                        n_runs,
                        time_range,
                        kind_counts,
                        all_probe_ids,
                    ),
                )
            )
            tid += 1

    # 3) Coverage gaps by chart mode default probes
    for cm in chart_modes.get("chart_modes", []):
        mode_id = cm.get("id", "")
        defaults = cm.get("default_probes", [])
        if not defaults:
            continue
        run_counts = [probe_stats.get(pid, {}).get("runs", 0) for pid in defaults]
        low = [pid for pid, c in zip(defaults, run_counts) if c < 1]
        if low:
            title = f"Chart {mode_id}: Add smoke coverage for default probes"
            rationale = f"Default probes with low/no runs: {', '.join(low)}"
            acceptance = "Each listed default probe has at least one successful smoke run artifact in probe_runs/."
            tasks.append(
                _mk_task(
                    f"TASK-{tid:03d}",
                    "P2",
                    "chart",
                    mode_id,
                    title,
                    rationale,
                    acceptance,
                    "A0_Integrator",
                    build_task_provenance(
                        {"runs": sum(run_counts), "fails": 0, "avg_seams": 0.0},
                        mode_id,
                        "chart",
                        n_runs,
                        time_range,
                        {},
                        low,
                    ),
                )
            )
            tid += 1

    # Sort: priority then implicit order
    priority_rank = {"P1": 0, "P2": 1, "P3": 2}
    tasks.sort(key=lambda t: (priority_rank.get(t["priority"], 9), t["id"]))
    return tasks
