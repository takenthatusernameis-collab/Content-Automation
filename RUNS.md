# RUNS

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
