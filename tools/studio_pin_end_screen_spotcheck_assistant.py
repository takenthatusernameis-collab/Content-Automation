#!/usr/bin/env python3
"""Print a structured human-friendly Studio pin / end-screen spot-check list.

Parses existing publish.md (or recommended_publish_fill.md / script.md fallback) for End screen / CTA text.
Prints presence, length, word count, and soft flags (empty, short/long, weak/engagement-bait patterns).
Reminds of the remaining manual YouTube Studio clicks (pin comment, end-screen elements, last-20s rule).
Does not invent content, rewrite files, or call YouTube. Hard gates remain elsewhere (end_screen_scan, publish locks).
Reduces recurring Studio pin / end-screen review minutes across future videos.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import END_SCREEN_WEAK_PATTERNS, normalize, compile_word_boundary_patterns  # noqa: E402

END_RE = re.compile(r"## (?:End screen|End Screen|CTA|Call to action|Final CTA)\s*\n(.*?)(?=\n## |\Z)", re.S | re.I)
_WEAK_RES = compile_word_boundary_patterns(END_SCREEN_WEAK_PATTERNS)


def extract_end_screen(text: str) -> str:
    m = END_RE.search(text.replace("\r\n", "\n"))
    return normalize(m.group(1).strip()) if m else ""


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print structured Studio pin / end-screen spot-check list (no invent, no write)."
    )
    parser.add_argument("packet", type=Path, help="Packet folder")
    args = parser.parse_args()
    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"Not a directory: {packet}")
        return 1

    sources = []
    end_text = ""
    source_name = ""

    # Prefer publish.md
    pub = packet / "publish.md"
    if pub.is_file():
        end_text = extract_end_screen(pub.read_text(encoding="utf-8", errors="replace"))
        if end_text:
            sources.append("publish.md")
            source_name = "publish.md"

    # Fallback to recommended_publish_fill.md
    if not end_text:
        fill = packet / "recommended_publish_fill.md"
        if fill.is_file():
            end_text = extract_end_screen(fill.read_text(encoding="utf-8", errors="replace"))
            if end_text:
                sources.append("recommended_publish_fill.md")
                source_name = "recommended_publish_fill.md"

    # Last resort: last spoken section of script.md if it looks like CTA
    if not end_text:
        script = packet / "script.md"
        if script.is_file():
            # Simple last-section grab; full extract lives in other tools
            text = script.read_text(encoding="utf-8", errors="replace")
            parts = re.split(r"^##[ \t]+", text, flags=re.M)
            if len(parts) > 1:
                last = parts[-1].strip()
                if "cta" in last.lower() or "call to action" in last.lower() or "close" in last.lower():
                    end_text = normalize(last)
                    sources.append("script.md (last section)")
                    source_name = "script.md"

    print("STUDIO PIN / END-SCREEN SPOTCHECK ASSISTANT (structured review list; no invent, no write)")
    print(f"Packet: {packet}")
    print(f"Source: {source_name or '(none found)'}")
    print("Hard gates remain: end_screen_scan.py, publish locks, youtube_upload dry-run.")
    print("=" * 70)
    print()

    flags = []
    if not end_text:
        print("End-screen / CTA text: (missing)")
        flags.append("missing_end_screen")
    else:
        words = len(end_text.split())
        chars = len(end_text)
        print(f"End-screen / CTA ({words} words, {chars} chars):")
        print(f"  {end_text[:200]}{'...' if len(end_text) > 200 else ''}")
        if words < 4:
            flags.append("end_screen_too_short")
        if words > 20:
            flags.append("end_screen_too_long")
        if "(add" in end_text.lower() or end_text.lower() in ("cta", "end screen", "tbd", "todo"):
            flags.append("placeholder")
        for phrase, cre in zip(END_SCREEN_WEAK_PATTERNS, _WEAK_RES):
            if cre.search(end_text):
                flags.append(f"weak_pattern:{phrase}")

    print()
    if flags:
        print("Soft flags (human still verifies):")
        for f in flags:
            print(f"  - {f}")
    else:
        print("No soft flags raised.")
    print()
    print("Manual Studio steps still required after upload (Data API cannot finish these):")
    print("  - Pin the first comment (from first_comment or recommended fill).")
    print("  - Add end-screen elements in last 20s: subscribe button, video, or playlist.")
    print("  - Confirm CTA text stays in the safe center zone (see end_screen_preview.png if generated).")
    print("  - Do not place critical text in lower-left / lower-right reserved zones.")
    print()
    print("These flags are soft hints only. Review against channel voice and last-20s rule.")
    print("Spot-check time is reduced by scanning this list instead of raw publish.md + Studio UI.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
