Run 1312 note: OAuth idle continues across 1300+ runs with published=0 (~47 days, HIGH / INCREASINGLY_SUSPICIOUS). Contracts 96/96 green. Pre-upload path complete. Enhanced research_verification_checklist.py to list non-heading digit lines as targeted potential claims (reduces research verification labor). Updated labor_reduction_map.md. No new soft tools. Do not add another aggregator, soft report, consistency printer, or contract lock while STALL_OAUTH_IDLE is primary. Prefer the human OAuth step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py then three secrets + single execute=true dispatch) or a truly new production capability that advances post-publish readiness or reduces minutes in the labor map without credentials. Do not poll secrets. Do not rematerialize media if present. Do not scaffold Q2. Long stall is HIGH suspicion and increasingly so; flag if no human progress. Successive pure-confirmation or minor pointer runs have diminishing returns and should be avoided when the stall is the sole blocker. After first private video id: consult docs/q1_post_publish_prep.md and docs/labor_reduction_map.md then python3 tools/post_publish_path_ready.py then after_upload_steps.py. Pure inspection runs should be minimized going forward.

# NEXT RUN PROMPT

## External-media materialization gate

Before treating `OPERATOR_HOLD.md` as read-only, check whether the durable Q1 media releases are available and `gh` is authenticated. When they are, run:

```bash
python3 tools/materialize_q1_release.py
```

This is a local media write only. Confirm with media_qa.py. Do not commit media.

## Delegated approval policy

The human operator has explicitly authorized the scheduled agent to perform **any action previously deferred solely because it was labeled human approval, review, sign-off, or an unchecked approval box**. Do not leave approval-only work blocked merely because an instruction assigns the check to a human.

This authorization includes, when the underlying artifact and evidence are available:

- checking repository approval/review boxes;
- reviewing and approving captions, thumbnails, metadata, and production QA;
- selecting an already-authorized generated fallback;
- completing the normal publish step after all mechanical gates pass.

Do not use this authorization to invent media, invent credentials, invent analytics, or bypass a real external dependency. Do not poll secrets. Do not rematerialize if media is present.
