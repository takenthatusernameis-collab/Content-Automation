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
from pipeline_status import format_report, inspect  # noqa: E402
from set_status import check as status_check, is_fixture  # noqa: E402
from validate_packet import packet_duration_warning, validate  # noqa: E402
from youtube_feedback import inspect_feedback  # noqa: E402
from youtube_upload import file_sha256, inspect_upload, master_block_reason  # noqa: E402

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
    from assemble import command_for
    cmd = command_for(
        Path("."),
        {"vo_rel": "vo/x.wav", "rows": [{"card": "cards/hook-x.png", "dur": 4.0}]},
    )
    joined = " ".join(cmd)
    if "apad=pad_dur=" not in joined:
        failures.append("assemble recipe must apad=pad_dur so -shortest keeps the end screen and does not hang")
    if "-shortest" not in cmd:
        failures.append("assemble recipe must keep -shortest after apad")
    if "[aout]" not in joined:
        failures.append("assemble recipe must map the padded audio, not raw 0:a")
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
        sample = p / "export" / "banned-sample.bin"
        sample.write_bytes(b"truncated-end-screen-fixture")
        digest = file_sha256(sample)
        reason = master_block_reason(sample, banned={digest})
        if not reason or digest not in reason:
            failures.append(f"banned master sha must block upload, got {reason}")
        src = Path(__file__).resolve().parent.joinpath("youtube_upload.py").read_text(encoding="utf-8")
        if "abec4eb94199d0cbbf00659891d4e79c0040a6b1bb5450fa6e1db0e54c4b4d53" not in src:
            failures.append("upload adapter must keep the r249 truncated master sha locked")

        from youtube_upload import request_body
        body = request_body(report2)
        caps = body.get("local", {}).get("captions") or {}
        if caps.get("uploaded") is not False:
            failures.append("upload dry-run must not claim captions were uploaded")
        if "captions.insert is not called" not in str(caps.get("note", "")):
            failures.append(f"upload captions note missing, got {caps}")
        if "captions.insert" not in src:
            failures.append("upload adapter must keep captions.insert uncalled")
        thumbs = body.get("local", {}).get("thumbnail") or {}
        if thumbs.get("uploaded") is not False:
            failures.append("upload dry-run must not claim the thumbnail was uploaded")
        if "thumbnails.set is not called" not in str(thumbs.get("note", "")):
            failures.append(f"upload thumbnail note missing, got {thumbs}")
        if "thumbnails.set" not in src:
            failures.append("upload adapter must keep thumbnails.set uncalled")

        (p / "publish.md").write_text(
            "## Title to upload\n\nFixture title\n\n"
            "## Description\n\nNo upload happened. Human locks title, description, and tags before YouTube. "
            "Twelve more words so length alone would pass the word count gate.\n\n"
            "## Tags\n\n- fixture\n\n"
            "## Human before upload\n\n- [ ] Description edited for search + honesty\n",
            encoding="utf-8",
        )
        report_stub = inspect_upload(p, env={})
        if report_stub["gate"] in {"READY", "YOUTUBE_AUTH_REQUIRED"}:
            failures.append("stub publish description must not look credential-ready")
        if report_stub["action"] != "HOLD_LOCAL":
            failures.append(f"stub publish copy must HOLD_LOCAL, got {report_stub['action']}")
        names_stub = {c["name"]: c["ok"] for c in report_stub["checks"]}
        if names_stub.get("publish_copy_approved"):
            failures.append("stub description must fail publish_copy_approved")
        vo = p / "vo"
        vo.mkdir()
        take = vo / f"{p.name}-take-selected.wav"
        short = p / "export" / "master.mp4"
        import subprocess
        wav = subprocess.run(
            ["ffmpeg", "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "2", str(take)],
            capture_output=True,
        )
        mp4 = subprocess.run(
            [
                "ffmpeg", "-y", "-f", "lavfi", "-i", "color=c=black:s=320x180:d=2",
                "-f", "lavfi", "-i", "anullsrc=r=44100:cl=mono", "-t", "2",
                "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-shortest",
                str(short),
            ],
            capture_output=True,
        )
        if wav.returncode == 0 and mp4.returncode == 0 and short.is_file():
            report3 = inspect_upload(p, env={})
            names3 = {c["name"]: c for c in report3["checks"]}
            row = names3.get("not_truncated_end_screen")
            if not row or row["ok"]:
                failures.append(f"VO-length master must fail end screen, got {row}")
            if report3["gate"] in {"READY", "YOUTUBE_AUTH_REQUIRED"}:
                failures.append("VO-length master must not look upload-ready")
        else:
            failures.append("ffmpeg fixture for truncated end screen failed")
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



def check_timeline_card_match() -> list[str]:
    """Beat N must not collapse onto Beat 1 via the shared word 'beat'."""
    from timeline import match_card

    cards = [
        {"beat": "Hook (0:00-0:12)", "file": "cards/hook-card.png", "type": "text-card"},
        {"beat": "Payoff promise", "file": "cards/payoff-same.png", "type": "text-card"},
        {"beat": "Beat 1 —", "file": "cards/beat1-split.png", "type": "diagram"},
        {"beat": "Beat 2 —", "file": "cards/beat2-hand.png", "type": "text-card"},
        {"beat": "Beat 3 —", "file": "cards/beat3-four.png", "type": "text-card"},
        {"beat": "Beat 4 —", "file": "cards/beat4-night.png", "type": "text-card"},
        {"beat": "CTA", "file": "cards/cta-cta.png", "type": "text-card"},
    ]
    expect = {
        "Hook (0:00-0:12)": "cards/hook-card.png",
        "Payoff promise": "cards/payoff-same.png",
        "Beat 1 —": "cards/beat1-split.png",
        "Beat 2 —": "cards/beat2-hand.png",
        "Beat 3 —": "cards/beat3-four.png",
        "Beat 4 —": "cards/beat4-night.png",
        "CTA": "cards/cta-cta.png",
    }
    failures = []
    for title, file in expect.items():
        got = match_card(title, cards)
        if not got or got["file"] != file:
            failures.append(f"timeline match_card {title!r} -> {got}")
    return failures



def check_q1_board_not_record() -> list[str]:
    """Live Q1 board must not send the operator back to a new DROP take."""
    failures: list[str] = []
    row = {
        "name": "002-stop-deciding-what-to-work-on-every-morning",
        "status": "ready_for_vo",
        "title": "Stop Deciding",
        "gate": "FAIL",
        "errors": [],
        "incompletes": [],
        "disk": "disk",
        "present": 0,
        "missing": 1,
        "open_human": 2,
        "drift": [],
        "vo_state": "missing",
        "vo_drop": "videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav",
    }
    report = format_report([row])
    if "Do not record" not in report:
        failures.append("pipeline_status Q1 detail must say Do not record")
    if "delete 'No upload happened'" in report:
        failures.append("pipeline_status Q1 detail must not tell the operator to delete the drafted stub")
    if "Description edited" not in report or "First comment approved" not in report:
        failures.append("pipeline_status Q1 detail must name the two open boxes")
    if "DROP `" in report:
        failures.append("pipeline_status Q1 detail must not print a DROP path")
    other = dict(row)
    other["name"] = "sample-001-why-systems-beat-motivation"
    other_report = format_report([other])
    if "DROP `" not in other_report:
        failures.append("pipeline_status non-Q1 missing VO must still print DROP")
    return failures



def check_q1_publish_draft_locked() -> list[str]:
    """Live Q1 metadata must be approved by the delegated agent, never restored to the old stub."""
    failures: list[str] = []
    path = ROOT / "videos" / "002-stop-deciding-what-to-work-on-every-morning" / "publish.md"
    if not path.is_file():
        failures.append("Q1 publish.md missing")
        return failures
    text = path.read_text(encoding="utf-8")
    if "No upload happened" in text:
        failures.append("Q1 publish.md must not restore the stub sentence")
    if "en-US-AndrewNeural" not in text:
        failures.append("Q1 publish.md must label generated narration")
    if "- [x] Description edited for search + honesty" not in text:
        failures.append("Q1 Description edited box must be checked under delegated approval")
    if "- [x] First comment approved" not in text:
        failures.append("Q1 First comment approved box must be checked under delegated approval")
    if "delegated agent" not in text:
        failures.append("Q1 publish.md must record delegated approval")
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
    failures.extend(check_timeline_card_match())
    failures.extend(check_q1_board_not_record())
    failures.extend(check_q1_publish_draft_locked())
    failures.extend(check_caption_align_fail_closed())
    failures.extend(check_caption_review_fail_closed())
    failures.extend(check_chapter_draft_fail_closed())
    failures.extend(check_thumbnail_draft_fail_closed())
    failures.extend(check_live_capabilities())

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



def check_caption_align_fail_closed() -> list[str]:
    """Draft SRT requires a wav and must not invent cues without one."""
    import wave
    import struct
    from caption_align import build

    failures: list[str] = []
    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "videos" / "009-caption-fixture"
        # build() uses packet/vo when present; script lives beside it.
        packet = Path(tmp) / "009-caption-fixture"
        (packet / "vo").mkdir(parents=True)
        script = (
            "# Script\n\n"
            "## Hook\n\nWORDS: One next action.\n\n"
            "## CTA\n\nWORDS: Write the sentence tonight.\n"
        )
        (packet / "script.md").write_text(script, encoding="utf-8")
        try:
            build(packet)
            failures.append("caption_align must refuse a missing wav")
        except FileNotFoundError as exc:
            if "REFUSE" not in str(exc):
                failures.append(f"caption_align refuse should say REFUSE: {exc}")
        wav = packet / "vo" / "009-caption-fixture-take-selected.wav"
        rate = 8000
        def tone(seconds: float, amp: int) -> bytes:
            n = int(rate * seconds)
            return b"".join(struct.pack("<h", amp if (i // 20) % 2 == 0 else -amp) for i in range(n))
        pcm = tone(0.4, 8000) + tone(0.3, 0) + tone(0.4, 8000)
        with wave.open(str(wav), "wb") as handle:
            handle.setnchannels(1)
            handle.setsampwidth(2)
            handle.setframerate(rate)
            handle.writeframes(pcm)
        try:
            text, info = build(packet)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"caption_align should draft from a wav: {exc}")
            return failures
        if info.get("method") != "silence-proportional":
            failures.append(f"caption_align method drift: {info}")
        if "-->" not in text or info.get("cues", 0) < 1:
            failures.append("caption_align draft missing cues")
        if "Whisper" in text:
            failures.append("caption_align srt must not claim Whisper")
    return failures


def check_chapter_draft_fail_closed() -> list[str]:
    failures: list[str] = []
    import tempfile
    from chapter_draft import build

    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "videos" / "009-chapter-fixture"
        packet.mkdir(parents=True)
        (packet / "script.md").write_text(
            "## Hook\nWORDS:\nAlpha one starts the open.\n\n"
            "## Beat 1 —\nWORDS:\nBeta two names the stall in plain steps.\n\n"
            "## CTA\nWORDS:\nGamma three writes tomorrow sentence now.\n",
            encoding="utf-8",
        )
        try:
            build(packet)
            failures.append("chapter_draft must refuse a missing srt")
        except FileNotFoundError as exc:
            if "REFUSE" not in str(exc):
                failures.append(f"chapter_draft refuse should say REFUSE: {exc}")
        (packet / "captions.srt").write_text(
            "1\n00:00:00,000 --> 00:00:04,000\nAlpha one starts the open.\n\n"
            "2\n00:00:20,000 --> 00:00:24,000\nBeta two names the stall in plain steps.\n\n"
            "3\n00:00:40,000 --> 00:00:44,000\nGamma three writes tomorrow sentence now.\n\n",
            encoding="utf-8",
        )
        try:
            sheet, info = build(packet)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"chapter_draft should draft chapters: {exc}")
            return failures
        if info.get("approval") is not False:
            failures.append("chapter_draft must not approve")
        if "- [x]" in sheet:
            failures.append("chapter_draft must not check a box")
        if not info.get("lines") or not info["lines"][0].startswith("0:00"):
            failures.append(f"chapter_draft first line must be 0:00: {info}")
        if info.get("chapters", 0) < 3:
            failures.append("chapter_draft fixture should keep 3 chapters")
    q1 = Path(__file__).resolve().parents[1] / "videos" / "002-stop-deciding-what-to-work-on-every-morning"
    chapters = q1 / "chapters.md"
    publish = q1 / "publish.md"
    if chapters.is_file() and publish.is_file():
        sheet = chapters.read_text(encoding="utf-8")
        body = publish.read_text(encoding="utf-8")
        if "0:00 The reopen" not in sheet or "0:00 The reopen" not in body:
            failures.append("Q1 chapter draft missing from chapters.md or publish.md")
        if "- [x]" in sheet:
            failures.append("Q1 chapters.md must not check a box")
        if "- [x] Description edited for search + honesty" not in body:
            failures.append("chapter review must preserve the delegated approval state")
    return failures


def check_caption_review_fail_closed() -> list[str]:
    failures: list[str] = []
    import tempfile
    from caption_review import build

    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "videos" / "009-caption-review"
        packet.mkdir(parents=True)
        try:
            build(packet)
            failures.append("caption_review must refuse a missing srt")
        except FileNotFoundError as exc:
            if "REFUSE" not in str(exc):
                failures.append(f"caption_review refuse should say REFUSE: {exc}")
        srt = packet / "captions.srt"
        srt.write_text(
            "1\n00:00:00,000 --> 00:00:01,200\nShort line.\n\n"
            "2\n00:00:01,200 --> 00:00:03,000\n"
            "This line is definitely longer than forty two characters.\n\n",
            encoding="utf-8",
        )
        try:
            review, info = build(packet)
        except Exception as exc:  # noqa: BLE001
            failures.append(f"caption_review should draft a sheet: {exc}")
            return failures
        if info.get("approval") is not False:
            failures.append("caption_review must not approve")
        if "- [x]" in review:
            failures.append("caption_review must not check a box")
        if "not an approval" not in review:
            failures.append("caption_review must label itself not an approval")
        if info.get("flagged", 0) < 1:
            failures.append("caption_review should flag an overlong line")
    q1 = Path(__file__).resolve().parents[1] / "videos" / "002-stop-deciding-what-to-work-on-every-morning" / "captions.md"
    if q1.is_file():
        body = q1.read_text(encoding="utf-8")
        if "do not invent one here" in body:
            failures.append("Q1 captions.md still assigns inventing the srt")
        if "captions_review.md" not in body:
            failures.append("Q1 captions.md must point at the spot-check sheet")
    return failures




def check_live_capabilities() -> list[str]:
    failures: list[str] = []
    upload = (ROOT / "tools" / "youtube_upload.py").read_text(encoding="utf-8")
    feedback = (ROOT / "tools" / "youtube_feedback.py").read_text(encoding="utf-8")
    api = (ROOT / "tools" / "youtube_api.py").read_text(encoding="utf-8")
    materializer = (ROOT / "tools" / "materialize_q1_release.py").read_text(encoding="utf-8")
    for name, text in (("youtube_upload.py", upload), ("youtube_feedback.py", feedback)):
        if "--execute" not in text:
            failures.append(f"{name} must expose explicit --execute mode")
    for needle, label in (
        ("videos", "youtube_api video upload path"),
        ("analytics_report", "youtube_api analytics path"),
        ("list_comment_threads", "youtube_api comments path"),
        ("YOUTUBE_REFRESH_TOKEN", "youtube_api OAuth"),
    ):
        if needle not in api:
            failures.append(f"youtube_api.py missing {label}")
    for needle in ("758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2", "4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546", "q1-media-r249", "q1-media-r253"):
        if needle not in materializer:
            failures.append(f"Q1 materializer missing checksum/release guard: {needle}")
    return failures


def check_thumbnail_draft_fail_closed() -> list[str]:
    failures = []
    import tempfile
    from thumbnail_draft import build

    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "videos" / "009-thumb-fixture"
        packet.mkdir(parents=True)
        try:
            build(packet)
            failures.append("thumbnail_draft must refuse a missing brief")
        except SystemExit as exc:
            if "REFUSE:" not in str(exc):
                failures.append(f"thumbnail_draft refuse should say REFUSE: {exc}")
        (packet / "thumbnail.md").write_text("# Thumbnail\n\nOn-image text: One Written Default\n", encoding="utf-8")
        try:
            info = build(packet)
        except SystemExit as exc:
            failures.append(f"thumbnail_draft should render: {exc}")
            info = {}
        if info.get("approval") is not False:
            failures.append("thumbnail_draft must not approve")
        if info.get("uploaded") is not False:
            failures.append("thumbnail_draft must not claim upload")
        if info.get("width") != 1280 or info.get("height") != 720:
            failures.append(f"thumbnail_draft size drift: {info}")
        review = packet / "thumbnail_review.md"
        if review.is_file() and "- [x]" in review.read_text(encoding="utf-8"):
            failures.append("thumbnail_review must not check a box")
        png = packet / "thumbnail.png"
        if not png.is_file() or png.stat().st_size < 1000:
            failures.append("thumbnail_draft png missing")
    q1 = Path(__file__).resolve().parents[1] / "videos" / "002-stop-deciding-what-to-work-on-every-morning"
    sheet = q1 / "thumbnail_review.md"
    if sheet.is_file():
        raw = sheet.read_text(encoding="utf-8")
        if "approval: pending-evidence" not in raw:
            failures.append("Q1 thumbnail review must remain evidence-gated until the PNG is accessible")
        if not (q1 / "thumbnail.png").is_file():
            failures.append("Q1 thumbnail.png missing beside the review")
    return failures



if __name__ == "__main__":
    raise SystemExit(main())
