#!/usr/bin/env python3
"""Suggest qualitative or direct replacements for quality_scan and claim_scan hits.

Reads script.md WORDS. Does not rewrite any file. Prints context + a short suggested
rewrite for each high-precision hit so future agents and humans spend less time
inventing neutral phrasing. A suggestion is a starting point, not a final sentence.
Uses the same word-boundary patterns as the scanners.

Run 709: also surfaces unsourced digit claims from claim_scan (when sources do not cite them).
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

# Reuse the exact pattern lists by importing the scanners
try:
    from quality_scan import PATTERNS as QUALITY_PATTERNS
    from claim_scan import HEDGES as CLAIM_HEDGES, scan_path as claim_scan_path
except ImportError:
    QUALITY_PATTERNS = ()
    CLAIM_HEDGES = ()
    def claim_scan_path(p): return []

WORD_RE = re.compile(r"WORDS:\s*(.*?)(?:\nVISUAL:|\n## |\Z)", re.S)

def spoken(text: str) -> str:
    parts = WORD_RE.findall(text.replace("\r\n", "\n"))
    return "\n".join(part.strip() for part in parts)

def context_around(body: str, match: re.Match) -> str:
    start = max(0, match.start() - 50)
    end = min(len(body), match.end() + 50)
    ctx = body[start:end].replace("\n", " ").strip()
    if len(ctx) > 120:
        ctx = ctx[:117] + "..."
    return ctx

def suggest_for_quality(phrase: str, ctx: str) -> str:
    """Return a short qualitative replacement direction."""
    low = phrase.lower()
    if any(x in low for x in ("dive in", "without further", "let's", "let’s")):
        return "Delete the opener. Start with the concrete action or mechanism."
    if any(x in low for x in ("key is", "secret", "truth is", "bottom line", "point is")):
        return "Replace with the specific next action or distinction the viewer can use."
    if any(x in low for x in ("in fact", "of course", "obviously", "clearly", "simply")):
        return "Remove the filler. State the observation directly."
    if "subscribe" in low or "like" in low:
        return "Move any CTA to the end screen or first comment. Keep spoken WORDS free of it."
    if any(x in low for x in ("here's what you need to know", "let me break it down", "long and short")):
        return "Delete the transition. State the concrete observation or mechanism immediately."
    return f"Replace '{phrase}' with a direct statement of the mechanism or observed fact."

def suggest_for_claim(phrase: str, ctx: str) -> str:
    """Return a short qualitative or citation direction for hedges."""
    return f"Either cite the exact source for '{phrase}' in research.md / sources.md, or rewrite the sentence as a qualitative observation without the hedge (e.g. 'some people report' or a concrete example)."

def suggest_for_digit(token: str, ctx: str) -> str:
    """Return a short qualitative direction for an unsourced number."""
    return f"Either cite the exact source and number '{token}' in research.md / sources.md, or rewrite the claim qualitatively (e.g. 'many people', 'a large share', 'often', or a concrete non-numeric example). Do not invent a source."

def scan_and_suggest(path: Path) -> list[tuple[str, str, str, str]]:
    """Return list of (kind, phrase, context, suggestion)."""
    script = path / "script.md"
    if not script.is_file():
        return []
    text = script.read_text(encoding="utf-8")
    body = spoken(text)
    results = []

    # Quality
    for phrase in QUALITY_PATTERNS:
        cre = re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE)
        for m in cre.finditer(body):
            ctx = context_around(body, m)
            sug = suggest_for_quality(phrase, ctx)
            results.append(("quality", phrase, ctx, sug))
            break  # first match per phrase

    # Claim hedges
    for phrase in CLAIM_HEDGES:
        cre = re.compile(r"\b" + re.escape(phrase) + r"\b", re.IGNORECASE)
        for m in cre.finditer(body):
            ctx = context_around(body, m)
            sug = suggest_for_claim(phrase, ctx)
            results.append(("claim", phrase, ctx, sug))
            break

    # Unsourced digits (reuse claim_scan which already checks sources)
    try:
        claim_hits = claim_scan_path(path)
        for kind, token, ctx in claim_hits:
            if kind == "digit":
                sug = suggest_for_digit(token, ctx)
                results.append(("digit", token, ctx, sug))
    except Exception:
        pass  # fail open if claim_scan import or sources logic changes

    return results

def main() -> int:
    parser = argparse.ArgumentParser(description="Suggest rewrites for quality and claim hits.")
    parser.add_argument("packet", nargs="?", help="Packet folder. Default: every videos/* with script.md")
    args = parser.parse_args()
    if args.packet:
        folders = [Path(args.packet)]
    else:
        videos = ROOT / "videos"
        folders = sorted(p for p in videos.iterdir() if p.is_dir() and (p / "script.md").is_file())

    print("REWRITE SUGGEST (qualitative / direct; no file writes)")
    total = 0
    for folder in folders:
        found = scan_and_suggest(folder)
        total += len(found)
        if not found:
            print(f"{folder.name}: clear")
            continue
        print(f"{folder.name}:")
        for kind, phrase, ctx, sug in found:
            print(f"  [{kind}] '{phrase}'")
            print(f"    context: {ctx}")
            print(f"    suggest: {sug}")
    print(f"suggestions: {total}")
    print("REWRITE SUGGEST DONE")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
