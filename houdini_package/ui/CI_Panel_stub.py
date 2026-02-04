"""Minimal Houdini Python Panel stub for A9.3 vertical slice."""

from __future__ import annotations

import traceback

try:
    from PySide2 import QtWidgets
except Exception:  # pragma: no cover - Houdini env dependent
    QtWidgets = None


class CIPanelStub(QtWidgets.QWidget if QtWidgets else object):
    def __init__(self, parent=None):
        if not QtWidgets:
            return
        super().__init__(parent)
        self.setWindowTitle("CI Panel Stub")

        from pathlib import Path
        import sys

        pkg_python = Path(__file__).resolve().parents[1] / "python"
        if str(pkg_python) not in sys.path:
            sys.path.insert(0, str(pkg_python))

        from ci import registry

        self._registry = registry.load_registry()
        self._chart_modes = registry.load_chart_modes()

        layout = QtWidgets.QVBoxLayout(self)

        self.probe_combo = QtWidgets.QComboBox()
        for probe in self._registry["probes"]:
            self.probe_combo.addItem(f"{probe['id']} - {probe['name']}", probe["id"])

        self.chart_combo = QtWidgets.QComboBox()
        for mode in self._chart_modes["chart_modes"]:
            self.chart_combo.addItem(f"{mode['id']} - {mode['name']}", mode["id"])

        run_btn = QtWidgets.QPushButton("Run Probe")
        run_btn.clicked.connect(self._run_probe)

        self.log = QtWidgets.QPlainTextEdit()
        self.log.setReadOnly(True)

        layout.addWidget(QtWidgets.QLabel("Probe"))
        layout.addWidget(self.probe_combo)
        layout.addWidget(QtWidgets.QLabel("Chart Mode"))
        layout.addWidget(self.chart_combo)
        layout.addWidget(run_btn)
        layout.addWidget(QtWidgets.QLabel("Log"))
        layout.addWidget(self.log)

    def _append(self, text: str) -> None:
        self.log.appendPlainText(text)

    def _run_probe(self):
        try:
            from ci.runner import run_probe

            probe_id = self.probe_combo.currentData()
            chart_mode_id = self.chart_combo.currentData()
            result = run_probe(probe_id=probe_id, chart_mode_id=chart_mode_id, stub_mode=True)
            self._append(
                f"{result['pass_fail']} | seams={result['seam_count']} | probe_output={result['probe_output_path']}"
            )
            outputs = result["probe_output"]["observable_values"]["outputs"]
            metrics = ", ".join([f"{k}={v}" for k, v in outputs.items() if k not in {"pass_fail", "seam_count"}])
            if metrics:
                self._append(f"metrics: {metrics}")
            if result["pass_fail"] == "FAIL":
                seam_types = []
                for sf in result["probe_output"]["observable_values"]["seam_flags"]:
                    desc = sf.get("description", "")
                    if "seam_type=" in desc:
                        seam_types.append(desc.split("seam_type=", 1)[1].split()[0])
                    else:
                        seam_types.append(sf.get("kind", "unknown"))
                self._append(f"seam_types: {', '.join(seam_types)}")
            self._append(f"ledger={result['ledger_paths']['ledger_event_json']}")
        except Exception as exc:  # pragma: no cover - UI feedback
            self._append(f"ERROR: {exc}")
            self._append(traceback.format_exc())


def createPanelInterface():  # Houdini panel entrypoint
    if not QtWidgets:
        raise RuntimeError("PySide2 is unavailable in this environment.")
    return CIPanelStub()
