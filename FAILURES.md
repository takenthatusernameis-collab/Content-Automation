# FAILURES

## Run 259 — stub description treated as a compose task
- **Tried:** Runs 254–258 kept telling the operator to delete `No upload happened` and write the description. The script, title, tags, and pin draft already existed. That loop did not move the packet.
- **Result:** Description is now a drafted viewer paragraph. Open boxes stay unchecked so approval is still human. next_action must not tell the operator to delete a sentence that is gone.
- **Avoid:** Restoring the stub sentence. Checking Description edited or First comment approved from an agent run. Another printer-only run while those boxes are the remaining human edit.

## Run 257 — front door still said record
- **Tried:** Treating the truncated-master copy fix as enough. human_session and agent_session still said remaining labor is the DROP file, so the next agent would synthesize again.
- **Result:** Those pages and Q1 next_action now point at the publish.md review.
- **Avoid:** Restoring "remaining labor is a new recording" while q1-media-r249 and q1-media-r253 exist.

Earlier failures remain in force in prior commits.
