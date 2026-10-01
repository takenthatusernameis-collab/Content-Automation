# HANDOFF

Updated: 2026-10-01T11:20:00Z (Run 244)

This file is not Selected VO. Audio stays gitignored. Do not `git add -f`.

## Why this file exists
Run 242 synthesized a labeled generated take and called it operator-downloadable. Run 243 found an empty workspace. Run 244 found the same empty workspace and no Drive file under the Run 243 checksum. A wav that lives only in a disposable sandbox path does not survive. A Google Drive file id does survive a new agent workspace.

## Current operator file
- Name: `002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`
- Durable copy: Google Drive file id `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl`
- Folder: `Content-Automation-handoff` (`1ftaVyh8BWQeWp45TIyX7Hh1o0MPmGRev`)
- Link: https://drive.google.com/file/d/1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl/view
- Session artifacts path this run: `handoff/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav` (not the durable copy)
- Bytes: 27200958
- Duration: 308.40 s
- Format: 44.1 kHz, mono, s16 wav
- Voice: edge-tts `en-US-AndrewNeural` (espeak-ng still cannot be installed in this sandbox)
- SHA256: `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2`
- Drive listing size_bytes: 27200958 (same file). Level constants measured on the local decode: peak=0.7713, rms=0.1012, silence_frac=0.5089, clip_frac=0.0000. Those four would PASS if the same file were at the DROP path. Cards and export would still FAIL.
- kind: generated. Not a human recording. Not gate-machine Selected VO.

## Fetch without regenerating
If the artifacts file is missing, download Drive file id `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl` and check sha256. Do not synthesize again while that Drive file lists 27200958 bytes. Regeneration is allowed only if both the Drive file and this checksum are gone.

## Copy (gate machine only)
```bash
PACKET=videos/002-stop-deciding-what-to-work-on-every-morning
DROP="$PACKET/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav"
mkdir -p "$PACKET/vo"
cp -n /path/to/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav "$DROP"
sha256sum "$DROP"
# expect 758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2
python3 tools/narration_adapter.py "$PACKET"
```
Keep `vo_origin.md` kind=generated. Do not commit the wav.
