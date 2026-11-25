#!/usr/bin/env python3
"""Estimate remaining human labor minutes for a packet.

Inspects packet status, key file presence, and simple structural signals
to produce a rough remaining-minutes table. Reduces recurring labor of
manually guessing how much work is left before upload on every future packet.
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

WPM = 150
TARGET_MIN_WORDS = 900
TARGET_MAX_WORDS = 1500


def count_words(text: str) -> int:
    if spoken_words is not None:
        cleaned = spoken_words(text)
        return len(cleaned.split()) if cleaned else 0
    cleaned = re.sub(r"[^\w\s'-]", " ", text)
    return len([w for w in cleaned.split() if w.strip()])


def script_word_count(packet: Path) -> int:
    for name in ("script.md", "draft.md"):
        p = packet / name
        if p.is_file():
            return count_words(p.read_text(encoding="utf-8"))
    return 0


def file_present(packet: Path, rel: str) -> bool:
    p = packet / rel
    return p.is_file() and p.stat().st_size > 0


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Estimate remaining human labor minutes from packet state. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    status = "unknown"
    packet_md = path / "packet.md"
    if packet_md.is_file():
        text = packet_md.read_text(encoding="utf-8")
        m = re.search(r"status:\s*(\S+)", text)
        if m:
            status = m.group(1).strip()

    words = script_word_count(path)
    in_band = TARGET_MIN_WORDS <= words <= TARGET_MAX_WORDS

    vo_present = any(
        file_present(path, f"vo/{path.name}-take-selected.{ext}")
        for ext in ("wav", "flac")
    ) or any(
        file_present(path, f"vo/{path.name}-take-selected-v2.{ext}")
        for ext in ("wav", "flac")
    )

    cards_dir = path / "cards"
    cards_present = cards_dir.is_dir() and any(cards_dir.glob("*.png"))

    timeline_present = file_present(path, "timeline.md")
    export_present = any(
        (path / "exports").glob("*.mp4") if (path / "exports").is_dir() else []
    )
    publish_ready = file_present(path, "publish.md")

    print("LABOR ESTIMATE (remaining human minutes; informational only)")
    print(f"Packet: {path.name}")
    print(f"Status: {status}")
    print(f"Spoken words: {words} ({'in band' if in_band else 'outside 900-1500'})")
    print()
    print("| Step | Present | Est. min | Notes |")
    print("|------|---------|---------:|-------|")

    steps = [
        ("Script in band", in_band, 0 if in_band else 20, "expand or cut to 900-1500"),
        ("Selected VO", vo_present, 0 if vo_present else 30, "record or materialize labeled generated"),
        ("Cards on disk", cards_present, 0 if cards_present else 10, "card_generator or materialize"),
        ("Timeline", timeline_present, 0 if timeline_present else 5, "timeline.py --write"),
        ("Master export", export_present, 0 if export_present else 15, "assemble after media_qa PASS"),
        ("Publish metadata", publish_ready, 0 if publish_ready else 10, "publish_brief or manual"),
        ("Upload", False, 5, "blocked on OAuth secrets; dispatch after"),
    ]

    total = 0
    for name, present, mins, note in steps:
        total += mins
        present_str = "yes" if present else "no"
        print(f"| {name} | {present_str} | {mins} | {note} |")

    print()
    print(f"Estimated remaining human minutes: {total}")
    print("This is a rough planning number only. Actual time varies.")
    print("Upload step stays blocked until the three GitHub Actions secrets exist.")
    print("This tool writes nothing.")

    # Suggested next local step (reduces decision time on every packet)
    next_step = "All local steps present; proceed to OAuth dispatch when ready."
    next_cmd = "python3 tools/oauth_complete_guide.py  # human only"
    if not in_band:
        next_step = "Bring script into 900-1500 spoken-word band."
        next_cmd = f"python3 tools/script_expander.py {path.name}  # or edit script.md then re-check"
    elif not vo_present:
        next_step = "Obtain Selected VO (record or materialize authorized generated)."
        next_cmd = "python3 tools/materialize_q1_release.py  # if Q1; else record to vo/"
    elif not cards_present:
        next_step = "Generate or materialize cards."
        next_cmd = f"python3 tools/card_generator.py {path}  # or materialize"
    elif not timeline_present:
        next_step = "Build timeline."
        next_cmd = f"python3 tools/timeline.py {path} --write"
    elif not export_present:
        next_step = "Assemble master after media_qa PASS."
        next_cmd = f"python3 tools/media_qa.py {path} && python3 tools/assemble.py {path}"
    elif not publish_ready:
        next_step = "Prepare publish metadata."
        next_cmd = f"python3 tools/publish_brief.py {path}"

    print()
    print("## SUGGESTED NEXT LOCAL STEP")
    print(f"  {next_step}")
    print(f"  Recommended command: {next_cmd}")
    print("  (informational; still review labor map and priority_review_summary for high-signal issues)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
