#!/usr/bin/env python3
"""Lock stall_watch flags. Does not poll OAuth or fail the build by itself."""

from __future__ import annotations

import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from stall_watch import (
    FLAG,
    IDLE_FLAG,
    INSTRUCTION_FLAG,
    LOCAL_GATE_FLAG,
    PREUPLOAD_FLAG,
    LOG_HYGIENE_FLAG,
    OPERATOR_CARD_FLAG,
    RECOVERY_EDGE_FLAG,
    UPLOAD_EDGE_FLAG,
    flag_text,
    idle_streak,
    run_deltas,
)


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
    if flags != ["idle_streak: 3"]:
        return fail(f"mixed window must be streak only: {flags}")
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
    if "idle_streak: 8" not in flags or "suspicious: oauth_idle_without_publish" not in flags:
        return fail(f"idle streak missing: {flags}")
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
    broken = delta(
        "OAuth secrets were not polled. Videos published stay 0. Fixed assemble only. No provider write."
    ) + edge
    if UPLOAD_EDGE_FLAG in flag_text(broken):
        return fail("a non-edge newest delta must clear the upload-edge flag")
    three = flag_text(delta("OAuth secrets were not polled. Videos published stay 0. topic switch.") * 3)
    if three != ["idle_streak: 3"]:
        return fail(f"three idle deltas must stay clear except streak: {three}")
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
    recovery = delta(
        "OAuth secrets were not polled. Videos published stay 0. persist_provider_state.py recover wrote provider-upload-state. No provider write."
    ) * 4
    flags = flag_text(recovery)
    if RECOVERY_EDGE_FLAG not in flags:
        return fail(f"recovery edge window missing: {flags}")
    if "suspicious: recovery_edge_without_publish" not in flags:
        return fail("recovery edge window must name the suspicious pattern")
    short_recovery = delta(
        "OAuth secrets were not polled. Videos published stay 0. rejected-push recovery. No provider write."
    ) * 3
    if RECOVERY_EDGE_FLAG in flag_text(short_recovery):
        return fail("three recovery deltas must not set the flag")
    cleared = delta(
        "OAuth secrets were not polled. Videos published stay 0. Compacted logs only. No provider write."
    ) + recovery
    if RECOVERY_EDGE_FLAG in flag_text(cleared):
        return fail("a non-recovery newest delta must clear the recovery flag")
    recovery_lock = delta(
        "OAuth secrets were not polled. Videos published stay 0. Do not add another recovery edge. No new recovery edge."
    ) * 4
    if RECOVERY_EDGE_FLAG in flag_text(recovery_lock):
        return fail("recovery lock boilerplate must not set the flag")
    card = delta(
        "OAuth secrets were not polled. Videos published stay 0. operator_card.py reprints console steps. No provider write."
    ) * 3
    flags = flag_text(card)
    if OPERATOR_CARD_FLAG not in flags:
        return fail(f"operator card window missing: {flags}")
    if "suspicious: operator_card_without_publish" not in flags:
        return fail("operator card window must name the suspicious pattern")
    card_lock = delta(
        "OAuth secrets were not polled. Videos published stay 0. Do not extend operator_card. No new operator card."
    ) * 3
    if OPERATOR_CARD_FLAG in flag_text(card_lock):
        return fail("operator card lock boilerplate must not set the flag")
    one_card = delta(
        "OAuth secrets were not polled. Videos published stay 0. operator_card.py reprints console steps. No provider write."
    )
    if OPERATOR_CARD_FLAG in flag_text(one_card):
        return fail("one operator card delta must not set the flag")
    hygiene = delta(
        "OAuth secrets were not polled. Videos published stay 0. compact_all.py --check now reads the archive pointer. No provider write."
    ) * 3
    flags = flag_text(hygiene)
    if LOG_HYGIENE_FLAG not in flags:
        return fail(f"log hygiene window missing: {flags}")
    if "suspicious: log_hygiene_without_publish" not in flags:
        return fail("log hygiene window must name the suspicious pattern")
    short_hygiene = delta(
        "OAuth secrets were not polled. Videos published stay 0. record_run.py refreshed the header. No provider write."
    ) * 2
    if LOG_HYGIENE_FLAG in flag_text(short_hygiene):
        return fail("two log hygiene deltas must not set the flag")
    hygiene_lock = delta(
        "OAuth secrets were not polled. Videos published stay 0. Do not add another compact check. Did not add a compact check."
    ) * 3
    if LOG_HYGIENE_FLAG in flag_text(hygiene_lock):
        return fail("log hygiene lock boilerplate must not set the flag")
    edge_lock = delta(
        "OAuth secrets were not polled. Videos published stay 0. Do not add another Location, session hold, or early-persist call."
    ) * 4
    if UPLOAD_EDGE_FLAG in flag_text(edge_lock):
        return fail("upload-edge lock boilerplate must not set the flag")
    published = delta("OAuth secrets were present. Videos published stay 1.") + idle
    flags = flag_text(published)
    if any(line.startswith("idle_streak:") for line in flags):
        return fail(f"a published newest delta must reset the streak to empty: {flags}")
    if idle_streak(run_deltas(published)) != 0:
        return fail("a published newest delta must reset idle_streak() to 0")
    if "suspicious: oauth_idle_without_publish" in flags:
        return fail("a published newest delta must clear suspicious")
    if IDLE_FLAG in flags:
        return fail("a published newest delta must clear idle flag")
    if idle_streak([]) != 0:
        return fail("empty streak must be 0")
    print("STALL WATCH CONTRACT PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
