#!/usr/bin/env python3
"""Flag a repeated no-progress pattern. Does not fail the build by itself.

Runs 314-316 each added a Studio handoff note while OAuth stayed unpolled
and videos published stayed 0. Prose flags did not stop the next run.
This printer makes that pattern machine-visible.

idle_streak counts every newest STATE delta that still says OAuth was not
polled and videos published stay 0. A streak at or above the idle window is
suspicious: the same blocker is being restated without a publish.
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
PREUPLOAD_FLAG = "STALL_PREUPLOAD_PROBE"
RECOVERY_EDGE_FLAG = "STALL_RECOVERY_EDGE"
OPERATOR_CARD_FLAG = "STALL_OPERATOR_CARD"
WINDOW = 3
IDLE_WINDOW = 8
UPLOAD_EDGE_WINDOW = 4
PREUPLOAD_WINDOW = 4
RECOVERY_EDGE_WINDOW = 4
OPERATOR_CARD_WINDOW = 3
UPLOAD_EDGE_TOKENS = (
    "early-persist",
    "early persist",
    "early_persist",
    "resumable",
    "session_expired",
    "session hold",
)
# Runs 350-353 each added an export, media, or caption probe while videos
# published stayed 0. Do not match the bare "do not add another" lock unless
# the delta also names the tool that was wired.
PREUPLOAD_TOKENS = (
    "caption_gate",
    "media_qa",
    "export_probe",
    "export probe",
)
# Runs 368-378 each added a provider-state recovery edge while videos
# published stayed 0. A lock sentence is not a wired edge.
RECOVERY_EDGE_TOKENS = (
    "provider-upload-state",
    "persist_provider_state.py recover",
    "persist_provider_state.py push",
    "rejected-push recovery",
    "rejected push recovery",
)
RECOVERY_EDGE_NEGATIONS = (
    "do not add another recovery edge",
    "do not add another provider-state recovery edge",
    "no new recovery edge",
    "did not add a recovery edge",
)
# Runs 383-384 each extended operator_card.py while videos published stayed 0.
# A lock sentence is not a wired card extension.
OPERATOR_CARD_TOKENS = (
    "operator_card.py",
    "operator card",
)
OPERATOR_CARD_NEGATIONS = (
    "do not add a second card",
    "do not extend operator_card",
    "did not extend operator_card",
    "no new operator card",
)
# Lock sentences repeat these tokens. A "do not add" line is not a wired probe.
PREUPLOAD_NEGATIONS = (
    "do not add another export probe, media checker, or caption cue gate",
    "do not add another export probe",
    "do not add another export_probe",
    "do not add another media checker",
    "do not add another caption cue gate",
    "do not wire another pre-upload checker",
    "do not wire another export probe",
    "do not add another pre-upload checker",
)
UPLOAD_EDGE_NEGATIONS = (
    "do not add another location, session hold, or early-persist call",
    "do not add another location",
    "do not add another resumable",
    "do not add another session hold",
    "do not add another early-persist",
    "do not add another early persist",
    "do not add another early_persist",
    "do not add another upload-edge",
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


def _oauth_unpolled(delta: str) -> bool:
    return "OAuth secrets were not polled" in delta and "Videos published stay 0" in delta


def _oauth_stall(deltas: list[str]) -> bool:
    if len(deltas) < WINDOW:
        return False
    return all(_oauth_unpolled(delta) for delta in deltas)


def idle_streak(deltas: list[str]) -> int:
    """Newest-first count of OAuth-unpolled, unpublished deltas."""
    streak = 0
    for delta in deltas:
        if not _oauth_unpolled(delta):
            break
        streak += 1
    return streak


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
            scrubbed = lowered
            for phrase in UPLOAD_EDGE_NEGATIONS:
                scrubbed = scrubbed.replace(phrase, "")
            if not any(token in scrubbed for token in UPLOAD_EDGE_TOKENS):
                edge = False
                break
        if edge:
            flags.extend([
                UPLOAD_EDGE_FLAG,
                f"last_{UPLOAD_EDGE_WINDOW}_runs: oauth_unpolled_and_upload_edge",
                "do_not: add another resumable Location, session hold, or early-persist call while this flag is set",
                "next: wait for the three YouTube secrets, or fix a production tool that is not the uploader",
            ])
    # Runs 350-353 each wired a pre-upload probe while videos published stayed 0.
    # That is the credential stall, not a missing checker.
    probe_deltas = run_deltas(text)[:PREUPLOAD_WINDOW]
    if _oauth_stall(probe_deltas) and len(probe_deltas) >= PREUPLOAD_WINDOW:
        probe = True
        for delta in probe_deltas:
            lowered = delta.lower()
            scrubbed = lowered
            for phrase in PREUPLOAD_NEGATIONS:
                scrubbed = scrubbed.replace(phrase, "")
            if not any(token in scrubbed for token in PREUPLOAD_TOKENS):
                probe = False
                break
        if probe:
            flags.extend([
                PREUPLOAD_FLAG,
                f"last_{PREUPLOAD_WINDOW}_runs: oauth_unpolled_and_preupload_probe",
                "do_not: add another export probe, media checker, or caption cue gate while this flag is set",
                "next: wait for the three YouTube secrets; do not wire another pre-upload checker",
            ])
    # Runs 368-378 each added a rejected-push recovery edge while videos
    # published stayed 0. That is the credential stall, not a missing recover path.
    recovery_deltas = run_deltas(text)[:RECOVERY_EDGE_WINDOW]
    if _oauth_stall(recovery_deltas) and len(recovery_deltas) >= RECOVERY_EDGE_WINDOW:
        recovery = True
        for delta in recovery_deltas:
            lowered = delta.lower()
            scrubbed = lowered
            for phrase in RECOVERY_EDGE_NEGATIONS:
                scrubbed = scrubbed.replace(phrase, "")
            if not any(token in scrubbed for token in RECOVERY_EDGE_TOKENS):
                recovery = False
                break
        if recovery:
            flags.extend([
                RECOVERY_EDGE_FLAG,
                f"last_{RECOVERY_EDGE_WINDOW}_runs: oauth_unpolled_and_recovery_edge",
                "do_not: add another provider-state recovery edge while this flag is set",
                "next: wait for the three YouTube secrets; do not dispatch execute again to retry videos.insert",
            ])
            flags.append("suspicious: recovery_edge_without_publish")
    # Runs 383-384 each extended the operator card while videos published
    # stayed 0. That is the credential stall, not a missing console step.
    card_deltas = run_deltas(text)[:OPERATOR_CARD_WINDOW]
    if _oauth_stall(card_deltas) and len(card_deltas) >= OPERATOR_CARD_WINDOW:
        card = True
        for delta in card_deltas:
            lowered = delta.lower()
            scrubbed = lowered
            for phrase in OPERATOR_CARD_NEGATIONS:
                scrubbed = scrubbed.replace(phrase, "")
            if not any(token in scrubbed for token in OPERATOR_CARD_TOKENS):
                card = False
                break
        if card:
            flags.extend([
                OPERATOR_CARD_FLAG,
                f"last_{OPERATOR_CARD_WINDOW}_runs: oauth_unpolled_and_operator_card",
                "do_not: extend operator_card.py or add a second card while this flag is set",
                "next: wait for the three YouTube secrets; do not reprint the console steps again",
            ])
            flags.append("suspicious: operator_card_without_publish")
    # Count the whole file, not the 8-delta flag window. A cleared newest
    # delta resets the streak to 0. A zero streak is not a flag: callers
    # treat a non-empty list as a stall. This does not poll secrets.
    streak = idle_streak(run_deltas(text))
    if streak:
        flags.append(f"idle_streak: {streak}")
    if streak >= IDLE_WINDOW:
        flags.append("suspicious: oauth_idle_without_publish")
        flags.append(
            "suspicious_note: the same OAuth-absent unpublished state has repeated; do not treat another restatement as progress"
        )
    return flags


def main() -> int:
    text = STATE.read_text(encoding="utf-8") if STATE.is_file() else ""
    flags = flag_text(text)
    if flags == ["idle_streak: 0"] or not flags:
        print("STALL_WATCH")
        print("status: clear")
        print("idle_streak: 0")
        return 0
    print("STALL_WATCH")
    for line in flags:
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
