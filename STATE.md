# STATE

Updated: 2026-10-01T19:20:00Z (Run 253)

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
- Executive: SHIP after YouTube OAuth. Do not re-encode. Do not upload r249. Do not expand architecture.

## Run 253 delta
- Re-encoded Q1 with assemble.py --execute. Duration 328.40s (VO 308.40 + 20s end screen). ftyp and moov present. 1920x1080 h264 + aac.
- sha256 `4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546` (6633603 bytes). Private release `q1-media-r253` asset `q1-master-r253.mp4`. Re-download matched.
- r249 master stays truncated (308.40s). Do not upload it. Do not re-encode unless r253 is missing. Packet status stays ready_for_vo (wav not in git).

## Run 252 delta
- assemble --execute refuses a muxed file without ftyp/moov and leaves export/.segments.
- Evidence: sandbox mux with bare apad was Killed; ffprobe reported moov atom not found.

## Run 251 delta
- assemble recipe and mux use apad=pad_dur=20 then -shortest. Bare apad hangs.
- r249 master sha256 `abec4eb94199d0cbbf00659891d4e79c0040a6b1bb5450fa6e1db0e54c4b4d53` is truncated.

## Metrics snapshot
| Metric | Previous | Current | Notes |
|--------|----------|---------|-------|
| Estimated human min / video | 3.2 | 2.5 | re-encode done; remaining human gate is YouTube OAuth |
| Automated steps | 96 | 96 | header refuse after mux |
| Videos produced | 0 | 0 | padded local master on q1-media-r253; not uploaded |

## Active constraints
- Do not upload q1-media-r249 q1-master.mp4 as the finished export
- Finished local export is q1-media-r253 q1-master-r253.mp4 (328.40s, sha256 4ff4c0e80ac6b5719aa1b8b5acc70b2845820208f56e83881f6e7bad30101546)
- Do not invent a committed wav or bump status past ready_for_vo without Selected VO on disk
- Do not write a dummy export/master.mp4 to flip gates
- Do not regenerate the wav or cards while HANDOFF checksums match
- Do not add a public curl/gdown fetcher
- Do not scaffold Q2
