# STATE

Updated: 2026-09-13T06:19:00Z (Run 111)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets + write-path + words.py band + idea-lock INFO + writer band-landing + template draft.md + new_packet draft overwrite reprint + empty-heading expand budget + live expand_prompt budget on stub + human_session empty-script Target column + hint expand-script Target comment + first human-approved Q1 packet** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- HTTPS clone from this agent sandbox still fails. Push via GitHub file API.
- Q1 is now scaffolded as `videos/002-stop-deciding-what-to-work-on-every-morning/` and marked `used`.
- Q1 `idea.md` is filled with the locked topic/problem/mechanism plus the channel-locked viewer/why-now/related fields.
- Q1 `draft.md` and `script.md` exist; `draft.md` remains the off-repo writer save target and `script.md` must only be populated through the existing apply path.
- Run 111 intentionally consumed the human decision that had blocked Runs 107-110. Brok should now work the real Q1 packet instead of changing another printer or reopening the scaffold decision.
- Do not fabricate spoken WORDS, VO, cards, exports, or publishing credentials.

## What exists now (after Run 111)
- First non-fixture packet: `videos/002-stop-deciding-what-to-work-on-every-morning/`
- Q1 queue row: `used`
- idea.md: PASTE READY for the locked fields
- draft.md: initialized as writer save target
- script.md: initialized from the packet template
- The next useful work is on the Q1 packet, not another repository-wide alignment pass.

## Pipeline map
Q1 is past the scaffold + idea gate. Next live work is the expand/write path: use the existing Target allocation and `prompts/script_writer.md`, then save the writer output to Q1/draft.md. From there use the existing words/apply/validate path. Do not treat draft.md as script.md until apply_script --write succeeds.

After a high-risk GitHub write: `python3 tools/prove_locks.py`.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 64 | 63 | Q1 scaffold/idea decision is now resolved once rather than revisited hourly |
| Automated steps | 84 | 84 | no new CLI |
| Videos produced | 0 | 0 | Q1 packet exists; production is not complete |

## Active constraints
- Do not return to Q1 scaffolding: the human-approved Q1 packet now exists.
- Do not auto-scaffold Q2 or later while Q1 is active.
- Do not fabricate WORDS, wav, cards, exports, or publish actions.
- Do not treat draft.md as script.md.
- Do not write idea.md again unless the packet's locked fields actually regress.
- Do not retry HTTPS clone as the first action.
- Do not add another wrapper CLI around idea_lock_notes.
- Do not add another idea_brief flag unless --queue regresses.
- Do not add WAVE 4.
- Do not rewrite writer prompts again unless the first real Q1 draft misses the 900-1500 band.
- Do not add a second draft template or a CLI that reprints Band landing.
- Do not add another new_packet followup unless the draft overwrite reprint regresses.
- Do not hide the empty-WORDS expand budget table again.
- Do not make expand_prompt write expand.md.
- Do not strip the Target column from docs/human_session.md step 3.
- Do not strip the Target comment from hint.py write-script/expand-script commands.
- Reconstruct-loop watch is closed for the current Q1 bottleneck: no new reconstruct path unless a real missing-file failure is proven.
