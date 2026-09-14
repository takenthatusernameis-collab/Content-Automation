# Render presence

Status: all-missing
Generated: 2026-09-14T01:10:00Z
Present: 0
Missing: 11
Packet: `002-stop-deciding-what-to-work-on-every-morning` (`002` / `stop-deciding-what-to-work-on-every-morning`)

This file is a presence checklist for names in `docs/format.md`.
It is not an ffmpeg recipe, not a concat list, and not an upload.
A `present` row means a file or folder exists in this packet.
A `missing` row means wait for a human VO / card / export. Do not invent it.

DROP `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`
Repo-root `vo/` is not Selected VO. Table paths below are packet-relative.

## Named outputs
| Role | Named path | On disk |
|------|------------|---------|
| Selected VO | `vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav` | missing |
| Timed captions | `captions.srt` | missing |
| Editor project | `edit/002-stop-deciding-what-to-work-on-every-morning` | missing |
| Master export | `exports/002-stop-deciding-what-to-work-on-every-morning-vN.mp4` | missing |
| Card | `cards/hook-card-on-a-closed-laptop-one-handwritte.png` | missing |
| Card | `cards/payoff-same-card-stop-rule-under-the-sentenc.png` | missing |
| Card | `cards/beat1-split-open-task-board-vs-one-index-car.png` | missing |
| Card | `cards/beat2-hand-writing-verb-object-place-on-a-ca.png` | missing |
| Card | `cards/beat3-four-crossed-out-themes-replaced-by-on.png` | missing |
| Card | `cards/beat4-night-card-morning-start-shutdown-rewr.png` | missing |
| Card | `cards/cta-cta-card-write-tomorrow-s-next-action-on.png` | missing |

## Rules
- Names: `docs/format.md`
- Cards listed here come from `assets.md` backticks (`cards/...png`)
- Export match: `exports/{id}-{slug}-vN.mp4` if that folder exists
- Selected VO match: packet-relative `vo/{id}-{slug}-take-selected(.wav|.flac)` plus optional `-v2`
- Selected VO drop from repo root: `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`
- `tools/render_brief.py` never writes media, never runs ffmpeg, never uploads

## Human
- [ ] Do not treat all-missing as a failed render
- [ ] Do not commit fake wav/png/mp4 to flip rows to present
- [ ] After a real selected take exists, re-run this tool with `--force`
