#!/usr/bin/env python3
"""Contract check for the non-fixture write path.

Temp tree only. Never writes videos/ or sample-001.
Locks apply_script refuse/allow and set_status evidence gates so later
runs cannot silently regress the dry-run-default write tools.
Also locks missing --from path messaging (draft.md convention),
the apply_script CLI exit 2 for a missing --from file,
the advertised dry-run CLI for an existing PATH/draft.md
(exit 0, Dry-run only, no script.md write),
and the advertised set_status CLI for ready_for_vo
(duration block and fixture block leave packet.md unchanged,
including when --write is passed on a blocked target).
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from apply_script import check as apply_check  # noqa: E402
from apply_script import extract_script, looks_like_expand_prompt  # noqa: E402
from apply_script import load_source, missing_source_error  # noqa: E402
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

    missing_msg = missing_source_error(Path("videos/002-example/draft.md"))
    fail(failures, "missing source file:" in missing_msg, "missing-source message lacks path header")
    fail(failures, "draft.md" in missing_msg, "missing-source message must name draft.md")
    fail(failures, "draft.md is not script.md" in missing_msg, "missing-source must not treat draft as script")
    fail(failures, "writes nothing" in missing_msg.lower(), "missing-source must stay dry-run")
    text, code = load_source("definitely-not-a-real-draft.md")
    fail(failures, text is None and code == 2, f"load_source missing file should be (None, 2), got {(text, code)}")

    with tempfile.TemporaryDirectory() as tmp:
        live = Path(tmp) / "videos" / "002-write-path-contract"
        live.mkdir(parents=True)
        (live / "packet.md").write_text(packet_md(), encoding="utf-8")
        short_script = script_body(hook_n=24, beat_n=20)
        long_script = script_body(hook_n=24, beat_n=40)
        (live / "script.md").write_text(short_script, encoding="utf-8")
        draft = live / "draft.md"
        draft.write_text(long_script, encoding="utf-8")
        loaded, lcode = load_source(str(draft))
        fail(failures, lcode == 0 and loaded is not None and "Beat 1" in loaded, "load_source should read existing draft.md")

        missing_from = live / "draft-missing.md"
        proc = subprocess.run(
            [
                sys.executable,
                str(TOOLS / "apply_script.py"),
                str(live),
                "--from",
                str(missing_from),
            ],
            capture_output=True,
            text=True,
        )
        err = (proc.stderr or "") + (proc.stdout or "")
        fail(failures, proc.returncode == 2, f"CLI missing --from should exit 2, got {proc.returncode}")
        fail(failures, "missing source file:" in err, "CLI missing --from should print path header")
        fail(failures, "draft.md is not script.md" in err, "CLI missing --from must not treat draft as script")
        fail(failures, "writes nothing" in err.lower(), "CLI missing --from must stay dry-run")
        fail(failures, not missing_from.exists(), "CLI missing --from must not create the source file")
        fail(
            failures,
            (live / "script.md").read_text(encoding="utf-8") == short_script,
            "CLI missing --from must not rewrite script.md",
        )

        dry = subprocess.run(
            [
                sys.executable,
                str(TOOLS / "apply_script.py"),
                str(live),
                "--from",
                str(draft),
            ],
            capture_output=True,
            text=True,
        )
        dry_out = (dry.stdout or "") + (dry.stderr or "")
        fail(failures, dry.returncode == 0, f"CLI dry-run --from draft.md should exit 0, got {dry.returncode}\n{dry_out}")
        fail(failures, "Dry-run only" in dry_out, "CLI dry-run --from draft.md must print Dry-run only")
        fail(failures, "--write" in dry_out, "CLI dry-run should mention --write without performing it")
        fail(
            failures,
            (live / "script.md").read_text(encoding="utf-8") == short_script,
            "CLI dry-run --from draft.md must not rewrite script.md",
        )
        fail(
            failures,
            draft.read_text(encoding="utf-8") == long_script,
            "CLI dry-run --from draft.md must not rewrite draft.md",
        )
        fail(failures, "Result: OK" in dry_out, f"CLI dry-run good draft should report OK: {dry_out[:200]!r}")

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

        live_packet_before = (live / "packet.md").read_text(encoding="utf-8")
        fixture_packet_before = (fixture / "packet.md").read_text(encoding="utf-8")

        status_dry = subprocess.run(
            [
                sys.executable,
                str(TOOLS / "set_status.py"),
                str(live),
                "--to",
                "ready_for_vo",
            ],
            capture_output=True,
            text=True,
        )
        status_out = (status_dry.stdout or "") + (status_dry.stderr or "")
        fail(failures, status_dry.returncode == 1, f"CLI set_status ready_for_vo short WORDS should exit 1, got {status_dry.returncode}\n{status_out}")
        fail(failures, "Result: BLOCKED" in status_out, "CLI set_status ready_for_vo short WORDS must print BLOCKED")
        fail(failures, "duration" in status_out.lower(), "CLI set_status ready_for_vo short WORDS must mention duration")
        fail(
            failures,
            (live / "packet.md").read_text(encoding="utf-8") == live_packet_before,
            "CLI set_status dry-run ready_for_vo must not rewrite packet.md",
        )

        status_write_blocked = subprocess.run(
            [
                sys.executable,
                str(TOOLS / "set_status.py"),
                str(live),
                "--to",
                "ready_for_vo",
                "--write",
            ],
            capture_output=True,
            text=True,
        )
        sw_out = (status_write_blocked.stdout or "") + (status_write_blocked.stderr or "")
        fail(failures, status_write_blocked.returncode == 1, f"CLI set_status --write blocked ready_for_vo should exit 1, got {status_write_blocked.returncode}\n{sw_out}")
        fail(
            failures,
            (live / "packet.md").read_text(encoding="utf-8") == live_packet_before,
            "CLI set_status --write on duration block must not rewrite packet.md",
        )
        fail(failures, "- status: draft" in (live / "packet.md").read_text(encoding="utf-8"), "blocked ready_for_vo must leave status draft")

        fixture_cli = subprocess.run(
            [
                sys.executable,
                str(TOOLS / "set_status.py"),
                str(fixture),
                "--to",
                "ready_for_vo",
                "--write",
            ],
            capture_output=True,
            text=True,
        )
        fix_out = (fixture_cli.stdout or "") + (fixture_cli.stderr or "")
        fail(failures, fixture_cli.returncode == 1, f"CLI set_status fixture promote should exit 1, got {fixture_cli.returncode}\n{fix_out}")
        fail(failures, "fixture" in fix_out.lower() or "sample-001" in fix_out.lower(), f"CLI fixture promote message: {fix_out[:200]!r}")
        fail(
            failures,
            (fixture / "packet.md").read_text(encoding="utf-8") == fixture_packet_before,
            "CLI set_status --write fixture promote must not rewrite packet.md",
        )

        repo_videos = Path(__file__).resolve().parents[1] / "videos"
        leak = repo_videos / "002-write-path-contract"
        fail(failures, not leak.exists(), f"temp packet leaked to {leak}")

    print("Write-path contract")
    print("apply: fixture refuse + prompt refuse + hook band + allow non-fixture + missing --from helper + CLI exit 2 + CLI dry-run existing draft.md")
    print("set_status: duration WARN blocks ready_for_vo; skip blocked; fixture blocked; CLI dry-run and blocked --write leave packet.md draft")
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
