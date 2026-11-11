#!/usr/bin/env python3
"""One-command metadata metrics summary for a packet.

Aggregates soft metrics suggestions from title, thumbnail, description,
and tags tools into a concise view. Soft only. Does not rewrite, invent
media, upload, or poll secrets. Exit 0 always (informational). Reduces
human tool-switching for the recurring metadata polishing step across
future videos.
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
        print("Usage: python3 tools/metadata_metrics_summary.py <packet>", file=sys.stderr)
        return 1
    packet = sys.argv[1]
    pkt = Path(packet).resolve()
    if not pkt.is_dir():
        print(f"Not a directory: {pkt}", file=sys.stderr)
        return 1

    print("METADATA METRICS SUMMARY (soft suggestions only; no invent, no upload)")
    print(f"Packet: {pkt.name}")
    print()

    checks = [
        ("title_metrics_suggest.py", "Title metrics"),
        ("thumbnail_metrics_suggest.py", "Thumbnail metrics"),
        ("description_metrics_suggest.py", "Description metrics"),
        ("tags_metrics_suggest.py", "Tags metrics"),
    ]

    for script, label in checks:
        code, out = run_tool(script, str(pkt))
        print(f"--- {label} ---")
        # Print first 20 lines to keep concise
        lines = out.splitlines()
        print("\n".join(lines[:20]) or "(no output)")
        if len(lines) > 20:
            print(f"... ({len(lines)-20} more lines)")
        print()

    print("OVERALL: soft metrics suggestions completed.")
    print("Use as signals only; preserve channel voice and anti-slop rules.")
    print("This is not a gate. Run individual scans or pre_upload_readiness_summary.py as needed.")
    print("Do not treat as ready for upload until human review and OAuth path is clear.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
