#!/usr/bin/env python3
"""Originality checklist printer for draft.md.

Prints the seven-item originality test from docs/content_quality.md
with packet-specific extracts from idea.md and draft.md so the questions
are grounded and easier to answer. Does not invent content, score, or
rewrite. Does not write files. Compounds by making the required pre-promotion
originality review mechanically assisted for every future packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

MECH_RE = re.compile(r"mechanism[^\n]*:\s*(.+)", re.I)
PROBLEM_RE = re.compile(r"problem:\s*(.+)", re.I)
TOPIC_RE = re.compile(r"topic:\s*(.+)", re.I)
VIEWER_RE = re.compile(r"viewer:\s*(.+)", re.I)
WORD_RE = re.compile(r"WORDS:\s*(.*?)(?:\nVISUAL:|\n## |\Z)", re.S | re.I)
SECTION_RE = re.compile(r"^##\s+(.+?)$", re.M)


def extract_idea(idea_text: str) -> dict[str, str]:
    out = {"mech": "", "problem": "", "topic": "", "viewer": ""}
    for line in idea_text.splitlines():
        m = MECH_RE.search(line)
        if m:
            out["mech"] = m.group(1).strip().rstrip(".")
        p = PROBLEM_RE.search(line)
        if p:
            out["problem"] = p.group(1).strip().rstrip(".")
        t = TOPIC_RE.search(line)
        if t:
            out["topic"] = t.group(1).strip().rstrip(".")
        v = VIEWER_RE.search(line)
        if v:
            out["viewer"] = v.group(1).strip().rstrip(".")
    return out


def extract_sections(text: str) -> list[tuple[str, str]]:
    sections = SECTION_RE.findall(text)
    words_blocks = WORD_RE.findall(text)
    result = []
    for i, heading in enumerate(sections):
        words = words_blocks[i].strip() if i < len(words_blocks) else ""
        result.append((heading.strip(), words))
    return result


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print packet-grounded originality checklist for draft.md. No writes, no inventing."
    )
    parser.add_argument("packet", help="Packet folder containing draft.md (or script.md) and idea.md")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    draft = path / "draft.md"
    source = draft if draft.is_file() else path / "script.md"
    idea = path / "idea.md"
    if not source.is_file():
        print(f"No draft.md or script.md in {args.packet}", file=sys.stderr)
        return 1
    if not idea.is_file():
        print(f"No idea.md in {args.packet}", file=sys.stderr)
        return 1

    text = source.read_text(encoding="utf-8").replace("\r\n", "\n")
    idea_text = idea.read_text(encoding="utf-8")
    idea_data = extract_idea(idea_text)
    sections = extract_sections(text)

    print("ORIGINALITY CHECKLIST (seven questions from docs/content_quality.md; packet-grounded extracts; no inventing, no scoring)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print()
    print(f"Mechanism: {idea_data['mech'] or '(none found)'}")
    print(f"Problem: {idea_data['problem'] or '(none found)'}")
    print(f"Topic: {idea_data['topic'] or '(none found)'}")
    print(f"Viewer: {idea_data['viewer'] or '(none found)'}")
    print()

    print("1. Could the mechanism be explained in one sentence?")
    print(f"   Extracted mechanism: {idea_data['mech'] or '(missing — stop and fix idea.md)'}")
    print("   Answer should be yes before promotion. If blank or pep-talk, revise idea.md.")
    print()

    print("2. Does each beat contain at least one concrete action, example, distinction, or test?")
    for heading, words in sections:
        if "beat" in heading.lower() or "hook" in heading.lower() or "payoff" in heading.lower() or "cta" in heading.lower():
            snippet = (words[:120] + "...") if len(words) > 120 else words
            print(f"   {heading}: {snippet or '(empty)'}")
    print("   Each should show a worked example, distinction, or operational test grounded in the mechanism.")
    print()

    print("3. Is there at least one detail that clearly belongs to this packet rather than any topic in the niche?")
    print(f"   Packet topic/problem: {idea_data['topic']} / {idea_data['problem']}")
    print("   Look for a detail (file, surface, verb, stall scene) that could not be swapped into a different video.")
    print()

    print("4. Are the examples internally consistent with the packet's viewer/problem?")
    print(f"   Viewer: {idea_data['viewer']}")
    print(f"   Problem: {idea_data['problem']}")
    print("   Examples should match this viewer and this stall, not a generic productivity scene.")
    print()

    print("5. Can any paragraph be deleted without losing information? If yes, cut it.")
    print("   Review the WORDS blocks above. Cut motivational padding, repeated conclusions, or meta framing.")
    print()

    print("6. Does the final CTA naturally follow from the mechanism?")
    cta_words = next((w for h, w in sections if "cta" in h.lower()), "")
    print(f"   CTA WORDS: {cta_words[:150] or '(empty)'}")
    print(f"   Mechanism: {idea_data['mech']}")
    print("   CTA should be the under-two-minute install of this mechanism, not generic engagement.")
    print()

    print("7. Does the script avoid pretending that generated prose is lived human experience?")
    print("   No fake anecdotes, 'I tested this', personal results, or implied experiments.")
    print("   Use 'you' procedures only. If any first-person experience appears, rewrite it.")
    print()

    print("Next (do not invent anecdotes, statistics, or sources):")
    print("- Answer each question. A 'no' is a revision signal before apply_script.py --write.")
    print("- Prefer concrete mechanism language from the extracts above.")
    print("- Then run tools/draft_pre_apply_coach.py for quality and claim signals.")
    print("This tool writes nothing. Preferred unblocked path remains human OAuth for publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
