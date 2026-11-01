#!/usr/bin/env python3
"""Write a local recommended_publish_fill.md from ranked metadata options.

Reuses the ranking logic from metadata_selector (term overlap with assignment primary
plus length fitness). For each field that has candidates, selects the highest-scoring
one and formats it as a ready-to-review section suitable for pasting into publish.md.

Does not write publish.md. Does not invent candidates. Output is local and gitignored.
Compounds the selector into a structured fill file so the final selection step
requires even less manual comparison and reformatting.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from metadata_selector import (  # noqa: E402
    extract_key_terms,
    extract_candidates,
    score_candidate,
)
from assignment_utils import read_primary  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write local recommended_publish_fill.md from ranked options"
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing file")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"FAIL: not a directory: {packet}", file=sys.stderr)
        return 1

    out_path = packet / "recommended_publish_fill.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    primary = read_primary(packet)
    if not primary:
        print("INFO: no assignment_source.md primary. Run tools/assignment_source_writer.py first.")
        print("No fill written.")
        return 0

    terms = extract_key_terms(primary)

    fields = [
        ("Title", "title_options.md", (40, 70)),
        ("Description", "description_options.md", (80, 200)),
        ("Thumbnail text", "thumbnail_options.md", (8, 28)),
        ("First comment", "first_comment_options.md", (40, 120)),
        ("End screen", "end_screen_options.md", (20, 60)),
        ("Tags", "tags_options.md", (5, 40)),
    ]

    lines = [
        "# Recommended Publish Fill (local; ranked from options)",
        "",
        "Generated from existing *options.md candidates ranked by key-term overlap",
        "with the assignment primary (via assignment_utils.read_primary) plus length fitness.",
        "Does not invent text. Does not write publish.md.",
        "Review and copy preferred sections into publish.md.",
        "",
        f"Primary assignment: {primary}",
        f"Key terms used: {terms}",
        "",
    ]

    any = False
    for label, fname, ideal in fields:
        path = packet / fname
        cands = extract_candidates(path)
        if not cands:
            lines.append(f"## {label}\n\n(no candidates in {fname})\n")
            continue
        any = True
        scored = []
        for c in cands:
            sc, reason = score_candidate(c, terms, ideal)
            scored.append((sc, c, reason))
        scored.sort(key=lambda x: -x[0])
        best = scored[0]
        lines.append(f"## {label}\n")
        lines.append(f"{best[1]}\n")
        lines.append(f"<!-- score={best[0]} ({best[2]}) -->\n")
        if len(scored) > 1:
            lines.append(f"<!-- runner-up: {scored[1][1]} -->\n")
        lines.append("")

    if not any:
        print("No options files with candidates. Generate them first.")
        return 0

    lines.append("---")
    lines.append("Review against channel voice and length gates before pasting into publish.md.")
    lines.append("Preferred unblocked path remains the human OAuth step for publish.")

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print("Recommended fill ready (local; ranked from existing candidates only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
