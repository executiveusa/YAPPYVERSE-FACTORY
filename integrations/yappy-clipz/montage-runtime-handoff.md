# Montage Runtime Handoff — YAPPY-CLIPZ V1

## Purpose

This document is the implementation handoff for `executiveusa/pauli-montage-video-agent` once that repository is writable from the active GitHub connector. It translates the already-merged YAPPY-CLIPZ service contract into the smallest safe Montage-side change set.

The V1 goal is deliberately narrow:

> One external client registers one real source video, submits one `social_reel_v1` job, observes durable job state, receives one independently verified 1080x1920 MP4 <= 30.5s, retrieves it through `/outputs`, and then completes a separate human approval step.

CapCut is V1.1. Publishing is out of scope.

## Reuse decision

Do not create a second editor, timeline, project store, or orchestration engine.

The Montage `feat/one-shot-autonomous-edit-loop` work already defines the desired execution model:

- `StudioProject` / canonical artifacts remain the source of truth;
- one-shot is a profile layered on the existing `hybrid` pipeline;
- edit decisions remain source-backed;
- rendering is followed by ffprobe/technical validation and visual review;
- render-review loops are bounded;
- the loop ends at review, never publish.

`social_reel_v1` therefore adapts the API job into that execution path.

## Required service boundary

Implement exactly these V1 routes:

```text
POST /api/v1/projects
POST /api/v1/projects/{project_id}/assets
POST /api/v1/projects/{project_id}/jobs
GET  /api/v1/jobs/{job_id}
GET  /api/v1/projects/{project_id}
GET  /api/v1/projects/{project_id}/outputs
POST /api/v1/projects/{project_id}/approve
```

The normative wire schema is:

`YAPPYVERSE-FACTORY/integrations/yappy-clipz/openapi.yaml`

Do not fork or reinterpret that contract in Montage. Generate/validate against it where practical.

## Internal boundary

Use four explicit application interfaces. Names may match existing Montage naming if equivalent services already exist.

### 1. ProjectService

Responsibilities:

- create/load canonical StudioProject;
- enforce tenant ownership;
- attach project metadata / brand profile references;
- expose project status without exposing Montage internals.

### 2. AssetService

Responsibilities:

- register immutable source URLs and metadata;
- assign stable asset IDs;
- validate tenant/project ownership;
- never infer media contents from filenames;
- hand source assets to the existing media-review/transcription path.

### 3. JobService

Responsibilities:

- atomically create or return a job by `(tenant_id, project_id, idempotency_key)`;
- return `202` before heavy production starts;
- persist status, progress, attempts, timestamps, terminal error metadata and cancellation state;
- enqueue work rather than executing a long render in the request handler.

Job lifecycle:

```text
queued -> analyzing -> editing -> rendering -> qa -> ready -> approved
```

Terminal alternatives:

```text
failed | rejected | cancelled
```

Required safety semantics:

- duplicate idempotency key returns the original job ID;
- retries cannot create duplicate output records;
- terminal states are monotonic;
- worker crash preserves the last verified canonical project state;
- bounded error objects contain no secrets or signed storage credentials.

### 4. OutputService

Responsibilities:

- register renderer outputs separately from canonical state;
- compute/store SHA-256;
- store width, height, duration, status and verification metadata;
- issue a retrievable URL without logging or persisting signed credentials into public evidence;
- a renderer failure must not corrupt StudioProject.

## `social_reel_v1` adapter

Input contract:

```json
{
  "recipe": "social_reel_v1",
  "source_asset_ids": ["asset-id"],
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

Adapter behavior:

1. Resolve the source asset into the existing source-media review path.
2. Use the existing transcriber capability and source timing.
3. Select the appropriate existing pipeline profile. Prefer the one-shot/hybrid path for source + support edits; use an already-existing talking-head path only if the source shape requires it.
4. Produce canonical `edit_decisions` / asset-manifest updates through existing Montage services.
5. Render from canonical state through the existing deterministic composition stack.
6. Run the existing watch/review loop with a hard maximum of 3 complete render-review rounds.
7. Produce a final review MP4; do not publish.
8. Verify technically before setting job `ready`.

Do not hardcode provider names in the API adapter. Provider/model selection stays behind the existing Montage registry/router and approved cost policy.

## Worker architecture

HTTP handlers are control-plane only.

```text
request
  -> validate/auth/tenant
  -> persist job
  -> enqueue/dispatch
  -> 202

worker
  -> load canonical project
  -> run recipe adapter
  -> update durable status
  -> render/review
  -> verify artifact
  -> persist output
  -> ready
```

Use the repository's existing worker/queue mechanism if one exists. If none exists, introduce the smallest interface-backed durable mechanism that works in preview and can later be swapped without changing the API contract. Do not couple client applications to that mechanism.

## MP4 readiness gate

A job cannot become `ready` merely because a renderer exited successfully.

Before `ready`, the service must record:

- output exists and is non-empty;
- ffprobe can decode it;
- at least one video stream exists;
- width = 1080;
- height = 1920;
- duration > 0 and <= 30.5 seconds;
- audio stream exists when selected by the edit;
- SHA-256 checksum;
- no unresolved critical Montage visual-QA finding;
- final render/review evidence reference.

The external factory proof will independently re-download and verify the artifact. Server-side claims are not sufficient.

## Approval boundary

`POST /api/v1/projects/{project_id}/approve` must:

- require an authenticated human identity;
- require a `ready` output;
- persist who approved, what output they approved, and timestamp;
- move project/job to approved state monotonically;
- never trigger publish in V1.

The external proof workflow intentionally stops before this endpoint. Approval must be a distinct human action.

## Authentication and tenancy

V1 requirements:

- bearer authentication at the service boundary;
- tenant identity is required on mutable calls;
- resource lookup must validate tenant ownership server-side;
- never trust client-supplied project/asset IDs without tenant authorization;
- errors and logs must not expose tokens, signed URLs, provider secrets, or raw credentials.

## Required tests in Montage

Add tests for:

1. project creation / retrieval;
2. cross-tenant project denial;
3. asset registration;
4. job creation returns 202;
5. repeated idempotency key returns same job ID;
6. illegal job-state transition rejected;
7. worker retry does not duplicate output;
8. failed render cannot become `ready`;
9. verified MP4 metadata persisted;
10. `/outputs` returns the verified artifact record;
11. approval rejected before ready;
12. approval stores human identity;
13. no publish side effect;
14. bounded/redacted error serialization.

## Preview proof sequence

After Montage implementation is deployed to a preview URL:

1. Configure these **secrets** in YAPPYVERSE-FACTORY GitHub Actions:
   - `YAPPY_CLIPZ_BASE_URL`
   - `YAPPY_CLIPZ_TOKEN`
   - `YAPPY_CLIPZ_SOURCE_URL`
2. Run workflow `YAPPY-CLIPZ V1 Proof` manually.
3. Supply an independent reviewer identity and non-secret visual-QA evidence reference.
4. Workflow must finish `READY_FOR_HUMAN_APPROVAL` and upload redacted evidence.
5. A human reviews the MP4.
6. Human calls `/approve` separately.
7. Record approval evidence on issue #19.
8. Only then mark V1 proven.

## V1 acceptance evidence

Required before production claim:

- Montage implementation commit SHA;
- preview deployment ID/URL;
- project / asset / job / output IDs;
- idempotency proof;
- job-state trace;
- output SHA-256;
- independent ffprobe result;
- black-frame analysis;
- independent visual-QA evidence;
- human approval record;
- CI/review green;
- rollback instructions.

## Rollback

Keep the service layer additive until V1 passes.

Rollback order:

1. disable external YAPPY-CLIPZ feature flag / credentials;
2. stop accepting new API jobs;
3. drain or cancel queued V1 jobs safely;
4. revert the service-adapter PR if required;
5. preserve canonical StudioProject data and existing Montage execution paths.

CapCut V1.1 must be independently disableable and must never be required for MP4 production.

## Explicit non-goals

Do not include in this PR:

- CapCut integration;
- publishing / Postiz / social APIs;
- new video providers solely for this recipe;
- new editor UI;
- second timeline/project format;
- broad API expansion beyond the seven routes;
- synchronous rendering inside request handlers.
