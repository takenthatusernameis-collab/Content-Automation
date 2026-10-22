#!/usr/bin/env python3
"""Suggest change-aligned hypothesis templates for an experiment.

Reads idea.md (or experiment_baseline.json if present) to identify the single allowed change
and extract mechanism/topic. Prints 2-3 concrete hypothesis phrasings that name the mechanism
and predict an effect on a typical metric for that change type.
Does not invent numeric baselines, results, or decisions. Does not write files. Does not call APIs.
Complements experiment_metric_suggest.py, experiment_guardrail_suggest.py, and the starters.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from experiment_loop import ALLOWED_CHANGES  # noqa: E402
from idea_utils import extract as idea_extract  # noqa: E402

# Mapping from change type to hypothesis templates (placeholders for mechanism and predicted effect).
# Templates stay qualitative on the effect until a real baseline exists.
HYPOTHESIS_MAP = {
    "hook": [
        "A stronger opening that names '{mech}' in the first 10 seconds will raise average view duration on the first 30 seconds compared with the prior video.",
        "Naming the mechanism '{mech}' before any example will improve early retention without changing the body or payoff.",
    ],
    "mechanism_framing": [
        "Framing the mechanism '{mech}' as a reusable system (instead of a one-off tip) will increase average percentage viewed.",
        "Explicitly labeling '{mech}' as the named mechanism in the first 15 seconds will improve retention without altering the examples.",
    ],
    "example_density": [
        "Adding one extra concrete example that still supports '{mech}' will raise average view duration without padding or changing the CTA.",
        "Keeping example density inside the format band while illustrating '{mech}' will preserve retention compared with a denser version.",
    ],
    "title_promise": [
        "A title that promises the outcome of '{mech}' more specifically will raise impressions CTR while the spoken hook stays identical.",
        "Matching the title promise exactly to what the first 30 seconds deliver for '{mech}' will improve early average percentage viewed.",
    ],
    "visual_explanation": [
        "A card that diagrams '{mech}' with readable text under the word limit will raise average view duration without rewriting the spoken script.",
        "Replacing a text-only card with a simple visual of '{mech}' will improve retention on that beat while the VO stays unchanged.",
    ],
    "pacing": [
        "Tightening pauses around the mechanism naming points for '{mech}' will raise average view duration without cutting examples or the payoff.",
        "Preserving the same content density while reducing dead air will improve retention on '{mech}' compared with the slower prior take.",
    ],
    "cta": [
        "A clearer end-screen CTA that references '{mech}' will raise end-screen click rate without changing the hook or body.",
        "Moving the CTA into the last 20 seconds while keeping the mechanism framing identical will improve subscribers gained relative to the prior video.",
    ],
    "topic_selection": [
        "A topic that applies the same '{mech}' mechanism to a closely related viewer problem will produce comparable average view duration to the prior video.",
        "Documenting why this topic continues the mechanism '{mech}' will allow a clean comparison on views without changing production format.",
    ],
}


def extract(idea_text: str) -> tuple[str, str]:
    mech, _problem, topic = idea_extract(idea_text)
    return mech, topic


def detect_change(packet: Path) -> str:
    """Prefer an existing baseline change, else fall back to idea.md heuristic."""
    baseline = packet / "experiment_baseline.json"
    if baseline.is_file():
        try:
            data = json.loads(baseline.read_text(encoding="utf-8"))
            ch = str(data.get("change") or "").strip()
            if ch in ALLOWED_CHANGES:
                return ch
        except json.JSONDecodeError:
            pass
    idea = packet / "idea.md"
    if idea.is_file():
        text = idea.read_text(encoding="utf-8")
        low = text.lower()
        if "hook" in low:
            return "hook"
        if "title" in low:
            return "title_promise"
        if "cta" in low or "call to action" in low:
            return "cta"
        if "visual" in low or "card" in low:
            return "visual_explanation"
        if "pace" in low or "pacing" in low:
            return "pacing"
        if "example" in low:
            return "example_density"
        if "topic" in low:
            return "topic_selection"
        return "mechanism_framing"
    return "mechanism_framing"


def recommended_actions(packet: str) -> list[str]:
    """Provide concrete copy-paste next steps after the hypothesis templates."""
    p = packet
    return [
        "pick one hypothesis template from the list above, edit if needed, and pair with a real metric + documented baseline",
        f"baseline skeleton: python3 tools/experiment_baseline_starter.py {p}",
        f"notes skeleton: python3 tools/experiment_notes_starter.py {p}",
        f"guardrails: python3 tools/experiment_guardrail_suggest.py {p}",
        f"package view: python3 tools/experiment_package_starter.py {p}",
        f"setup suggestions: python3 tools/experiment_setup_report.py {p}",
        f"quality scans: python3 tools/quality_scan.py {p} && python3 tools/claim_scan.py {p}",
        f"full production if needed: python3 tools/full_production_starter.py {p}",
        "do not invent numeric baselines, results, or decisions; experiment_loop.py rejects placeholder sources",
    ]


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Suggest hypothesis templates for an experiment change. No invented results."
    )
    parser.add_argument("packet", help="Packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    change = detect_change(path)
    idea = path / "idea.md"
    mech = "the mechanism"
    topic = ""
    if idea.is_file():
        text = idea.read_text(encoding="utf-8")
        mech_extracted, topic = extract(text)
        if mech_extracted:
            mech = mech_extracted[:80]
    templates = HYPOTHESIS_MAP.get(change, HYPOTHESIS_MAP["mechanism_framing"])
    print("EXPERIMENT HYPOTHESIS SUGGEST (templates only; no invented baseline or decision)")
    print(f"packet: {path.name}")
    print(f"detected_change: {change}")
    print(f"mechanism: {mech}")
    print(f"topic: {topic or '(none)'}")
    print(f"allowed_changes: {', '.join(ALLOWED_CHANGES)}")
    print()
    print("Recommended hypothesis templates (edit one, then pair with a real metric and baseline):")
    for t in templates:
        print(f"  - {t.format(mech=mech)}")
    print()
    print("These keep the single-variable rule and name the mechanism so the comparison stays interpretable.")
    print("Do not invent a numeric baseline or result. Use experiment_baseline_starter.py after choosing one.")
    print("experiment_loop.py still requires a documented numeric baseline and explicit decision file.")
    print()
    print("## RECOMMENDED NEXT (copy-paste ready; no invent)")
    for rec in recommended_actions(str(path)):
        print(f"- {rec}")
    print()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
