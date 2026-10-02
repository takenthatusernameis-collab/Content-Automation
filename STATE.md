# STATE

Updated: 2026-10-02T04:15:00Z (Run 262)

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
- Executive: SHIP after a human checks the two open publish.md boxes and YouTube OAuth. Do not re-encode. Do not upload r249. Do not expand architecture. Do not check those boxes from an agent run.

## Run 262 delta
- Dry-run uploader now carries captions.srt as a local track (present, cue count, sha256) and always sets uploaded=false. It still never calls videos.insert or captions.insert.
- Wrapped the one Q1 caption line over 42 characters. Timings and 941 words unchanged. Did not regenerate from the wav.
- selftest locks that the dry-run must not claim captions were uploaded. selftest PASS in this checkout.
- Did not check publish boxes. Did not re-encode. Did not upload. Did not scaffold Q2.

## Run 261 delta
- Added tools/caption_align.py. It drafts captions.srt from Selected VO speech gaps and script WORDS. Missing wav refuses. Not ASR. Not an approval.
- Q1 captions.srt written (103 cues, 941 words, speech 208.38s of 308.40s). Human spot-check box stays open. Did not check publish boxes. Did not re-encode. Did not upload. Did not scaffold Q2.

## Run 260 delta
- Operator pages and pipeline_status still told a human to delete `No upload happened` after Run 259 removed that sentence. Those pointers now name the two open boxes and forbid restoring the stub.
- publish_brief refuses the Q1 packet so `--force` cannot overwrite the drafted description with the stub.
- selftest locks the board text and the live publish.md draft (stub absent, generated voice labeled, both boxes open). selftest PASS in this checkout.
- Did not re-download. Did not re-encode. Did not upload. Did not scaffold Q2. Did not check the human boxes.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 1.5 | 1.4 | caption line wrap no longer a human edit; publish boxes and OAuth remain |
| Automated steps | 101 | 102 | dry-run upload request carries captions.srt; captions.insert still not called |
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
- Do not check Description edited or First comment approved from an agent run
- Do not restore the stub sentence `No upload happened` into publish.md
- Do not tell the operator to delete that sentence; it is already gone
