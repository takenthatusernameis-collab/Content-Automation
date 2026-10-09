#!/usr/bin/env python3
"""Lock chapter titles so a dropped negation cannot invert the beat.

Does not write chapters.md. Does not edit publish.md. Does not touch Q1.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
from chapter_draft import build  # noqa: E402


def fail(msg: str) -> int:
    print("CHAPTER DRAFT CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    q1 = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"
    before = (q1 / "chapters.md").read_bytes() if (q1 / "chapters.md").is_file() else None
    publish_before = (q1 / "publish.md").read_bytes() if (q1 / "publish.md").is_file() else None
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "videos" / "009-chapter-not"
        packet.mkdir(parents=True)
        (packet / "script.md").write_text(
            "## Hook\nWORDS: Do not *reopen* the inbox after you shut the lid.\n"
            "VISUAL: closed laptop\nON SCREEN: FACE DOWN\n\n"
            "## Beat 1 — write the next action\n"
            "WORDS: Write one verb, one object, and one place on the card.\n\n"
            "## CTA\nWORDS: Tonight, write tomorrow's first action on the card.\n",
            encoding="utf-8",
        )
        (packet / "captions.srt").write_text(
            "1\n00:00:00,000 --> 00:00:04,000\nDo not reopen the inbox after you shut the lid.\n\n"
            "2\n00:00:12,000 --> 00:00:18,000\nWrite one verb, one object, and one place on the card.\n\n"
            "3\n00:00:28,000 --> 00:00:34,000\nTonight, write tomorrow's first action on the card.\n\n",
            encoding="utf-8",
        )
        sheet, info = build(packet)
        lines = info.get("lines") or []
        hook = lines[0] if lines else ""
        if "not" not in hook.lower() or "reopen" not in hook.lower():
            return fail(f"negation dropped from hook chapter: {hook}")
        if hook.lower().startswith("0:00 do reopen"):
            return fail(f"chapter inverted the beat: {hook}")
        if "FACE DOWN" in sheet or "ON SCREEN" in sheet:
            return fail("on-screen label leaked into chapter sheet")
        if info.get("approval") is not False:
            return fail("chapter draft must not approve")
    if before is not None and (q1 / "chapters.md").read_bytes() != before:
        return fail("contract rewrote Q1 chapters.md")
    if publish_before is not None and (q1 / "publish.md").read_bytes() != publish_before:
        return fail("contract rewrote Q1 publish.md")
    print("CHAPTER DRAFT CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
