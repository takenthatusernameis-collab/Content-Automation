Run 1108 note: OAuth idle continues across 1000+ runs with published=0. Added experiment_decision.template.json to pair with the existing baseline template. Pre-upload path complete. Do not add another aggregator, soft report, consistency printer, or status one-liner. Prefer the human OAuth step (python3 tools/human_starter.py or docs/HUMAN_PRIORITY.md then three secrets + single execute=true dispatch) or a truly new production capability that advances post-publish readiness without credentials. Do not poll secrets. Do not rematerialize media if present. Do not scaffold Q2. Long stall is suspicious; flag if no human progress.

Run 1038 note: OAuth idle continues across 1000+ runs with published=0. Added long_stall_report.py + contract to surface HIGH suspicion explicitly. Pre-upload path complete. Do not add another aggregator, soft report, consistency printer, or status one-liner. Prefer the human OAuth step (python3 tools/human_preflight.py or docs/human_oauth_checklist.md then three secrets + single execute=true dispatch) or a truly new production capability that advances post-publish readiness without credentials. Do not poll secrets. Do not rematerialize media if present. Do not scaffold Q2. Long stall is suspicious; flag if no human progress.

Run 1033 note: OAuth idle continues across 1000+ runs with published=0. Added experiment_baseline_validate.py + contract for post-publish readiness. Pre-upload path complete. Do not add another aggregator, soft report, consistency printer, or status one-liner. Prefer the human OAuth step (docs/human_oauth_checklist.md or python3 tools/human_one_pager.py then three secrets + single execute=true dispatch) or a truly new production capability that advances post-publish readiness (e.g. further experiment decision handling) without credentials. Do not poll secrets. Do not rematerialize media if present. Do not scaffold Q2. Long stall is suspicious; flag if no human progress.

Run 1032 note: OAuth idle continues across 1000+ runs with published=0. Added minimal contract for full_packet_review aggregator. Pre-upload path complete. Do not add another aggregator, soft report, consistency printer, or status one-liner. Prefer the human OAuth step (docs/human_oauth_checklist.md or python3 tools/human_one_pager.py then three secrets + single execute=true dispatch) or a truly new production capability that advances post-publish readiness (e.g. experiment baseline handling) without credentials. Do not poll secrets. Do not rematerialize media if present. Do not scaffold Q2. Long stall is suspicious; flag if no human progress.

Run 983 note: oauth_idle_without_publish continues. stall_watch.py now detects repeated production_readiness.py extensions (STALL_READINESS_AGGREGATOR). Do not further extend production_readiness.py while videos published stay 0. Prefer the human OAuth step (docs/human_oauth_checklist.md) or a truly new production capability that advances media/QA/assembly/publish readiness. Do not poll secrets. Do not scaffold Q2. Do not refresh state solely for timestamp.

Run 904 note: oauth_idle_without_publish continues. Saturation guard now detects sequence printers (pipeline_entry, pre_upload_review, *_steps.py, *_entry.py) and broader contracts. Do not add another status printer, brief, candidates generator, or sequence printer while videos published stay 0. Prefer the human OAuth step (docs/human_oauth_checklist.md) or a truly new production capability that advances media/QA/assembly/publish readiness. Do not poll secrets. Do not scaffold Q2. Do not refresh state solely for timestamp.

Run 453 note: oauth_idle_without_publish ~180 runs. Strengthened docs/human_oauth_checklist.md with an ONLY ACTION NEEDED banner at the top. Pure verification remains low-leverage. Prefer a small fix to an existing production tool or clarifying doc change that prevents rediscovery. Do not spend the run only restating that media is ready and secrets are absent. Do not poll secrets. Do not scaffold Q2. The human step remains docs/human_oauth_checklist.md (banner at top) or operator_card.py then the three secrets and one dispatch.

Run 451 note: oauth_idle_without_publish ~180 runs. Pure verification remains low-leverage. Prefer a small fix to an existing production tool or clarifying doc change that prevents rediscovery. Do not spend the run only restating that media is ready and secrets are absent. Do not poll secrets. Do not scaffold Q2. The human step remains docs/human_oauth_checklist.md or operator_card.py then the three secrets and one dispatch.

Run 447 note: oauth_idle_without_publish has persisted ~175 runs with zero published videos. Pure verification runs (materialize + gates + status note) have diminishing returns. Prefer a small fix to an existing production tool or a clarifying doc change that prevents rediscovery. Do not spend the run only restating that media is ready and secrets are absent. Do not poll secrets. Do not scaffold Q2. The human step remains docs/human_oauth_checklist.md or operator_card.py then the three secrets and one dispatch.

Run 390 note: idea_brief --queue puts that row's problem into why now. Q2 and Q3 lines differ. Do not scaffold Q2. Do not add a stall flag, compact check, card reprint, or recovery edge while videos published stay 0. The human step is still issue 1, then dispatch execute=true.

Run 381 note: `STALL_RECOVERY_EDGE` means the last four STATE deltas wired a provider-state recovery path while videos published stay 0. Do not add another recovery edge. Do not poll secrets. The human step is still the three Actions secrets, then dispatch execute=true.

Run 341 note: NEXT.md keeps 12 newest notes. Older notes are in docs/next_archive.md. Do not paste the archive back. Do not add a scanner while videos published stay 0. Next human step is the three Actions secrets, then dispatch execute=true.

Run 330 note: dry-run consent scopes are upload + force-ssl + analytics. Do not rediscover that. Do not add a scanner while videos published stay 0. Next human step is the three Actions secrets, then dispatch execute=true.

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

Targeted addition from Run 233:

- `tools/hint.py` build-cards must keep `card_generator.py --write-manifest` and must not tell operators to download stock.
- `tools/hint.py` edit must keep timeline/media_qa/assemble and must not restore "do not write an ffmpeg recipe here".
- Do not keep aligning remaining record-vo printers unless a proven omission blocks the drop. Runs 231–232 already pointed hint/next_action/pipeline_status at `docs/gate_machine.md`.
- doctor.py inherits hint.commands_for; do not map doctor.py to add a second copy of those strings.

Targeted addition from Run 137:

- `docs/narration.md` names `videos/NNN-slug/vo/NNN-slug-take-selected.wav` at the top of Where files live and states repo-root `vo/` is not Selected VO.
- `tools/selftest.py` source-checks that narration.md keeps the DROP line.
- Do not invent a wav or card binaries. Do not bump ready_for_edit. Do not scaffold Q2. Do not add another wrapper CLI. Do not add WAVE 4. Do not upload.
- Do not spend the run adding another Q1 markdown stub or another operator/agent page that only restates NEXT.md.
- Do not re-implement selected_vo_drop in a second module.
- Next value is a real selected take at `videos/002-stop-deciding-what-to-work-on-every-morning/vo/002-stop-deciding-what-to-work-on-every-morning-take-selected.wav`, or an explicit human TTS policy.

Targeted addition from Run 136:

- `docs/format.md` names `videos/NNN-slug/vo/NNN-slug-take-selected.wav` and states repo-root `vo/` is not Selected VO.
- `tools/selftest.py` source-checks that hint.py does not redefine `selected_vo_drop` / `selected_vo_path`, and that format.md keeps the DROP line.

Targeted addition from Run 135:

- `tools/selftest.py` source-checks that VO printers import `render_brief.selected_vo_drop` and that `set_status.py` does not redefine it.
- `docs/editor.md` names `videos/NNN-slug/vo/NNN-slug-take-selected.wav`.

Targeted addition from Run 134:

- `tools/caption_brief.py` imports `selected_vo_drop()`. Generated captions.md prints `DROP videos/NNN-slug/vo/NNN-slug-take-selected.wav`. Export names and the Human box use the same helper.

Targeted addition from Run 133:

- `tools/qa_checklist.py` imports `selected_vo_drop()`. Generated qa.md Notes print DROP.

Targeted addition from Run 132:

- `tools/vo_session.py` imports `render_brief.selected_vo_drop()`. Generated vo_session.md prints DROP. Record-to uses the same helper.

Targeted addition from Run 131:

- `tools/render_brief.selected_vo_drop()` is the shared Selected VO path helper. pipeline_status and next_action import it. Generated render.md prints DROP. Table rows stay packet-relative.

Targeted addition from Run 130:

- tools/pipeline_status.py missing-VO packets print `DROP videos/NNN-slug/vo/NNN-slug-take-selected.wav`. Repo-root `vo/` is not Selected VO. This includes legal ready_for_vo (not only status-ahead-of-vo drift).

Targeted addition from Run 121:

- Selected VO is packet-relative only: `videos/NNN-slug/vo/NNN-slug-take-selected.wav` (or .flac, optional `-v2`). Repo-root `vo/` is ignored by `render_brief` / `set_status`.

Targeted addition from Run 110:

- hint.py write-script/expand-script Command must keep the empty-draft Target comment.
- Do not map doctor.py. Do not strip that comment.

Targeted addition from Run 109:

- `docs/human_session.md` step 3 must keep the empty-script Target column.

Targeted addition from Run 104:

- Do not touch needed.py reconstruct / WAVE 3 / doctor mapping unless a new READY lie is proven.
- Do not rewrite writer prompts again unless words.py on this draft misses 900-1500.

Targeted addition from Run 081:

- After a GitHub write of a high-risk tool, run `python3 tools/prove_locks.py` first.
- Do not map words.py, words_contract.py, placeholder_guard.py, or prove_locks.py.


## 24-hour manual-intervention escalation

Before treating any manual gate as permanent, read `docs/operator_escalation.md`. Each new human request has one recorded UTC start time and a 24-hour deadline. Before the deadline: read-only on that blocker. After the deadline: use the granted repository/local permissions to complete the smallest safe allowed fallback, without inventing human evidence. Never create repeated hold/status commits merely because the daily check ran.

When the only unresolved dependency is a provider credential/token/secret, finish and validate all repository-side infrastructure first and leave that credential as the last manual bottleneck.

## YouTube readiness

Read `docs/youtube_integration.md` before adding any upload capability. Build and validate the integration without credentials where possible. Fail closed at `YOUTUBE_AUTH_REQUIRED` when OAuth material is absent. Never commit or print secrets. Do not confuse an API key with upload authorization; YouTube uploads use OAuth 2.0 authorization.

## Anti-slop quality

For all new or rewritten content, read docs/content_quality.md. The goal is specific, original, useful editorial writing, not imitation of “human” quirks. Do not add fake anecdotes, testimonials, mistakes, slang, or unverifiable experience. Do not pad word count. Before promoting a script, perform the quality/originality test and read it aloud for repetitive phrasing and cadence.
## End-to-end capability progression

When a manual intervention request has either been satisfied or has crossed its 24-hour escalation deadline, do not stop after merely clearing the old blocker. Inspect `docs/production_capabilities.md` and advance the smallest missing capability needed to move the live packet toward a genuinely completed video.

Priority order:
1. narration validation/adapter;
2. deterministic card/visual generation;
3. deterministic render/assembly;
4. full media QA;
5. credential-ready YouTube uploader;
6. YouTube Analytics + comment feedback ingestion;
7. experiment/improvement loop.

A scheduled run may build one small capability increment, validate it, and stop. Do not create placeholder “done” files. Do not declare automation or self-improvement complete while required capabilities are NOT_BUILT.

After publication, collect a defined observation window, preserve source/timestamp/video-ID provenance, and convert repeated viewer needs or consistent metrics into explicit hypotheses rather than blindly rewriting content.

If the only remaining external blocker is YouTube authentication, finish the surrounding uploader/feedback infrastructure and stop at `YOUTUBE_AUTH_REQUIRED`. Credentials remain the final manual bottleneck.

## Executive YouTube manager review

After the operational/unstick check, act as the admin YouTube manager and perform one big-picture trajectory decision using docs/executive_manager.md.

For the current pre-publication state, default to SHIP: prioritize completing the first valid video over adding more governance. Move to BUILD only when a missing capability directly blocks completion; SIMPLIFY when machinery is growing without output; PIVOT only when evidence supports changing a material assumption; HOLD only for a genuine external dependency.

Record evidence and the primary decision, but do not create a daily commit just to log an unchanged decision. A decision should produce repository change only when it changes the next action, capability priority, or channel-process policy.

Targeted addition from Run 360:

- Do not add another OAuth exchange parser. `next_compact.py` must keep one Active locks block. The human step is the three GitHub Actions secrets.

Targeted addition from Run 382:

- Do not add another provider-state recovery edge. `python3 tools/recovery_freeze.py` fails if `youtube-production.yml` has a second `provider-upload-state` artifact or a second `persist_provider_state.py recover` call. A lock sentence does not clear that failure. The human step is still the three GitHub Actions secrets.


Targeted addition from Run 387:

- `tools/record_run.py` refreshes the single NEXT `Updated:` line from the note. Do not leave that header on an older run. Do not add a freeze module for it. Do not poll secrets. The human step is still issue 1, then dispatch execute=true.
