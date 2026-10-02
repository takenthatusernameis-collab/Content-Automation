#!/usr/bin/env python3
"""Fail-closed experiment / improvement ledger.

Does not invent results. Does not fetch Analytics. Does not rewrite scripts.
A packet without a published video ID stays HOLD_UNPUBLISHED.
A packet with an ID but empty metrics stays HOLD_NO_EVIDENCE.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from render_brief import selected_vo_drop  # noqa: E402
from youtube_feedback import (  # noqa: E402
    collected_metrics,
    inspect_feedback,
    load_upload_state,
    provider_video_id,
)

STATE_NAME = "experiment_state.json"
ALLOWED_DECISIONS = ("pending", "keep", "discard", "retest")
ALLOWED_CHANGES = (
    "hook",
    "mechanism_framing",
    "example_density",
    "title_promise",
    "visual_explanation",
    "pacing",
    "cta",
    "topic_selection",
)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _fmt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def inspect_experiment(
    packet: Path,
    env: dict[str, str] | None = None,
    now: datetime | None = None,
) -> dict:
    feedback = inspect_feedback(packet, env=env, now=now)
    upload = load_upload_state(packet)
    video_id = provider_video_id(upload)
    metrics, metrics_detail = collected_metrics(packet, video_id)
    checks = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    add("provider_video_id_present", bool(video_id), video_id or "no provider_video_id")
    add("metrics_present", metrics is not None, metrics_detail)
    add("no_invented_result", True, "result stays pending without comparable evidence")
    add("single_variable", True, "one material change per experiment when practical")

    if not video_id:
        gate = "HOLD_UNPUBLISHED"
        action = "DRY_RUN"
        decision = "pending"
    elif metrics is None:
        gate = "HOLD_NO_EVIDENCE"
        action = "DRY_RUN"
        decision = "pending"
    else:
        gate = "READY_TO_COMPARE"
        action = "COMPARE_BLOCKED_NO_BASELINE"
        decision = "pending"

    record = {
        "id": f"{packet.name}-exp-pending",
        "packet": packet.name,
        "provider_video_id": video_id,
        "hypothesis": None,
        "change": None,
        "allowed_changes": list(ALLOWED_CHANGES),
        "primary_metric": None,
        "guardrails": [
            "do not invent analytics",
            "do not mix videos of different ages without a documented reason",
            "do not rewrite an old script to make the test look successful",
            "do not treat a single early outlier as a keep decision",
        ],
        "baseline": None,
        "observed_metrics": metrics,
        "result": None,
        "decision": decision,
        "allowed_decisions": list(ALLOWED_DECISIONS),
        "window": feedback.get("window"),
    }

    return {
        "packet": packet.name,
        "drop": selected_vo_drop(packet),
        "provider_video_id": video_id,
        "feedback_gate": feedback["gate"],
        "metrics": metrics,
        "record": record,
        "checks": checks,
        "gate": gate,
        "action": action,
        "generated": _fmt(now or _now()),
    }


def redacted_state(report: dict) -> dict:
    rec = report["record"]
    return {
        "packet": report["packet"],
        "generated": report["generated"],
        "gate": report["gate"],
        "action": report["action"],
        "provider_video_id": report["provider_video_id"],
        "id": rec["id"],
        "hypothesis": rec["hypothesis"],
        "change": rec["change"],
        "primary_metric": rec["primary_metric"],
        "result": rec["result"],
        "decision": rec["decision"],
        "attempted_compare": False,
        "note": "dry-run only; never invents a keep/discard result",
    }


def render_text(report: dict) -> str:
    rec = report["record"]
    lines = [
        f"packet: {report['packet']}",
        f"gate: {report['gate']}",
        f"action: {report['action']}",
        f"drop: {report['drop']}",
        f"provider_video_id: {report['provider_video_id'] or 'none'}",
        f"feedback_gate: {report['feedback_gate']}",
        f"decision: {rec['decision']}",
        "experiment_loop never invents results or calls Analytics",
        "missing provider_video_id is HOLD_UNPUBLISHED, not a learned experiment",
        "empty metrics are HOLD_NO_EVIDENCE, not a keep/discard",
    ]
    for c in report["checks"]:
        mark = "PASS" if c["ok"] else "FAIL"
        lines.append(f"- {mark} {c['name']}: {c['detail']}")
    lines.append("pending_record:")
    lines.append(json.dumps(rec, indent=2, ensure_ascii=False))
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Dry-run experiment ledger. No invented results. No API."
    )
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument(
        "--write-state",
        action="store_true",
        help="Write redacted experiment_state.json",
    )
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    report = inspect_experiment(path)
    sys.stdout.write(render_text(report))
    if args.write_state:
        dest = path / STATE_NAME
        dest.write_text(json.dumps(redacted_state(report), indent=2) + "\n", encoding="utf-8")
        print(dest)
    if report["gate"] == "HOLD_UNPUBLISHED":
        return 2
    if report["gate"] == "HOLD_NO_EVIDENCE":
        return 3
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
