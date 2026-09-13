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
51aq. idea_brief --queue reprints paste before scaffold — **done (Run 095)**
51ar. idea_brief_contract locks --queue — **done (Run 096)**
51as. queue_status / next_topic print --queue; queue_contract locks it — **done (Run 097)**
51at. doctor all-packet Queue next footer; queue_contract locks it — **done (Run 098)**
51au. needed.py --plan WAVE 3 prints doctor then board printers; doctor stays unmapped — **done (Run 099)**
51av. needed.py --plan WAVE 3 reconstructs unmapped doctor.py before running it — **done (Run 100)**
51aw. needed.py doctor.py lists imports so READY means doctor can import — **done (Run 101)**
51ax. needed.py doctor.py reconstruct lists next_topic.py so READY means WAVE 3 start can run — **done (Run 102)**
51ay. needed.py alias appends asked file so next_topic READY does not lie — **done (Run 103)**
51az. Writer prompts name first-draft spoken-word allocation — **done (Run 104)**
51ba. Packet template includes draft.md save target — **done (Run 105)**

## Later (automation)
52. Human scaffolds Q1, pastes idea fields, overwrites copied draft.md, and lands WORDS in band on a non-fixture packet
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
- Another idea_brief flag unless --queue regresses
- Mapping idea_brief.py or idea_brief_contract.py or doctor.py
- Printing --queue for mark-needed rows
- Printing doctor Queue next on a single-packet doctor invocation
- Wrapping doctor in start.py
- Another needed.py reconstruct path unless a READY lie is proven
- Another writer-prompt rewrite unless the first real draft misses 900–1500
- A second draft template or a Band-landing reprint CLI
