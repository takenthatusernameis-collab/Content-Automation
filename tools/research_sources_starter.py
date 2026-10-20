#!/usr/bin/env python3
"""Reusable research sources Markdown starter for a packet.

Detects key claims or mechanism from idea.md and emits a structured
sources.md template with sections for primary claims, evidence type,
suggested source categories, and notes, grounded in the idea without
inventing specific URLs, numbers, or citations.

Does not invent sources or results. Does not call external APIs.
Useful for preparing factual-claim support before claim_scan.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def extract_mechanism_topic(idea_text: str) -> tuple[str, str]:
    """Heuristic extract of mechanism and topic from idea.md."""
    mechanism = ""
    topic = ""
    for line in idea_text.splitlines():
        low = line.lower()
        if "mechanism" in low and not mechanism:
            mechanism = line.split(":", 1)[-1].strip() if ":" in line else line.strip()
        if "topic" in low and not topic:
            topic = line.split(":", 1)[-1].strip() if ":" in line else line.strip()
        if "problem" in low and not topic:
            topic = line.split(":", 1)[-1].strip() if ":" in line else line.strip()
    return mechanism or "unspecified mechanism", topic or "unspecified topic"


def recommended_actions(packet: str) -> list[str]:
    """Provide concrete copy-paste next steps after the research sources starter."""
    p = packet
    return [
        f"fill sources: edit {p}/sources.md with real, verifiable sources for the listed claims (no invented URLs or citations)",
        "  (Source-log table Source column or non-placeholder bullets are auto-extracted by claim_scan.py; no need to also rewrite research.md)",
        f"research brief: python3 tools/research_brief_starter.py {p} or python3 tools/research_package_starter.py {p}",
        f"claim scan: python3 tools/claim_scan.py {p} after sources are filled to confirm support",
        f"move to draft: python3 tools/draft_starter.py {p} once research is ready",
        f"full package: python3 tools/pre_production_package_starter.py {p} for research + draft path",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print a structured sources.md skeleton grounded in idea.md. No invented sources."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    parser.add_argument("--write", action="store_true", help="Write sources.md (default: print only)")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    idea_path = path / "idea.md"
    if not idea_path.is_file():
        print(f"No idea.md in {args.packet}", file=sys.stderr)
        return 1

    idea_text = idea_path.read_text(encoding="utf-8")
    mechanism, topic = extract_mechanism_topic(idea_text)

    skeleton = f"""# Research Sources

**Packet:** {path.name}
**Topic / Problem:** {topic}
**Mechanism:** {mechanism}

## Primary claims to support
<!-- List 2-5 consequential factual claims from the script or idea that need sources.
     Prefer qualitative restatements if numbers are not verified. -->

1. 
2. 
3. 

## Evidence types preferred
- Primary research / peer-reviewed study
- Official statistics or government data
- Reputable secondary summary with original link
- Direct observation or documented case (if applicable)

## Suggested source categories
<!-- Fill with real, verifiable sources. Do not invent URLs or citations. -->

- Academic / journal:
- Official / government:
- Industry / practitioner report:
- Primary document or dataset:

## Notes and caveats
<!-- Record date retrieved, any limitations, and how the source supports the claim.
     claim_scan.py will flag unsupported numbers or assertions. -->

## Source log
<!-- Filled Source column values (non-empty, non-placeholder) and any non-placeholder
     bullets elsewhere in this file are automatically extracted by tools/claim_scan.py
     and treated as citations. The extractor is header-aware: it detects the Source column
     from the table header and combines Claim + Source strings so both digits and hedges
     in the claim clear reliably. You do not need to also rewrite research.md. -->
| Claim | Source | Retrieved | Notes |
|-------|--------|-----------|-------|
|       |        |           |       |

Do not invent sources. Prefer existing reputable references. Update before promotion.
"""

    print("RESEARCH SOURCES STARTER (skeleton only; no invented URLs or citations)")
    print(skeleton)

    if args.write:
        out_path = path / "sources.md"
        out_path.write_text(skeleton, encoding="utf-8")
        print(f"Wrote {out_path}", file=sys.stderr)

    print("\n---")
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(str(path)):
        print(f"- {rec}")
    print()
    print("Next: fill with real sources before running claim_scan.py. Preferred unblocked path remains human OAuth for publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
