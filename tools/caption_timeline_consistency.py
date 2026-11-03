#!/usr/bin/env python3
"""Caption / timeline consistency check.

Read-only. Parses captions.srt (same cue rules as caption_gate) and compares cue coverage
to timeline.plan() spoken sections. Flags large start lag, end overrun, or uncovered gaps
between section boundaries and cue spans. Complements vo_ and card_timeline_consistency.
Does not invent media, run ffmpeg, poll secrets, bump status, or write files.
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

CUE_RE = re.compile(
    r"(\d+)\s*\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\s*\n(.*?)(?=\n\n|\Z)",
    re.S,
)


def _seconds(stamp: str) -> float:
    h, m, rest = stamp.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def parse_cues(packet: Path) -> list[dict] | None:
    path = packet / "captions.srt"
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8")
    cues = []
    for match in CUE_RE.finditer(text.strip() + "\n"):
        cues.append(
            {
                "start": _seconds(match.group(2)),
                "end": _seconds(match.group(3)),
            }
        )
    return cues if cues else None


def inspect(packet: Path) -> dict:
    data = plan(packet)
    rows = data.get("rows") or []
    spoken = float(data.get("spoken") or 0.0)
    cues = parse_cues(packet)
    if not rows or spoken <= 0 or not cues:
        return {
            "ok": False,
            "code": "NO_DATA",
            "detail": "missing timeline rows, spoken estimate, or captions.srt",
            "spoken_s": spoken,
            "cue_count": len(cues) if cues else 0,
            "start_lag_s": None,
            "end_overrun_s": None,
            "uncovered_sections": 0,
        }

    first_start = min(c["start"] for c in cues)
    last_end = max(c["end"] for c in cues)
    start_lag = round(first_start, 2)
    end_overrun = round(last_end - spoken, 2)

    # Simple coverage: a section is "covered" if some cue overlaps its [start, start+dur]
    uncovered = 0
    for r in rows:
        s = float(r.get("start") or 0)
        d = float(r.get("dur") or 0)
        end = s + d
        if not any(c["end"] > s and c["start"] < end for c in cues):
            uncovered += 1

    # Soft thresholds
    warn = (
        start_lag > 2.0
        or end_overrun > 3.0
        or end_overrun < -5.0
        or uncovered > 0
    )
    return {
        "ok": not warn,
        "code": "WARN" if warn else "OK",
        "detail": f"lag={start_lag}s overrun={end_overrun}s uncovered={uncovered}",
        "spoken_s": spoken,
        "cue_count": len(cues),
        "start_lag_s": start_lag,
        "end_overrun_s": end_overrun,
        "uncovered_sections": uncovered,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check caption cue coverage against timeline spoken sections. No writes."
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
    print(f"cue_count: {rep.get('cue_count')}")
    print(f"start_lag_s: {rep.get('start_lag_s') if rep.get('start_lag_s') is not None else 'n/a'}")
    print(f"end_overrun_s: {rep.get('end_overrun_s') if rep.get('end_overrun_s') is not None else 'n/a'}")
    print(f"uncovered_sections: {rep.get('uncovered_sections')}")
    print(f"consistency: {rep['code']} ({rep['detail']})")
    print("Does not execute encode, invent media, or poll OAuth.")
    return 0 if rep["code"] != "NO_DATA" else 2


if __name__ == "__main__":
    raise SystemExit(main())
