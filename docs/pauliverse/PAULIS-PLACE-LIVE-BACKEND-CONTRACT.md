# Pauli's Place Live Backend Contract

## Status
VERIFIED FRONTEND CONTRACT / RUNTIME GAP

## Purpose
This document records the API and WebSocket contract currently expected by the deployed Pauli's Place frontend so the Mission 001 backend can be implemented without rediscovering the bundle.

This is derived from inspection of the live production JavaScript bundle on 2026-08-10. It is an integration contract, not a claim that the backend is currently live.

## Current production behavior

The deployed frontend has two API-base conventions:

```text
NEXT_PUBLIC_API_URL
NEXT_PUBLIC_API_BASE_URL
```

Both fall back to:

```text
http://localhost:8000
```

The 3D Lounge WebSocket uses:

```text
NEXT_PUBLIC_LOUNGE_WS_URL
```

and falls back to:

```text
ws://localhost:8000/ws
```

When these backends fail, the application deliberately substitutes in-browser demo data. Therefore a visually active dashboard is not evidence that the portfolio system is actually connected.

## Lounge / observability endpoints

The current 3D Lounge client expects:

### `GET /api/hermes/health`
Returns current Hermes/system health.

### `GET /api/envelopes/recent?limit=<n>`
Returns:

```json
{
  "envelopes": []
}
```

### `GET /api/lounge/state`
Expected fields include:

```json
{
  "lounge": "Pauli's Place",
  "setting": "...",
  "avatars": [],
  "schedule_cue": "..."
}
```

### `GET /api/lounge/scenes?limit=<n>`
Returns:

```json
{
  "scenes": []
}
```

### `POST /api/voice/command`
Request:

```json
{
  "transcript": "natural-language command"
}
```

Response is an event/envelope. The current UI checks for halt/judge outcomes and may trigger an avatar speaking state.

## WebSocket

The Lounge attempts a WebSocket connection to the configured lounge URL.

Current client behavior expects messages similar to:

```json
{
  "type": "event",
  "envelope": {
    "route": "R-02:...",
    "stage": "...",
    "body": {},
    "event_id": "...",
    "ts": "..."
  }
}
```

The current UI treats selected `R-02` events as scene/feed updates and selected `R-04` events as speaking/target-avatar updates.

Mission 001 should preserve compatibility during migration, but the stable Pauliverse event envelope remains the authoritative cross-node event contract. A compatibility adapter may translate Pauliverse events into legacy Lounge route envelopes rather than making legacy `R-*` routes the new ontology.

## Existing commercial/dashboard endpoints

The production dashboard client currently expects these routes:

### Dashboard

```text
GET /api/dashboard/stats
GET /api/dashboard/revenue-chart?days=<n>
GET /api/dashboard/niches
```

### Products

```text
GET /api/products/
GET /api/products/?platform=<p>&status=<s>&niche=<n>
GET /api/products/<id>
GET /api/products/<id>/image
```

### Approval Queue

```text
GET  /api/approvals/queue
POST /api/approvals/action
```

The current approval request body is structurally equivalent to:

```json
{
  "product_ids": [123],
  "action": "approve"
}
```

### Tasks

```text
GET /api/tasks/
GET /api/tasks/?status=<status>
GET /api/tasks/summary
GET /api/tasks/recent-errors
```

### Triggers

```text
POST /api/trigger/scan-trends
POST /api/trigger/score-trends
POST /api/trigger/create-products
```

## Critical security correction

The existing browser contract for approval actions is not sufficient authority for high-consequence execution by itself.

Mission 001 requires the backend to bind approvals to server-side records containing at minimum:

```yaml
approval_id: stable-id
subject_type: product|opportunity|mission|transaction|deployment|other
subject_ids: []
action: ""
requested_by: ""
requested_at: ""
approved_by: ""
approved_at: ""
expires_at: ""
run_or_correlation_id: ""
policy_version: ""
status: requested|approved|denied|expired|consumed
```

A client request such as `{"product_ids": [1], "action": "approve"}` may request an action, but it must not be treated as proof that an authorized human approved the action.

For publish/payment/credential/destructive operations, the server must verify the approval receipt, subject, action, actor, expiry and one-time consumption before side effects.

## Demo-data prohibition

The current client includes synthetic fallback values for products, revenue, margins, council decisions, trends, tasks and scenes.

During Mission 001:

- demo data may remain available only when clearly labeled as demo;
- demo values must never be merged into commercial or portfolio evidence;
- the owner cockpit must expose whether each card/node/event is `LIVE`, `STALE`, `DEMO`, or `UNVERIFIED`;
- financial totals shown as live must originate from a verified financial/commerce source;
- council rulings shown as live must point to a real decision record;
- product publish status must point to a real provider/order/catalog receipt.

## Preferred production topology

The frontend is suitable for Vercel. The authoritative Hermes runtime should be treated as a persistent agent runtime rather than forced into a frontend framework preset.

Recommended separation:

```text
PAULI'S PLACE / VERCEL
  Next.js UI
  read-only/approval web surface
        |
        | HTTPS + WSS
        v
HERMES CONTROL API
  persistent runtime
  authenticated API + event stream
  council/orchestration
        |
        +--> worker nodes (Pi / specialists)
        +--> portfolio ontology/evidence store
        +--> Pauli's Place commercial services
```

If Hermes remains on Vercel, its project/root/build configuration must explicitly match the runtime being deployed. The current build path installs `ui` dependencies and then fails Next.js detection, so the deployment is not reaching the Hermes runtime.

## Compatibility objective for the next implementation slice

The next builder must make these three claims true with proof:

1. `GET /api/hermes/health` returns a real Hermes/control-plane status rather than demo fallback.
2. `GET /api/lounge/scenes` returns events derived from the Pauliverse event stream and includes provenance/evidence refs.
3. Pauli's Place displays a visible `LIVE` source badge only when the backend handshake, schema version and freshness checks pass.

Only after those pass should the 3D scene be upgraded to render the full repository ontology.
