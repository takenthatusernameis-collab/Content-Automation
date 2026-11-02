#!/usr/bin/env python3
"""Single-command local production readiness aggregator.

Imports and runs media_qa.inspect_media + assemble.inspect_assemble.
Optionally notes captions.srt presence (does not run caption_align or rewrite).
Prints a compact summary. Never invents media, never runs ffmpeg, never bumps status,
never polls secrets, never dispatches. Exit 0 only when media_qa PASS and assemble
gate is READY_TO_ENCODE or EXPORT_EXISTS.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

TOOLS = Path(__file__).resolve().parent
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from media_qa import inspect_media  # noqa: E402
from assemble import inspect_assemble  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Aggregate local media/QA/assembly readiness. No ffmpeg execute, no secrets."
    )
    parser.add_argument("packet", help="Path to packet folder")
    args = parser.parse_args()
    path = Path(args.packet).resolve()
    if not path.is_dir():
        print(f"not a directory: {path}", file=sys.stderr)
        return 1

    media = inspect_media(path)
    assemble_rep = inspect_assemble(path)
    captions = (path / "captions.srt").is_file()

    print(f"packet: {path.name}")
    print(f"media_qa: {media['gate']}")
    print(f"assemble_gate: {assemble_rep['gate']}")
    print(f"ready_to_assemble: {'yes' if media.get('ready_to_assemble') else 'no'}")
    print(f"export_present: {'yes' if media.get('export_present') else 'no'}")
    print(f"captions_srt: {'present' if captions else 'missing'}")
    print(f"ffmpeg_on_path: {'yes' if assemble_rep.get('ffmpeg') else 'no'}")

    hard_ok = media["gate"] == "PASS" and assemble_rep["gate"] in {"READY_TO_ENCODE", "EXPORT_EXISTS"}
    print(f"local_ready_for_human_dispatch: {'yes' if hard_ok else 'no'}")
    print("Does not execute encode, does not invent media, does not poll OAuth.")
    return 0 if hard_ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
