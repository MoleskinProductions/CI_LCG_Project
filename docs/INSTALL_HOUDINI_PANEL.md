# Install CI Graph Overlay Panel (Houdini 21)

## 1) Register the package
- Ensure this repo is on disk, then place a package file in `~/houdini21.0/packages/`.
- Option A (recommended): symlink this file:
  - `~/houdini21.0/packages/ci_lcg.json -> <repo>/houdini_package/package.json`
- Option B: copy `houdini_package/package.json` into `~/houdini21.0/packages/` and adjust paths if needed.

## 2) Verify Houdini path wiring
- Launch Houdini 21 and check the package is loaded.
- The package sets:
  - `HOUDINI_PATH` to include `<repo>/houdini_package/houdini`
  - `PYTHONPATH` to include `<repo>/houdini_package/python`
  - `HOUDINI_PYTHON_PANEL_PATH` to include `<repo>/houdini_package/houdini/python_panels`

## 3) Open the panel
- In Houdini: `New Pane Tab Type` -> `Python Panel` -> select **CI Graph Overlay**.

## 4) Troubleshooting
- **Panel missing in list**
  - Confirm package JSON is under `~/houdini21.0/packages/`.
  - Confirm panel definition exists: `houdini_package/houdini/python_panels/CI_GraphOverlay.pypanel`.
- **Import error for `ci` or `ci_panels`**
  - Verify `PYTHONPATH` includes `<repo>/houdini_package/python`.
  - Run smoke test:
    - `python tools/smoke_test_panel_import.py`
- **Qt binding issues**
  - Houdini 21 uses PySide6; panel imports PySide6 first and falls back to PySide2.
  - If PySide6 import fails outside Houdini, run inside Houdini Python shell to verify runtime environment.
