# YAPPY-CLIPZ Service v1

## Decision

Use `executiveusa/pauli-montage-video-agent` (YAPPY-CLIPZ) as the shared video-production control plane. Customer-facing apps submit production intent through a stable service contract. Rendering/editing engines remain replaceable adapters.

## V1 outcome

An external application can submit source media and receive a verified 9:16 social reel output without importing Montage internals.

## Boundary

```text
client app -> YAPPY-CLIPZ service -> production pipeline -> output router
                                             |-> FFmpeg/Remotion -> MP4
                                             `-> CapCut adapter   -> editable draft
```

Applications own customer experience. YAPPY-CLIPZ owns production state, jobs, routing, approvals, costs, QA, and outputs.

## Minimal API contract

- `POST /api/v1/projects`
- `POST /api/v1/projects/{project_id}/assets`
- `POST /api/v1/projects/{project_id}/jobs`
- `GET /api/v1/jobs/{job_id}`
- `GET /api/v1/projects/{project_id}`
- `GET /api/v1/projects/{project_id}/outputs`
- `POST /api/v1/projects/{project_id}/approve`

See `openapi.yaml` for the normative contract.

## First recipe: social_reel_v1

Required proof slice:

1. Create project.
2. Register at least one source video asset.
3. Submit `social_reel_v1` job.
4. Produce 1080x1920 MP4, <=30 seconds.
5. Verify output exists, is decodable, has valid audio when expected, and matches aspect ratio.
6. Expose preview/output through service response.
7. Require human approval before publish.
8. Optional second output: editable CapCut draft.

## Status model

`queued -> analyzing -> editing -> rendering -> qa -> ready -> approved`

Failure states are terminal unless a new retry job is created: `failed`, `rejected`, `cancelled`.

## CapCut rule

CapCut is an output adapter, never canonical project state.

The adapter may translate the canonical timeline into:

- `create_draft`
- `add_video`
- `add_audio`
- `add_image`
- `add_text`
- `add_subtitle`
- `add_effect`
- `add_sticker`
- `add_video_keyframe`
- `save_draft`

If CapCut generation fails, MP4 production must remain independently recoverable.

## Security / sovereignty

- No secrets in client payloads or repository files.
- Service authentication must be server-to-server.
- Tenant ID is mandatory on every project and job.
- Storage URLs should be signed/short-lived where applicable.
- Publishing is out of scope for V1.
- Human approval is mandatory before any downstream publishing bridge.

## Rollback

This integration is additive. Rollback is deleting or reverting `integrations/yappy-clipz/`; no existing service contract is changed.

## Proof gate

Do not call the system production-ready until a real external client demonstrates:

`upload -> project -> job -> render -> QA -> output retrieval -> human approval`

and the evidence includes request/response IDs plus a playable output artifact.
