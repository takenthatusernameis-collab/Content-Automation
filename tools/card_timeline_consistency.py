#!/usr/bin/env python3
"""Card / timeline consistency check.

Read-only. Uses timeline.plan() so rates, floors, and end-screen reserve stay identical
to the planner and to vo_timeline_consistency.py. Flags short holds (<1.5s), missing
cards, and whether the final CTA segment covers into the 20s end-screen reserve.
Does not invent media, run ffmpeg, poll secrets, bump status, or write files.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from timeline import plan, MIN_HOLD, END_SCREEN  # noqa: E402


def inspect(packet: Path) -> dict:
    data = plan(packet)
    rows = data.get("rows") or []
    if not rows:
        return {
            "ok": False,
            "code": "NO_DATA",
            "detail": "no timeline rows",
            "short_holds": 0,
            "missing_cards": 0,
            "cta_covers_reserve": False,
            "export_s": data.get("export"),
            "spoken_s": data.get("spoken"),
        }

    short = []
    missing = []
    for r in rows:
        if r.get("dur", 0) < MIN_HOLD:
            short.append(f"{r.get('title', '?')} ({r.get('dur')}s)")
        if r.get("card") and r.get("card_on_disk") != "yes":
            missing.append(r.get("card") or r.get("title"))

    # CTA coverage into end-screen: last row should start early enough that its hold
    # plus the reserve keeps the card visible for the final 20s.
    last = rows[-1]
    last_start = float(last.get("start") or 0)
    last_dur = float(last.get("dur") or 0)
    export = float(data.get("export") or 0)
    reserve_start = max(0.0, export - END_SCREEN)
    cta_covers = (last_start + last_dur) >= reserve_start and last_dur >= MIN_HOLD

    warn = bool(short or missing or not cta_covers)
    return {
        "ok": not warn,
        "code": "WARN" if warn else "OK",
        "detail": f"short={len(short)} missing={len(missing)} cta_ok={cta_covers}",
        "short_holds": len(short),
        "missing_cards": len(missing),
        "cta_covers_reserve": cta_covers,
        "export_s": export,
        "spoken_s": data.get("spoken"),
        "short_list": short[:5],
        "missing_list": missing[:5],
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check timeline holds, card presence, and CTA end-screen coverage. No writes."
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
    print(f"short_holds: {rep.get('short_holds')}")
    print(f"missing_cards: {rep.get('missing_cards')}")
    print(f"cta_covers_reserve: {rep.get('cta_covers_reserve')}")
    print(f"consistency: {rep['code']} ({rep['detail']})")
    if rep.get("short_list"):
        print("short examples:", ", ".join(rep["short_list"]))
    if rep.get("missing_list"):
        print("missing examples:", ", ".join(rep["missing_list"]))
    print("Does not execute encode, invent media, or poll OAuth.")
    return 0 if rep["code"] != "NO_DATA" else 2


if __name__ == "__main__":
    raise SystemExit(main())
