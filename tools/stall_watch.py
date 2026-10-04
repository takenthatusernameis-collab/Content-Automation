#!/usr/bin/env python3
"""Flag a repeated no-progress pattern. Does not fail the build by itself.

Runs 314-316 each added a Studio handoff note while OAuth stayed unpolled
and videos published stayed 0. Prose flags did not stop the next run.
This printer makes that pattern machine-visible.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STATE = ROOT / "STATE.md"
FLAG = "STALL_OAUTH_AND_STUDIO"
WINDOW = 3


def run_deltas(text: str) -> list[str]:
    parts = text.split("## Run ")
    deltas = []
    for part in parts[1:]:
        if "delta" not in part[:40]:
            continue
        deltas.append(part)
    return deltas


def flag_text(text: str, window: int = WINDOW) -> list[str]:
    deltas = run_deltas(text)[:window]
    if len(deltas) < window:
        return []
    for delta in deltas:
        if "OAuth secrets were not polled" not in delta:
            return []
        if "Videos published stay 0" not in delta:
            return []
        lowered = delta.lower()
        if "studio" not in lowered and "end screen" not in lowered and "end_screen" not in lowered:
            return []
    return [
        FLAG,
        f"last_{window}_runs: oauth_unpolled_and_studio_handoff",
        "do_not: add another Studio URL or end-screen sentence while this flag is set",
        "next: bind an existing constant, or wait for the three YouTube secrets",
    ]


def main() -> int:
    text = STATE.read_text(encoding="utf-8") if STATE.is_file() else ""
    flags = flag_text(text)
    if not flags:
        print("STALL_WATCH")
        print("status: clear")
        return 0
    print("STALL_WATCH")
    for line in flags:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
