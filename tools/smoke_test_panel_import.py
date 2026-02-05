#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    python_dir = repo / "houdini_package" / "python"
    if str(python_dir) not in sys.path:
        sys.path.insert(0, str(python_dir))

    from ci_panels.CI_GraphOverlay_panel import CIGraphOverlayPanel, QtWidgets  # type: ignore

    if QtWidgets is None:
        print("OK (module import only; Qt unavailable in this runtime)")
        return 0

    app = QtWidgets.QApplication.instance() or QtWidgets.QApplication([])
    panel = CIGraphOverlayPanel()
    panel.deleteLater()
    if app is not None:
        app.quit()
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
