#!/usr/bin/env python3
"""Title / publish Title-to-upload consistency check.

Read-only. Extracts the Primary from titles.md and the Title to upload
from publish.md. Reports whether they match after light normalization
(case, punctuation, extra spaces) so future packets can surface title
drift before upload.
Does not invent text, rewrite files, poll secrets, or extend production_readiness.
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path


def extract_primary(titles_text: str) -> str:
    m = re.search(r"^Primary:\s*(.+)$", titles_text, re.M)
    return m.group(1).strip() if m else ""


def extract_title_to_upload(publish_text: str) -> str:
    m = re.search(
        r"^##[ \t]*Title to upload[^\n]*\n\s*(.+?)(?=\n##|\n\n|\Z)",
        publish_text,
        re.M | re.S | re.I,
    )
    if not m:
        return ""
    # Take first non-empty line
    for line in m.group(1).splitlines():
        line = line.strip()
        if line:
            return line
    return ""


def normalize(text: str) -> str:
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def inspect(packet: Path) -> dict:
    titles_path = packet / "titles.md"
    pub_path = packet / "publish.md"
    if not titles_path.is_file() or not pub_path.is_file():
        return {
            "ok": False,
            "code": "NO_DATA",
            "detail": "missing titles.md or publish.md",
            "primary": "",
            "upload": "",
            "match": False,
        }
    primary = extract_primary(titles_path.read_text(encoding="utf-8"))
    upload = extract_title_to_upload(pub_path.read_text(encoding="utf-8"))
    if not primary or not upload:
        return {
            "ok": False,
            "code": "NO_DATA",
            "detail": "could not extract Primary or Title to upload",
            "primary": primary,
            "upload": upload,
            "match": False,
        }
    n_primary = normalize(primary)
    n_upload = normalize(upload)
    match = n_primary == n_upload
    return {
        "ok": match,
        "code": "OK" if match else "WARN",
        "detail": "titles match after normalization" if match else "Primary and Title to upload differ after normalization",
        "primary": primary,
        "upload": upload,
        "normalized_primary": n_primary,
        "normalized_upload": n_upload,
        "match": match,
    }


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Check titles.md Primary vs publish.md Title to upload. No writes."
    )
    parser.add_argument("packet", help="Path to packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1
    rep = inspect(path)
    print(f"packet: {path.name}")
    print(f"primary: {rep.get('primary')}")
    print(f"title_to_upload: {rep.get('upload')}")
    print(f"match: {rep.get('match')}")
    print(f"consistency: {rep['code']} ({rep['detail']})")
    print("Does not invent text, rewrite files, or poll OAuth.")
    return 0 if rep["code"] != "NO_DATA" else 2


if __name__ == "__main__":
    raise SystemExit(main())
