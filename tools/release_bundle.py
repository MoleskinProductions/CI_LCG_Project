#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from datetime import datetime, timezone
from pathlib import Path


def _run(cmd: list[str], cwd: Path) -> tuple[int, str]:
    proc = subprocess.run(cmd, cwd=str(cwd), text=True, capture_output=True)
    out = (proc.stdout or "") + (("\n" + proc.stderr) if proc.stderr else "")
    return proc.returncode, out.strip()


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    report_path = repo / "reports" / "release_bundle.md"
    report_path.parent.mkdir(parents=True, exist_ok=True)
    now = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

    checks = [
        ("CI doctor", ["python", "tools/ci_doctor.py"]),
        ("Precommit smoke", ["bash", "tools/precommit_smoke.sh"]),
        (
            "Probe parity",
            [
                "python",
                "houdini_package/tools/ci_probe_cli.py",
                "--probe-id",
                "P-PRB-006",
                "--chart-mode-id",
                "CHART-003",
                "--seed",
                "1",
            ],
        ),
        ("Suggest parity", ["python", "tools/ci_suggest_cli.py", "--last-n", "5", "--limit", "3"]),
        ("Patch assistant list", ["python", "tools/ci_patch_assistant.py", "--list", "--last-n", "5"]),
    ]

    results = []
    all_pass = True
    for name, cmd in checks:
        code, output = _run(cmd, repo)
        ok = code == 0
        all_pass = all_pass and ok
        results.append((name, cmd, code, output))

    lines = ["# Release Bundle", "", f"- Timestamp: {now}", f"- Status: {'PASS' if all_pass else 'FAIL'}", ""]
    for name, cmd, code, output in results:
        lines.append(f"## {name}")
        lines.append(f"- Command: `{' '.join(cmd)}`")
        lines.append(f"- Exit: `{code}`")
        lines.append("```text")
        if output:
            lines.append(output[:4000])
        else:
            lines.append("(no output)")
        lines.append("```")
        lines.append("")

    report_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote {report_path}")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
