# HANDOFF

Updated: 2026-10-01T10:25:00Z (Run 243)

This file is not Selected VO. Audio stays gitignored. Do not `git add -f`.

## Why this file exists
Run 242 synthesized a labeled generated take and called it operator-downloadable. The next run found an empty workspace and no `vo/` directory. A wav that lives only in a disposable sandbox path does not survive. That class is now flagged in FAILURES.md.

## Current operator file
- Name: `002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`
- Location this run: operator artifacts folder `handoff/` (session download). Not in git. Not at the packet DROP path.
- Bytes: 27200958
- Duration: 308.40 s
- Format: 44.1 kHz, mono, s16 wav
- Voice: edge-tts `en-US-AndrewNeural` (espeak-ng still cannot be installed in this sandbox)
- SHA256: `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2`
- Level constants from `tools/media_qa.py` measured locally (not via `media_qa.py`, no checkout): peak=0.7713, rms=0.1012, silence_frac=0.5086, clip_frac=0.0000. Those four would PASS if the same file were at the DROP path. Cards and export would still FAIL.
- kind: generated. Not a human recording.

## Copy (gate machine only)
```bash
PACKET=videos/002-stop-deciding-what-to-work-on-every-morning
DROP="$PACKET/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav"
mkdir -p "$PACKET/vo"
cp -n /path/to/handoff/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav "$DROP"
sha256sum "$DROP"
# expect 758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2
python3 tools/narration_adapter.py "$PACKET"
```
Keep `vo_origin.md` kind=generated. Do not commit the wav. Do not regenerate unless this file and the checksum above are both lost.
