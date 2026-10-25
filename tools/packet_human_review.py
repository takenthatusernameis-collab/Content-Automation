#!/usr/bin/env python3
"""Print a concise human-review brief for a video packet.

Extracts title, promise, hook/CTA spoken words, description snippet,
open checkboxes, and basic media presence. Reduces recurring labor of
opening multiple packet files before final human review or upload dispatch.
Does not invent content, rewrite files, poll secrets, or call external services.
Exit 0 always; this is informational only.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

try:
    from phrase_utils import spoken_words  # type: ignore
except Exception:
    spoken_words = None  # type: ignore


def section(text: str, heading: str) -> str:
    parts = re.split(rf"^##\s+{re.escape(heading)}\s*$", text, maxsplit=1, flags=re.M)
    if len(parts) < 2:
        return ""
    rest = re.split(r"^##\s+", parts[1], maxsplit=1, flags=re.M)[0]
    return rest.strip()


def first_words(text: str, n: int = 40) -> str:
    if spoken_words is not None:
        cleaned = spoken_words(text)
    else:
        cleaned = re.sub(r"[^\w\s'-]", " ", text)
    words = cleaned.split()
    return " ".join(words[:n]) + ("..." if len(words) > n else "")


def open_boxes(text: str) -> list[str]:
    boxes = []
    for line in text.splitlines():
        if line.strip().startswith("- [ ]"):
            boxes.append(line.strip()[6:].strip())
    return boxes


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print a concise human-review brief for a packet. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("PACKET HUMAN REVIEW BRIEF (informational only; no writes)")
    print(f"Packet: {path.name}")
    print()

    # Title
    titles = path / "titles.md"
    title = "(missing titles.md)"
    if titles.is_file():
        ttext = titles.read_text(encoding="utf-8")
        m = re.search(r"^Primary:[ \t]*([^\n]*)$", ttext, re.M)
        if m:
            title = m.group(1).strip() or title
    print(f"Title: {title}")

    # Promise / idea
    idea = path / "idea.md"
    if idea.is_file():
        itext = idea.read_text(encoding="utf-8")
        topic = re.search(r"^-?\s*topic:[ \t]*([^\n]*)$", itext, re.M | re.I)
        mech = re.search(r"^-?\s*mechanism:[ \t]*([^\n]*)$", itext, re.M | re.I)
        problem = re.search(r"^-?\s*problem:[ \t]*([^\n]*)$", itext, re.M | re.I)
        if topic:
            print(f"Topic: {topic.group(1).strip()}")
        if mech:
            print(f"Mechanism: {mech.group(1).strip()}")
        if problem:
            print(f"Problem: {problem.group(1).strip()}")
    print()

    # Script highlights
    script = path / "script.md"
    if not script.is_file():
        script = path / "draft.md"
    if script.is_file():
        stext = script.read_text(encoding="utf-8")
        hook = section(stext, "Hook") or section(stext, "hook")
        cta = section(stext, "CTA") or section(stext, "cta") or section(stext, "Call to action")
        if hook:
            print(f"Hook (first words): {first_words(hook)}")
        if cta:
            print(f"CTA (first words): {first_words(cta)}")
        words = len((spoken_words(stext) if spoken_words else stext).split())
        print(f"Spoken words (approx): {words}")
    else:
        print("Script: missing script.md / draft.md")
    print()

    # Publish snippet
    publish = path / "publish.md"
    if publish.is_file():
        ptext = publish.read_text(encoding="utf-8")
        desc = section(ptext, "Description")
        if desc:
            print("Description snippet:")
            print(desc[:300] + ("..." if len(desc) > 300 else ""))
            print()
        comment = section(ptext, "First comment (pin candidate)") or section(ptext, "First comment")
        if comment:
            print(f"First comment: {comment.strip()[:200]}")
    else:
        print("Publish: missing publish.md")
    print()

    # Open human boxes
    packet_md = path / "packet.md"
    if packet_md.is_file():
        boxes = open_boxes(packet_md.read_text(encoding="utf-8"))
        if boxes:
            print("Open human checkboxes:")
            for b in boxes:
                print(f"  - {b}")
        else:
            print("Open human checkboxes: none")
    print()

    # Media presence (lightweight)
    vo_ok = any((path / "vo").glob("*.wav")) if (path / "vo").is_dir() else False
    cards_ok = any((path / "cards").glob("*.png")) if (path / "cards").is_dir() else False
    master_ok = (path / "export" / "master.mp4").is_file() or any((path / "exports").glob("*.mp4")) if (path / "exports").is_dir() else False
    print(f"Media: VO={'yes' if vo_ok else 'no'} | Cards={'yes' if cards_ok else 'no'} | Master={'yes' if master_ok else 'no'}")
    print()
    print("This brief is a starting point for human review. It does not approve or upload.")
    print("Run quality/claim/description scans separately if needed. This tool writes nothing.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
