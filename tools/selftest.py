#!/usr/bin/env python3
"""Read-only fixture contract check.

Runs against videos/sample-001-* only. Writes nothing.
Purpose: future runs can prove validate/doctor/hint/set_status/apply_script
contracts instead of leaving runtime unverified.
"""

from __future__ import annotations

import os
import sys
import tempfile
from datetime import datetime, timedelta, timezone
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
from youtube_upload import artifact_block_reason, caption_timing_reason, content_rule_reason, file_sha256, inspect_upload, master_block_reason, metadata_block_reason, missing_provider_scopes, png_dimensions  # noqa: E402
from upload_variant_freeze import check_repo, check_texts  # noqa: E402

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
        from youtube_upload import synthetic_media_flag, vo_origin_kind
        if synthetic_media_flag("generated") is not True or synthetic_media_flag("human") is not False:
            failures.append("synthetic disclosure must be true for generated and false for human")
        if synthetic_media_flag("unknown") is not None:
            failures.append("unknown vo origin must not invent containsSyntheticMedia")
        (p / "vo_origin.md").write_text("kind: generated\n", encoding="utf-8")
        if vo_origin_kind(p) != "generated":
            failures.append("vo_origin.md kind generated must be read")
        body_gen = request_body({"packet": p.name, "export": "export/master.mp4", "fingerprint": "fixture", "meta": report2["meta"], "privacy": "private", "contains_synthetic_media": True, "captions": {}, "thumbnail": {}})
        if body_gen.get("status", {}).get("containsSyntheticMedia") is not True:
            failures.append("request_body must disclose generated narration")
        if "containsSyntheticMedia" not in src:
            failures.append("upload adapter must set status.containsSyntheticMedia")
        from youtube_upload import audience_designation, made_for_kids_flag
        if audience_designation() != "not_made_for_kids" or made_for_kids_flag("not_made_for_kids") is not False:
            failures.append("channel audience must stay not_made_for_kids until the channel decision changes")
        if made_for_kids_flag("made_for_kids") is not True or made_for_kids_flag("unknown") is not None:
            failures.append("unknown audience must not invent selfDeclaredMadeForKids")
        if body_gen.get("status", {}).get("selfDeclaredMadeForKids") is not False:
            failures.append("request_body must set selfDeclaredMadeForKids false for this channel")
        from youtube_upload import category_id, channel_license, ASSIGNABLE_CATEGORY_IDS, CHANNEL_LICENSES
        if category_id() != "27" or channel_license() != "youtube":
            failures.append("channel category_id must stay 27 and license youtube until the channel decision changes")
        if category_id(Path("/tmp")) != "unknown" or channel_license(Path("/tmp")) != "unknown":
            failures.append("missing channel.md must not invent category 27 or creativeCommon")
        if body_gen.get("snippet", {}).get("categoryId") != "27":
            failures.append("request_body must send channel categoryId 27")
        if body_gen.get("status", {}).get("license") != "youtube":
            failures.append("request_body must send channel license youtube")
        if '"categoryId": "27"' in src:
            failures.append("upload adapter must not hardcode categoryId 27")
        if "METADATA_REJECTED:category_unknown" not in src or "METADATA_REJECTED:license_unknown" not in src:
            failures.append("unknown category or license must be METADATA_REJECTED before the token refresh")
        if "category_known" not in src or "license_known" not in src:
            failures.append("inspect must HOLD_LOCAL on unknown category or license")
        api_src = Path(__file__).resolve().parent.joinpath("youtube_api.py").read_text(encoding="utf-8")
        if "setdefault(\"selfDeclaredMadeForKids\"" in api_src or "AUDIENCE_UNKNOWN" not in api_src:
            failures.append("upload transport must refuse a missing selfDeclaredMadeForKids instead of defaulting it")

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
        (p / "titles.md").write_text("Primary: GRIND harder today\n", encoding="utf-8")
        reason = content_rule_reason(p)
        if not reason or "title_scan" not in reason:
            failures.append(f"shouted title must fail content_rule_reason, got {reason}")
        report_shout = inspect_upload(p, env={})
        names_shout = {c["name"]: c for c in report_shout["checks"]}
        row_shout = names_shout.get("content_rules_clear")
        if not row_shout or row_shout["ok"]:
            failures.append(f"shouted title must fail content_rules_clear, got {row_shout}")
        if report_shout["gate"] in {"READY", "YOUTUBE_AUTH_REQUIRED"}:
            failures.append("shouted title must not look upload-ready")
        if "content_rules_clear" not in src:
            failures.append("upload hard local gates must include content_rules_clear")

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
        if report3["gate"] != "OBSERVATION_WINDOW_UNKNOWN":
            failures.append(
                f"feedback without uploaded_at must stay unknown, got {report3['gate']}"
            )
        if report3["action"] != "HOLD_WINDOW":
            failures.append(f"missing upload time must HOLD_WINDOW, got {report3['action']}")
        if report3["metrics"] is not None:
            failures.append("early window must not invent metrics")
        recent = (datetime.now(timezone.utc)).strftime("%Y-%m-%dT%H:%M:%SZ")
        with_id.write_text(
            '{"provider_video_id":"abc123","video_upload":{"uploaded_at":"%s"}}\n' % recent,
            encoding="utf-8",
        )
        report4 = inspect_feedback(p, env=dummy)
        if report4["gate"] != "OBSERVATION_WINDOW_NOT_DUE":
            failures.append(f"feedback inside 7d window must not be READY, got {report4['gate']}")
        if report4["action"] != "HOLD_WINDOW":
            failures.append(f"early collect must HOLD_WINDOW, got {report4['action']}")
        old = (datetime.now(timezone.utc) - timedelta(days=8)).strftime("%Y-%m-%dT%H:%M:%SZ")
        with_id.write_text(
            '{"provider_video_id":"abc123","video_upload":{"uploaded_at":"%s"}}\n' % old,
            encoding="utf-8",
        )
        report5 = inspect_feedback(p, env=dummy)
        if report5["gate"] != "READY":
            failures.append(f"feedback after window + OAuth env must be READY, got {report5['gate']}")
        if report5["action"] != "FETCH_BLOCKED_NO_NETWORK":
            failures.append(f"feedback READY action must stay offline, got {report5['action']}")
    return failures




def _solid_png(path: Path, width: int, height: int) -> None:
    import struct
    import zlib

    def chunk(tag: bytes, data: bytes) -> bytes:
        return struct.pack(">I", len(data)) + tag + data + struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)

    raw = b"".join(b"\x00" + (b"\xff\xff\xff" * width) for _ in range(height))
    ihdr = struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0)
    png = b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr) + chunk(b"IDAT", zlib.compress(raw)) + chunk(b"IEND", b"")
    path.write_bytes(png)


def check_artifact_limits() -> list[str]:
    failures = []
    packet = Path("/tmp/ca-artifact-limit")
    packet.mkdir(parents=True, exist_ok=True)
    for child in packet.iterdir():
        child.unlink()
    thumb = packet / "thumbnail.png"
    caps = packet / "captions.srt"
    thumb.write_bytes(b"not a png")
    if artifact_block_reason(packet) != "thumbnail_not_png":
        failures.append("non-png thumbnail must fail before videos.insert")
    _solid_png(thumb, 320, 180)
    reason = artifact_block_reason(packet)
    if reason != "thumbnail_too_small 320x180":
        failures.append(f"undersized thumbnail must fail closed, got {reason}")
    _solid_png(thumb, 640, 360)
    if png_dimensions(thumb) != (640, 360):
        failures.append("png IHDR reader must return width and height")
    if artifact_block_reason(packet) is not None:
        failures.append("640x360 png under 2MB must pass the artifact gate")
    caps.write_text("no timestamps here\n", encoding="utf-8")
    if artifact_block_reason(packet) != "captions_missing_timestamp":
        failures.append("caption file without a cue timestamp must fail closed")
    caps.write_text("1\n00:00:00,000 --> 00:00:01,000\nHello\n", encoding="utf-8")
    if artifact_block_reason(packet) is not None:
        failures.append("valid caption cue must pass the artifact gate")
    caps.write_text("1\n00:00:02,000 --> 00:00:01,000\nBackwards\n", encoding="utf-8")
    if artifact_block_reason(packet) != "captions_cue_not_forward":
        failures.append("a backward caption cue must fail before videos.insert")
    caps.write_text(
        "1\n00:00:01,000 --> 00:00:02,000\nLater\n\n2\n00:00:00,000 --> 00:00:01,000\nEarlier\n",
        encoding="utf-8",
    )
    if artifact_block_reason(packet) != "captions_cues_out_of_order":
        failures.append("out-of-order caption cues must fail before videos.insert")
    caps.write_text(
        "1\n00:00:00,000 --> 00:00:02,000\nFirst\n\n2\n00:00:01,000 --> 00:00:03,000\nOverlap\n",
        encoding="utf-8",
    )
    if artifact_block_reason(packet) != "captions_cues_overlap":
        failures.append("overlapping caption cues must fail before videos.insert")
    if caption_timing_reason("1\n00:00:05,000 --> 00:00:06,000\nPast\n", 3.0) != "captions_past_video 6.00>4.00":
        failures.append("a cue past the known master must fail before videos.insert")
    caps.write_text("1\n00:00:00,000 --> 00:00:01,000\nHello\n", encoding="utf-8")
    long_comment = {"pin_comment": "x" * 10001}
    if artifact_block_reason(packet, long_comment) != "comment_too_long 10001>10000":
        failures.append("pin comment over 10000 characters must fail closed")
    thumb.write_bytes(b"\x89PNG\r\n\x1a\n" + b"0" * (2 * 1024 * 1024))
    reason = artifact_block_reason(packet)
    if not reason or not reason.startswith("thumbnail_too_large"):
        failures.append(f"thumbnail over 2MB must fail closed, got {reason}")
    from youtube_upload import png_has_iend
    _solid_png(thumb, 640, 360)
    raw = thumb.read_bytes()
    thumb.write_bytes(raw[:-12])
    if png_has_iend(thumb):
        failures.append("a PNG missing IEND must not count as complete")
    if artifact_block_reason(packet) != "thumbnail_truncated_png":
        failures.append("a truncated PNG must fail before videos.insert")
    return failures


def check_upload_stamp_preserved() -> list[str]:
    failures: list[str] = []
    from youtube_upload import preserved_upload_stamp
    if preserved_upload_stamp(None) is not None:
        failures.append("missing prior must not invent uploaded_at")
    if preserved_upload_stamp({"generated": "2026-01-01T00:00:00Z"}) is not None:
        failures.append("generated field must not become uploaded_at")
    stamp = "2026-09-01T12:00:00Z"
    got = preserved_upload_stamp({"video_upload": {"status": "uploaded", "uploaded_at": stamp}})
    if got != stamp:
        failures.append(f"resume must keep video_upload.uploaded_at, got {got}")
    got2 = preserved_upload_stamp({"uploaded_at": stamp})
    if got2 != stamp:
        failures.append(f"resume must keep top-level uploaded_at, got {got2}")
    from youtube_upload import incomplete_post_uploads
    if incomplete_post_uploads({"caption_upload": {"status": "uploaded"}, "thumbnail_upload": {"status": "uploaded"}}) != []:
        failures.append("finished caption and thumbnail must not be incomplete")
    failed = incomplete_post_uploads({"caption_upload": {"status": "failed"}, "thumbnail_upload": {"status": "not_attempted"}})
    if failed != ["captions"]:
        failures.append(f"failed captions must fail closed, got {failed}")
    if incomplete_post_uploads({"caption_upload": {"status": "not_attempted"}}) != []:
        failures.append("missing caption attempt must not be treated as a failed upload")
    from youtube_upload import should_post_comment
    approved = {"pin_comment": "Write tomorrow's next action on the card.", "comment_approved": True}
    if not should_post_comment(approved):
        failures.append("approved pin comment must post on execute without a second flag")
    if should_post_comment(approved, skipped=True):
        failures.append("skip-comment must opt out of the approved pin post")
    if should_post_comment({"pin_comment": "draft", "comment_approved": False}):
        failures.append("unchecked first comment must not post")
    if should_post_comment({"pin_comment": "", "comment_approved": True}):
        failures.append("empty pin comment must stay missing")
    if should_post_comment(approved, requested=True, skipped=True):
        failures.append("skip-comment must win over an extra post-comment request")
    upload_src = (TOOLS / "youtube_upload.py").read_text(encoding="utf-8")
    if '"pinned": False' not in upload_src:
        failures.append("posted comment must stay unpinned; Data API insert is not a Studio pin")
    from youtube_upload import existing_upload_action, fingerprint
    prior = {
        "provider_video_id": "abc123",
        "fingerprint": "same",
        "caption_upload": {"status": "failed"},
        "thumbnail_upload": {"status": "not_attempted"},
    }
    if existing_upload_action(prior, "same", caption_file=True, thumbnail_file=True) != "resume":
        failures.append("failed caption with a video id must resume, not finish")
    done = {
        "provider_video_id": "abc123",
        "fingerprint": "same",
        "caption_upload": {"status": "uploaded"},
        "thumbnail_upload": {"status": "uploaded"},
    }
    if existing_upload_action(done, "same", caption_file=True, thumbnail_file=True) != "finished":
        failures.append("completed post-upload must stay idempotent")
    if existing_upload_action(done, "other", caption_file=True, thumbnail_file=True) != "mismatch":
        failures.append("changed export identity must not upload a second video")
    if existing_upload_action(None, "same", caption_file=True, thumbnail_file=True) != "none":
        failures.append("missing prior must not look like an existing video")
    left = Path(tempfile.mkdtemp()) / "export.mp4"
    left.write_bytes(b"same-master-bytes")
    right = Path(tempfile.mkdtemp()) / "export.mp4"
    right.write_bytes(b"same-master-bytes")
    import os
    os.utime(left, (1_700_000_000, 1_700_000_000))
    os.utime(right, (1_800_000_000, 1_800_000_000))
    meta = {"title": "t", "description": "d"}
    if fingerprint(Path("packet"), meta, left) != fingerprint(Path("packet"), meta, right):
        failures.append("fingerprint must ignore mtime so rematerialize does not duplicate")
    if fingerprint(Path("packet"), meta, left) == fingerprint(Path("packet"), meta, None):
        failures.append("fingerprint must include export bytes")
    upload_src = Path(__file__).resolve().parent.joinpath("youtube_upload.py").read_text(encoding="utf-8")
    if "st_mtime" in upload_src.split("def fingerprint", 1)[1].split("def existing_upload_action", 1)[0]:
        failures.append("fingerprint must not read mtime")
    if 'gate = "RESUME"' not in upload_src or "RESUME_POST_UPLOAD" not in upload_src:
        failures.append("inspect must expose a resume gate for incomplete post-upload")
    if "EXISTING_VIDEO_FINGERPRINT_MISMATCH" not in upload_src:
        failures.append("execute must refuse a second upload when the fingerprint drifted")
    if metadata_block_reason({"title": "ok", "description": "d", "tags": ["one"]}) is not None:
        failures.append("short metadata must pass provider limits")
    if metadata_block_reason({"title": "   ", "description": "d", "tags": ["one"]}) != "title_empty":
        failures.append("empty title must fail before videos.insert")
    if metadata_block_reason({"title": "bad <title>", "description": "d", "tags": ["one"]}) != "title_invalid_characters":
        failures.append("title angle brackets must fail before videos.insert")
    if metadata_block_reason({"title": "x" * 101, "description": "d", "tags": ["one"]}) is None:
        failures.append("title over 100 characters must fail before videos.insert")
    if metadata_block_reason({"title": "ok", "description": "d" * 5001, "tags": ["one"]}) is None:
        failures.append("description over 5000 characters must fail before videos.insert")
    if metadata_block_reason({"title": "ok", "description": "d", "tags": ["t"] * 13}) is None:
        failures.append("more than 12 tags must fail instead of being sliced")
    if metadata_block_reason({"title": "ok", "description": "d", "tags": ["bad,tag"]}) is None:
        failures.append("a comma inside a tag must fail")
    spaced = ["ab cd" * 8] * 12
    if sum(len(tag) for tag in spaced) > 500:
        failures.append("tag budget fixture must stay under a raw 500 sum")
    if metadata_block_reason({"title": "ok", "description": "d", "tags": spaced}) is None:
        failures.append("quoted spaces and tag commas must count toward the 500 limit")
    if metadata_block_reason({"title": "ok", "description": "d", "tags": ["focused work", "deep work"]}) is not None:
        failures.append("short spaced tags must still pass")
    upload_only = {"https://www.googleapis.com/auth/youtube.upload"}
    full = {"https://www.googleapis.com/auth/youtube"}
    both = upload_only | {"https://www.googleapis.com/auth/youtube.force-ssl"}
    if missing_provider_scopes(upload_only, captions=True, thumbnail=True, comment=False) != [
        "https://www.googleapis.com/auth/youtube.force-ssl"
    ]:
        failures.append("upload-only token must refuse captions before insert")
    if missing_provider_scopes(both, captions=True, thumbnail=True, comment=False):
        failures.append("upload plus force-ssl must pass caption and thumbnail")
    if missing_provider_scopes(full, captions=True, thumbnail=True, comment=True):
        failures.append("full youtube scope must cover upload, captions, and comment")
    if missing_provider_scopes(set(), captions=False, thumbnail=False, comment=False) != [
        "https://www.googleapis.com/auth/youtube.upload"
    ]:
        failures.append("empty grant must refuse videos.insert")
    if "tags[:12]" in upload_src or '["tags"][:12]' in upload_src:
        failures.append("upload must not silently drop tags")
    if "METADATA_REJECTED" not in upload_src or "PRIVACY_NOT_PRIVATE" not in upload_src:
        failures.append("execute must refuse invalid metadata and non-private privacy before the token refresh")
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
        (p / "feedback_state.json").write_text(
            '{"gate":"COLLECTED","attempted_fetch":true,"provider_video_id":"other","metrics":[{"views":1}]}\n',
            encoding="utf-8",
        )
        report3 = inspect_experiment(p, env={})
        if report3["gate"] != "HOLD_NO_EVIDENCE":
            failures.append(
                f"mismatched feedback video id must stay HOLD_NO_EVIDENCE, got {report3['gate']}"
            )
        if (report3.get("record") or {}).get("result") is not None:
            failures.append("mismatched feedback must not invent a result")
        (p / "feedback_state.json").write_text(
            '{"gate":"COLLECTED","attempted_fetch":true,"provider_video_id":"abc123","metrics":[{"views":4,"averageViewPercentage":32.0}]}\n',
            encoding="utf-8",
        )
        report4 = inspect_experiment(p, env={})
        if report4["gate"] != "READY_TO_COMPARE":
            failures.append(
                f"collected matching metrics must be READY_TO_COMPARE, got {report4['gate']}"
            )
        if report4.get("action") != "COMPARE_BLOCKED_NO_BASELINE":
            failures.append(f"collected metrics must not decide, got {report4.get('action')}")
        if (report4.get("record") or {}).get("result") is not None:
            failures.append("collected metrics must not invent a keep/discard")
        if (report4.get("record") or {}).get("observed_metrics") != [{"views": 4, "averageViewPercentage": 32.0}]:
            failures.append("collected metrics were not passed through")
        (p / "experiment_baseline.json").write_text(
            '{"hypothesis":"x","change":"not-a-variable","primary_metric":"views","baseline":1,"source":"invented"}\n',
            encoding="utf-8",
        )
        report5 = inspect_experiment(p, env={})
        if report5.get("action") != "COMPARE_BLOCKED_NO_BASELINE":
            failures.append(f"rejected baseline must stay blocked, got {report5.get('action')}")
        if (report5.get("record") or {}).get("result") is not None:
            failures.append("rejected baseline must not invent a result")
        (p / "experiment_baseline.json").write_text(
            '{"hypothesis":"A narrower hook holds average view percentage","change":"hook","primary_metric":"averageViewPercentage","baseline":28.0,"source":"Q0 private upload analytics export 2026-09-01"}\n',
            encoding="utf-8",
        )
        report6 = inspect_experiment(p, env={})
        if report6.get("action") != "COMPARED":
            failures.append(f"documented baseline with metric must be COMPARED, got {report6.get('action')}")
        rec6 = report6.get("record") or {}
        if rec6.get("result") is not None or rec6.get("decision") != "pending":
            failures.append("documented baseline must not decide keep/discard")
        if rec6.get("change") != "hook" or rec6.get("baseline") != 28.0:
            failures.append("documented baseline fields were not passed through")
        comparison = rec6.get("comparison") or {}
        if comparison.get("observed") != 32.0 or comparison.get("delta") != 4.0:
            failures.append(f"primary metric delta was not computed, got {comparison}")
        if comparison.get("direction") != "higher" or comparison.get("decision") != "pending":
            failures.append("comparison must stay pending and directional")
        (p / "experiment_baseline.json").write_text(
            '{"hypothesis":"A narrower hook holds average view percentage","change":"hook","primary_metric":"missingMetric","baseline":28.0,"source":"Q0 private upload analytics export 2026-09-01"}\n',
            encoding="utf-8",
        )
        report7 = inspect_experiment(p, env={})
        if report7.get("action") != "COMPARE_BLOCKED_METRIC":
            failures.append(f"missing primary metric must stay blocked, got {report7.get('action')}")
        if (report7.get("record") or {}).get("comparison") is not None:
            failures.append("missing primary metric must not invent a comparison")
        if (report7.get("record") or {}).get("decision") != "pending":
            failures.append("missing primary metric must not decide")
        (p / "experiment_decision.json").write_text(
            '{"decision":"keep","reason":"looks better","source":"invented"}\n',
            encoding="utf-8",
        )
        report8 = inspect_experiment(p, env={})
        if report8.get("action") != "COMPARE_BLOCKED_METRIC":
            failures.append(f"decision without comparison must stay blocked, got {report8.get('action')}")
        if (report8.get("record") or {}).get("result") is not None:
            failures.append("decision without comparison must not record a result")
        (p / "experiment_baseline.json").write_text(
            '{"hypothesis":"A narrower hook holds average view percentage","change":"hook","primary_metric":"averageViewPercentage","baseline":28.0,"source":"Q0 private upload analytics export 2026-09-01"}\n',
            encoding="utf-8",
        )
        report9 = inspect_experiment(p, env={})
        if report9.get("action") != "COMPARED":
            failures.append(f"invented decision source must stay COMPARED, got {report9.get('action')}")
        if (report9.get("record") or {}).get("decision") != "pending":
            failures.append("invented decision source must not decide")
        (p / "experiment_decision.json").write_text(
            '{"decision":"keep","reason":"average view percentage rose 4 points versus the documented Q0 export","source":"operator review after COMPARED 2026-10-09","primary_metric":"averageViewPercentage"}\n',
            encoding="utf-8",
        )
        report10 = inspect_experiment(p, env={})
        rec10 = report10.get("record") or {}
        if report10.get("action") != "DECISION_RECORDED":
            failures.append(f"explicit decision must be DECISION_RECORDED, got {report10.get('action')}")
        if rec10.get("decision") != "keep" or rec10.get("result") != "keep":
            failures.append("explicit decision was not recorded")
        if rec10.get("decision_source") != "operator review after COMPARED 2026-10-09":
            failures.append("decision source was not passed through")
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





def check_persist_provider_state() -> list[str]:
    """A provider video id must be committed, and a rejected push must retry without force."""
    failures: list[str] = []
    import persist_provider_state as persist

    if persist.upload_commit_decision({"provider_video_id": "abc"}) != "commit_provider_video_id":
        failures.append("upload state with a provider id must be committed")
    if persist.upload_commit_decision({"error_class": "RESUMABLE_SESSION_EXPIRED"}) != "skip_transient":
        failures.append("transient upload failure must not be committed")
    gone = persist.upload_commit_decision(
        {
            "completed_without_id": True,
            "error_class": "RESUMABLE_COMPLETED_SESSION_GONE",
        }
    )
    if gone != "commit_completed_without_id":
        failures.append("completed-without-id hold must be committed")
    if persist.feedback_commit_decision({"gate": "COLLECTED", "attempted_fetch": True, "provider_video_id": "abc"}) != "commit_collected":
        failures.append("collected feedback with a provider id must be committed")
    if persist.feedback_commit_decision({"gate": "COLLECTED", "attempted_fetch": False, "provider_video_id": "abc"}) != "skip_not_collected":
        failures.append("dry-run feedback must not be committed")
    if not persist.push_needs_retry("failed to push some refs: updates were rejected"):
        failures.append("non-fast-forward push must be retried")
    if persist.push_needs_retry("protected branch"):
        failures.append("unrelated push failure must not be treated as a retry")
    calls: list[list[str]] = []

    def run(cmd):
        calls.append(cmd)
        if cmd[:2] == ["git", "push"] and sum(1 for c in calls if c[:2] == ["git", "push"]) == 1:
            return 1, "", "failed to push some refs: non-fast-forward"
        if cmd[:3] == ["git", "rev-parse", "--is-shallow-repository"]:
            return 0, "false\n", ""
        return 0, "", ""

    if persist.push_with_retry(run) != "pushed":
        failures.append("rejected push must succeed after fetch and rebase")
    if ["git", "push", "--force", "origin", "HEAD:main"] in calls or any("--force" in part for cmd in calls for part in cmd):
        failures.append("persist must not force-push")
    if calls[1:4] != [
        ["git", "rev-parse", "--is-shallow-repository"],
        ["git", "fetch", "origin", "main"],
        ["git", "rebase", "origin/main"],
    ]:
        failures.append(f"persist retry order drift: {calls}")
    shallow_calls: list[list[str]] = []

    def shallow_run(cmd):
        shallow_calls.append(cmd)
        if cmd[:2] == ["git", "push"] and sum(1 for c in shallow_calls if c[:2] == ["git", "push"]) == 1:
            return 1, "", "updates were rejected"
        if cmd[:3] == ["git", "rev-parse", "--is-shallow-repository"]:
            return 0, "true\n", ""
        return 0, "", ""

    if persist.push_with_retry(shallow_run) != "pushed":
        failures.append("shallow rejected push must succeed after unshallow and rebase")
    if shallow_calls[1:5] != [
        ["git", "rev-parse", "--is-shallow-repository"],
        ["git", "fetch", "--unshallow", "origin"],
        ["git", "fetch", "origin", "main"],
        ["git", "rebase", "origin/main"],
    ]:
        failures.append(f"shallow persist retry order drift: {shallow_calls}")
    src = (TOOLS / "persist_provider_state.py").read_text(encoding="utf-8")
    if "--unshallow" not in src or "--is-shallow-repository" not in src:
        failures.append("persist must unshallow a shallow checkout before rebase")
    workflow = (ROOT / ".github" / "workflows" / "youtube-production.yml").read_text(encoding="utf-8")
    if "tools/persist_provider_state.py" not in workflow:
        failures.append("production workflow must classify state before commit")
    if "git push origin HEAD:main" in workflow or "git push --force" in workflow:
        failures.append("production workflow must not bare-push or force-push provider state")
    if "push_with_retry" not in workflow:
        failures.append("production workflow must retry a rejected provider-state push")
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
    if "already approved" not in report:
        failures.append("pipeline_status Q1 detail must say publish copy is already approved")
    if "check Description edited" in report or "still unchecked" in report:
        failures.append("pipeline_status Q1 detail must not send the operator to re-check approved boxes")
    if "Description edited" not in report or "First comment approved" not in report:
        failures.append("pipeline_status Q1 detail must name the approved boxes")
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



def check_oauth_setup_recipe() -> list[str]:
    """The setup recipe must name the secrets and scopes and must not print values."""
    failures = []
    path = ROOT / "tools" / "oauth_setup.py"
    source = path.read_text(encoding="utf-8")
    for name in ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"):
        if name not in source:
            failures.append(f"oauth setup recipe missing {name}")
    for scope in (
        "https://www.googleapis.com/auth/youtube.upload",
        "https://www.googleapis.com/auth/youtube.force-ssl",
        "https://www.googleapis.com/auth/yt-analytics.readonly",
    ):
        if scope not in source:
            failures.append(f"oauth setup recipe missing {scope}")
    if "print(os.environ" in source or "os.environ.get(name" not in source:
        failures.append("oauth setup recipe must check presence without printing values")
    if "gh secret set" not in source:
        failures.append("oauth setup recipe must name gh secret set")
    sys.path.insert(0, str(ROOT / "tools"))
    import oauth_setup
    text = oauth_setup.recipe()
    if "youtube.upload alone" not in text:
        failures.append("oauth setup recipe must warn against an upload-only token")
    saved = {name: os.environ.get(name) for name in oauth_setup.SECRET_NAMES}
    try:
        for name in oauth_setup.SECRET_NAMES:
            os.environ.pop(name, None)
        if oauth_setup.missing_names() != list(oauth_setup.SECRET_NAMES):
            failures.append("oauth setup must report all three names missing when unset")
        os.environ["YOUTUBE_CLIENT_ID"] = "not-a-real-client"
        os.environ["YOUTUBE_CLIENT_SECRET"] = "not-a-real-secret"
        os.environ["YOUTUBE_REFRESH_TOKEN"] = "not-a-real-token"
        if oauth_setup.missing_names():
            failures.append("oauth setup must treat non-empty values as present")
        rendered = oauth_setup.recipe()
        if "not-a-real" in rendered:
            failures.append("oauth setup recipe must not echo env values")
    finally:
        for name, value in saved.items():
            if value is None:
                os.environ.pop(name, None)
            else:
                os.environ[name] = value
    return failures






def check_title_scan() -> list[str]:
    """Shouted titles must refuse ready_for_vo and must not rewrite Q1."""
    import subprocess
    contract = ROOT / "tools" / "title_scan_contract.py"
    if not contract.is_file():
        return ["title_scan_contract.py missing"]
    proc = subprocess.run([sys.executable, str(contract)], cwd=ROOT, text=True, capture_output=True)
    if proc.returncode != 0 or "TITLE SCAN CONTRACT PASS" not in proc.stdout:
        return [f"title_scan_contract failed: {proc.stdout[-400:]} {proc.stderr[-200:]}"]
    return []


def check_claim_scan() -> list[str]:
    """Unsourced spoken claims must refuse ready_for_vo and must not rewrite Q1."""
    import subprocess
    contract = ROOT / "tools" / "claim_scan_contract.py"
    if not contract.is_file():
        return ["claim_scan_contract.py missing"]
    proc = subprocess.run([sys.executable, str(contract)], cwd=ROOT, text=True, capture_output=True)
    if proc.returncode != 0 or "CLAIM SCAN CONTRACT PASS" not in proc.stdout:
        return [f"claim_scan_contract failed: {proc.stdout[-400:]} {proc.stderr[-200:]}"]
    return []


def check_quality_scan() -> list[str]:
    """Anti-slop scan must report hits and must not rewrite script.md."""
    import subprocess
    contract = ROOT / "tools" / "quality_scan_contract.py"
    if not contract.is_file():
        return ["quality_scan_contract.py missing"]
    proc = subprocess.run([sys.executable, str(contract)], cwd=ROOT, text=True, capture_output=True)
    if proc.returncode != 0 or "QUALITY SCAN CONTRACT PASS" not in proc.stdout:
        return [f"quality_scan_contract failed: {proc.stdout[-400:]} {proc.stderr[-200:]}"]
    return []


def check_stall_watch() -> list[str]:
    """Instruction-lock and Studio stalls must stay machine-visible."""
    import subprocess
    contract = ROOT / "tools" / "stall_watch_contract.py"
    if not contract.is_file():
        return ["stall_watch_contract.py missing"]
    proc = subprocess.run([sys.executable, str(contract)], cwd=ROOT, text=True, capture_output=True)
    if proc.returncode != 0 or "STALL WATCH CONTRACT PASS" not in proc.stdout:
        return [f"stall_watch_contract failed: {proc.stdout[-400:]} {proc.stderr[-200:]}"]
    return []


def check_idea_gate() -> list[str]:
    """fill-idea must name apply_idea and must not tell the operator to paste by hand."""
    import subprocess
    contract = ROOT / "tools" / "idea_gate_contract.py"
    if not contract.is_file():
        return ["idea_gate_contract.py missing"]
    proc = subprocess.run([sys.executable, str(contract)], cwd=ROOT, text=True, capture_output=True)
    if proc.returncode != 0 or "IDEA GATE CONTRACT PASS" not in proc.stdout:
        return [f"idea_gate_contract failed: {proc.stdout[-400:]} {proc.stderr[-200:]}"]
    return []

def check_apply_idea() -> list[str]:
    """Blank idea.md fill must stay fail-closed and must not scaffold Q2."""
    import subprocess
    failures = []
    tool = ROOT / "tools" / "apply_idea.py"
    contract = ROOT / "tools" / "apply_idea_contract.py"
    if not tool.is_file():
        return ["apply_idea.py missing"]
    if not contract.is_file():
        return ["apply_idea_contract.py missing"]
    proc = subprocess.run([sys.executable, str(contract)], cwd=ROOT, text=True, capture_output=True)
    if proc.returncode != 0 or "APPLY IDEA CONTRACT PASS" not in proc.stdout:
        failures.append(f"apply_idea_contract failed: {proc.stdout[-400:]} {proc.stderr[-200:]}")
    return failures


def check_packet_path() -> list[str]:
    import subprocess
    contract = ROOT / "tools" / "packet_path_contract.py"
    if not contract.is_file():
        return ["packet_path_contract.py missing"]
    proc = subprocess.run([sys.executable, str(contract)], cwd=ROOT, text=True, capture_output=True)
    if proc.returncode != 0:
        return [f"packet_path_contract failed: {proc.stdout[-400:]} {proc.stderr[-200:]}"]
    return []

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
    failures.extend(check_resumable_video_upload())
    failures.extend(check_artifact_limits())
    failures.extend(check_feedback_fail_closed())
    failures.extend(check_upload_stamp_preserved())
    failures.extend(check_experiment_fail_closed())
    failures.extend(check_complete_fail_closed())
    failures.extend(check_timeline_card_match())
    failures.extend(check_q1_board_not_record())
    failures.extend(check_q1_publish_draft_locked())
    failures.extend(check_persist_provider_state())
    failures.extend(check_caption_align_fail_closed())
    failures.extend(check_caption_review_fail_closed())
    failures.extend(check_chapter_draft_fail_closed())
    failures.extend(check_chapter_sync_before_insert())
    failures.extend(check_thumbnail_draft_fail_closed())
    failures.extend(check_live_capabilities())
    failures.extend(check_oauth_setup_recipe())
    failures.extend(check_job_timeout_covers_upload())
    failures.extend(check_caption_waits_for_processing())
    failures.extend(check_upload_variant_freeze())
    failures.extend(check_stall_watch())
    failures.extend(check_prove_locks_on_push())
    failures.extend(check_apply_idea())
    failures.extend(check_idea_gate())
    failures.extend(check_quality_scan())
    failures.extend(check_claim_scan())
    failures.extend(check_title_scan())
    failures.extend(check_packet_path())
    failures.extend(check_stall_watch())

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



def check_chapter_sync_before_insert() -> list[str]:
    """Drafted chapter lines must be in the description before videos.insert."""
    failures: list[str] = []
    import tempfile
    from youtube_upload import chapter_sync_reason

    with tempfile.TemporaryDirectory() as tmp:
        packet = Path(tmp) / "videos" / "009-chapter-sync"
        packet.mkdir(parents=True)
        (packet / "chapters.md").write_text(
            "# Chapter draft\n\n## YouTube lines\n\n"
            "0:00 The reopen\n"
            "0:24 The stall\n"
            "1:25 Install the default\n",
            encoding="utf-8",
        )
        good = "Intro.\n\n0:00 The reopen\n0:24 The stall\n1:25 Install the default\n"
        if chapter_sync_reason(packet, good) is not None:
            failures.append("aligned chapter lines must pass")
        missing = chapter_sync_reason(packet, "Intro only.\n")
        if missing != "chapter_line_missing_from_description":
            failures.append(f"dropped chapter line drift: {missing}")
        short = "0:00 The reopen\n0:05 The stall\n1:25 Install the default\n"
        (packet / "chapters.md").write_text(
            "# Chapter draft\n\n## YouTube lines\n\n"
            "0:00 The reopen\n0:05 The stall\n1:25 Install the default\n",
            encoding="utf-8",
        )
        gap = chapter_sync_reason(packet, short)
        if gap != "chapter_gap_under_10s":
            failures.append(f"short chapter gap drift: {gap}")
        if chapter_sync_reason(packet.parent, good) is not None:
            failures.append("missing chapters.md must stay missing")
    q1 = Path(__file__).resolve().parents[1] / "videos" / "002-stop-deciding-what-to-work-on-every-morning"
    if (q1 / "chapters.md").is_file() and (q1 / "publish.md").is_file():
        from youtube_upload import parse_publish
        meta = parse_publish((q1 / "publish.md").read_text(encoding="utf-8"))
        reason = chapter_sync_reason(q1, meta.get("description") or "")
        if reason is not None:
            failures.append(f"Q1 chapter sync failed: {reason}")
    src = (Path(__file__).resolve().parent / "youtube_upload.py").read_text(encoding="utf-8")
    if "METADATA_REJECTED:{chapter_block}" not in src:
        failures.append("execute must refuse a drifted chapter list before insert")
    if "chapters_in_description" not in src:
        failures.append("inspect must report chapter sync")
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
    for needle in (
        "758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2",
        "4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546",
        "q1-media-r249",
        "q1-media-r253",
        "ignore_truncated_r249_master",
        "ignored known-truncated r249 q1-master.mp4",
    ):
        if needle not in materializer:
            failures.append(f"Q1 materializer missing checksum/release guard: {needle}")
    if "ignore_truncated_r249_master(r249)" not in materializer:
        failures.append("materializer must ignore the bundled truncated r249 master before copying wav/cards")
    workflow = (ROOT / ".github" / "workflows" / "youtube-production.yml").read_text(encoding="utf-8")
    if "tools/oauth_preflight.py" not in workflow:
        failures.append("production workflow must fail fast on missing OAuth before materialize")
    if workflow.find("tools/oauth_preflight.py") > workflow.find("tools/materialize_q1_release.py"):
        failures.append("oauth preflight must run before materialize")
    if "collect_feedback:" not in workflow or "default: false" not in workflow:
        failures.append("production workflow must keep collect_feedback default off")
    if "tools/youtube_feedback.py" not in workflow or "--execute" not in workflow:
        failures.append("production workflow must call youtube_feedback.py --execute only from the collect step")
    if workflow.find("tools/youtube_feedback.py") < workflow.find("tools/youtube_upload.py"):
        failures.append("feedback collect must stay after the upload step")
    if "inputs.collect_feedback == true" not in workflow:
        failures.append("feedback collect must be gated on collect_feedback")
    if "inputs.execute == true || inputs.collect_feedback == true" not in workflow:
        failures.append("oauth preflight must cover execute and collect_feedback")
    if "always() && inputs.execute == true" not in workflow:
        failures.append("upload state persist must run after a post-upload failure")
    if "inputs.collect_feedback == true && inputs.execute != true" not in workflow:
        failures.append("collect must not run in the same dispatch as execute")
    if "SCOPE_INSUFFICIENT" not in upload or "missing_provider_scopes" not in upload:
        failures.append("execute must refuse captions before insert when force-ssl is missing")
    if "POST_UPLOAD_INCOMPLETE" not in upload:
        failures.append("upload execute must fail closed when caption or thumbnail fails")
    if "RESUME_POST_UPLOAD" not in upload:
        failures.append("upload must resume incomplete post-upload instead of holding idempotent")
    if "st_mtime" in upload.split("def fingerprint", 1)[1].split("def existing_upload_action", 1)[0]:
        failures.append("production fingerprint must not depend on export mtime")
    if "OBSERVATION_WINDOW_NOT_DUE" not in feedback:
        failures.append("feedback collect must refuse an early observation window")
    from oauth_preflight import presence
    empty = presence({})
    if any(empty.values()) or set(empty) != {"YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN"}:
        failures.append(f"oauth preflight empty env drift: {empty}")
    filled = presence({key: "x" for key in empty})
    if not all(filled.values()):
        failures.append("oauth preflight must treat non-empty values as present")
    blank = presence({key: "  " for key in empty})
    if any(blank.values()):
        failures.append("oauth preflight must treat blank values as missing")
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




def check_resumable_video_upload() -> list[str]:
    """videos.insert must use resumable chunks, not one multipart POST of the master."""
    failures: list[str] = []
    import json
    import tempfile

    import youtube_api

    source = (ROOT / "tools" / "youtube_api.py").read_text(encoding="utf-8")
    if 'uploadType": "multipart"' in source.split("def upload_video", 1)[-1].split("def insert_caption", 1)[0]:
        failures.append("upload_video must not use multipart")
    if "uploadType=resumable" not in source and 'uploadType": "resumable"' not in source:
        failures.append("upload_video must start a resumable session")
    if youtube_api.resume_offset("bytes=0-262143", 0) != 262144:
        failures.append("resume_offset must continue after the last received byte")
    if youtube_api.resume_offset(None, 9) != 9:
        failures.append("resume_offset must keep the fallback when Range is missing")
    if youtube_api.RESUMABLE_CHUNK % (256 * 1024) != 0:
        failures.append("resumable chunk must be a multiple of 256 KiB")

    calls: list[tuple[str, str, dict]] = []

    def fake_http(url, *, method, headers, body, timeout):
        calls.append((method, url, dict(headers)))
        if method == "POST":
            return 200, {"Location": "https://upload.example/session"}, b""
        rng = headers.get("Content-Range", "")
        if rng.startswith("bytes 0-"):
            return 308, {"Range": "bytes=0-7"}, b""
        return 201, {}, json.dumps({"id": "vid-resume"}).encode()

    original = youtube_api._http
    original_chunk = youtube_api.RESUMABLE_CHUNK
    youtube_api._http = fake_http
    youtube_api.RESUMABLE_CHUNK = 8
    try:
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp) / "master.mp4"
            media.write_bytes(b"0123456789abcdef")
            data = youtube_api.upload_video(
                "token-not-printed",
                export_path=media,
                metadata={"snippet": {"title": "t"}, "status": {"selfDeclaredMadeForKids": False}},
                privacy="private",
            )
            try:
                youtube_api.upload_video(
                    "token-not-printed",
                    export_path=media,
                    metadata={"snippet": {"title": "t"}},
                    privacy="private",
                )
            except youtube_api.YouTubeAPIError as exc:
                if exc.reason != "AUDIENCE_UNKNOWN":
                    failures.append(f"missing audience must be AUDIENCE_UNKNOWN, got {exc.reason}")
            else:
                failures.append("missing selfDeclaredMadeForKids must not start a session")
    finally:
        youtube_api._http = original
        youtube_api.RESUMABLE_CHUNK = original_chunk
    if data.get("id") != "vid-resume":
        failures.append(f"resumable upload must return the video id: {data}")
    if len(calls) != 3:
        failures.append(f"resumable upload should init, 308, then finish: {len(calls)}")
    elif "uploadType=resumable" not in calls[0][1]:
        failures.append("session start must set uploadType=resumable")
    elif calls[1][2].get("Content-Range") != "bytes 0-7/16":
        failures.append(f"first chunk range drift: {calls[1][2].get('Content-Range')}")
    elif calls[2][2].get("Content-Range") != "bytes 8-15/16":
        failures.append(f"resume range drift: {calls[2][2].get('Content-Range')}")
    if any("token-not-printed" in json.dumps(call) and False for call in calls):
        pass

    retry_calls: list[tuple[str, str]] = []

    def retry_http(url, *, method, headers, body, timeout):
        retry_calls.append((method, headers.get("Content-Range", "")))
        if method == "POST":
            return 200, {"Location": "https://upload.example/session"}, b""
        if headers.get("Content-Range", "").startswith("bytes */"):
            return 308, {"Range": "bytes=0-7"}, b""
        if headers.get("Content-Range", "").startswith("bytes 0-"):
            raise youtube_api.YouTubeAPIError(503, "backendError")
        return 201, {}, json.dumps({"id": "vid-503"}).encode()

    original_sleep = youtube_api._sleep
    youtube_api._http = retry_http
    youtube_api._sleep = lambda _seconds: None
    youtube_api.RESUMABLE_CHUNK = 8
    try:
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp) / "master.mp4"
            media.write_bytes(b"0123456789abcdef")
            data = youtube_api.upload_video(
                "token-not-printed",
                export_path=media,
                metadata={"snippet": {"title": "t"}, "status": {"selfDeclaredMadeForKids": False}},
                privacy="private",
            )
    finally:
        youtube_api._http = original
        youtube_api._sleep = original_sleep
        youtube_api.RESUMABLE_CHUNK = original_chunk
    if data.get("id") != "vid-503":
        failures.append(f"503 must resume via status query, not abort: {data}")
    if not any(rng.startswith("bytes */") for _method, rng in retry_calls):
        failures.append(f"503 must query session with bytes */size: {retry_calls}")
    if not any(rng == "bytes 8-15/16" for _method, rng in retry_calls):
        failures.append(f"503 resume must continue after server Range: {retry_calls}")

    missing_calls: list[str] = []

    def missing_range_http(url, *, method, headers, body, timeout):
        rng = headers.get("Content-Range", "")
        missing_calls.append(rng)
        if method == "POST":
            return 200, {"Location": "https://upload.example/session"}, b""
        if rng.startswith("bytes 0-") and missing_calls.count(rng) == 1:
            return 308, {}, b""
        if rng.startswith("bytes 0-"):
            return 308, {"Range": "bytes=0-7"}, b""
        return 201, {}, json.dumps({"id": "vid-norange"}).encode()

    youtube_api._http = missing_range_http
    youtube_api._sleep = lambda _seconds: None
    youtube_api.RESUMABLE_CHUNK = 8
    try:
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp) / "master.mp4"
            media.write_bytes(b"0123456789abcdef")
            data = youtube_api.upload_video(
                "token-not-printed",
                export_path=media,
                metadata={"snippet": {"title": "t"}, "status": {"selfDeclaredMadeForKids": False}},
                privacy="private",
            )
    finally:
        youtube_api._http = original
        youtube_api._sleep = original_sleep
        youtube_api.RESUMABLE_CHUNK = original_chunk
    if data.get("id") != "vid-norange":
        failures.append(f"308 without Range must restart, not skip the chunk: {data}")
    zero_puts = [rng for rng in missing_calls if rng.startswith("bytes 0-")]
    if len(zero_puts) < 2:
        failures.append(f"308 without Range must re-PUT from byte 0: {missing_calls}")
    if any(rng.startswith("bytes 8-") and missing_calls.index(rng) < 3 for rng in missing_calls):
        failures.append(f"missing Range must not advance to the next chunk: {missing_calls}")

    init_calls: list[str] = []

    def init_retry_http(url, *, method, headers, body, timeout):
        init_calls.append(method + " " + headers.get("Content-Range", ""))
        if method == "POST" and init_calls.count("POST ") == 1:
            return 503, {}, b""
        if method == "POST":
            return 200, {"Location": "https://upload.example/session"}, b""
        return 201, {}, json.dumps({"id": "vid-init"}).encode()

    youtube_api._http = init_retry_http
    youtube_api._sleep = lambda _seconds: None
    youtube_api.RESUMABLE_CHUNK = 8
    try:
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp) / "master.mp4"
            media.write_bytes(b"0123456789abcdef")
            data = youtube_api.upload_video(
                "token-not-printed",
                export_path=media,
                metadata={"snippet": {"title": "t"}, "status": {"selfDeclaredMadeForKids": False}},
                privacy="private",
            )
    finally:
        youtube_api._http = original
        youtube_api._sleep = original_sleep
        youtube_api.RESUMABLE_CHUNK = original_chunk
    if data.get("id") != "vid-init":
        failures.append(f"session 503 without Location must retry the same insert: {data}")
    posts = [row for row in init_calls if row.startswith("POST")]
    if len(posts) != 2:
        failures.append(f"session 503 without Location must POST twice, not abort: {init_calls}")

    hidden_calls: list[str] = []

    def hidden_session_http(url, *, method, headers, body, timeout):
        hidden_calls.append(method)
        if method == "POST":
            return 503, {"Location": "https://upload.example/session"}, b""
        return 201, {}, json.dumps({"id": "vid-hidden"}).encode()

    youtube_api._http = hidden_session_http
    youtube_api._sleep = lambda _seconds: None
    youtube_api.RESUMABLE_CHUNK = 8
    try:
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp) / "master.mp4"
            media.write_bytes(b"0123456789abcdef")
            data = youtube_api.upload_video(
                "token-not-printed",
                export_path=media,
                metadata={"snippet": {"title": "t"}, "status": {"selfDeclaredMadeForKids": False}},
                privacy="private",
            )
    finally:
        youtube_api._http = original
        youtube_api._sleep = original_sleep
        youtube_api.RESUMABLE_CHUNK = original_chunk
    if data.get("id") != "vid-hidden":
        failures.append(f"503 with Location must use that session: {data}")
    if hidden_calls.count("POST") != 1:
        failures.append(f"503 with Location must not start a second videos.insert: {hidden_calls}")

    artifact_calls: list[int] = []

    def artifact_request(url, *, method="GET", token=None, body=None, content_type=None, accept="application/json", timeout=120):
        artifact_calls.append(1)
        if len(artifact_calls) == 1:
            raise youtube_api.YouTubeAPIError(503, "backendError")
        return json.dumps({"id": "cap-1"}).encode()

    original_request = youtube_api._request
    youtube_api._request = artifact_request
    youtube_api._sleep = lambda _seconds: None
    try:
        with tempfile.TemporaryDirectory() as tmp:
            cap = Path(tmp) / "captions.srt"
            cap.write_text("1\n00:00:00,000 --> 00:00:01,000\nhi\n", encoding="utf-8")
            data = youtube_api.insert_caption("token-not-printed", video_id="vid", caption_path=cap)
    finally:
        youtube_api._request = original_request
        youtube_api._sleep = original_sleep
    if data.get("id") != "cap-1":
        failures.append(f"caption 503 must retry the same insert: {data}")
    if len(artifact_calls) != 2:
        failures.append(f"caption 503 must retry once then succeed: {len(artifact_calls)}")

    def permanent_request(url, *, method="GET", token=None, body=None, content_type=None, accept="application/json", timeout=120):
        raise youtube_api.YouTubeAPIError(400, "captionExists")

    youtube_api._request = permanent_request
    try:
        with tempfile.TemporaryDirectory() as tmp:
            cap = Path(tmp) / "captions.srt"
            cap.write_text("1\n00:00:00,000 --> 00:00:01,000\nhi\n", encoding="utf-8")
            try:
                youtube_api.insert_caption("token-not-printed", video_id="vid", caption_path=cap)
            except youtube_api.YouTubeAPIError as exc:
                if exc.reason != "captionExists":
                    failures.append(f"caption 400 must stay permanent: {exc.reason}")
            else:
                failures.append("caption 400 must not be treated as success")
    finally:
        youtube_api._request = original_request
        youtube_api._sleep = original_sleep

    refresh_calls = {"n": 0}
    seen_tokens: list[str] = []

    def unauthorized_caption(url, *, method="GET", token=None, body=None, content_type=None, accept="application/json", timeout=120):
        seen_tokens.append(str(token))
        if "videos" in url and "captions" not in url:
            raise youtube_api.YouTubeAPIError(0, "unexpected_videos_insert")
        if token == "token-not-printed":
            raise youtube_api.YouTubeAPIError(401, "authError", "Invalid Credentials")
        return json.dumps({"id": "cap-401"}).encode()

    def refresh_once():
        refresh_calls["n"] += 1
        return "token-refreshed"

    youtube_api._request = unauthorized_caption
    youtube_api._sleep = lambda _seconds: None
    try:
        with tempfile.TemporaryDirectory() as tmp:
            cap = Path(tmp) / "captions.srt"
            cap.write_text("1\n00:00:00,000 --> 00:00:01,000\nhi\n", encoding="utf-8")
            data = youtube_api.insert_caption(
                "token-not-printed",
                video_id="vid",
                caption_path=cap,
                token_refresher=refresh_once,
            )
    finally:
        youtube_api._request = original_request
        youtube_api._sleep = original_sleep
    if data.get("id") != "cap-401":
        failures.append(f"caption 401 must retry after refresh: {data}")
    if refresh_calls["n"] != 1 or seen_tokens[-1] != "token-refreshed":
        failures.append(f"caption 401 must use the refreshed token: {seen_tokens} {refresh_calls}")

    def unchanged_caption(url, *, method="GET", token=None, body=None, content_type=None, accept="application/json", timeout=120):
        raise youtube_api.YouTubeAPIError(401, "authError", "Invalid Credentials")

    youtube_api._request = unchanged_caption
    youtube_api._sleep = lambda _seconds: None
    try:
        with tempfile.TemporaryDirectory() as tmp:
            cap = Path(tmp) / "captions.srt"
            cap.write_text("1\n00:00:00,000 --> 00:00:01,000\nhi\n", encoding="utf-8")
            try:
                youtube_api.insert_caption(
                    "token-not-printed",
                    video_id="vid",
                    caption_path=cap,
                    token_refresher=lambda: "token-not-printed",
                )
            except youtube_api.YouTubeAPIError as exc:
                if exc.reason != "POST_UPLOAD_TOKEN_REFRESH_EXHAUSTED":
                    failures.append(f"unchanged caption token must exhaust: {exc.reason}")
            else:
                failures.append("unchanged caption token must not succeed")
    finally:
        youtube_api._request = original_request
        youtube_api._sleep = original_sleep

    auth_calls: list[tuple[str, str]] = []

    def unauthorized_http(url, *, method, headers, body, timeout):
        auth = headers.get("Authorization", "")
        auth_calls.append((method, auth))
        if method == "POST":
            return 200, {"Location": "https://upload.example/session-401"}, b""
        if auth.endswith("token-not-printed"):
            raise youtube_api.YouTubeAPIError(401, "authError", "Invalid Credentials")
        rng = headers.get("Content-Range", "")
        if rng.startswith("bytes */"):
            return 308, {"Range": "bytes=0-7"}, b""
        return 201, {}, json.dumps({"id": "vid-401"}).encode()

    youtube_api._http = unauthorized_http
    youtube_api.RESUMABLE_CHUNK = 8
    youtube_api._sleep = lambda _seconds: None
    try:
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp) / "master.mp4"
            media.write_bytes(b"0123456789abcdef")
            data = youtube_api.upload_video(
                "token-not-printed",
                export_path=media,
                metadata={"snippet": {"title": "t"}, "status": {"selfDeclaredMadeForKids": False}},
                privacy="private",
                token_refresher=lambda: "token-refreshed",
            )
    finally:
        youtube_api._http = original
        youtube_api.RESUMABLE_CHUNK = original_chunk
        youtube_api._sleep = original_sleep
    if data.get("id") != "vid-401":
        failures.append(f"401 must resume the same session after refresh: {data}")
    posts = [item for item in auth_calls if item[0] == "POST"]
    if len(posts) != 1:
        failures.append(f"401 must not start a second videos.insert: {posts}")
    if not any(item[0] == "PUT" and item[1].endswith("token-refreshed") for item in auth_calls):
        failures.append(f"401 resume must use the refreshed token: {auth_calls}")

    empty_calls: list[tuple[str, str]] = []

    def empty_complete_http(url, *, method, headers, body, timeout):
        empty_calls.append((method, headers.get("Content-Range", "")))
        if method == "POST":
            return 200, {"Location": "https://upload.example/session"}, b""
        rng = headers.get("Content-Range", "")
        if rng.startswith("bytes */"):
            return 200, {}, json.dumps({"id": "vid-empty-body"}).encode()
        return 201, {}, b""

    youtube_api._http = empty_complete_http
    youtube_api.RESUMABLE_CHUNK = 8
    try:
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp) / "master.mp4"
            media.write_bytes(b"0123456789abcdef")
            data = youtube_api.upload_video(
                "token-not-printed",
                export_path=media,
                metadata={"snippet": {"title": "t"}, "status": {"selfDeclaredMadeForKids": False}},
                privacy="private",
            )
    finally:
        youtube_api._http = original
        youtube_api.RESUMABLE_CHUNK = original_chunk
    if data.get("id") != "vid-empty-body":
        failures.append(f"empty 201 body must recover the video id from the session: {data}")
    posts = [item for item in empty_calls if item[0] == "POST"]
    if len(posts) != 1:
        failures.append(f"empty 201 body must not start a second videos.insert: {posts}")
    if not any(rng.startswith("bytes */") for _method, rng in empty_calls):
        failures.append(f"empty 201 body must query the same session: {empty_calls}")

    gone_calls: list[str] = []

    def gone_after_complete(url, *, method, headers, body, timeout):
        gone_calls.append(method)
        if method == "POST":
            return 200, {"Location": "https://upload.example/session-gone"}, b""
        rng = headers.get("Content-Range", "")
        if rng.startswith("bytes */"):
            raise youtube_api.YouTubeAPIError(410, "gone", "session expired after complete")
        return 201, {}, b""

    youtube_api._http = gone_after_complete
    youtube_api.RESUMABLE_CHUNK = 8
    try:
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp) / "master.mp4"
            media.write_bytes(b"0123456789abcdef")
            try:
                youtube_api.upload_video(
                    "token-not-printed",
                    export_path=media,
                    metadata={"snippet": {"title": "t"}, "status": {"selfDeclaredMadeForKids": False}},
                    privacy="private",
                )
            except youtube_api.YouTubeAPIError as exc:
                if exc.reason != "RESUMABLE_COMPLETED_SESSION_GONE":
                    failures.append(f"410 after empty 201 must be session gone: {exc.reason}")
            else:
                failures.append("410 after empty 201 must not look like a recovered video")
    finally:
        youtube_api._http = original
        youtube_api.RESUMABLE_CHUNK = original_chunk
    if gone_calls.count("POST") != 1:
        failures.append(f"410 after empty 201 must not start a second videos.insert: {gone_calls}")

    youtube_api.RESUMABLE_CHUNK = 8 * 1024 * 1024
    if youtube_api.sendable_offset(100, 5000):
        failures.append("unaligned resume offset must not be sendable")
    if not youtube_api.sendable_offset(256 * 1024, 8 * 1024 * 1024):
        failures.append("256 KiB resume offset must be sendable")
    align_calls: list[str] = []

    def unaligned_http(url, *, method, headers, body, timeout):
        align_calls.append(method)
        if method == "POST":
            return 200, {"Location": "https://upload.example/session-align"}, b""
        return 308, {"Range": "bytes=0-99"}, b""

    youtube_api._http = unaligned_http
    try:
        with tempfile.TemporaryDirectory() as tmp:
            media = Path(tmp) / "master.mp4"
            media.write_bytes(b"x" * (256 * 1024 + 10))
            try:
                youtube_api.upload_video(
                    "token-not-printed",
                    export_path=media,
                    metadata={"snippet": {"title": "t"}, "status": {"selfDeclaredMadeForKids": False}},
                    privacy="private",
                )
            except youtube_api.YouTubeAPIError as exc:
                if exc.reason != "RESUMABLE_STALLED" or "unaligned_offset=100" not in exc.detail:
                    failures.append(f"unaligned Range must stall: {exc.reason} {exc.detail}")
            else:
                failures.append("unaligned Range must not continue the upload")
    finally:
        youtube_api._http = original
        youtube_api.RESUMABLE_CHUNK = original_chunk
    if align_calls.count("POST") != 1:
        failures.append(f"unaligned Range must not start a second videos.insert: {align_calls}")
    if align_calls.count("PUT") != 1:
        failures.append(f"unaligned Range must not send the next chunk: {align_calls}")
    return failures



def check_job_timeout_covers_upload() -> list[str]:
    """A killed Actions job drops the video id. The job must outlast one chunk retry budget."""
    failures = []
    workflow = (ROOT / ".github/workflows/youtube-production.yml").read_text(encoding="utf-8")
    if "skip_comment:" not in workflow or "--skip-comment" not in workflow:
        failures.append("production workflow must expose skip_comment and pass --skip-comment")
    if "tools/studio_handoff.py" not in workflow or "--write" not in workflow:
        failures.append("production workflow must write the Studio pin file after execute")
    if 'git add "$PACKET/studio_pin.md"' not in workflow:
        failures.append("production persist must commit studio_pin.md with the video id")
    if "pinned: false" not in (ROOT / "tools" / "studio_handoff.py").read_text(encoding="utf-8"):
        failures.append("studio handoff must not claim the comment is pinned")
    import studio_handoff
    rendered = studio_handoff.render(
        {"provider_video_id": "abc123", "comment_post": {"status": "posted"}},
        "Pin this sentence.",
    )
    if "https://studio.youtube.com/video/abc123/comments" not in rendered:
        failures.append("studio handoff must print the Studio comments URL")
    if "pinned: false" not in rendered:
        failures.append("studio handoff render must keep pinned false")
    if "needs_studio_pin" not in rendered:
        failures.append("studio handoff must name the remaining Studio pin")
    empty = studio_handoff.render({})
    if "no_video_id" not in empty or "studio.youtube.com" in empty:
        failures.append("studio handoff must not invent a video id")
    note = studio_handoff.pin_markdown(
        {"provider_video_id": "abc123", "comment_post": {"status": "posted"}},
        "Pin this sentence.",
    )
    if not note or "https://studio.youtube.com/video/abc123/comments" not in note or "pinned: false" not in note:
        failures.append("studio pin file must keep the URL and pinned false")
    if studio_handoff.pin_markdown({}) is not None:
        failures.append("studio pin file must not be written without a video id")
    if not note or "end_screen: not_set" not in note or "https://studio.youtube.com/video/abc123/edit" not in note:
        failures.append("studio pin file must keep the end screen unset and the editor URL")
    if "end_screen: not_set" not in rendered or "https://studio.youtube.com/video/abc123/edit" not in rendered:
        failures.append("studio handoff must print the unset end screen and editor URL")
    from timeline import END_SCREEN
    reserve = f"end_screen_reserve_s: {END_SCREEN:.0f}"
    if reserve not in rendered or reserve not in (note or ""):
        failures.append("studio handoff reserve must come from timeline.END_SCREEN")
    if "last 20 seconds" in (ROOT / "tools" / "studio_handoff.py").read_text(encoding="utf-8"):
        failures.append("studio handoff must not hardcode the end-screen reserve")
    if "studio.youtube.com" in empty:
        failures.append("studio handoff must not invent an end-screen URL")
    if "inputs.packet" not in workflow or "videos/002-stop-deciding-what-to-work-on-every-morning" not in workflow:
        failures.append("production workflow must keep the Q1 packet as the default dispatch input")
    if "PACKET: ${{ inputs.packet }}" not in workflow:
        failures.append("production PACKET must come from the dispatch input, not a second hardcoded env")
    if "inputs.packet == 'videos/002-stop-deciding-what-to-work-on-every-morning'" not in workflow:
        failures.append("Q1 release materialize must stay limited to the Q1 packet path")
    if "python3 tools/packet_path.py" not in workflow:
        failures.append("production workflow must refuse a bad packet path before materialize")
    if "_template" not in (ROOT / "tools" / "packet_path.py").read_text(encoding="utf-8"):
        failures.append("packet path gate must keep refusing the template folder")
    if "fetch-depth: 0" not in workflow:
        failures.append("production checkout must be full history so provider-state rebase has a merge base")
    if "fetch-depth: 1" in workflow:
        failures.append("do not restore a depth-1 production checkout")
    if "timeout-minutes: 60" not in workflow:
        failures.append("youtube-production job timeout must stay 60 minutes")
    if "timeout-minutes: 20" in workflow:
        failures.append("do not restore the 20-minute job timeout; it can kill a chunk PUT before persist")
    sys.path.insert(0, str(ROOT / "tools"))
    import youtube_api
    budget = youtube_api.RESUMABLE_RETRY_LIMIT * youtube_api.CHUNK_PUT_TIMEOUT
    if budget >= 60 * 60:
        failures.append(f"chunk retry budget {budget}s must fit inside the 60-minute job")
    if youtube_api.CHUNK_PUT_TIMEOUT != 180:
        failures.append("chunk PUT timeout must stay 180s so three retries fit before the runner is killed")
    return failures




def check_upload_variant_freeze() -> list[str]:
    failures = check_repo(ROOT)
    injected = check_texts(
        {"youtube_api.py": 'raise YouTubeAPIError(0, "RESUMABLE_NEW_STATUS")'},
        "",
    )
    if not injected:
        failures.append("upload variant freeze must reject a new reason without live evidence")
    allowed = check_texts(
        {"youtube_api.py": 'raise YouTubeAPIError(0, "RESUMABLE_NEW_STATUS")'},
        "live_status: RESUMABLE_NEW_STATUS\nactions_run: 1\n",
    )
    if allowed:
        failures.append(f"live_status line must allow a recorded reason, got {allowed}")
    return failures


def check_caption_waits_for_processing() -> list[str]:
    """captions.insert before processing finishes is a permanent 400. Wait first."""
    failures = []
    upload = (ROOT / "tools/youtube_upload.py").read_text(encoding="utf-8")
    if "wait_for_caption_ready" not in upload:
        failures.append("youtube_upload must wait for processing before captions.insert")
    wait_at = upload.find("wait_for_caption_ready")
    insert_at = upload.find("insert_caption(")
    if wait_at < 0 or insert_at < 0 or wait_at > insert_at:
        failures.append("wait_for_caption_ready must run before insert_caption")
    sys.path.insert(0, str(ROOT / "tools"))
    import youtube_api
    budget = youtube_api.CAPTION_READY_POLLS * youtube_api.CAPTION_READY_POLL_SECONDS
    if budget < 480:
        failures.append("caption wait budget must cover several minutes of HD processing, not 60 seconds")
    if budget > 15 * 60:
        failures.append("caption wait budget must stay inside the 60-minute job")
    if youtube_api.caption_processing_status({"items": [{"processingDetails": {"processingStatus": "succeeded"}}]}) != "succeeded":
        failures.append("caption_processing_status must read processingDetails")
    calls = []

    def fake_request(url, **kwargs):
        calls.append(url)
        status = "processing" if len(calls) == 1 else "succeeded"
        body = ('{"items":[{"processingDetails":{"processingStatus":"%s"}}]}' % status).encode()
        return body

    original = youtube_api._request_retrying
    youtube_api._request_retrying = fake_request
    try:
        got = youtube_api.wait_for_caption_ready(
            "token-not-printed",
            video_id="vid",
            sleeper=lambda _s: None,
            max_polls=3,
            poll_seconds=0,
        )
    finally:
        youtube_api._request_retrying = original
    if got != "succeeded":
        failures.append(f"processing then succeeded must become ready, got {got}")
    if len(calls) != 2:
        failures.append(f"processing wait must poll again, calls={len(calls)}")
    if any("videos.insert" in c or "uploadType" in c for c in calls):
        failures.append("processing wait must not start videos.insert")

    def always_processing(url, **kwargs):
        return b'{"items":[{"processingDetails":{"processingStatus":"processing"}}]}'

    youtube_api._request_retrying = always_processing
    try:
        try:
            youtube_api.wait_for_caption_ready(
                "token-not-printed",
                video_id="vid",
                sleeper=lambda _s: None,
                max_polls=2,
                poll_seconds=0,
            )
            failures.append("still processing must raise VIDEO_PROCESSING_NOT_READY")
        except youtube_api.YouTubeAPIError as exc:
            if exc.reason != "VIDEO_PROCESSING_NOT_READY":
                failures.append(f"still processing reason was {exc.reason}")
    finally:
        youtube_api._request_retrying = original
    return failures


def check_prove_locks_on_push() -> list[str]:
    """Write-path locks must run on every push, not only when an agent remembers.

    prove_locks.py stays unmapped in needed.py. This check only requires the
    selftest workflow to invoke it. Do not treat PASS as apply --write.
    """
    failures = []
    workflow = (ROOT / ".github/workflows/selftest.yml").read_text(encoding="utf-8")
    if "python3 tools/prove_locks.py" not in workflow:
        failures.append("selftest workflow must run prove_locks.py on every push")
    return failures


def check_stall_watch() -> list[str]:
    """The OAuth-and-Studio loop must be detectable. The flag does not fail CI."""
    import stall_watch
    failures = []
    sample = ""
    for n in (9, 8, 7):
        sample += (
            f"## Run {n} delta\n"
            "- OAuth secrets were not polled\n"
            "end_screen note in studio_pin.md\n"
            "Videos published stay 0.\n\n"
        )
    if "STALL_OAUTH_AND_STUDIO" not in stall_watch.flag_text(sample):
        failures.append("stall_watch must flag three OAuth-and-studio deltas")
    if stall_watch.flag_text("## Run 1 delta\n- fixed assemble\n"):
        failures.append("stall_watch must stay quiet without the repeated pattern")
    return failures

if __name__ == "__main__":
    raise SystemExit(main())

