# Yappyverse Install-Ready V1

Status: PRE-INSTALL / PROOF-GATED
Owner issue: YAPPYVERSE-FACTORY#26
Runtime repo: executiveusa/pauli-berd
Runtime branch under proof: feature/yappyverse-hermes-wire-v1

## Decision

Yappyverse V1 remains a branded distribution of the existing Berd/Tauri runtime. The runtime plumbing is frozen for this slice. Hermes is the only agent wired for execution proof. Every other Grinion is identity/configuration only until a later approved slice.

## Architecture lock

```text
Yappyverse character (Hermes)
  -> Yappyverse registry
  -> provider: hermes-acp
  -> existing Berd / Goose ACP plumbing
  -> external hermes-acp executable
  -> Hermes native ACP server
  -> Hermes tools / skills / model selection
```

No custom Hermes bridge is required. Do not add Hermes to Berd's managed npm bridge installer. `hermes-acp` must be resolved as an external executable from the user's environment.

## What is allowed before install

- product name, logo, icon, colors, visible copy, splash/about labels
- character/avatar identity through existing presentation hooks
- distribution config and manifests
- Hermes provider registration through the existing external ACP lane
- tests, preflight, acceptance receipts, rollback tooling

## Frozen until after V1 proof

- Goose/ACP transport internals
- auth/database redesign
- multiplayer rooms
- DeepSeek Harness integration
- model-router redesign
- new backend services
- 3D runtime/animation engine
- automatic wiring of Pi, Cosmos, TARS, Jarvis, Lightning, or MAXX

## Build gates

The exact runtime checkout must pass:

```bash
just setup
just ci
```

For a local interactive proof:

```bash
just dev
```

For an installable desktop bundle:

```bash
just bundle
```

A release is not accepted merely because a bundle exists. It must also have a Hermes round-trip receipt.

## Hermes native acceptance receipt

The machine used for final proof must establish all of the following:

1. `hermes-acp` is resolvable without a PTY wrapper.
2. Berd/Yappyverse spawns it with pipe-backed stdio.
3. ACP `initialize` succeeds.
4. `session/new` succeeds.
5. A prompt is sent from the Yappyverse UI.
6. Hermes returns a response to the same UI session.
7. The app can be closed and reopened without corrupting the provider/agent state.

## Install handoff sequence

1. Clone or update `executiveusa/pauli-berd`.
2. Check out the approved Yappyverse runtime commit/branch.
3. Install/verify Hermes so `hermes-acp` resolves on PATH.
4. Run `scripts/yappyverse-preflight.ps1 -RepoPath <path-to-pauli-berd>` from this factory repo.
5. In the runtime repo run `just setup` then `just ci`.
6. Start `just dev` and perform the Hermes round trip.
7. Save the receipt using `scripts/yappyverse-acceptance.ps1`.
8. Only after the receipt is green: merge the runtime PR.
9. Run `just bundle` from the merged release candidate.
10. Install the generated native bundle on a clean test profile and repeat the smoke test.

## Rollback

If Hermes launch or UI behavior regresses:

- do not patch Goose/ACP plumbing first;
- revert the isolated Hermes/Yappyverse runtime PR;
- verify the base Berd runtime still passes its normal checks;
- reopen only the failing boundary as a new isolated slice.

## Definition of install-ready

V1 is INSTALL-READY only when all are true:

- runtime code is merged from a reviewed, isolated PR;
- `just ci` passes on the exact merged commit;
- `hermes-acp` preflight passes;
- UI -> Hermes -> UI receipt exists;
- `just bundle` succeeds;
- rollback commit/PR is known;
- installer artifact has been smoke-tested after installation.
