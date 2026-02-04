#!/usr/bin/env python3
import argparse
import json
import sys
from pathlib import Path


def _bootstrap_path() -> None:
    pkg_python = Path(__file__).resolve().parents[1] / "python"
    if str(pkg_python) not in sys.path:
        sys.path.insert(0, str(pkg_python))


def main() -> int:
    _bootstrap_path()
    from ci.runner import run_probe, DEFAULT_PROBE_ID

    parser = argparse.ArgumentParser(description="Run CI probe stub and write schema-valid artifacts.")
    parser.add_argument("--probe-id", default=DEFAULT_PROBE_ID)
    parser.add_argument("--chart-mode-id", default=None)
    parser.add_argument("--output-dir", default=None)
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument(
        "--inputs-json",
        default=None,
        help="Optional JSON object string passed to runner inputs (e.g. '{\"edge_id\":\"E000024\"}').",
    )
    parser.add_argument("--json", action="store_true", help="Print full result JSON")
    args = parser.parse_args()

    inputs = {}
    if args.inputs_json:
        inputs = json.loads(args.inputs_json)

    result = run_probe(
        probe_id=args.probe_id,
        chart_mode_id=args.chart_mode_id,
        inputs=inputs,
        output_dir=args.output_dir,
        stub_mode=True,
        seed=args.seed,
    )

    msg = f"{result['pass_fail']} seam_count={result['seam_count']} probe_output={result['probe_output_path']}"
    print(msg)
    if args.json:
        print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
