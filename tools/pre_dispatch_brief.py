#!/usr/bin/env python3
"""Print a concise pre-dispatch readiness brief for a packet.

Extracts title, mechanism, whether mechanism tokens appear in early Hook and CTA,
open checkboxes in publish.md, basic media file presence flags, and the next human action.
No file writes, no invented content, no secret polling. Exit 0 always; informational only.
Reduces recurring labor of opening multiple packet files and running several tools
before the human performs the OAuth step and dispatches execute=true.
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


def extract_field(text: str, key: str) -> str:
    m = re.search(rf"^-?\s*{re.escape(key)}:\s*(.+)$", text, re.M | re.I)
    return m.group(1).strip() if m else ""


def section(text: str, heading: str) -> str:
    parts = re.split(rf"^##\s+{re.escape(heading)}\s*$", text, maxsplit=1, flags=re.M)
    if len(parts) < 2:
        return ""
    rest = re.split(r"^##\s+", parts[1], maxsplit=1, flags=re.M)[0]
    return rest.strip()


def first_spoken(text: str, n: int = 40) -> str:
    if spoken_words is not None:
        cleaned = spoken_words(text)
    else:
        cleaned = re.sub(r"[^\w\s'-]", " ", text)
    return " ".join(cleaned.split()[:n]).lower()


def mechanism_tokens(mech: str) -> list[str]:
    stop = {"the", "a", "an", "of", "to", "and", "or", "for", "in", "on", "with", "that", "this"}
    words = re.findall(r"\b\w{4,}\b", mech.lower())
    return [w for w in words if w not in stop][:5]


def open_boxes(text: str) -> list[str]:
    # Unchecked markdown checkboxes
    return re.findall(r"^- \[ \]\s*(.+)$", text, re.M)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Concise pre-dispatch readiness brief. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("PRE-DISPATCH BRIEF (informational only; no writes)")
    print(f"Packet: {path.name}")
    print()

    # Title
    titles = path / "titles.md"
    title = ""
    if titles.is_file():
        title = extract_field(titles.read_text(encoding="utf-8"), "title") or extract_field(titles.read_text(encoding="utf-8"), "primary")
    print(f"Title: {title or '(missing)'}")

    # Mechanism
    idea = path / "idea.md"
    mechanism = ""
    if idea.is_file():
        mechanism = extract_field(idea.read_text(encoding="utf-8"), "mechanism")
    print(f"Mechanism: {mechanism or '(missing)'}")

    # Mechanism presence
    script = path / "script.md"
    if not script.is_file():
        script = path / "draft.md"
    hook_ok = cta_ok = False
    if script.is_file() and mechanism:
        stext = script.read_text(encoding="utf-8")
        hook = section(stext, "Hook") or section(stext, "hook")
        cta = section(stext, "CTA") or section(stext, "cta") or section(stext, "Call to action")
        tokens = mechanism_tokens(mechanism)
        hook_text = first_spoken(hook) if hook else ""
        cta_text = first_spoken(cta, 60) if cta else ""
        hook_ok = any(tok in hook_text for tok in tokens)
        cta_ok = any(tok in cta_text for tok in tokens)
    print(f"Mechanism in early Hook: {'yes' if hook_ok else 'no'}")
    print(f"Mechanism in CTA: {'yes' if cta_ok else 'no'}")

    # Open boxes
    publish = path / "publish.md"
    boxes = []
    if publish.is_file():
        boxes = open_boxes(publish.read_text(encoding="utf-8"))
    print(f"Open checkboxes in publish.md: {len(boxes)}")
    for b in boxes[:3]:
        print(f"  - {b[:80]}")
    if len(boxes) > 3:
        print(f"  ... and {len(boxes)-3} more")

    # Media flags (presence only; no content inspection)
    vo = any((path / "vo").glob("*-take-selected.wav")) or any((path / "vo").glob("*-take-selected.flac"))
    cards = any((path / "cards").glob("*.png"))
    export = (path / "export" / "master.mp4").is_file()
    thumb = (path / "thumbnail.png").is_file()
    print(f"Selected VO present: {'yes' if vo else 'no'}")
    print(f"Cards present: {'yes' if cards else 'no'}")
    print(f"Export master present: {'yes' if export else 'no'}")
    print(f"Thumbnail present: {'yes' if thumb else 'no'}")

    print()
    print("Next human action: complete OAuth secrets (see docs/human_oauth_checklist.md) then dispatch execute=true once.")
    print("Do not dispatch until a private video id appears in upload_state.json.")
    print()
    print("This tool writes nothing and invents no content.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
