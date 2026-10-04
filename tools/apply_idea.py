#!/usr/bin/env python3
"""Fill idea.md from the locked queue paste. Does not write spoken WORDS.

Dry-run default. --write replaces idea.md only when the file is still the
blank template or already equal to the paste. A different non-blank idea.md
is refused and left unchanged. Does not create a packet folder. Does not
scaffold. Does not mark the topic queue used.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
sys.path.insert(0, str(TOOLS))

from idea_brief import paste_block  # noqa: E402
from new_packet import idea_followup  # noqa: E402

FIELDS = (
    "topic",
    "viewer",
    "problem",
    "mechanism (the system, not the pep talk)",
    "why now",
    "related videos to avoid repeating",
)


def packet_dir(raw: str) -> Path:
    path = Path(raw)
    if not path.is_absolute():
        path = ROOT / path
    return path


def is_blank_template(text: str) -> bool:
    if not text.startswith("# Idea"):
        return False
    for name in FIELDS:
        needle = f"- {name}:"
        if needle not in text:
            return False
        for line in text.splitlines():
            if line.startswith(needle):
                if line.split(":", 1)[1].strip():
                    return False
    return True


def refuse_reason(packet: Path, title: str) -> str:
    if not packet.is_dir():
        return "packet folder missing; this command does not scaffold"
    if "sample-001" in packet.name:
        return "fixture packet refused"
    idea = packet / "idea.md"
    if not idea.is_file():
        return "idea.md missing; this command does not create a packet"
    follow = "\n".join(idea_followup(title))
    if "write one before expand" in follow or "(no locked problem" in follow:
        return "problem line is not locked; do not write idea.md"
    if "(no matching queue" in follow:
        return "no matching queue row; do not write idea.md"
    return ""


def main() -> int:
    parser = argparse.ArgumentParser(description="Fill idea.md from the queue paste. Dry-run default.")
    parser.add_argument("packet", help="Existing packet folder")
    parser.add_argument("--title", default="", help="Working title. Defaults to packet.md or folder slug.")
    parser.add_argument("--write", action="store_true", help="Write idea.md when blank or already equal")
    args = parser.parse_args()

    packet = packet_dir(args.packet)
    title = args.title.strip()
    if not title:
        packet_md = packet / "packet.md"
        if packet_md.is_file():
            for line in packet_md.read_text(encoding="utf-8").splitlines():
                if line.startswith("- working_title:"):
                    title = line.split(":", 1)[1].strip()
                    break
        if not title:
            title = packet.name.split("-", 1)[-1].replace("-", " ")

    reason = refuse_reason(packet, title)
    if reason:
        print(f"APPLY IDEA REFUSED: {reason}")
        print("This command does not write spoken WORDS and does not scaffold.")
        return 2

    paste = paste_block(title)
    if not paste.endswith("\n"):
        paste += "\n"
    idea = packet / "idea.md"
    current = idea.read_text(encoding="utf-8")
    if not current.endswith("\n"):
        current += "\n"
    same = current == paste
    blank = is_blank_template(current)
    print("APPLY IDEA")
    print(f"packet: {packet}")
    print("writes spoken WORDS: no")
    print("scaffolds: no")
    if same:
        print("status: already_pasted")
    elif blank:
        print("status: blank_template")
    else:
        print("status: different_nonblank")
        print("APPLY IDEA REFUSED: idea.md is not the blank template and does not match the paste")
        print("This command does not overwrite a reviewed idea.md.")
        return 2
    if not args.write:
        print("dry-run: idea.md unchanged")
        print(paste, end="")
        return 0
    idea.write_text(paste, encoding="utf-8")
    print("wrote: idea.md")
    return 0


if __name__ == "__main__":
    sys.exit(main())
