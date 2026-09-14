#!/usr/bin/env python3
"""Write captions.md cue list from script.md spoken WORDS.

Estimates start times from word count at 150 wpm. Not Whisper, not SRT
export, not a timed transcript of a VO file.
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

from render_brief import selected_vo_drop  # noqa: E402

WPM = 150.0
PLACEHOLDER_MARKERS = (
    "(add ",
    "todo",
    "tbd",
    "placeholder",
    "after script words exist",
    "write spoken lines",
)


def section(text: str, heading: str) -> str:
    parts = re.split(rf"^##\s+{re.escape(heading)}\s*$", text, maxsplit=1, flags=re.M)
    if len(parts) < 2:
        return ""
    rest = re.split(r"^##\s+", parts[1], maxsplit=1, flags=re.M)[0]
    return rest.strip()


def spoken_words(block: str) -> list[str]:
    m = re.search(r"WORDS:\s*(.*?)(?:VISUAL:|\Z)", block, re.S)
    blob = m.group(1) if m else block
    blob = re.sub(r"\*[^*]+\*", " ", blob)
    return re.findall(r"[A-Za-z0-9']+", blob)


def spoken_text(block: str) -> str:
    m = re.search(r"WORDS:\s*(.*?)(?:VISUAL:|\Z)", block, re.S)
    blob = m.group(1) if m else ""
    blob = re.sub(r"\*[^*]+\*", " ", blob)
    return " ".join(blob.split())


def fmt_ts(seconds: float) -> str:
    if seconds < 0:
        seconds = 0
    whole = int(round(seconds))
    m, s = divmod(whole, 60)
    return f"{m:02d}:{s:02d}"


def script_cues(script: str) -> list[dict[str, str | int | float]]:
    headings = re.findall(r"^##\s+(.+)$", script, re.M)
    cues: list[dict[str, str | int | float]] = []
    t = 0.0
    for heading in headings:
        block = section(script, heading)
        text = spoken_text(block)
        words = spoken_words(block)
        n = len(words)
        dur = (n / WPM) * 60.0 if n else 0.0
        cues.append(
            {
                "label": heading.strip(),
                "text": text,
                "words": n,
                "start": t,
                "dur": dur,
            }
        )
        t += dur
    return cues


def captions_is_filled(text: str) -> bool:
    if not text.strip():
        return False
    low = text.lower()
    if any(p in low for p in PLACEHOLDER_MARKERS) and "WORDS empty" not in text:
        if "cue count: 0" in low or "## Cues\n(add" in text or "(add spoken" in low:
            return False
    block_parts = re.split(r"^##\s+Cues\s*$", text, maxsplit=1, flags=re.M)
    if len(block_parts) < 2:
        return False
    rest = re.split(r"^##\s+", block_parts[1], maxsplit=1, flags=re.M)[0]
    lines = [
        ln
        for ln in rest.splitlines()
        if ln.startswith("- ") and " — " in ln and len(ln.split(" — ", 1)[-1].strip()) >= 12
    ]
    if not lines:
        return False
    joined = " ".join(lines).lower()
    if any(p in joined for p in PLACEHOLDER_MARKERS):
        return False
    return True


def render(packet: Path) -> str:
    script_path = packet / "script.md"
    script = script_path.read_text(encoding="utf-8") if script_path.is_file() else ""
    cues = script_cues(script)
    spoken = [c for c in cues if int(c["words"]) > 0]
    generated = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    total_words = sum(int(c["words"]) for c in cues)
    total_s = sum(float(c["dur"]) for c in cues)
    drop = selected_vo_drop(packet)

    if not spoken:
        cue_body = (
            "(add spoken lines after script WORDS exist)\n"
            "- Hook / beats / CTA will appear here from script.md WORDS.\n"
            "- Estimated times use 150 wpm. They are not a VO alignment."
        )
        status = "placeholder"
    else:
        rows = []
        for c in spoken:
            start = fmt_ts(float(c["start"]))
            end = fmt_ts(float(c["start"]) + float(c["dur"]))
            rows.append(
                f"- {start}–{end}  {c['label']}  ({c['words']}w) — {c['text']}"
            )
        cue_body = "\n".join(rows)
        status = "stub"

    return f"""# Captions

Status: {status}
Generated: {generated}
WPM assumption: {int(WPM)}
Cue count: {len(spoken)}
Spoken words: {total_words}
Estimated speech: {fmt_ts(total_s)} (not a video duration)

This file is a caption intake stub from script.md WORDS. It is not Whisper,
not an SRT file, and not proof that captions were burned or uploaded.
Do not treat estimated times as aligned to a take.

DROP `{drop}`
Repo-root `vo/` is not Selected VO. Cues below are script-derived, not take-aligned.

## Cues
{cue_body}

## Export names (when a human makes real captions)
- Working text: `videos/{packet.name}/captions.md` (this file)
- Timed file later: `videos/{packet.name}/captions.srt` (do not invent one here)
- Selected VO drop from repo root: `{drop}`
- VO path rules: `docs/narration.md`

## Human
- [ ] Read cues against the selected VO take at `{drop}`
- [ ] Fix wording that was spoken differently than script.md
- [ ] Split long lines for on-screen readability
- [ ] Do not upload estimated times as final captions
- [ ] Do not invent a wav or treat repo-root `vo/` as Selected VO
"""


def write_empty_captions(dest: Path) -> str:
    path = dest / "captions.md"
    existing = path.read_text(encoding="utf-8") if path.is_file() else ""
    if captions_is_filled(existing):
        return f"kept {dest.name}/captions.md (already filled)"
    path.write_text(render(dest), encoding="utf-8")
    return f"wrote {dest.name}/captions.md"


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Write captions.md cue list from script WORDS. No Whisper."
    )
    parser.add_argument("packet", help="Path to packet folder")
    parser.add_argument("--dry-run", action="store_true", help="Print captions.md; do not write")
    parser.add_argument("--force", action="store_true", help="Overwrite a filled captions.md")
    args = parser.parse_args()

    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1

    dest = path / "captions.md"
    existing = dest.read_text(encoding="utf-8") if dest.is_file() else ""
    filled = captions_is_filled(existing)
    if filled and not args.force and not args.dry_run:
        print(f"captions.md already filled; pass --force to overwrite: {dest}", file=sys.stderr)
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
