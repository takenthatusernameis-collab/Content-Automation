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

--queue ID prints the same paste-ready body from docs/topic_queue.md
without requiring a videos/ folder. Still does not write idea.md.
--check cannot be used with --queue (there is no idea.md to compare).

Run 089: paste_block includes viewer / why now / related so a hand paste
fills the whole idea.md template, not only topic / problem / mechanism.
--check still gates those three locked fields only.
Run 095: --queue ID unlocks the paste before scaffold.
Run 415: an unmatched packet with a filled problem still pasted the channel morning line.
Suggested paste now uses that packet's problem when the queue has no row.
Run 398: the default reprint used to print the shared morning why-now line
even after --block and --queue used why_now_line. Suggested paste names this row's viewer and stall. Install stays off unless the row says it.
the same row-specific line. A blank problem still falls back to WHY_NOW.
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
from queue_lib import parse_queue  # noqa: E402

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

# Channel lock from docs/channel.md. Hard-coded so a blank or planning packet still pastes.
# A later topic must not inherit the planning-stall viewer unless it already says planning.
VIEWER = (
    "People who already plan their week, then stall when it is time to start."
)
WHY_NOW = (
    "The week is already planned, but the morning still reopens the whole list."
)
RELATED = "none published yet"
QUEUE = ROOT / "docs" / "topic_queue.md"


def field(text: str, name: str) -> str:
    # Dash bullets are the writer format. A pasted "Topic:" line is the same field.
    pat = rf"^-?\s*{re.escape(name)}:[ \t]*(.*)$"
    m = re.search(pat, text, re.M | re.I)
    if m and m.group(1).strip():
        return m.group(1).strip()
    if name == "mechanism":
        m = re.search(
            r"^-?\s*mechanism \(the system, not the pep talk\):[ \t]*(.*)$",
            text,
            re.M | re.I,
        )
        if m and m.group(1).strip():
            return m.group(1).strip()
    return ""


def working_title(path: Path) -> str:
    packet = path / "packet.md"
    if packet.is_file():
        m = re.search(r"^-?\s*working_title:[ \t]*(.*)$", packet.read_text(encoding="utf-8"), re.M | re.I)
        if m and m.group(1).strip():
            return m.group(1).strip()
    idea = path / "idea.md"
    if idea.is_file():
        t = field(idea.read_text(encoding="utf-8"), "topic")
        if t:
            return t
    return path.name.split("-", 1)[-1].replace("-", " ")


def queue_row(qid: str) -> dict[str, str] | None:
    if not QUEUE.is_file():
        return None
    want = qid.strip().upper()
    for row in parse_queue(QUEUE.read_text(encoding="utf-8")):
        if row.get("id", "").upper() == want:
            return row
    return None


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


def viewer_line(topic: str, problem: str) -> str:
    """Name the viewer from this row. Planning-stall audience stays only when the row says planning."""
    blob = f"{topic} {problem}".lower()
    if (
        "planning" in blob
        or "after planning" in blob
        or "every morning" in blob
        or "reopen the whole work list" in blob
    ):
        return VIEWER
    stall = problem.strip().rstrip(".")
    if not stall or stall.startswith("("):
        stall = topic.strip().rstrip(".")
    short = " ".join(stall.split()[:12])
    return f"Someone who wants focused work but stalls on this: {short}"


def usable_field(value: str) -> bool:
    """A real packet field. Placeholders and blanks are not a stall."""
    cleaned = value.strip()
    return bool(cleaned) and not cleaned.startswith("(")


def grounded_fields(title: str, current: str) -> tuple[str, str, str]:
    """Prefer this packet when the queue has no row.

    A pasted card with a problem must not be told to use the channel morning line.
    Queue matches still win. This does not write idea.md.
    """
    topic, problem, mechanism = suggested_values(title)
    cur_t = field(current, "topic")
    cur_p = field(current, "problem")
    cur_m = field(current, "mechanism")
    if usable_field(cur_t):
        topic = cur_t
    if not usable_field(problem) and usable_field(cur_p):
        problem = cur_p
    if not usable_field(mechanism) and usable_field(cur_m):
        mechanism = cur_m
    return topic, problem, mechanism


def rewrite_followup(lines: list[str], problem: str, mechanism: str) -> list[str]:
    """Replace queue placeholders with this packet's fields. Does not write idea.md."""
    out = []
    for line in lines:
        if line.startswith("  - problem:") and usable_field(problem) and "(no matching" in line:
            out.append(f"  - problem: {problem}")
        elif line.startswith("  - mechanism") and usable_field(mechanism) and "(no matching" in line:
            out.append(f"  - mechanism (the system, not the pep talk): {mechanism}")
        else:
            out.append(line)
    return out


def why_now_line(problem: str, mechanism: str = "") -> str:
    """This row's stall. A blank problem keeps the channel line.

    "Install" stays only when this row already says install or default.
    A later card must not be told to install a stall it did not name.
    This does not write idea.md and does not create a packet.
    """
    cleaned = problem.strip().rstrip(".")
    if not cleaned or cleaned.startswith("("):
        return WHY_NOW
    blob = f"{problem} {mechanism}".lower()
    if "install" in blob or "default" in blob:
        return f"The week is already planned. The stall to install is this: {cleaned}."
    return f"The stall in this packet is this: {cleaned}."


def paste_block(title: str, problem: str | None = None, mechanism: str | None = None, topic: str | None = None) -> str:
    got_t, got_p, got_m = suggested_values(title)
    if topic and usable_field(topic):
        got_t = topic
    if problem is not None and usable_field(problem):
        got_p = problem
    if mechanism is not None and usable_field(mechanism):
        got_m = mechanism
    topic, problem, mechanism = got_t, got_p, got_m
    return (
        "# Idea\n\n"
        f"- topic: {topic}\n"
        f"- viewer: {viewer_line(topic, problem)}\n"
        f"- problem: {problem}\n"
        f"- mechanism (the system, not the pep talk): {mechanism}\n"
        f"- why now: {why_now_line(problem, mechanism)}\n"
        f"- related videos to avoid repeating: {RELATED}\n"
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
    got_v = field(current, "viewer")
    got_w = field(current, "why now")
    got_r = field(current, "related videos to avoid repeating")
    if is_blankish(got_v) or is_blankish(got_w) or is_blankish(got_r):
        lines.append("  INFO extra template fields still blank; --block now includes viewer / why now / related.")
        lines.append("  INFO those extras are not a --check gate.")
    if mismatches:
        lines.append("PASTE INCOMPLETE. Fill a blank idea.md with apply_idea.py PACKET --write, then re-run --check. Do not paste by hand.")
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


def print_queue_block(qid: str) -> int:
    row = queue_row(qid)
    if row is None:
        print(f"no topic_queue row: {qid}", file=sys.stderr)
        print("This command writes nothing.")
        return 2
    title = row["working_title"]
    print(paste_block(title), end="")
    print(f"# Queue {row['id']} status={row['status']}. This command writes nothing.")
    print("# After the packet folder exists, fill a blank idea.md with apply_idea.py PACKET --write. This reprint writes nothing.")
    print("# Do not treat this reprint as scaffold or as script.md.")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only idea.md reprint. Does not write idea.md."
    )
    parser.add_argument("packet", nargs="?", help="Packet folder")
    parser.add_argument(
        "--queue",
        metavar="ID",
        help="Print paste-ready idea.md from a topic_queue id. No folder required. Still does not write.",
    )
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

    if args.queue:
        if args.check:
            print("--check needs a packet folder; --queue only reprints the paste.", file=sys.stderr)
            print("This command writes nothing.")
            return 2
        return print_queue_block(args.queue)

    if not args.packet:
        print("packet folder required unless --queue ID is set", file=sys.stderr)
        return 1

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
        topic, problem, mechanism = grounded_fields(title, current)
        print(paste_block(title, problem, mechanism, topic), end="")
        print("# This command writes nothing. Fill a blank idea.md with apply_idea.py PACKET --write. Do not paste by hand.")
        return 0

    print(f"Packet: {path.name}")
    print(f"Title: {title}")
    print("Current idea.md:")
    print(f"  - topic: {field(current, 'topic') or '(blank)'}")
    print(f"  - viewer: {field(current, 'viewer') or '(blank)'}")
    print(f"  - problem: {field(current, 'problem') or '(blank)'}")
    print(f"  - mechanism: {field(current, 'mechanism') or '(blank)'}")
    print(f"  - why now: {field(current, 'why now') or '(blank)'}")
    print(
        "  - related videos to avoid repeating: "
        f"{field(current, 'related videos to avoid repeating') or '(blank)'}"
    )
    print("Suggested paste (does not write idea.md):")
    topic, problem, mechanism = grounded_fields(title, current)
    for line in rewrite_followup(idea_followup(title), problem, mechanism):
        print(line)
    print(f"  - viewer: {viewer_line(topic, problem)}")
    print(f"  - why now: {why_now_line(problem, mechanism)}")
    print(f"  - related videos to avoid repeating: {RELATED}")
    print("Paste-ready block (still does not write). Re-run with --block to print only this:")
    print(f"  {block_command(path)}")
    print(paste_block(title, problem, mechanism, topic), end="")
    print("After paste, confirm without writing:")
    print(f"  {check_command(path)}")
    if "sample-001" in path.name:
        print("Fixture lock: do not treat this packet as the first real video.")
    print("This command writes nothing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
