#!/usr/bin/env python3
"""Originality report for one packet's script.

Reads script.md WORDS and idea.md, then reports signals for the 7-point originality
test in docs/content_quality.md. Does not write files, invent facts, or call the
network. A report is a starting point for revision, not a pass/fail gate.

Compounds across every future video by making the editorial originality check
repeatable and visible in one command.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from idea_utils import extract as idea_extract  # noqa: E402


def extract_words(script_text: str) -> str:
    """Pull all WORDS: blocks from script.md."""
    words = []
    current = []
    in_words = False
    for line in script_text.splitlines():
        if line.strip().startswith("WORDS:"):
            in_words = True
            current = []
            continue
        if in_words and (line.startswith("##") or line.strip().startswith("VISUAL:")):
            if current:
                words.append(" ".join(current).strip())
            in_words = False
            current = []
            continue
        if in_words:
            current.append(line.strip())
    if current:
        words.append(" ".join(current).strip())
    return "\n".join(words)


def extract_mechanism(idea_text: str) -> str:
    mech, _problem, _topic = idea_extract(idea_text)
    return mech


def extract_priority_signals(lines: list[str]) -> list[str]:
    """Surface high-signal weak/missing/check lines first for focused review."""
    priority = []
    for line in lines:
        low = line.lower()
        if any(k in low for k in ("weak", "missing", "check", "long", "review", "no idea")):
            priority.append(line.strip())
    return priority[:6]


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: python3 tools/originality_report.py <packet-folder>")
        return 1
    packet = Path(sys.argv[1]).resolve()
    if not packet.is_dir():
        print(f"not a directory: {packet}")
        return 1

    script_path = packet / "script.md"
    idea_path = packet / "idea.md"
    if not script_path.is_file():
        print("no script.md")
        return 1

    script_text = script_path.read_text(encoding="utf-8")
    idea_text = idea_path.read_text(encoding="utf-8") if idea_path.is_file() else ""
    words = extract_words(script_text)
    mechanism = extract_mechanism(idea_text)

    print(f"ORIGINALITY REPORT: {packet.name}")
    print("=" * 60)
    print(f"Mechanism from idea: {mechanism or '(missing)'}")
    print(f"WORDS length: {len(words.split())} words")
    print()

    report_lines = []

    # 1. Could the mechanism be explained in one sentence?
    print("1. Mechanism one-sentence explainable?")
    if mechanism and len(mechanism.split()) <= 25:
        sig = "  signal: yes (idea mechanism is already short)"
        print(sig)
    else:
        sig = "  signal: check idea.md mechanism length"
        print(sig)
    report_lines.append(sig)

    # 2. Each beat contains at least one concrete action/example?
    print("\n2. Concrete actions / examples present?")
    concrete_patterns = [
        r"\b(write|put|open|start|send|record|reply|close|hide|cover|rewrite|pick|name)\b",
        r"\b(verb|sentence|card|surface|file|folder|list|board|planner)\b",
    ]
    hits = sum(len(re.findall(p, words, re.IGNORECASE)) for p in concrete_patterns)
    if hits >= 8:
        sig = f"  signal: strong ({hits} concrete markers)"
    elif hits >= 4:
        sig = f"  signal: moderate ({hits} concrete markers)"
    else:
        sig = f"  signal: weak ({hits} concrete markers) — add specific verbs/objects"
    print(sig)
    report_lines.append(sig)

    # 3. At least one detail that belongs to this packet?
    print("\n3. Packet-specific detail present?")
    if mechanism:
        key = mechanism.split()[0:4]
        key_phrase = " ".join(key).lower()
        if key_phrase in words.lower() or any(k.lower() in words.lower() for k in key if len(k) > 3):
            sig = "  signal: yes (mechanism language appears in WORDS)"
        else:
            sig = "  signal: weak — mechanism terms not clearly in WORDS"
    else:
        sig = "  signal: no idea mechanism to check against"
    print(sig)
    report_lines.append(sig)

    # 4. Examples internally consistent?
    print("\n4. Examples consistent with viewer/problem?")
    _mech, problem, _topic = idea_extract(idea_text) if idea_text else ("", "", "")
    if problem and any(w in words.lower() for w in problem.lower().split() if len(w) > 4):
        sig = "  signal: yes (problem language echoed)"
    else:
        sig = "  signal: check manually"
    print(sig)
    report_lines.append(sig)

    # 5. Can any paragraph be deleted without losing information?
    print("\n5. Cuttable paragraphs / repetition?")
    sentences = [s.strip() for s in re.split(r"[.!?]", words) if s.strip()]
    if len(sentences) > 40:
        sig = f"  signal: long ({len(sentences)} sentences) — look for repeated conclusions"
    else:
        sig = f"  signal: compact ({len(sentences)} sentences)"
    print(sig)
    report_lines.append(sig)

    # 6. Final CTA naturally follows from the mechanism?
    print("\n6. CTA follows mechanism?")
    cta_match = re.search(r"## CTA.*?WORDS:\s*(.+?)(?=##|\Z)", script_text, re.DOTALL | re.IGNORECASE)
    cta = cta_match.group(1).strip() if cta_match else ""
    if cta and mechanism and any(w.lower() in cta.lower() for w in mechanism.split() if len(w) > 4):
        sig = "  signal: yes"
    else:
        sig = "  signal: check CTA vs mechanism"
    print(sig)
    report_lines.append(sig)

    # 7. Avoids pretending generated prose is lived experience?
    print("\n7. No fake lived experience claims?")
    fake = re.findall(r"\b(i tried|i tested|my clients|users reported|in my experience)\b", words, re.IGNORECASE)
    if not fake:
        sig = "  signal: clear (no personal-experience claims detected)"
    else:
        sig = f"  signal: review ({len(fake)} potential claims)"
    print(sig)
    report_lines.append(sig)

    priority = extract_priority_signals(report_lines)
    print()
    print("=" * 60)
    if priority:
        print("--- Priority review: high-signal originality issues (focus first) ---")
        for p in priority:
            print(p)
        print()
    print("ORIGINALITY REPORT DONE (no files written)")
    print("Use as revision signals. Re-run quality_scan / claim_scan after edits.")
    if priority:
        print(f"PRIORITY: {len(priority)} high-signal issues listed above for first attention.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
