#!/usr/bin/env python3
"""Reusable research brief Markdown starter for a packet.

Extracts mechanism/topic/problem from idea.md and emits a structured
research.md template with sections for overview, potential claims to
support, evidence preferences, source capture skeleton, and claim_scan
notes. Grounded in the idea without inventing specific URLs, numbers,
citations, or results.

Complements research_sources_starter.py by providing the full research
document skeleton. Does not invent sources. Does not call external APIs.
Useful for preparing factual support before script drafting and claim_scan.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def extract_fields(idea_text: str) -> dict[str, str]:
    """Heuristic extract of key fields from idea.md."""
    fields = {"mechanism": "", "topic": "", "problem": "", "viewer": ""}
    for line in idea_text.splitlines():
        low = line.lower().strip()
        if not low or low.startswith("#"):
            continue
        if ":" in line:
            key, val = line.split(":", 1)
            key = key.strip().lower()
            val = val.strip()
            if "mechanism" in key and not fields["mechanism"]:
                fields["mechanism"] = val
            elif "topic" in key and not fields["topic"]:
                fields["topic"] = val
            elif "problem" in key and not fields["problem"]:
                fields["problem"] = val
            elif "viewer" in key and not fields["viewer"]:
                fields["viewer"] = val
    fields["mechanism"] = fields["mechanism"] or "unspecified mechanism"
    fields["topic"] = fields["topic"] or fields["problem"] or "unspecified topic"
    fields["problem"] = fields["problem"] or "unspecified problem"
    fields["viewer"] = fields["viewer"] or "the viewer"
    return fields


def suggest_claims(fields: dict[str, str]) -> list[str]:
    """Qualitative claim templates grounded in the packet. No numbers."""
    mech = fields["mechanism"][:60]
    problem = fields["problem"][:60]
    return [
        f"The stall described by '{problem}' occurs when no concrete default is present.",
        f"Installing '{mech}' as a written next action reduces the reopen cycle for this viewer.",
        f"A single under-two-minute install of the mechanism ends the decision delay on the same day.",
    ]


def recommended_actions(packet: str) -> list[str]:
    """Provide concrete copy-paste next steps after the research brief starter."""
    p = packet
    return [
        f"fill research: edit {p}/research.md with real overview, claims support, and verifiable sources (no invented URLs, numbers, or citations)",
        "  (Filled Source column values in the Primary claims table or non-placeholder bullets are auto-extracted by claim_scan.py; no need to also rewrite a ## Sources section)",
        f"sources detail: python3 tools/research_sources_starter.py {p} or python3 tools/research_package_starter.py {p} if more structured sources.md is needed",
        f"claim scan: python3 tools/claim_scan.py {p} after research is filled to confirm support",
        f"move to draft: python3 tools/draft_starter.py {p} once research is ready",
        f"full package: python3 tools/pre_production_package_starter.py {p} or python3 tools/script_package_starter.py {p} for research + draft path",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print a structured research.md skeleton grounded in idea.md. No invented sources or numbers."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    parser.add_argument("--write", action="store_true", help="Write research.md (default: print only)")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    idea_path = path / "idea.md"
    if not idea_path.is_file():
        print(f"No idea.md in {args.packet}", file=sys.stderr)
        return 1

    idea_text = idea_path.read_text(encoding="utf-8")
    fields = extract_fields(idea_text)
    claims = suggest_claims(fields)

    skeleton = f"""# Research Brief

**Packet:** {path.name}
**Viewer:** {fields['viewer']}
**Topic / Problem:** {fields['topic']}
**Mechanism:** {fields['mechanism']}

## Overview
<!-- Restate the problem and mechanism in operational terms. No slogans. -->

The viewer faces {fields['problem']}. The mechanism is {fields['mechanism']}.
This research brief collects support for any consequential claims before script drafting.

## Potential claims to support
<!-- Prefer qualitative restatements. Do not invent statistics. claim_scan.py will flag unsupported digits or hedges. -->

"""
    for i, claim in enumerate(claims, 1):
        skeleton += f"{i}. {claim}\n"
    skeleton += f"""
## Evidence types preferred
- Direct observation of the stall and the install action
- Documented procedure or checklist from a primary source
- Reputable secondary summary that links to the original
- Qualitative case that matches this viewer's context (no invented numbers)

## Source capture
<!-- Fill with real, verifiable sources. Do not invent URLs, dates, or citations.
     Prefer the structure from research_sources_starter.py if more detail is needed.
     Filled Source column values (non-empty, non-placeholder) in the table below
     and any non-placeholder bullets are automatically extracted by tools/claim_scan.py
     and treated as citations. The extractor is header-aware: it detects the Source column
     from the table header and combines Claim + Source strings so both digits and hedges
     in the claim clear reliably. You do not need to also rewrite a ## Sources section. -->

### Primary claims and sources
| Claim | Source (title + link or citation) | Retrieved | How it supports the claim | Notes |
|-------|-----------------------------------|-----------|---------------------------|-------|
|       |                                   |           |                           |       |

### Suggested source categories
- Academic / peer-reviewed:
- Official / government / standards:
- Practitioner documentation:
- Primary data or observation:

## Claim_scan compliance notes
- Avoid digit tokens unless the exact number appears in a non-placeholder Sources bullet or extracted table Source column.
- Avoid survey/authority hedges ("studies show", "experts agree", etc.) unless sourced.
- Prefer qualitative language: "the stall repeats when the default is missing" rather than percentages.
- Update this file before running claim_scan.py or promoting the script.

Do not invent sources, numbers, or results. Update with real references before promotion.
Preferred unblocked path remains human OAuth for publish.
"""

    print("RESEARCH BRIEF STARTER (full research.md skeleton; no invented URLs, numbers, or citations)")
    print(skeleton)

    if args.write:
        out_path = path / "research.md"
        out_path.write_text(skeleton, encoding="utf-8")
        print(f"Wrote {out_path}", file=sys.stderr)

    print("\n---")
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(str(path)):
        print(f"- {rec}")
    print()
    print("Next: fill with real sources and support, then run tools/claim_scan.py after drafting script WORDS. Complements research_sources_starter.py; use either or both. Preferred unblocked path remains human OAuth for publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
