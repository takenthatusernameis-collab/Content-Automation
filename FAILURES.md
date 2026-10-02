# FAILURES

## Run 261 — caption timing left as a blank task
- **Tried:** Runs 254-260 kept restating the publish hold. captions.md still said do not invent an SRT, so every future video would need a human to time 900+ words.
- **Result:** caption_align.py writes a labeled draft from the DROP wav. Q1 captions.srt exists. Approval stays unchecked.
- **Avoid:** Calling the draft Whisper or uploaded captions. Checking publish boxes from an agent run. Another run that only reprints the hold.

## Run 260 — compose instruction survived on the human pages
- **Tried:** Run 259 updated next_action and hint, then left gate_machine, human_session, agent_session, HANDOFF, and pipeline_status telling the operator to delete `No upload happened`.
- **Result:** Those surfaces now name the two open boxes and forbid restoring the stub. publish_brief refuses the Q1 packet.
- **Avoid:** Another printer-only pass that does not change the human action. Checking the boxes from an agent run. Restoring the stub. Flag if Runs 261+ only restate this hold.

## Run 259 — stub description treated as a compose task
- **Tried:** Runs 254–258 kept telling the operator to delete `No upload happened` and write the description. The script, title, tags, and pin draft already existed. That loop did not move the packet.
- **Result:** Description is now a drafted viewer paragraph. Open boxes stay unchecked so approval is still human. next_action must not tell the operator to delete a sentence that is gone.
- **Avoid:** Restoring the stub sentence. Checking Description edited or First comment approved from an agent run. Another printer-only run while those boxes are the remaining human edit.

## Run 257 — front door still said record
- **Tried:** Treating the truncated-master copy fix as enough. human_session and agent_session still said remaining labor is the DROP file, so the next agent would synthesize again.
- **Result:** Those pages and Q1 next_action now point at the publish.md review.
- **Avoid:** Restoring "remaining labor is a new recording" while q1-media-r249 and q1-media-r253 exist.

Earlier failures remain in force in prior commits.
