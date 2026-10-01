# BLOCKED

External work is parked here so runs do not retry it blindly.

| Dependency            | Why needed                         | Simplest human setup                                      | Status   |
|-----------------------|------------------------------------|-----------------------------------------------------------|----------|
| Channel niche/brand   | Every template depends on it       | Confirm or replace `docs/channel.md`                      | temporary default set |
| YouTube Data API OAuth| Upload, titles, analytics          | Cloud project + OAuth client + token file documented      | not started |
| TTS or microphone VO  | Narration audio                    | Record to `videos/NNN-slug/vo/NNN-slug-take-selected.wav` (or .flac). Repo-root `vo/` is not Selected VO. Optional local TTS only if a human names that policy. | path convention locked packet-relative (Runs 121-123); no vendor; no wav in repo |
| Stock / original media| B-roll and thumbs                  | Decide “text-card + public-domain” vs licensed stock; card names live in packet `assets.md` and `docs/assets.md` | filename convention exists; no shopping; pngs gitignored |
| ffmpeg render profile | Repeatable export                  | Format lock is `docs/format.md`; add a recipe only after one packet has selected VO + ready cards | format named; recipe not started |
| Private-repo git clone| Native checkout in agent sandbox   | Not required. Reconstruct per `docs/agent_session.md`. Push via GitHub file API. | parked; do not retry each run |
| Unauthenticated Drive download | Gate-machine copy of Q1 wav/cards | Signed-in download of folder `1ftaVyh8BWQeWp45TIyX7Hh1o0MPmGRev`, or copy the Run 248 chat zip, then `cp` to the packet paths in `HANDOFF.md`. Run 246: anonymous curl returned a Google sign-in page. Run 248: no Drive share-permission tool and no GitHub release-upload tool. | parked; do not add a public-link fetcher |

Do not poll APIs hoping credentials appear.
Do not invent a selected take to clear this table.
Do not `git add -f` ignored media.
Do not treat a Drive file id as anonymously fetchable.
Do not retry a share-permission or release-upload tool that is not in the connected tool list.
