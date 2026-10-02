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
BASELINE_NAME = "experiment_baseline.json"
DECISION_NAME = "experiment_decision.json"
ALLOWED_DECISIONS = ("pending", "keep", "discard", "retest")
RECORDED_DECISIONS = ("keep", "discard", "retest")
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
REJECTED_SOURCES = {"invented", "assumed", "placeholder", "guess"}


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _fmt(dt: datetime) -> str:
    return dt.strftime("%Y-%m-%dT%H:%M:%SZ")


def load_baseline(packet: Path) -> tuple[dict | None, str]:
    """Read a human- or prior-run-authored baseline. Never invent one."""
    path = packet / BASELINE_NAME
    if not path.is_file():
        return None, "no experiment_baseline.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None, "experiment_baseline.json is not json"
    if not isinstance(data, dict):
        return None, "experiment_baseline.json must be an object"
    hypothesis = str(data.get("hypothesis") or "").strip()
    change = str(data.get("change") or "").strip()
    metric = str(data.get("primary_metric") or "").strip()
    source = str(data.get("source") or "").strip()
    baseline = data.get("baseline")
    if not hypothesis or not metric or not source:
        return None, "baseline missing hypothesis, primary_metric, or source"
    if change not in ALLOWED_CHANGES:
        return None, f"baseline change {change!r} is not an allowed single variable"
    if source.lower() in REJECTED_SOURCES:
        return None, "baseline source must be a documented observation, not invented"
    if baseline is None or baseline == "":
        return None, "baseline value missing"
    return {
        "hypothesis": hypothesis,
        "change": change,
        "primary_metric": metric,
        "baseline": baseline,
        "source": source,
    }, "documented baseline loaded; decision stays pending"


def _numeric(value):
    if isinstance(value, bool) or value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        try:
            return float(value.strip())
        except ValueError:
            return None
    return None


def compare_primary(baseline: dict, metrics: list) -> tuple[dict | None, str]:
    """Compute one observed-minus-baseline delta. Never chooses keep/discard."""
    name = baseline["primary_metric"]
    found = []
    for row in metrics:
        if name not in row:
            continue
        number = _numeric(row.get(name))
        if number is None:
            return None, f"primary metric {name} is not numeric"
        found.append(number)
    if not found:
        return None, f"primary metric {name} missing from collected rows"
    if len(set(found)) != 1:
        return None, f"primary metric {name} has conflicting collected values"
    base = _numeric(baseline.get("baseline"))
    if base is None:
        return None, "baseline value is not numeric"
    observed = found[0]
    delta = observed - base
    if delta > 0:
        direction = "higher"
    elif delta < 0:
        direction = "lower"
    else:
        direction = "flat"
    return {
        "primary_metric": name,
        "baseline": base,
        "observed": observed,
        "delta": delta,
        "direction": direction,
        "decision": "pending",
        "note": "numeric comparison only; not a keep/discard",
    }, f"{name} observed {observed} vs baseline {base} ({direction})"



def load_decision(packet: Path, comparison: dict | None) -> tuple[dict | None, str]:
    """Read an explicit keep/discard/retest. Never invent one.

    A file is ignored until a numeric comparison exists. complete.py still
    needs the other evidence rows; this only records the learning decision.
    """
    path = packet / DECISION_NAME
    if comparison is None:
        if path.is_file():
            return None, "decision file ignored until a numeric comparison exists"
        return None, "no experiment_decision.json; decision stays pending"
    if not path.is_file():
        return None, "no experiment_decision.json; decision stays pending"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None, "experiment_decision.json is not json"
    if not isinstance(data, dict):
        return None, "experiment_decision.json must be an object"
    decision = str(data.get("decision") or "").strip().lower()
    reason = str(data.get("reason") or "").strip()
    source = str(data.get("source") or "").strip()
    if decision not in RECORDED_DECISIONS:
        return None, "decision must be keep, discard, or retest"
    if not reason or not source:
        return None, "decision missing reason or source"
    if source.lower() in REJECTED_SOURCES:
        return None, "decision source must be a documented review, not invented"
    metric = str(data.get("primary_metric") or "").strip()
    if metric and metric != comparison.get("primary_metric"):
        return None, "decision primary_metric does not match the comparison"
    return {
        "decision": decision,
        "reason": reason,
        "source": source,
        "primary_metric": comparison.get("primary_metric"),
        "note": "explicit review recorded; not inferred from the delta",
    }, f"recorded {decision}; not inferred from the delta"


def inspect_experiment(
    packet: Path,
    env: dict[str, str] | None = None,
    now: datetime | None = None,
) -> dict:
    feedback = inspect_feedback(packet, env=env, now=now)
    upload = load_upload_state(packet)
    video_id = provider_video_id(upload)
    metrics, metrics_detail = collected_metrics(packet, video_id)
    baseline, baseline_detail = load_baseline(packet)
    checks = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    add("provider_video_id_present", bool(video_id), video_id or "no provider_video_id")
    add("metrics_present", metrics is not None, metrics_detail)
    comparison = None
    comparison_detail = "comparison waits for a documented baseline and collected rows"
    if baseline is not None and metrics is not None:
        comparison, comparison_detail = compare_primary(baseline, metrics)
    decision_file, decision_detail = load_decision(packet, comparison)
    add("baseline_documented", baseline is not None, baseline_detail)
    add("primary_metric_compared", comparison is not None, comparison_detail)
    add("decision_recorded", decision_file is not None, decision_detail)
    add("no_invented_result", True, "a delta is not a keep/discard; only experiment_decision.json records one")
    add("single_variable", baseline is None or baseline.get("change") in ALLOWED_CHANGES, "one material change per experiment when practical")

    decision = "pending"
    result = None
    if not video_id:
        gate = "HOLD_UNPUBLISHED"
        action = "DRY_RUN"
    elif metrics is None:
        gate = "HOLD_NO_EVIDENCE"
        action = "DRY_RUN"
    elif baseline is None:
        gate = "READY_TO_COMPARE"
        action = "COMPARE_BLOCKED_NO_BASELINE"
    elif comparison is None:
        gate = "READY_TO_COMPARE"
        action = "COMPARE_BLOCKED_METRIC"
    elif decision_file is None:
        gate = "READY_TO_COMPARE"
        action = "COMPARED"
    else:
        gate = "READY_TO_COMPARE"
        action = "DECISION_RECORDED"
        decision = decision_file["decision"]
        result = decision

    record = {
        "id": f"{packet.name}-exp-pending",
        "packet": packet.name,
        "provider_video_id": video_id,
        "hypothesis": None if baseline is None else baseline["hypothesis"],
        "change": None if baseline is None else baseline["change"],
        "allowed_changes": list(ALLOWED_CHANGES),
        "primary_metric": None if baseline is None else baseline["primary_metric"],
        "guardrails": [
            "do not invent analytics",
            "do not mix videos of different ages without a documented reason",
            "do not rewrite an old script to make the test look successful",
            "do not treat a single early outlier as a keep decision",
            "do not invent a baseline to clear COMPARE_BLOCKED_NO_BASELINE",
        ],
        "baseline": None if baseline is None else baseline["baseline"],
        "baseline_source": None if baseline is None else baseline["source"],
        "observed_metrics": metrics,
        "comparison": comparison,
        "result": result,
        "decision": decision,
        "decision_reason": None if decision_file is None else decision_file["reason"],
        "decision_source": None if decision_file is None else decision_file["source"],
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
        "comparison": rec.get("comparison"),
        "attempted_compare": rec.get("comparison") is not None,
        "note": "numeric comparison only; never invents a keep/discard result",
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
        "a documented baseline with one numeric primary metric is COMPARED; decision stays pending",
        "a missing or conflicting primary metric is COMPARE_BLOCKED_METRIC, not a keep/discard",
        "experiment_decision.json records keep/discard/retest only after COMPARED; a missing file stays pending",
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
