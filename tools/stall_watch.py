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
IDLE_FLAG = "STALL_OAUTH_IDLE"
UPLOAD_EDGE_FLAG = "STALL_UPLOAD_EDGE"
WINDOW = 3
IDLE_WINDOW = 8
UPLOAD_EDGE_WINDOW = 4
UPLOAD_EDGE_TOKENS = (
    "early-persist",
    "early persist",
    "early_persist",
    "resumable",
    "session_expired",
    "session hold",
)
LOCAL_GATE_TOKENS = (
    "quality_scan",
    "claim_scan",
    "title_scan",
    "content_rules",
    "packet_path",
)
# Bare "scanner" matched the boilerplate "No new scanner" and kept
# STALL_LOCAL_GATE set after the subject had already changed.
LOCAL_GATE_NEGATIONS = (
    "no new scanner",
    "no scanner",
    "not a new scanner",
    "not a scanner",
    "no new quality_scan",
    "no new claim_scan",
    "no new title_scan",
    "no new packet_path",
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
            scrubbed = lowered
            for phrase in LOCAL_GATE_NEGATIONS:
                scrubbed = scrubbed.replace(phrase, "")
            if not any(token in scrubbed for token in LOCAL_GATE_TOKENS):
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
    # A 3-run topic window clears when the next run switches subject.
    # Runs 314-331 stayed OAuth-unpolled with videos published at 0 anyway.
    idle_deltas = run_deltas(text)[:IDLE_WINDOW]
    if _oauth_stall(idle_deltas) and len(idle_deltas) >= IDLE_WINDOW:
        flags.extend([
            IDLE_FLAG,
            f"last_{IDLE_WINDOW}_runs: oauth_unpolled_videos_published_0",
            "do_not: add another scanner, Studio sentence, or playlist variant while this flag is set",
            "do_not: spend the run only restating the missing YouTube secrets",
            "next: a live execute result, or a fix for an existing tool that already runs on the production job",
        ])
    # Runs 344-348 each patched resumable/early-persist edges while videos
    # published stayed 0. That is the credential stall, not a missing session branch.
    edge_deltas = run_deltas(text)[:UPLOAD_EDGE_WINDOW]
    if _oauth_stall(edge_deltas) and len(edge_deltas) >= UPLOAD_EDGE_WINDOW:
        edge = True
        for delta in edge_deltas:
            lowered = delta.lower()
            if not any(token in lowered for token in UPLOAD_EDGE_TOKENS):
                edge = False
                break
        if edge:
            flags.extend([
                UPLOAD_EDGE_FLAG,
                f"last_{UPLOAD_EDGE_WINDOW}_runs: oauth_unpolled_and_upload_edge",
                "do_not: add another resumable Location, session hold, or early-persist call while this flag is set",
                "next: wait for the three YouTube secrets, or fix a production tool that is not the uploader",
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
