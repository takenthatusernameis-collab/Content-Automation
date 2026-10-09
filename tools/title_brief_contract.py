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

from title_thumb_brief import candidate_titles, contrast_line, load_packet_inputs, thumb_line  # noqa: E402

Q1 = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning" / "titles.md"
Q1_THUMB = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning" / "thumbnail.md"
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
        short = """# Idea

- topic: Inbox
- viewer: someone who leaves mail mixed
- problem: Unread mail piles up.
- mechanism (the system, not the pep talk): Inbox.
- status: queued
"""
        short_packet = Path(tmp) / "010-inbox-only"
        short_packet.mkdir()
        (short_packet / "idea.md").write_text(short, encoding="utf-8")
        short_line = thumb_line(load_packet_inputs(short_packet))
        if short_line.lower() != "inbox":
            failures.append(f"one-word mechanism renamed: {short_line}")
        if "name the step" in short_line.lower():
            failures.append(f"thumb stamped Name The Step: {short_line}")
        thin = candidate_titles(load_packet_inputs(short_packet))
        joined = " | ".join(thin).lower()
        if any(" step " in f" {item.lower()} " for item in thin):
            failures.append(f"thin packet invented step N: {joined}")
        if len(thin) != len({item.lower() for item in thin}):
            failures.append(f"thin packet repeated a title: {joined}")
        if "the default" in joined or "this step" in joined:
            failures.append(f"thin packet used a filler mechanism: {joined}")
        contrast = contrast_line(src)
        if "planning clutter" in contrast.lower() or "empty panel" in contrast.lower():
            failures.append(f"contrast copied Q1 visual: {contrast}")
        if "folder" not in contrast.lower() and "message" not in contrast.lower() and "reply" not in contrast.lower():
            failures.append(f"contrast missed the packet: {contrast}")
        plain = Path(tmp) / "004-close-the-extra-tab"
        plain.mkdir()
        (plain / "idea.md").write_text(
            "Topic: Close the extra tab\nProblem: A second tab stays open\nMechanism: close the extra tab before the next click\n",
            encoding="utf-8",
        )
        plain_src = load_packet_inputs(plain)
        if plain_src["topic"].lower().startswith("004"):
            failures.append(f"plain Topic line used the folder id: {plain_src['topic']}")
        if "close the extra tab" not in plain_src["topic"].lower():
            failures.append(f"plain Topic line missed the idea: {plain_src['topic']}")

        empty = Path(tmp) / "011-empty-working-title"
        empty.mkdir()
        (empty / "idea.md").write_text(
            "Topic: Put the start cue on the work itself\n"
            "Problem: the planned task has no visible start cue\n"
            "Mechanism: Name one physical cue on the work\n",
            encoding="utf-8",
        )
        (empty / "packet.md").write_text(
            "# Packet\n- status: draft\n- working_title:\n## Promise\nOne sentence: Name one physical cue.\n",
            encoding="utf-8",
        )
        empty_src = load_packet_inputs(empty)
        if empty_src["working"].lower() in {"", "promise", "## promise"} or "promise" == empty_src["topic"].lower():
            if empty_src["topic"].lower() != "put the start cue on the work itself":
                failures.append(f"empty working_title swallowed the heading: {empty_src}")
        if "promise" in empty_src["working"].lower() or empty_src["working"].startswith("#"):
            failures.append(f"empty working_title captured the next heading: {empty_src['working']}")
        if "start cue" not in empty_src["working"].lower():
            failures.append(f"empty working_title did not fall back to the topic: {empty_src['working']}")
        empty_titles = candidate_titles(empty_src)
        if not empty_titles or empty_titles[0].lower() == "promise":
            failures.append(f"primary became the next heading: {empty_titles[:2]}")

        long = {
            "topic": "Keep the checklist where the stall happens",
            "problem": "the constraint lives away from the stall, so the delay has nothing to hit",
            "mechanism": "Put the constraint on the desk, file, or app that already absorbs the delay",
            "viewer": "Someone who wants focused work but stalls on this checklist",
            "working": "Keep the checklist where the stall happens",
        }
        long_titles = candidate_titles(long)
        if not long_titles:
            failures.append("long clause produced no titles")
        for title in long_titles:
            last = title.split()[-1].lower().strip(".,;:")
            if last in {"to", "the", "so", "from", "a", "of", "before", "after", "into"}:
                failures.append(f"title ended on a dangling word: {title}")
        phone = {
            "topic": "Silence the phone before the first block",
            "problem": "the phone is still face up, so the first block starts as a notification check",
            "mechanism": "Face the phone down in another room before the first two minutes",
            "viewer": "People who already closed the extra tab, then stall when a notification lands",
            "working": "Silence the phone before the first block",
        }
        phone_titles = candidate_titles(phone)
        if not phone_titles:
            failures.append("phone packet produced no titles")
        for title in phone_titles:
            last = title.split()[-1].lower().strip(".,;:")
            if last in {"before", "after", "into", "to", "the", "so"}:
                failures.append(f"phone title ended on a dangling word: {title}")
            if "morning" in title.lower() and "phone" not in title.lower():
                failures.append(f"phone title borrowed the morning line: {title}")
        phone_thumb = thumb_line(phone)
        phone_last = phone_thumb.split()[-1].lower().strip(".,;:") if phone_thumb else ""
        if phone_last in {"before", "after", "into"}:
            failures.append(f"phone thumb ended on a dangling word: {phone_thumb}")
        charger = {
            "topic": "Park the charger across the room",
            "problem": "The charger stays within arm's reach.",
            "mechanism": "Leave the charger in the kitchen before the block.",
            "viewer": "someone who charges the phone on the desk",
            "working": "Park the charger across the room",
        }
        charger_thumb = thumb_line(charger)
        if not charger_thumb:
            failures.append("charger packet produced no thumb line")
        else:
            last = charger_thumb.split()[-1].lower().strip(".,;:")
            if last in {"before", "after", "into"}:
                failures.append(f"charger thumb ended on a dangling word: {charger_thumb}")
            if "charger" not in charger_thumb.lower():
                failures.append(f"charger thumb missed the packet: {charger_thumb}")

        negate = {
            "topic": "Do not reopen the inbox",
            "problem": "Do not reopen the inbox until the block ends",
            "mechanism": "Leave the lid down without a second look",
            "viewer": "someone who reopens mail mid-block",
            "working": "Do not reopen the inbox",
        }
        negate_titles = candidate_titles(negate)
        negate_blob = " ".join(negate_titles).lower()
        if "do reopen" in negate_blob:
            failures.append(f"negation flipped in titles: {negate_titles}")
        if not any("not" in title.lower().split() for title in negate_titles):
            failures.append(f"negation dropped from titles: {negate_titles}")
        negate_thumb = thumb_line(negate)
        negate_last = negate_thumb.split()[-1].lower().strip(".,;:") if negate_thumb else ""
        if negate_last in {"before", "after", "into", "so", "without", "until", "because"}:
            failures.append(f"inbox thumb ended on a dangling word: {negate_thumb}")
        plain_titles = " ".join(candidate_titles(plain_src)).lower()
        if plain_titles.startswith("004") or " 004 " in f" {plain_titles} ":
            failures.append(f"plain Topic titles include the folder id: {plain_titles}")
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
    thumb_before = _sha(Q1_THUMB) if Q1_THUMB.is_file() else ""
    if Q1_THUMB.is_file():
        thumb = Q1_THUMB.read_text(encoding="utf-8")
        if "calm empty panel vs leftover planning clutter" not in thumb:
            failures.append("Q1 thumbnail contrast missing")
        if _sha(Q1_THUMB) != thumb_before:
            failures.append("Q1 thumbnail.md changed")
    if failures:
        print("TITLE BRIEF CONTRACT FAIL")
        for item in failures:
            print(f"  - {item}")
        return 1
    print("TITLE BRIEF CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
