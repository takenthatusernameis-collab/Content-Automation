#!/usr/bin/env python3
"""Reprint suggested idea.md fields for an existing packet.

Read-only. Does not write idea.md, the queue, or packets.
Recovers the new_packet idea_followup after scaffold stdout is gone.
--block prints only the paste-ready idea.md body. Still does not write.
--check compares current idea.md to the suggested paste. Still does not write.
On PASTE INCOMPLETE, prints the exact --block command for that packet.
On PASTE READY, prints the exact expand_prompt command for that packet,
then the dry-run apply_script line using PATH/draft.md (no --write).
Default reprint prints the exact --check command for that packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from new_packet import idea_followup  # noqa: E402

BLANKISH = frozenset(
    {
        "",
        "template-default",
        "template default",
        "tbd",
        "todo",
        "generic",
        "(blank)",
    }
)


def field(text: str, name: str) -> str:
    pat = rf"^- {re.escape(name)}:[ \t]*(.*)$"
    m = re.search(pat, text, re.M)
    if m:
        return m.group(1).strip()
    if name == "mechanism":
        m = re.search(
            r"^- mechanism \(the system, not the pep talk\):[ \t]*(.*)$",
            text,
            re.M,
        )
        if m:
            return m.group(1).strip()
    return ""


def working_title(path: Path) -> str:
    packet = path / "packet.md"
    if packet.is_file():
        m = re.search(r"^- working_title:[ \t]*(.*)$", packet.read_text(encoding="utf-8"), re.M)
        if m and m.group(1).strip():
            return m.group(1).strip()
    idea = path / "idea.md"
    if idea.is_file():
        t = field(idea.read_text(encoding="utf-8"), "topic")
        if t:
            return t
    return path.name.split("-", 1)[-1].replace("-", " ")


def suggested_values(title: str) -> tuple[str, str, str]:
    """Parse topic / problem / mechanism from idea_followup lines."""
    topic = title
    problem = ""
    mechanism = ""
    for line in idea_followup(title):
        raw = line.strip()
        if raw.startswith("- topic:"):
            topic = raw.split(":", 1)[1].strip()
        elif raw.startswith("- problem:"):
            problem = raw.split(":", 1)[1].strip()
        elif raw.startswith("- mechanism"):
            mechanism = raw.split(":", 1)[1].strip()
    return topic, problem, mechanism


def paste_block(title: str) -> str:
    topic, problem, mechanism = suggested_values(title)
    return (
        "# Idea\n\n"
        f"- topic: {topic}\n"
        f"- problem: {problem}\n"
        f"- mechanism (the system, not the pep talk): {mechanism}\n"
    )


def is_blankish(value: str) -> bool:
    return value.strip().lower() in BLANKISH


def expand_command(packet: Path) -> str:
    return f"python3 tools/expand_prompt.py {packet}"


def draft_path(packet: Path) -> str:
    return f"{packet}/draft.md"


def apply_command(packet: Path) -> str:
    return f"python3 tools/apply_script.py {packet} --from {draft_path(packet)}"


def block_command(packet: Path) -> str:
    return f"python3 tools/idea_brief.py {packet} --block"


def check_command(packet: Path) -> str:
    return f"python3 tools/idea_brief.py {packet} --check"


def check_fields(current: str, title: str, packet: Path) -> tuple[int, list[str]]:
    want_t, want_p, want_m = suggested_values(title)
    got_t = field(current, "topic")
    got_p = field(current, "problem")
    got_m = field(current, "mechanism")
    lines = ["Idea check (does not write idea.md):"]
    mismatches = 0
    for label, got, want in (
        ("topic", got_t, want_t),
        ("problem", got_p, want_p),
        ("mechanism", got_m, want_m),
    ):
        if is_blankish(got):
            lines.append(f"  MISMATCH {label}: current is blank/template; want {want!r}")
            mismatches += 1
        elif got != want:
            lines.append(f"  MISMATCH {label}: current {got!r}; want {want!r}")
            mismatches += 1
        else:
            lines.append(f"  MATCH {label}")
    if mismatches:
        lines.append("PASTE INCOMPLETE. Paste --block into idea.md by hand, then re-run --check.")
        lines.append(f"  {block_command(packet)}")
        lines.append("This command writes nothing.")
        return 2, lines
    lines.append("PASTE READY. Next live command is expand_prompt (off-repo), not this tool.")
    lines.append(f"  {expand_command(packet)}")
    lines.append("Do not treat expand_prompt stdout as script.md.")
    lines.append(f"Save the off-repo draft to {draft_path(packet)} (not script.md).")
    lines.append("After that file exists, dry-run apply_script first:")
    lines.append(f"  {apply_command(packet)}")
    lines.append("This command writes nothing.")
    return 0, lines


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only idea.md reprint. Does not write idea.md."
    )
    parser.add_argument("packet", help="Packet folder")
    group = parser.add_mutually_exclusive_group()
    group.add_argument(
        "--block",
        action="store_true",
        help="Print only the paste-ready idea.md body. Still does not write idea.md.",
    )
    group.add_argument(
        "--check",
        action="store_true",
        help="Compare current idea.md to the suggested paste. Still does not write idea.md.",
    )
    args = parser.parse_args()
    path = Path(args.packet)
    if not path.is_dir():
        print(f"not a packet folder: {path}", file=sys.stderr)
        return 1

    title = working_title(path)
    idea_path = path / "idea.md"
    current = idea_path.read_text(encoding="utf-8") if idea_path.is_file() else ""

    if args.check:
        code, lines = check_fields(current, title, path)
        for line in lines:
            print(line)
        return code

    if args.block:
        print(paste_block(title), end="")
        print("# This command writes nothing. Paste the block above into idea.md by hand.")
        return 0

    print(f"Packet: {path.name}")
    print(f"Title: {title}")
    print("Current idea.md:")
    print(f"  - topic: {field(current, 'topic') or '(blank)'}")
    print(f"  - problem: {field(current, 'problem') or '(blank)'}")
    print(f"  - mechanism: {field(current, 'mechanism') or '(blank)'}")
    print("Suggested paste (does not write idea.md):")
    for line in idea_followup(title):
        print(line)
    print("Paste-ready block (still does not write). Re-run with --block to print only this:")
    print(f"  {block_command(path)}")
    print(paste_block(title), end="")
    print("After paste, confirm without writing:")
    print(f"  {check_command(path)}")
    if "sample-001" in path.name:
        print("Fixture lock: do not treat this packet as the first real video.")
    print("This command writes nothing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
