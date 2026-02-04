"""Minimal CI Graph Overlay panel (PySide2 + QGraphicsScene)."""

from __future__ import annotations

import json
import traceback
from datetime import datetime, timezone
from pathlib import Path

try:
    from PySide2 import QtCore, QtGui, QtWidgets
except Exception:  # pragma: no cover
    QtCore = QtGui = QtWidgets = None


class CIGraphOverlayPanel(QtWidgets.QWidget if QtWidgets else object):
    EDGE_KIND_ORDER = ["E3", "E4", "E1"]

    def __init__(self, parent=None):
        if not QtWidgets:
            return
        super().__init__(parent)
        self.setWindowTitle("CI Graph Overlay")

        import sys

        pkg_python = Path(__file__).resolve().parents[1] / "python"
        if str(pkg_python) not in sys.path:
            sys.path.insert(0, str(pkg_python))

        from ci import aggregate, graph, registry, run_store, suggest, trends

        self._aggregate_mod = aggregate
        self._graph_mod = graph
        self._registry_mod = registry
        self._run_store = run_store
        self._suggest_mod = suggest
        self._trends_mod = trends
        self._graph = graph.load_lcg_graph()
        self._index = graph.index_nodes_edges(self._graph)
        self._registry = registry.load_registry()
        self._chart_modes = registry.load_chart_modes()
        self._overlay = None
        self._agg_stats = {"node_stats": {}, "edge_stats": {}, "probe_stats": {}, "errors": []}
        self._task_suggestions = []
        self._trend_diff = {"node_deltas": {}, "edge_deltas": {}, "seam_kind_delta_total": {}}

        self._build_ui()
        self._load_runs()
        self._redraw_scene()

    def _build_ui(self):
        root = QtWidgets.QVBoxLayout(self)

        controls = QtWidgets.QHBoxLayout()
        self.refresh_btn = QtWidgets.QPushButton("Refresh Runs")
        self.refresh_btn.clicked.connect(self._load_runs)

        self.mode_combo = QtWidgets.QComboBox()
        self.mode_combo.addItem("Single run", "single")
        self.mode_combo.addItem("Aggregate", "aggregate")
        self.mode_combo.currentIndexChanged.connect(self._on_mode_changed)

        self.n_runs_spin = QtWidgets.QSpinBox()
        self.n_runs_spin.setRange(1, 500)
        self.n_runs_spin.setValue(25)
        self.n_runs_spin.valueChanged.connect(self._on_aggregate_params_changed)

        self.constellation_combo = QtWidgets.QComboBox()
        self.constellation_combo.addItem("All", "ALL")
        for c in self._index["constellation_order"]:
            self.constellation_combo.addItem(c, c)
        self.constellation_combo.currentIndexChanged.connect(self._redraw_scene)

        self.edge_checks = {}
        for kind in self.EDGE_KIND_ORDER:
            cb = QtWidgets.QCheckBox(kind)
            cb.setChecked(True)
            cb.stateChanged.connect(self._redraw_scene)
            self.edge_checks[kind] = cb

        controls.addWidget(self.refresh_btn)
        controls.addWidget(QtWidgets.QLabel("Mode"))
        controls.addWidget(self.mode_combo)
        controls.addWidget(QtWidgets.QLabel("N runs"))
        controls.addWidget(self.n_runs_spin)
        controls.addWidget(QtWidgets.QLabel("Constellation"))
        controls.addWidget(self.constellation_combo)
        controls.addWidget(QtWidgets.QLabel("Edge Types"))
        for kind in self.EDGE_KIND_ORDER:
            controls.addWidget(self.edge_checks[kind])
        controls.addStretch(1)

        root.addLayout(controls)

        body = QtWidgets.QSplitter()
        body.setOrientation(QtCore.Qt.Horizontal)

        self.run_list = QtWidgets.QListWidget()
        self.run_list.currentRowChanged.connect(self._on_run_selected)
        body.addWidget(self.run_list)

        self.scene = QtWidgets.QGraphicsScene(self)
        self.view = QtWidgets.QGraphicsView(self.scene)
        self.view.setRenderHint(QtGui.QPainter.Antialiasing, True)
        body.addWidget(self.view)

        right_pane = QtWidgets.QWidget()
        right_layout = QtWidgets.QVBoxLayout(right_pane)

        self.right_tabs = QtWidgets.QTabWidget()

        # Overview tab
        overview_tab = QtWidgets.QWidget()
        overview_layout = QtWidgets.QVBoxLayout(overview_tab)
        self.details = QtWidgets.QPlainTextEdit()
        self.details.setReadOnly(True)
        overview_layout.addWidget(self.details)

        task_controls = QtWidgets.QHBoxLayout()
        self.generate_tasks_btn = QtWidgets.QPushButton("Generate Tasks")
        self.generate_tasks_btn.clicked.connect(self._generate_tasks)
        self.copy_task_btn = QtWidgets.QPushButton("Copy Selected")
        self.copy_task_btn.clicked.connect(self._copy_selected_task)
        self.save_suggestions_cb = QtWidgets.QCheckBox("Save Suggestions")
        self.generate_tasks_btn.setEnabled(False)
        self.copy_task_btn.setEnabled(False)
        task_controls.addWidget(self.generate_tasks_btn)
        task_controls.addWidget(self.copy_task_btn)
        task_controls.addWidget(self.save_suggestions_cb)
        task_controls.addStretch(1)
        overview_layout.addLayout(task_controls)

        self.task_list = QtWidgets.QListWidget()
        overview_layout.addWidget(self.task_list)

        self.right_tabs.addTab(overview_tab, "Overview")

        # Trend tab
        trend_tab = QtWidgets.QWidget()
        trend_layout = QtWidgets.QVBoxLayout(trend_tab)
        trend_controls = QtWidgets.QHBoxLayout()
        self.trend_recent_spin = QtWidgets.QSpinBox()
        self.trend_recent_spin.setRange(1, 500)
        self.trend_recent_spin.setValue(25)
        self.trend_prev_spin = QtWidgets.QSpinBox()
        self.trend_prev_spin.setRange(1, 500)
        self.trend_prev_spin.setValue(25)
        self.trend_refresh_btn = QtWidgets.QPushButton("Refresh Trend")
        self.trend_refresh_btn.clicked.connect(self._refresh_trend)
        trend_controls.addWidget(QtWidgets.QLabel("Recent N"))
        trend_controls.addWidget(self.trend_recent_spin)
        trend_controls.addWidget(QtWidgets.QLabel("Previous N"))
        trend_controls.addWidget(self.trend_prev_spin)
        trend_controls.addWidget(self.trend_refresh_btn)
        trend_controls.addStretch(1)
        trend_layout.addLayout(trend_controls)

        self.trend_text = QtWidgets.QPlainTextEdit()
        self.trend_text.setReadOnly(True)
        trend_layout.addWidget(self.trend_text)
        self.trend_suggestions_list = QtWidgets.QListWidget()
        trend_layout.addWidget(self.trend_suggestions_list)
        self.right_tabs.addTab(trend_tab, "Trend")

        right_layout.addWidget(self.right_tabs)

        body.addWidget(right_pane)
        body.setSizes([240, 760, 420])
        root.addWidget(body)

    def _load_runs(self):
        try:
            self.run_list.clear()
            self._run_paths = self._run_store.list_recent_runs(limit=50)
            self._recompute_aggregate()
            self._refresh_trend()
            for path in self._run_paths:
                try:
                    summary = self._run_store.summarize_run(path)
                except Exception:
                    continue
                text = f"{summary['record_id']} | {summary['probe_id']} | {summary['pass_fail']} | seams={summary['seam_count']}"
                item = QtWidgets.QListWidgetItem(text)
                item.setData(QtCore.Qt.UserRole, summary)
                self.run_list.addItem(item)
            if self.run_list.count() > 0:
                self.run_list.setCurrentRow(0)
                self._refresh_details_for_mode()
            else:
                self._overlay = None
                self.details.setPlainText("No recent runs found.")
                self._redraw_scene()
        except Exception as exc:
            self.details.setPlainText(f"ERROR loading runs: {exc}\n{traceback.format_exc()}")

    def _recompute_aggregate(self):
        n = self.n_runs_spin.value()
        paths = self._run_paths[:n] if hasattr(self, "_run_paths") else []
        self._agg_stats = self._aggregate_mod.aggregate_runs(paths)

    def _refresh_trend(self):
        run_paths = getattr(self, "_run_paths", [])
        n_recent = self.trend_recent_spin.value()
        n_prev = self.trend_prev_spin.value()
        recent_paths = run_paths[:n_recent]
        prev_paths = run_paths[n_recent : n_recent + n_prev]
        stats_recent = self._trends_mod.aggregate_window(recent_paths)
        stats_prev = self._trends_mod.aggregate_window(prev_paths)
        self._trend_diff = self._trends_mod.diff_stats(stats_prev, stats_recent)
        self._render_trend()

    def _load_recent_suggestions(self, limit=10):
        p = self._suggestions_jsonl_path()
        if not p.exists():
            return []
        rows = []
        with p.open("r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    rows.append(json.loads(line))
                except Exception:
                    continue
        return rows[-limit:]

    def _render_trend(self):
        diff = self._trend_diff
        node_d = diff.get("node_deltas", {})
        edge_d = diff.get("edge_deltas", {})
        seam_delta = diff.get("seam_kind_delta_total", {})

        node_items = []
        for nid, d in node_d.items():
            node_items.append((nid, d.get("fail_rate_delta", 0.0), d.get("seam_hits_delta", 0)))
        improving_nodes = sorted(node_items, key=lambda x: (x[1], x[2]))[:5]
        worsening_nodes = sorted(node_items, key=lambda x: (x[1], x[2]), reverse=True)[:5]

        edge_items = []
        for eid, d in edge_d.items():
            edge_items.append((eid, d.get("hit_delta", 0)))
        improving_edges = sorted(edge_items, key=lambda x: x[1])[:5]
        worsening_edges = sorted(edge_items, key=lambda x: x[1], reverse=True)[:5]

        lines = []
        wa = diff.get("window_a", {})
        wb = diff.get("window_b", {})
        lines.append(
            f"Recent window: runs={wb.get('runs_considered',0)} start={wb.get('window_start')} end={wb.get('window_end')}"
        )
        lines.append(
            f"Previous window: runs={wa.get('runs_considered',0)} start={wa.get('window_start')} end={wa.get('window_end')}"
        )
        lines.append("")
        lines.append("Top 5 improving nodes (delta fail_rate, delta seams):")
        for nid, frd, shd in improving_nodes:
            lines.append(f"  - {nid}: fail_rate_delta={frd:+.2f}, seam_hits_delta={shd:+d}")
        lines.append("")
        lines.append("Top 5 worsening nodes (delta fail_rate, delta seams):")
        for nid, frd, shd in worsening_nodes:
            lines.append(f"  - {nid}: fail_rate_delta={frd:+.2f}, seam_hits_delta={shd:+d}")
        lines.append("")
        lines.append("Top 5 improving edges (delta hits):")
        for eid, hd in improving_edges:
            lines.append(f"  - {eid}: hit_delta={hd:+d}")
        lines.append("")
        lines.append("Top 5 worsening edges (delta hits):")
        for eid, hd in worsening_edges:
            lines.append(f"  - {eid}: hit_delta={hd:+d}")
        lines.append("")
        lines.append(f"Seam kind shifts: {seam_delta if seam_delta else 'none'}")
        self.trend_text.setPlainText("\n".join(lines))

        # Suggestions with trend markers
        self.trend_suggestions_list.clear()
        recent_suggestions = self._load_recent_suggestions(limit=10)
        if not recent_suggestions:
            self.trend_suggestions_list.addItem("No persisted suggestions found.")
            return
        for s in recent_suggestions:
            target = s.get("target_id", "?")
            scope = s.get("scope", "?")
            marker = "→"
            if scope == "node" and target in node_d:
                frd = node_d[target].get("fail_rate_delta", 0.0)
                if frd < -1e-9:
                    marker = "↑ improving"
                elif frd > 1e-9:
                    marker = "↓ worsening"
            elif scope == "edge" and target in edge_d:
                hd = edge_d[target].get("hit_delta", 0)
                if hd < 0:
                    marker = "↑ improving"
                elif hd > 0:
                    marker = "↓ worsening"
            title = s.get("title", "(untitled)")
            self.trend_suggestions_list.addItem(f"{marker} | {scope} {target} | {title}")

    def _on_mode_changed(self):
        is_agg = self.mode_combo.currentData() == "aggregate"
        self.generate_tasks_btn.setEnabled(is_agg)
        self.copy_task_btn.setEnabled(is_agg)
        self._refresh_details_for_mode()
        self._redraw_scene()

    def _on_aggregate_params_changed(self):
        self._recompute_aggregate()
        self._refresh_trend()
        if self.mode_combo.currentData() == "aggregate":
            self._refresh_details_for_mode()
            self._redraw_scene()

    def _on_run_selected(self, row: int):
        if row < 0 or row >= self.run_list.count():
            return
        item = self.run_list.item(row)
        summary = item.data(QtCore.Qt.UserRole)
        run_data = self._run_store.load_run(summary["path"])
        self._overlay = self._graph_mod.apply_run_overlay(run_data)
        if self.mode_combo.currentData() == "single":
            self._update_single_details(summary)
        self._redraw_scene()

    def _update_single_details(self, summary):
        lines = []
        lines.append(f"probe_id: {summary['probe_id']}")
        lines.append(f"chart_mode: {summary['chart_mode']}")
        lines.append(f"node_id: {summary['node_id']}")
        lines.append(f"pass/fail: {summary['pass_fail']}")
        lines.append(f"seam_count: {summary['seam_count']}")
        lines.append("")
        lines.append("seam_flags:")
        if not summary["seam_flags"]:
            lines.append("  - none")
        else:
            for sf in summary["seam_flags"]:
                lines.append(
                    "  - severity={severity} scope={scope} kind={kind} desc={desc}".format(
                        severity=sf.get("severity", "?"),
                        scope=sf.get("scope", "?"),
                        kind=sf.get("kind", "?"),
                        desc=sf.get("description", ""),
                    )
                )
        self.details.setPlainText("\n".join(lines))

    def _update_aggregate_details(self):
        stats = self._agg_stats
        node_stats = stats.get("node_stats", {})
        edge_stats = stats.get("edge_stats", {})

        def node_rank(item):
            _nid, d = item
            fail_rate = (d["fails"] / d["runs"]) if d["runs"] else 0.0
            return (fail_rate, d["seam_hits"], d["runs"])

        top_nodes = sorted(node_stats.items(), key=node_rank, reverse=True)[:5]
        top_edges = sorted(edge_stats.items(), key=lambda kv: kv[1]["hits"], reverse=True)[:5]

        seam_kind_total = {}
        for d in node_stats.values():
            for k, v in d.get("seam_kind_counts", {}).items():
                seam_kind_total[k] = seam_kind_total.get(k, 0) + v

        lines = []
        lines.append(f"mode: AGGREGATE (last {self.n_runs_spin.value()} runs)")
        lines.append(f"loaded_runs: {min(self.n_runs_spin.value(), len(getattr(self, '_run_paths', [])))}")
        if stats.get("errors"):
            lines.append(f"malformed_runs_skipped: {len(stats['errors'])}")
        lines.append("")
        lines.append("top-5 hottest nodes:")
        if not top_nodes:
            lines.append("  - none")
        else:
            for nid, d in top_nodes:
                fr = (d["fails"] / d["runs"]) if d["runs"] else 0.0
                lines.append(f"  - {nid}: runs={d['runs']} fails={d['fails']} fail_rate={fr:.2f} seams={d['seam_hits']}")
        lines.append("")
        lines.append("top-5 hottest edges:")
        if not top_edges:
            lines.append("  - none")
        else:
            for eid, d in top_edges:
                lines.append(f"  - {eid}: hits={d['hits']} kinds={d.get('seam_kind_counts', {})}")
        lines.append("")
        lines.append(f"seam kinds: {seam_kind_total if seam_kind_total else 'none'}")
        self.details.setPlainText("\n".join(lines))

    def _refresh_details_for_mode(self):
        if self.mode_combo.currentData() == "aggregate":
            self._update_aggregate_details()
            return
        row = self.run_list.currentRow()
        if row >= 0 and row < self.run_list.count():
            item = self.run_list.item(row)
            summary = item.data(QtCore.Qt.UserRole)
            self._update_single_details(summary)
        else:
            self.details.setPlainText("No run selected.")

    def _task_to_markdown(self, task):
        scope_label = task["scope"].capitalize()
        lines = [
            f"- [ ] ({task['priority']}) {scope_label} {task['target_id']}: {task['title']}",
            f"  - Rationale: {task['rationale']}",
            f"  - Acceptance: {task['acceptance_criteria']}",
            f"  - Suggested agent: {task['suggested_agent']}",
        ]
        prov = task.get("provenance") or {}
        if prov:
            runs = prov.get("runs", "?")
            ws = prov.get("window_start")
            we = prov.get("window_end")
            if ws and we:
                lines.append(f"  - Provenance: runs={runs}, window_start={ws}, window_end={we}")
            else:
                lines.append(f"  - Provenance: runs={runs}")
            lines.append(f"  - Provenance seam_kinds: {prov.get('seam_kinds', {})}")
            if "fail_rate" in prov:
                lines.append(f"  - Provenance fail_rate: {prov.get('fail_rate'):.2f}")
            if "edge_hits" in prov:
                lines.append(f"  - Provenance edge_hits: {prov.get('edge_hits')}")
            lines.append(f"  - Provenance probes: {prov.get('probes', [])}")
        return "\n".join(lines)

    def _suggestions_jsonl_path(self) -> Path:
        pkg_root = Path(__file__).resolve().parents[1]
        out_dir = pkg_root / "output" / "ledger"
        out_dir.mkdir(parents=True, exist_ok=True)
        return out_dir / "task_suggestions.jsonl"

    def _save_suggestions(self, tasks):
        p = self._suggestions_jsonl_path()
        now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")
        with p.open("a", encoding="utf-8") as f:
            for t in tasks:
                rec = {"timestamp": now, **t}
                f.write(json.dumps(rec) + "\n")
        self.details.appendPlainText(f"\nSaved {len(tasks)} suggestions to {p}")

    def _generate_tasks(self):
        if self.mode_combo.currentData() != "aggregate":
            self.details.appendPlainText("\nTask generation is available in Aggregate mode.")
            return
        self._recompute_aggregate()
        self._task_suggestions = self._suggest_mod.suggest_tasks(
            self._agg_stats, self._graph, self._registry, self._chart_modes
        )
        self.task_list.clear()
        for task in self._task_suggestions[:10]:
            item = QtWidgets.QListWidgetItem(
                f"{task['priority']} | {task['scope']} {task['target_id']} | {task['title']}"
            )
            item.setData(QtCore.Qt.UserRole, task)
            self.task_list.addItem(item)
        if self.save_suggestions_cb.isChecked() and self._task_suggestions:
            self._save_suggestions(self._task_suggestions[:10])
        self.details.appendPlainText(f"\nGenerated {min(len(self._task_suggestions), 10)} task suggestions.")

    def _copy_selected_task(self):
        item = self.task_list.currentItem()
        if not item:
            self.details.appendPlainText("\nNo task selected.")
            return
        task = item.data(QtCore.Qt.UserRole)
        md = self._task_to_markdown(task)
        QtWidgets.QApplication.clipboard().setText(md)
        self.details.appendPlainText("\nCopied selected task markdown to clipboard.")

    def _visible_constellation(self) -> str:
        return self.constellation_combo.currentData()

    def _visible_edge_kinds(self) -> set[str]:
        return {k for k, cb in self.edge_checks.items() if cb.isChecked()}

    def _redraw_scene(self):
        self.scene.clear()

        visible_constellation = self._visible_constellation()
        visible_edge_kinds = self._visible_edge_kinds()

        nodes = self._index["nodes"]
        edges = self._index["edges"]
        cols = self._index["constellation_order"]
        is_aggregate = self.mode_combo.currentData() == "aggregate"
        node_stats = self._agg_stats.get("node_stats", {}) if is_aggregate else {}
        edge_stats = self._agg_stats.get("edge_stats", {}) if is_aggregate else {}

        x_spacing = 260
        y_spacing = 84
        x0 = 30
        y0 = 40

        col_nodes = {c: [] for c in cols}
        other_nodes = []
        for nid, node in sorted(nodes.items()):
            c = node.get("constellation", "UNASSIGNED")
            if c in col_nodes:
                col_nodes[c].append(node)
            else:
                other_nodes.append(node)

        if visible_constellation != "ALL":
            for c in cols:
                if c != visible_constellation:
                    col_nodes[c] = []

        positions = {}

        for ci, c in enumerate(cols):
            x = x0 + ci * x_spacing
            self.scene.addText(c).setPos(x, 4)
            for ni, node in enumerate(col_nodes[c]):
                y = y0 + ni * y_spacing
                positions[node["id"]] = (x, y)

        # Draw edges first.
        max_edge_hits = max((d.get("hits", 0) for d in edge_stats.values()), default=0)
        for edge in edges:
            if edge["kind"] not in visible_edge_kinds:
                continue
            s = edge["source"]
            t = edge["target"]
            if s not in positions or t not in positions:
                continue

            sx, sy = positions[s]
            tx, ty = positions[t]
            p1 = QtCore.QPointF(sx + 70, sy + 14)
            p2 = QtCore.QPointF(tx + 70, ty + 14)

            pen = QtGui.QPen(QtGui.QColor(130, 130, 130), 1.2)
            if edge["kind"] == "E3":
                pen.setColor(QtGui.QColor(60, 110, 180))
                pen.setWidthF(1.6)
            elif edge["kind"] == "E4":
                pen.setColor(QtGui.QColor(90, 150, 90))
                pen.setStyle(QtCore.Qt.DashLine)
            elif edge["kind"] == "E1":
                pen.setColor(QtGui.QColor(140, 140, 140))
                pen.setStyle(QtCore.Qt.DotLine)

            if self._overlay and edge["id"] in self._overlay["highlighted_edge_ids"]:
                pen.setColor(QtGui.QColor(200, 60, 60))
                pen.setWidthF(2.4)
            elif is_aggregate:
                hits = edge_stats.get(edge["id"], {}).get("hits", 0)
                if hits > 0 and max_edge_hits > 0:
                    intensity = hits / max_edge_hits
                    pen.setColor(QtGui.QColor(230, 120, 40))
                    pen.setWidthF(1.0 + 2.0 * intensity)

            self.scene.addLine(QtCore.QLineF(p1, p2), pen)

        # Draw nodes.
        max_fail_rate = 0.0
        max_seams = 0
        if is_aggregate:
            for d in node_stats.values():
                if d.get("runs"):
                    max_fail_rate = max(max_fail_rate, d["fails"] / d["runs"])
                max_seams = max(max_seams, d.get("seam_hits", 0))

        for nid, (x, y) in positions.items():
            node = nodes[nid]
            rect = QtCore.QRectF(x, y, 140, 28)
            brush = QtGui.QBrush(QtGui.QColor(230, 230, 235))
            border = QtGui.QPen(QtGui.QColor(80, 80, 90), 1.0)

            if self._overlay and self._overlay.get("active_node_id") == nid:
                if self._overlay.get("seam_count", 0) > 0:
                    brush = QtGui.QBrush(QtGui.QColor(245, 180, 180))
                else:
                    brush = QtGui.QBrush(QtGui.QColor(185, 230, 185))
                border = QtGui.QPen(QtGui.QColor(30, 30, 30), 1.6)
            elif is_aggregate and nid in node_stats:
                d = node_stats[nid]
                fail_rate = (d["fails"] / d["runs"]) if d["runs"] else 0.0
                seam_hits = d.get("seam_hits", 0)
                fail_intensity = (fail_rate / max_fail_rate) if max_fail_rate > 0 else 0.0
                seam_intensity = (seam_hits / max_seams) if max_seams > 0 else 0.0
                intensity = min(1.0, max(fail_intensity, seam_intensity))
                # Heatmap from gray to red-orange.
                r = int(225 + 30 * intensity)
                g = int(225 - 120 * intensity)
                b = int(230 - 140 * intensity)
                brush = QtGui.QBrush(QtGui.QColor(r, g, b))
                border = QtGui.QPen(QtGui.QColor(90, 70, 70), 1.2)

            self.scene.addRect(rect, border, brush)
            label = f"{nid}"
            if self._overlay and self._overlay.get("active_node_id") == nid:
                label += "  [active]"
            elif is_aggregate and nid in node_stats:
                d = node_stats[nid]
                fr = (d["fails"] / d["runs"]) if d["runs"] else 0.0
                label += f"  [h={d.get('seam_hits',0)} fr={fr:.2f}]"
            text_item = self.scene.addText(label)
            text_item.setPos(x + 4, y + 4)

        self.scene.setSceneRect(0, 0, x0 + len(cols) * x_spacing + 120, 900)


def createPanelInterface():  # Houdini panel entrypoint
    if not QtWidgets:
        raise RuntimeError("PySide2 is unavailable in this environment.")
    return CIGraphOverlayPanel()
