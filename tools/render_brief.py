#!/usr/bin/env python3
"""Write render.md presence checklist for named format outputs.

Exists vs missing only. Not an ffmpeg recipe, not a concat list,
not proof a packet is ready to upload.
"""

from __future__ import annotations

import argparse
import datetime as dt
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from validate_packet import field  # noqa: E402

PLACEHOLDER_MARKERS = (
    "status: placeholder",
    "(no files checked yet)",
)


def packet_id_slug(packet: Path) -> tuple[str, str]:
    text = (packet / "packet.md").read_text(encoding="utf-8") if (packet / "packet.md").is_file() else ""
    vid = field(text, "id")
    slug = field(text, "slug")
    if not vid or not slug:
        m = re.match(r"^(\d+)-(.+)$", packet.name)
        if m:
            vid = vid or m.group(1)
            slug = slug or m.group(2)
    return vid or "000", slug or "untitled"


def selected_vo_drop(packet: Path) -> str:
    """Canonical Selected VO path from repo root. Repo-root vo/ is not Selected VO."""
    vid, slug = packet_id_slug(packet)
    return f"videos/{vid}-{slug}/vo/{vid}-{slug}-take-selected.wav"


def planned_cards(packet: Path) -> list[str]:
    text = (packet / "assets.md").read_text(encoding="utf-8") if (packet / "assets.md").is_file() else ""
    found: list[str] = []
    seen: set[str] = set()
    for m in re.finditer(r"`(cards/[^`]+)`", text):
        name = m.group(1).strip()
        if name and name not in seen:
            seen.add(name)
            found.append(name)
    return found


def exists_any(packet: Path, relatives: list[str]) -> tuple[bool, str]:
    for rel in relatives:
        p = packet / rel
        if p.is_file() or p.is_dir():
            return True, rel
    return False, relatives[0] if relatives else ""


def export_hits(packet: Path, vid: str, slug: str) -> list[str]:
    folder = packet / "exports"
    if not folder.is_dir():
        return []
    pat = re.compile(rf"^{re.escape(vid)}-{re.escape(slug)}-v\d+\.mp4$", re.I)
    names = []
    for p in sorted(folder.iterdir()):
        if p.is_file() and pat.match(p.name):
            names.append(f"exports/{p.name}")
    return names


def presence_rows(packet: Path) -> list[dict[str, str]]:
    vid, slug = packet_id_slug(packet)
    vo_candidates = [
        f"vo/{vid}-{slug}-take-selected.wav",
        f"vo/{vid}-{slug}-take-selected.flac",
        f"vo/{vid}-{slug}-take-selected-v2.wav",
        f"vo/{vid}-{slug}-take-selected-v2.flac",
    ]
    vo_ok, vo_rel = exists_any(packet, vo_candidates)
    exports = export_hits(packet, vid, slug)
    export_expected = f"exports/{vid}-{slug}-vN.mp4"
    cap_ok = (packet / "captions.srt").is_file()
    edit_ok = (packet / "edit" / f"{vid}-{slug}").exists() or (packet / f"edit/{vid}-{slug}").exists()

    rows = [
        {
            "role": "Selected VO",
            "path": vo_rel if vo_ok else vo_candidates[0],
            "state": "present" if vo_ok else "missing",
        },
        {
            "role": "Timed captions",
            "path": "captions.srt",
            "state": "present" if cap_ok else "missing",
        },
        {
            "role": "Editor project",
            "path": f"edit/{vid}-{slug}",
            "state": "present" if edit_ok else "missing",
        },
        {
            "role": "Master export",
            "path": exports[0] if exports else export_expected,
            "state": "present" if exports else "missing",
        },
    ]
    for card in planned_cards(packet):
        ok = (packet / card).is_file()
        rows.append(
            {
                "role": "Card",
                "path": card,
                "state": "present" if ok else "missing",
            }
        )
    return rows


def render_is_filled(text: str) -> bool:
    if not text.strip():
        return False
    low = text.lower()
    if any(p in low for p in PLACEHOLDER_MARKERS):
        return False
    return bool(
        re.search(r"^status:\s*(all-missing|partial|all-present)\s*$", text, re.M | re.I)
    )


def render(packet: Path) -> str:
    rows = presence_rows(packet)
    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    present = sum(1 for r in rows if r["state"] == "present")
    missing = sum(1 for r in rows if r["state"] == "missing")
    status = "stub"
    if present == 0:
        status = "all-missing"
    elif missing == 0:
        status = "all-present"
    else:
        status = "partial"

    table = [
        "| Role | Named path | On disk |",
        "|------|------------|---------|",
    ]
    for r in rows:
        table.append(f"| {r['role']} | `{r['path']}` | {r['state']} |")

    vid, slug = packet_id_slug(packet)
    drop = selected_vo_drop(packet)
    return f"""# Render presence

Status: {status}
Generated: {generated}
Present: {present}
Missing: {missing}
Packet: `{packet.name}` (`{vid}` / `{slug}`)

This file is a presence checklist for names in `docs/format.md`.
It is not an ffmpeg recipe, not a concat list, and not an upload.
A `present` row means a file or folder exists in this packet.
A `missing` row means wait for a human VO / card / export. Do not invent it.

DROP `{drop}`
Repo-root `vo/` is not Selected VO. Table paths below are packet-relative.

## Named outputs
{chr(10).join(table)}

## Rules
- Names: `docs/format.md`
- Cards listed here come from `assets.md` backticks (`cards/...png`)
- Export match: `exports/{{id}}-{{slug}}-vN.mp4` if that folder exists
- Selected VO match: packet-relative `vo/{{id}}-{{slug}}-take-selected(.wav|.flac)` plus optional `-v2`
- Selected VO drop from repo root: `{drop}`
- `tools/render_brief.py` never writes media, never runs ffmpeg, never uploads

## Human
- [ ] Do not treat all-missing as a failed render
- [ ] Do not commit fake wav/png/mp4 to flip rows to present
- [ ] After a real selected take exists, re-run this tool with `--force`
"""


def write_empty_render(dest: Path) -> str:
    path = dest / "render.md"
    existing = path.read_text(encoding="utf-8") if path.is_file() else ""
    if render_is_filled(existing):
        return f"kept {dest.name}/render.md (already filled)"
    path.write_text(render(dest), encoding="utf-8")
    return f"wrote {dest.name}/render.md"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write render.md exists-vs-missing checklist. No ffmpeg."
    )
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument("--dry-run", action="store_true", help="Print render.md; do not write")
    parser.add_argument("--force", action="store_true", help="Overwrite a filled render.md")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1

    dest = path / "render.md"
    existing = dest.read_text(encoding="utf-8") if dest.is_file() else ""
    filled = render_is_filled(existing)
    if filled and not args.force and not args.dry_run:
        print(f"render.md already filled; pass --force to overwrite: {dest}", file=sys.stderr)
        return 1

    text = render(path)
    if args.dry_run:
        sys.stdout.write(text)
        return 0

    dest.write_text(text, encoding="utf-8")
    print(dest)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
