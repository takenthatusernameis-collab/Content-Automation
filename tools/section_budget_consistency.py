#!/usr/bin/env python3
"""Section budget consistency check.

Read-only. Uses phrase_utils.extract_sections + count_spoken_words so word counts
stay identical to the rest of the pipeline. Classifies sections and flags spoken
word counts outside the locked format section bands used by expand_brief:
hook 20-35, payoff 40-70, each beat 140-220, CTA 40-80.
Complements section_pacing_consistency (duration) and structure_order_consistency.
Does not invent media, run ffmpeg, poll secrets, bump status, or write files.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from phrase_utils import extract_sections, count_spoken_words  # noqa: E402

HOOK_BAND = (20, 35)
PAYOFF_BAND = (40, 70)
BEAT_BAND = (140, 220)
CTA_BAND = (40, 80)


def _classify(title: str) -> str:
    t = title.lower().strip()
    if re.match(r"hook\b", t):
        return "hook"
    if re.match(r"payoff\b", t):
        return "payoff"
    if re.match(r"cta\b", t):
        return "cta"
    if re.search(r"beat\s*\d+", t):
        return "beat"
    return "other"


def inspect(packet: Path) -> dict:
    script_path = packet / "script.md"
    if not script_path.is_file():
        return {
            "ok": False,
            "code": "NO_DATA",
            "detail": "missing script.md",
            "sections": [],
            "issues": [],
        }
    script = script_path.read_text(encoding="utf-8")
    sections = extract_sections(script)
    if not sections:
        return {
            "ok": False,
            "code": "NO_DATA",
            "detail": "no sections extracted",
            "sections": [],
            "issues": [],
        }

    issues = []
    report_rows = []
    for sec in sections:
        kind = _classify(sec["title"])
        words = count_spoken_words(sec["spoken"])
        band = None
        if kind == "hook":
            band = HOOK_BAND
        elif kind == "payoff":
            band = PAYOFF_BAND
        elif kind == "beat":
            band = BEAT_BAND
        elif kind == "cta":
            band = CTA_BAND
        in_band = True
        if band and words > 0:
            lo, hi = band
            if not (lo <= words <= hi):
                in_band = False
                issues.append(f"{sec['title']}={words} (want {lo}-{hi})")
        report_rows.append({
            "title": sec["title"],
            "kind": kind,
            "words": words,
            "band": band,
            "in_band": in_band,
        })

    warn = bool(issues)
    return {
        "ok": not warn,
        "code": "WARN" if warn else "OK",
        "detail": "; ".join(issues) if issues else "all classified sections in band",
        "sections": report_rows,
        "issues": issues,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check section spoken-word counts against format budget bands. No writes."
    )
    parser.add_argument("packet", help="Path to packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    rep = inspect(path)
    print(f"packet: {path.name}")
    print(f"consistency: {rep['code']} ({rep['detail']})")
    for row in rep.get("sections") or []:
        band_str = f"{row['band'][0]}-{row['band'][1]}" if row.get("band") else "n/a"
        status = "OK" if row.get("in_band") else "WARN"
        print(f"  {row['title']}: {row['words']} words (band {band_str}) [{status}]")
    print("Does not execute encode, invent media, or poll OAuth.")
    return 0 if rep["code"] != "NO_DATA" else 2


if __name__ == "__main__":
    raise SystemExit(main())
