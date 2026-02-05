#!/usr/bin/env bash
set -euo pipefail

python tools/smoke_test_imports.py
python tools/smoke_test_paths.py
python tools/check_legacy_shims.py
