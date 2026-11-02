#!/usr/bin/env python3
"""Read-only caption speed / readability report for a packet's captions.srt.

Parses cues the same way caption_gate does. Reports characters-per-second (CPS)
per cue, overall stats, and flags cues that are likely too fast (>21 cps) or
too slow (<8 cps) for comfortable reading. Does not rewrite captions, does not
call YouTube, does not encode, does not invent media, does not poll secrets.

Exit 0 when the file is parseable (even if some cues are flagged). Exit 2 if
captions.srt is absent. Exit 1 only on unparseable content.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

FAST_CPS = 21.0
SLOW_CPS = 8.0
CUE_RE = re.compile(
    r"(\d+)\s*\n(\d{2}:\d{2}:\d{2},\d{3}) --> (\d{2}:\d{2}:\d{2},\d{3})\s*\n(.*?)(?=\n\n|\Z)",
    re.S,
)


def _seconds(stamp: str) -> float:
    h, m, rest = stamp.split(":")
    s, ms = rest.split(",")
    return int(h) * 3600 + int(m) * 60 + int(s) + int(ms) / 1000.0


def inspect_speed(packet: Path) -> dict:
    path = packet / "captions.srt"
    if not path.is_file():
        return {"ok": False, "code": "CAPTIONS_ABSENT", "detail": str(path), "cues": 0, "flagged": []}
    text = path.read_text(encoding="utf-8")
    cues = []
    for match in CUE_RE.finditer(text.strip() + "\n"):
        body = match.group(4).strip("\n")
        lines = [line.strip() for line in body.splitlines() if line.strip()]
        chars = sum(len(line) for line in lines)
        start = _seconds(match.group(2))
        end = _seconds(match.group(3))
        dur = max(0.001, end - start)
        cps = chars / dur
        cues.append(
            {
                "index": int(match.group(1)),
                "start": start,
                "end": end,
                "chars": chars,
                "dur": round(dur, 3),
                "cps": round(cps, 1),
                "lines": lines,
            }
        )
    if not cues:
        return {"ok": False, "code": "CAPTIONS_UNPARSEABLE", "detail": path.name, "cues": 0, "flagged": []}

    flagged = []
    for c in cues:
        reasons = []
        if c["cps"] > FAST_CPS:
            reasons.append(f"fast {c['cps']}cps")
        if c["cps"] < SLOW_CPS and c["dur"] > 1.5:
            reasons.append(f"slow {c['cps']}cps")
        if reasons:
            flagged.append({**c, "reasons": reasons})

    cps_values = [c["cps"] for c in cues]
    avg_cps = round(sum(cps_values) / len(cps_values), 1) if cps_values else 0.0
    max_cps = round(max(cps_values), 1) if cps_values else 0.0
    min_cps = round(min(cps_values), 1) if cps_values else 0.0

    return {
        "ok": True,
        "code": "REPORT",
        "detail": f"{len(cues)} cues, avg {avg_cps}cps, max {max_cps}, min {min_cps}, flagged {len(flagged)}",
        "cues": len(cues),
        "avg_cps": avg_cps,
        "max_cps": max_cps,
        "min_cps": min_cps,
        "flagged": flagged,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Read-only caption speed report (CPS). Does not rewrite or upload."
    )
    parser.add_argument("packet", type=Path)
    args = parser.parse_args()
    report = inspect_speed(args.packet)
    print("CAPTION_SPEED_REPORT")
    print(f"code: {report['code']}")
    print(f"detail: {report['detail']}")
    print(f"cues: {report['cues']}")
    if report.get("avg_cps") is not None:
        print(f"avg_cps: {report['avg_cps']}")
        print(f"max_cps: {report['max_cps']}")
        print(f"min_cps: {report['min_cps']}")
    if report["flagged"]:
        print("flagged_cues:")
        for f in report["flagged"][:20]:  # cap output
            preview = " | ".join(f["lines"])[:60]
            print(f"  cue {f['index']}: {', '.join(f['reasons'])}  '{preview}'")
        if len(report["flagged"]) > 20:
            print(f"  ... and {len(report['flagged']) - 20} more")
    else:
        print("flagged_cues: none")
    print("Does not rewrite captions, does not call YouTube, does not invent media.")
    if not report["ok"]:
        if report["code"] == "CAPTIONS_ABSENT":
            return 2
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
