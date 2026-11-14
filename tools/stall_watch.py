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

import re
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
LOG_HYGIENE_FLAG = "STALL_LOG_HYGIENE"
BANNER_REFRESH_FLAG = "STALL_BANNER_REFRESH"
GATE_CONFIRM_FLAG = "STALL_GATE_CONFIRM"
READINESS_AGG_FLAG = "STALL_READINESS_AGGREGATOR"
WINDOW = 3
IDLE_WINDOW = 8
UPLOAD_EDGE_WINDOW = 4
PREUPLOAD_WINDOW = 4
RECOVERY_EDGE_WINDOW = 4
OPERATOR_CARD_WINDOW = 3
LOG_HYGIENE_WINDOW = 3
BANNER_WINDOW = 4
GATE_CONFIRM_WINDOW = 4
READINESS_AGG_WINDOW = 4
CONSISTENCY_PRINTER_FLAG = "STALL_CONSISTENCY_PRINTER"
CONSISTENCY_PRINTER_WINDOW = 4

CONSISTENCY_PRINTER_TOKENS = (
    "consistency.py",
    "tags_hygiene.py",
    "_consistency",
    "tags_hygiene",
)
CONSISTENCY_PRINTER_NEGATIONS = (
    "do not add another consistency",
    "do not add another tags_hygiene",
    "did not add a consistency printer",
    "no new consistency printer",
    "saturation risk",
)


def run_deltas(text: str) -> list[str]:
    """Extract delta bodies from newest to oldest.

    Supports both the older "## Run N delta" headers and the current
    "YYYY-MM-DDTHH:MM:SSZ (Run N)" timestamped blocks used in STATE.md.
    """
    if not text:
        return []
    # Prefer the live timestamped format; fall back to the ## Run delta form.
    if re.search(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z \(Run \d+\)", text):
        parts = re.split(r"(?=\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z \(Run \d+\))", text)
        deltas = []
        for part in parts:
            part = part.strip()
            if re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z \(Run \d+\)", part):
                # drop the timestamp header line
                body = re.sub(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z \(Run \d+\)\s*", "", part, count=1).strip()
                if body:
                    deltas.append(body)
        return deltas  # newest first as written
    # Legacy path used by the contract fixtures
    parts = re.split(r"(?=## Run \d+ delta)", text)
    deltas = []
    for part in parts:
        part = part.strip()
        if part.startswith("## Run"):
            body = re.sub(r"^## Run \d+ delta\s*", "", part, count=1).strip()
            if body:
                deltas.append(body)
    return deltas


def is_idle_delta(body: str) -> bool:
    low = body.lower()
    no_poll = (
        "oauth secrets were not polled" in low
        or "no secrets polled" in low
        or "oauth was not polled" in low
        or "oauth not polled" in low
        or "do not poll secrets" in low
        or "do not poll" in low and "secret" in low
        or "secrets absent" in low
        or "no poll" in low
        or "stall_oauth_idle" in low
    )
    published_zero = (
        "videos published stay 0" in low
        or "published=0" in low
        or "published stay 0" in low
        or "videos published: 0" in low
        or "videos_published: 0" in low
        or "published stay 0" in low
        or "videos published stay 0" in low
        or "1000+ runs" in low
        or "stall_oauth_idle" in low
        or "published: 0" in low
    )
    return (
        no_poll
        and published_zero
        and "videos published stay 1" not in low
        and "oauth secrets were present" not in low
        and "secrets present" not in low
        and "published=1" not in low
    )


def idle_streak(deltas: list[str]) -> int:
    """Count consecutive newest idle deltas."""
    streak = 0
    for body in deltas:  # newest first
        if is_idle_delta(body):
            streak += 1
        else:
            break
    return streak


def _window_matches(deltas: list[str], window: int, predicates) -> bool:
    if len(deltas) < window:
        return False
    recent = deltas[:window]
    return all(pred(b) for b, pred in zip(recent, predicates)) if len(predicates) == window else all(predicates[0](b) for b in recent)


def flag_text(text: str) -> list[str]:
    deltas = run_deltas(text)
    streak = idle_streak(deltas)
    flags: list[str] = []
    if streak > 0:
        flags.append(f"idle_streak: {streak}")
    if streak >= IDLE_WINDOW:
        flags.append(IDLE_FLAG)
        flags.append("suspicious: oauth_idle_without_publish")

    # Studio pattern: 3 deltas with studio/end screen
    if len(deltas) >= WINDOW and all("studio" in d.lower() or "end screen" in d.lower() for d in deltas[:WINDOW]):
        if not any("do not" in d.lower() and "studio" in d.lower() for d in deltas[:WINDOW]):
            flags.append(FLAG)

    # Instruction lock: fill-idea / paste idea.md
    if len(deltas) >= WINDOW and all(
        ("fill-idea" in d.lower() or "paste idea.md" in d.lower() or "queue hint" in d.lower())
        for d in deltas[:WINDOW]
    ):
        flags.append(INSTRUCTION_FLAG)

    # Local gate: quality_scan / claim_scan / title_scan
    if len(deltas) >= WINDOW and all(
        any(tok in d.lower() for tok in ("quality_scan", "claim_scan", "title_scan"))
        for d in deltas[:WINDOW]
    ) and not any("no new scanner" in d.lower() for d in deltas[:WINDOW]):
        flags.append(LOCAL_GATE_FLAG)

    # Upload edge
    if len(deltas) >= UPLOAD_EDGE_WINDOW and all(
        "early-persist" in d.lower() or "resumable location" in d.lower()
        for d in deltas[:UPLOAD_EDGE_WINDOW]
    ) and not any("do not add another" in d.lower() for d in deltas[:UPLOAD_EDGE_WINDOW]):
        flags.append(UPLOAD_EDGE_FLAG)

    # Preupload probe
    if len(deltas) >= PREUPLOAD_WINDOW and all(
        any(tok in d.lower() for tok in ("export_probe.py", "caption_gate.py", "media_qa"))
        for d in deltas[:PREUPLOAD_WINDOW]
    ) and not any("do not add another" in d.lower() for d in deltas[:PREUPLOAD_WINDOW]):
        flags.append(PREUPLOAD_FLAG)

    # Recovery edge
    if len(deltas) >= RECOVERY_EDGE_WINDOW and all(
        "persist_provider_state.py recover" in d.lower() or "rejected-push recovery" in d.lower()
        for d in deltas[:RECOVERY_EDGE_WINDOW]
    ) and not any("do not add another recovery" in d.lower() for d in deltas[:RECOVERY_EDGE_WINDOW]):
        flags.append(RECOVERY_EDGE_FLAG)
        flags.append("suspicious: recovery_edge_without_publish")

    # Operator card
    if len(deltas) >= OPERATOR_CARD_WINDOW and all(
        "operator_card.py" in d.lower()
        for d in deltas[:OPERATOR_CARD_WINDOW]
    ) and not any("do not extend operator_card" in d.lower() for d in deltas[:OPERATOR_CARD_WINDOW]):
        flags.append(OPERATOR_CARD_FLAG)
        flags.append("suspicious: operator_card_without_publish")

    # Log hygiene
    if len(deltas) >= LOG_HYGIENE_WINDOW and all(
        "compact_all.py" in d.lower() or "archive pointer" in d.lower()
        for d in deltas[:LOG_HYGIENE_WINDOW]
    ) and not any("do not add another compact" in d.lower() for d in deltas[:LOG_HYGIENE_WINDOW]):
        flags.append(LOG_HYGIENE_FLAG)
        flags.append("suspicious: log_hygiene_without_publish")

    # Consistency printer (bonus)
    if len(deltas) >= CONSISTENCY_PRINTER_WINDOW and all(
        any(tok in d.lower() for tok in CONSISTENCY_PRINTER_TOKENS)
        for d in deltas[:CONSISTENCY_PRINTER_WINDOW]
    ) and not any(neg in d.lower() for d in deltas[:CONSISTENCY_PRINTER_WINDOW] for neg in CONSISTENCY_PRINTER_NEGATIONS):
        flags.append(CONSISTENCY_PRINTER_FLAG)

    return flags


def main() -> int:
    text = STATE.read_text(encoding="utf-8") if STATE.is_file() else ""
    for line in flag_text(text):
        print(line)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
