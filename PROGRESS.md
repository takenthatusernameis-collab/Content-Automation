# PROGRESS

## Efficiency ledger

| When | Human min / video | Automated steps | Notes |
|------|-------------------|-----------------|-------|
| 2026-09-14 Run 137 | ~11 estimate | 85 | narration.md DROP + selftest page lock; VO still human |
| 2026-09-19 Run 213 | ~10 estimate | 86 | narration_adapter + labeled generated fallback after 24h; take still local-only |

These numbers are **estimates**, not stopwatch data. Earlier rows remain in prior commits.

## Capability additions
- Run 213: `tools/narration_adapter.py` extracts WORDS, inspects a packet-relative take, writes `vo_origin.md`. Q1 origin labeled generated after deadline. Workspace TTS MP3 not committed. Status stayed ready_for_vo. Narration capability: READY_FOR_MEDIA.
- Run 137: `docs/narration.md` names the repo-root DROP. `tools/selftest.py` fails if narration.md drops the DROP line. No new CLI. No wav. Status stayed ready_for_vo.
