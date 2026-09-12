# ROADMAP

## Next (assisted production)
31–51n. Queue through write_path apply locks — **done (Runs 027–066; body restored Run 067)**
51o. write_path_contract locks in-band set_status ready_for_vo — **done (Run 067)**
51p. Separate source-shape lock for write_path_contract.py — **done (Run 068)**
51q. contract_shape trio (apply_script + set_status) — **done (Run 069)**
51r. One-command verify_write_path order lock — **done (Run 070)**
51s. Read-only words.py band check on draft.md — **done (Run 071)**
51t. words.py Delta + Next + import fallback — **done (Run 072)**
51u. words.py Hook Delta (20-35) — **done (Run 073)**
51v. words.py Beats + Thin (per-heading counts) — **done (Run 074)**
51w. words.py Grow (one heading first) — **done (Run 075)**
51x. words.py Cut (one heading first when ABOVE) — **done (Run 076)**
51y. words_contract.py lock for words.py — **done (Run 077)**
51z. placeholder_guard.py lock for emptied high-risk tools — **done (Run 078)**
51aa. prove_locks.py one-command post-write order wrapper — **done (Run 079)**
51ab. NEXT_RUN_PROMPT names prove_locks first — **done (Run 080)**
51ac. placeholder_guard witnesses prove_locks.py — **done (Run 081)**

## Later (automation)
52. Human scaffolds Q1, pastes idea fields, and lands WORDS in band on a non-fixture packet
53. TTS narration path (optional)
54. Caption timing from a real selected take
55. ffmpeg assembly after one packet has VO + cards
56. YouTube upload after packet QA passes

## Not yet
- Auto-scaffolding Q1
- Auto-writing idea.md
- WAVE 4
- Weakening write_path_contract CLI locks
- Replacing write_path_contract.py with a docstring-only file
- Dropping tools/contract_shape.py
- Dropping tools/verify_write_path.py or using it as a substitute for the two files it runs
- Treating words.py as a lock or as apply --write
- Mapping words.py, words_contract.py, placeholder_guard.py, or prove_locks.py in needed.py
- Treating words.py Delta, Hook Delta, Beats, Thin, Grow, or Cut as filler permission
- Making words.py --strict fail on hook length, thin headings, Grow, or Cut alone
- Treating PLACEHOLDER GUARD PASS or PROVE LOCKS PASS as apply --write
- Dropping tools/prove_locks.py or using it as a substitute for the three files it runs
- Adding another order wrapper around prove_locks.py
- Dropping the prove_locks.py check from placeholder_guard.py
