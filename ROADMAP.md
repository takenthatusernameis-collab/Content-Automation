# ROADMAP

## Next (assisted production)
31–51n. Queue through write_path apply locks — **done (Runs 027–066; body restored Run 067)**
51o–51aj. Write-path / words / prove_locks / printer + page alignment — **done (Runs 067–088)**
51ak. idea_brief --block pastes the full idea.md template — **done (Run 089)**
51al. expand_prompt prints Idea locks — **done (Run 090)**
51am. apply_script dry-run prints idea-lock INFO — **done (Run 091)**
51an. idea_lock.py prints the same INFO — **done (Run 092)**
51ao. words.py prints the same idea-lock INFO — **done (Run 093)**
51ap. words_contract locks IN BAND --strict exit 0 with INFO present — **done (Run 094)**

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
- Making apply or words idea-lock INFO a BLOCKED error or --strict FAIL
- Another primary run whose only change is naming idea_brief on one more page
- Another wrapper CLI around idea_lock_notes
- Dropping the words.py import fallback
- Another words.py contract case unless the printer regresses
