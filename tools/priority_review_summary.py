#!/usr/bin/env python3
"""Single-command priority review summary across key QA tools.

Runs quality_scan.py, originality_report.py, caption_quality_summary.py,
and metadata_qa_report.py for a packet (or default videos/* for quality_scan),
then extracts and prints only their PRIORITY / high-signal sections.

Does not rewrite files, invent content/media, upload, or call network.
Soft only. Compounds by giving humans one focused entry point instead of
multiple sequential reports. Exit 0 always (individual tools may signal issues).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"


def run_tool(script: str, args: list[str]) -> tuple[int, str]:
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    cmd = [sys.executable, str(path)] + args
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False)
        out = (proc.stdout or "").strip()
        if proc.stderr:
            out += "\n" + proc.stderr.strip()
        return proc.returncode, out
    except Exception as exc:
        return 1, f"EXCEPTION {script}: {exc}"


def extract_priority_block(output: str) -> list[str]:
    """Pull lines from a PRIORITY section or high-signal header."""
    lines = []
    in_priority = False
    for line in output.splitlines():
        stripped = line.strip()
        if "--- Priority review" in line or "PRIORITY:" in line.upper() or "high-signal" in line.lower():
            in_priority = True
            if stripped and not stripped.startswith("---"):
                lines.append(stripped)
            continue
        if in_priority:
            if stripped.startswith("---") or stripped.startswith("=") or (not stripped and lines):
                break
            if stripped:
                lines.append(stripped)
    return lines[:8]


def main() -> int:
    packet = sys.argv[1] if len(sys.argv) > 1 else None
    print("PRIORITY REVIEW SUMMARY (high-signal issues only; for focused human spot-check)")
    print("Aggregates: quality_scan, originality_report, caption_quality_summary, metadata_qa_report")
    print("Does not rewrite, invent, or upload. Review signals only.")
    print("=" * 72)

    # 1. Quality scan (anti-slop)
    q_args = [packet] if packet else []
    _, q_out = run_tool("quality_scan.py", q_args)
    q_pri = extract_priority_block(q_out)
    print("\n## SCRIPT ANTI-SLOP (quality_scan)")
    if q_pri:
        for line in q_pri:
            print(f"  {line}")
    else:
        print("  (no high-signal priority hits or clear)")

    # 2. Originality (requires packet)
    if packet:
        _, o_out = run_tool("originality_report.py", [packet])
        o_pri = extract_priority_block(o_out)
        print("\n## SCRIPT ORIGINALITY")
        if o_pri:
            for line in o_pri:
                print(f"  {line}")
        else:
            print("  (no high-signal priority signals or clear)")
    else:
        print("\n## SCRIPT ORIGINALITY")
        print("  (skipped: provide packet path for originality_report)")

    # 3. Captions
    if packet:
        _, c_out = run_tool("caption_quality_summary.py", [packet])
        c_pri = extract_priority_block(c_out)
        print("\n## CAPTIONS")
        if c_pri:
            for line in c_pri:
                print(f"  {line}")
        else:
            print("  (no high-signal priority cues or absent)")
    else:
        print("\n## CAPTIONS")
        print("  (skipped: provide packet path)")

    # 4. Metadata
    if packet:
        _, m_out = run_tool("metadata_qa_report.py", [packet])
        m_pri = extract_priority_block(m_out)
        print("\n## METADATA")
        if m_pri:
            for line in m_pri:
                print(f"  {line}")
        else:
            print("  (no high-signal priority issues or clear)")
    else:
        print("\n## METADATA")
        print("  (skipped: provide packet path)")

    print("\n" + "=" * 72)
    print("PRIORITY REVIEW SUMMARY DONE.")
    print("Focus on the lines above first. Re-run individual tools for full context.")
    print("Do not treat any of this as a hard gate or upload approval.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
