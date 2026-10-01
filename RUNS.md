# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-10-01T10:25:00Z — Run 243

- **Objective:** Do not repeat a hold heartbeat. The Run 242 handoff was the only production step left, and it was not durable. Recover that handoff without committing audio and without claiming Selected VO.
- **Inspected:** STATE, NEXT, FAILURES, RUNS, OPERATOR_HOLD, docs/gate_machine.md, .gitignore, live packet listing, tools/media_qa.py level constants. Packet still 15 markdown files. No `vo/` directory. Workspace artifacts empty at start. HTTPS clone not retried.
- **Action taken:** Confirmed the Run 242 wav was gone. Regenerated 941 WORDS with edge-tts `en-US-AndrewNeural` (espeak-ng still uninstallable: not present, apt not retried). Wrote the wav only under operator artifacts `handoff/`. Measured PCM with the same constants as media_qa.py. Recorded sha256 in `HANDOFF.md`. Pointed `docs/gate_machine.md` at that checksum. Did not `git add` the wav. Did not bump status. Did not scaffold Q2. Did not add a TTS wrapper.
- **Result:** Operator file `handoff/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`, 27200958 bytes, 308.40 s, sha256 `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2`, peak=0.7713, rms=0.1012, silence_frac=0.5086, clip_frac=0.0000. Those four level checks would PASS media_qa if copied to the packet-relative DROP. Automated steps stay 94. Videos produced stay 0. Estimated human minutes stay 3.7. Packet status stays `ready_for_vo`.
- **Verification status:** GitHub file API listing confirms no `vo/`. Local wave decode plus media_qa constants (SILENCE_ABS 0.02, CLIP_ABS 0.99, MIN_PEAK 0.05, MAX_PEAK 0.999, MIN_RMS 0.008, MAX_SILENCE_FRAC 0.60). ffprobe duration 00:05:08.40. Not run through `media_qa.py` (no checkout). Not on the gate machine. Drive listing not separately confirmed; the artifacts write is the handoff.
- **Important discovery:** Run 242's "do not regenerate unless lost" instruction could not be followed as written, because the file and the loss signal both died with the sandbox. Checksum-in-git plus artifacts file is the smallest durable handoff that still respects gitignore.
- **Blocker:** Packet-relative Selected VO still absent. No OAuth. No local master in the repo.
- **Recommended next action:** Operator copies the artifacts handoff to the DROP path and checks sha256 against `HANDOFF.md`, then runs narration_adapter / vo_session / card_generator / timeline / media_qa. Do not regenerate if that file is present. Do not commit the wav.

## 2026-10-01T09:16:00Z — Run 242

- **Objective:** Do not repeat the Run 241 same-day heartbeat. Try the only unblocked production step the gate page already authorizes: a labeled generated take for Q1. Do not commit audio. Do not claim the gate machine now has Selected VO.
- **Inspected:** STATE, NEXT, FAILURES, RUNS, OPERATOR_HOLD, BLOCKED, docs/gate_machine.md, narration_adapter.py, media_qa.py thresholds, live packet listing. Packet still 15 markdown files. No `vo/` directory. HEAD before this commit was Run 241 `56c4aeb`. HTTPS clone not retried.
- **Action taken:** Attempted the gate-page espeak-ng one-liner. apt-get cannot install espeak-ng in this sandbox (`setgroups` / `setegid` permission failure). Synthesized 941 WORDS with edge-tts `en-US-AndrewNeural`, converted with ffmpeg to 44.1 kHz s16 mono wav. Measured against media_qa level constants. Did not `git add` the wav. Did not bump status. Did not scaffold Q2. Did not add a TTS wrapper under tools/. Did not add a selftest fixture.
- **Result:** Operator-downloadable handoff only: `002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`, 27,200,958 bytes, 308.40 s, peak=0.7713, rms=0.1012, silence_frac=0.5087, clip_frac=0.0000. Those four level checks would PASS media_qa if the same file were placed at the packet-relative DROP. Automated steps stay 94. Videos produced stay 0. Estimated human minutes stay 3.7. Packet status stays `ready_for_vo`.
- **Verification status:** GitHub file API listing confirms no `vo/`. Local `wave` decode plus PCM peak/RMS/silence/clip against the constants in `tools/media_qa.py` (MIN_PEAK 0.05, MAX_PEAK 0.999, MIN_RMS 0.008, MAX_SILENCE_FRAC 0.60, clip_frac < 0.01). ffprobe duration 00:05:08.40. Not run through `media_qa.py` (no checkout). Not on the gate machine.
- **Important discovery:** This sandbox can make a level-passing generated wav, and still cannot place it where the next agent can see it. Run 213 already proved a sandbox MP3 does not clear the gate. Repeating synthesis without an operator copy is the same stall.
- **Blocker:** Packet-relative Selected VO still absent from git and from any persistent gate machine. apt cannot install espeak-ng here. No OAuth. No local master in the repo.
- **Recommended next action:** Operator copies the handoff wav to `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav` on the gate machine, keeps `vo_origin.md` kind=generated, then runs narration_adapter / vo_session / card_generator / timeline / media_qa. Do not regenerate the wav unless that handoff was lost. Do not commit the wav. Do not commit another hold-only note this week.

## 2026-10-01T08:11:00Z — Run 241

See prior entry in git history before this commit if truncated. Summary: 11-day HOLD heartbeat. Packet had no `vo/`. No capability change.

## 2026-09-20 — Runs 239–240

HOLD verified. No Selected VO. No printer change.

## 2026-09-16 — Runs 138–238

See prior commits. Summary: late-pipeline printers landed; Q1 remains ready_for_vo without an on-disk take.
