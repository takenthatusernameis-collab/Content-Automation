# NEXT RUN PROMPT

## Absolute no-op gate while OPERATOR_HOLD is active

Before doing anything else, inspect `OPERATOR_HOLD.md`. If it is active and the packet-relative Selected VO file is still missing, this run is complete after read-only inspection. **Do not modify any repository file and do not create a commit.** This includes `STATE.md`, `NEXT.md`, `RUNS.md`, prompts, logs, documentation, tests, lock files, and generated outputs. Do not “log the hold,” refresh timestamps, restate the blocker, or make any other bookkeeping change. A scheduled run that creates a commit under this condition is a failed/non-productive run.

A write is permitted only if at least one of these is true:

1. the real Selected VO file now exists at the packet-relative path;
2. the blocker materially changed;
3. a genuine regression prevents the already-defined next action; or
4. a human explicitly changed the policy.

If none is true, report the current blocker out-of-band and exit with no repository write.

Keep the original master prompt unchanged.

**Hard-stop addition from Run 184:**

- If `OPERATOR_HOLD.md` is active and the packet-relative Selected VO file is still missing, the run must be **read-only**: inspect state, report the blocker, and make **no repository changes and no commit**. Do not refresh `STATE.md`, `NEXT.md`, `RUNS.md`, or any other hold-status snapshot merely to record that the hold still exists.
- A new commit is permitted only when the hold condition changes (for example, a real selected VO file is supplied), a genuine regression prevents the already-defined next action, or a human explicitly changes the policy.
- Repeatedly re-asserting the same hold is non-productive churn and must be treated as a failed run, not as progress.

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