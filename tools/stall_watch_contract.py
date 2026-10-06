#!/usr/bin/env python3
"""Lock stall_watch flags. Does not poll OAuth or fail the build by itself."""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from stall_watch import FLAG, IDLE_FLAG, INSTRUCTION_FLAG, LOCAL_GATE_FLAG, PREUPLOAD_FLAG, UPLOAD_EDGE_FLAG, flag_text  # noqa: E402


def delta(body: str) -> str:
    return f"## Run 1 delta\n{body}\n"


def fail(msg: str) -> int:
    print("STALL WATCH CONTRACT FAIL")
    print(msg)
    return 1


def main() -> int:
    studio = delta(
        "OAuth secrets were not polled. Videos published stay 0. Added a Studio URL and end screen sentence."
    ) * 3
    flags = flag_text(studio)
    if FLAG not in flags or INSTRUCTION_FLAG in flags:
        return fail(f"studio window wrong: {flags}")
    instruction = delta(
        "OAuth secrets were not polled. Videos published stay 0. fill-idea still said paste idea.md. queue hint only."
    ) * 3
    flags = flag_text(instruction)
    if INSTRUCTION_FLAG not in flags or FLAG in flags:
        return fail(f"instruction window wrong: {flags}")
    mixed = delta("OAuth secrets were not polled. Videos published stay 0. quality_scan only. No instruction sentence.")
    mixed += delta("OAuth secrets were not polled. Videos published stay 0. fill-idea paste hint.")
    mixed += delta("OAuth secrets were not polled. Videos published stay 0. queue column.")
    flags = flag_text(mixed)
    if flags:
        return fail(f"mixed window must be clear: {flags}")
    local_gate = delta(
        "OAuth secrets were not polled. Videos published stay 0. quality_scan contract only. No provider write."
    )
    local_gate += delta(
        "OAuth secrets were not polled. Videos published stay 0. claim_scan hits. No provider write."
    )
    local_gate += delta(
        "OAuth secrets were not polled. Videos published stay 0. title_scan content_rules. No provider write."
    )
    flags = flag_text(local_gate)
    if LOCAL_GATE_FLAG not in flags or FLAG in flags or INSTRUCTION_FLAG in flags:
        return fail(f"local gate window wrong: {flags}")
    negated = delta(
        "OAuth secrets were not polled. Videos published stay 0. No new scanner. No provider write."
    ) * 3
    flags = flag_text(negated)
    if LOCAL_GATE_FLAG in flags or FLAG in flags or INSTRUCTION_FLAG in flags:
        return fail(f"negated scanner boilerplate must not set local gate: {flags}")
    idle = delta(
        "OAuth secrets were not polled. Videos published stay 0. No new provider write."
    ) * 8
    flags = flag_text(idle)
    if IDLE_FLAG not in flags:
        return fail(f"idle window missing: {flags}")
    edge = delta(
        "OAuth secrets were not polled. Videos published stay 0. Early-persist the resumable Location."
    ) * 4
    flags = flag_text(edge)
    if UPLOAD_EDGE_FLAG not in flags:
        return fail(f"upload edge window missing: {flags}")
    short_edge = delta(
        "OAuth secrets were not polled. Videos published stay 0. Early-persist the resumable Location."
    ) * 3
    if UPLOAD_EDGE_FLAG in flag_text(short_edge):
        return fail("three upload-edge deltas must not set the flag")
    broken = edge + delta(
        "OAuth secrets were not polled. Videos published stay 0. Fixed assemble only. No provider write."
    )
    # Newest delta is first in the file, so prepend the non-edge run.
    broken = delta(
        "OAuth secrets were not polled. Videos published stay 0. Fixed assemble only. No provider write."
    ) + edge
    if UPLOAD_EDGE_FLAG in flag_text(broken):
        return fail("a non-edge newest delta must clear the upload-edge flag")
    if flag_text(delta("OAuth secrets were not polled. Videos published stay 0. topic switch.") * 3):
        return fail("three idle deltas must stay clear")
    probe = delta(
        "OAuth secrets were not polled. Videos published stay 0. tools/export_probe.py wired. No provider write."
    ) * 4
    flags = flag_text(probe)
    if PREUPLOAD_FLAG not in flags:
        return fail(f"preupload probe window missing: {flags}")
    short_probe = delta(
        "OAuth secrets were not polled. Videos published stay 0. tools/caption_gate.py wired. No provider write."
    ) * 3
    if PREUPLOAD_FLAG in flag_text(short_probe):
        return fail("three preupload deltas must not set the flag")
    cleared = delta(
        "OAuth secrets were not polled. Videos published stay 0. Fixed assemble only. No provider write."
    ) + probe
    if PREUPLOAD_FLAG in flag_text(cleared):
        return fail("a non-probe newest delta must clear the preupload flag")
    lock_only = delta(
        "OAuth secrets were not polled. Videos published stay 0. Do not add another export probe, media checker, or caption cue gate."
    ) * 4
    if PREUPLOAD_FLAG in flag_text(lock_only):
        return fail("preupload lock boilerplate must not set the flag")
    edge_lock = delta(
        "OAuth secrets were not polled. Videos published stay 0. Do not add another Location, session hold, or early-persist call."
    ) * 4
    if UPLOAD_EDGE_FLAG in flag_text(edge_lock):
        return fail("upload-edge lock boilerplate must not set the flag")
    print("STALL WATCH CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
