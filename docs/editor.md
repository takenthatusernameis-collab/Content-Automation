# Editor conventions

Face-free explainer. Naming and export only. No ffmpeg profile yet.
Timing lock: `docs/format.md`.

## Project name
`NNN-slug` matching the packet folder.

## Tracks (top to bottom)
1. `VO` — narration only
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
Follow `docs/format.md`.
- Cut on sentence ends from `script.md` WORDS
- Hold a card at least 1.5s
- Hook 8–12s spoken; end-screen reserve last 20s of the export
- No jump-cut montage as the default edit

## Export
- File: `exports/NNN-slug-vN.mp4`
- Target: 1920x1080, 30fps, stereo 48kHz
- YouTube end screen: last 20s reserved, keep CTA card readable

## Out of scope
Do not add an ffmpeg recipe until VO + card assets exist for one packet.
