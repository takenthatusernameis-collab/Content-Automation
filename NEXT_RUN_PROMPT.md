Run 1220 note: OAuth idle continues across 1000+ runs with published=0. Successive pure inspection/confirmation runs recorded; no new tools or contracts. Pre-upload path complete. Contracts expected green. Do not add another aggregator, soft report, consistency printer, or contract lock while STALL_OAUTH_IDLE is primary. Prefer the human OAuth step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py then three secrets + single execute=true dispatch) or a truly new production capability that advances post-publish readiness without credentials. Do not poll secrets. Do not rematerialize media if present. Do not scaffold Q2. Long stall is HIGH suspicion and increasingly so; flag if no human progress. Successive pure-confirmation runs have diminishing returns and should be avoided when the stall is the sole blocker.

Run 1218 note: OAuth idle continues across 1000+ runs with published=0. Successive pure inspection/confirmation runs recorded; no new tools or contracts. Pre-upload path complete. Contracts expected green. Do not add another aggregator, soft report, consistency printer, or contract lock while STALL_OAUTH_IDLE is primary. Prefer the human OAuth step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py then three secrets + single execute=true dispatch) or a truly new production capability that advances post-publish readiness without credentials. Do not poll secrets. Do not rematerialize media if present. Do not scaffold Q2. Long stall is HIGH suspicion and increasingly so; flag if no human progress. Successive pure-confirmation runs have diminishing returns and should be avoided when the stall is the sole blocker.

Run 1172 note: OAuth idle continues across 1000+ runs with published=0. Pure inspection recorded; no new tools or contracts. Pre-upload path complete. Contracts expected 96/96. Do not add another aggregator, soft report, consistency printer, or contract lock while STALL_OAUTH_IDLE is primary. Prefer the human OAuth step (python3 tools/oauth_complete_guide.py or docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py then three secrets + single execute=true dispatch) or a truly new production capability that advances post-publish readiness without credentials. Do not poll secrets. Do not rematerialize media if present. Do not scaffold Q2. Long stall is HIGH suspicion and increasingly so; flag if no human progress. Successive pure-confirmation runs have diminishing returns. After collect: feedback_review_brief.py then feedback_to_baseline_suggest.py && feedback_topic_suggest.py. After comparison: feedback_to_decision_suggest.py. After decision: next_from_decision.py.

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

Do not fabricate evidence. For a sensory or artifact-based check, perform the check when the artifact is actually accessible to the agent; do not claim to have listened to audio, watched video, or inspected an inaccessible binary. An evidence boundary is still a real blocker even though a “human approval” label is no longer a blocker.

Third-party authentication/authorization, payment, safety, and provider-policy boundaries remain hard constraints. The agent may not bypass them or invent credentials. Once valid credentials are available, approval-only holds must not stop the normal production/publish path.

**Hard-stop addition from Run 184:**

- If `OPERATOR_HOLD.md` is active and the packet-relative Selected VO file is still missing, the run must be **read-only**: inspect state, report the blocker, and make **no repository changes and no commit**. Do not refresh `STATE.md`, `NEXT.md`, `RUNS.md`, or any other hold-status snapshot merely to record that the hold still exists.
- A new commit is permitted only when the hold condition changes (for example, a real selected VO file is supplied), a genuine regression prevents the already-defined next action, or a human explicitly changes the policy.
- Repeatedly re-asserting the same hold is non-productive churn and must be treated as a failed run, not as progress.

## Production-first freeze after authorized fallback

The selected-VO escalation has elapsed and generated narration is authorized. Do not add capability scaffolding while the live packet can be advanced through the existing production path.

The first action for a missing Q1 packet media set is `tools/materialize_q1_release.py` when authenticated `gh` access and the durable releases exist. Only when that source is unavailable should the run stop for the external media-access blocker.

Do not treat `vo_origin.md kind: generated` as proof that a file is on disk; the materializer or another verified copy operation must create the packet-relative files first.

Once the files are present, resume the existing narration, card, timeline, media-QA, and assembly gates in order.

**This freeze supersedes broad capability progression while the existing packet can be advanced through its defined production path.**

(Older targeted additions and full prompt body remain below or are preserved from prior version. Do not expand scope.)
