# Narration conventions

Text-first. No TTS vendor and no microphone brand in this file.

## Where files live
Packet folder: `videos/NNN-slug/`

| Role | Path | Notes |
|------|------|-------|
| Script (source of spoken words) | `script.md` | WORDS blocks only |
| VO session card | `vo_session.md` | Reading order + named take path; not a wav |
| Caption intake | `captions.md` | Generated from WORDS; estimated times |
| Timed captions later | `captions.srt` | Human or tool after a real take; do not invent |
| Selected voice take | `vo/NNN-slug-take-selected.wav` | One selected file; wav or flac |
| Rejected takes | `vo/takes/` | Optional; do not point the editor at these |

Keep VO media out of git unless a human explicitly adds a small fixture.
Do not commit large raw session dumps.

## Naming
- Selected take matches the packet id + slug.
- Version a replacement: `vo/NNN-slug-take-selected-v2.wav`
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

## Out of scope
- No TTS CLI, API key, or voice id here.
- No ffmpeg VO cleanup recipe until one selected take exists on disk.
- Status `ready_for_vo` means script WORDS exist; it does not mean a wav exists.
