#!/usr/bin/env python3
"""Freeze upload error reasons until a live execute records one.

Runs 281-306 added provider status and snippet gates while the publish
gate stayed the missing OAuth secrets. A new YouTubeAPIError reason in
youtube_api.py or youtube_upload.py is a failed selftest unless
docs/live_execute_evidence.md contains a line:

    live_status: REASON_CODE

Do not add a reason to this allowlist to bypass that file.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
EVIDENCE = ROOT / "docs" / "live_execute_evidence.md"

# Static reason prefixes already in the client as of Run 307.
# A new literal must be named in live_execute_evidence.md first.
FROZEN_REASONS = frozenset(
    {
        "ARTIFACT_REJECTED",
        "AUDIENCE_UNKNOWN",
        "EXISTING_VIDEO_FINGERPRINT_MISMATCH",
        "EXPORT_EMPTY",
        "HOLD_COMPLETED_WITHOUT_ID",
        "LOCAL_GATE_",
        "METADATA_REJECTED",
        "POST_UPLOAD_RETRY_EXHAUSTED",
        "POST_UPLOAD_TOKEN_REFRESH_EXHAUSTED",
        "PRIVACY_NOT_PRIVATE",
        "RESUMABLE_COMPLETED_SESSION_GONE",
        "RESUMABLE_MISSING_VIDEO_ID",
        "RESUMABLE_RETRY_EXHAUSTED",
        "RESUMABLE_SESSION_EXPIRED",
        "RESUMABLE_SESSION_MISSING",
        "RESUMABLE_STALLED",
        "RESUMABLE_TOKEN_REFRESH_EXHAUSTED",
        "RESUMABLE_UNEXPECTED_STATUS",
        "SCOPE_CHECK_FAILED",
        "SCOPE_INSUFFICIENT",
        "SYNTHETIC_DISCLOSURE_UNKNOWN",
        "VIDEO_PROCESSING_FAILED",
        "VIDEO_PROCESSING_NOT_READY",
        "YOUTUBE_AUTH_REQUIRED",
        "channel_id_unavailable",
        "invalid_json_response",
        "invalid_token_response",
        "network_error",
        "oauth_refresh_failed",
        "unexpected_json_shape",
        "upload_response_missing_video_id",
    }
)

REASON_RE = re.compile(
    r"YouTubeAPIError\(\s*[^,\n]+,\s*(?:f)?([\"'])([A-Za-z][A-Za-z0-9_]*)"
)
SCAN_FILES = ("youtube_api.py", "youtube_upload.py")


def reason_prefixes(text: str) -> set[str]:
    return {match.group(2) for match in REASON_RE.finditer(text)}


def evidence_allows(code: str, evidence: str) -> bool:
    return f"live_status: {code}" in evidence


def unexplained(found: set[str], evidence: str) -> list[str]:
    extra = []
    for code in sorted(found):
        if code in FROZEN_REASONS:
            continue
        if evidence_allows(code, evidence):
            continue
        extra.append(code)
    return extra


def check_texts(texts: dict[str, str], evidence: str) -> list[str]:
    failures = []
    for name, text in texts.items():
        for code in unexplained(reason_prefixes(text), evidence):
            failures.append(
                f"{name} adds YouTubeAPIError reason {code} without "
                "docs/live_execute_evidence.md live_status line"
            )
    return failures


def check_repo(root: Path = ROOT) -> list[str]:
    texts = {}
    for name in SCAN_FILES:
        path = root / "tools" / name
        if not path.is_file():
            return [f"missing {path}"]
        texts[name] = path.read_text(encoding="utf-8")
    evidence_path = root / "docs" / "live_execute_evidence.md"
    evidence = evidence_path.read_text(encoding="utf-8") if evidence_path.is_file() else ""
    return check_texts(texts, evidence)


def main() -> int:
    failures = check_repo()
    if failures:
        print("UPLOAD VARIANT FREEZE FAIL")
        for row in failures:
            print(row)
        return 1
    print("UPLOAD VARIANT FREEZE PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
