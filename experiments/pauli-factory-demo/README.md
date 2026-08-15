# Pauli Factory Slice-1 Demo

A dependency-free executable demonstration of the Pauli Factory control-plane contract.

## Proven in this demo

- `POST /jobs` (`create_job`)
- `GET /jobs/:id` (`get_job`)
- `POST /jobs/:id/cancel` (`cancel_job`)
- durable JSON job/evidence state
- request idempotency
- repository lease preventing overlapping mutable jobs
- bounded budget validation
- builder/reviewer separation
- trusted-test gate
- independent-review gate
- cleanup evidence
- induced failure handling
- cancellation
- health endpoint

## Run

```bash
npm run demo
```

For an interactive API:

```bash
npm run serve
```

Then call `http://127.0.0.1:8787/healthz` and `/jobs`.

## What is mocked

`src/mock-orca-adapter.mjs` is intentionally a seam. Replace it with a `RealOrcaAdapter` that invokes the version-matched Orca runtime discovered on the Hostinger VPS. The public factory contract and supervisor behavior should remain stable.

This demo does **not** claim that Hermes, Orca, or Hostinger are live-integrated yet. It proves the control-plane behavior that the live adapter must preserve.
