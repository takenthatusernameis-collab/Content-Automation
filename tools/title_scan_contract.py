#!/usr/bin/env python3
"""Lock the title shout scan. Does not touch the live Q1 packet."""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOL = ROOT / "tools" / "title_scan.py"


def fail(msg: str) -> int:
    print("TITLE SCAN CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    if not TOOL.is_file():
        return fail("title_scan.py missing")
    sys.path.insert(0, str(ROOT / "tools"))
    from set_status import check
    from title_scan import scan_path

    q1 = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"
    titles_before = (q1 / "titles.md").read_bytes()
    thumb_before = (q1 / "thumbnail.md").read_bytes()
    q1_hits = scan_path(q1)
    if q1_hits:
        return fail(f"Q1 was not clear: {q1_hits}")
    if (q1 / "titles.md").read_bytes() != titles_before or (q1 / "thumbnail.md").read_bytes() != thumb_before:
        return fail("scanner rewrote Q1")

    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "videos" / "009-contract"
        packet.mkdir(parents=True)
        (packet / "packet.md").write_text(
            "- id: contract\n- working_title: contract\n- status: draft\n",
            encoding="utf-8",
        )
        (packet / "titles.md").write_text(
            "# Titles\n\nPrimary: STOP GRINDING Every Morning\nAlts:\n1. Build a Default Not a Mood\n",
            encoding="utf-8",
        )
        (packet / "thumbnail.md").write_text(
            "# Thumbnail\n\nOn-image text (max 5 words): One Written Default\nMatches title: No\n",
            encoding="utf-8",
        )
        blocked = check(packet, "ready_for_vo")
        if not any("title_scan hits" in item and "GRINDING" in item for item in blocked):
            return fail(f"set_status did not refuse shouted title: {blocked}")
        if not any("title_scan hits" in item and "thumb:No" in item for item in blocked):
            return fail(f"set_status did not refuse thumbnail mismatch: {blocked}")
        (packet / "titles.md").write_text(
            "# Titles\n\nPrimary: Stop Deciding Every Morning\nAlts:\n1. Build a Default Not a Mood\n2. Use One API Default\n",
            encoding="utf-8",
        )
        (packet / "thumbnail.md").write_text(
            "# Thumbnail\n\nOn-image text (max 5 words): One Written Default\nMatches title: Yes\n",
            encoding="utf-8",
        )
        if scan_path(packet):
            return fail(f"acronym title was not clear: {scan_path(packet)}")
        (packet / "titles.md").write_text(
            "# Titles\n\nPrimary: STOP GRINDING Every Morning\nAlts:\n1. Build a Default\n",
            encoding="utf-8",
        )
        shouted = scan_path(packet)
        if not any(kind == "shout" and "STOP" in detail for kind, detail in shouted):
            return fail(f"two shouted words were clear: {shouted}")
        if "STOP GRINDING" not in (packet / "titles.md").read_text(encoding="utf-8"):
            return fail("contract rewrote titles.md")

    proc = subprocess.run(
        [sys.executable, str(TOOL), str(q1)],
        cwd=ROOT,
        text=True,
        capture_output=True,
    )
    if proc.returncode != 0 or "clear" not in proc.stdout:
        return fail(proc.stdout + proc.stderr)
    print("TITLE SCAN CONTRACT PASS")
    return 0


if __name__ == "__main__":
    sys.exit(main())
