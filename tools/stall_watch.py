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
INSTRUCTION_FLAG = "STALL_INSTRUCTION_LOCK"
LOCAL_GATE_FLAG = "STALL_LOCAL_GATE"
WINDOW = 3
LOCAL_GATE_TOKENS = (
    "quality_scan",
    "claim_scan",
    "title_scan",
    "content_rules",
    "packet_path",
    "scanner",
)


def run_deltas(text: str) -> list[str]:
    parts = text.split("## Run ")
    deltas = []
    for part in parts[1:]:
        if "delta" not in part[:40]:
            continue
        deltas.append(part)
    return deltas


def _oauth_stall(deltas: list[str]) -> bool:
    if len(deltas) < WINDOW:
        return False
    for delta in deltas:
        if "OAuth secrets were not polled" not in delta:
            return False
        if "Videos published stay 0" not in delta:
            return False
    return True


def flag_text(text: str, window: int = WINDOW) -> list[str]:
    deltas = run_deltas(text)[:window]
    flags: list[str] = []
    if _oauth_stall(deltas):
        studio = True
        for delta in deltas:
            lowered = delta.lower()
            if "studio" not in lowered and "end screen" not in lowered and "end_screen" not in lowered:
                studio = False
                break
        if studio:
            flags.extend([
                FLAG,
                f"last_{window}_runs: oauth_unpolled_and_studio_handoff",
                "do_not: add another Studio URL or end-screen sentence while this flag is set",
                "next: bind an existing constant, or wait for the three YouTube secrets",
            ])
        instruction = True
        for delta in deltas:
            lowered = delta.lower()
            if not any(token in lowered for token in ("apply_idea", "fill-idea", "paste", "queue", "hint")):
                instruction = False
                break
            if "provider video id" in lowered or "videos.insert" in lowered:
                instruction = False
                break
        if instruction:
            flags.extend([
                INSTRUCTION_FLAG,
                f"last_{window}_runs: oauth_unpolled_and_instruction_lock",
                "do_not: add another paste, hint, or queue-column sentence while this flag is set",
                "next: run tools/quality_scan.py on a new script before ready_for_vo; do not rewrite Q1 WORDS",
            ])
        local_gate = True
        for delta in deltas:
            lowered = delta.lower()
            if not any(token in lowered for token in LOCAL_GATE_TOKENS):
                local_gate = False
                break
            if "provider video id" in lowered or "videos.insert" in lowered:
                local_gate = False
                break
        if local_gate:
            flags.extend([
                LOCAL_GATE_FLAG,
                f"last_{window}_runs: oauth_unpolled_and_local_gate",
                "do_not: add another scanner, packet path gate, or content-rule refusal while this flag is set",
                "next: add the three YouTube secrets, then dispatch execute=true; do not scaffold Q2",
            ])
    return flags


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
