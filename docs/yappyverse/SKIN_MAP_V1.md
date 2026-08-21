# Yappyverse Skin Map V1

Purpose: rebrand Berd into Yappyverse without changing runtime behavior.

## Governing rule

**Keep the plumbing; change the paint.**

This document is a change-boundary map, not permission to redesign the application architecture.

## Allowed visual/product surfaces

Search the runtime repository for the current product identity and update only presentation/distribution surfaces that are already designed to vary by distribution.

Target classes:

1. **Visible product name**
   - app/window title
   - settings/about labels
   - welcome/onboarding copy
   - empty states where the product refers to itself

2. **Brand assets**
   - logo
   - launcher/app icon
   - splash/loading artwork
   - favicon/webview assets when applicable

3. **Theme tokens**
   - existing color variables/tokens only
   - existing typography tokens only
   - no component architecture rewrite

4. **Agent presentation**
   - display name
   - avatar
   - description/persona copy
   - labels using `Grinion` / `Grinions`

5. **Distribution metadata**
   - package/product display metadata where Berd explicitly exposes a distribution seam
   - installer-visible product name/icon only after build validation

## Do not modify in the skin PR

- ACP protocol code
- Goose sidecar management
- provider transport behavior
- auth
- persistence/database
- model routing
- update protocol
- network permissions/capabilities
- Tauri command surface
- IPC contracts
- managed ACP bridge installation
- Hermes ACP implementation beyond the already-isolated provider registration

## Character/runtime separation

A Grinion is a visual/product identity. It must not encode a model or harness directly into its presentation layer.

```text
Grinion identity
  -> runtime/provider binding
  -> optional harness
  -> model/provider
```

Changing a Grinion's avatar must not require changing its runtime. Changing Hermes' model must not require changing the Hermes character.

## V1 roster presentation

The factory contract lives at `config/yappyverse/grinions.v1.json`.

- Hermes: visible and execution-proof target
- Pi: identity only
- Cosmos: identity only
- TARS: identity only
- Jarvis: identity only
- Lightning: identity only
- Agent Max / MAXX: identity only
- Fanni: excluded from Yappyverse Core

Do not present identity-only Grinions as connected or operational.

## Safe implementation sequence in runtime repo

1. Branch from the exact proven Hermes runtime commit.
2. Inventory all current visible `Berd` brand references.
3. Classify every candidate as PRESENTATION, DISTRIBUTION, or RUNTIME.
4. Change PRESENTATION and approved DISTRIBUTION references only.
5. Replace assets through existing asset seams; do not introduce a new renderer or 3D engine.
6. Run `just check` after frontend changes.
7. Run `just test` for covered identity/provider behavior.
8. Run `just ci` before merge.
9. Launch `just dev` and confirm Hermes still completes the same UI round trip.
10. Run `just bundle` only after the above gates are green.

## Skin PR proof checklist

- [ ] no ACP/Goose transport files changed
- [ ] no database/auth/model-router files changed
- [ ] no new backend service added
- [ ] product-visible name is Yappyverse
- [ ] agent noun is Grinion/Grinions where appropriate
- [ ] Hermes retains provider `hermes-acp`
- [ ] identity-only fleet members are not falsely shown as connected
- [ ] `just check` green
- [ ] `just test` green
- [ ] `just ci` green
- [ ] Hermes UI round trip still green
- [ ] installer/bundle uses Yappyverse presentation metadata

## Rollback

The skin PR must remain separately revertible from the Hermes runtime wiring PR. If any functional regression appears, revert the skin PR first. Do not modify transport code to make a branding regression disappear.
