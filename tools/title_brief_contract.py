#!/usr/bin/env python3
"""Later title briefs must not copy the first video's slogans.

Does not write titles.md. Does not rewrite the approved Q1 titles.
Does not call YouTube or GitHub.
"""

from __future__ import annotations

import hashlib
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from title_thumb_brief import candidate_titles, load_packet_inputs, thumb_line  # noqa: E402

Q1 = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning" / "titles.md"
BORROWED = (
    "stop deciding every morning",
    "written default",
    "one default beats a mood",
    "start before the mood",
    "put the cue on the calendar",
)


def _sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    failures: list[str] = []
    before = _sha(Q1) if Q1.is_file() else ""
    if before and "Stop Deciding What to Work on Every Morning" not in Q1.read_text(encoding="utf-8"):
        failures.append("Q1 primary title missing")
    idea = """# Idea

- topic: Clear the inbox before noon
- viewer: someone whose unread mail is the morning
- problem: Three folders stay mixed until the afternoon.
- mechanism (the system, not the pep talk): Sort each new message into reply, file, or delete before opening the next one.
- status: queued
"""
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "009-clear-the-inbox"
        packet.mkdir()
        (packet / "idea.md").write_text(idea, encoding="utf-8")
        src = load_packet_inputs(packet)
        titles = candidate_titles(src)
        line = thumb_line(src)
        blob = " ".join(titles + [line]).lower()
        if len(titles) < 5:
            failures.append(f"need 5 titles from the packet, got {len(titles)}")
        if not any(len(t) < 50 for t in titles):
            failures.append("need one title under 50 characters")
        for borrowed in BORROWED:
            if borrowed in blob:
                failures.append(f"borrowed Q1 slogan: {borrowed}")
        if "inbox" not in blob and "folder" not in blob and "reply" not in blob:
            failures.append(f"fixture title missed the packet: {blob}")
        if "default" in line.lower() or "mood" in line.lower():
            failures.append(f"thumb copied Q1: {line}")
        for title in titles:
            low = title.lower()
            if low.startswith("stop "):
                failures.append(f"stop template without packet verb: {title}")
            if low.startswith("name the "):
                failures.append(f"name template without packet verb: {title}")
            if low.startswith("write the "):
                failures.append(f"write template without packet verb: {title}")
    if Q1.is_file() and _sha(Q1) != before:
        failures.append("Q1 titles.md changed")
    if failures:
        print("TITLE BRIEF CONTRACT FAIL")
        for item in failures:
            print(f"  - {item}")
        return 1
    print("TITLE BRIEF CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
