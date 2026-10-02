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


def upload_video(
    token: str,
    *,
    export_path: Path,
    metadata: Mapping[str, Any],
    privacy: str,
) -> dict[str, Any]:
    body = dict(metadata)
    status = dict(body.get("status") or {})
    status["privacyStatus"] = privacy
    status.setdefault("selfDeclaredMadeForKids", False)
    body["status"] = status
    return upload_related(
        "videos",
        token=token,
        metadata=body,
        media=export_path,
        media_type="video/mp4",
        params={"part": "snippet,status", "uploadType": "multipart", "notifySubscribers": "false"},
    )


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
