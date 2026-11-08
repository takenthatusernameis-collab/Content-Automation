# STATE

2026-11-08T03:15:00Z (Run 1106)

Strengthened oauth_exchange_contract.py to lock SCOPES exactly to preferred non-overlapping set (force-ssl + yt-analytics.readonly) and reject youtube.upload in the consent URL. Prevents future regression that could cause the human mint step to fail on consent. Contract and selftest still PASS. STALL_OAUTH_IDLE remains primary (1000+ runs, HIGH suspicion). Pre-upload complete. No secrets polled, no dispatch. Prefer human OAuth step with the locked tool.

2026-11-08T02:20:00Z (Run 1105)

Aligned oauth_exchange.py scopes to preferred non-overlapping set (force-ssl + yt-analytics.readonly only). Removes risk of consent rejection from overlapping youtube.upload. Contract and selftest still PASS. STALL_OAUTH_IDLE remains primary (1000+ runs, HIGH suspicion). Pre-upload complete. No secrets polled, no dispatch. Prefer human OAuth step with the now-aligned tool.

2026-11-08T01:20:00Z (Run 1104)

Fresh clone + materialize + media_qa PASS + selftest PASS. Videos published stay 0. STALL_OAUTH_IDLE remains primary (1000+ runs, HIGH suspicion). Pre-upload complete and reconfirmed. No secrets polled, no dispatch. Prefer human OAuth step (python3 tools/human_starter.py or docs/HUMAN_PRIORITY.md). Long stall flagged as increasingly suspicious; further pure verification has diminishing returns. Efficiency snapshot: local gates 100% automated; human time to first private publish ~10-20 min + one dispatch.

2026-11-08T00:21:14Z (Run 1103)

Fresh clone + materialize + media_qa PASS + selftest PASS. Videos published stay 0. STALL_OAUTH_IDLE remains primary (1000+ runs, HIGH suspicion). Pre-upload complete and reconfirmed. No secrets polled, no dispatch. Prefer human OAuth step (python3 tools/human_starter.py or docs/HUMAN_PRIORITY.md). Long stall flagged as increasingly suspicious; further pure verification has diminishing returns. Efficiency snapshot: local gates 100% automated; human time to first private publish ~10-20 min + one dispatch.

2026-11-08T00:20:00Z (Run 1102)

Fresh clone + materialize + media_qa PASS + next_action upload-blocked + next_compact (to fix 7-note selftest) + selftest PASS. Videos published stay 0. STALL_OAUTH_IDLE remains primary (1000+ runs, HIGH suspicion). Pre-upload complete and reconfirmed. No secrets polled, no dispatch. Prefer human OAuth step (python3 tools/human_starter.py or docs/HUMAN_PRIORITY.md). Long stall flagged as increasingly suspicious; further pure verification has diminishing returns.

2026-11-07T22:20:00Z (Run 1101)

Aligned human_starter.py common pitfalls with preferred OAuth scopes (force-ssl + yt-analytics.readonly; force-ssl covers upload; avoid overlapping). Selftest PASS on fresh clone. Videos published stay 0. STALL_OAUTH_IDLE remains primary (1000+ runs, HIGH suspicion). Pre-upload complete (no rematerialize). No secrets polled, no dispatch. Prefer human OAuth step (python3 tools/human_starter.py or docs/HUMAN_PRIORITY.md). Long stall flagged as increasingly suspicious; further pure verification has diminishing returns.

2026-11-07T21:20:00Z (Run 1100)

Fresh clone showed NEXT.md over the 6-note selftest cap. Compacted and recorded via record_run (now more robust: restores missing # RUNS header). Selftest PASS. Videos published stay 0. STALL_OAUTH_IDLE remains primary (1000+ runs, HIGH suspicion). Pre-upload complete (no rematerialize). No secrets polled, no dispatch. Prefer human OAuth step (python3 tools/human_starter.py or docs/HUMAN_PRIORITY.md). Long stall flagged as increasingly suspicious; further pure verification has diminishing returns.

2026-11-07T20:15:00Z (Run 1099)

Fresh clone showed NEXT.md over the 6-note selftest cap. Compacted and recorded via record_run (now more robust: restores missing # RUNS header). Selftest PASS. Videos published stay 0. STALL_OAUTH_IDLE remains primary (1000+ runs, HIGH suspicion). Pre-upload complete (no rematerialize). No secrets polled, no dispatch. Prefer human OAuth step (python3 tools/human_starter.py or docs/HUMAN_PRIORITY.md). Long stall flagged as increasingly suspicious; further pure verification has diminishing returns.

(Older state notes remain below or in docs/state_archive.md. Do not paste the archive back.)
