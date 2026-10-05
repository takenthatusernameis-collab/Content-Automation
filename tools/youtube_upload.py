#!/usr/bin/env python3
"""YouTube upload adapter.

Dry-run is the default. --execute performs authenticated provider writes only after
all local gates pass. Secrets are never printed or written to repository state.
"""


from __future__ import annotations

import argparse
import hashlib
import re
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from media_qa import mp4_header_ok  # noqa: E402
from publish_brief import primary_title, section  # noqa: E402
from render_brief import selected_vo_drop  # noqa: E402
from timeline import END_SCREEN  # noqa: E402
from youtube_api import (  # noqa: E402
    YouTubeAPIError,
    access_token_scopes,
    compact_api_error,
    insert_caption,
    wait_for_caption_ready,
    insert_top_level_comment,
    refresh_access_token,
    set_thumbnail,
    upload_video,
)

AUTH_STATE = "YOUTUBE_AUTH_REQUIRED"
OAUTH_KEYS = ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN")
# Run 249 master is VO-length only. Do not upload it. Run 253 is the padded export.
TRUNCATED_MASTER_SHA256 = {
    "abec4eb94199d0cbbf00659891d4e79c0040a6b1bb5450fa6e1db0e54c4b4d53",
}
UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
MANAGE_SCOPE = "https://www.googleapis.com/auth/youtube"
FORCE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
ANALYTICS_SCOPE = "https://www.googleapis.com/auth/yt-analytics.readonly"
DEFAULT_PRIVACY = "private"
EXPORT_REL = "export/master.mp4"
STATE_NAME = "upload_state.json"
# videos.insert rejects these. Fail before the token refresh so the first
# authenticated dispatch does not spend a provider write on invalid snippet fields.
TITLE_MAX = 100
DESCRIPTION_MAX = 5000
TAG_COUNT_MAX = 12
TAG_TOTAL_MAX = 500
# videos.insert counts a comma between tags, and wraps a tag that contains a
# space in quotes. Those extra characters count toward the 500 limit. A raw
# sum can pass locally and still return invalidTags.
# thumbnails.set rejects files over 2MB, images narrower than 640px, and a
# truncated PNG that has an IHDR but no IEND. captions.insert rejects an empty
# track, a cue that is not forward, cues out of order, overlapping cues, and a
# last cue past the known master. Fail before videos.insert so a bad draft
# cannot create a private video that then loops on POST_UPLOAD_INCOMPLETE.
THUMB_MAX_BYTES = 2 * 1024 * 1024
THUMB_MIN_WIDTH = 640
THUMB_MIN_HEIGHT = 360
CAPTION_MAX_BYTES = 100 * 1024 * 1024
COMMENT_MAX = 10000
PNG_MAGIC = bytes((0x89, 0x50, 0x4E, 0x47, 0x0D, 0x0A, 0x1A, 0x0A))
PNG_IEND = b"IEND"
CAPTION_LANGUAGE = "en"
CAPTION_NAME = "English"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def preserved_upload_stamp(prior: dict | None) -> str | None:
    """Copy a real upload timestamp. Never invent one from generated or fetched fields."""
    if not isinstance(prior, dict):
        return None
    video = prior.get("video_upload")
    if isinstance(video, dict):
        raw = video.get("uploaded_at")
        if isinstance(raw, str) and raw.strip():
            return raw.strip()
    raw = prior.get("uploaded_at")
    if isinstance(raw, str) and raw.strip():
        return raw.strip()
    return None


STUB_DESCRIPTION_MARKERS = (
    "No upload happened",
    "Human locks title, description, and tags before YouTube",
)



def missing_provider_scopes(
    granted: set[str] | list[str],
    *,
    captions: bool,
    thumbnail: bool,
    comment: bool,
) -> list[str]:
    """Scopes required before videos.insert or a caption/thumbnail resume.

    youtube.upload can insert a video and set a thumbnail, but captions.insert
    and commentThreads.insert need youtube.force-ssl or the full youtube scope.
    A token with only the upload scope would create a private video and then
    loop on POST_UPLOAD_INCOMPLETE. Fail before that write.
    """
    have = set(granted)
    missing: list[str] = []
    can_upload = bool(have & {UPLOAD_SCOPE, MANAGE_SCOPE, FORCE_SSL_SCOPE})
    can_caption = bool(have & {FORCE_SSL_SCOPE, MANAGE_SCOPE})
    can_thumb = bool(have & {UPLOAD_SCOPE, MANAGE_SCOPE})
    can_comment = bool(have & {FORCE_SSL_SCOPE, MANAGE_SCOPE})
    if not can_upload:
        missing.append(UPLOAD_SCOPE)
    if captions and not can_caption and FORCE_SSL_SCOPE not in missing:
        missing.append(FORCE_SSL_SCOPE)
    if thumbnail and not can_thumb and UPLOAD_SCOPE not in missing:
        missing.append(UPLOAD_SCOPE)
    if comment and not can_comment and FORCE_SSL_SCOPE not in missing:
        missing.append(FORCE_SSL_SCOPE)
    return missing


def metadata_block_reason(meta: dict) -> str | None:
    """Refuse snippet fields YouTube will reject. Do not truncate tags silently."""
    title = meta.get("title") or ""
    description = meta.get("description") or ""
    tags = meta.get("tags") or []
    if not title.strip():
        return "title_empty"
    if "<" in title or ">" in title:
        return "title_invalid_characters"
    if len(title) > TITLE_MAX:
        return f"title_too_long {len(title)}>{TITLE_MAX}"
    if len(description) > DESCRIPTION_MAX:
        return f"description_too_long {len(description)}>{DESCRIPTION_MAX}"
    if len(tags) > TAG_COUNT_MAX:
        return f"too_many_tags {len(tags)}>{TAG_COUNT_MAX}"
    for tag in tags:
        if not tag or tag != tag.strip() or "," in tag or "<" in tag or ">" in tag:
            return "tag_invalid"
    total = tag_budget(tags)
    if total > TAG_TOTAL_MAX:
        return f"tags_too_long {total}>{TAG_TOTAL_MAX}"
    return None


def chapter_lines(packet: Path) -> list[str]:
    """YouTube chapter lines drafted in chapters.md. Empty if that file is absent."""
    path = packet / "chapters.md"
    if not path.is_file():
        return []
    lines = path.read_text(encoding="utf-8").splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip() == "## YouTube lines":
            start = i + 1
            break
    if start is None:
        return []
    found = []
    for line in lines[start:]:
        if line.startswith("#"):
            break
        stripped = line.strip()
        if not stripped:
            continue
        if not re.match(r"^\d+:\d{2}(?:\s|$)", stripped):
            continue
        found.append(stripped)
    return found


def _chapter_seconds(stamp: str) -> int | None:
    parts = stamp.split(":")
    if len(parts) == 2:
        minutes, seconds = parts
        hours = "0"
    elif len(parts) == 3:
        hours, minutes, seconds = parts
    else:
        return None
    if not (hours.isdigit() and minutes.isdigit() and seconds.isdigit()):
        return None
    if len(seconds) != 2 or not (1 <= len(minutes) <= 2) or len(hours) > 2:
        return None
    return int(hours) * 3600 + int(minutes) * 60 + int(seconds)


def content_rule_reason(packet: Path) -> str | None:
    """Refuse upload when a pre-VO scanner still hits. Does not rewrite packet files.

    ready_for_vo already refuses these hits. This check covers a packet whose
    status was set earlier, or whose titles/script changed after that status.
    A missing titles.md or script.md is not a hit.
    """
    from claim_scan import scan_path as claim_scan_path
    from quality_scan import scan_path as quality_scan_path
    from title_scan import scan_path as title_scan_path

    hits = []
    for label, scanner in (
        ("quality_scan", quality_scan_path),
        ("claim_scan", claim_scan_path),
        ("title_scan", title_scan_path),
    ):
        found = scanner(packet)
        if found:
            hits.append(f"{label}: {found[0]}")
    if not hits:
        return None
    return "; ".join(hits[:3])


def chapter_sync_reason(packet: Path, description: str) -> str | None:
    """Refuse a drafted chapter list that videos.insert would upload without chapters.

    YouTube ignores a description chapter list when the first line is not 0:00,
    there are fewer than three timestamps, a gap is under 10 seconds, or the
    lines are not at the start of their own description lines. A missing
    chapters.md stays missing. This does not regenerate chapters.md.
    """
    lines = chapter_lines(packet)
    if not lines:
        return None
    if len(lines) < 3:
        return f"chapter_lines_too_few {len(lines)}<3"
    stamps = []
    for line in lines:
        stamp = line.split()[0]
        seconds = _chapter_seconds(stamp)
        if seconds is None:
            return "chapter_stamp_unparseable"
        stamps.append(seconds)
    if stamps[0] != 0:
        return "chapter_first_not_zero"
    for prev, cur in zip(stamps, stamps[1:]):
        if cur - prev < 10:
            return "chapter_gap_under_10s"
    description_lines = [line.strip() for line in (description or "").splitlines()]
    positions = []
    for line in lines:
        try:
            positions.append(description_lines.index(line))
        except ValueError:
            return "chapter_line_missing_from_description"
    if positions != sorted(positions):
        return "chapter_lines_out_of_order"
    return None


def tag_budget(tags: list) -> int:
    """Characters videos.insert counts toward the 500 keyword limit.

    A raw sum undercounts a tag that contains a space (the server wraps it in
    quotes) and undercounts the comma separators between tags.
    """
    if not tags:
        return 0
    total = 0
    for tag in tags:
        total += len(tag)
        if " " in tag:
            total += 2
    total += len(tags) - 1
    return total



def png_dimensions(path: Path) -> tuple[int, int] | None:
    """Read width and height from a PNG IHDR. None if the file is not a PNG."""
    try:
        raw = path.read_bytes()[:24]
    except OSError:
        return None
    if len(raw) < 24 or raw[:8] != PNG_MAGIC or raw[12:16] != b"IHDR":
        return None
    return int.from_bytes(raw[16:20], "big"), int.from_bytes(raw[20:24], "big")


def png_has_iend(path: Path) -> bool:
    """True only if a PNG ends with the IEND chunk. IHDR alone is not enough."""
    try:
        raw = path.read_bytes()
    except OSError:
        return False
    return len(raw) >= 12 and raw[-8:-4] == PNG_IEND


CUE_TIME = re.compile(
    r"(\d{2}):(\d{2}):(\d{2}),(\d{3})\s*-->\s*(\d{2}):(\d{2}):(\d{2}),(\d{3})"
)


def _cue_seconds(hours: str, minutes: str, seconds: str, millis: str) -> float | None:
    hour, minute, second, milli = int(hours), int(minutes), int(seconds), int(millis)
    if minute > 59 or second > 59:
        return None
    return hour * 3600 + minute * 60 + second + milli / 1000.0


def caption_timing_reason(text: str, duration: float | None = None) -> str | None:
    """Refuse SRT cues captions.insert will reject after a video exists.

    A missing cue stays missing. A present cue that runs backward, overlaps
    the previous cue, is unparseable, or ends after the known master must not
    reach videos.insert. Duration is optional so a packet without a probed
    export still checks order and overlap.
    """
    blocks = [block for block in text.replace("\r\n", "\n").strip().split("\n\n") if block.strip()]
    seen = 0
    previous_start = -1.0
    previous_end = -1.0
    last_end = 0.0
    for block in blocks:
        match = CUE_TIME.search(block)
        if match is None:
            if "-->" in block:
                return "captions_invalid_timestamp"
            continue
        start = _cue_seconds(*match.groups()[:4])
        end = _cue_seconds(*match.groups()[4:])
        if start is None or end is None or end <= start:
            return "captions_cue_not_forward" if start is not None and end is not None else "captions_invalid_timestamp"
        if start < previous_start:
            return "captions_cues_out_of_order"
        if previous_end >= 0 and start < previous_end:
            return "captions_cues_overlap"
        previous_start = start
        previous_end = end
        last_end = end
        seen += 1
    if seen == 0:
        return "captions_missing_timestamp"
    if duration is not None and last_end > duration + 1.0:
        return f"captions_past_video {last_end:.2f}>{duration + 1.0:.2f}"
    return None


def artifact_block_reason(packet: Path, meta: dict | None = None) -> str | None:
    """Refuse local drafts YouTube will reject after videos.insert.

    Missing thumbnail or captions stay missing. A present file that cannot
    be set or inserted must fail before the provider video exists.
    """
    thumb = packet / "thumbnail.png"
    if thumb.is_file():
        size = thumb.stat().st_size
        if size <= 0 or size > THUMB_MAX_BYTES:
            return f"thumbnail_too_large {size}>{THUMB_MAX_BYTES}"
        dims = png_dimensions(thumb)
        if dims is None:
            return "thumbnail_not_png"
        width, height = dims
        if width < THUMB_MIN_WIDTH or height < THUMB_MIN_HEIGHT:
            return f"thumbnail_too_small {width}x{height}"
        if not png_has_iend(thumb):
            return "thumbnail_truncated_png"
    captions = packet / "captions.srt"
    if captions.is_file():
        size = captions.stat().st_size
        if size <= 0 or size > CAPTION_MAX_BYTES:
            return f"captions_too_large {size}>{CAPTION_MAX_BYTES}"
        try:
            text = captions.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return "captions_not_utf8"
        if "-->" not in text:
            return "captions_missing_timestamp"
        export = export_path(packet)
        duration = probe_duration(export) if export.is_file() else None
        timing = caption_timing_reason(text, duration)
        if timing:
            return timing
    comment = ((meta or {}).get("pin_comment") or "").strip()
    if comment and len(comment) > COMMENT_MAX:
        return f"comment_too_long {len(comment)}>{COMMENT_MAX}"
    return None


def comment_approved(text: str) -> bool:
    """True only when the delegated first-comment box is checked.

    Execute already refuses unchecked publish copy. This keeps the pin
    post tied to that box so a later gate change cannot post a draft.
    """
    for line in text.splitlines():
        stripped = line.strip().lower()
        if stripped.startswith("- [x]") and "first comment approved" in stripped:
            return True
    return False


def should_post_comment(meta: dict, *, requested: bool = False, skipped: bool = False) -> bool:
    """Post the pin comment on execute when it is approved and non-empty.

    --post-comment remains an explicit request. --skip-comment is the opt-out
    and wins over --post-comment. A missing comment stays missing. This does
    not invent comment text. The Data API insert is not a Studio pin.
    """
    if skipped:
        return False
    text = ((meta or {}).get("pin_comment") or "").strip()
    if not text:
        return False
    if requested:
        return True
    return bool((meta or {}).get("comment_approved"))


def incomplete_post_uploads(result: dict) -> list[str]:
    """Return post-upload artifacts that failed after a provider video id existed.

    A video id with a failed caption or thumbnail must not look like a finished upload.
    Missing artifacts stay missing. This does not invent an upload timestamp.
    """
    failed = []
    for key, label in (
        ("caption_upload", "captions"),
        ("thumbnail_upload", "thumbnail"),
    ):
        status = (result.get(key) or {}).get("status")
        if status == "failed":
            failed.append(label)
    comment = result.get("comment_post") or {}
    if comment.get("status") == "failed":
        failed.append("comment")
    return failed


def unchecked_publish_items(text: str) -> list[str]:
    block = section(text, "Human before upload")
    open_items = []
    for line in block.splitlines():
        line = line.strip()
        if line.startswith("- [ ]"):
            item = line[5:].strip()
            if item and "No YouTube upload" not in item:
                open_items.append(item)
    return open_items


def copy_block_reason(text: str, meta: dict) -> str | None:
    description = meta.get("description") or ""
    for marker in STUB_DESCRIPTION_MARKERS:
        if marker in description:
            return f"stub description still contains {marker!r}"
    open_items = unchecked_publish_items(text)
    if open_items:
        return "unchecked publish copy: " + "; ".join(open_items)
    return None


def parse_publish(text: str) -> dict:
    title = section(text, "Title to upload").splitlines()[0].strip() if text else ""
    description = section(text, "Description").strip()
    tags_block = section(text, "Tags")
    tags = []
    for line in tags_block.splitlines():
        line = line.strip()
        if line.startswith("- "):
            tag = line[2:].strip()
            if tag:
                tags.append(tag)
    comment = section(text, "First comment (pin candidate)").strip()
    return {
        "title": title,
        "description": description,
        "tags": tags,
        "pin_comment": comment,
        "comment_approved": comment_approved(text),
        "word_count": len(description.split()) if description else 0,
    }



def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def probe_duration(path: Path) -> float | None:
    import subprocess

    try:
        proc = subprocess.run(
            [
                "ffprobe",
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=nw=1:nk=1",
                str(path),
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if proc.returncode != 0:
        return None
    try:
        return float(proc.stdout.strip())
    except ValueError:
        return None


def packet_vo(packet: Path) -> Path | None:
    matches = sorted((packet / "vo").glob(f"{packet.name}-take-selected.wav")) if (packet / "vo").is_dir() else []
    return matches[0] if matches else None


def master_block_reason(
    export: Path,
    vo: Path | None = None,
    banned: set[str] | None = None,
) -> str | None:
    """Refuse the known truncated Q1 master and any export missing the end screen."""
    banned = TRUNCATED_MASTER_SHA256 if banned is None else banned
    digest = file_sha256(export)
    if digest in banned:
        return f"truncated_master sha256={digest}"
    if vo is not None and vo.is_file():
        vo_d = probe_duration(vo)
        ex_d = probe_duration(export)
        needed = None if vo_d is None else vo_d + END_SCREEN
        if vo_d is not None and ex_d is not None and needed is not None and ex_d + 0.75 < needed:
            return (
                f"end_screen_missing export={ex_d:.2f}s vo={vo_d:.2f}s "
                f"need>={needed:.2f}s"
            )
    return None


def export_path(packet: Path) -> Path:
    return packet / EXPORT_REL


def fingerprint(packet: Path, meta: dict, export: Path | None) -> str:
    """Content identity for idempotency. Do not include mtime.

    Actions rematerializes the same release asset with a new mtime. A clock
    in this hash would miss the persisted video id and upload a second copy.
    """
    h = hashlib.sha256()
    h.update(packet.name.encode("utf-8"))
    h.update(b"\n")
    h.update((meta.get("title") or "").encode("utf-8"))
    h.update(b"\n")
    h.update((meta.get("description") or "").encode("utf-8"))
    if export and export.is_file():
        h.update(file_sha256(export).encode("utf-8"))
    return h.hexdigest()[:16]


def completed_without_id(prior: dict | None, fingerprint_value: str) -> bool:
    """True when a finishing PUT was accepted and the session can no longer return an id.

    Matching fingerprint must not start another videos.insert. A different
    fingerprint is a different export and is not this hold.
    """
    if not prior or str(prior.get("provider_video_id") or "").strip():
        return False
    if prior.get("fingerprint") != fingerprint_value:
        return False
    return bool(prior.get("completed_without_id"))


def existing_upload_action(
    prior: dict | None,
    fingerprint_value: str,
    *,
    caption_file: bool,
    thumbnail_file: bool,
) -> str:
    """Classify a persisted provider video id before another execute.

    Returns none, resume, finished, or mismatch. Mismatch must not upload again.
    not_attempted captions or thumbnails still need a resume when the local file exists.
    """
    if not prior or not str(prior.get("provider_video_id") or "").strip():
        return "none"
    if prior.get("fingerprint") != fingerprint_value:
        return "mismatch"
    caption_status = (prior.get("caption_upload") or {}).get("status")
    thumb_status = (prior.get("thumbnail_upload") or {}).get("status")
    comment_status = (prior.get("comment_post") or {}).get("status")
    if caption_file and caption_status not in {"uploaded", "already_uploaded"}:
        return "resume"
    if thumbnail_file and thumb_status not in {"uploaded", "already_uploaded"}:
        return "resume"
    if comment_status == "failed":
        return "resume"
    return "finished"


def auth_status(env: dict[str, str] | None = None) -> dict:
    source = env if env is not None else os.environ
    present = {key: bool(str(source.get(key, "")).strip()) for key in OAUTH_KEYS}
    missing = [k for k, ok in present.items() if not ok]
    return {
        "complete": not missing,
        "missing": missing,
        "api_key_alone": bool(str(source.get("YOUTUBE_API_KEY", "")).strip()) and bool(missing),
        "channel_id_set": bool(str(source.get("YOUTUBE_CHANNEL_ID", "")).strip()),
        "scope": UPLOAD_SCOPE,
        "required_scopes": [UPLOAD_SCOPE, FORCE_SSL_SCOPE, ANALYTICS_SCOPE],
        "scope_note": "youtube.upload alone can insert a video and then fail captions.insert",
        "state": AUTH_STATE if missing else "YOUTUBE_AUTH_PRESENT",
    }


def load_prior_state(packet: Path) -> dict | None:
    path = packet / STATE_NAME
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if not isinstance(data, dict):
        return None
    return data


def inspect_upload(packet: Path, env: dict[str, str] | None = None) -> dict:
    pub = packet / "publish.md"
    text = pub.read_text(encoding="utf-8") if pub.is_file() else ""
    meta = parse_publish(text)
    if not meta["title"]:
        meta["title"] = primary_title(packet)
    exp = export_path(packet)
    header_ok = exp.is_file() and exp.stat().st_size > 0 and mp4_header_ok(exp)
    block = master_block_reason(exp, packet_vo(packet)) if header_ok else None
    export_ok = header_ok and block is None
    auth = auth_status(env)
    prior = load_prior_state(packet)
    fp = fingerprint(packet, meta, exp if export_ok else None)
    existing = existing_upload_action(
        prior,
        fp,
        caption_file=(packet / "captions.srt").is_file(),
        thumbnail_file=(packet / "thumbnail.png").is_file(),
    )
    duplicate = existing == "finished"

    checks = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    add("publish_md_present", pub.is_file(), "publish.md" if pub.is_file() else "missing publish.md")
    add("title_present", bool(meta["title"]), meta["title"] or "empty title")
    add("description_usable", meta["word_count"] >= 12, f"{meta['word_count']} words")
    copy_block = copy_block_reason(text, meta)
    add("publish_copy_approved", copy_block is None, copy_block or "description and human checklist approved")
    meta_block = metadata_block_reason(meta)
    add("metadata_within_provider_limits", meta_block is None, meta_block or "title, description, and tags fit videos.insert")
    chapter_block = chapter_sync_reason(packet, meta.get("description") or "")
    add(
        "chapters_in_description",
        chapter_block is None,
        chapter_block or "drafted chapter lines are present and YouTube-shaped, or chapters.md is absent",
    )
    content_block = content_rule_reason(packet)
    add(
        "content_rules_clear",
        content_block is None,
        content_block or "quality, claim, and title scans clear, or those files are absent",
    )
    artifact_block = artifact_block_reason(packet, meta)
    add(
        "artifacts_within_provider_limits",
        artifact_block is None,
        artifact_block or "thumbnail and captions fit thumbnails.set and captions.insert",
    )
    add("tags_present", bool(meta["tags"]), f"{len(meta['tags'])} tags")
    add(
        "master_export_present",
        export_ok,
        EXPORT_REL if export_ok else (block or f"missing or invalid {EXPORT_REL}"),
    )
    add("not_truncated_end_screen", block is None, block or "end screen not proven missing")
    add("oauth_complete", auth["complete"], auth["state"] if auth["complete"] else ",".join(auth["missing"]))
    add("not_api_key_only", not auth["api_key_alone"], "API key is not upload authorization")
    add(
        "no_duplicate_fingerprint",
        existing != "finished",
        fp if existing == "none" else f"{existing}:{fp}",
    )
    add(
        "existing_video_matches_export",
        existing != "mismatch",
        "no persisted video" if existing == "none" else existing,
    )
    origin = vo_origin_kind(packet)
    synthetic = synthetic_media_flag(origin)
    add(
        "synthetic_disclosure_known",
        synthetic is not None,
        f"containsSyntheticMedia={synthetic} kind={origin}" if synthetic is not None else "vo_origin.md kind must be generated or human",
    )
    designation = audience_designation()
    kids = made_for_kids_flag(designation)
    add(
        "audience_known",
        kids is not None,
        f"selfDeclaredMadeForKids={kids} designation={designation}" if kids is not None else "docs/channel.md audience_designation must be not_made_for_kids or made_for_kids",
    )
    category = category_id()
    add(
        "category_known",
        category in ASSIGNABLE_CATEGORY_IDS,
        f"categoryId={category}" if category in ASSIGNABLE_CATEGORY_IDS else "docs/channel.md category_id must be an assignable videoCategories id",
    )
    license_value = channel_license()
    add(
        "license_known",
        license_value in CHANNEL_LICENSES,
        f"license={license_value}" if license_value in CHANNEL_LICENSES else "docs/channel.md license must be youtube or creativeCommon",
    )

    hard_local = [c for c in checks if c["name"] in {"publish_md_present", "title_present", "master_export_present", "publish_copy_approved", "metadata_within_provider_limits", "artifacts_within_provider_limits", "chapters_in_description", "content_rules_clear", "synthetic_disclosure_known", "audience_known", "category_known", "license_known"}]
    local_ok = all(c["ok"] for c in hard_local)
    if not local_ok:
        gate = "FAIL"
        action = "HOLD_LOCAL"
    elif completed_without_id(prior, fp):
        gate = "FAIL"
        action = "HOLD_COMPLETED_WITHOUT_ID"
    elif not auth["complete"]:
        gate = AUTH_STATE
        action = "DRY_RUN"
    elif existing == "mismatch":
        gate = "FAIL"
        action = "HOLD_FINGERPRINT_MISMATCH"
    elif existing == "finished":
        gate = "FAIL"
        action = "HOLD_IDEMPOTENT"
    elif existing == "resume":
        gate = "RESUME"
        action = "RESUME_POST_UPLOAD"
    else:
        gate = "READY"
        action = "UPLOAD_BLOCKED_NO_NETWORK"

    return {
        "packet": packet.name,
        "drop": selected_vo_drop(packet),
        "export": EXPORT_REL,
        "export_present": export_ok,
        "meta": meta,
        "auth": auth,
        "fingerprint": fp,
        "privacy": DEFAULT_PRIVACY,
        "contains_synthetic_media": synthetic,
        "vo_origin_kind": origin,
        "made_for_kids": kids,
        "audience_designation": designation,
        "category_id": category,
        "license": license_value,
        "checks": checks,
        "gate": gate,
        "action": action,
        "prior": prior,
        "captions": caption_track(packet),
        "thumbnail": thumbnail_track(packet),
        "generated": _now(),
    }



def thumbnail_track(packet: Path) -> dict:
    """Local thumbnail draft for a later thumbnails.set. This adapter never uploads it."""
    path = packet / "thumbnail.png"
    if not path.is_file():
        return {
            "path": "thumbnail.png",
            "present": False,
            "uploaded": False,
            "note": "missing draft; thumbnails.set is not called",
        }
    return {
        "path": "thumbnail.png",
        "present": True,
        "sha256": file_sha256(path),
        "uploaded": False,
        "note": "draft only; not a design sign-off; thumbnails.set is not called",
    }


def caption_track(packet: Path) -> dict:
    """Local captions draft for a later captions.insert. This adapter never uploads it."""
    path = packet / "captions.srt"
    if not path.is_file():
        return {
            "path": "captions.srt",
            "present": False,
            "uploaded": False,
            "note": "missing draft; captions.insert is not called",
        }
    raw = path.read_text(encoding="utf-8")
    cues = [b for b in raw.strip().split("\n\n") if b.strip()]
    return {
        "path": "captions.srt",
        "present": True,
        "cues": len(cues),
        "sha256": file_sha256(path),
        "uploaded": False,
        "note": "draft only; not ASR; captions.insert is not called; spot-check stays human",
    }


def vo_origin_kind(packet: Path) -> str:
    """Return generated, human, or unknown. Do not invent a recording."""
    path = packet / "vo_origin.md"
    if not path.is_file():
        return "unknown"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lower().startswith("kind:"):
            kind = line.split(":", 1)[1].strip().lower()
            return kind if kind in {"generated", "human"} else "unknown"
    return "unknown"


def synthetic_media_flag(kind: str) -> bool | None:
    """YouTube status.containsSyntheticMedia. None means do not insert.

    Generated narration is altered speech and must be disclosed. A human take
    is disclosed as false. Text cards alone are not a reason to invent true.
    """
    if kind == "generated":
        return True
    if kind == "human":
        return False
    return None


# Assignable videoCategories as of the Data API list. Do not invent 27.
ASSIGNABLE_CATEGORY_IDS = frozenset(
    {"1", "2", "10", "15", "17", "19", "20", "22", "23", "24", "25", "26", "27", "28", "29"}
)
CHANNEL_LICENSES = frozenset({"youtube", "creativeCommon"})


def channel_line(key: str, root: Path | None = None) -> str:
    """Read one docs/channel.md field. Missing file or key is empty."""
    path = (root or Path(__file__).resolve().parents[1]) / "docs" / "channel.md"
    if not path.is_file():
        return ""
    prefix = key.lower() + ":"
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.lower().startswith(prefix):
            return line.split(":", 1)[1].strip()
    return ""


def audience_designation(root: Path | None = None) -> str:
    """Read docs/channel.md. Do not invent made-for-kids."""
    value = channel_line("audience_designation", root).lower()
    return value if value in {"not_made_for_kids", "made_for_kids"} else "unknown"


def category_id(root: Path | None = None) -> str:
    """Read snippet.categoryId. Do not default a missing id to 27."""
    value = channel_line("category_id", root)
    return value if value in ASSIGNABLE_CATEGORY_IDS else "unknown"


def channel_license(root: Path | None = None) -> str:
    """Read status.license. Do not invent creativeCommon."""
    value = channel_line("license", root)
    return value if value in CHANNEL_LICENSES else "unknown"


def made_for_kids_flag(designation: str) -> bool | None:
    """YouTube status.selfDeclaredMadeForKids. None means do not insert.

    Omitting the field is not false. YouTube then blocks the video until Studio
    sets the audience. This channel is not_made_for_kids unless channel.md changes.
    """
    if designation == "not_made_for_kids":
        return False
    if designation == "made_for_kids":
        return True
    return None


def request_body(report: dict) -> dict:
    meta = report["meta"]
    status = {
        "privacyStatus": report["privacy"],
    }
    kids = report.get("made_for_kids")
    if not isinstance(kids, bool):
        kids = made_for_kids_flag(audience_designation())
    if isinstance(kids, bool):
        status["selfDeclaredMadeForKids"] = kids
    if isinstance(report.get("contains_synthetic_media"), bool):
        status["containsSyntheticMedia"] = report["contains_synthetic_media"]
    category = report.get("category_id")
    if category not in ASSIGNABLE_CATEGORY_IDS:
        category = category_id()
    license_value = report.get("license")
    if license_value not in CHANNEL_LICENSES:
        license_value = channel_license()
    snippet = {
        "title": meta["title"],
        "description": meta["description"],
        "tags": meta["tags"],
        "defaultLanguage": CAPTION_LANGUAGE,
        "defaultAudioLanguage": CAPTION_LANGUAGE,
    }
    if category in ASSIGNABLE_CATEGORY_IDS:
        snippet["categoryId"] = category
    if license_value in CHANNEL_LICENSES:
        status["license"] = license_value
    return {
        "snippet": snippet,
        "status": status,
        "local": {
            "packet": report["packet"],
            "export": report["export"],
            "fingerprint": report["fingerprint"],
            "scope": UPLOAD_SCOPE,
            "required_scopes": [UPLOAD_SCOPE, FORCE_SSL_SCOPE, ANALYTICS_SCOPE],
            "scope_note": "do not mint a refresh token with youtube.upload alone",
            "captions": report.get("captions") or {
                "path": "captions.srt",
                "present": False,
                "uploaded": False,
                "note": "captions.insert is not called",
            },
            "thumbnail": report.get("thumbnail") or {
                "path": "thumbnail.png",
                "present": False,
                "uploaded": False,
                "note": "thumbnails.set is not called",
            },
        },
    }


def redacted_state(report: dict) -> dict:
    return {
        "packet": report["packet"],
        "generated": report["generated"],
        "gate": report["gate"],
        "action": report["action"],
        "fingerprint": report["fingerprint"],
        "privacy": report["privacy"],
        "export": report["export"],
        "export_present": report["export_present"],
        "auth_state": report["auth"]["state"],
        "missing_env": report["auth"]["missing"],
        "provider_video_id": None,
        "attempted_upload": False,
        "error_class": report["gate"] if report["gate"] != "READY" else None,
        "note": "dry-run only; this adapter never calls videos.insert",
    }


def write_upload_state(packet: Path, state: dict) -> None:
    dest = packet / STATE_NAME
    tmp = dest.with_suffix(dest.suffix + ".tmp")
    tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    tmp.replace(dest)


def execute_upload(packet: Path, report: dict, *, post_comment: bool = False) -> dict:
    meta_block = metadata_block_reason(report.get("meta") or {})
    if meta_block:
        raise YouTubeAPIError(0, f"METADATA_REJECTED:{meta_block}")
    chapter_block = chapter_sync_reason(packet, (report.get("meta") or {}).get("description") or "")
    if chapter_block:
        raise YouTubeAPIError(0, f"METADATA_REJECTED:{chapter_block}")
    artifact_block = artifact_block_reason(packet, report.get("meta") or {})
    if artifact_block:
        raise YouTubeAPIError(0, f"ARTIFACT_REJECTED:{artifact_block}")
    if report.get("privacy") != DEFAULT_PRIVACY:
        raise YouTubeAPIError(0, "PRIVACY_NOT_PRIVATE")
    if not isinstance(report.get("contains_synthetic_media"), bool):
        raise YouTubeAPIError(0, "SYNTHETIC_DISCLOSURE_UNKNOWN")
    if not isinstance(report.get("made_for_kids"), bool):
        raise YouTubeAPIError(0, "AUDIENCE_UNKNOWN")
    if report.get("category_id") not in ASSIGNABLE_CATEGORY_IDS:
        raise YouTubeAPIError(0, "METADATA_REJECTED:category_unknown")
    if report.get("license") not in CHANNEL_LICENSES:
        raise YouTubeAPIError(0, "METADATA_REJECTED:license_unknown")
    export = export_path(packet)
    prior = load_prior_state(packet)
    prior_video_id = None
    if prior and str(prior.get("provider_video_id") or "").strip():
        if prior.get("fingerprint") != report["fingerprint"]:
            raise YouTubeAPIError(0, "EXISTING_VIDEO_FINGERPRINT_MISMATCH")
        prior_video_id = str(prior.get("provider_video_id") or "").strip()
    if completed_without_id(prior, report["fingerprint"]):
        raise YouTubeAPIError(0, "HOLD_COMPLETED_WITHOUT_ID")
    if report["gate"] not in {"READY", "RESUME"} and not prior_video_id:
        raise YouTubeAPIError(0, f"LOCAL_GATE_{report['gate']}")

    result = {
        "packet": packet.name,
        "generated": _now(),
        "fingerprint": report["fingerprint"],
        "privacy": report["privacy"],
        "attempted_upload": bool(not prior_video_id),
        "provider_video_id": prior_video_id,
        "video_upload": {"status": "resuming" if prior_video_id else "pending"},
        "caption_upload": prior.get("caption_upload", {"status": "not_attempted"}) if prior else {"status": "not_attempted"},
        "thumbnail_upload": prior.get("thumbnail_upload", {"status": "not_attempted"}) if prior else {"status": "not_attempted"},
        "comment_post": prior.get("comment_post", {"status": "not_attempted"}) if prior else {"status": "not_attempted"},
    }
    try:
        token = refresh_access_token()
        granted = access_token_scopes(token)
        scope_gap = missing_provider_scopes(
            granted,
            captions=(packet / "captions.srt").is_file()
            and result["caption_upload"].get("status") not in {"uploaded", "already_uploaded"},
            thumbnail=(packet / "thumbnail.png").is_file()
            and result["thumbnail_upload"].get("status") not in {"uploaded", "already_uploaded"},
            comment=bool(
                post_comment
                and report["meta"].get("pin_comment")
                and result["comment_post"].get("status") not in {"posted", "already_posted"}
            ),
        )
        if scope_gap:
            raise YouTubeAPIError(0, "SCOPE_INSUFFICIENT:" + ",".join(scope_gap))
        if prior_video_id:
            video_id = prior_video_id
            result["video_upload"] = {"status": "already_uploaded", "video_id": video_id}
            stamp = preserved_upload_stamp(prior)
            if stamp:
                result["video_upload"]["uploaded_at"] = stamp
                result["uploaded_at"] = stamp
        else:
            video = upload_video(
                token,
                export_path=export,
                metadata={
                    "snippet": request_body(report)["snippet"],
                    "status": {
                        "containsSyntheticMedia": report["contains_synthetic_media"],
                        "selfDeclaredMadeForKids": report["made_for_kids"],
                        "license": report["license"],
                    },
                },
                privacy=report["privacy"],
            )
            video_id = str(video.get("id") or "").strip()
            if not video_id:
                raise YouTubeAPIError(0, "upload_response_missing_video_id")
            result["provider_video_id"] = video_id
            stamp = _now()
            result["uploaded_at"] = stamp
            result["video_upload"] = {"status": "uploaded", "video_id": video_id, "uploaded_at": stamp}
            # Persist the provider ID immediately so a later caption/thumbnail failure
            # can resume without re-uploading the video.
            write_upload_state(packet, result)

        captions = packet / "captions.srt"
        if captions.is_file() and result["caption_upload"].get("status") not in {"uploaded", "already_uploaded"}:
            try:
                # Captions.insert before processing finishes is a 400. That status is
                # permanent here, so wait first. A not-ready result is a caption miss,
                # not a second videos.insert.
                wait_for_caption_ready(token, video_id=video_id)
                cap = insert_caption(
                    token,
                    video_id=video_id,
                    caption_path=captions,
                    language=CAPTION_LANGUAGE,
                    name=CAPTION_NAME,
                )
                result["caption_upload"] = {"status": "uploaded", "caption_id": cap.get("id")}
            except Exception as exc:
                result["caption_upload"] = {"status": "failed", "error": compact_api_error(exc)}
            write_upload_state(packet, result)

        thumb = packet / "thumbnail.png"
        if thumb.is_file() and result["thumbnail_upload"].get("status") not in {"uploaded", "already_uploaded"}:
            try:
                set_thumbnail(token, video_id=video_id, thumbnail_path=thumb)
                result["thumbnail_upload"] = {"status": "uploaded"}
            except Exception as exc:
                result["thumbnail_upload"] = {"status": "failed", "error": compact_api_error(exc)}
            write_upload_state(packet, result)

        if post_comment and report["meta"].get("pin_comment") and result["comment_post"].get("status") not in {"posted", "already_posted"}:
            try:
                from youtube_api import get_channel_id
                channel_id = get_channel_id(token)
                comment = insert_top_level_comment(
                    token,
                    video_id=video_id,
                    channel_id=channel_id,
                    text=report["meta"]["pin_comment"],
                )
                result["comment_post"] = {
                    "status": "posted",
                    "comment_id": comment.get("id"),
                    "pinned": False,
                    "pin_note": "commentThreads.insert does not pin; Studio pin stays manual",
                }
            except Exception as exc:
                result["comment_post"] = {"status": "failed", "error": compact_api_error(exc)}
            write_upload_state(packet, result)

        incomplete = incomplete_post_uploads(result)
        result["generated"] = _now()
        if incomplete:
            result["error_class"] = "POST_UPLOAD_INCOMPLETE:" + ",".join(incomplete)
            write_upload_state(packet, result)
            raise YouTubeAPIError(0, result["error_class"])
        result["error_class"] = None
        write_upload_state(packet, result)
        return result
    except Exception as exc:
        reason = getattr(exc, "reason", "")
        if result.get("provider_video_id") and str(reason).startswith("POST_UPLOAD_INCOMPLETE"):
            write_upload_state(packet, result)
            raise
        if str(reason).startswith("SCOPE_INSUFFICIENT"):
            raise
        if str(reason) == "RESUMABLE_COMPLETED_SESSION_GONE":
            result["provider_video_id"] = None
            result["completed_without_id"] = True
            result["attempted_upload"] = True
            result["video_upload"] = {"status": "completed_session_gone"}
            result["error_class"] = "RESUMABLE_COMPLETED_SESSION_GONE"
            write_upload_state(packet, result)
            raise
        result["video_upload"] = result.get("video_upload") or {"status": "failed"}
        result["error_class"] = compact_api_error(exc)
        write_upload_state(packet, result)
        raise

def render_text(report: dict) -> str:
    lines = [
        f"packet: {report['packet']}",
        f"gate: {report['gate']}",
        f"action: {report['action']}",
        f"drop: {report['drop']}",
        f"export: {report['export']} present={'yes' if report['export_present'] else 'no'}",
        f"fingerprint: {report['fingerprint']}",
        f"privacy: {report['privacy']}",
        "captions: {path} present={present} uploaded=no".format(
            path=(report.get("captions") or {}).get("path", "captions.srt"),
            present="yes" if (report.get("captions") or {}).get("present") else "no",
        ),
        f"auth: {report['auth']['state']}",
        "consent_scopes: youtube.upload youtube.force-ssl yt-analytics.readonly",
        "youtube.upload alone fails captions.insert after the video exists; do not mint that token",
        "dry-run default; --execute performs authenticated API calls only after all local gates pass",
        "an API key alone is not upload authorization",
        "a junk export/master.mp4 is not a master",
        "captions.srt stays a draft in dry-run; --execute calls captions.insert and fails closed if that call fails",
        "thumbnail: {path} present={present} uploaded=no".format(
            path=(report.get("thumbnail") or {}).get("path", "thumbnail.png"),
            present="yes" if (report.get("thumbnail") or {}).get("present") else "no",
        ),
        "thumbnail.png stays a draft in dry-run; --execute calls thumbnails.set and fails closed if that call fails",
    ]
    for c in report["checks"]:
        mark = "PASS" if c["ok"] else "FAIL"
        lines.append(f"- {mark} {c['name']}: {c['detail']}")
    body = request_body(report)
    lines.append("dry_run_request:")
    lines.append(json.dumps(body, indent=2, ensure_ascii=False))
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="YouTube upload adapter. Dry-run by default; --execute performs authenticated writes."
    )
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument(
        "--write-state",
        action="store_true",
        help="Write redacted dry-run upload_state.json (never contains secrets)",
    )
    parser.add_argument(
        "--execute",
        action="store_true",
        help="Perform the authenticated video upload and available post-upload artifacts.",
    )
    parser.add_argument(
        "--post-comment",
        action="store_true",
        help="Post the first comment even if the approval box parser missed it.",
    )
    parser.add_argument(
        "--skip-comment",
        action="store_true",
        help="Do not post the approved first comment on this execute.",
    )
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    report = inspect_upload(path)
    sys.stdout.write(render_text(report))
    if report["gate"] == AUTH_STATE and not args.execute:
        if args.write_state:
            dest = path / STATE_NAME
            dest.write_text(json.dumps(redacted_state(report), indent=2) + "\n", encoding="utf-8")
            print(dest)
        return 3
    if report["gate"] == "FAIL":
        if args.write_state:
            dest = path / STATE_NAME
            dest.write_text(json.dumps(redacted_state(report), indent=2) + "\n", encoding="utf-8")
            print(dest)
        return 2
    if args.execute:
        try:
            post_comment = should_post_comment(
                report.get("meta") or {},
                requested=args.post_comment,
                skipped=args.skip_comment,
            )
            state = execute_upload(path, report, post_comment=post_comment)
            print(json.dumps(state, indent=2, ensure_ascii=False))
            return 0
        except YouTubeAPIError as exc:
            print(json.dumps({"error": compact_api_error(exc)}, ensure_ascii=False), file=sys.stderr)
            return 3 if exc.reason == "YOUTUBE_AUTH_REQUIRED" else 4
        except Exception as exc:
            print(json.dumps({"error": compact_api_error(exc)}, ensure_ascii=False), file=sys.stderr)
            return 4
    if args.write_state:
        dest = path / STATE_NAME
        dest.write_text(json.dumps(redacted_state(report), indent=2) + "\n", encoding="utf-8")
        print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
