# PROMPT EVOLUTION

Original prompt is frozen in `ORIGINAL_MASTER_PROMPT.md`.

## Observed issues (Run 001)
- Repo started empty; prompt assumes “inspect recent progress” — first run must bootstrap memory or it will loop on empty READMEs.
- Prompt asks for many status files; that is useful. Creating extra product ideas is not.
- No instruction to treat an empty repo as “create the operating system first.”

## Observed issues (Run 002)
- NEXT.md listed three items; doing all of them is fine if they are one capability (niche + intake + writer prompt).
- Private-repo clone over HTTPS failed in the agent sandbox (`could not read Username`). Use GitHub push tools, not `git clone`, for this repo.
- Full packet QA and idea intake have different success criteria. The master prompt does not distinguish them.

## Allowed changes
Recorded as proposals in `NEXT_RUN_PROMPT.md` only. Do not edit the original archive.
