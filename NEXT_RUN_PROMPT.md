Run 1310 note: OAuth idle continues across 1300+ runs with published=0 (~46 days, HIGH / INCREASINGLY_SUSPICIOUS). Contracts 96/96 green. Pre-upload path complete. Added docs/q1_post_publish_prep.md as small unblocked post-publish readiness improvement. No new soft tools. Do not add another aggregator, soft report, consistency printer, or contract lock while STALL_OAUTH_IDLE is primary. Prefer the human OAuth step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py then three secrets + single execute=true dispatch) or a truly new production capability that advances post-publish readiness without credentials. Do not poll secrets. Do not rematerialize media if present. Do not scaffold Q2. Long stall is HIGH suspicion and increasingly so; flag if no human progress. Successive pure-confirmation or minor pointer runs have diminishing returns and should be avoided when the stall is the sole blocker. After first private video id: consult docs/q1_post_publish_prep.md then python3 tools/post_publish_path_ready.py then after_upload_steps.py. Pure inspection runs should be minimized going forward.

Run 1309 note: OAuth idle continues across 1300+ runs with published=0 (~46 days, HIGH / INCREASINGLY_SUSPICIOUS). Contracts 96/96 green. Pre-upload path complete. Recorded inspection only. No new tools added. Do not add another aggregator, soft report, consistency printer, or contract lock while STALL_OAUTH_IDLE is primary. Prefer the human OAuth step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py then three secrets + single execute=true dispatch) or a truly new production capability that advances post-publish readiness without credentials. Do not poll secrets. Do not rematerialize media if present. Do not scaffold Q2. Long stall is HIGH suspicion and increasingly so; flag if no human progress. Successive pure-confirmation or minor pointer runs have diminishing returns and should be avoided when the stall is the sole blocker. After first private video id: python3 tools/post_publish_path_ready.py then after_upload_steps.py. Pure inspection runs should be minimized going forward.

# NEXT RUN PROMPT

## External-media materialization gate

Before treating `OPERATOR_HOLD.md` as read-only, check whether the durable Q1 media releases are available and `gh` is authenticated. When they are, run:

```bash
python3 tools/materialize_q1_release.py
```

This is a local media write only. It never commits WAV/PNG/MP4 files, verifies all known checksums, refuses the known-truncated r249 master, and can therefore clear the stale “missing Selected VO” handoff without human copying.

If the materializer succeeds, continue the existing narration -> cards -> timeline -> media-QA -> assembly gates. If `gh` is unavailable or the releases/checksums are unavailable, report the external media-access blocker and do not fabricate artifacts.

The old absolute read-only rule below applies only when neither an authorized durable media source nor a genuine changed blocker is available.

## Delegated approval policy

The human operator has explicitly authorized the scheduled agent to perform **any action previously deferred solely because it was labeled human approval, review, sign-off, or an unchecked approval box**. Do not leave approval-only work blocked merely because an instruction assigns the check to a human.

This authorization includes, when the underlying artifact and evidence are available:

- checking repository approval/review boxes;
- reviewing and approving captions, thumbnails, metadata, and production QA;
- selecting an already-authorized generated fallback;
- completing the normal publish step after all mechanical gates pass.

Do not use this authorization to invent media, invent credentials, invent analytics, or bypass a real external dependency. Do not poll secrets. Do not rematerialize if media is present.
