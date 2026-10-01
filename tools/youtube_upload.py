#!/usr/bin/env python3
"""Credential-ready YouTube upload adapter.

Dry-run only unless every local gate passes AND OAuth env vars exist.
Never prints secret values. Never calls the YouTube API from this tool.
Never bumps packet status. Never treats a named export as a master.
A junk export/master.mp4 is not a master; require an ISO BMFF ftyp box.
"""

from __future__ import annotations

import argparse
import hashlib
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

AUTH_STATE = "YOUTUBE_AUTH_REQUIRED"
OAUTH_KEYS = ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN")
# Run 249 master is VO-length only. Do not upload it. Run 253 is the padded export.
TRUNCATED_MASTER_SHA256 = {
    "abec4eb94199d0cbbf00659891d4e79c0040a6b1bb5450fa6e1db0e54c4b4d53",
}
UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
DEFAULT_PRIVACY = "private"
EXPORT_REL = "export/master.mp4"
STATE_NAME = "upload_state.json"


def _now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


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
    h = hashlib.sha256()
    h.update(packet.name.encode("utf-8"))
    h.update(b"\n")
    h.update((meta.get("title") or "").encode("utf-8"))
    h.update(b"\n")
    h.update((meta.get("description") or "").encode("utf-8"))
    if export and export.is_file():
        h.update(str(export.stat().st_size).encode("utf-8"))
        h.update(b"\n")
        h.update(str(int(export.stat().st_mtime)).encode("utf-8"))
    return h.hexdigest()[:16]


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
    duplicate = bool(prior and prior.get("fingerprint") == fp and prior.get("provider_video_id"))

    checks = []

    def add(name: str, ok: bool, detail: str) -> None:
        checks.append({"name": name, "ok": ok, "detail": detail})

    add("publish_md_present", pub.is_file(), "publish.md" if pub.is_file() else "missing publish.md")
    add("title_present", bool(meta["title"]), meta["title"] or "empty title")
    add("description_usable", meta["word_count"] >= 12, f"{meta['word_count']} words")
    add("tags_present", bool(meta["tags"]), f"{len(meta['tags'])} tags")
    add(
        "master_export_present",
        export_ok,
        EXPORT_REL if export_ok else (block or f"missing or invalid {EXPORT_REL}"),
    )
    add("not_truncated_end_screen", block is None, block or "end screen not proven missing")
    add("oauth_complete", auth["complete"], auth["state"] if auth["complete"] else ",".join(auth["missing"]))
    add("not_api_key_only", not auth["api_key_alone"], "API key is not upload authorization")
    add("no_duplicate_fingerprint", not duplicate, fp)

    hard_local = [c for c in checks if c["name"] in {"publish_md_present", "title_present", "master_export_present"}]
    local_ok = all(c["ok"] for c in hard_local)
    if not local_ok:
        gate = "FAIL"
        action = "HOLD_LOCAL"
    elif not auth["complete"]:
        gate = AUTH_STATE
        action = "DRY_RUN"
    elif duplicate:
        gate = "FAIL"
        action = "HOLD_IDEMPOTENT"
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
        "checks": checks,
        "gate": gate,
        "action": action,
        "prior": prior,
        "generated": _now(),
    }


def request_body(report: dict) -> dict:
    meta = report["meta"]
    return {
        "snippet": {
            "title": meta["title"],
            "description": meta["description"],
            "tags": meta["tags"][:12],
            "categoryId": "27",
        },
        "status": {
            "privacyStatus": report["privacy"],
            "selfDeclaredMadeForKids": False,
        },
        "local": {
            "packet": report["packet"],
            "export": report["export"],
            "fingerprint": report["fingerprint"],
            "scope": UPLOAD_SCOPE,
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


def render_text(report: dict) -> str:
    lines = [
        f"packet: {report['packet']}",
        f"gate: {report['gate']}",
        f"action: {report['action']}",
        f"drop: {report['drop']}",
        f"export: {report['export']} present={'yes' if report['export_present'] else 'no'}",
        f"fingerprint: {report['fingerprint']}",
        f"privacy: {report['privacy']}",
        f"auth: {report['auth']['state']}",
        "youtube_upload never prints secret values and never calls the API",
        "an API key alone is not upload authorization",
        "a junk export/master.mp4 is not a master",
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
        description="Dry-run YouTube upload adapter. No API. No secrets printed."
    )
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument(
        "--write-state",
        action="store_true",
        help="Write redacted upload_state.json (never contains secrets)",
    )
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    report = inspect_upload(path)
    sys.stdout.write(render_text(report))
    if args.write_state:
        dest = path / STATE_NAME
        dest.write_text(json.dumps(redacted_state(report), indent=2) + "\n", encoding="utf-8")
        print(dest)
    if report["gate"] == AUTH_STATE:
        return 3
    if report["gate"] == "FAIL":
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
