#!/usr/bin/env python3
"""End-screen reserve check for CTA spoken duration.

Estimates spoken duration of the CTA section (and total) from script.md or
draft.md at the documented ~150 wpm clock. Flags whether the CTA is long
enough to support a readable hold through the final 20 s end-screen reserve
required by docs/format.md.

Prints a short table with status. Reduces recurring manual estimation of
whether the CTA card can stay visible for the YouTube end-screen window.
Does not invent content, rewrite files, or call external services.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))


WPM = 150
END_SCREEN_SECONDS = 20
MIN_CTA_SECONDS = 12  # enough for a readable hold into the reserve
MIN_TOTAL_SECONDS = 360  # ~6 min floor from format


def extract_sections(text: str) -> list[dict[str, str]]:
    sections: list[dict[str, str]] = []
    parts = re.split(r"^##[ \t]+", text, flags=re.M)
    for part in parts[1:]:
        lines = part.splitlines()
        if not lines:
            continue
        title = lines[0].strip()
        body = "\n".join(lines[1:])
        words_m = re.search(r"^WORDS:\s*\n(.*?)(?=^VISUAL:|^##|\Z)", body, re.M | re.S)
        spoken = (words_m.group(1).strip() if words_m else body)
        spoken = re.sub(r"\s+", " ", spoken).strip()
        sections.append({"title": title, "spoken": spoken})
    return sections


def count_words(text: str) -> int:
    """Count words in already-extracted spoken section text.

    The caller (extract_sections) has already pulled the body after WORDS:.
    Do not re-apply spoken_words, which expects a full document containing WORDS: blocks.
    """
    cleaned = re.sub(r"[^\w\s'-]", " ", text)
    return len([w for w in cleaned.split() if w.strip()])


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

    cta_words = 0
    total_words = 0
    for sec in sections:
        wc = count_words(sec["spoken"])
        total_words += wc
        if classify(sec["title"]) == "cta":
            cta_words += wc

    cta_sec = (cta_words / WPM) * 60 if cta_words else 0.0
    total_sec = (total_words / WPM) * 60 if total_words else 0.0

    print("END-SCREEN RESERVE CHECK (CTA hold vs docs/format.md last 20 s)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print(f"Clock: ~{WPM} wpm")
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
    return 0 if overall == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
