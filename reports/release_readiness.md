# Release Readiness
Date: 2026-02-05

## Gates
- [x] Imports smoke: `python tools/smoke_test_imports.py`
- [x] Pathing smoke: `python tools/smoke_test_paths.py`
- [x] Legacy shim sanity: `python tools/check_legacy_shims.py`
- [x] Panel import smoke: `python tools/smoke_test_panel_import.py`
- [x] Headless parity: probe + suggest chain runs (`ci_probe_cli.py`, `ci_suggest_cli.py`)
- [x] Patch verify gate active in `tools/ci_patch_assistant.py` (blocks `--apply` on FAIL unless `--force`)

## Canonical Sources
- Houdini package file: `houdini_package/package.json`
- Python panel implementation: `houdini_package/python/ci_panels/CI_GraphOverlay_panel.py`
- Panel definition: `houdini_package/houdini/python_panels/CI_GraphOverlay.pypanel`

## Compatibility (temporary)
- Legacy package: `houdini_package/ci_package.json` (deprecated)
- Legacy panel shim: `houdini_package/ui/CI_GraphOverlay_panel.py` (forwarder only)
- Planned removal window: on/after 2026-03-31 after stability verification.
