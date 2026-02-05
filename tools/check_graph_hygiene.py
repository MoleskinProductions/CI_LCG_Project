#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def _bootstrap_path() -> None:
    repo = Path(__file__).resolve().parents[1]
    pkg_python = repo / "houdini_package" / "python"
    if str(pkg_python) not in sys.path:
        sys.path.insert(0, str(pkg_python))


def main() -> int:
    _bootstrap_path()
    from ci import paths
    import json

    graph_path = paths.lcg_graph_path()
    if not graph_path.exists():
        print(f"FAIL: graph file missing: {graph_path}")
        return 1

    graph = json.loads(graph_path.read_text(encoding="utf-8"))
    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])

    errors = []

    # Node discriminator id uniqueness within node
    for n in nodes:
        dids = [d.get("id") for d in n.get("discriminators", [])]
        if len(dids) != len(set(dids)):
            errors.append(f"node {n.get('id')} has duplicate discriminator ids")

    # Edge required fields + endpoint existence
    node_ids = {n.get("id") for n in nodes}
    required_edge_fields = {"type", "weight", "justification", "tags", "evidence_refs", "source", "target"}
    for e in edges:
        eid = e.get("id")
        missing = [f for f in required_edge_fields if f not in e]
        if missing:
            errors.append(f"edge {eid} missing fields: {missing}")
        if e.get("source") not in node_ids:
            errors.append(f"edge {eid} source missing node: {e.get('source')}")
        if e.get("target") not in node_ids:
            errors.append(f"edge {eid} target missing node: {e.get('target')}")

        etype = str(e.get("type", ""))
        if etype.startswith("E4"):
            iv = e.get("interface_variable")
            if not iv and "Interface variable:" not in str(e.get("justification", "")):
                errors.append(f"edge {eid} E4 missing interface variable in field/justification")

    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        return 1

    print("PASS: graph hygiene checks")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
