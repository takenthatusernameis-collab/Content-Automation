#!/usr/bin/env python3
"""End-screen reserve check for CTA spoken duration.

Estimates spoken duration of the CTA section (and total) from script.md or
draft.md. Selects rate from vo_origin.md (190 wpm generated, 140 wpm human)
to match speaking_time_estimate.py. Flags whether the CTA is long enough to
support a readable hold through the final 20 s end-screen reserve required by
docs/format.md.

Prints a short table with status. Reduces recurring manual estimation of
whether the CTA card can stay visible for the YouTube end-screen window.
Does not invent content, rewrite files, or call external services.

Uses shared phrase_utils.extract_sections and count_spoken_words so section
boundaries and word counts stay identical to other duration tools.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))

from phrase_utils import spoken_words, count_spoken_words, extract_sections


HUMAN_WPM = 140
GENERATED_WPM = 190
END_SCREEN_SECONDS = 20
MIN_CTA_SECONDS = 12  # enough for a readable hold into the reserve
MIN_TOTAL_SECONDS = 360  # ~6 min floor from format


def classify(title: str) -> str:
    low = title.lower()
    if low.startswith("hook"):
        return "hook"
    if "payoff" in low:
        return "payoff"
    if low.startswith("cta") or "cta" in low:
        return "cta"
    if low.startswith("beat"):
        return "beat"
    return "other"


def select_rate(path: Path) -> tuple[int, str]:
    """Return (wpm, label) based on vo_origin.md if present."""
    origin_path = path / "vo_origin.md"
    is_generated = False
    if origin_path.is_file():
        origin_text = origin_path.read_text(encoding="utf-8").lower()
        is_generated = "kind: generated" in origin_text or "kind=generated" in origin_text
    if is_generated:
        return GENERATED_WPM, "generated"
    return HUMAN_WPM, "human"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Estimate whether CTA duration supports the 20 s end-screen reserve. No file writes."
    )
    parser.add_argument("packet", help="Packet folder under videos/")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"Not a directory: {path}", file=sys.stderr)
        return 1

    script = path / "script.md"
    draft = path / "draft.md"
    source = script if script.is_file() else draft
    if not source.is_file():
        print(f"No script.md or draft.md in {path}", file=sys.stderr)
        return 1

    text = source.read_text(encoding="utf-8")
    sections = extract_sections(text)

    # Prefer the shared extractor for the official total so it matches
    # quality_scan / claim_scan / words.py conventions.
    total_spoken = spoken_words(text)
    total_words = count_spoken_words(total_spoken)

    cta_words = 0
    for sec in sections:
        if classify(sec["title"]) == "cta":
            cta_words += count_spoken_words(sec["spoken"])

    rate, rate_label = select_rate(path)
    cta_sec = (cta_words / rate) * 60 if cta_words else 0.0
    total_sec = (total_words / rate) * 60 if total_words else 0.0

    print("END-SCREEN RESERVE CHECK (CTA hold vs docs/format.md last 20 s)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print(f"Clock: ~{rate} wpm ({rate_label} default from vo_origin)")
    print()
    print("| Metric | Value | Target | Status |")
    print("|--------|------:|--------|--------|")

    overall = "PASS"
    notes: list[str] = []

    cta_status = "OK" if cta_sec >= MIN_CTA_SECONDS else "SHORT"
    if cta_status != "OK":
        overall = "WARN"
        notes.append(f"CTA spoken ~{cta_sec:.1f}s < {MIN_CTA_SECONDS}s (may not cover readable end-screen hold)")
    print(f"| CTA words | {cta_words} | - | - |")
    print(f"| CTA duration | {cta_sec:.1f}s | ≥{MIN_CTA_SECONDS}s | {cta_status} |")

    total_status = "OK" if total_sec >= MIN_TOTAL_SECONDS else "SHORT"
    if total_status != "OK":
        overall = "WARN"
        notes.append(f"Total estimated {total_sec:.0f}s < {MIN_TOTAL_SECONDS}s floor")
    print(f"| Total words | {total_words} | 900-1500 | - |")
    print(f"| Total duration | {total_sec:.0f}s | ≥{MIN_TOTAL_SECONDS}s | {total_status} |")
    print(f"| End-screen reserve | {END_SCREEN_SECONDS}s | last 20 s | (format rule) |")

    print()
    print(f"Overall: {overall}")
    if notes:
        for n in notes:
            print(f"- {n}")
    else:
        print("- CTA duration appears sufficient for a readable hold through the end-screen reserve.")

    print()
    print("Rule (docs/format.md): CTA card stays readable through the final 20 s end-screen reserve.")
    print("Leave lower-right and lower-left clear. This tool writes nothing.")
    print("Confirm with actual VO duration when a selected take exists.")
    print("Section extraction and word counts use shared phrase_utils helpers.")
    print("Rate selection matches speaking_time_estimate.py (generated vs human).")
    return 0 if overall == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
