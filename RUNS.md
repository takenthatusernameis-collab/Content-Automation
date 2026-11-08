# RUNS

## Run 1106 — 2026-11-08T03:15:00Z
- Objective: Lock the preferred non-overlapping OAuth scopes in the exchange contract so a future change cannot reintroduce consent-rejection risk on the remaining human step.
- Action: Updated tools/oauth_exchange_contract.py to require set(SCOPES) == {force-ssl, analytics.readonly} and to fail if youtube.upload appears in the consent URL. Ran contract PASS and selftest PASS. No secrets, no dispatch, no media writes.
- Result: Scope lock is now enforced by the contract. Human mint step is more resistant to regression. All local gates still PASS. Videos published stay 0.
- Verification: oauth_exchange_contract.py exit 0; selftest.py exit 0.
- Discovery: Previous contract only checked presence, not exact preferred set; overlapping scope could have been re-added without detection.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall remains HIGH suspicion.
- Recommended next: human step (python3 tools/human_starter.py or docs/HUMAN_PRIORITY.md then mint with the locked tool + secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1105 — 2026-11-08T02:20:00Z
- Objective: Align the OAuth mint tool with the documented preferred scopes to reduce human-step failure risk from overlapping consent scopes.
- Action: Updated tools/oauth_exchange.py SCOPES to (force-ssl, analytics.readonly) only. Updated printed guidance. Ran oauth_exchange_contract.py PASS and selftest.py PASS. No secrets, no dispatch, no media writes.
- Result: Consent URL now requests only the preferred scopes. Risk of consent rejection from overlapping youtube.upload reduced. All local gates still PASS. Videos published stay 0.
- Verification: oauth_exchange_contract.py exit 0; selftest.py exit 0; URL inspection confirmed no youtube.upload scope.
- Discovery: oauth_exchange.py was requesting three scopes while docs and starter warned against overlapping; this could cause the sole remaining human step to fail on consent.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall remains HIGH suspicion.
- Recommended next: human step (python3 tools/human_starter.py or docs/HUMAN_PRIORITY.md then mint with the aligned tool + secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1104 — 2026-11-08T01:20:00Z
- Objective: Confirm current system health on fresh clone (materialize + media_qa + selftest), record continued OAuth stall with efficiency snapshot for future runs, and leave clear handoff without adding low-leverage artifacts.
- Action: Cloned repository. Ran materialize_q1_release.py (success). Ran media_qa.py (PASS). Ran selftest.py (PASS). No secrets polled, no dispatch. Updated state files.
- Result: All local gates PASS. Videos published stay 0. Pre-upload path unchanged and verified. Efficiency: local automation 100%; remaining human ~10-20 min + dispatch. Estimated savings: future runs start from green confirmed path.
- Verification: materialize exit 0; media_qa PASS; selftest.py exit 0. Soft documentation only. No regressions.
- Discovery: STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable. Further pure verification has diminishing returns.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1103 — 2026-11-08T00:21:14Z
- Objective: Confirm current system health on fresh clone (materialize + media_qa + selftest), record continued OAuth stall with efficiency snapshot for future runs, and leave clear handoff without adding low-leverage artifacts.
- Action: Cloned repository. Ran materialize_q1_release.py (success). Ran media_qa.py (PASS). Ran selftest.py (PASS). No secrets polled, no dispatch. Updated state files.
- Result: All local gates PASS. Videos published stay 0. Pre-upload path unchanged and verified. Efficiency: local automation 100%; remaining human ~10-20 min + dispatch. Estimated savings: future runs start from green confirmed path.
- Verification: materialize exit 0; media_qa PASS; selftest.py exit 0. Soft documentation only. No regressions.
- Discovery: STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable. Further pure verification has diminishing returns.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

## Run 1102 — 2026-11-08T00:20:00Z
- Objective: Confirm current system health on fresh clone including materialize path and selftest (with compact), record continued OAuth stall for future runs, and leave clear handoff without adding low-leverage artifacts.
- Action: Cloned repository. Ran materialize_q1_release.py (success). Ran media_qa.py (PASS). Ran next_action.py (upload-blocked). Detected NEXT.md over limit (7 notes). Ran next_compact.py (moved 1 note). Selftest now PASS. No secrets polled, no dispatch, no media writes beyond materialize. Updated state files via record_run.
- Result: All local gates PASS. Videos published stay 0. Pre-upload path unchanged and verified. Estimated savings: future runs start from green selftest and verified materialize path without rediscovery.
- Verification: materialize exit 0; media_qa PASS; next_action upload-blocked; next_compact OK; selftest.py exit 0. Soft documentation only. No regressions.
- Discovery: NEXT.md can drift over the selftest note cap between runs; compact must be part of recording. STALL_OAUTH_IDLE persists across 1000+ runs with no human progress on secrets. Pre-upload complete and stable after materialize. Further pure verification has diminishing returns.
- Blocker: STALL_OAUTH_IDLE (three GitHub Actions secrets absent). Do not poll. Long stall is suspicious and increasingly so after extreme duration (1000+ runs).
- Recommended next: human step (open docs/HUMAN_PRIORITY.md or python3 tools/human_starter.py then secrets + single execute=true dispatch). After id appears: python3 tools/human_success_check.py then python3 tools/post_publish_sequence.py.

(Older run logs remain in docs/runs_archive.md. Do not paste the archive back.)

Permanent log. Newest first.
