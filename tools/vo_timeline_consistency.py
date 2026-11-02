#!/usr/bin/env python3
"""Compare timeline spoken estimate to actual Selected VO duration.

Read-only. Stdlib only. Does not invent media, run ffmpeg, poll secrets, or bump status.
Useful for spotting large timing mismatches before assembly on future packets.
"""

from __future__ import annotations

import argparse
import sys
import wave
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from timeline import plan  # noqa: E402


def actual_vo_seconds(packet: Path) -> float | None:
    """Return duration of the first *take-selected.wav under vo/, or None."""
    vo_dir = packet / "vo"
    if not vo_dir.is_dir():
        return None
    found = sorted(vo_dir.glob("*take-selected.wav"))
    if not found:
        return None
    try:
        with wave.open(str(found[0]), "rb") as wf:
            rate = wf.getframerate()
            if rate <= 0:
                return None
            return round(wf.getnframes() / float(rate), 2)
    except (wave.Error, OSError):
        return None


def inspect(packet: Path) -> dict:
    data = plan(packet)
    spoken = float(data.get("spoken") or 0.0)
    actual = actual_vo_seconds(packet)
    if actual is None or spoken <= 0:
        return {
            "ok": False,
            "code": "NO_DATA",
            "spoken_s": spoken,
            "actual_s": actual,
            "diff_s": None,
            "pct": None,
            "detail": "missing VO or zero spoken estimate",
        }
    diff = round(actual - spoken, 2)
    pct = round(100.0 * diff / spoken, 1) if spoken else 0.0
    # Soft thresholds: >15% or >8s absolute is a warning worth a human glance
    warn = abs(pct) > 15.0 or abs(diff) > 8.0
    return {
        "ok": not warn,
        "code": "WARN" if warn else "OK",
        "spoken_s": spoken,
        "actual_s": actual,
        "diff_s": diff,
        "pct": pct,
        "detail": f"{diff:+.2f}s ({pct:+.1f}%)",
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Compare timeline spoken estimate vs actual Selected VO duration. No writes."
    )
    parser.add_argument("packet", help="Path to packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    rep = inspect(path)
    print(f"packet: {path.name}")
    print(f"spoken_estimate_s: {rep['spoken_s']}")
    print(f"actual_vo_s: {rep['actual_s'] if rep['actual_s'] is not None else 'n/a'}")
    print(f"diff_s: {rep['diff_s'] if rep['diff_s'] is not None else 'n/a'}")
    print(f"pct: {rep['pct'] if rep['pct'] is not None else 'n/a'}")
    print(f"consistency: {rep['code']} ({rep['detail']})")
    print("Does not execute encode, invent media, or poll OAuth.")
    return 0 if rep["code"] != "NO_DATA" else 2


if __name__ == "__main__":
    raise SystemExit(main())
