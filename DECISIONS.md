# DECISIONS

Format: date | decision | why | revisit when

- 2026-09-10 | needed.py --missing exits 0 even when files are absent | A reconstruct checker that fails the process looks like a broken session start; NOT READY is the signal | If a CI job is added that should fail on incomplete reconstruct
- 2026-09-10 | needed.py FALLBACK_ALIAS resolves edited-tool names when which_contract is missing | Clone-less agents fetch needed.py first; requiring the router file to resolve new_packet.py recreates the guess problem | If which_contract.MAP tool lists change
- 2026-09-09 | which_contract.py is the map of tool edit → contract command; it must not write videos/ or the queue | Four locks already existed; NEXT and agent_session were duplicating the map and would drift | If a fifth lock class is added, extend the map in which_contract.py instead of another paragraph in NEXT
- 2026-09-09 | queue_contract.py is the regression lock for the queue board; it must not write the repo | Run 031 codes and --strict exits are easy to break while editing queue_status; selftest.py only covers sample-001 | If queue format changes
- 2026-09-09 | queue_status --strict is opt-in; default exit stays 0 | A clean board used as session start must not look like a failed command | If a CI job is added that should always use --strict
- 2026-09-09 | queue_status.py is read-only and must not write the queue | Humans still scan the table against videos/ after scaffold; a writer-board would hide missing-folder mistakes | If a human later wants --write on the board (do not add without evidence)
- 2026-09-09 | new_packet prints mark_topic dry-run after scaffold but never calls --write | Looking up Q-id is leftover labor; auto-mark would hide a missing-folder mistake | If a human later wants a --mark flag on new_packet (do not add without evidence)
- 2026-09-09 | Shared queue helpers live in tools/queue_lib.py | next_id/slugify/parse drifted across three files in one run | If a second queue format is added
- 2026-09-09 | `mark_topic.py` is the only writer of topic-queue status; dry-run default; used requires a matching non-fixture folder | Hand-editing the status column after scaffold is recurring labor and easy to do before the folder exists | If a human wants auto-mark from new_packet (do not add without evidence; would couple a writer to scaffold)

Earlier decisions remain in force (see prior commits for the full list).
