# Format: face-free explainer

Locked format for packets with `format: explainer-6-10min`.
Timing and named outputs only. No ffmpeg command line.

Default target: 8 minutes. Allowed range: 6–10 minutes spoken plus holds.
Clock source: selected VO take when it exists; otherwise script WORDS at the calibrated rate from tools/phrase_utils.select_rate (190 wpm when vo_origin marks generated, 140 wpm otherwise; ~150 wpm was the earlier approximate default).

Spoken-word band at 150 wpm: **900–1500 words**. Target ~1200.
`tools/validate_packet.py` prints WARN when WORDS sit outside that band.
`--duration` turns the same check into FAIL. The sample fixture is allowed to stay short.
`tools/expand_brief.py` writes a per-beat budget into `expand.md`. It does not rewrite WORDS.

## Timeline

| Segment | Spoken target | On-screen | Rule |
|---------|---------------|-----------|------|
| Hook | 8–12 s (~20–35 words) | Hook card | Same promise as script hook. Card on from first word. |
| Payoff | Before beat 2 | Payoff card if VISUAL has one | Viewer can state the outcome before the middle. |
| Beats | Rest of body, 4–7 beats | One primary card per beat | Hold each card ≥ 1.5 s. Cut on sentence ends. |
| CTA | Last spoken beat | CTA card | Assignment text, not “subscribe”. |
| End-screen reserve | Last 20 s of the export | CTA card stays readable | Leave lower-right and lower-left clear for YouTube elements. |

Do not add a face track. Do not default to jump-cut montage.
B-roll is optional texture under cards, never the format.

## Holds

- Card minimum: 1.5 s even if the sentence is shorter.
- If a beat has two VISUAL lines, stack them; do not flash.
- CTA card stays through the end-screen reserve.
- Silence / breath after a sentence is allowed; do not fill with a new slogan.

## Named outputs (not a recipe)

Paths live inside the packet folder `videos/NNN-slug/`.
DROP from repo root: `videos/NNN-slug/vo/NNN-slug-take-selected.wav` (or `.flac`).
Repo-root `vo/` is not Selected VO. Table paths below are packet-relative.

| Role | Path |
|------|------|
| Selected VO | `vo/NNN-slug-take-selected.wav` |
| Planned cards | `cards/{beat}-{slug}.png` (see `docs/assets.md`) |
| Timed captions (later) | `captions.srt` |
| Editor project | `edit/NNN-slug` (NLE-native; not committed by default) |
| Master export | `exports/NNN-slug-vN.mp4` |
| Upload candidate | same file after human QA; do not invent a second name |

Export target (from `docs/editor.md`): 1920×1080, 30 fps, stereo 48 kHz.
A path in this table is a name. It is not proof the file exists.
Presence on disk is listed in packet `render.md` (`tools/render_brief.py`). That file is also not a recipe.

## Out of scope

- No ffmpeg filtergraph, CRF, or concat list.
- No YouTube upload.
- No second format (shorts) until a human changes DECISIONS.md.
- No automatic rewrite of script WORDS from `expand.md`.
