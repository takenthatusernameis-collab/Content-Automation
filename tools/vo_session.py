#!/usr/bin/env python3
"""Write vo_session.md reading card from script.md spoken WORDS.

A session card is not a wav, not TTS, and not proof a take exists.
"""

from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from caption_brief import WPM, fmt_ts, script_cues  # noqa: E402
from render_brief import packet_id_slug, presence_rows, selected_vo_drop  # noqa: E402

PLACEHOLDER_MARKERS = (
    "status: placeholder",
    "(add spoken lines after script words exist)",
)


def session_is_filled(text: str) -> bool:
    if not text.strip():
        return False
    low = text.lower()
    if any(p in low for p in PLACEHOLDER_MARKERS):
        return False
    return "status: ready-to-record" in low or "status: recorded" in low


def vo_state(packet: Path) -> tuple[str, str]:
    for row in presence_rows(packet):
        if row["role"] == "Selected VO":
            return row["state"], row["path"]
    vid, slug = packet_id_slug(packet)
    return "missing", f"vo/{vid}-{slug}-take-selected.wav"


def render(packet: Path) -> str:
    script_path = packet / "script.md"
    script = script_path.read_text(encoding="utf-8") if script_path.is_file() else ""
    cues = script_cues(script)
    spoken = [c for c in cues if int(c["words"]) > 0]
    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    total_words = sum(int(c["words"]) for c in cues)
    total_s = sum(float(c["dur"]) for c in cues)
    state, _vo_rel = vo_state(packet)
    drop = selected_vo_drop(packet)
    status = "recorded" if state == "present" else ("ready-to-record" if spoken else "placeholder")

    if not spoken:
        read_body = (
            "(add spoken lines after script WORDS exist)\n"
            "- Hook / beats / CTA will appear here from script.md WORDS.\n"
            "- Estimated times use 150 wpm. They are not a take."
        )
    else:
        rows = []
        for c in spoken:
            start = fmt_ts(float(c["start"]))
            end = fmt_ts(float(c["start"]) + float(c["dur"]))
            rows.append(f"### {c['label']}  ({start}–{end}, {c['words']}w)\n\n{c['text']}\n")
        read_body = "\n".join(rows).rstrip()

    return f"""# VO session

Status: {status}
Generated: {generated}
WPM assumption: {int(WPM)}
Spoken words: {total_words}
Estimated speech: {fmt_ts(total_s)} (not a take duration)
DROP `{drop}`
Selected take on disk: {state}
Repo-root `vo/` is not Selected VO. Packet-relative name is `vo/` plus the take filename.

This file is a reading card from script.md WORDS. It is not a wav, not TTS,
and not proof a take was recorded. Copy the selected file to the named path
after a human records. Do not invent audio.

## Record to
- Selected: `{drop}`
- Repo-root `vo/` is ignored. Tools only check inside this packet.
- Rejected takes (optional): `videos/{packet.name}/vo/takes/`
- Rules: `docs/narration.md`

## Read-aloud
{read_body}

## Human
- [ ] Confirm hook is 20–35 spoken words before recording
- [ ] Record one selected take to DROP (wav or flac)
- [ ] Do not commit raw session dumps by default
- [ ] Do not run a TTS vendor from this tool
- [ ] After the file exists, re-run `tools/vo_session.py PATH --force` then dry-run `tools/set_status.py PATH --to ready_for_edit`
"""


def write_empty_session(dest: Path) -> str:
    path = dest / "vo_session.md"
    existing = path.read_text(encoding="utf-8") if path.is_file() else ""
    if session_is_filled(existing):
        return f"kept {dest.name}/vo_session.md (already filled)"
    path.write_text(render(dest), encoding="utf-8")
    return f"wrote {dest.name}/vo_session.md"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write vo_session.md reading card from script WORDS. No TTS. No wav."
    )
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument("--dry-run", action="store_true", help="Print vo_session.md; do not write")
    parser.add_argument("--force", action="store_true", help="Overwrite a filled vo_session.md")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1

    dest = path / "vo_session.md"
    existing = dest.read_text(encoding="utf-8") if dest.is_file() else ""
    filled = session_is_filled(existing)
    if filled and not args.force and not args.dry_run:
        print(f"vo_session.md already filled; pass --force to overwrite: {dest}", file=sys.stderr)
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
