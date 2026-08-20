# Proof Protocol — social_reel_v1

## Goal

Prove that an external product can call YAPPY-CLIPZ as a service and receive one verified vertical MP4 without importing Montage internals.

**V1 ends at independently verified MP4 + explicit human approval. CapCut is V1.1 and is not part of the V1 production gate.**

## Preconditions

- Service deployed outside the client application.
- `YAPPY_CLIPZ_BASE_URL` configured in the client runtime.
- `YAPPY_CLIPZ_TOKEN` stored as a server-side secret.
- `YAPPY_CLIPZ_SOURCE_URL` points to one real source video through an accessible signed URL.
- `ffprobe` and `ffmpeg` are installed where the proof harness runs.
- Independent visual-QA evidence exists as JSON for the exact returned artifact.
- No publishing integration enabled.
- Service job execution is durable and separate from ordinary request handling.

## Automated technical proof harness

Run:

```bash
YAPPY_CLIPZ_BASE_URL="https://<preview-host>" \
YAPPY_CLIPZ_TOKEN="<server-secret>" \
YAPPY_CLIPZ_SOURCE_URL="<signed-source-video-url>" \
YAPPY_CLIPZ_VISUAL_QA_JSON="./evidence/visual-qa.json" \
node integrations/yappy-clipz/proof-social-reel-v1.mjs
```

Optional controls:

```bash
YAPPY_CLIPZ_TENANT_ID="proof-tenant"
YAPPY_CLIPZ_TIMEOUT_MS="600000"
YAPPY_CLIPZ_POLL_MS="2000"
```

The harness intentionally submits the same job request twice with the same idempotency key. A compliant service must return the same job ID rather than duplicate production work.

The harness then downloads the returned MP4 transiently, recomputes SHA-256, runs local `ffprobe`, verifies video dimensions and duration, checks audio-stream presence, and runs an FFmpeg black-frame check. It does **not** trust `verified=true` by itself.

The harness never saves or prints the signed output URL. It removes the downloaded artifact after verification.

A compliant visual-QA JSON file must identify an independent reviewer and confirm:

```json
{
  "artifact_reviewed": true,
  "captions_visible": true,
  "critical_findings_resolved": true,
  "reviewer": "<independent-reviewer-id>",
  "evidence_ref": "<non-secret-reference>"
}
```

Never commit tokens, signed source URLs, or signed output URLs.

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
  "outputs": ["mp4"],
  "idempotency_key": "<stable-test-key>"
}
```

## Pass criteria

### API and durable job semantics

- Project creation returns 201 and a stable ID.
- Asset registration returns 201 and a stable ID.
- Job submission returns 202 and a stable job ID.
- Repeating the same request with the same idempotency key returns the same job ID.
- Job can be polled without importing Montage internals.
- Job state transitions are recorded and retrievable.
- Terminal technical-success state is `ready` or `approved`.
- Failures expose a bounded error object without secrets.
- In-flight client requests obey their deadline/abort signal.
- Worker retry/attempt metadata does not create duplicate outputs.

### Canonical-state integrity

- `StudioProject` / canonical pipeline artifacts remain the source of truth.
- The service layer does not create a second hidden timeline.
- Every render is derived from canonical edit decisions and registered assets.
- Renderer/worker failure cannot corrupt the last verified canonical state.

### MP4 — independently verified

- Output record has `kind=mp4`, `status=ready`.
- The artifact URL can be downloaded by the proof runner.
- Downloaded artifact is non-empty.
- Recomputed SHA-256 exactly matches the service-recorded checksum.
- `ffprobe` can decode the file and finds a video stream.
- Width = 1080.
- Height = 1920.
- Duration is > 0 and <= 30.5 seconds.
- Audio-stream presence is recorded.
- FFmpeg black-frame analysis does not indicate a black-frame-only render.
- Captions are visually confirmed when `captions=true` by separate visual QA.
- Service-side `verified=true` is recorded only as a claim; it is not sufficient proof by itself.

### Editorial review

- A technically valid MP4 alone is not enough.
- The Montage watch loop must have no unresolved critical visual-QA findings.
- Independent visual-QA evidence must identify the reviewer.
- Captions/titles are inside safe areas.
- Source/support visuals are semantically relevant.
- The final review render and its review evidence are both retrievable.

### Human approval — separate step

The automated technical harness must **stop before approval** and return `READY_FOR_HUMAN_APPROVAL`.

A human reviewer must then inspect the actual reel and explicitly call:

```http
POST /api/v1/projects/{project_id}/approve
```

with their own identity and the reviewed output ID.

After that action, approval must be independently verified from service state/evidence before V1 is declared passed.

- No harness or builder may approve on behalf of the human.
- No publish action occurs automatically.
- `POST /approve` records the approving human identity.
- Rejection or failed QA cannot be represented as approved.
- Production-ready status requires both the automated proof bundle and the separate approval record.

## Evidence bundle

Save the following IDs/artifacts with the test run:

- commit SHA
- deploy identifier
- project ID
- asset ID(s)
- job ID
- idempotency key (non-secret)
- job-state trace
- attempt/retry metadata
- output ID
- request timestamps
- recomputed output SHA-256 checksum
- ffprobe summary
- black-frame analysis summary
- render-review/visual-QA evidence reference
- screenshot of rendered reel
- separate human approval record

Never save bearer tokens, signed source URLs, or signed output URLs in the evidence bundle.

## V1.1 — CapCut adapter proof

Only after the complete V1 proof above passes, repeat the same canonical project with a CapCut output request.

Required V1.1 criteria:

- Output record has `kind=capcut`, `status=ready`.
- Draft opens in the supported CapCut Desktop version.
- Source clips resolve.
- Timeline length matches the canonical edit.
- Captions/text are editable.
- At least one keyframe/transition survives when present in the canonical edit plan.
- A CapCut failure does not invalidate the verified MP4 artifact.
- CapCut never becomes canonical project state.

## Rollback

If the service path causes regressions, disable the calling product's YAPPY-CLIPZ feature flag or remove its base URL/token. Existing product functionality must remain unaffected.

The API/service layer must be additive to Montage's existing execution paths until the external proof passes. Renderers remain independently disableable. V1.1 CapCut can be rolled back without affecting verified MP4 production.
