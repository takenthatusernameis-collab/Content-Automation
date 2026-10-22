#!/usr/bin/env python3
"""Combined draft expansion coach: progress table + targeted SHORT beat guidance.

Parses draft.md (or script.md fallback), reports spoken-word progress vs targets
for all sections, and for every SHORT body beat prints the matching
mechanism-grounded checklist items plus exact word deficit. Does not invent
spoken lines, statistics, or anecdotes. One-command view that compounds the
value of draft_word_progress.py and draft_short_beat_coach.py, reducing
sequential calls and free-form padding for every future packet.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

from idea_utils import extract

WORD_RE = re.compile(r"WORDS:\s*(.*?)(?:\nVISUAL:|\n## |\Z)", re.S | re.I)
SECTION_RE = re.compile(r"^##\s+(.+?)$", re.M)

TARGETS = {
    "hook": (20, 45),
    "payoff": (40, 90),
    "beat": (140, 220),
    "cta": (40, 90),
    "total": (900, 1500),
}


def count_words(text: str) -> int:
    cleaned = re.sub(r"[^\w\s'-]", " ", text)
    return len([w for w in cleaned.split() if w.strip()])


def classify(heading: str) -> str:
    h = heading.lower()
    if "hook" in h:
        return "hook"
    if "payoff" in h:
        return "payoff"
    if "cta" in h or "end" in h:
        return "cta"
    if "beat" in h:
        return "beat"
    return "other"


def extract_mech(idea_text: str) -> tuple[str, str]:
    mech, problem, _ = extract(idea_text)
    return mech or "the written default", problem or "the stall"


def checklist_for(heading: str, mech: str) -> list[str]:
    base = mech[:50]
    h = heading.lower()
    if "install" in h or "beat 1" in h:
        return [
            f"One worked example of writing the {base} at the top of the open list before scrolling.",
            "A distinction between reopening the whole page vs. finishing the first two minutes.",
            "The exact file or note location the viewer already has.",
        ]
    if "place" in h or "cue" in h or "beat 2" in h:
        return [
            f"Where the written {base} lives so the reopen ends (sticky, note app, top of document).",
            "A short scene of the stall starting when the cue is missing.",
            "One physical or file action the viewer can finish in under two minutes.",
        ]
    if "test" in h or "beat 3" in h:
        return [
            f"An operational check the viewer can run the same day using the {base}.",
            "What success looks like (the stall does not reopen).",
            "A failure signal if the test is skipped.",
        ]
    if "failure" in h or "beat 4" in h:
        return [
            f"What repeats when the {base} is absent: the list stays the whole page, the next action stays unnamed.",
            "A concrete scene of the delay starting again.",
            "The missing cue that would have ended the reopen.",
        ]
    if "keep" in h or "beat 5" in h:
        return [
            f"How the constraint of the {base} stays after the first install (not pep).",
            "One way the cue remains visible on the device or in the file the viewer already uses.",
            "What changes if the default is removed.",
        ]
    return [
        f"One concrete worked example of the {base} on this packet's stall.",
        "A distinction or operational test the viewer can run the same day.",
        "A short failure-mode scene when the mechanism is absent.",
    ]


def recommended_actions(rows: list, total_status: str, short_count: int, packet_path: Path) -> list[str]:
    """Map progress signals to smallest useful next tool with concrete copy-paste commands (no invent)."""
    p = str(packet_path)
    recs = []
    if short_count > 0:
        recs.append(f"expansion: expand SHORT beats using the checklists above; then re-run python3 tools/draft_expansion_coach.py {p} or python3 tools/draft_short_beat_coach.py {p}")
    if total_status == "SHORT":
        recs.append(f"total: overall spoken words SHORT of 900; grow thinnest beats with concrete mechanism scenes; then re-run python3 tools/draft_expansion_coach.py {p}")
    elif total_status == "LONG":
        recs.append(f"total: overall spoken words LONG of 1500; cut filler/repetition rather than mechanism; then re-run python3 tools/draft_expansion_coach.py {p}")
    # Always suggest the full pre-apply gate as the next quality step
    recs.append(f"quality gate: after expansion signals improve, run python3 tools/draft_pre_apply_coach.py {p} for full signals + copy-paste next")
    if not recs or (short_count == 0 and total_status == "OK"):
        recs.append(f"all expansion OK: proceed to python3 tools/draft_pre_apply_coach.py {p} then apply consideration")
    return recs


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Combined progress table + SHORT-beat coach for draft.md. No invented lines."
    )
    parser.add_argument("packet", help="Packet folder containing draft.md and idea.md")
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
    mech, _problem = extract_mech(idea_text)
    sections = SECTION_RE.findall(text)
    words_blocks = WORD_RE.findall(text)

    print("DRAFT EXPANSION COACH (progress table + targeted SHORT-beat guidance; no invented lines/stats)")
    print(f"Source: {source.name}")
    print(f"Packet: {path.name}")
    print(f"Mechanism: {mech}")
    print()

    # Progress table
    total = 0
    rows = []
    block_idx = 0
    for heading in sections:
        kind = classify(heading)
        count = 0
        if block_idx < len(words_blocks):
            count = count_words(words_blocks[block_idx])
            block_idx += 1
        total += count
        lo, hi = TARGETS.get(kind, (0, 9999))
        if kind == "other":
            status = "OK"
            target_str = "-"
        elif count < lo:
            status = "SHORT"
            target_str = f"{lo}-{hi}"
        elif count > hi:
            status = "LONG"
            target_str = f"{lo}-{hi}"
        else:
            status = "OK"
            target_str = f"{lo}-{hi}"
        rows.append((heading.strip(), count, target_str, status, kind))

    print(f"{'Section':<40} {'Words':>6} {'Target':>10} {'Status':>8}")
    print("-" * 70)
    for heading, count, target_str, status, _k in rows:
        short_h = (heading[:37] + "...") if len(heading) > 40 else heading
        print(f"{short_h:<40} {count:>6} {target_str:>10} {status:>8}")

    lo, hi = TARGETS["total"]
    total_status = "SHORT" if total < lo else ("LONG" if total > hi else "OK")
    print("-" * 70)
    print(f"{'TOTAL':<40} {total:>6} {lo}-{hi:>6} {total_status:>8}")
    print()

    # Targeted coaching for SHORT body beats
    short_count = 0
    for heading, count, _ts, status, kind in rows:
        if kind != "beat" or status != "SHORT":
            continue
        short_count += 1
        deficit = TARGETS["beat"][0] - count
        print(f"## {heading}  ({count} words, SHORT by {deficit})")
        print("Add these concrete elements while expanding (do not invent sources, numbers, or anecdotes):")
        for item in checklist_for(heading, mech):
            print(f"- {item}")
        print(f"<!-- Grow by ~{deficit} spoken words using only the above. Aim for {TARGETS['beat'][0]}-{TARGETS['beat'][1]}. -->")
        print()

    if short_count == 0:
        print("No SHORT body beats. Progress table above is complete.")
    else:
        print(f"---\n{short_count} SHORT body beat(s). Expand using the items above, then re-run this tool.")
    print()

    print("## RECOMMENDED NEXT (signal-specific; copy-paste ready; no invent)")
    for rec in recommended_actions(rows, total_status, short_count, path):
        print(f"- {rec}")
    print()

    print("Next (do not invent sources, numbers, or anecdotes):")
    print("- Prefer concrete mechanism language; avoid anti-slop phrases in docs/content_quality.md.")
    print("- Run python3 tools/quality_scan.py and python3 tools/claim_scan.py before apply_script.py --write.")
    print("- Trim any LONG sections by cutting filler rather than adding more.")
    print("This tool writes nothing. Preferred unblocked path remains human OAuth for publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
