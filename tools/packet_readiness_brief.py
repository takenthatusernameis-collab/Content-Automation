#!/usr/bin/env python3
"""Print a structured packet readiness brief.

Inspects the packet folder for presence of key production files and basic
spoken-word band status, then prints a Markdown checklist of pipeline stages
(research, script, assets, captions, chapters, publish, thumbnail, VO, export).
Reduces recurring labor of manually opening multiple files to see what is still
missing before media, QA, or upload planning on every future packet.
Does not invent content, write files, poll secrets, or call external services.
Exit 0 always (informational). Missing files are expected until the stage is done.
Useful early and throughout production to surface the next concrete gap.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import spoken_words  # type: ignore

TARGET_MIN = 900
TARGET_MAX = 1500


def check_file(path: Path, name: str) -> str:
    if (path / name).is_file():
        size = (path / name).stat().st_size
        return f"present ({size} bytes)"
    return "MISSING"


def spoken_status(path: Path) -> str:
    for name in ("script.md", "draft.md"):
        f = path / name
        if f.is_file():
            text = f.read_text(encoding="utf-8")
            spoken = spoken_words(text)
            wc = len(spoken.split()) if spoken.strip() else 0
            if wc == 0:
                return f"{name}: no spoken WORDS detected"
            band = "in band" if TARGET_MIN <= wc <= TARGET_MAX else (
                "below band" if wc < TARGET_MIN else "above band"
            )
            return f"{name}: {wc} spoken words ({band})"
    return "no script.md or draft.md"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print packet readiness brief. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    print("PACKET READINESS BRIEF (informational only; no writes)")
    print(f"Packet: {path.name}")
    print("Checklist of key files and basic script status. Missing items are normal until the stage is complete.")
    print("Do not invent media or secrets. Use individual tools for deeper checks.")
    print()

    stages = [
        ("Idea / topic", "idea.md"),
        ("Research", "research.md"),
        ("Script", "script.md"),
        ("Draft (fallback)", "draft.md"),
        ("Assets plan", "assets.md"),
        ("Publish metadata", "publish.md"),
        ("Titles", "titles.md"),
        ("Thumbnail plan", "thumbnail.md"),
        ("Chapters", "chapters.md"),
        ("Captions (SRT)", "captions.srt"),
        ("Captions notes", "captions.md"),
        ("QA notes", "qa.md"),
        ("Render notes", "render.md"),
        ("VO origin", "vo_origin.md"),
        ("VO session", "vo_session.md"),
    ]

    print("### File presence")
    for label, fname in stages:
        status = check_file(path, fname)
        print(f"- {label}: {status}")

    print()
    print("### Spoken WORDS status")
    print(f"- {spoken_status(path)}")

    print()
    print("### Pipeline stage notes")
    print("- Research: fill sources for any digit/hedge claims (see script_research_gap_brief.py).")
    print("- Script: land in 900–1500 spoken words; run quality_prep_brief.py before promotion.")
    print("- Assets: list the planned cards; card_generator.py can materialize when ready.")
    print("- Captions: captions.srt must pass caption_gate.py before upload.")
    print("- VO: Selected take must be on disk under the packet (not repo-root vo/).")
    print("- Export: master.mp4 with ftyp is required before youtube_upload.py --execute.")
    print("- Upload: blocked on YOUTUBE_* secrets. Do not poll.")
    print()
    print("This brief does not invent content or write files.")
    print("Useful to see the next concrete gap without opening every file on every packet.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
