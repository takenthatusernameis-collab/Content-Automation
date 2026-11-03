#!/usr/bin/env python3
"""Section pacing consistency check.

Read-only. Uses timeline.plan() so rates and floors stay identical to the planner.
Classifies sections (hook / payoff / beat / cta) and flags durations outside the
locked format band (hook 8-12s spoken, CTA last, overall spoken 6-10 min).
Complements vo_/card_/caption_timeline_consistency. Does not invent media,
run ffmpeg, poll secrets, bump status, or write files.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from timeline import plan, MIN_HOLD  # noqa: E402

HOOK_MIN = 8.0
HOOK_MAX = 12.0
SPOKEN_MIN = 6 * 60
SPOKEN_MAX = 10 * 60


def _classify(title: str) -> str:
    t = title.lower().strip()
    if re.match(r"hook\b", t):
        return "hook"
    if re.match(r"payoff\b", t):
        return "payoff"
    if re.match(r"cta\b", t):
        return "cta"
    if re.search(r"beat\s*\d+", t):
        return "beat"
    return "other"


def inspect(packet: Path) -> dict:
    data = plan(packet)
    rows = data.get("rows") or []
    spoken = float(data.get("spoken") or 0.0)
    if not rows or spoken <= 0:
        return {
            "ok": False,
            "code": "NO_DATA",
            "detail": "no timeline rows or zero spoken",
            "hook_s": None,
            "cta_is_last": False,
            "beat_count": 0,
            "spoken_s": spoken,
            "spoken_ok": False,
        }

    classes = [(_classify(r.get("title", "")), float(r.get("dur") or 0)) for r in rows]
    hook_durs = [d for c, d in classes if c == "hook"]
    hook_s = hook_durs[0] if hook_durs else None
    beat_count = sum(1 for c, _ in classes if c == "beat")
    cta_is_last = bool(classes and classes[-1][0] == "cta")
    spoken_ok = SPOKEN_MIN <= spoken <= SPOKEN_MAX

    issues = []
    if hook_s is None:
        issues.append("no_hook")
    elif not (HOOK_MIN <= hook_s <= HOOK_MAX):
        issues.append(f"hook={hook_s}s")
    if not cta_is_last:
        issues.append("cta_not_last")
    if beat_count < 4 or beat_count > 7:
        issues.append(f"beats={beat_count}")
    if not spoken_ok:
        issues.append(f"spoken={spoken:.0f}s")

    warn = bool(issues)
    return {
        "ok": not warn,
        "code": "WARN" if warn else "OK",
        "detail": "; ".join(issues) if issues else "within format band",
        "hook_s": hook_s,
        "cta_is_last": cta_is_last,
        "beat_count": beat_count,
        "spoken_s": spoken,
        "spoken_ok": spoken_ok,
        "export_s": data.get("export"),
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check section durations against format pacing targets. No writes."
    )
    parser.add_argument("packet", help="Path to packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    rep = inspect(path)
    print(f"packet: {path.name}")
    print(f"spoken_s: {rep.get('spoken_s')}")
    print(f"export_s: {rep.get('export_s')}")
    print(f"hook_s: {rep.get('hook_s') if rep.get('hook_s') is not None else 'n/a'}")
    print(f"cta_is_last: {rep.get('cta_is_last')}")
    print(f"beat_count: {rep.get('beat_count')}")
    print(f"spoken_ok: {rep.get('spoken_ok')}")
    print(f"consistency: {rep['code']} ({rep['detail']})")
    print("Does not execute encode, invent media, or poll OAuth.")
    return 0 if rep["code"] != "NO_DATA" else 2


if __name__ == "__main__":
    raise SystemExit(main())
