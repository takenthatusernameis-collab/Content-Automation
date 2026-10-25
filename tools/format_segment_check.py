#!/usr/bin/env python3
"""Early format segment word-band check for script.md or draft.md.

Extracts ## sections, classifies Hook / Payoff / Beat / CTA by title,
counts spoken words (preferring WORDS: blocks), and compares against
channel format bands from docs/format.md and expand_brief.py.
Prints a compact table with per-segment status and overall PASS/WARN.
Reduces recurring manual word-counting against hook 20-35, beat 140-220,
etc., before full validate_packet or expand.md generation on every future packet.
Does not invent content, rewrite files, or call external services.
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

HOOK_BAND = (20, 35)
PAYOFF_BAND = (40, 70)
CTA_BAND = (40, 80)
BEAT_BAND = (140, 220)
TOTAL_BAND = (900, 1500)


def extract_sections(text: str) -> list[dict[str, str]]:
    """Split on ## headings; capture title and spoken body."""
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
    if spoken_words is not None:
        cleaned = spoken_words(text)
        return len(cleaned.split()) if cleaned else 0
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


def band_for(kind: str) -> tuple[int, int] | None:
    return {
        "hook": HOOK_BAND,
        "payoff": PAYOFF_BAND,
        "cta": CTA_BAND,
        "beat": BEAT_BAND,
    }.get(kind)


def status_for(count: int, lo: int, hi: int) -> str:
    if count == 0:
        return "EMPTY"
    if count < lo:
        return "SHORT"
    if count > hi:
        return "LONG"
    return "OK"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check script/draft section word counts against format bands. No file writes."
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

    print("FORMAT SEGMENT CHECK (early word-band vs docs/format.md)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print()
    print("| Section | Kind | Words | Band | Status |")
    print("|---------|------|------:|------|--------|")

    total_words = 0
    overall = "PASS"
    notes: list[str] = []
    for sec in sections:
        kind = classify(sec["title"])
        wc = count_words(sec["spoken"])
        total_words += wc
        band = band_for(kind)
        if band:
            lo, hi = band
            st = status_for(wc, lo, hi)
            band_str = f"{lo}-{hi}"
            if st != "OK":
                overall = "WARN"
                notes.append(f"{sec['title'][:30]} ({kind}): {st} ({wc} words)")
        else:
            st = "n/a"
            band_str = "-"
        print(f"| {sec['title'][:40]} | {kind} | {wc} | {band_str} | {st} |")

    print()
    print(f"Total spoken words: {total_words}")
    lo, hi = TOTAL_BAND
    total_st = status_for(total_words, lo, hi)
    print(f"Total band: {lo}-{hi} → {total_st}")
    if total_st != "OK":
        overall = "WARN"
        notes.append(f"Total words {total_st} ({total_words})")

    print()
    print(f"Overall: {overall}")
    if notes:
        for n in notes:
            print(f"- {n}")
    else:
        print("- All classified sections in band.")

    print()
    print("Bands from docs/format.md + expand_brief.py (hook 20-35, payoff 40-70, beat 140-220, CTA 40-80).")
    print("This tool writes nothing. Run expand_brief.py for a full budget table or validate_packet.py for the gate.")
    return 0 if overall == "PASS" else 2


if __name__ == "__main__":
    sys.exit(main())
