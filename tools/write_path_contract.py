#!/usr/bin/env python3
"""Contract check for the non-fixture write path.

Temp tree only. Never writes videos/ or sample-001.
Locks apply_script refuse/allow and set_status evidence gates so later
runs cannot silently regress the dry-run-default write tools.
Also locks missing --from path messaging (draft.md convention),
the apply_script CLI exit 2 for a missing --from file,
the advertised dry-run CLI for an existing PATH/draft.md
(exit 0, Dry-run only, no script.md write),
the advertised set_status CLI for ready_for_vo
(duration block and fixture block leave packet.md unchanged,
including when --write is passed on a blocked target),
the advertised apply_script CLI --write against the fixture
(exit 1, BLOCKED, script.md unchanged),
and the advertised non-fixture apply_script CLI
(--refresh without --write writes nothing;
--write replaces script.md only;
--write --refresh replaces script.md and refreshes
expand.md / vo_session.md / captions.md; packet.md stays draft).
"""
