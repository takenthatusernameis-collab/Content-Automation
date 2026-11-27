#!/usr/bin/env python3
"""Print a structured human-friendly script spot-check list.

Parses an existing script.md (does not rewrite or invent content).
Prints each ## section with title, spoken word count, and soft flags
(short/long section, missing WORDS, total out of band) so a human can scan
faster than reading the raw script. Hard gates remain elsewhere (apply_script,
quality scanners, set_status).
Reduces recurring script draft/final review minutes across future videos.
Does not call YouTube, does not encode, does not write files.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

# Prefer shared helpers when available
try:
    from phrase_utils import extract_sections, count_spoken_words, spoken_words
except ImportError:
    # Minimal fallback so the tool still runs standalone
    import re

    def normalize(text: str) -> str:
        return text.replace("\u2019", "'").replace("\u2018", "'").replace("\u201c", '"').replace("\u201d", '"')

    def extract_sections(text: str) -> list[dict[str, str]]:
        sections: list[dict[str, str]] = []
        parts = re.split(r"^##[ \t]+", text.replace("\r\n", "\n"), flags=re.M)
        for part in parts[1:]:
            lines = part.splitlines()
            if not lines:
                continue
            title = lines[0].strip()
            body = "\n".join(lines[1:])
            words_m = re.search(r"^WORDS:\s*\n(.*?)(?=^VISUAL:|^##|\Z)", body, re.M | re.S)
            spoken = (words_m.group(1).strip() if words_m else body)
            spoken = re.sub(r"\s+", " ", spoken).strip()
            sections.append({"title": title, "spoken": normalize(spoken), "need": ""})
        return sections

    def count_spoken_words(text: str) -> int:
        cleaned = re.sub(r"[^\w\s'-]", " ", normalize(text or ""))
        return len([w for w in cleaned.split() if w.strip()])

    def spoken_words(text: str) -> str:
        return text  # unused in fallback


# Soft thresholds (align roughly with apply_script hook band and overall 900-1500)
SHORT_SECTION = 30
LONG_SECTION = 250
TARGET_BAND = (900, 1500)
HOOK_BAND = (20, 35)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print structured script spot-check list (no invent, no write)."
    )
    parser.add_argument("packet", type=Path, help="Packet folder containing script.md")
    args = parser.parse_args()
    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"Not a directory: {packet}")
        return 1

    path = packet / "script.md"
    if not path.is_file():
        print(f"No script.md in {packet}")
        print("Hard gate remains apply_script.py (dry-run) and quality scanners.")
        return 1

    text = path.read_text(encoding="utf-8", errors="replace")
    sections = extract_sections(text)
    if not sections:
        print("SCRIPT_UNPARSEABLE (no ## sections extracted)")
        return 1

    print("SCRIPT SPOTCHECK ASSISTANT (structured review list; no invent, no write)")
    print(f"Packet: {packet}")
    print(f"Sections: {len(sections)}")
    print("Hard gates remain: apply_script.py dry-run, quality_prep_brief.py, set_status.py")
    print("=" * 70)
    print()

    total_words = 0
    flag_counts = {"short": 0, "long": 0, "missing_words": 0, "hook_band": 0}
    for i, sec in enumerate(sections, 1):
        title = sec["title"]
        spoken = sec["spoken"]
        wc = count_spoken_words(spoken)
        total_words += wc
        flags = []
        if not spoken.strip():
            flags.append("missing_words")
            flag_counts["missing_words"] += 1
        else:
            if wc < SHORT_SECTION:
                flags.append("short")
                flag_counts["short"] += 1
            if wc > LONG_SECTION:
                flags.append("long")
                flag_counts["long"] += 1
            # Soft hook check if title looks like hook
            if title.lower().startswith("hook") and not (HOOK_BAND[0] <= wc <= HOOK_BAND[1]):
                flags.append("hook_band")
                flag_counts["hook_band"] += 1
        flag_str = " [" + ", ".join(flags) + "]" if flags else ""
        print(f"{i:2d}. {title} ({wc} words){flag_str}")
        # Truncated preview of first line of spoken for scannability
        preview = spoken.split(".")[0][:80] if spoken else "(empty)"
        print(f"     {preview}{'...' if len(spoken) > 80 else ''}")
        print()

    in_band = TARGET_BAND[0] <= total_words <= TARGET_BAND[1]
    band_note = "in band" if in_band else f"OUT OF BAND (target {TARGET_BAND[0]}-{TARGET_BAND[1]})"
    print(f"Total spoken words: {total_words}  {band_note}")
    print()
    print("Soft flag summary (human still verifies):")
    print(f"  short (<{SHORT_SECTION} words): {flag_counts['short']}")
    print(f"  long (>{LONG_SECTION} words): {flag_counts['long']}")
    print(f"  missing_words: {flag_counts['missing_words']}")
    print(f"  hook_band (not {HOOK_BAND[0]}-{HOOK_BAND[1]}): {flag_counts['hook_band']}")
    print()
    print("These flags are soft hints only. Run apply_script.py (dry-run) and quality_prep_brief.py for hard/structured signals.")
    print("Spot-check time is reduced by scanning this list instead of raw script.md.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
