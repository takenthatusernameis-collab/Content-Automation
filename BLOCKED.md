# BLOCKED

External work is parked here so runs do not retry it blindly.

| Dependency            | Why needed                         | Simplest human setup                                      | Status   |
|-----------------------|------------------------------------|-----------------------------------------------------------|----------|
| Channel niche/brand   | Every template depends on it       | Confirm or replace `docs/channel.md`                      | temporary default set |
| Series playlist id | Add each video to one playlist without a per-video Studio click | Create one playlist in Studio. Replace `playlist_id: not_set` in `docs/channel.md` with that PL id. Upload does not wait on this. | optional; not the publish gate |
| YouTube Data API OAuth| Upload, titles, analytics          | Add `YOUTUBE_CLIENT_ID`, `YOUTUBE_CLIENT_SECRET`, and `YOUTUBE_REFRESH_TOKEN` as GitHub Actions secrets. Then dispatch `youtube-production.yml` with execute=true. After a provider video id exists and uploaded_at is at least 7 days old, dispatch collect_feedback=true. Early collect is OBSERVATION_WINDOW_NOT_DUE. Privacy stays private. | secrets absent on Actions; dry-run 36983196381 confirmed local gates pass; authenticated dispatch fails before materialize if any secret is empty. Recurring stall since before Run 270. Do not poll. Do not spend a run only restating this row. |
| TTS or microphone VO  | Narration audio                    | Record to `videos/NNN-slug/vo/NNN-slug-take-selected.wav` (or .flac). Repo-root `vo/` is not Selected VO. Optional local TTS only if a human names that policy. | Q1 generated take is on private release r249; do not regenerate while checksum matches |
| Stock / original media| B-roll and thumbs                  | Decide “text-card + public-domain” vs licensed stock; card names live in packet `assets.md` and `docs/assets.md` | Q1 cards and thumbnail draft exist; pngs gitignored |
| ffmpeg render profile | Repeatable export                  | Format lock is `docs/format.md`; finished Q1 export is q1-media-r253 | do not re-encode while r253 exists |
| Private-repo git clone| Native checkout in agent sandbox   | `gh` auth / GH_TOKEN. Actions checkout works. Still do not commit media. | unblocked on Actions |
| Unauthenticated Drive download | Gate-machine copy of Q1 wav/cards | Use `tools/materialize_q1_release.py` or `gh release download`. It must ignore r249 `q1-master.mp4` and install r253 only. Anonymous curl still returns a sign-in page. | release fetch verified on Actions run 36983196381 |

Do not poll APIs hoping credentials appear.
Do not invent a selected take to clear this table.
Do not `git add -f` ignored media.
Do not treat a Drive file id as anonymously fetchable.
Do not retry a share-permission or release-upload tool that is not in the connected tool list.
Do not treat the known truncated r249 master as a reason to abort materialize.
