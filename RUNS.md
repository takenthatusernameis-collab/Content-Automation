# RUNS

## Run 1114 — 2026-11-08T11:20:00Z
- Objective: Reduce time-to-recovery on the remaining human OAuth step by adding structured hints for common failure modes.
- Action: Created tools/oauth_recovery_hints.py (prints cause + fix for scope rejection, test-user block, missing refresh_token, secret-set mistakes, incomplete post-upload). Linked from oauth_step_checklist.py and human_starter.py. Confirmed materialize + media_qa PASS + next_action=upload-blocked on this clone. No secrets polled, no dispatch. Updated state files.
- Result: Recovery tool available. Checklist and starter now point to it. All local gates remain PASS. Videos published stay 0. Pre-upload path unchanged. Efficiency: local automation 100%; remaining human ~10-20 min + dispatch; recovery hints reduce rediscovery of fixes.
- Verification: File created, syntax checked with py_compile, executable, runs cleanly. References inserted and syntax-checked. Soft only; no hard gates changed.
- Discovery: STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable. Common pitfalls were documented but lacked a dedicated recovery printer.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py or python3 tools/oauth_step_checklist.py or python3 tools/oauth_recovery_hints.py if needed, then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1113 — 2026-11-08T10:15:28Z
- Objective: Further reduce navigation friction on the longest part of the remaining human OAuth step by adding direct deep links to Google Cloud console pages inside the existing checklist tool.
- Action: Updated tools/oauth_step_checklist.py to print exact console URLs for API enablement, consent screen, and credentials/Desktop client creation. No secrets polled, no dispatch. Updated state files.
- Result: Checklist now includes copy-paste deep links. Complements human_starter.py and human_oauth_checklist.md. All local gates remain PASS. Videos published stay 0. Pre-upload path unchanged. Efficiency: local automation 100%; remaining human ~10-20 min + dispatch; deep links reduce rediscovery of console navigation.
- Verification: File updated and committed. Soft only; no hard gates changed.
- Discovery: STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable. Console navigation was the remaining friction point after the basic checklist existed.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py or python3 tools/oauth_step_checklist.py then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1112 — 2026-11-08T09:19:06Z
- Objective: Reduce rediscovery and missed steps on the remaining human OAuth action by adding a checkbox-style checklist tool.
- Action: Created tools/oauth_step_checklist.py (prints ordered checkboxes for Google Cloud setup, mint, secrets, single dispatch, success criteria). No secrets polled, no dispatch. Updated state files.
- Result: Checklist tool available for the human. Complements existing human_starter.py and human_oauth_checklist.md. All local gates remain PASS. Videos published stay 0. Pre-upload path unchanged. Efficiency: local automation 100%; remaining human ~10-20 min + dispatch; new tool reduces missed pitfalls.
- Verification: File created, syntax checked with py_compile, executable. Soft only; no hard gates changed.
- Discovery: STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable. A structured checklist was missing despite detailed docs.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py or python3 tools/oauth_step_checklist.py then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.


## Run 1111 — 2026-11-08T08:21:00Z
- Objective: Reduce future human labor when starting the next video after an experiment decision by adding a reusable direction skeleton tool.
- Action: Created tools/next_from_decision.py (reads filled experiment_decision.json; prints keep/discard/retest next-topic skeleton; no invent). Updated tools/post_publish_sequence.py to recommend it after validating a decision. No secrets polled, no dispatch. Updated state files.
- Result: next_from_decision.py available for post-decision use. post_publish_sequence.py now surfaces it. All local gates remain PASS. Videos published stay 0. Pre-upload path unchanged. Efficiency: local automation 100%; remaining human ~10-20 min + dispatch; new tool reduces rediscovery of next-topic structure.
- Verification: File created and committed; post_publish_sequence.py updated and committed. Soft only; no hard gates changed.
- Discovery: STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable. Post-publish experiment path now has a next-video bridge.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py (now includes validator + next_from_decision). When a decision exists, run next_from_decision.py before scaffolding the next packet.

## Run 1110 — 2026-11-08T07:23:00Z
- Objective: Reduce future human error on the post-publish experiment decision step by surfacing the existing experiment_template_validator.py inside the ordered post-publish sequence.
- Action: Cloned repository. Updated tools/post_publish_sequence.py to recommend the validator after filling experiment_baseline.json and experiment_decision.json. Confirmed validator still correctly rejects templates. No secrets polled, no dispatch. Updated state files.
- Result: post_publish_sequence.py now guides the human to validate filled experiment files before committing them. All local gates remain PASS. Videos published stay 0. Pre-upload path unchanged. Efficiency: local automation 100%; remaining human ~10-20 min + dispatch; validator reduces rediscovery of load rules.
- Verification: post_publish_sequence.py syntax ok; validator FAILs templates as expected (exit 1). No regressions.
- Discovery: STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable. Sequence printer now points to the validator added in Run 1109.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py (now includes validator step). When metrics exist, fill templates and run the validator before committing.

# RUNS

## Run 1109 — 2026-11-08T06:30:00Z
- Objective: Confirm system health on fresh clone and add a reusable validator that reduces future human error when filling experiment baseline/decision files after the first publish.
- Action: Cloned repository. Ran materialize_q1_release.py (success). Ran media_qa.py (PASS). Confirmed next_action upload-blocked. Created tools/experiment_template_validator.py and updated the two templates with a usage note. No secrets polled, no dispatch. Updated state files via record_run.
- Result: All local gates PASS. Videos published stay 0. Pre-upload path unchanged and verified. New validator available for when a real comparison exists. Efficiency: local automation 100%; remaining human ~10-20 min + dispatch.
- Verification: materialize exit 0; media_qa PASS; next_action upload-blocked; validator correctly FAILs the templates (expected).
- Discovery: STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable. Decision/baseline templates lacked a local pre-check against the load rules.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py. When metrics exist, fill templates and run the new validator before committing.

## Run 1108 — 2026-11-08T05:16:26Z
- Objective: Confirm system health on fresh clone and add a small reusable post-publish template that reduces future human error on experiment decisions.
- Action: Cloned repository. Ran materialize_q1_release.py (success). Ran media_qa.py (PASS). Ran selftest.py (PASS). Created docs/experiment_decision.template.json matching the load_decision contract. No secrets polled, no dispatch. Updated state files.
- Result: All local gates PASS. Videos published stay 0. Pre-upload path unchanged and verified. New template available for when a real comparison exists. Efficiency: local automation 100%; remaining human ~10-20 min + dispatch.
- Verification: materialize exit 0; media_qa PASS; selftest.py exit 0; template JSON valid.
- Discovery: STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable. Decision template was missing while baseline template existed.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py. When metrics exist, use the new decision template.

## Run 1107 — 2026-11-08T06:20:00Z
- Objective: Confirm current system health on fresh clone (materialize + media_qa + selftest), record continued OAuth stall with efficiency snapshot for future runs, and leave clear handoff without adding low-leverage artifacts.
- Action: Cloned repository. Ran materialize_q1_release.py (success). Ran media_qa.py (PASS). Ran selftest.py (PASS). No secrets polled, no dispatch. Updated state files.
- Result: All local gates PASS. Videos published stay 0. Pre-upload path unchanged and verified. Efficiency: local automation 100%; remaining human ~10-20 min + dispatch. Estimated savings: future runs start from green confirmed path.
- Verification: materialize exit 0; media_qa PASS; selftest.py exit 0. Soft documentation only. No regressions.
- Discovery: STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable. Further pure verification has diminishing returns.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1106 — 2026-11-08T03:15:00Z
- Objective: Lock the preferred non-overlapping OAuth scopes in the exchange contract so a future change cannot reintroduce consent-rejection risk on the remaining human step.
- Action: Updated tools/oauth_exchange_contract.py to require set(SCOPES) == {force-ssl, analytics.readonly} and to fail if youtube.upload appears in the consent URL. Ran contract PASS and selftest PASS. No secrets, no dispatch, no media writes.
- Result: Scope lock is now enforced by the contract. Human mint step is more resistant to regression. All local gates still PASS. Videos published stay 0.
- Verification: oauth_exchange_contract.py exit 0; selftest.py exit 0.
- Discovery: Previous contract only checked presence, not exact preferred set; overlapping scope could have been re-added without detection.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall remains HIGH suspicion.
- Recommended next: human step (python3 tools/human_starter.py or docs/HUMAN_PRIORITY.md then mint with the locked tool + secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)

Permanent log. Newest first.
