#!/usr/bin/env python3
"""Generate a preliminary early_assets.md stub from idea.md visual plan.

Extracts mechanism/problem/topic and builds a card table in assets.md format
using the same visual sequence logic. Grounded only in those fields. No invented
content. Output stays local (gitignored). Allows card planning and filename
suggestions before script.md VISUAL lines exist. Complements asset_brief.py
(which requires script) and visual_sequence_plan.py. Reduces recurring labor
of manually transferring the plan into an assets intake stub for every future
packet. Aligns with text-card first, short on-screen, channel voice.
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from idea_utils import extract as idea_extract  # noqa: E402

try:
    from visual_sequence_plan import build_visuals
except ImportError:
    def build_visuals(mech, problem, topic):
        base = mech or "written next-action default"
        stall = problem or "the stall"
        return [
            {"segment": "Hook", "on_screen": f"Stall: {stall[:40]}", "type": "text-card", "note": "Same promise as hook."},
            {"segment": "Payoff", "on_screen": "Default installed", "type": "text-card", "note": "Outcome before middle."},
            {"segment": "Beat 1", "on_screen": f"Name the stall: {stall[:30]}", "type": "text-card", "note": "First verb."},
            {"segment": "Beat 2", "on_screen": f"Place: {base[:30]}", "type": "text-card", "note": "Where eyes land."},
            {"segment": "Beat 3", "on_screen": "First action (5 min)", "type": "text-card", "note": "Concrete step."},
            {"segment": "Beat 4", "on_screen": "Point at the default", "type": "text-card", "note": "When stall returns."},
            {"segment": "CTA", "on_screen": f"Install: {base[:35]}", "type": "text-card", "note": "Assignment."},
        ]


def slugify(text: str, limit: int = 36) -> str:
    import re
    s = text.lower()
    s = re.sub(r"[^a-z0-9]+", "-", s)
    s = re.sub(r"-{2,}", "-", s).strip("-")
    return s[:limit].strip("-") or "card"


def beat_prefix(segment: str) -> str:
    s = segment.strip().lower()
    if s.startswith("hook"):
        return "hook"
    if s.startswith("payoff"):
        return "payoff"
    if s.startswith("beat"):
        return s.replace(" ", "")
    if s.startswith("cta"):
        return "cta"
    return "card"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Generate local early_assets.md stub from idea.md visual plan"
    )
    parser.add_argument("packet", type=Path, help="Packet directory")
    parser.add_argument("--force", action="store_true", help="Overwrite existing file")
    args = parser.parse_args()

    packet = args.packet.resolve()
    if not packet.is_dir():
        print(f"FAIL: not a directory: {packet}", file=sys.stderr)
        return 1

    idea_path = packet / "idea.md"
    if not idea_path.is_file():
        print("FAIL: idea.md missing", file=sys.stderr)
        return 2

    out_path = packet / "early_assets.md"
    if out_path.exists() and not args.force:
        print(f"SKIP: {out_path} exists (use --force to overwrite)")
        return 0

    idea_text = idea_path.read_text(encoding="utf-8")
    mech, problem, topic = idea_extract(idea_text)

    if not mech and not problem:
        print("FAIL: no mechanism or problem found in idea.md", file=sys.stderr)
        return 2

    visuals = build_visuals(mech, problem, topic)
    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    lines = [
        "# Early Assets Stub (preliminary)",
        "",
        "Generated locally from idea.md mechanism/problem/topic visual plan only.",
        "Preliminary card table for planning before script.md VISUAL lines exist.",
        "Not the official assets.md. Use tools/asset_brief.py after script is ready.",
        "Text-card first. On-screen short. No invented content, stock, or claims.",
        "Channel voice: calm, specific, operational. Assignment, not a reply prompt.",
        "",
        f"- Topic: {topic or '(none)'}",
        f"- Problem: {problem or '(none)'}",
        f"- Mechanism / default: {mech or '(none)'}",
        "",
        f"Generated: {generated}",
        f"Card count: {len(visuals)}",
        "",
        "## Cards",
        "",
        "| Beat | Need | Type | Suggested file | Source | Status |",
        "|------|------|------|----------------|--------|--------|",
    ]
    for v in visuals:
        beat = v["segment"]
        need = v["on_screen"].replace("|", "/")
        ctype = v["type"]
        prefix = beat_prefix(beat)
        fname = f"cards/{prefix}-{slugify(need)}.png"
        lines.append(f"| {beat} | {need} | {ctype} | `{fname}` | plan | planned |")

    lines.extend([
        "",
        "## Filename convention",
        "- Pattern: `cards/{beat}-{short-slug}.png`",
        "- Types: text-card or diagram (from plan)",
        "- Rules: docs/assets.md",
        "",
        "---",
        "Review and adapt. Prefer official assets.md from script VISUAL when available.",
        "Do not mark ready until files exist. Do not invent locations or claims.",
    ])

    out_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"WROTE: {out_path}")
    print(f"cards: {len(visuals)}")
    print(f"mech_found: {bool(mech)}")
    print(f"problem_found: {bool(problem)}")
    print(f"topic_found: {bool(topic)}")
    print("Early assets stub ready (local; estimated from packet fields only).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
