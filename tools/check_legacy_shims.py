#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    legacy_panel = repo / "houdini_package" / "ui" / "CI_GraphOverlay_panel.py"
    canonical_panel = repo / "houdini_package" / "python" / "ci_panels" / "CI_GraphOverlay_panel.py"
    legacy_package = repo / "houdini_package" / "ci_package.json"
    canonical_package = repo / "houdini_package" / "package.json"

    errors = []

    if not canonical_panel.exists():
        errors.append(f"Missing canonical panel: {canonical_panel}")
    if not canonical_package.exists():
        errors.append(f"Missing canonical package file: {canonical_package}")
    if not legacy_package.exists():
        errors.append(f"Missing legacy compatibility package file: {legacy_package}")

    if not legacy_panel.exists():
        errors.append(f"Missing legacy shim file: {legacy_panel}")
    else:
        text = legacy_panel.read_text(encoding="utf-8")
        must_have = [
            "Legacy shim for CI Graph Overlay panel",
            "from ci_panels.CI_GraphOverlay_panel import CIGraphOverlayPanel",
            '__all__ = ["CIGraphOverlayPanel"]',
        ]
        for marker in must_have:
            if marker not in text:
                errors.append(f"Legacy shim missing marker: {marker}")
        # Guard against full duplicate implementation drifting back in.
        banned_markers = ["class CIGraphOverlayPanel", "from PySide2", "from PySide6"]
        for marker in banned_markers:
            if marker in text:
                errors.append(f"Legacy shim should not implement panel logic ({marker})")

    if errors:
        for err in errors:
            print(f"FAIL: {err}")
        return 1

    print("OK: legacy shim/package compatibility checks passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
