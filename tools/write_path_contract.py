#!/usr/bin/env python3
"""Contract check for the non-fixture write path.

Temp tree only. Never writes videos/ or sample-001.
Locks apply_script refuse/allow and set_status evidence gates so later
runs cannot silently regress the dry-run-default write tools.
Also locks missing --from path messaging (draft.md convention),
the apply_script CLI exit 2 for a missing --from file,
the advertised dry-run CLI for an existing PATH/draft.md
(exit 0, Dry-run only, no script.md write),
the advertised set_status CLI for ready_for_vo
(duration block and fixture block leave packet.md unchanged,
including when --write is passed on a blocked target),
the advertised apply_script CLI --write against the fixture
(exit 1, BLOCKED, script.md unchanged),
the advertised non-fixture apply_script CLI
(--refresh without --write writes nothing;
--write replaces script.md only;
--write --refresh replaces script.md and refreshes
expand.md / vo_session.md / captions.md; packet.md stays draft),
and the advertised non-fixture set_status CLI when WORDS are in band
(dry-run exit 0 leaves packet.md draft;
--write exit 0 sets status ready_for_vo and does not create media).
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
ROOT = TOOLS.parent
PY = sys.executable

HOOK = (
    "Most mornings you reopen the whole work list instead of starting "
    "the one job you already chose yesterday evening first."
)
PAYOFF = "After this you start from a default instead of a blank list."
BEAT = (
    "Pick one next action the night before and put it on a card. "
    "In the morning read only that card. Do not reopen the queue."
)
CTA = "Tonight write tomorrow's first move on one line and leave it on the desk."


def words(n: int) -> str:
    return " ".join(f"word{i:03d}" for i in range(n))


def script_body(hook: str, beat_words: int) -> str:
    beat = (BEAT + " " + words(max(0, beat_words))).strip()
    return (
        "# Script\n\n"
        "Spoken words only under each beat. Visual notes in italics.\n\n"
        "## Hook (0:00–0:12)\n"
        f"WORDS:\n{hook}\n\nVISUAL:\n\n"
        "## Payoff promise\n"
        f"WORDS:\n{PAYOFF}\n\n"
        "## Beat 1 — default\n"
        f"WORDS:\n{beat}\n\nVISUAL:\n\n"
        "## Beat 2 — morning\n"
        f"WORDS:\n{beat}\n\nVISUAL:\n\n"
        "## Beat 3 — queue\n"
        f"WORDS:\n{beat}\n\nVISUAL:\n\n"
        "## Beat 4 — close\n"
        f"WORDS:\n{beat}\n\nVISUAL:\n\n"
        "## CTA\n"
        f"WORDS:\n{CTA}\n"
    )


def packet_md(status: str = "draft") -> str:
    return (
        "# Packet\n\n"
        "- id: 002\n"
        "- slug: stop-deciding-what-to-work-on-every-morning\n"
        "- working_title: Stop deciding what to work on every morning\n"
        f"- status: {status}\n"
        "- format: explainer-6-10min\n"
        "- target_duration_min: 8\n"
        "- created: 2026-09-11\n"
        "- updated: 2026-09-11\n\n"
        "## Promise\n"
        "One sentence: after watching, the viewer can start from a default.\n\n"
        "## Remaining human work\n"
        "- [ ] Lock title\n"
        "- [ ] Record or generate VO\n"
    )


def extra_files() -> dict[str, str]:
    return {
        "idea.md": "# Idea\n\n- topic: Stop deciding what to work on every morning\n"
        "- problem: they reopen the whole work list every morning instead of starting\n"
        "- mechanism: next-action default\n",
        "titles.md": (
            "# Titles\n\n"
            "Primary: Stop deciding every morning\n"
            "1. Stop deciding every morning\n"
            "2. A default beats a blank list\n"
            "3. Do not reopen the queue\n"
            "4. One card for tomorrow\n"
            "5. Start from last night\n"
        ),
        "thumbnail.md": "On-image text: Start this card\n",
        "qa.md": "# QA\n",
        "expand.md": "SENTINEL_EXPAND\n",
        "vo_session.md": "SENTINEL_VO\n",
        "captions.md": "SENTINEL_CAP\n",
    }


def write_packet(dest: Path, script: str, status: str = "draft") -> None:
    dest.mkdir(parents=True, exist_ok=True)
    (dest / "packet.md").write_text(packet_md(status), encoding="utf-8")
    (dest / "script.md").write_text(script, encoding="utf-8")
    for name, body in extra_files().items():
        (dest / name).write_text(body, encoding="utf-8")


def run_tool(name: str, args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [PY, str(TOOLS / name), *args],
        capture_output=True,
        text=True,
    )


def fail(failures: list[str], cond: bool, msg: str) -> None:
    if not cond:
        failures.append(msg)


def main() -> int:
    failures: list[str] = []
    apply = TOOLS / "apply_script.py"
    status_tool = TOOLS / "set_status.py"
    fail(failures, apply.is_file(), "apply_script.py missing")
    fail(failures, status_tool.is_file(), "set_status.py missing")
    if failures:
        print("WRITE PATH CONTRACT FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1

    short = script_body(HOOK, 20)
    long = script_body(HOOK, 220)

    with tempfile.TemporaryDirectory() as tmp:
        tmp_path = Path(tmp)
        fixture = tmp_path / "sample-001-why-systems-beat-motivation"
        live = tmp_path / "002-stop-deciding-what-to-work-on-every-morning"
        write_packet(fixture, short)
        write_packet(live, short)
        fixture_script_before = (fixture / "script.md").read_text(encoding="utf-8")
        fixture_packet_before = (fixture / "packet.md").read_text(encoding="utf-8")
        live_script_before = (live / "script.md").read_text(encoding="utf-8")

        missing = run_tool(
            "apply_script.py",
            [str(live), "--from", str(live / "draft.md")],
        )
        fail(failures, missing.returncode == 2, f"missing --from exit {missing.returncode}")
        blob = (missing.stdout + missing.stderr).lower()
        fail(failures, "draft.md" in blob, "missing --from hint lacks draft.md")
        fail(
            failures,
            (live / "script.md").read_text(encoding="utf-8") == live_script_before,
            "missing --from wrote script.md",
        )

        (live / "draft.md").write_text(long, encoding="utf-8")
        dry = run_tool(
            "apply_script.py",
            [str(live), "--from", str(live / "draft.md")],
        )
        fail(failures, dry.returncode == 0, f"existing draft dry-run exit {dry.returncode}\n{dry.stdout}\n{dry.stderr}")
        fail(failures, "Dry-run only" in dry.stdout, f"dry-run banner missing: {dry.stdout}")
        fail(
            failures,
            (live / "script.md").read_text(encoding="utf-8") == live_script_before,
            "existing draft dry-run wrote script.md",
        )

        blocked_status = run_tool(
            "set_status.py",
            [str(live), "--to", "ready_for_vo"],
        )
        fail(failures, blocked_status.returncode == 1, f"short WORDS set_status exit {blocked_status.returncode}")
        fail(failures, "BLOCKED" in blocked_status.stdout, "short WORDS set_status not BLOCKED")
        fail(
            failures,
            "- status: draft" in (live / "packet.md").read_text(encoding="utf-8"),
            "short WORDS set_status wrote packet.md",
        )

        blocked_write = run_tool(
            "set_status.py",
            [str(live), "--to", "ready_for_vo", "--write"],
        )
        fail(failures, blocked_write.returncode == 1, "short WORDS --write exit not 1")
        fail(
            failures,
            "- status: draft" in (live / "packet.md").read_text(encoding="utf-8"),
            "short WORDS --write mutated packet.md",
        )

        fixture_status = run_tool(
            "set_status.py",
            [str(fixture), "--to", "ready_for_vo", "--write"],
        )
        fail(failures, fixture_status.returncode == 1, "fixture set_status --write exit not 1")
        fail(
            failures,
            (fixture / "packet.md").read_text(encoding="utf-8") == fixture_packet_before,
            "fixture set_status wrote packet.md",
        )

        (fixture / "draft.md").write_text(long, encoding="utf-8")
        fixture_apply = run_tool(
            "apply_script.py",
            [str(fixture), "--from", str(fixture / "draft.md"), "--write"],
        )
        fail(failures, fixture_apply.returncode == 1, f"fixture apply --write exit {fixture_apply.returncode}")
        fail(failures, "BLOCKED" in fixture_apply.stdout, "fixture apply --write not BLOCKED")
        fail(
            failures,
            (fixture / "script.md").read_text(encoding="utf-8") == fixture_script_before,
            "fixture apply --write wrote script.md",
        )

        refresh_dry = run_tool(
            "apply_script.py",
            [str(live), "--from", str(live / "draft.md"), "--refresh"],
        )
        fail(failures, refresh_dry.returncode == 0, f"--refresh without --write exit {refresh_dry.returncode}\n{refresh_dry.stdout}")
        fail(failures, "Dry-run only" in refresh_dry.stdout, "--refresh without --write not dry-run")
        fail(
            failures,
            (live / "script.md").read_text(encoding="utf-8") == live_script_before,
            "--refresh without --write wrote script.md",
        )
        fail(failures, (live / "expand.md").read_text(encoding="utf-8") == "SENTINEL_EXPAND\n", "refresh-without-write touched expand.md")
        fail(failures, (live / "vo_session.md").read_text(encoding="utf-8") == "SENTINEL_VO\n", "refresh-without-write touched vo_session.md")
        fail(failures, (live / "captions.md").read_text(encoding="utf-8") == "SENTINEL_CAP\n", "refresh-without-write touched captions.md")

        write_only = run_tool(
            "apply_script.py",
            [str(live), "--from", str(live / "draft.md"), "--write"],
        )
        fail(failures, write_only.returncode == 0, f"non-fixture --write exit {write_only.returncode}\n{write_only.stdout}\n{write_only.stderr}")
        fail(failures, (live / "script.md").read_text(encoding="utf-8") == long, "non-fixture --write did not replace script.md")
        fail(failures, (live / "expand.md").read_text(encoding="utf-8") == "SENTINEL_EXPAND\n", "--write without --refresh touched expand.md")
        fail(failures, "- status: draft" in (live / "packet.md").read_text(encoding="utf-8"), "--write bumped packet status")

        write_refresh = run_tool(
            "apply_script.py",
            [str(live), "--from", str(live / "draft.md"), "--write", "--refresh"],
        )
        fail(failures, write_refresh.returncode == 0, f"--write --refresh exit {write_refresh.returncode}\n{write_refresh.stdout}\n{write_refresh.stderr}")
        fail(failures, (live / "script.md").read_text(encoding="utf-8") == long, "--write --refresh lost script.md")
        fail(failures, (live / "expand.md").read_text(encoding="utf-8") != "SENTINEL_EXPAND\n", "--write --refresh did not refresh expand.md")
        fail(failures, (live / "vo_session.md").read_text(encoding="utf-8") != "SENTINEL_VO\n", "--write --refresh did not refresh vo_session.md")
        fail(failures, (live / "captions.md").read_text(encoding="utf-8") != "SENTINEL_CAP\n", "--write --refresh did not refresh captions.md")
        fail(failures, "- status: draft" in (live / "packet.md").read_text(encoding="utf-8"), "--write --refresh bumped packet status")

        ready = tmp_path / "002-in-band-ready"
        write_packet(ready, long)
        status_dry = run_tool(
            "set_status.py",
            [str(ready), "--to", "ready_for_vo"],
        )
        fail(failures, status_dry.returncode == 0, f"in-band set_status dry-run exit {status_dry.returncode}\n{status_dry.stdout}\n{status_dry.stderr}")
        fail(failures, "Dry-run only" in status_dry.stdout, "in-band set_status dry-run banner missing")
        fail(failures, "BLOCKED" not in status_dry.stdout, f"in-band set_status dry-run BLOCKED: {status_dry.stdout}")
        fail(
            failures,
            "- status: draft" in (ready / "packet.md").read_text(encoding="utf-8"),
            "in-band set_status dry-run wrote packet.md",
        )

        status_write = run_tool(
            "set_status.py",
            [str(ready), "--to", "ready_for_vo", "--write"],
        )
        fail(failures, status_write.returncode == 0, f"in-band set_status --write exit {status_write.returncode}\n{status_write.stdout}\n{status_write.stderr}")
        after = (ready / "packet.md").read_text(encoding="utf-8")
        fail(failures, "- status: ready_for_vo" in after, "in-band set_status --write did not set ready_for_vo")
        fail(failures, not (ready / "vo").exists(), "set_status created vo/")

        leak = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning"
        fail(failures, not leak.exists(), f"contract leaked {leak}")

    print("Write path contract")
    print("apply missing --from: exit 2, draft.md hint, no script.md write")
    print("apply existing draft.md: exit 0, Dry-run only, no script.md write")
    print("set_status short/fixture ready_for_vo: exit 1, packet.md unchanged")
    print("apply fixture --write: exit 1, BLOCKED, script.md unchanged")
    print("apply --refresh without --write: dry-run, no derived writes")
    print("apply --write: script.md only; packet.md draft")
    print("apply --write --refresh: script + expand/vo_session/captions; packet.md draft")
    print("set_status in-band ready_for_vo: dry-run no write; --write sets status")
    if failures:
        print("WRITE PATH CONTRACT FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("WRITE PATH CONTRACT PASS")
    print("This command writes nothing in videos/ and does not mark the queue.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
