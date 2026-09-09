# STATE

Updated: 2026-09-09T13:04:00Z (Run 027)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> **monitored packets** -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- No YouTube / TTS / stock / render integrations configured
- HTTPS clone from this agent sandbox still fails (private repo). Push via GitHub file API.
- Reconstruct + selftest path: `docs/agent_session.md`

## What exists now (after Run 027)
- Operating memory files
- Frozen original master prompt
- Video packet standard + scaffold CLI + packet QA (publish gate + draft gate + optional duration gate)
- Sample packet fixture `videos/sample-001-why-systems-beat-motivation/`
- Working niche locked in `docs/channel.md`
- Topic queue `docs/topic_queue.md` (five queued titles; not drafts)
- Read-only next-topic printer `tools/next_topic.py`
- Operator path `docs/human_session.md` (doctor first; fixture freeze; expand → apply → set_status dry-run)
- Agent path `docs/agent_session.md` (clone-once, reconstruct selftest tree, record runtime)
- Fixture contract selftest `tools/selftest.py` (read-only; sample-001 only)
- **Runtime verified 2026-09-09T12:22Z:** reconstructed `/tmp/ca`, `SELFTEST PASS`, exit 0, 153 words, code `expand-script`
- Idea / script / expand / title / QA / research / publish / caption / asset / render / VO / board / next-action / apply-script / set-status / hint / doctor / next-topic tools
- Status writer `tools/set_status.py` (dry-run default; `--write` required; fixture and evidence gates unchanged)
- Command map `tools/hint.py` and health check `tools/doctor.py` remain read-only
- Spoken-duration band: 900-1500 words for `explainer-6-10min` at 150 wpm. Default validate WARNs; `--duration` FAILs. Sample fixture stays PASS + WARN.

## Pipeline map
| Stage        | Status      | Notes                                      |
|--------------|-------------|--------------------------------------------|
| Research     | assisted    | stub written at scaffold; human verifies   |
| Ideas        | assisted    | queue + `new_idea.py`; human still locks   |
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
| Oversight    | monitored   | board + next-action + hint + doctor + gated status write + fixture selftest |
| Topic pick   | templated   | `docs/topic_queue.md` + `next_topic.py`    |
| Operator path| templated   | `docs/human_session.md`                    |
| Agent path   | templated   | `docs/agent_session.md`                    |
| Publishing   | blocked     | YouTube API not configured                 |
| Analytics    | unbuilt     |                                            |

## Metrics snapshot
| Metric                         | Previous     | Current        | Notes                          |
|--------------------------------|--------------|----------------|--------------------------------|
| Estimated human min / video    | 151          | 148            | title pick no longer blank     |
| Automated steps                | 24           | 25             | next_topic is read-only        |
| Remaining manual steps         | most         | most           | source check, script words, VO, card build, edit, caption align, publish |
| Videos produced by system      | 0            | 0              | sample packet is a fixture     |
| Channel niche decided          | locked (temp)| locked (temp)  | `docs/channel.md`              |
| Fixture selftest runtime       | PASS         | PASS (Run 026) | not re-run; no gated-tool edit |

## Active constraints
- Niche lock is agent-chosen until a human overrides DECISIONS.md
- Topic queue titles are working titles, not scripts
- `next_topic.py` must stay read-only and must not call `new_packet.py`
- Do not auto-scaffold Q1 without a human instruction
- No secrets or platform APIs
- Do not invent published videos or integrations
- Do not overwrite sample-001 titles/thumbs/script WORDS
- `apply_script.py` must refuse sample-001 and expand_prompt stdout
- Default apply is dry-run; `--write` is required to replace script.md
- `set_status.py` is the only status writer; dry-run default; no sample-001 promote
- `hint.py`, `doctor.py`, `selftest.py`, and `next_topic.py` are read-only
- Format lock is `explainer-6-10min` only; no shorts split, no ffmpeg recipe
- Default validate 2-tuple stays (errors, incompletes). Duration WARN must not become FAIL unless `--duration`.
- Do not retry HTTPS clone after one failure in a run. Reconstruct per `docs/agent_session.md`.
