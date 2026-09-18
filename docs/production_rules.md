# Production rules

Apply to every video packet. QA checks what can be checked mechanically.

## Packet
- One video = one folder `videos/NNN-slug/`
- Required files: `packet.md`, `idea.md`, `script.md`, `titles.md`, `thumbnail.md`, `qa.md`
- Optional: `research.md`, `assets.md`, `narration.md`, `publish.md`, `captions.md`, `render.md`, `vo_session.md`, `expand.md`
- Status in `packet.md` must be one of: `draft`, `ready_for_vo`, `ready_for_edit`, `ready_to_publish`, `published`, `abandoned`
- Field values stay on the same line as the key
- `python3 tools/new_idea.py "topic"` / `python3 tools/new_packet.py "title"` copy the template and write generated titles/thumbs (if empty), `publish.md` (if empty), `captions.md` (if empty), `assets.md` (if empty), `render.md` (if empty), `vo_session.md` (if empty), `expand.md` (if empty), `research.md`, and `qa.md` unless `--no-generate`
- Neither `new_packet.py` nor `idea_brief.py` writes idea.md. After a mark-needed folder exists, reprint then paste by hand:
  - `python3 tools/idea_brief.py PATH --block`
  - paste idea fields by hand into `PATH/idea.md`
  - `python3 tools/idea_brief.py PATH --check`
- `python3 tools/doctor.py` is the session-start health check. It does not write files.
- `python3 tools/pipeline_status.py` is the read-only board across packets. It does not write files.
- `python3 tools/next_action.py` is the read-only next human step. It does not write files. fill-idea Why names idea_brief --block / paste / --check.
- `python3 tools/hint.py` is the read-only copy-paste CLI for that step. It does not write files. `--write` is never the first command. After scaffold, fill-idea prints idea_brief; write-script/expand-script print words.py and PATH/draft.md apply lines.
- `python3 tools/set_status.py PATH --to STATUS` is the only status writer. Dry-run default. `--write` required. Refuses fixture promote, skip-ahead, and evidence-free bumps.
- After a GitHub write of a high-risk tool, run `python3 tools/prove_locks.py` first. PASS is not apply --write.

## Format
- Default packet format is `explainer-6-10min` (face-free).
- Timing, holds, end-screen reserve, and named export paths: `docs/format.md`.
- Spoken-word band at 150 wpm: 900-1500 words (target ~1200 / 8 min).
- Editor tracks: `docs/editor.md`. Do not treat named paths as existing files.
- `python3 tools/render_brief.py PATH` writes `render.md` exists-vs-missing for those names.
- A `missing` row is the expected state until a human puts a file on disk. Do not invent media.
- `--force` is required to replace a filled `render.md`.
- Scaffold writes render.md only when empty.

## Script
- Hook in the first 8-12 seconds of spoken words (about 20-35 words)
- State the viewer payoff before beat 2
- 4-7 beats after the hook
- One primary CTA
- Total spoken WORDS should match the locked format band (900-1500 for `explainer-6-10min`)
- Default validate prints WARN when the band is missed; `--duration` fails
- Do not record VO while the duration WARN is present on a real packet
- Do not pad `videos/sample-001-*` to clear the WARN
- Off-repo expand lands in `PATH/draft.md`. That file is not `script.md` until apply --write.
- `python3 tools/words.py PATH` is a read-only band printer. It prefers PATH/draft.md when present. Read Result, Delta, Hook Delta, Beats, Thin, Grow or Cut. `--strict` keys off the total band only. IN BAND is not apply --write.
- `python3 tools/expand_brief.py PATH` writes `expand.md` per-beat Have/Target/Add from current WORDS
- An expand.md budget is not a rewritten script. Do not autofill WORDS from it
- `--force` is required to replace a filled `expand.md`
- Scaffold writes expand.md only when empty
- `python3 tools/expand_prompt.py PATH` prints a paste-ready expander pack. It does not write `script.md`
- A printed prompt is not a draft. Do not write it onto sample-001
- `python3 tools/apply_script.py PATH --from FILE` dry-runs a pasted script body. Refuse sample-001 and expand_prompt stdout. Prefer `--from PATH/draft.md` after words.py is IN BAND.
- `--write` is required to replace script.md on a non-fixture packet. `--refresh` then rewrites expand.md, vo_session.md, and captions.md. No status bump.
- No unverifiable statistics; if a number is used, cite source in `research.md`
- Working-niche tone: specific, calm, operational. No hustle slogans.

## Research
- `python3 tools/research_brief.py PATH` writes the stub (topic seed, source slots, spoken-number scan).
- Listing a URL is not verification. Do not scrape pages into Facts.
- `--source "line"` adds a human-provided pointer. `--force` is required to replace a filled file.
- Digit scan looks only at WORDS blocks (not `0:00` / `Beat 1` headings).
- Scaffold already runs this stub writer; do not treat the generated file as verified research.

## Titles
- Provide at least 5 options
- One must be under 50 characters
- No ALL CAPS words except a single acronym
- Numbered options stay on the same line as `1.` — blank `1.` is not a title
- Scaffold fills titles/thumbs from `title_thumb_brief.py` only when `titles.md` parses empty

## Thumbnail
- One sentence of on-image text, max 5 words
- Describe subject, contrast, and what *not* to include
- Must match the chosen title promise

## Publish metadata
- `python3 tools/publish_brief.py PATH` writes `publish.md`: title to upload, description, tags, first comment.
- No YouTube API call. A filled file is not a published video.
- `--force` is required to replace a filled `publish.md`.
- Scaffold writes publish.md after titles (so Primary exists) only when the file is still a placeholder.

## Captions and narration
- `python3 tools/caption_brief.py PATH` writes `captions.md` cues from script WORDS at 150 wpm.
- Not Whisper. Not an SRT. Estimated times are not aligned to a take.
- `--force` is required to replace a filled `captions.md`.
- Scaffold writes captions.md only when empty.
- `python3 tools/vo_session.py PATH` writes `vo_session.md` reading card + named take path.
- Not TTS. Not a wav. Status `ready-to-record` is not a take.
- `--force` is required to replace a filled `vo_session.md`.
- Scaffold writes vo_session.md only when empty.
- VO file names live in `docs/narration.md`. Do not commit raw session dumps by default.

## Assets
- `python3 tools/asset_brief.py PATH` writes `assets.md` card rows from script VISUAL lines.
- Suggested filenames only. Not stock shopping. Not a download. Status stays `planned`.
- `--force` is required to replace a filled `assets.md`.
- Scaffold writes assets.md only when empty.
- Filename rules: `docs/assets.md`. Editor tracks: `docs/editor.md`.

## QA gates
- `python3 tools/validate_packet.py PATH` — publish/completeness. Empty WORDS fail. Duration misses print WARN.
- `python3 tools/validate_packet.py --draft PATH` — intake/structure. Empty WORDS/titles/thumb are incomplete, not fail.
- `python3 tools/validate_packet.py --duration PATH` — same as publish gate plus spoken-length FAIL.
- `python3 tools/qa_checklist.py PATH` — writes `qa.md` mechanical boxes from files + human ticks from editor conventions. Never invents scores or auto-checks VO/cards/export/captions.
- `python3 tools/pipeline_status.py` — read-only: status + gate + disk + drift. `--strict` fails on FAIL/drift. Duration WARN is not FAIL and not drift.
- `python3 tools/next_action.py` — read-only: one next human step. Routes `expand-script` before `record-vo` when duration WARN is present. Does not bump status.
- `python3 tools/hint.py` — read-only: copy-paste CLI for that step. Does not bump status. Does not lead with `--write`.
- `python3 tools/doctor.py` — read-only session start: gate, drift, duration WARN, next-action, hint CLI.
- A hook that has words but is outside 20-35 still fails in both validate gates.
- Status drift: `ready_for_vo` needs a PASS script gate; `ready_for_edit` needs selected VO on disk; `ready_to_publish` / `published` need VO + export. Do not bump status to hide missing files.

## Human handoff

Manual gates are time-bounded by `docs/operator_escalation.md`: after 24 hours, the recurring agent may take the documented safe fallback instead of repeatedly re-asking for the same action. Provider credentials/authentication remain a separate hard boundary.

Operator path: `docs/human_session.md`.

While Q1 is `ready_for_vo` with no selected take, the live job is the named packet-relative take — not session-start printers. Do not start at `doctor.py` / `queue_status.py` / `next_topic.py`. Those commands are new-packet only. Follow `docs/human_session.md` Live job + steps 5–7.

Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning`
Selected VO: `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`

After a mark-needed folder exists (new packet only) those printers, `docs/human_session.md`, `docs/agent_session.md` WAVE 3, README Human session, and this page name:

```bash
python3 tools/idea_brief.py PATH --block
# paste idea fields by hand into PATH/idea.md
python3 tools/idea_brief.py PATH --check
```

After saving PATH/draft.md, run `python3 tools/words.py PATH` before apply --write.
After a GitHub write of a high-risk tool, run `python3 tools/prove_locks.py`.
Anything a human must still do is listed under `Remaining human work` in `packet.md`.
`tools/next_action.py` picks one of those constraints from gate + drift + disk + duration band.
`tools/hint.py` prints the matching dry-run command.
Editing conventions: `docs/editor.md`.
Format timing: `docs/format.md`.
Narration paths: `docs/narration.md`.
Asset filenames: `docs/assets.md`.
Render presence: packet `render.md`.
VO reading card: packet `vo_session.md`.
Beat budget: packet `expand.md`.
Expand paste pack: `python3 tools/expand_prompt.py PATH`.
Paste-back gate: `python3 tools/apply_script.py PATH --from PATH/draft.md` (dry-run; `--write --refresh` on non-fixture only).
Status gate: `python3 tools/set_status.py PATH --to STATUS` (dry-run; `--write` after evidence).
Human visual/audio ticks live in `qa.md` under **Human**.
