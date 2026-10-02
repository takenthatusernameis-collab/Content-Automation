# RUNS

Permanent log. Newest first. If the same action repeats across runs with no progress, flag it.

## 2026-10-02T03:20:00Z — Run 261

- **Objective:** Stop leaving caption timing as a blank human task after the Selected VO duration was already known.
- **Inspected:** STATE/NEXT/RUNS/FAILURES after Run 260. Failures said another printer-only restatement of the publish hold should be flagged. captions.md was still a 150 wpm stub. Downloaded r249 wav (27200958 bytes, 308.40s) and measured speech gaps.
- **Action taken:** Added tools/caption_align.py. Wrote Q1 captions.srt (103 cues). Left publish boxes and the caption spot-check unchecked. Did not re-encode. Did not upload. Did not scaffold Q2.
- **Result:** Future packets can draft an SRT from a DROP wav without Whisper. Human caption work is spot-check, not invent times. Estimated human minutes stay 1.5 because publish boxes and OAuth still dominate. Automated steps 100 -> 101. Videos published stay 0.
- **Verification status:** python3 tools/selftest.py printed SELFTEST PASS. caption_align.py printed CAPTION_DRAFT cues=103 words=941 speech_s=208.38 duration=308.40. First cues match the script hook. Not claimed as ASR.
- **Important discovery:** The r249 wav has 208.38s of speech inside 308.40s. Equal word spacing on speech time is enough for a review draft. Runs 254-260 did not move this.
- **Blocker:** Human must check the two open publish boxes and spot-check captions.srt. YouTube OAuth still absent.
- **Recommended next action:** Human reviews publish.md and captions.srt. Copy q1-master-r253.mp4 only onto export/master.mp4. Set OAuth. Do not record. Do not restore the stub sentence.

## 2026-10-02T02:12:00Z — Run 260

- **Objective:** Stop the remaining operator pages from assigning a compose task Run 259 already finished.
- **Inspected:** STATE/NEXT/RUNS/HANDOFF/publish.md after Run 259. Releases not re-downloaded. publish.md has the drafted description, generated-voice label, and two open boxes. pipeline_status, gate_machine, human_session, agent_session, and HANDOFF still said delete `No upload happened`.
- **Action taken:** Those pointers now say review the draft and check the two boxes. publish_brief refuses the Q1 packet. selftest locks the board text and the live publish.md. Did not check the boxes. Did not re-download. Did not re-encode. Did not upload. Did not scaffold Q2.
- **Result:** A human following the gate page no longer hunts for a missing sentence. Estimated human minutes stay 1.5. Automated steps stay 100. Videos published stay 0. Packet status stays ready_for_vo.
- **Verification status:** `python3 tools/selftest.py` printed SELFTEST PASS in this checkout. `publish_brief.py` on Q1 exited 1 with the refuse line. pipeline_status printed the review line, not the delete line. Push pending this record.
- **Important discovery:** Run 259 fixed next_action and hint only. The pages a human actually opens still assigned the old compose step.
- **Blocker:** Human must check the two open publish boxes. YouTube OAuth still absent.
- **Recommended next action:** Human reviews publish.md and checks Description edited and First comment approved. Copy q1-master-r253.mp4 only onto export/master.mp4. Set OAuth. Do not record. Do not restore the stub sentence.

## 2026-10-02T04:20:00Z — Run 259

- **Objective:** Stop the recurring stall on composing the Q1 description. Draft the viewer copy and leave approval unchecked.
- **Inspected:** STATE/NEXT/RUNS/HANDOFF after Run 258. Releases `q1-media-r253` (2026-10-01T19:18:04Z) and `q1-media-r249` still listed. publish.md still contained `No upload happened` and two open boxes. Runs 254–258 only redirected printers; the compose step did not move.
- **Action taken:** Replaced the Description section with a mechanism-specific draft that labels narration as generated. Left Description edited and First comment approved unchecked. next_action and hint now name those boxes instead of deleting the stub sentence. Did not check the boxes. Did not re-download. Did not re-encode. Did not upload. Did not scaffold Q2.
- **Result:** Human work on this packet is review-and-check, not write-the-description. Estimated human minutes 2.0 -> 1.5. Automated steps 99 -> 100. Videos published stay 0. Packet status stays ready_for_vo. Commits: 764124d (publish.md, STATE, NEXT) and b7272f7 (hint.py, next_action.py).
- **Verification status:** GitHub push accepted for those commits. selftest not re-run in that sandbox (no checkout). Box check not claimed. Releases listed, not re-downloaded.
- **Important discovery:** The repeated miss was treating the stub sentence as a human compose task after the script, title, and pin draft already existed.
- **Blocker:** Human must check the two open publish boxes. YouTube OAuth still absent.
- **Recommended next action:** Human reviews publish.md and checks Description edited and First comment approved. Copy q1-master-r253.mp4 only onto export/master.mp4. Set OAuth. Do not record. Do not restore the stub sentence.

Earlier runs remain in git history at 65cca063 and prior.
