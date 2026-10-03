#!/usr/bin/env python3
"""Small dependency-free YouTube OAuth/Data/Analytics HTTP client.

The client intentionally uses only the Python standard library so the production
runner does not need google-api-python-client. It never prints tokens or client
secrets. Callers choose explicitly whether to perform provider writes/reads.
"""

from __future__ import annotations

import json
import mimetypes
import os
import secrets
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from pathlib import Path
from typing import Any, Mapping

TOKEN_URL = "https://oauth2.googleapis.com/token"
TOKENINFO_URL = "https://oauth2.googleapis.com/tokeninfo"
DATA_BASE = "https://www.googleapis.com/youtube/v3"
UPLOAD_BASE = "https://www.googleapis.com/upload/youtube/v3"
ANALYTICS_BASE = "https://youtubeanalytics.googleapis.com/v2"

OAUTH_KEYS = ("YOUTUBE_CLIENT_ID", "YOUTUBE_CLIENT_SECRET", "YOUTUBE_REFRESH_TOKEN")
UPLOAD_SCOPE = "https://www.googleapis.com/auth/youtube.upload"
FORCE_SSL_SCOPE = "https://www.googleapis.com/auth/youtube.force-ssl"
READONLY_SCOPE = "https://www.googleapis.com/auth/youtube.readonly"
ANALYTICS_SCOPE = "https://www.googleapis.com/auth/yt-analytics.readonly"


class YouTubeAPIError(RuntimeError):
    def __init__(self, status: int, reason: str, detail: str = "") -> None:
        self.status = status
        self.reason = reason or "api_error"
        self.detail = detail
        super().__init__(f"HTTP {status}: {self.reason}")


def _json_bytes(obj: Mapping[str, Any]) -> bytes:
    return json.dumps(obj, ensure_ascii=False, separators=(",", ":")).encode("utf-8")


def _read_error(exc: urllib.error.HTTPError) -> tuple[int, str, str]:
    try:
        raw = exc.read(64 * 1024)
        body = json.loads(raw.decode("utf-8", errors="replace"))
        error = body.get("error", body)
        reason = str(error.get("status") or error.get("errors", [{}])[0].get("reason") or "api_error")
        message = str(error.get("message") or "")
        return int(exc.code), reason, message[:500]
    except Exception:
        return int(exc.code), "http_error", ""


def _request(
    url: str,
    *,
    method: str = "GET",
    token: str | None = None,
    body: bytes | None = None,
    content_type: str | None = None,
    accept: str = "application/json",
    timeout: int = 120,
) -> bytes:
    headers = {"Accept": accept, "User-Agent": "Content-Automation/1.0"}
    if token:
        headers["Authorization"] = f"Bearer {token}"
    if content_type:
        headers["Content-Type"] = content_type
    req = urllib.request.Request(url, data=body, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read()
    except urllib.error.HTTPError as exc:
        status, reason, detail = _read_error(exc)
        raise YouTubeAPIError(status, reason, detail) from exc
    except urllib.error.URLError as exc:
        raise YouTubeAPIError(0, "network_error", str(exc.reason)[:500]) from exc


def access_token_scopes(token: str) -> set[str]:
    """Return granted scopes. Never include the token in an error detail."""
    if not str(token or "").strip():
        raise YouTubeAPIError(0, "SCOPE_CHECK_FAILED", "empty_token")
    try:
        raw = _request(
            TOKENINFO_URL + "?" + urllib.parse.urlencode({"access_token": token}),
            method="GET",
        )
    except YouTubeAPIError as exc:
        raise YouTubeAPIError(exc.status, "SCOPE_CHECK_FAILED", exc.reason) from exc
    try:
        data = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise YouTubeAPIError(0, "SCOPE_CHECK_FAILED", "invalid_tokeninfo") from exc
    scope = data.get("scope") if isinstance(data, dict) else ""
    return {part for part in str(scope or "").split() if part.startswith("https://")}


def refresh_access_token(env: Mapping[str, str] | None = None) -> str:
    source = env if env is not None else os.environ
    missing = [k for k in OAUTH_KEYS if not str(source.get(k, "")).strip()]
    if missing:
        raise YouTubeAPIError(0, "YOUTUBE_AUTH_REQUIRED", ",".join(missing))
    form = urllib.parse.urlencode(
        {
            "client_id": source["YOUTUBE_CLIENT_ID"],
            "client_secret": source["YOUTUBE_CLIENT_SECRET"],
            "refresh_token": source["YOUTUBE_REFRESH_TOKEN"],
            "grant_type": "refresh_token",
        }
    ).encode("utf-8")
    raw = _request(
        TOKEN_URL,
        method="POST",
        body=form,
        content_type="application/x-www-form-urlencoded",
    )
    try:
        data = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise YouTubeAPIError(0, "invalid_token_response") from exc
    token = str(data.get("access_token") or "").strip()
    if not token:
        err = str(data.get("error") or "no_access_token")
        raise YouTubeAPIError(0, "oauth_refresh_failed", err)
    return token


def _query_url(base: str, path: str, params: Mapping[str, Any] | None = None) -> str:
    url = base.rstrip("/") + "/" + path.lstrip("/")
    if params:
        query = [(k, v) for k, v in params.items() if v is not None]
        if query:
            url += "?" + urllib.parse.urlencode(query)
    return url


def api_json(
    method: str,
    path: str,
    *,
    token: str,
    params: Mapping[str, Any] | None = None,
    body: Mapping[str, Any] | None = None,
    base: str = DATA_BASE,
    timeout: int = 120,
) -> dict[str, Any]:
    raw = _request(
        _query_url(base, path, params),
        method=method,
        token=token,
        body=_json_bytes(body) if body is not None else None,
        content_type="application/json; charset=UTF-8" if body is not None else None,
        timeout=timeout,
    )
    if not raw:
        return {}
    try:
        parsed = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise YouTubeAPIError(0, "invalid_json_response") from exc
    if not isinstance(parsed, dict):
        raise YouTubeAPIError(0, "unexpected_json_shape")
    return parsed


def _multipart_related(metadata: Mapping[str, Any], media: Path, media_type: str) -> tuple[bytes, str]:
    boundary = "CA" + secrets.token_hex(12)
    meta = _json_bytes(metadata)
    data = media.read_bytes()
    chunks = [
        f"--{boundary}\r\n".encode(),
        b"Content-Type: application/json; charset=UTF-8\r\n\r\n",
        meta,
        b"\r\n",
        f"--{boundary}\r\n".encode(),
        f"Content-Type: {media_type}\r\n\r\n".encode(),
        data,
        b"\r\n",
        f"--{boundary}--\r\n".encode(),
    ]
    return b"".join(chunks), f"multipart/related; boundary={boundary}"


def upload_related(
    path: str,
    *,
    token: str,
    metadata: Mapping[str, Any],
    media: Path,
    media_type: str,
    params: Mapping[str, Any] | None = None,
    timeout: int = 600,
) -> dict[str, Any]:
    body, content_type = _multipart_related(metadata, media, media_type)
    raw = _request(
        _query_url(UPLOAD_BASE, path, params),
        method="POST",
        token=token,
        body=body,
        content_type=content_type,
        timeout=timeout,
    )
    try:
        data = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise YouTubeAPIError(0, "invalid_json_response") from exc
    if not isinstance(data, dict):
        raise YouTubeAPIError(0, "unexpected_json_shape")
    return data


# YouTube requires every non-final chunk to be a multiple of 256 KiB.
RESUMABLE_CHUNK = 8 * 1024 * 1024
# Official resumable guide: 500/502/503/504 are resumeable, not permanent.
# 408 and 429 are resumeable on an existing session. A new videos.insert is not.
RESUMABLE_RETRYABLE = {408, 429, 500, 502, 503, 504}
RESUMABLE_RETRY_LIMIT = 3
RESUMABLE_BACKOFF_SECONDS = (1, 2, 4)


def _sleep(seconds: float) -> None:
    time.sleep(seconds)


def resume_offset(range_header: str | None, fallback: int) -> int:
    """Byte offset after a 308 Range header. `bytes=0-262143` means resume at 262144."""
    text = str(range_header or "")
    if "bytes=" in text:
        text = text.split("bytes=", 1)[1]
    text = text.strip().split(",")[-1].strip()
    if "-" not in text:
        return fallback
    end = text.split("-", 1)[1].strip()
    if not end.isdigit():
        return fallback
    return int(end) + 1


def received_offset(headers: Mapping[str, str]) -> int | None:
    """Resume point from a 308. None means Range was omitted, so nothing is stored.

    The YouTube resumable guide says a 308 with no Range header means the
    server has not received any bytes. Do not treat that as the chunk just sent.
    """
    raw = _header(headers, "Range")
    if not raw:
        return None
    return resume_offset(raw, 0)


def _pause(headers: Mapping[str, str], retries: int) -> None:
    """Backoff, and honor Retry-After when the guide says to wait before resume."""
    backoff = RESUMABLE_BACKOFF_SECONDS[min(retries, len(RESUMABLE_BACKOFF_SECONDS) - 1)]
    retry_after = _header(headers, "Retry-After").strip()
    extra = int(retry_after) if retry_after.isdigit() else 0
    _sleep(max(backoff, min(extra, 30)))


def _http(
    url: str,
    *,
    method: str,
    headers: Mapping[str, str],
    body: bytes | None,
    timeout: int,
) -> tuple[int, dict[str, str], bytes]:
    """Return status, headers, and body. 308 is a resumable progress signal, not a failure."""
    req = urllib.request.Request(url, data=body, headers=dict(headers), method=method)
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            hdrs = {k: v for k, v in resp.headers.items()}
            return int(resp.status), hdrs, resp.read()
    except urllib.error.HTTPError as exc:
        hdrs = {k: v for k, v in exc.headers.items()} if exc.headers else {}
        try:
            raw = exc.read(64 * 1024)
        except Exception:
            raw = b""
        if int(exc.code) == 308:
            return 308, hdrs, raw
        status, reason, detail = _read_error(exc)
        raise YouTubeAPIError(status, reason, detail) from exc
    except urllib.error.URLError as exc:
        raise YouTubeAPIError(0, "network_error", str(exc.reason)[:500]) from exc


def _header(headers: Mapping[str, str], name: str) -> str:
    want = name.lower()
    for key, value in headers.items():
        if key.lower() == want:
            return str(value)
    return ""



def _start_resumable_session(
    init_url: str,
    init_headers: Mapping[str, str],
    body: bytes,
) -> tuple[str, int]:
    """Start one resumable session. Retry only when no Location came back.

    A 503 on the chunk PUT must not call this again. That session already
    exists and a second videos.insert can hide it. A 503 on this POST with
    no Location has no session to resume, so a bounded retry is the same
    upload, not a second video.
    """
    last_code = 0
    headers: dict[str, str] = {}
    for attempt in range(RESUMABLE_RETRY_LIMIT):
        try:
            code, headers, _raw = _http(
                init_url,
                method="POST",
                headers=init_headers,
                body=body,
                timeout=120,
            )
        except YouTubeAPIError as exc:
            if exc.status not in RESUMABLE_RETRYABLE and exc.reason != "network_error":
                raise
            code, headers = exc.status, {}
        session = _header(headers, "Location")
        if session.startswith("https://"):
            return session, code
        last_code = code
        if code not in RESUMABLE_RETRYABLE and code != 0:
            return "", code
        if attempt + 1 >= RESUMABLE_RETRY_LIMIT:
            break
        _pause(headers, attempt)
    return "", last_code


def upload_video(
    token: str,
    *,
    export_path: Path,
    metadata: Mapping[str, Any],
    privacy: str,
) -> dict[str, Any]:
    """Insert a video with the resumable protocol.

    A single multipart POST of a multi-minute master is the wrong transport:
    proxies and the 20-minute Actions job drop it, and a lost response can hide
    a created video id. Captions and thumbnails stay multipart; they are small.
    """
    body = dict(metadata)
    status = dict(body.get("status") or {})
    status["privacyStatus"] = privacy
    status.setdefault("selfDeclaredMadeForKids", False)
    body["status"] = status
    size = export_path.stat().st_size
    if size <= 0:
        raise YouTubeAPIError(0, "EXPORT_EMPTY")
    init_headers = {
        "Authorization": f"Bearer {token}",
        "Content-Type": "application/json; charset=UTF-8",
        "X-Upload-Content-Length": str(size),
        "X-Upload-Content-Type": "video/mp4",
        "User-Agent": "Content-Automation/1.0",
    }
    init_url = _query_url(
        UPLOAD_BASE,
        "videos",
        {"part": "snippet,status", "uploadType": "resumable", "notifySubscribers": "false"},
    )
    session, code = _start_resumable_session(init_url, init_headers, _json_bytes(body))
    if not session.startswith("https://"):
        raise YouTubeAPIError(code, "RESUMABLE_SESSION_MISSING")
    offset = 0
    retries = 0
    empty_ranges = 0
    with export_path.open("rb") as handle:
        while offset < size:
            handle.seek(offset)
            chunk = handle.read(RESUMABLE_CHUNK)
            if not chunk:
                raise YouTubeAPIError(0, "RESUMABLE_STALLED", f"offset={offset}")
            end = offset + len(chunk) - 1
            put_headers = {
                "Authorization": f"Bearer {token}",
                "Content-Type": "video/mp4",
                "Content-Length": str(len(chunk)),
                "Content-Range": f"bytes {offset}-{end}/{size}",
                "User-Agent": "Content-Automation/1.0",
            }
            try:
                put_code, put_headers_out, raw = _http(
                    session,
                    method="PUT",
                    headers=put_headers,
                    body=chunk,
                    timeout=600,
                )
            except YouTubeAPIError as exc:
                if exc.status not in RESUMABLE_RETRYABLE and exc.reason != "network_error":
                    raise
                put_code, put_headers_out, raw = exc.status, {}, b""
            if put_code in {200, 201}:
                return _video_resource(put_code, raw)
            if put_code == 308:
                nxt = received_offset(put_headers_out)
                if nxt is None:
                    empty_ranges += 1
                    if empty_ranges >= RESUMABLE_RETRY_LIMIT:
                        raise YouTubeAPIError(308, "RESUMABLE_STALLED", f"offset={offset} missing_range")
                    _pause(put_headers_out, empty_ranges - 1)
                    offset = 0
                    continue
                if nxt <= offset or nxt > size:
                    raise YouTubeAPIError(308, "RESUMABLE_STALLED", f"offset={offset}")
                offset = nxt
                retries = 0
                empty_ranges = 0
                continue
            if put_code in RESUMABLE_RETRYABLE or put_code == 0:
                if retries >= RESUMABLE_RETRY_LIMIT:
                    raise YouTubeAPIError(put_code, "RESUMABLE_RETRY_EXHAUSTED", f"offset={offset}")
                _pause(put_headers_out, retries)
                retries += 1
                status_code, status_headers, status_raw = _query_resumable(session, token, size)
                if status_code in {200, 201}:
                    return _video_resource(status_code, status_raw)
                if status_code == 308:
                    nxt = received_offset(status_headers)
                    if nxt is None:
                        empty_ranges += 1
                        if empty_ranges >= RESUMABLE_RETRY_LIMIT:
                            raise YouTubeAPIError(308, "RESUMABLE_STALLED", f"offset={offset} missing_range")
                        offset = 0
                        continue
                    if nxt < 0 or nxt > size:
                        raise YouTubeAPIError(308, "RESUMABLE_STALLED", f"offset={offset}")
                    offset = nxt
                    retries = 0
                    continue
                if status_code == 404:
                    raise YouTubeAPIError(404, "RESUMABLE_SESSION_EXPIRED", f"offset={offset}")
                continue
            raise YouTubeAPIError(put_code, "RESUMABLE_UNEXPECTED_STATUS")
    raise YouTubeAPIError(0, "RESUMABLE_STALLED", "loop_ended")


def _video_resource(status: int, raw: bytes) -> dict[str, Any]:
    try:
        data = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise YouTubeAPIError(status, "invalid_json_response") from exc
    if not isinstance(data, dict) or not str(data.get("id") or "").strip():
        raise YouTubeAPIError(status, "RESUMABLE_MISSING_VIDEO_ID")
    return data


def _query_resumable(session: str, token: str, size: int) -> tuple[int, dict[str, str], bytes]:
    """Ask the session how many bytes it already has. Empty PUT, Content-Range bytes */size."""
    headers = {
        "Authorization": f"Bearer {token}",
        "Content-Length": "0",
        "Content-Range": f"bytes */{size}",
        "User-Agent": "Content-Automation/1.0",
    }
    try:
        return _http(session, method="PUT", headers=headers, body=b"", timeout=120)
    except YouTubeAPIError as exc:
        if exc.status in RESUMABLE_RETRYABLE or exc.reason == "network_error" or exc.status == 404:
            return exc.status, {}, b""
        raise


def insert_caption(
    token: str,
    *,
    video_id: str,
    caption_path: Path,
    language: str = "en",
    name: str = "English",
) -> dict[str, Any]:
    metadata = {
        "snippet": {
            "videoId": video_id,
            "language": language,
            "name": name,
            "isDraft": False,
        }
    }
    return upload_related(
        "captions",
        token=token,
        metadata=metadata,
        media=caption_path,
        media_type="application/octet-stream",
        params={"part": "snippet", "uploadType": "multipart"},
    )


def set_thumbnail(token: str, *, video_id: str, thumbnail_path: Path) -> dict[str, Any]:
    mime = mimetypes.guess_type(thumbnail_path.name)[0] or "image/png"
    return upload_binary(
        "thumbnails/set",
        token=token,
        media=thumbnail_path,
        media_type=mime,
        params={"videoId": video_id},
    )


def upload_binary(
    path: str,
    *,
    token: str,
    media: Path,
    media_type: str,
    params: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    raw = _request(
        _query_url(UPLOAD_BASE, path, params),
        method="POST",
        token=token,
        body=media.read_bytes(),
        content_type=media_type,
        timeout=300,
    )
    try:
        data = json.loads(raw.decode("utf-8"))
    except json.JSONDecodeError as exc:
        raise YouTubeAPIError(0, "invalid_json_response") from exc
    if not isinstance(data, dict):
        raise YouTubeAPIError(0, "unexpected_json_shape")
    return data


def get_channel_id(token: str) -> str:
    data = api_json("GET", "channels", token=token, params={"part": "id", "mine": "true"})
    items = data.get("items") or []
    if not items or not items[0].get("id"):
        raise YouTubeAPIError(0, "channel_id_unavailable")
    return str(items[0]["id"])


def insert_top_level_comment(token: str, *, video_id: str, channel_id: str, text: str) -> dict[str, Any]:
    body = {
        "snippet": {
            "channelId": channel_id,
            "videoId": video_id,
            "topLevelComment": {"snippet": {"textOriginal": text}},
        }
    }
    return api_json(
        "POST",
        "commentThreads",
        token=token,
        params={"part": "snippet"},
        body=body,
    )


def analytics_report(
    token: str,
    *,
    start_date: str,
    end_date: str,
    metrics: list[str],
    video_id: str | None = None,
) -> dict[str, Any]:
    params: dict[str, Any] = {
        "ids": "channel==MINE",
        "startDate": start_date,
        "endDate": end_date,
        "metrics": ",".join(metrics),
    }
    if video_id:
        params["filters"] = f"video=={video_id}"
    return api_json("GET", "reports", token=token, params=params, base=ANALYTICS_BASE)


def list_comment_threads(
    token: str,
    *,
    video_id: str,
    max_results: int = 100,
) -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []
    page_token: str | None = None
    while True:
        params: dict[str, Any] = {
            "part": "snippet,replies",
            "videoId": video_id,
            "maxResults": min(max_results, 100),
            "order": "time",
            "pageToken": page_token,
        }
        data = api_json("GET", "commentThreads", token=token, params=params)
        items = data.get("items") or []
        out.extend(items)
        page_token = data.get("nextPageToken")
        if not page_token or len(out) >= max_results:
            return out[:max_results]


def compact_api_error(exc: Exception) -> dict[str, Any]:
    if isinstance(exc, YouTubeAPIError):
        return {
            "status": exc.status,
            "reason": exc.reason,
            "detail": exc.detail,
        }
    return {"status": 0, "reason": "unexpected_error", "detail": str(exc)[:500]}
