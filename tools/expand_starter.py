#!/usr/bin/env python3
"""Pre-script expand / beat-budget starter for a packet.

Extracts mechanism/topic/problem/viewer from idea.md and prints a structured
beat plan with recommended word targets (hook/payoff/beats/CTA) grounded in
the packet. Suggests 5 body beats by default so total spoken WORDS land near
the ~1200 target for explainer-6-10min without inventing spoken lines,
statistics, or anecdotes.

Does not write files. Does not invent WORDS. Complements draft_starter.py
and expand_brief.py (which needs script headings). Useful before the first
draft so agents know the shape and size before expanding suggestions.
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


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Print a pre-script beat budget and structure skeleton from idea.md. No invented WORDS."
    )
    parser.add_argument("packet", help="Packet folder containing idea.md")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    idea_path = path / "idea.md"
    if not idea_path.is_file():
        print(f"No idea.md in {args.packet}", file=sys.stderr)
        return 1

    idea_text = idea_path.read_text(encoding="utf-8")
    fields = extract_fields(idea_text)
    mech = fields["mechanism"][:70]
    problem = fields["problem"][:70]

    print("EXPAND STARTER (pre-script beat budget and structure; no invented WORDS)")
    print(f"Packet: {path.name}")
    print(f"Viewer: {fields['viewer']}")
    print(f"Topic / Problem: {fields['topic']}")
    print(f"Mechanism: {fields['mechanism']}")
    print()
    print("Format: explainer-6-10min")
    print("Target spoken WORDS: ~1200 (band 900–1500)")
    print("Recommended shape (do not add extra ## headings):")
    print("  Hook (20–35) → Payoff promise (40–70) → 5 body beats (140–220 each) → CTA (40–80)")
    print()
    print("## Suggested beat plan")
    print("| Section              | Target words | Focus (grounded in idea.md) | Notes |")
    print("|----------------------|--------------|------------------------------|-------|")
    print(f"| Hook (0:00–0:12)     | 20–35         | Name the stall ({problem[:40]}) and the mechanism | Keep short; one sting |")
    print(f"| Payoff promise       | 40–70         | One doable outcome using {mech[:40]} | Viewer can state it before beat 2 |")
    print("| Beat 1 — Install      | 140–220       | Show the concrete install of the mechanism on the stall | Worked example |")
    print("| Beat 2 — Cue          | 140–220       | Where the written default lives so the reopen ends | Physical or file cue |")
    print("| Beat 3 — Test         | 140–220       | One small test the viewer can run the same day | Operational check |")
    print("| Beat 4 — Failure mode | 140–220       | What repeats when the mechanism is absent | Use the packet stall |")
    print("| Beat 5 — Keep it      | 140–220       | How the default stays after the first install | Constraint, not pep |")
    print(f"| CTA                  | 40–80         | One under-two-minute action that installs {mech[:30]} | No subscribe pitch |")
    print()
    print("Rough total if mid-band: 28 + 55 + 5×180 + 60 ≈ 1043 (inside 900–1500).")
    print()
    print("Next steps (do not invent spoken lines or statistics):")
    print("1. Optionally run python3 tools/draft_starter.py", args.packet, "for mechanism-aligned WORD candidates.")
    print("2. Expand preferred lines into draft.md, landing each beat near its target.")
    print("3. After headings exist, python3 tools/expand_brief.py", args.packet, "writes the live budget from actual WORDS.")
    print("4. Run tools/quality_scan.py and tools/claim_scan.py before apply_script.py --write.")
    print("This starter writes nothing. Preferred unblocked path remains human OAuth for publish.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
