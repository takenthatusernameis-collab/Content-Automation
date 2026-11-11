#!/usr/bin/env python3
"""One-command caption quality summary for human spot-check.

Aggregates caption_speed_report.py, caption_timeline_consistency.py, and caption_gate.py
into a concise view. Soft only. Does not rewrite, upload, or invent media.
Exit 0 if tools are present and packet has captions.srt (or reports absence).
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"


def run_tool(script: str, packet: str) -> tuple[int, str]:
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    try:
        proc = subprocess.run(
            [sys.executable, str(path), packet],
            capture_output=True,
            text=True,
            check=False,
        )
        out = (proc.stdout or "").strip() + ("\n" + proc.stderr.strip() if proc.stderr else "")
        return proc.returncode, out
    except Exception as exc:
        return 1, f"EXCEPTION {script}: {exc}"


def main() -> int:
    if len(sys.argv) < 2:
        print("Usage: python3 tools/caption_quality_summary.py <packet>", file=sys.stderr)
        return 1
    packet = sys.argv[1]
    print("CAPTION QUALITY SUMMARY (for human spot-check; draft only)")
    print(f"Packet: {packet}")
    print()
    code1, out1 = run_tool("caption_speed_report.py", packet)
    print("--- Speed / readability ---")
    print(out1 or "(no output)")
    print()
    code2, out2 = run_tool("caption_timeline_consistency.py", packet)
    print("--- Timeline consistency ---")
    print(out2 or "(no output)")
    print()
    code3, out3 = run_tool("caption_gate.py", packet)
    print("--- Gate (empty/overlap/reversed/line length/past wav) ---")
    print(out3 or "(no output)")
    print()
    codes = [code1, code2, code3]
    if all(c == 0 for c in codes):
        print("SUMMARY: all reports available and gate PASS. Review flagged cues before any upload.")
    elif any(c == 2 for c in codes):  # absent
        print("SUMMARY: captions.srt absent (expected for draft until aligned).")
    else:
        print("SUMMARY: one or more reports incomplete or gate issues. Check individual tools.")
    print("Do not treat captions.srt as approved for upload until human spot-check.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
