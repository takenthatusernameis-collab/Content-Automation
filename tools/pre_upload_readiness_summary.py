#!/usr/bin/env python3
"""One-command pre-upload readiness summary for a packet.

Aggregates key soft quality and structure checks (quality_scan, claim_scan,
title_scan, description_scan, and caption_quality_summary if captions exist)
into a concise view. Soft only. Does not rewrite, invent media, upload, or
poll secrets. Exit 0 always (informational). Reduces human tool-switching
for the recurring pre-upload review step across future videos.
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
        print("Usage: python3 tools/pre_upload_readiness_summary.py <packet>", file=sys.stderr)
        return 1
    packet = sys.argv[1]
    pkt = Path(packet).resolve()
    if not pkt.is_dir():
        print(f"Not a directory: {pkt}", file=sys.stderr)
        return 1

    print("PRE-UPLOAD READINESS SUMMARY (soft checks only; no invent, no upload)")
    print(f"Packet: {pkt.name}")
    print()

    checks = [
        ("quality_scan.py", "Anti-slop / quality"),
        ("claim_scan.py", "Claims / sources"),
        ("title_scan.py", "Title signals"),
        ("description_scan.py", "Description signals"),
    ]

    results = []
    for script, label in checks:
        code, out = run_tool(script, str(pkt))
        results.append((label, code, out))
        print(f"--- {label} ---")
        # Print first 15 lines to keep concise
        lines = out.splitlines()
        print("\n".join(lines[:15]) or "(no output)")
        if len(lines) > 15:
            print(f"... ({len(lines)-15} more lines)")
        print()

    # Caption if present
    captions = pkt / "captions.srt"
    if captions.is_file():
        code, out = run_tool("caption_quality_summary.py", str(pkt))
        print("--- Caption quality (present) ---")
        print(out or "(no output)")
        print()
    else:
        print("--- Caption quality ---")
        print("captions.srt absent (expected until caption_align.py run and spot-check)")
        print()

    # Overall
    has_issues = any(code != 0 for _, code, _ in results)
    print("OVERALL: soft checks completed.")
    if has_issues:
        print("Some tools reported non-zero (review details above; default exits are 0 on clean).")
    else:
        print("No hard signals from these soft scans.")
    print("This is not a gate. Run contracts_suite.py and media_qa.py separately when media exists.")
    print("Do not treat as ready for upload until human review and OAuth path is clear.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
