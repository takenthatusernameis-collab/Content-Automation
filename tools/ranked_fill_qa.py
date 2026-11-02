#!/usr/bin/env python3
"""Post-fill QA brief for ranked publish metadata.

After recommended_publish_fill.py has written ranked sections, this tool:
1. Extracts each field via shared phrase_utils extractors (the ones fixed in Run 964).
2. Reports presence and word-count against the fill writer's ideal ranges.
3. Aggregates the existing no-write scanners (title_scan, thumbnail_scan,
   description_scan, end_screen_scan, first_comment_scan) that operate on
   publish.md or related files.

Prints one glanceable brief. Does not rewrite files, invent text, or call
external services. Compounds ranking into a single review step that reduces
recurring human labor of separate checks on every future packet.
Hits remain revision signals only. Default exit 0.
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from phrase_utils import (
    extract_recommended_title,
    extract_recommended_description,
    extract_recommended_thumbnail,
    extract_recommended_end_screen,
    extract_recommended_first_comment,
    count_spoken_words,
)

# Ideal word ranges match the extractors' acceptance windows in phrase_utils.py
FIELD_BOUNDS = {
    "Title": (3, 20),
    "Description": (10, 120),
    "Thumbnail text": (1, 10),
    "End screen": (4, 15),
    "First comment": (4, 80),
}

SCANNERS = [
    ("TITLE SCAN", "title_scan.py"),
    ("THUMBNAIL SCAN", "thumbnail_scan.py"),
    ("DESCRIPTION SCAN", "description_scan.py"),
    ("END SCREEN SCAN", "end_screen_scan.py"),
    ("FIRST COMMENT SCAN", "first_comment_scan.py"),
]


def run_tool(script: str, packet: str) -> tuple[int, str]:
    path = TOOLS / script
    if not path.is_file():
        return 1, f"MISSING {script}"
    try:
        proc = subprocess.run(
            [sys.executable, str(path), packet],
            capture_output=True,
            text=True,
            check=False,
        )
        out = (proc.stdout or "") + (proc.stderr or "")
        return proc.returncode, out.strip()
    except Exception as e:
        return 1, f"EXCEPTION running {script}: {e}"


def ranked_fields(fill_text: str) -> dict[str, str | None]:
    return {
        "Title": extract_recommended_title(fill_text),
        "Description": extract_recommended_description(fill_text),
        "Thumbnail text": extract_recommended_thumbnail(fill_text),
        "End screen": extract_recommended_end_screen(fill_text),
        "First comment": extract_recommended_first_comment(fill_text),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print post-fill ranked metadata QA brief. No file writes."
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"Not a directory: {packet}", file=sys.stderr)
        return 1

    print("RANKED FILL QA BRIEF (presence, length, and scanner signals)")
    print("Uses shared extractors from phrase_utils (Run 964). Hits are revision signals only.")
    print("Does not invent text or rewrite files. Run after recommended_publish_fill.py.")
    print("=" * 72)
    print()

    fill_path = packet / "recommended_publish_fill.md"
    if not fill_path.is_file():
        print("No recommended_publish_fill.md present.")
        print("Generate options then run: python3 tools/recommended_publish_fill.py <packet>")
        print("Then re-run this tool.")
        return 0

    fill_text = fill_path.read_text(encoding="utf-8")
    fields = ranked_fields(fill_text)

    print("## RANKED FIELD PRESENCE AND LENGTH")
    print("-" * 40)
    any_ranked = False
    for label, text in fields.items():
        lo, hi = FIELD_BOUNDS[label]
        if text is None:
            print(f"{label}: MISSING (extractor returned None)")
            continue
        any_ranked = True
        wc = count_spoken_words(text)
        status = "OK" if lo <= wc <= hi else f"OUT_OF_RANGE (expected {lo}-{hi})"
        preview = text if len(text) <= 90 else text[:87] + "..."
        print(f"{label}: {status} ({wc} words) [{preview}]")
    if not any_ranked:
        print("(no ranked sections extracted; check options files and re-run fill)")
    print()

    print("## EXISTING SCANNER RESULTS")
    print("-" * 40)
    any_scanner = False
    for title, script in SCANNERS:
        print(f"### {title}")
        rc, output = run_tool(script, str(packet))
        if output and "MISSING" not in output:
            any_scanner = True
            print(output)
        else:
            print(output or f"(no useful output from {script}; may need publish.md)")
        print()

    print("=" * 72)
    print("Next: revise options or ranked fill if MISSING / OUT_OF_RANGE / hits remain, then re-run.")
    print("Copy preferred sections into publish.md only after clear signals.")
    print("Preferred unblocked path remains the human OAuth step for actual publish.")
    if not any_ranked and not any_scanner:
        print("No ranked fields and no scanner output. Ensure options and fill exist.")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
