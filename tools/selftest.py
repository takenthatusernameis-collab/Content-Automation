#!/usr/bin/env python3
"""Read-only fixture contract check.

Runs against videos/sample-001-* only. Writes nothing.
Purpose: future runs can prove validate/doctor/hint/set_status/apply_script
contracts instead of leaving runtime unverified.
"""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from apply_script import check as apply_check  # noqa: E402
from assemble import inspect_assemble  # noqa: E402
from complete import inspect_complete  # noqa: E402
from experiment_loop import inspect_experiment  # noqa: E402
from hint import commands_for  # noqa: E402
from media_qa import inspect_media  # noqa: E402
from narration_adapter import extract_words  # noqa: E402
from next_action import recommend  # noqa: E402
from pipeline_status import inspect  # noqa: E402
from set_status import check as status_check, is_fixture  # noqa: E402
from validate_packet import packet_duration_warning, validate  # noqa: E402
from youtube_feedback import inspect_feedback  # noqa: E402
from youtube_upload import inspect_upload  # noqa: E402

# Printers that must reuse render_brief.selected_vo_drop, not a second builder.
DROP_IMPORTERS = (
    "pipeline_status.py",
    "next_action.py",
    "caption_brief.py",
    "qa_checklist.py",
    "vo_session.py",
    "narration_adapter.py",
    "media_qa.py",
    "youtube_upload.py",
    "assemble.py",
    "youtube_feedback.py",
    "experiment_loop.py",
    "complete.py",
)


def sample_packet() -> Path:
    videos = ROOT / "videos"
    hits = sorted(
        p
        for p in videos.iterdir()
        if p.is_dir() and p.name.startswith("sample-001")
    )
    if not hits:
        raise SystemExit("selftest: no videos/sample-001-* fixture")
    return hits[0]


def first_live_command(cmds: list[str]) -> str | None:
    for c in cmds:
        s = c.strip()
        if s and not s.startswith("#"):
            return s
    return None


def _page_names_drop(rel: str, text: str, failures: list[str]) -> None:
    if "videos/NNN-slug/vo/NNN-slug-take-selected.wav" not in text:
        failures.append(f"{rel} must name the repo-root Selected VO DROP path")
    if "Repo-root `vo/` is not Selected VO" not in text and "repo-root `vo/` is not Selected VO" not in text:
        failures.append(f"{rel} must say repo-root vo/ is not Selected VO")


def check_selected_vo_drop_lock() -> list[str]:
    """Fail if a VO printer stops importing the shared DROP helper."""
    failures: list[str] = []
    helper = TOOLS / "render_brief.py"
    if not helper.is_file():
        failures.append("missing tools/render_brief.py (selected_vo_drop home)")
        return failures
    helper_text = helper.read_text(encoding="utf-8")
    if "def selected_vo_drop(" not in helper_text:
        failures.append("render_brief.py must define selected_vo_drop(")
    for name in DROP_IMPORTERS:
        path = TOOLS / name
        if not path.is_file():
            continue
        text = path.read_text(encoding="utf-8")
        if "selected_vo_drop" not in text:
            failures.append(f"{name} must use selected_vo_drop")
        if "from render_brief import" not in text and "import render_brief" not in text:
            failures.append(f"{name} must import selected_vo_drop from render_brief")
    status = TOOLS / "set_status.py"
    if status.is_file():
        text = status.read_text(encoding="utf-8")
        if "selected_vo_path" not in text and "selected_vo_drop" not in text:
            failures.append("set_status.py must reuse selected_vo_path or selected_vo_drop")
        if "def selected_vo_drop(" in text:
            failures.append("set_status.py must not re-implement selected_vo_drop")
    hint = TOOLS / "hint.py"
    if hint.is_file():
        text = hint.read_text(encoding="utf-8")
        if "selected_vo_path" not in text and "selected_vo_drop" not in text:
            failures.append("hint.py must reuse selected_vo_path or selected_vo_drop")
        if "def selected_vo_drop(" in text:
            failures.append("hint.py must not re-implement selected_vo_drop")
        if "def selected_vo_path(" in text:
            failures.append("hint.py must not re-implement selected_vo_path")
    format_page = ROOT / "docs" / "format.md"
    if format_page.is_file():
        _page_names_drop("docs/format.md", format_page.read_text(encoding="utf-8"), failures)
    narration_page = ROOT / "docs" / "narration.md"
    if narration_page.is_file():
        _page_names_drop("docs/narration.md", narration_page.read_text(encoding="utf-8"), failures)
    return failures


def check_words_extract() -> list[str]:
    sample = (
        "# Script\n\n"
        "## Hook\nWORDS:\nHello world.\n\nVISUAL:\n*x*\n\n"
        "## CTA\nWORDS:\nGoodbye now.\n"
    )
    got = extract_words(sample)
    if "Hello world." not in got or "Goodbye now." not in got:
        return [f"extract_words missed WORDS blocks: {got!r}"]
    return []


def check_media_qa_fail_closed() -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp)
        (p / "script.md").write_text(
            "# Script\n\n## Hook\nWORDS:\nHello there world.\n\nVISUAL:\n*x*\n",
            encoding="utf-8",
        )
        (p / "assets.md").write_text(
            "| Beat | Type | File | Status |\n|---|---|---|---|\n| Hook | text-card | cards/hook-x.png | planned |\n",
            encoding="utf-8",
        )
        report = inspect_media(p)
        if report["gate"] != "FAIL":
            failures.append(f"media_qa must FAIL without media, got {report['gate']}")
        names = {c["name"]: c["ok"] for c in report["checks"]}
        if names.get("selected_vo_present"):
            failures.append("selected_vo_present must be false without a take")
        if names.get("ready_to_assemble"):
            failures.append("ready_to_assemble must be false without media")
        for level_name in ("vo_peak", "vo_rms", "vo_silence", "vo_clip"):
            if level_name not in names:
                failures.append(f"media_qa must report {level_name}")
            elif names[level_name]:
                failures.append(f"{level_name} must be false without a take")
        if "export_decodable" not in names:
            failures.append("media_qa must report export_decodable")
        elif names["export_decodable"]:
            failures.append("export_decodable must be false without an export")
        (p / "export").mkdir()
        (p / "export" / "master.mp4").write_bytes(b"junk-not-mp4")
        report2 = inspect_media(p)
        names2 = {c["name"]: c["ok"] for c in report2["checks"]}
        if names2.get("export_decodable"):
            failures.append("export_decodable must be false on a junk master.mp4")
        if report2["gate"] != "FAIL":
            failures.append(f"junk export must not PASS media_qa, got {report2['gate']}")
    return failures


def check_assemble_fail_closed() -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp)
        (p / "script.md").write_text(
            "# Script\n\n## Hook\nWORDS:\nHello there world.\n\nVISUAL:\n*x*\n",
            encoding="utf-8",
        )
        (p / "assets.md").write_text(
            "| Beat | Type | File | Status |\n|---|---|---|---|\n| Hook | text-card | cards/hook-x.png | planned |\n",
            encoding="utf-8",
        )
        report = inspect_assemble(p)
        if report["gate"] != "HOLD_MEDIA":
            failures.append(f"assemble must HOLD_MEDIA without media, got {report['gate']}")
        if report["action"] != "DRY_RUN":
            failures.append(f"assemble default action must be DRY_RUN, got {report['action']}")
        if report.get("ready_to_assemble"):
            failures.append("assemble ready_to_assemble must be false without media")
        (p / "export").mkdir()
        (p / "export" / "master.mp4").write_bytes(b"junk-not-mp4")
        report2 = inspect_assemble(p)
        if report2["gate"] == "EXPORT_EXISTS":
            failures.append("assemble must not treat a junk master.mp4 as EXPORT_EXISTS")
        if report2.get("export_present"):
            failures.append("assemble export_present must stay false on junk ftyp")
    return failures


def check_upload_fail_closed() -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp)
        (p / "publish.md").write_text(
            "## Title to upload\n\nFixture title\n\n"
            "## Description\n\nTwelve words here so the description check can pass easily.\n\n"
            "## Tags\n\n- fixture\n",
            encoding="utf-8",
        )
        report = inspect_upload(p, env={})
        if report["gate"] != "FAIL":
            failures.append(f"upload must FAIL without a master, got {report['gate']}")
        if report["action"] != "HOLD_LOCAL":
            failures.append(f"upload without master must HOLD_LOCAL, got {report['action']}")
        if report.get("export_present"):
            failures.append("upload export_present must be false without a master")
        names = {c["name"]: c["ok"] for c in report["checks"]}
        if names.get("master_export_present"):
            failures.append("upload master_export_present must be false without export/master.mp4")
        (p / "export").mkdir()
        (p / "export" / "master.mp4").write_bytes(b"junk-not-mp4")
        report2 = inspect_upload(p, env={})
        if report2["gate"] != "FAIL":
            failures.append(f"upload must FAIL on junk master.mp4, got {report2['gate']}")
        if report2["action"] != "HOLD_LOCAL":
            failures.append(f"junk master must stay HOLD_LOCAL, got {report2['action']}")
        if report2.get("export_present"):
            failures.append("upload export_present must stay false on junk ftyp")
        names2 = {c["name"]: c["ok"] for c in report2["checks"]}
        if names2.get("master_export_present"):
            failures.append("upload master_export_present must stay false on junk ftyp")
        if report2["gate"] in {"READY", "YOUTUBE_AUTH_REQUIRED"}:
            failures.append("junk master must not look credential-ready or upload-READY")
    return failures


def check_feedback_fail_closed() -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp)
        report = inspect_feedback(p, env={})
        if report["gate"] != "HOLD_UNPUBLISHED":
            failures.append(f"feedback must HOLD_UNPUBLISHED without video id, got {report['gate']}")
        if report["metrics"] is not None:
            failures.append("feedback must not invent metrics")
        if report["action"] != "DRY_RUN":
            failures.append(f"feedback default action must be DRY_RUN, got {report['action']}")
        with_id = p / "upload_state.json"
        with_id.write_text('{"provider_video_id": "abc123"}\n', encoding="utf-8")
        report2 = inspect_feedback(p, env={})
        if report2["gate"] != "YOUTUBE_AUTH_REQUIRED":
            failures.append(f"feedback with video id and no OAuth must be YOUTUBE_AUTH_REQUIRED, got {report2['gate']}")
        dummy = {
            "YOUTUBE_CLIENT_ID": "x",
            "YOUTUBE_CLIENT_SECRET": "y",
            "YOUTUBE_REFRESH_TOKEN": "z",
        }
        report3 = inspect_feedback(p, env=dummy)
        if report3["gate"] != "READY":
            failures.append(f"feedback with video id + OAuth env must be READY, got {report3['gate']}")
        if report3["action"] != "FETCH_BLOCKED_NO_NETWORK":
            failures.append(f"feedback READY action must stay offline, got {report3['action']}")
    return failures


def check_experiment_fail_closed() -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp)
        report = inspect_experiment(p, env={})
        if report["gate"] != "HOLD_UNPUBLISHED":
            failures.append(f"experiment must HOLD_UNPUBLISHED without video id, got {report['gate']}")
        rec = report.get("record") or {}
        if rec.get("result") is not None:
            failures.append("experiment must not invent a result")
        if rec.get("hypothesis") is not None:
            failures.append("experiment must not invent a hypothesis")
        if rec.get("decision") != "pending":
            failures.append(f"experiment decision must stay pending, got {rec.get('decision')}")
        (p / "upload_state.json").write_text(
            '{"provider_video_id": "abc123"}\n', encoding="utf-8"
        )
        report2 = inspect_experiment(p, env={})
        if report2["gate"] != "HOLD_NO_EVIDENCE":
            failures.append(
                f"experiment with video id and empty metrics must be HOLD_NO_EVIDENCE, got {report2['gate']}"
            )
        if (report2.get("record") or {}).get("result") is not None:
            failures.append("experiment must not invent a keep/discard from empty metrics")
    return failures


def check_complete_fail_closed() -> list[str]:
    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        p = Path(tmp)
        (p / "script.md").write_text(
            "# Script\n\n## Hook\nWORDS:\nHello there world.\n\nVISUAL:\n*x*\n",
            encoding="utf-8",
        )
        (p / "assets.md").write_text(
            "| Beat | Type | File | Status |\n|---|---|---|---|\n| Hook | text-card | cards/hook-x.png | planned |\n",
            encoding="utf-8",
        )
        report = inspect_complete(p, env={})
        if report["gate"] != "INCOMPLETE_MEDIA":
            failures.append(f"complete must INCOMPLETE_MEDIA without media, got {report['gate']}")
        if report.get("experiment_result") is not None:
            failures.append("complete must not invent an experiment result")
        if report.get("metrics") is not None:
            failures.append("complete must not invent metrics")
        if report.get("provider_video_id"):
            failures.append("complete must not invent a provider_video_id")
        names = {c["name"]: c["ok"] for c in report["checks"]}
        if names.get("selected_vo_present"):
            failures.append("complete selected_vo_present must be false without a take")
        if names.get("master_export_present"):
            failures.append("complete master_export_present must be false without export/master.mp4")
        (p / "upload_state.json").write_text(
            '{"provider_video_id": "abc123"}\n', encoding="utf-8"
        )
        (p / "export").mkdir()
        (p / "export" / "master.mp4").write_bytes(b"junk-not-mp4")
        report2 = inspect_complete(p, env={})
        if report2["gate"] != "INCOMPLETE_MEDIA":
            failures.append(
                f"complete with only a video id must stay INCOMPLETE_MEDIA, got {report2['gate']}"
            )
        names2 = {c["name"]: c["ok"] for c in report2["checks"]}
        if names2.get("master_export_present"):
            failures.append("complete master_export_present must stay false on junk ftyp")
    return failures


def main() -> int:
    path = sample_packet()
    failures: list[str] = []

    if not is_fixture(path):
        failures.append(f"is_fixture({path.name}) is False")

    errors, incompletes = validate(path, draft=False)
    if errors:
        failures.append(f"publish gate should PASS, got FAIL: {errors}")
    if incompletes:
        failures.append(f"publish gate incompletes unexpected: {incompletes}")

    dur = packet_duration_warning(path)
    if not dur:
        failures.append("expected duration WARN on short fixture WORDS")
    elif "below" not in dur:
        failures.append(f"duration WARN should say below band, got: {dur}")

    errs_dur, _ = validate(path, draft=False, duration=True)
    if not errs_dur:
        failures.append("--duration should FAIL the short fixture")

    row = inspect(path)
    if row["gate"] != "PASS":
        failures.append(f"inspect gate expected PASS, got {row['gate']}")
    if row["status"] != "draft":
        failures.append(f"fixture status expected draft, got {row['status']}")
    if row["drift"]:
        failures.append(f"fixture should have no drift, got {row['drift']}")

    code, why = recommend(path, row)
    if code != "expand-script":
        failures.append(f"next-action code expected expand-script, got {code} ({why})")

    cmds = commands_for(path, row, code)
    live = first_live_command(cmds)
    if live is None:
        failures.append("hint produced no live command")
    elif "--write" in live:
        failures.append(f"first live command must not include --write: {live}")
    lock = any("fixture lock" in c.lower() for c in cmds)
    if not lock:
        failures.append("hint must print fixture lock on sample-001")

    blocked_status = status_check(path, "ready_for_vo")
    if not blocked_status:
        failures.append("set_status ready_for_vo must refuse the fixture")
    else:
        blob = " ".join(blocked_status).lower()
        if "fixture" not in blob and "sample-001" not in blob:
            failures.append(f"set_status refuse should mention fixture: {blocked_status}")

    fake_script = (
        "# Script\n\n"
        "## Hook (0:00–0:12)\n\n"
        "WORDS: This line is only here so apply_script has headings to parse.\n\n"
        "## Payoff promise\n\nWORDS: payoff\n\n"
        "## Beat 1\n\nWORDS: beat\n\n"
        "## Beat 2\n\nWORDS: beat\n\n"
        "## Beat 3\n\nWORDS: beat\n\n"
        "## Beat 4\n\nWORDS: beat\n\n"
        "## CTA\n\nWORDS: cta\n"
    )
    blocked_apply = apply_check(path, fake_script)
    if not blocked_apply:
        failures.append("apply_script must refuse the fixture")
    elif not any("fixture" in e.lower() or "sample-001" in e.lower() for e in blocked_apply):
        failures.append(f"apply_script refuse should mention fixture: {blocked_apply}")

    failures.extend(check_selected_vo_drop_lock())
    failures.extend(check_words_extract())
    failures.extend(check_media_qa_fail_closed())
    failures.extend(check_assemble_fail_closed())
    failures.extend(check_upload_fail_closed())
    failures.extend(check_feedback_fail_closed())
    failures.extend(check_experiment_fail_closed())
    failures.extend(check_complete_fail_closed())

    print(f"Fixture: {path.name}")
    print(f"Gate: {row['gate']}")
    print(f"Status: {row['status']}")
    print(f"Code: {code}")
    print(f"Duration WARN: {dur or '—'}")
    print(f"First live command: {live}")
    if failures:
        print("SELFTEST FAIL")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("SELFTEST PASS")
    print("This command writes nothing.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
