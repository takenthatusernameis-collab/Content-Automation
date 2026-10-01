# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-10-01T11:20:00Z — Run 244

- **Objective:** Stop the lost-sandbox-wav stall. Run 243's artifacts handoff was not durable. Recover the same bytes and leave a pointer the next agent can fetch. Do not claim Selected VO. Do not commit audio.
- **Inspected:** STATE, NEXT, HANDOFF, FAILURES, RUNS, OPERATOR_HOLD, docs/gate_machine.md, live packet listing. Packet still 15 markdown files. No `vo/` directory. Workspace artifacts empty at start. Drive search for the exact wav name returned no file. HTTPS clone not retried.
- **Action taken:** Regenerated 941 WORDS with edge-tts `en-US-AndrewNeural`. sha256 matched Run 243 (`758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2`, 27200958 bytes). Created Drive folder `Content-Automation-handoff` (`1ftaVyh8BWQeWp45TIyX7Hh1o0MPmGRev`) and uploaded the wav. Re-searched Drive and confirmed file id `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl` at 27200958 bytes. Did not `git add` the wav. Did not bump status. Did not scaffold Q2. Did not add a TTS wrapper.
- **Result:** Durable generated handoff is the Drive file, not the session artifacts path. Automated steps stay 94. Videos produced stay 0. Estimated human minutes stay 3.7. Packet status stays `ready_for_vo`.
- **Verification status:** Local sha256 match against HANDOFF.md. Drive files.list exact-name search returned the file id and size_bytes 27200958. Packet listing via GitHub file API still has no `vo/`. Not run through `media_qa.py` (no checkout). Not on the gate machine.
- **Important discovery:** Session artifacts writes do not appear in the connected Drive the next run can search. An explicit Drive upload with a recorded file id does. That still does not clear the packet-relative gate.
- **Blocker:** Packet-relative Selected VO still absent. No OAuth. No local master in the repo.
- **Recommended next action:** Download Drive file `1lnk7JB9uu2puCsWPuyScs_CchoQZsxZl`, copy it to the DROP path, check sha256, then run narration_adapter / vo_session / card_generator / timeline / media_qa. Do not regenerate while that Drive file lists 27200958 bytes. Do not commit the wav.

## 2026-10-01T10:25:00Z — Run 243

- **Objective:** Do not repeat a hold heartbeat. The Run 242 handoff was the only production step left, and it was not durable. Recover that handoff without committing audio and without claiming Selected VO.
- **Inspected:** STATE, NEXT, FAILURES, RUNS, OPERATOR_HOLD, docs/gate_machine.md, .gitignore, live packet listing, tools/media_qa.py level constants. Packet still 15 markdown files. No `vo/` directory. Workspace artifacts empty at start. HTTPS clone not retried.
- **Action taken:** Confirmed the Run 242 wav was gone. Regenerated 941 WORDS with edge-tts `en-US-AndrewNeural` (espeak-ng still uninstallable: not present, apt not retried). Wrote the wav only under operator artifacts `handoff/`. Measured PCM with the same constants as media_qa.py. Recorded sha256 in `HANDOFF.md`. Pointed `docs/gate_machine.md` at that checksum. Did not `git add` the wav. Did not bump status. Did not scaffold Q2. Did not add a TTS wrapper.
- **Result:** Operator file `handoff/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`, 27200958 bytes, 308.40 s, sha256 `758bfa4056c7d3ce588dafe7b40c5cccdd3a54df429ecf4583fa256cb1591da2`, peak=0.7713, rms=0.1012, silence_frac=0.5086, clip_frac=0.0000. Those four level checks would PASS media_qa if copied to the packet-relative DROP. Automated steps stay 94. Videos produced stay 0. Estimated human minutes stay 3.7. Packet status stays `ready_for_vo`.
- **Verification status:** GitHub file API listing confirms no `vo/`. Local wave decode plus media_qa constants (SILENCE_ABS 0.02, CLIP_ABS 0.99, MIN_PEAK 0.05, MAX_PEAK 0.999, MIN_RMS 0.008, MAX_SILENCE_FRAC 0.60). ffprobe duration 00:05:08.40. Not run through `media_qa.py` (no checkout). Not on the gate machine. Drive listing not separately confirmed; the artifacts write is the handoff.
- **Important discovery:** Run 242's "do not regenerate unless lost" instruction could not be followed as written, because the file and the loss signal both died with the sandbox. Checksum-in-git plus artifacts file is the smallest durable handoff that still respects gitignore.
- **Blocker:** Packet-relative Selected VO still absent. No OAuth. No local master in the repo.
- **Recommended next action:** Operator copies the artifacts handoff to the DROP path and checks sha256 against `HANDOFF.md`, then runs narration_adapter / vo_session / card_generator / timeline / media_qa. Do not regenerate if that file is present. Do not commit the wav.

Earlier runs remain in git history before this file was rewritten with the Run 244 entry. Run 242 and earlier summaries are in commit `fb03114b8629771e9a7921615f0584d0e2f28af2` and below.
