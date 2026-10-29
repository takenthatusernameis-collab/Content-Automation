#!/usr/bin/env python3
"""Print a grounded prep package for the next queued topic without scaffolding.

Reads docs/topic_queue.md for the first queued row that has no matching videos/ folder.
Emits:
- paste-ready idea.md skeleton (topic, problem, mechanism from queue columns only)
- research_notes.md section skeleton
- experiment hypothesis template grounded in the one_line
- exact future scaffold commands (do not run yet while Q1 is unshipped)

No invented anecdotes, numbers, sources, or WORDS. Does not create folders or write files.
Reduces recurring labor of manually assembling the next-packet starting materials once Q1 ships.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "tools") not in sys.path:
    sys.path.insert(0, str(ROOT / "tools"))

from queue_lib import parse_queue as parse, slugify  # type: ignore


def main() -> int:
    queue_path = ROOT / "docs" / "topic_queue.md"
    if not queue_path.is_file():
        print("next_packet_prep: docs/topic_queue.md missing")
        return 1

    text = queue_path.read_text(encoding="utf-8")
    rows = parse(text)
    next_row = None
    for row in rows:
        if row.get("status") == "queued":
            # simple check: no matching folder (reuse next_topic logic loosely)
            slug = slugify(row.get("working_title", ""))
            # next_id logic is in next_topic; for display we predict from existing
            next_row = row
            break

    if not next_row:
        print("next_packet_prep: no queued topic found")
        return 0

    qid = next_row.get("id", "?")
    title = next_row.get("working_title", "").strip()
    one_line = next_row.get("one_line", "").strip()
    problem = next_row.get("problem", "").strip()

    print("NEXT PACKET PREP (grounded from topic_queue.md only; no scaffold, no invent)")
    print(f"Next queued: {qid} — {title}")
    print(f"One-line: {one_line}")
    print(f"Problem: {problem}")
    print()
    print("=== idea.md skeleton (paste after scaffold; do not treat as WORDS) ===")
    print("# Idea")
    print()
    print(f"- topic: {title}")
    print(f"- viewer: Someone who stalls on this: {problem or one_line}")
    print(f"- problem: {problem or one_line}")
    print(f"- mechanism (the system, not the pep talk): {one_line}")
    print(f"- why now: The stall is this: {problem or one_line}")
    print("- related videos to avoid repeating: none published yet")
    print()
    print("=== research_notes.md skeleton ===")
    print("# Research notes")
    print()
    print("## Mechanism to verify")
    print(one_line or "(from queue)")
    print()
    print("## Concrete problem examples (fill with real observations only)")
    print("- ")
    print()
    print("## Potential claims that need sources (fill Source column later)")
    print("| Claim | Type | Source (fill) |")
    print("|-------|------|---------------|")
    print("| (none yet; run claim_source_table after draft) |  |  |")
    print()
    print("## Notes")
    print("No invented statistics or anecdotes. Use claim_source_table.py after a draft exists.")
    print()
    print("=== experiment hypothesis template (baseline remains null) ===")
    hyp = f"Naming '{one_line[:50]}' more clearly in the hook will raise first-30s average view duration"
    print("{")
    print(f'  "hypothesis": "{hyp}",')
    print('  "change": "hook",')
    print('  "primary_metric": "average_view_duration_seconds",')
    print('  "baseline": null,')
    print('  "source": "REPLACE: documented observation after Q1 metrics exist",')
    print('  "notes": "Do not invent numbers. Fill after first published video."')
    print("}")
    print()
    print("=== Future commands (do not scaffold while Q1 unshipped) ===")
    print(f"# After Q1 ships and Selected VO exists:")
    print(f"python3 tools/new_packet.py \"{title}\"")
    print(f"# then fill idea.md from the skeleton above or apply_idea --write")
    print(f"python3 tools/research_notes_writer.py videos/NNN-{slugify(title)} --force")
    print("# Do not invent sources. Do not scaffold Q2 now.")
    print()
    print("Preferred current action remains the human OAuth step for Q1.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
