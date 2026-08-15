# OpenCode/Hermes next action

The included mock control-plane demo already passes its Slice-1 behavioral checks. Do not rewrite it from scratch.

## Required live conversion

1. Copy/adapt this scaffold into the approved Pauli factory branch/worktree.
2. On Hostinger, run `node src/capability-discovery.mjs` with the installed Orca binary.
3. Inspect `runtime/orca-capabilities.json` (redacted output only in reports).
4. Replace `RealOrcaAdapter.prepare/build/test/review/cleanup` with exact version-matched Orca calls proven by that snapshot and `orca ... --help` output.
5. Wire Hermes to `POST /jobs`, `GET /jobs/:id`, and `POST /jobs/:id/cancel` or equivalent in-process calls.
6. Replace demo JSON persistence/lease implementation with the existing durable Hermes/Postgres layer if already present; preserve the contract and atomic/idempotent semantics.
7. Add Beads ownership around every implementation task and live factory job.
8. Run the same demo matrix against real Orca: success, duplicate request, overlapping repo job, induced test failure, cancellation, cleanup.
9. Return the evidence JSON and service health proof. Do not claim live completion before these pass.

## Current gate

The only intentional fail-closed gap is the exact real-Orca command binding. This must be derived from the actual installed runtime, not guessed from docs or memory.
