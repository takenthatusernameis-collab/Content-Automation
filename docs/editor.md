# Editor conventions

Face-free explainer. Naming and export only. No ffmpeg profile yet.
Timing lock: `docs/format.md`.
Cut list: `tools/timeline.py` (WORDS clock, not a recipe).
Media gate: `tools/media_qa.py` (fail-closed; no ffmpeg).

## Project name
`NNN-slug` matching the packet folder.

## Selected VO
DROP from repo root: `videos/NNN-slug/vo/NNN-slug-take-selected.wav` (or `.flac`).
Repo-root `vo/` is not Selected VO. Put that packet file on the `VO` track.
Do not invent a wav in git. Do not `git add -f` the take.

## Tracks (top to bottom)
1. `VO` — narration only (packet-relative selected take above)
2. `MUSIC` — bed, ducked under VO
3. `SFX` — optional, sparse
4. `TITLES` — hook card, beat labels, CTA card
5. `DIAGRAM` — simple boards / checklists
6. `BROLL` — optional texture; never required

## Cards
- Hook card: same promise as script hook, not a new slogan
- Beat cards: short label from the beat title, max 5 words
- CTA card: the assignment, not “subscribe”
- Planned names come from `assets.md` / `docs/assets.md` (`cards/{beat}-{slug}.png`)

## Timing
Follow `docs/format.md` and the packet `timeline.md` when present.
- Cut on sentence ends from `script.md` WORDS
- Hold a card at least 1.5s
- Hook 8–12s spoken; end-screen reserve last 20s of the export
- No jump-cut montage as the default edit

```bash
python3 tools/timeline.py PATH --dry-run
python3 tools/timeline.py PATH --write
python3 tools/media_qa.py PATH
python3 tools/music_cue_suggest.py PATH
python3 tools/broll_cue_suggest.py PATH
```

`--write` refreshes `timeline.md`. It does not render a master.
`media_qa.py` prints FAIL until the packet-relative take and 1920x1080 cards exist.
`music_cue_suggest.py` emits sparse operational suggestions for the MUSIC and SFX tracks (no audio generated).
`broll_cue_suggest.py` emits sparse operational suggestions for the optional BROLL track (no footage generated; prefer empty).

## Export
- File: `exports/NNN-slug-vN.mp4`
- Target: 1920x1080, 30fps, stereo 48kHz
- YouTube end screen: last 20s reserved, keep CTA card readable

## After cards exist locally

Operator copy lives in `docs/human_session.md` step 6. Q1 names are the Suggested file column in that packet `assets.md`.

```bash
python3 tools/card_generator.py PATH --write-manifest
python3 tools/timeline.py PATH --write
python3 tools/media_qa.py PATH
python3 tools/render_brief.py PATH --force
python3 tools/qa_checklist.py PATH --force
python3 tools/music_cue_suggest.py PATH
python3 tools/broll_cue_suggest.py PATH
```

Do not commit pngs. Do not invent files to flip presence rows. Do not add an ffmpeg recipe until `timeline.py` prints ready_to_assemble=yes and `media_qa.py` prints gate PASS.

## Out of scope
Do not add an ffmpeg recipe until VO + card assets exist for one packet and the timeline gate is yes.
