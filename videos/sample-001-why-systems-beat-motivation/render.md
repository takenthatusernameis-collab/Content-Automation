# Render presence

Status: all-missing
Generated: 2026-08-27T23:12:00Z
Present: 0
Missing: 9
Packet: `sample-001-why-systems-beat-motivation` (`001` / `why-systems-beat-motivation`)

This file is a presence checklist for names in `docs/format.md`.
It is not an ffmpeg recipe, not a concat list, and not an upload.
A `present` row means a file or folder exists in this packet.
A `missing` row means wait for a human VO / card / export. Do not invent it.

## Named outputs
| Role | Named path | On disk |
|------|------------|---------|
| Selected VO | `vo/001-why-systems-beat-motivation-take-selected.wav` | missing |
| Timed captions | `captions.srt` | missing |
| Editor project | `edit/001-why-systems-beat-motivation` | missing |
| Master export | `exports/001-why-systems-beat-motivation-vN.mp4` | missing |
| Card | `cards/hook-start-cue-problem.png` | missing |
| Card | `cards/beat1-calendar-vs-cloud-icon-contrast.png` | missing |
| Card | `cards/beat2-cue-to-two-minute-action-diagram.png` | missing |
| Card | `cards/beat3-night-note-on-desk.png` | missing |
| Card | `cards/beat4-simple-checkbox-row.png` | missing |

## Rules
- Names: `docs/format.md`
- Cards listed here come from `assets.md` backticks (`cards/...png`)
- Export match: `exports/{id}-{slug}-vN.mp4` if that folder exists
- Selected VO match: `vo/{id}-{slug}-take-selected(.wav|.flac)` plus optional `-v2`
- `tools/render_brief.py` never writes media, never runs ffmpeg, never uploads

## Human
- [ ] Do not treat all-missing as a failed render
- [ ] Do not commit fake wav/png/mp4 to flip rows to present
- [ ] After a real selected take exists, re-run this tool with `--force`
