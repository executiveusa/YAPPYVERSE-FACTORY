# Proof Protocol — social_reel_v1

## Goal

Prove that an external product can call YAPPY-CLIPZ as a service and receive a verified reel artifact.

## Preconditions

- Service deployed outside the client application.
- `YAPPY_CLIPZ_BASE_URL` configured in the client runtime.
- `YAPPY_CLIPZ_TOKEN` stored as a server-side secret.
- One real source video is available through an accessible signed URL.
- No publishing integration enabled.

## Test payload

Create a project for a non-production tenant, register one source video, then submit:

```json
{
  "tenant_id": "proof-tenant",
  "recipe": "social_reel_v1",
  "source_asset_ids": ["<asset-id>"],
  "instructions": {
    "duration_seconds": 30,
    "width": 1080,
    "height": 1920,
    "captions": true,
    "hook": true,
    "cta": true,
    "platform": "instagram"
  },
  "outputs": ["mp4"]
}
```

After MP4 passes, repeat the same source with `outputs: ["mp4", "capcut"]`.

## Pass criteria

### API

- Project creation returns 201 and a stable ID.
- Asset registration returns 201 and a stable ID.
- Job submission returns 202 and a stable job ID.
- Job can be polled without importing Montage internals.
- Terminal success state is `ready` or `approved`.
- Failures expose a bounded error object without secrets.

### MP4

- Output record has `kind=mp4`, `status=ready`, `verified=true`.
- Width = 1080.
- Height = 1920.
- Duration is > 0 and <= 30.5 seconds.
- File is decodable by FFmpeg/ffprobe.
- Video stream exists.
- Audio stream exists when the recipe selected source/bed audio.
- Captions are visually present when `captions=true`.
- No black-frame-only, zero-byte, or corrupt output.

### CapCut adapter

- Output record has `kind=capcut`, `status=ready`.
- Draft opens in the supported CapCut Desktop version.
- Source clips resolve.
- Timeline length matches the canonical edit.
- Captions/text are editable.
- At least one keyframe/transition survives when present in the canonical edit plan.
- A CapCut failure does not invalidate the verified MP4 artifact.

### Approval

- No publish action occurs automatically.
- `POST /approve` records the approving human identity.
- Rejection or failed QA cannot be represented as approved.

## Evidence bundle

Save the following IDs/artifacts with the test run:

- commit SHA
- deploy identifier
- project ID
- asset ID(s)
- job ID
- output ID(s)
- request timestamps
- output checksums
- ffprobe summary
- screenshot of rendered reel
- screenshot of opened CapCut draft for the adapter proof

Never save bearer tokens or signed storage credentials in the evidence bundle.

## Rollback

If the service path causes regressions, disable the calling product's YAPPY-CLIPZ feature flag or remove its base URL/token. Existing product functionality must remain unaffected. The CapCut adapter can be disabled independently while MP4 rendering remains active.
