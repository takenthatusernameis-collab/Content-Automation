#!/usr/bin/env python3
"""One-command full pre-upload summary for a packet.

Combines media QA (when media is present), key quality scans, and metadata
metrics into a concise overview. Soft only. Does not rewrite, invent media,
upload, or poll secrets. Exit 0 always (informational). Reduces human and
future-agent tool-switching for the recurring final review step before the
OAuth/publish gate on any packet.

Designed to be run after materialize_q1_release.py (or when media is already
on disk). Complements status_report.py, next_action.py, quality_prep_brief.py,
and metadata_metrics_summary.py without replacing them.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"


def run_tool(script: str, packet: str, extra: list[str] | None = None) -> tuple[int, str]:
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    cmd = [sys.executable, str(path), packet]
    if extra:
        cmd.extend(extra)
    try:
        proc = subprocess.run(
            cmd,
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
        print("Usage: python3 tools/full_pre_upload_summary.py <packet>", file=sys.stderr)
        return 1
    packet = sys.argv[1]
    pkt = Path(packet).resolve()
    if not pkt.is_dir():
        print(f"Not a directory: {pkt}", file=sys.stderr)
        return 1

    print("FULL PRE-UPLOAD SUMMARY (soft + media checks; no invent, no upload, no poll)")
    print(f"Packet: {pkt.name}")
    print()

    # Media QA if present
    vo_dir = pkt / "vo"
    cards_dir = pkt / "cards"
    export = pkt / "export" / "master.mp4"
    media_present = vo_dir.is_dir() and any(vo_dir.iterdir()) and cards_dir.is_dir() and export.is_file()
    if media_present:
        print("--- Media QA ---")
        code, out = run_tool("media_qa.py", str(pkt))
        lines = out.splitlines()
        # Print gate line and a few PASSes
        for line in lines:
            if "gate:" in line or line.startswith("- PASS") or line.startswith("- FAIL"):
                print(line)
        if code != 0:
            print(f"(media_qa exit {code})")
        print()
    else:
        print("--- Media QA ---")
        print("Media not fully present (vo/ + cards/ + export/master.mp4).")
        print("Run: python3 tools/materialize_q1_release.py  (for Q1) then re-run this summary.")
        print()

    # Quality brief (limited output)
    print("--- Quality / structure brief (first 25 lines) ---")
    code, out = run_tool("quality_prep_brief.py", str(pkt))
    lines = out.splitlines()
    print("\n".join(lines[:25]) or "(no output)")
    if len(lines) > 25:
        print(f"... ({len(lines)-25} more lines; run quality_prep_brief.py for full)")
    print()

    # Metadata summary (limited)
    print("--- Metadata metrics (first 30 lines) ---")
    code, out = run_tool("metadata_metrics_summary.py", str(pkt))
    lines = out.splitlines()
    print("\n".join(lines[:30]) or "(no output)")
    if len(lines) > 30:
        print(f"... ({len(lines)-30} more lines)")
    print()

    print("OVERALL: soft pre-upload summary completed.")
    print("Media gate and quality/metadata signals are revision aids only.")
    print("OAuth secrets remain the hard publish gate. Prefer human OAuth step next.")
    print("Do not treat this as authorization to upload or scaffold Q2.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
