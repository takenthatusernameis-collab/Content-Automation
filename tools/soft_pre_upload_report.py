#!/usr/bin/env python3
"""One-command soft pre-upload report for a packet.

Aggregates the soft limit and format match tools (title length, tags length,
description length, thumbnail size/bytes/format, VO duration) into a single
summary. Surfaces any hard-limit risks or soft guidelines that a human should
glance at before the OAuth step. Does not change hard gates, invent text or
media, rewrite files, poll secrets, encode, or upload. Reduces sequential
command labor for future packets. Reusable.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
DEFAULT_PACKET = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"

SOFT_TOOLS = [
    ("title_length_match.py", "TITLE LENGTH"),
    ("tags_length_match.py", "TAGS LENGTH"),
    ("description_length_match.py", "DESCRIPTION LENGTH"),
    ("thumbnail_size_match.py", "THUMBNAIL SIZE"),
    ("thumbnail_bytes_match.py", "THUMBNAIL BYTES"),
    ("thumbnail_format_match.py", "THUMBNAIL FORMAT"),
    ("vo_duration_match.py", "VO DURATION"),
]


def run_tool(script: str, packet: Path) -> tuple[int, str]:
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    cmd = [sys.executable, str(path), str(packet)]
    try:
        proc = subprocess.run(cmd, capture_output=True, text=True, check=False, timeout=30)
        out = ((proc.stdout or "") + ("\n" + proc.stderr if proc.stderr else "")).strip()
        return proc.returncode, out
    except Exception as e:
        return 1, f"EXCEPTION {script}: {e}"


def main() -> int:
    packet = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PACKET
    if not packet.is_dir():
        print(f"soft_pre_upload_report: packet dir missing ({packet})")
        return 1

    print("SOFT PRE-UPLOAD REPORT (aggregated soft limits; gates unchanged)")
    print(f"packet: {packet.name}")
    print("Signals are advisory only. Hard gates live in pre_upload_qa_suite / media_qa / etc.")
    print("=" * 72)
    print()

    notes = []
    for script, label in SOFT_TOOLS:
        code, out = run_tool(script, packet)
        print(f"## {label}")
        print(out or "(no output)")
        print()
        low = out.lower()
        if any(k in low for k in ("exceeded", "hard limit: exceeded", "size match: no", "under", "too brief", "may truncate")):
            notes.append(label)

    print("=" * 72)
    if notes:
        print(f"ADVISORY NOTES: {', '.join(notes)} (review before dispatch; soft only)")
    else:
        print("ADVISORY NOTES: none (all soft checks within limits/guidelines)")
    print()
    print("Next: python3 tools/human_one_pager.py or docs/human_oauth_checklist.md")
    print("Do not poll secrets. Do not invent media. SOFT PRE-UPLOAD REPORT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
