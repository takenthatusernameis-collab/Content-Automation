#!/usr/bin/env python3
"""Later expand briefs must name this packet's stall, not a morning scene.

expand.md used to say only "expand the beat by N words". A human following
that line on a short tab-closing draft would still write the first video's
morning reopen. This contract checks a tempfile render. It does not write
expand.md, does not scaffold Q2, and does not call YouTube.
"""

from __future__ import annotations

import hashlib
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from expand_brief import render  # noqa: E402

Q1_EXPAND = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning" / "expand.md"


def fail(failures: list[str], ok: bool, message: str) -> None:
    if not ok:
        failures.append(message)


def main() -> int:
    failures: list[str] = []
    before = hashlib.sha256(Q1_EXPAND.read_bytes()).hexdigest() if Q1_EXPAND.is_file() else ""
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "009-close-the-extra-tab"
        packet.mkdir()
        (packet / "packet.md").write_text(
            "# Packet\n\n- working_title: Close the extra tab before you open the work\n"
            "- format: explainer-6-10min\n",
            encoding="utf-8",
        )
        (packet / "idea.md").write_text(
            "# Idea\n\n"
            "- topic: Close the extra tab before you open the work\n"
            "- problem: the extra tab is still open, so starting the work means checking one more thing\n"
            "- mechanism (the system, not the pep talk): close the extra tab before the work file opens\n",
            encoding="utf-8",
        )
        (packet / "script.md").write_text(
            "# Script\n\n"
            "## Hook\n\nWORDS: Close the extra tab before the file opens.\n\n"
            "## Beat 1 — tab\n\nWORDS: The extra tab is still open.\n\n"
            "## CTA\n\nWORDS: Close that tab first.\n",
            encoding="utf-8",
        )
        text = render(packet)
    low = text.lower()
    fail(failures, "extra tab" in low, "short expand brief must name the tab stall")
    fail(failures, "grow a short beat from this stall" in low, "short expand brief must point at this stall")
    fail(failures, "do not invent a morning reopen" in low, "short expand brief must forbid a morning reopen")
    fail(failures, "reopens the whole list" not in low, "short expand brief copied the first video stall")
    fail(failures, "written default that removes" not in low, "short expand brief invented the first video mechanism")
    after = hashlib.sha256(Q1_EXPAND.read_bytes()).hexdigest() if Q1_EXPAND.is_file() else ""
    fail(failures, before == after, "Q1 expand.md changed")
    if failures:
        print("EXPAND BRIEF CONTRACT FAIL")
        for item in failures:
            print(f"- {item}")
        return 1
    print("EXPAND BRIEF CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
