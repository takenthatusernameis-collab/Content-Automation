# STATE

Updated: 2026-10-02T02:20:00Z (Run 257)

## What this system is
A YouTube production system under construction. Goal: reliable, repeatable videos with declining human minutes per video.

## Current maturity
manual -> assisted scaffolding -> monitored packets + Q1 ready_for_vo + Selected VO path locked packet-relative + narration adapter + labeled generated fallback + local card generator + WORDS timeline planner + fail-closed media QA + credential-ready dry-run uploader + fail-closed ffmpeg assemble planner (segmented execute + apad=pad_dur end screen + post-mux ftyp/moov refuse) + fail-closed feedback/experiment/complete gates + gate-machine drop recipe -> automated -> self-improving

## Repo reality
- GitHub: `takenthatusernameis-collab/Content-Automation`
- Default branch: `main`
- No published videos
- Live packet: `videos/002-stop-deciding-what-to-work-on-every-morning` status `ready_for_vo`
- Durable fetch: private release `q1-media-r253` (padded master) plus r249 wav/cards and Drive folder in HANDOFF.md
- r249 master is truncated (308.40s). Finished local export is `q1-media-r253` `q1-master-r253.mp4` (328.40s).
- Executive: SHIP after publish.md human edit and YouTube OAuth. Do not re-encode. Do not upload r249. Do not expand architecture.

## Run 257 delta
- `docs/human_session.md` and `docs/agent_session.md` no longer tell the live job to record or drop a new take. Remaining labor is the publish.md stub edit plus YouTube OAuth. Fetch stays r249 wav/cards and r253 master only.
- `tools/next_action.py` returns `upload-blocked` for this packet at `ready_for_vo` instead of `record-vo`. `tools/hint.py` names the same edit. Other packets still record-vo.
- Releases `q1-media-r253` and `q1-media-r249` still listed. Did not re-download. Did not re-encode. Did not upload. Did not edit the human description.

## Run 256 delta
- HANDOFF no longer copies `q1-media-r249` `q1-master.mp4` onto `export/master.mp4`. That block now copies wav and PNGs only. Finished master copy is the r253 asset only.
- Release list still shows `q1-media-r253` and `q1-media-r249`. Did not re-download. Did not re-encode. Did not upload. Did not edit the human description.

## Run 255 delta
- youtube_upload now HOLD_LOCAL when publish.md still has the stub sentence "No upload happened" or an unchecked Human before upload item (description / pin). Word count alone no longer looks upload-ready.
- Live Q1 dry-run: gate FAIL, action HOLD_LOCAL, publish_copy_approved FAIL. Master still absent on this checkout. Did not re-encode. Did not upload. Did not edit the human description.
- selftest PASS.

## Run 254 delta
- `youtube_upload.py` refuses r249 truncated master sha256 `abec4eb94199d0cbbf00659891d4e79c0040a6b1bb5450fa6e1db0e54c4b4d53` and any VO-length export missing the 20s end screen.
- `docs/gate_machine.md` no longer tells the operator to copy r249 `q1-master.mp4` onto export/master.mp4. Finished master remains `q1-media-r253`.
- selftest PASS. Did not re-encode. Did not upload. Packet status stays ready_for_vo.

## Run 253 delta
- Re-encoded Q1 with assemble.py --execute. Duration 328.40s (VO 308.40 + 20s end screen). ftyp and moov present. 1920x1080 h264 + aac.
- sha256 `4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546` (6633603 bytes). Private release `q1-media-r253` asset `q1-master-r253.mp4`. Re-download matched.
- r249 master stays truncated (308.40s). Do not upload it. Do not re-encode unless r253 is missing. Packet status stays ready_for_vo (wav not in git).

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 2.5 | 2.0 | publish edit is delete-one-sentence plus two checks; OAuth remains |
| Automated steps | 98 | 98 | Q1 next_action no longer routes to record-vo |
| Videos produced | 0 | 0 | padded local master on q1-media-r253; not uploaded |

## Active constraints
- Do not upload q1-media-r249 q1-master.mp4 as the finished export
- Do not follow an old HANDOFF snippet that copies that file onto export/master.mp4
- Finished local export is q1-media-r253 q1-master-r253.mp4 (328.40s, sha256 4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546)
- Do not invent a committed wav or bump status past ready_for_vo without Selected VO on disk
- Do not write a dummy export/master.mp4 to flip gates
- Do not regenerate the wav or cards while HANDOFF checksums match
- Do not add a public curl/gdown fetcher
- Do not scaffold Q2
