import json
import os
import re
from pathlib import Path
from typing import Any, Dict


CONSTELLATION_ORDER = ["C1", "C2", "C3", "C4", "C5"]
_CONSTELLATION_FULL = {
    "C1": "C1_CI_Method",
    "C2": "C2_Ontology_Ground_Inversion",
    "C3": "C3_Physics_Gauge_Detectability",
    "C4": "C4_Time_Identity",
    "C5": "C5_Mind_Intentionality",
}


def _package_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _repo_root() -> Path:
    return _package_root().parent


def _default_graph_path() -> Path:
    return _repo_root() / "lcg" / "lcg_graph.json"


def _default_constellations_path() -> Path:
    return _repo_root() / "reports" / "constellations.md"


def load_lcg_graph(graph_path: str | None = None) -> Dict[str, Any]:
    path = Path(graph_path or os.environ.get("CI_LCG_GRAPH", _default_graph_path()))
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _to_short_constellation(name: str) -> str:
    for short, full in _CONSTELLATION_FULL.items():
        if name == full:
            return short
    return "UNASSIGNED"


def _load_constellation_map() -> Dict[str, str]:
    path = _default_constellations_path()
    mapping: Dict[str, str] = {}
    if path.exists():
        text = path.read_text(encoding="utf-8")
        for line in text.splitlines():
            if not line.startswith("| Q"):
                continue
            cols = [c.strip() for c in line.split("|")]
            if len(cols) >= 5:
                qid = cols[1]
                primary = cols[3]
                if re.match(r"^Q\d{6}$", qid):
                    mapping[qid] = _to_short_constellation(primary)
    if mapping:
        return mapping

    # Fallback map for current graph if reports/constellations.md is unavailable.
    return {
        "Q000002": "C1", "Q000007": "C1", "Q000008": "C1", "Q000021": "C1",
        "Q000001": "C2", "Q000004": "C2", "Q000011": "C2", "Q000012": "C2", "Q000013": "C2",
        "Q000014": "C2", "Q000016": "C2", "Q000017": "C2", "Q000018": "C2",
        "Q000003": "C3", "Q000005": "C3", "Q000006": "C3", "Q000009": "C3", "Q000010": "C3",
        "Q000015": "C4", "Q000019": "C4",
        "Q000020": "C5",
    }


def index_nodes_edges(graph: Dict[str, Any]) -> Dict[str, Any]:
    constellation_map = _load_constellation_map()
    nodes: Dict[str, Dict[str, Any]] = {}
    for node in graph.get("nodes", []):
        nid = node["id"]
        nodes[nid] = {
            "id": nid,
            "title": node.get("title", nid),
            "constellation": constellation_map.get(nid, "UNASSIGNED"),
            "raw": node,
        }

    edges = []
    for edge in graph.get("edges", []):
        etype = edge.get("type", "")
        edge_kind = "E3" if etype.startswith("E3_") else "E4" if etype.startswith("E4_") else "E1" if etype.startswith("E1_") else "OTHER"
        edges.append({
            "id": edge["id"],
            "source": edge["source"],
            "target": edge["target"],
            "type": etype,
            "kind": edge_kind,
            "raw": edge,
        })

    by_node_edges: Dict[str, list[Dict[str, Any]]] = {nid: [] for nid in nodes}
    for edge in edges:
        if edge["source"] in by_node_edges:
            by_node_edges[edge["source"]].append(edge)
        if edge["target"] in by_node_edges:
            by_node_edges[edge["target"]].append(edge)

    return {
        "nodes": nodes,
        "edges": edges,
        "by_node_edges": by_node_edges,
        "constellation_order": list(CONSTELLATION_ORDER),
    }


def apply_run_overlay(probe_output_json: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(probe_output_json, dict):
        raise TypeError("probe_output_json must be a dict parsed from probe output JSON")

    active_node_id = probe_output_json.get("node_id")
    probe_id = probe_output_json.get("probe_id")
    chart_mode = probe_output_json.get("chart_mode")
    pass_fail = str(probe_output_json.get("split_result", "inconclusive")).lower()

    observable_values = probe_output_json.get("observable_values", {})
    seam_flags = observable_values.get("seam_flags", []) if isinstance(observable_values, dict) else []

    highlighted_edge_ids = set()
    seam_types = []
    for sf in seam_flags:
        edge_id = sf.get("edge_id")
        if edge_id:
            highlighted_edge_ids.add(edge_id)
        desc = sf.get("description", "")
        if "seam_type=" in desc:
            seam_types.append(desc.split("seam_type=", 1)[1].split()[0])
        else:
            seam_types.append(sf.get("kind", "unknown"))

    return {
        "active_node_id": active_node_id,
        "probe_id": probe_id,
        "chart_mode": chart_mode,
        "pass_fail": pass_fail,
        "seam_count": len(seam_flags),
        "seam_flags": seam_flags,
        "seam_types": seam_types,
        "highlighted_edge_ids": highlighted_edge_ids,
    }
