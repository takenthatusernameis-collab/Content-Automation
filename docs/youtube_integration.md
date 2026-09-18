# YouTube integration contract

## Goal

Keep the repository structurally ready for automated YouTube publishing so that, once the channel credentials are supplied, credentials are the final manual bottleneck rather than a missing implementation.

The current production repository intentionally has no live YouTube uploader. This document is the durable contract for constructing that layer without blocking on credentials.

## Required pipeline

1. Validate the packet locally: status, selected VO, cards, captions/metadata as applicable, and final master export.
2. Read `videos/NNN-slug/publish.md` as the canonical upload-metadata source.
3. Validate the local export and metadata in a **dry run** with no provider call.
4. Check for the required YouTube authentication material without printing its values.
5. When credentials are present, authenticate and upload through the YouTube Data API.
6. Persist only non-secret operational state: upload-attempt timestamp, provider video ID, final privacy state, and a redacted result/error code.
7. Never upload, publish, or change channel state merely because a manual hold expired; the hold only removes the repository-side block.

## Credential-last design

The repository may construct and test the uploader, metadata mapping, request formatting, retry behavior, idempotency guard, and redacted state handling **without** credentials.

The final manual bottleneck is provider authorization material, stored outside Git:

- `YOUTUBE_CLIENT_ID`
- `YOUTUBE_CLIENT_SECRET`
- `YOUTUBE_REFRESH_TOKEN`
- optional `YOUTUBE_API_KEY` for public-read/quota diagnostics
- optional `YOUTUBE_CHANNEL_ID` as a non-secret routing value

Never commit any of these values. Do not put them in `publish.md`, `STATE.md`, logs, test fixtures, or workflow output.

For uploads, an OAuth 2.0 authorization token is required; an API key by itself is not sufficient for `videos.insert`. Use the minimum upload scope needed by the implementation.

## Authentication boundary

The future uploader should fail closed with a single explicit state such as:

`YOUTUBE_AUTH_REQUIRED`

when required OAuth credentials are absent or invalid.

The daily unstick agent may construct or repair everything up to that boundary without waiting for a human. When the boundary is reached, it should request only the missing credential material and nothing else.

## Safety / idempotency

Before an upload attempt:

- require a completed local master export;
- require a valid `publish.md`;
- compute a stable packet/export fingerprint;
- refuse to upload the same fingerprint twice unless an explicit replacement operation is requested;
- use a non-destructive initial privacy mode configured by the repository policy;
- keep provider IDs and statuses in redacted state only.

Do not implement automatic deletion or channel-wide maintenance as part of the first uploader.

## Construction order

The daily agent may build these pieces in order without credentials:

1. metadata parser and validation;
2. export-path validation;
3. fingerprint/idempotency contract;
4. OAuth configuration loader;
5. dry-run request builder;
6. redacted result/state writer;
7. authenticated upload adapter;
8. final credential-only integration test.

The last step that cannot be completed without a real channel credential must be clearly reported as `YOUTUBE_AUTH_REQUIRED`.

## External reference

YouTube's current Data API documentation states that insert/update/delete requests require authorization, and `videos.insert` accepts OAuth scopes including `https://www.googleapis.com/auth/youtube.upload`.

References:
- https://developers.google.com/youtube/v3/docs
- https://developers.google.com/youtube/v3/docs/videos/insert
- https://developers.google.com/youtube/v3/guides/authentication


## Feedback access

After publication, the same credentialed integration should support:

- YouTube Analytics reports through the Analytics API, using an appropriately authorized readonly scope.
- Video comment-thread retrieval through the Data API, with `comments.list` available when complete reply retrieval is required.
- Redacted storage of the video ID, retrieval timestamp, observation window, and imported metrics/comments. Never store OAuth tokens in feedback files.

YouTube's Analytics reporting API supports metrics such as views, likes/dislikes, estimated minutes watched, average view duration, and average view percentage. citeturn562536search5turn562536search7
YouTube's Data API supports comment-thread retrieval by video ID; replies may require the comments.list method. citeturn562536search0turn562536search2

The feedback collector must fail closed at `YOUTUBE_AUTH_REQUIRED` when readonly authorization is absent, just as the uploader does for upload authorization.
