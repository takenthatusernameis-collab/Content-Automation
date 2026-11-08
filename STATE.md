# STATE

2026-11-08T09:18:57Z (Run 1112)

Added tools/oauth_step_checklist.py (checkbox-style printable checklist for the exact human OAuth sequence; reduces rediscovery of steps and pitfalls). STALL_OAUTH_IDLE remains primary (1000+ runs, HIGH suspicion). Pre-upload complete and reconfirmed. No secrets polled, no dispatch. Prefer human OAuth step (python3 tools/human_starter.py or the new checklist or docs/HUMAN_PRIORITY.md). Long stall flagged as increasingly suspicious; further pure verification has diminishing returns. Efficiency snapshot: local gates 100% automated; human time to first private publish ~10-20 min + one dispatch. New checklist tool reduces missed steps on the remaining human action.

# STATE

2026-11-08T08:21:00Z (Run 1111)

Added tools/next_from_decision.py (prints a next-video direction skeleton from a filled experiment_decision.json; keep/discard/retest only; no invent). Updated post_publish_sequence.py to recommend it after validating a decision. Reduces future human labor when starting the next packet after learning. STALL_OAUTH_IDLE remains primary (1000+ runs, HIGH suspicion). Pre-upload complete and reconfirmed. No secrets polled, no dispatch. Prefer human OAuth step (python3 tools/human_starter.py or docs/HUMAN_PRIORITY.md). Long stall flagged as increasingly suspicious; further pure verification has diminishing returns. Efficiency snapshot: local gates 100% automated; human time to first private publish ~10-20 min + one dispatch. New tool reduces rediscovery of next-topic structure after a decision.

# STATE

2026-11-08T07:23:00Z (Run 1110)

Updated post_publish_sequence.py to recommend experiment_template_validator.py after filling baseline and decision files. Reduces future human error on the post-publish experiment step. Fresh clone confirms materialize path still valid. STALL_OAUTH_IDLE remains primary (1000+ runs, HIGH suspicion). Pre-upload complete and reconfirmed. No secrets polled, no dispatch. Prefer human OAuth step (python3 tools/human_starter.py or docs/HUMAN_PRIORITY.md). Long stall flagged as increasingly suspicious; further pure verification has diminishing returns. Efficiency snapshot: local gates 100% automated; human time to first private publish ~10-20 min + one dispatch. Validator now surfaced in the post-publish sequence.

2026-11-08T06:30:00Z (Run 1109)

Fresh clone + materialize + media_qa PASS + next_action=upload-blocked. Added tools/experiment_template_validator.py (validates filled baseline/decision JSON against load rules; correctly rejects templates). Templates updated with usage note. STALL_OAUTH_IDLE remains primary (1000+ runs, HIGH suspicion). Pre-upload complete and reconfirmed. No secrets polled, no dispatch. Prefer human OAuth step (python3 tools/human_starter.py or docs/HUMAN_PRIORITY.md). Long stall flagged as increasingly suspicious; further pure verification has diminishing returns. Efficiency snapshot: local gates 100% automated; human time to first private publish ~10-20 min + one dispatch. New validator reduces future post-publish human error.

2026-11-08T05:16:26Z (Run 1108)

Fresh clone + materialize + media_qa PASS + selftest PASS. Added docs/experiment_decision.template.json (mirrors baseline template; reduces post-publish human error when recording keep/discard/retest). Videos published stay 0. STALL_OAUTH_IDLE remains primary (1000+ runs, HIGH suspicion). Pre-upload complete and reconfirmed. No secrets polled, no dispatch. Prefer human OAuth step (python3 tools/human_starter.py or docs/HUMAN_PRIORITY.md). Long stall flagged as increasingly suspicious; further pure verification has diminishing returns. Efficiency snapshot: local gates 100% automated; human time to first private publish ~10-20 min + one dispatch.

2026-11-08T06:20:00Z (Run 1107)

Fresh clone + materialize + media_qa PASS + selftest PASS. Videos published stay 0. STALL_OAUTH_IDLE remains primary (1000+ runs, HIGH suspicion). Pre-upload complete and reconfirmed. No secrets polled, no dispatch. Prefer human OAuth step (python3 tools/human_starter.py or docs/HUMAN_PRIORITY.md). Long stall flagged as increasingly suspicious; further pure verification has diminishing returns. Efficiency snapshot: local gates 100% automated; human time to first private publish ~10-20 min + one dispatch.

2026-11-08T03:15:00Z (Run 1106)

Strengthened oauth_exchange_contract.py to lock SCOPES exactly to preferred non-overlapping set (force-ssl + yt-analytics.readonly) and reject youtube.upload in the consent URL. Prevents future regression that could cause the human mint step to fail on consent. Contract and selftest still PASS. STALL_OAUTH_IDLE remains primary (1000+ runs, HIGH suspicion). Pre-upload complete. No secrets polled, no dispatch. Prefer human OAuth step with the locked tool.

2026-11-08T02:20:00Z (Run 1105)

Aligned oauth_exchange.py scopes to preferred non-overlapping set (force-ssl + yt-analytics.readonly only). Removes risk of consent rejection from overlapping youtube.upload. Contract and selftest still PASS. STALL_OAUTH_IDLE remains primary (1000+ runs, HIGH suspicion). Pre-upload complete. No secrets polled, no dispatch. Prefer human OAuth step with the now-aligned tool.

2026-11-08T01:20:00Z (Run 1104)

Fresh clone + materialize + media_qa PASS + selftest PASS. Videos published stay 0. STALL_OAUTH_IDLE remains primary (1000+ runs, HIGH suspicion). Pre-upload complete and reconfirmed. No secrets polled, no dispatch. Prefer human OAuth step (python3 tools/human_starter.py or docs/HUMAN_PRIORITY.md). Long stall flagged as increasingly suspicious; further pure verification has diminishing returns. Efficiency snapshot: local gates 100% automated; human time to first private publish ~10-20 min + one dispatch.

(Older state notes remain below or in docs/state_archive.md. Do not paste the archive back.)
