#!/usr/bin/env python3
"""A10 Task-to-Patch Assistant.

Generates machine + human patch artifacts from persisted task suggestions.
By default writes a patched graph copy to lcg/lcg_graph.patched.json.
Use --apply to overwrite lcg/lcg_graph.json.
"""

from __future__ import annotations

import argparse
import copy
import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Tuple

REQUIRED_TASK_KEYS = {
    "id",
    "priority",
    "scope",
    "target_id",
    "title",
    "rationale",
    "acceptance_criteria",
    "suggested_agent",
}

VALID_SCOPES = {"node", "edge", "probe", "chart"}
VALID_PRIORITIES = {"P1", "P2", "P3"}


def _bootstrap_ci_python() -> None:
    repo = Path(__file__).resolve().parents[1]
    ci_python = repo / "houdini_package" / "python"
    if str(ci_python) not in sys.path:
        sys.path.insert(0, str(ci_python))


def now_utc() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def write_json(path: Path, obj: Dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2) + "\n", encoding="utf-8")


def _validate_task_suggestion(obj: Dict[str, Any], line_no: int) -> str | None:
    missing = sorted(REQUIRED_TASK_KEYS - set(obj.keys()))
    if missing:
        return f"line {line_no}: missing keys {missing}"
    if obj.get("scope") not in VALID_SCOPES:
        return f"line {line_no}: invalid scope '{obj.get('scope')}'"
    if obj.get("priority") not in VALID_PRIORITIES:
        return f"line {line_no}: invalid priority '{obj.get('priority')}'"
    return None


def load_task_suggestions(path: Path) -> Tuple[List[Dict[str, Any]], List[str]]:
    tasks: List[Dict[str, Any]] = []
    warnings: List[str] = []
    if not path.exists():
        return tasks, warnings
    with path.open("r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue
            try:
                obj = json.loads(line)
            except Exception:
                warnings.append(f"line {i}: invalid JSON")
                continue
            if isinstance(obj, dict):
                issue = _validate_task_suggestion(obj, i)
                if issue:
                    warnings.append(issue)
                    continue
                tasks.append(obj)
            else:
                warnings.append(f"line {i}: expected object, got {type(obj).__name__}")
    return tasks, warnings


def parse_interface_variables(path: Path) -> List[str]:
    if not path.exists():
        return []
    vars_out: List[str] = []
    text = path.read_text(encoding="utf-8")
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("- `") and "`:" in line:
            var = line.split("`", 2)[1]
            vars_out.append(var)
    return vars_out


def find_node(graph: Dict[str, Any], node_id: str) -> Dict[str, Any] | None:
    for n in graph.get("nodes", []):
        if n.get("id") == node_id:
            return n
    return None


def find_edge(graph: Dict[str, Any], edge_id: str) -> Dict[str, Any] | None:
    for e in graph.get("edges", []):
        if e.get("id") == edge_id:
            return e
    return None


def next_discriminator_id(graph: Dict[str, Any]) -> str:
    max_n = 0
    pat = re.compile(r"^D-A10-(\d{3})$")
    for n in graph.get("nodes", []):
        for d in n.get("discriminators", []):
            did = d.get("id", "")
            m = pat.match(did)
            if m:
                max_n = max(max_n, int(m.group(1)))
    return f"D-A10-{max_n+1:03d}"


def choose_interface_variable(task: Dict[str, Any], known: List[str]) -> str:
    text = " ".join(
        [
            str(task.get("title", "")),
            str(task.get("rationale", "")),
            str(task.get("acceptance_criteria", "")),
        ]
    ).lower()
    candidates = [
        "primitive budget / silent premise",
        "ledger stability / taxonomy drift",
        "local arrow persistence",
        "observability equivalence class",
        "dimensionless drift",
        "orientation residue",
        "constraint-order coupling",
        "loop/closure residue",
    ]
    for c in candidates:
        if c in known and c.lower().split("/")[0].strip() in text:
            return c
    for c in candidates:
        if c in known:
            return c
    return known[0] if known else "primitive budget / silent premise"


def infer_discriminator_pattern(task: Dict[str, Any]) -> str:
    t = str(task.get("title", "")).lower()
    r = str(task.get("rationale", "")).lower()
    text = t + " " + r
    if "handoff" in text or "silent_upgrade" in text:
        return "interface_scatter"
    if "taxonomy" in text or "robustness" in text:
        return "ensemble_split"
    if "scatter" in text:
        return "interface_scatter"
    return "orthogonal_probe"


def build_patch(task: Dict[str, Any], graph: Dict[str, Any], interface_vars: List[str]) -> Tuple[Dict[str, Any], Dict[str, Any]]:
    scope = task.get("scope")
    target_id = task.get("target_id")
    title = str(task.get("title", ""))
    rationale = str(task.get("rationale", ""))

    patch_ops: List[Dict[str, Any]] = []

    if scope == "node":
        node = find_node(graph, target_id)
        if not node:
            raise ValueError(f"Target node not found: {target_id}")
        t = title.lower()

        if "discriminator" in t:
            pattern = infer_discriminator_pattern(task)
            did = next_discriminator_id(graph)
            stub = {
                "id": did,
                "name": f"A10 stub for {target_id}",
                "pattern": pattern,
                "how_to": "Observable: TODO define measurable axis from task hotspot. Split criterion: TODO define pass/fail boundary with explicit seam condition.",
                "transferable": False,
            }
            patch_ops.append({"op": "add", "path": f"/nodes/{target_id}/discriminators/-", "value": stub})

        if "interface" in t or "handoff" in t:
            iv = choose_interface_variable(task, interface_vars)
            ivs = node.get("interface_variables") or []
            if iv not in ivs:
                patch_ops.append({"op": "add", "path": f"/nodes/{target_id}/interface_variables/-", "value": iv})

    elif scope == "edge":
        edge = find_edge(graph, target_id)
        if not edge:
            raise ValueError(f"Target edge not found: {target_id}")
        t = title.lower()

        if edge.get("type", "").startswith("E3") and ("chart dependence" in t or "downgrade" in t or "e3" in t):
            iv = choose_interface_variable(task, interface_vars)
            patch_ops.append({"op": "replace", "path": f"/edges/{target_id}/type", "value": "E4_ChartBridge"})
            patch_ops.append({"op": "replace", "path": f"/edges/{target_id}/weight", "value": 0.6})
            new_just = f"Interface variable: {iv}. Proposed by A10 from hotspot task; review translation-specific seam behavior before transfer claims."
            patch_ops.append({"op": "replace", "path": f"/edges/{target_id}/justification", "value": new_just})

            # Bind interface variable on endpoints.
            s = edge.get("source")
            tnode = edge.get("target")
            for nid in [s, tnode]:
                n = find_node(graph, nid)
                if n is not None:
                    ivs = n.get("interface_variables") or []
                    if iv not in ivs:
                        patch_ops.append({"op": "add", "path": f"/nodes/{nid}/interface_variables/-", "value": iv})

        elif edge.get("type", "").startswith("E4") and ("promot" in t or "transfer" in t):
            patch_ops.append({"op": "replace", "path": f"/edges/{target_id}/type", "value": "E3_DiscriminatorTransfer"})
            patch_ops.append({"op": "replace", "path": f"/edges/{target_id}/weight", "value": 0.7})
            new_just = "Shared discriminator pattern: TODO. Shared observable axis: TODO. Transfer rationale: TODO establish stable split portability."
            patch_ops.append({"op": "replace", "path": f"/edges/{target_id}/justification", "value": new_just})

        # schema hygiene operation for edges
        if "schema" in t or "hygiene" in t or True:
            if "tags" not in edge:
                patch_ops.append({"op": "add", "path": f"/edges/{target_id}/tags", "value": ["a10_patch"]})
            if "evidence_refs" not in edge:
                patch_ops.append({"op": "add", "path": f"/edges/{target_id}/evidence_refs", "value": []})

    elif scope == "chart":
        # coverage tasks do not patch graph structure; produce no-op marker for traceability.
        patch_ops.append(
            {
                "op": "add",
                "path": "/meta/a10_notes/-",
                "value": f"Coverage suggestion for {target_id}: {title}",
            }
        )

    else:
        raise ValueError(f"Unsupported task scope: {scope}")

    patch_id = f"PATCH-{datetime.now(timezone.utc).strftime('%Y%m%d-%H%M%S')}"
    patch_obj = {
        "patch_id": patch_id,
        "task_id": task.get("id", "UNKNOWN"),
        "target": {"scope": scope, "id": target_id},
        "operations": patch_ops,
    }

    meta = {
        "title": title,
        "rationale": rationale,
        "acceptance_criteria": task.get("acceptance_criteria", ""),
        "suggested_agent": task.get("suggested_agent", ""),
    }

    return patch_obj, meta


def apply_ops(graph: Dict[str, Any], patch: Dict[str, Any]) -> Dict[str, Any]:
    g = copy.deepcopy(graph)

    def add_to_node_array(node_id: str, field: str, value: Any):
        n = find_node(g, node_id)
        if n is None:
            return
        arr = n.setdefault(field, [])
        if field == "interface_variables" and value in arr:
            return
        arr.append(value)

    for op in patch.get("operations", []):
        action = op.get("op")
        path = op.get("path", "")
        value = op.get("value")

        if path.startswith("/nodes/"):
            _, _, node_id, *rest = path.split("/")
            node = find_node(g, node_id)
            if node is None:
                continue
            if len(rest) >= 2 and rest[1] == "-" and action == "add":
                field = rest[0]
                add_to_node_array(node_id, field, value)
            elif len(rest) == 1:
                field = rest[0]
                if action in {"add", "replace"}:
                    node[field] = value

        elif path.startswith("/edges/"):
            _, _, edge_id, *rest = path.split("/")
            edge = find_edge(g, edge_id)
            if edge is None:
                continue
            if len(rest) == 1:
                field = rest[0]
                if action in {"add", "replace"}:
                    edge[field] = value

        elif path == "/meta/a10_notes/-" and action == "add":
            meta = g.setdefault("meta", {})
            arr = meta.setdefault("a10_notes", [])
            arr.append(value)

    return g


def make_patch_md(patch: Dict[str, Any], task_meta: Dict[str, Any]) -> str:
    ops = patch.get("operations", [])
    lines = []
    lines.append(f"# {patch['patch_id']}")
    lines.append("")
    lines.append(f"- Task: `{patch.get('task_id')}`")
    lines.append(f"- Target: `{patch.get('target',{}).get('scope')}` `{patch.get('target',{}).get('id')}`")
    lines.append("")
    lines.append("## Why This Addresses the Hotspot")
    lines.append(task_meta.get("rationale", "(no rationale provided)"))
    lines.append("")
    lines.append("## Operations")
    if not ops:
        lines.append("- No graph mutation ops (advisory patch only).")
    else:
        for op in ops:
            lines.append(f"- `{op.get('op')}` `{op.get('path')}`")
    lines.append("")
    lines.append("## What Could Go Wrong (New Seams)")
    lines.append("- Placeholder discriminator text may create false confidence if not refined before execution.")
    lines.append("- Edge reclassification can overfit current runs; validate with at least two additional seeds.")
    lines.append("- Interface-variable binding can be too generic if the selected variable is mismatched to observed seams.")
    lines.append("")
    lines.append("## Acceptance Criteria")
    lines.append(task_meta.get("acceptance_criteria", "(not provided)"))
    lines.append("")
    lines.append(f"- Suggested agent: `{task_meta.get('suggested_agent','A0_Integrator')}`")
    return "\n".join(lines) + "\n"


def _parse_interface_variable_from_justification(justification: str) -> str | None:
    if not justification:
        return None
    m = re.search(r"Interface variable:\s*([^\.]+)\.", justification)
    if not m:
        return None
    return m.group(1).strip()


def verify_patched_graph(graph: Dict[str, Any], known_interface_vars: List[str] | None = None) -> Dict[str, Any]:
    errors: List[str] = []
    warnings: List[str] = []

    nodes = graph.get("nodes", [])
    edges = graph.get("edges", [])
    node_ids = [n.get("id") for n in nodes]
    edge_ids = [e.get("id") for e in edges]

    # 1) ID integrity
    if len(node_ids) != len(set(node_ids)):
        errors.append("Node id uniqueness failed: duplicate node ids detected.")
    if len(edge_ids) != len(set(edge_ids)):
        errors.append("Edge id uniqueness failed: duplicate edge ids detected.")

    for n in nodes:
        dids = [d.get("id") for d in n.get("discriminators", [])]
        if len(dids) != len(set(dids)):
            errors.append(f"Discriminator id uniqueness failed within node {n.get('id')}.")

    # 2) Edge integrity
    node_id_set = set(node_ids)
    required_edge_fields = ["type", "weight", "justification", "tags", "evidence_refs"]
    for e in edges:
        eid = e.get("id")
        src = e.get("source")
        tgt = e.get("target")
        if src not in node_id_set:
            errors.append(f"Edge {eid} source missing node: {src}")
        if tgt not in node_id_set:
            errors.append(f"Edge {eid} target missing node: {tgt}")
        for f in required_edge_fields:
            if f not in e:
                errors.append(f"Edge {eid} missing required field: {f}")

    # 3) E4 interface binding integrity
    node_map = {n.get("id"): n for n in nodes}
    for e in edges:
        eid = e.get("id")
        etype = str(e.get("type", ""))
        if not etype.startswith("E4"):
            continue
        iv = e.get("interface_variable") or _parse_interface_variable_from_justification(str(e.get("justification", "")))
        if not iv:
            errors.append(f"E4 edge {eid} has no interface variable in field/justification.")
            continue
        if known_interface_vars and iv not in known_interface_vars:
            warnings.append(f"E4 edge {eid} uses interface variable not found in interface doc: {iv}")
        src = e.get("source")
        tgt = e.get("target")
        for nid in [src, tgt]:
            n = node_map.get(nid, {})
            ivs = n.get("interface_variables") or []
            if iv not in ivs:
                errors.append(f"E4 edge {eid} interface variable '{iv}' not bound on node {nid}.")

    # 4) Soft checks
    allowed_patterns = {
        "hysteresis",
        "ablation",
        "intervention",
        "orthogonal_probe",
        "interface_scatter",
        "ensemble_split",
        "stress_ramp",
    }
    for e in edges:
        w = e.get("weight")
        if isinstance(w, (int, float)):
            if w < 0 or w > 1:
                warnings.append(f"Edge {e.get('id')} has out-of-range weight: {w}")
        else:
            warnings.append(f"Edge {e.get('id')} has non-numeric weight: {w!r}")
        t = str(e.get("type", ""))
        if not (t.startswith("E1_") or t.startswith("E2_") or t.startswith("E3_") or t.startswith("E4_")):
            warnings.append(f"Edge {e.get('id')} has unknown type prefix: {t}")

    for n in nodes:
        for d in n.get("discriminators", []):
            p = d.get("pattern")
            if p not in allowed_patterns:
                warnings.append(f"Node {n.get('id')} discriminator {d.get('id')} has unknown pattern: {p}")
            how_to = str(d.get("how_to", ""))
            if "TODO" in how_to or "placeholder" in how_to.lower():
                warnings.append(
                    f"Node {n.get('id')} discriminator {d.get('id')} contains placeholder guidance in how_to."
                )

    return {
        "pass": len(errors) == 0,
        "errors": errors,
        "warnings": warnings,
    }


def make_verify_report(verify_result: Dict[str, Any], patched_path: Path, canonical_path: Path) -> str:
    lines = []
    status = "PASS" if verify_result.get("pass") else "FAIL"
    lines.append("# Patch Verify Report")
    lines.append("")
    lines.append(f"- Status: **{status}**")
    lines.append(f"- Patched graph: `{patched_path}`")
    lines.append(f"- Canonical graph: `{canonical_path}`")
    lines.append("")
    lines.append("## Errors")
    if not verify_result.get("errors"):
        lines.append("- none")
    else:
        for e in verify_result["errors"]:
            lines.append(f"- {e}")
    lines.append("")
    lines.append("## Warnings")
    if not verify_result.get("warnings"):
        lines.append("- none")
    else:
        for w in verify_result["warnings"]:
            lines.append(f"- {w}")
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate guided graph patch artifacts from task suggestions.")
    parser.add_argument("--list", action="store_true", help="List last N task suggestions and exit.")
    parser.add_argument("--last-n", type=int, default=20, help="Number of latest suggestions to inspect.")
    parser.add_argument("--task-id", default=None, help="Pick task by id (e.g., TASK-001).")
    parser.add_argument("--index", type=int, default=None, help="Pick task by 1-based index in latest list.")
    parser.add_argument("--apply", action="store_true", help="Overwrite canonical lcg/lcg_graph.json.")
    parser.add_argument("--force", action="store_true", help="Allow --apply even if verify checks fail.")
    args = parser.parse_args()

    _bootstrap_ci_python()
    from ci import paths as ci_paths

    ci_paths.ensure_runtime_dirs()
    repo = ci_paths.repo_root()
    graph_path = ci_paths.lcg_graph_path()
    suggestion_path = ci_paths.task_suggestions_path()
    iface_path = ci_paths.reports_dir() / "interface_variables.md"

    graph = read_json(graph_path)
    suggestions_all, suggestion_warnings = load_task_suggestions(suggestion_path)
    suggestions = suggestions_all[-args.last_n :]
    if suggestion_warnings:
        print(
            f"WARN: skipped {len(suggestion_warnings)} malformed task suggestion entries from {suggestion_path}",
            file=sys.stderr,
        )
        for msg in suggestion_warnings[:5]:
            print(f"  - {msg}", file=sys.stderr)

    if not suggestions_all:
        # Fallback seed task to keep assistant operational before first persisted suggestions file.
        suggestions_all = [
            {
                "id": "TASK-BOOTSTRAP",
                "priority": "P2",
                "scope": "node",
                "target_id": "Q000021",
                "title": "Node Q000021: Add orthogonal_probe discriminator for seam visibility under re-description",
                "rationale": "No persisted task suggestions yet; bootstrap patch proposes additional discriminator coverage on the method-to-ontology bridge node.",
                "acceptance_criteria": "Node gains a second non-overlapping discriminator and rerun artifacts confirm seam visibility under handoff translation.",
                "suggested_agent": "C1_Method_Specialist",
            }
        ]
        suggestions = suggestions_all

    if args.list:
        if not suggestions:
            print("No task suggestions found.")
            return 0
        for i, t in enumerate(suggestions, start=1):
            print(f"{i:02d}. {t.get('id','?')} | {t.get('scope')} {t.get('target_id')} | {t.get('title')}")
        return 0

    if not suggestions:
        raise SystemExit("No task suggestions available.")

    task = None
    if args.task_id:
        for t in reversed(suggestions_all):
            if t.get("id") == args.task_id:
                task = t
                break
        if task is None:
            raise SystemExit(f"Task id not found: {args.task_id}")
    elif args.index is not None:
        idx = args.index - 1
        if idx < 0 or idx >= len(suggestions):
            raise SystemExit(f"Index out of range: {args.index}")
        task = suggestions[idx]
    else:
        task = suggestions[-1]

    interface_vars = parse_interface_variables(iface_path)
    patch, task_meta = build_patch(task, graph, interface_vars)

    patched = apply_ops(graph, patch)

    patches_dir = ci_paths.patches_dir()
    patches_dir.mkdir(parents=True, exist_ok=True)
    patch_json_path = patches_dir / f"{patch['patch_id']}.json"
    patch_md_path = patches_dir / f"{patch['patch_id']}.md"
    write_json(patch_json_path, patch)
    patch_md_path.write_text(make_patch_md(patch, task_meta), encoding="utf-8")

    patched_copy = ci_paths.lcg_graph_path().parent / "lcg_graph.patched.json"
    write_json(patched_copy, patched)

    verify = verify_patched_graph(patched, known_interface_vars=interface_vars)
    verify_report_path = ci_paths.reports_dir() / "patch_verify_report.md"
    verify_report_path.write_text(
        make_verify_report(verify, patched_copy, graph_path), encoding="utf-8"
    )

    print(f"Generated patch: {patch_json_path}")
    print(f"Generated explainer: {patch_md_path}")
    print(f"Patched graph copy: {patched_copy}")
    print(f"Verification report: {verify_report_path}")
    print(
        f"Verification status: {'PASS' if verify.get('pass') else 'FAIL'} "
        f"(errors={len(verify.get('errors', []))}, warnings={len(verify.get('warnings', []))})"
    )
    if args.apply:
        if verify.get("pass") or args.force:
            write_json(graph_path, patched)
            print(f"Applied to canonical graph: {graph_path}")
            if (not verify.get("pass")) and args.force:
                print("Applied with --force despite verification FAIL.")
        else:
            print("Refused --apply because verification FAILED. Use --force to override.")
    else:
        print("Canonical graph unchanged (use --apply to overwrite).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
