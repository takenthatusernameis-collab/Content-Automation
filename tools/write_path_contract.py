#!/usr/bin/env python3
"""Contract check for the non-fixture write path.

Temp tree only. Never writes videos/ or sample-001.
Locks apply_script refuse/allow and set_status evidence gates so later
runs cannot silently regress the dry-run-default write tools.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from apply_script import check as apply_check  # noqa: E402
from apply_script import extract_script, looks_like_expand_prompt  # noqa: E402
from set_status import check as status_check, is_fixture  # noqa: E402


def words(n: int, seed: str = "word") -> str:
    return " ".join(f"{seed}{i}" for i in range(n))


def script_body(*, hook_n: int = 24, beat_n: int = 40) -> str:
    hook = words(hook_n, "hook")
    beat = words(beat_n, "beat")
    payoff = words(30, "pay")
    cta = words(20, "cta")
    return (
        "# Script\n\n"
        "Spoken words only under each beat. Visual notes in italics.\n\n"
        "## Hook (0:00–0:12)\n"
        f"WORDS: {hook}\n\n"
        "## Payoff promise\n"
        f"WORDS: {payoff}\n\n"
        "## Beat 1 — first\n"
        f"WORDS: {beat}\n\n"
        "## Beat 2 — second\n"
        f"WORDS: {beat}\n\n"
        "## Beat 3 — third\n"
        f"WORDS: {beat}\n\n"
        "## Beat 4 — fourth\n"
        f"WORDS: {beat}\n\n"
        "## CTA\n"
        f"WORDS: {cta}\n"
    )


def packet_md() -> str:
    return (
        "# Packet\n\n"
        "- id: 002\n"
        "- slug: write-path-contract\n"
        "- working_title: Write path contract\n"
        "- status: draft\n"
        "- format: explainer-6-10min\n"
        "- target_duration_min: 8\n"
        "- created: 2026-09-09\n"
        "- updated: 2026-09-09\n"
    )


def fail(failures: list[str], cond: bool, msg: str) -> None:
    if not cond:
        failures.append(msg)


def main() -> int:
    failures: list[str] = []

    promptish = (
        "You are expanding an existing YouTube explainer script.\n"
        "## Writer contract (follow)\n"
        "## Beat budget (size hint only)\n"
    )
    fail(failures, looks_like_expand_prompt(promptish), "prompt marker not detected")
    fail(
        failures,
        not looks_like_expand_prompt(script_body()),
        "real script flagged as expand prompt",
    )

    fenced = "```markdown\n" + script_body() + "```\n"
    extracted = extract_script(fenced)
    fail(failures, extracted.startswith("# Script"), f"extract fence start: {extracted[:20]!r}")
    fail(failures, "```" not in extracted, "extract left a fence")

    with tempfile.TemporaryDirectory() as tmp:
        live = Path(tmp) / "videos" / "002-write-path-contract"
        live.mkdir(parents=True)
        (live / "packet.md").write_text(packet_md(), encoding="utf-8")
        (live / "script.md").write_text(script_body(hook_n=24, beat_n=20), encoding="utf-8")

        fixture = Path(tmp) / "videos" / "sample-001-why-systems-beat-motivation"
        fixture.mkdir(parents=True)
        (fixture / "packet.md").write_text(packet_md().replace("002", "001"), encoding="utf-8")
        (fixture / "script.md").write_text(script_body(), encoding="utf-8")

        fail(failures, is_fixture(fixture), "fixture detect failed")
        fail(failures, not is_fixture(live), "live packet treated as fixture")

        blocked_fix = apply_check(fixture, script_body())
        fail(failures, bool(blocked_fix), "apply must refuse fixture")
        fail(
            failures,
            any("fixture" in e.lower() or "sample-001" in e.lower() for e in blocked_fix),
            f"apply fixture message: {blocked_fix}",
        )

        blocked_prompt = apply_check(live, promptish + "\n## Hook\nWORDS: " + words(24))
        fail(failures, bool(blocked_prompt), "apply must refuse expand_prompt stdout")

        short_hook = apply_check(live, script_body(hook_n=10))
        fail(
            failures,
            any("hook" in e.lower() for e in short_hook),
            f"short hook should block: {short_hook}",
        )

        good = apply_check(live, script_body(hook_n=24, beat_n=40))
        fail(failures, good == [], f"good non-fixture script blocked: {good}")

        blocked_vo = status_check(live, "ready_for_vo")
        fail(failures, bool(blocked_vo), "set_status ready_for_vo must block short WORDS")
        fail(
            failures,
            any("duration" in e.lower() for e in blocked_vo),
            f"ready_for_vo block should mention duration: {blocked_vo}",
        )

        skip = status_check(live, "ready_for_edit")
        fail(
            failures,
            any("skip" in e.lower() for e in skip),
            f"skip draft->ready_for_edit should block: {skip}",
        )

        same = status_check(live, "draft")
        fail(failures, any("already" in e.lower() for e in same), f"already draft: {same}")

        bad = status_check(live, "not-a-status")
        fail(failures, any("invalid" in e.lower() for e in bad), f"invalid target: {bad}")

        fixture_promote = status_check(fixture, "ready_for_vo")
        fail(failures, bool(fixture_promote), "fixture promote must block")

        repo_videos = Path(__file__).resolve().parents[1] / "videos"
        leak = repo_videos / "002-write-path-contract"
        fail(failures, not leak.exists(), f"temp packet leaked to {leak}")

    print("Write-path contract")
    print("apply: fixture refuse + prompt refuse + hook band + allow non-fixture")
    print("set_status: duration WARN blocks ready_for_vo; skip blocked; fixture blocked")
    if failures:
        print("WRITE PATH CONTRACT FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("WRITE PATH CONTRACT PASS")
    print("This command writes nothing in the repo.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
