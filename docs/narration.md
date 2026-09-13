# Narration conventions

Text-first. No TTS vendor and no microphone brand in this file.

## Where files live
Packet folder: `videos/NNN-slug/`

Every path in the table is **inside that packet folder**. A file at repo-root `vo/` is not Selected VO. `render_brief` and `set_status` only check `videos/NNN-slug/vo/`.

`.gitignore` excludes packet `vo/` audio and `cards/` images. Local presence still works. Do not force-add media.

| Role | Path | Notes |
|------|------|-------|
| Script (source of spoken words) | `script.md` | WORDS blocks only |
| VO session card | `vo_session.md` | Reading order + named take path; not a wav |
| Caption intake | `captions.md` | Generated from WORDS; estimated times |
| Timed captions later | `captions.srt` | Human or tool after a real take; do not invent |
| Selected voice take | `vo/NNN-slug-take-selected.wav` | Packet-relative; wav or flac |
| Rejected takes | `vo/takes/` | Optional; do not point the editor at these |

Keep VO media out of git unless a human explicitly adds a small fixture.
Do not commit large raw session dumps.

## Naming
- Selected take matches the packet id + slug and lives under the packet `vo/` folder.
- Version a replacement: `vo/NNN-slug-take-selected-v2.wav` (still packet-relative).
- Editor track name stays `VO` (`docs/editor.md`).

## Timing
- Cut the edit on sentence ends from `script.md` WORDS.
- Caption stub times and `vo_session.md` estimates assume 150 words/minute and ignore pauses.
- A selected take is the clock. The stub is not.

## Session card
- `python3 tools/vo_session.py PATH` writes the reading card.
- Status `placeholder` means WORDS are empty.
- Status `ready-to-record` means WORDS exist and the named take is missing.
- Status `recorded` means the named take is on disk. It is not an upload.
- Scaffold writes `vo_session.md` only when the file is still empty.

## After the named take is on disk

```bash
python3 tools/vo_session.py PATH --force
python3 tools/set_status.py PATH --to ready_for_edit
# --write only after dry-run OK and Selected VO present
```

Q1 named path: `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`.
Operator copy lives in `docs/human_session.md` step 5. Do not invent the file to make `--write` look legal. Do not drop the take at repo-root `vo/`.

## Out of scope
- No TTS CLI, API key, or voice id here.
- No ffmpeg VO cleanup recipe until one selected take exists on disk.
- Status `ready_for_vo` means script WORDS exist; it does not mean a wav exists.
