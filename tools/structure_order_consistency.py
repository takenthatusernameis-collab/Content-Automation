#!/usr/bin/env python3
"""Structure order consistency check.

Read-only. Uses timeline.plan() so section titles stay identical to the planner.
Classifies sections and verifies the locked format order: hook first, payoff before
any numbered beat, beats sequential, CTA last. Complements section_pacing_consistency
(which checks durations and counts). Does not invent media, run ffmpeg, poll secrets,
bump status, or write files.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from timeline import plan  # noqa: E402


def _classify(title: str) -> tuple[str, int | None]:
    t = title.lower().strip()
    if re.match(r"hook\b", t):
        return "hook", None
    if re.match(r"payoff\b", t):
        return "payoff", None
    if re.match(r"cta\b", t):
        return "cta", None
    m = re.search(r"beat\s*(\d+)", t)
    if m:
        return "beat", int(m.group(1))
    return "other", None


def inspect(packet: Path) -> dict:
    data = plan(packet)
    rows = data.get("rows") or []
    if not rows:
        return {
            "ok": False,
            "code": "NO_DATA",
            "detail": "no timeline rows",
            "sequence": [],
            "hook_first": False,
            "payoff_before_beats": False,
            "beats_sequential": False,
            "cta_last": False,
        }

    classified = [_classify(r.get("title", "")) for r in rows]
    sequence = [c[0] + (str(c[1]) if c[1] is not None else "") for c in classified]

    hook_first = bool(classified and classified[0][0] == "hook")
    cta_last = bool(classified and classified[-1][0] == "cta")

    # Payoff before any numbered beat
    payoff_idx = next((i for i, c in enumerate(classified) if c[0] == "payoff"), None)
    first_beat_idx = next((i for i, c in enumerate(classified) if c[0] == "beat"), None)
    payoff_before_beats = (
        payoff_idx is not None
        and (first_beat_idx is None or payoff_idx < first_beat_idx)
    )

    # Beats sequential (1,2,3... without gaps or duplicates in order)
    beat_nums = [c[1] for c in classified if c[0] == "beat" and c[1] is not None]
    beats_sequential = True
    if beat_nums:
        expected = list(range(1, len(beat_nums) + 1))
        beats_sequential = beat_nums == expected

    issues = []
    if not hook_first:
        issues.append("hook_not_first")
    if not payoff_before_beats:
        issues.append("payoff_not_before_beats" if payoff_idx is not None else "no_payoff")
    if not beats_sequential:
        issues.append(f"beats_not_sequential={beat_nums}")
    if not cta_last:
        issues.append("cta_not_last")

    warn = bool(issues)
    return {
        "ok": not warn,
        "code": "WARN" if warn else "OK",
        "detail": "; ".join(issues) if issues else "order matches format",
        "sequence": sequence,
        "hook_first": hook_first,
        "payoff_before_beats": payoff_before_beats,
        "beats_sequential": beats_sequential,
        "cta_last": cta_last,
        "beat_nums": beat_nums,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check section order against locked format (hook, payoff, sequential beats, CTA last). No writes."
    )
    parser.add_argument("packet", help="Path to packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    rep = inspect(path)
    print(f"packet: {path.name}")
    print(f"sequence: {' -> '.join(rep.get('sequence') or [])}")
    print(f"hook_first: {rep.get('hook_first')}")
    print(f"payoff_before_beats: {rep.get('payoff_before_beats')}")
    print(f"beats_sequential: {rep.get('beats_sequential')}")
    print(f"cta_last: {rep.get('cta_last')}")
    print(f"consistency: {rep['code']} ({rep['detail']})")
    print("Does not execute encode, invent media, or poll OAuth.")
    return 0 if rep["code"] != "NO_DATA" else 2


if __name__ == "__main__":
    raise SystemExit(main())
