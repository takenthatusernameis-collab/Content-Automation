# STATE

Updated: 2026-08-28T14:15:00+03:00 (Run 021)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- No YouTube / TTS / stock / render integrations configured

## What exists now (after Run 021)
- Operating memory files
- Frozen original master prompt
- Video packet standard + scaffold CLI + packet QA (publish gate + draft gate + optional duration gate)
- Sample packet fixture `videos/sample-001-why-systems-beat-motivation/`
- Working niche locked in `docs/channel.md`
- Idea / script / expand / title / QA / research / publish / caption / asset / render / VO / board / next-action / apply-script tools as of Run 020
- Status writer `tools/set_status.py` (dry-run default; `--write` required; refuses sample-001 promote; refuses skip-ahead; refuses ready_for_vo on duration WARN; refuses ready_for_edit without Selected VO; refuses publish statuses without VO + export + PASS). Does not create media. Board tools stay read-only.
- Spoken-duration band: 900-1500 words for `explainer-6-10min` at 150 wpm. Default validate WARNs; `--duration` FAILs. Sample fixture stays PASS + WARN.

## Pipeline map
| Stage        | Status      | Notes                                      |
|--------------|-------------|--------------------------------------------|
| Research     | assisted    | stub written at scaffold; human verifies   |
| Ideas        | assisted    | `tools/new_idea.py` fills idea card        |
| Scripts      | assisted    | beats + duration WARN + expand.md + paste prompt + paste-back gate |
| Narration    | assisted    | session card + path rules; no VO file / TTS|
| Assets       | assisted    | VISUAL -> planned card names; no binaries  |
| Editing      | templated   | tracks in editor.md; timing in format.md   |
| Captions     | assisted    | cue list from WORDS; not timed to a take   |
| Thumbnails   | assisted    | heuristic brief at scaffold if empty       |
| Titles       | assisted    | heuristic brief at scaffold if empty       |
| QA           | assisted    | checklist written at scaffold after titles |
| Publish meta | assisted    | `publish.md` stub; no API                  |
| Rendering    | assisted    | `render.md` presence only; no ffmpeg       |
| Oversight    | monitored   | board + next-action + gated status write   |
| Publishing   | blocked     | YouTube API not configured                 |
| Analytics    | unbuilt     |                                            |

## Metrics snapshot
| Metric                         | Previous     | Current        | Notes                          |
|--------------------------------|--------------|----------------|--------------------------------|
| Estimated human min / video    | 167          | 162            | skip hand status edits + drift repair |
| Automated steps                | 20           | 21             | set_status evidence gate       |
| Remaining manual steps         | most         | most           | source check, script words, VO, card build, edit, caption align, publish |
| Videos produced by system      | 0            | 0              | sample packet is a fixture     |
| Channel niche decided          | locked (temp)| locked (temp)  | `docs/channel.md`              |

## Active constraints
- Niche lock is agent-chosen until a human overrides DECISIONS.md
- No secrets or platform APIs
- Do not invent published videos or integrations
- Do not overwrite sample-001 titles/thumbs/script WORDS
- `apply_script.py` must refuse sample-001 and expand_prompt stdout
- Default apply is dry-run; `--write` is required to replace script.md
- `--refresh` may rewrite expand.md / vo_session.md / captions.md only after a successful write on a non-fixture packet
- apply_script does not bump packet.md status
- `set_status.py` is the only status writer; dry-run default; no sample-001 promote
- `expand_prompt.py` may print a fixture lock banner; that print is not a draft
- New packets should use default scaffold generate; `--no-generate` is the opt-out
- Format lock is `explainer-6-10min` only; no shorts split, no ffmpeg recipe
- `pipeline_status.py` and `next_action.py` must stay read-only
- Default validate 2-tuple stays (errors, incompletes). Duration WARN must not become FAIL unless `--duration`.
