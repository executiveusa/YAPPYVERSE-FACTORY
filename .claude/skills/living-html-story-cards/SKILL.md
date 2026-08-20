---
name: living-html-story-cards
description: >
  Builds lightweight cinematic interactive story cards from approved still art using HTML/CSS/Canvas/SVG first,
  with multiplane depth, scroll/tilt parallax, motivated lighting, atmosphere, HUD/evidence overlays, and optional
  3D/WebGL progressive enhancement. Use for Pauli/Yappyverse story cards, case-file panels, landing-page scenes,
  digital flipbooks, evidence objects, character cards, and collectible moments that should feel alive without
  requiring video. Preserves source-image fidelity, mobile performance, canon boundaries, and reversibility.
alwaysApply: false
---

# Living HTML Story Cards

## Prime directive

Turn one approved still into a **living scene**, not a video substitute and not a generic UI card.

The card should feel like a tiny world: depth changes with scroll/touch, rain/fog moves independently, practical
lights flicker, reflections breathe, signal overlays react, clues can be inspected, and the story can advance through
interaction — while the original approved source image remains authoritative and visually recognizable.

## Canon and source-image rule

1. Approved source art is immutable unless the owner explicitly authorizes an edit.
2. Do not repaint, regenerate, relabel, crop away the focal subject, or invent canonical details.
3. Motion layers may reveal depth or attention; they may not change what happened.
4. Player interaction changes discovery/knowledge, not canon truth.
5. All generated overlays/effects are presentation layers and must be removable without losing the scene.

## Rendering hierarchy

Use the lightest layer that can achieve the intended result:

1. **HTML/CSS** — transforms, perspective, opacity, filters, blend modes, masks, gradients, shadows, text/HUD.
2. **SVG** — rain streaks, scanlines, light cones, masks, glints, vector HUD, controlled distortion.
3. **Canvas 2D** — dense rain, fog particles, dust, sparks, procedural signal noise, inexpensive atmosphere.
4. **WebGL / Three.js** — only when real geometry, camera depth, volumetric behavior, or shader work materially improves the scene.
5. **Video** — optional authored or generated accent, never required for baseline playability.

Default mode: **LIVE_STILL**.

## LIVE_STILL scene recipe

For each approved still, derive presentation layers without changing source content:

- `base` — original full scene / far plate.
- `mid` — optional duplicate or masked region for middle-depth motion.
- `near` — optional foreground duplicate/mask for stronger parallax.
- `atmosphere` — Canvas/SVG rain, fog, smoke, grain, dust.
- `light` — practical flicker, window pulse, reflection breathing, vehicle glint, lightning/signal flash.
- `hud` — minimal semantic evidence metadata, never decorative dashboard clutter.
- `interaction` — hotspot, clue, witness fragment, object inspect, branch choice, or unlock.

Use CSS `perspective`, `translate3d`, `scale`, `filter`, `clip-path`, `mask-image`, `mix-blend-mode`, and `will-change`
carefully. Prefer transforms/opacity for animation. Avoid layout-thrashing properties on every frame.

## Liveness grammar

A scene gets **1–2 motivated effects by default**, not every possible effect.

Approved effect vocabulary:
- rain / droplet drift
- fog or cloud drift
- lamp/window/neon flicker
- reflection breathing
- vehicle/chrome glint
- focus breathing
- surveillance scan / signal tear
- camera micro-sway
- shallow pointer/touch tilt
- subtle depth parallax
- particle dust / mist

Every effect must serve at least one purpose: **depth, attention, story escalation, evidence, or atmosphere**.
If it serves none, remove it.

## 3D card behavior

The card is a layered 2.5D scene first.

Pointer-capable devices may add a shallow `rotateX/rotateY` tilt and depth separation. Touch devices use scroll-driven
pan/parallax instead of hover-dependent behavior. Full WebGL is progressive enhancement only.

Do not make the user fight the card. Maximum perceived tilt should remain restrained; the story image must remain legible.

## Mobile law

Primary acceptance viewport: **390x844**.

- Never rely on hover.
- Wide 16:9 art gets a per-scene focal point and controlled discovery pan rather than a destructive center crop.
- Keep current card/scene plus at most adjacent expensive media mounted/decoded on low-memory devices.
- Video must not block first interaction.
- Reduced-motion mode preserves all story information and interactions.
- Touch targets >= 44 CSS px where practical.
- Keep the DOM/2D experience narratively complete if WebGL is disabled.

## Perceptual Seam Lock

When multiple cards form a scroll world, transitions should feel like one continuous camera move.

For still-to-still transitions:
- overlap outgoing/incoming scenes;
- preserve camera velocity;
- keep focal direction coherent;
- keep persistent HUD stable through crossover;
- allow a short blur/signal veil only as support;
- scrolling upward must reverse cleanly.

For video connectors, use frame-identical or visually matched seam frames where possible.

## Story-card contract

Every card must contain:

```yaml
id: string
source_asset: path-or-url
canon_status: locked|approved|proposed
focal_point: { x: 0.0-1.0, y: 0.0-1.0 }
mode: LIVE_STILL|HYBRID|VIDEO_CHAIN
depth_layers:
  base: required
  mid: optional
  near: optional
effects: [] # normally 1-2
interaction:
  type: inspect|choice|unlock|witness|none
  target: optional
payoff:
  type: evidence|access|clue|unlock|interaction|invite|none
mobile:
  pan: optional
  fallback: required
reduced_motion: required
```

## Payoff law

A story card should not consume attention without returning something. When appropriate it gives the player one of:

- evidence;
- a clue;
- access;
- an unlock;
- a new character interaction;
- a theory update;
- an invitation/reward entitlement;
- a meaningful forward question.

Do not manufacture fake rewards. The payoff must have real narrative or product value.

## Performance budget

Target the following before adding complexity:

- no animation work that blocks initial content paint;
- scroll/tilt animation driven by `requestAnimationFrame` or compositor-friendly motion;
- lazy-mount heavy layers;
- lazy-decode images and optional video;
- no permanent high-DPR full-screen Canvas if a small layer works;
- pause atmosphere when card is offscreen;
- pause/reduce work when tab is hidden;
- progressive enhancement based on device capability/preferences;
- measure LCP, INP, CLS, dropped frames, and memory where available.

A WebGL/shader/Rust/WASM layer is not justified until profiling identifies a real bottleneck or visual requirement.

## Card factory workflow

1. **LOCK SOURCE** — identify exact approved image and canonical constraints.
2. **MARK FOCAL DEPTH** — far/mid/near regions and mobile focal point.
3. **NAME STORY JOB** — what must the user feel/notice/learn/do?
4. **CHOOSE 1–2 EFFECTS** — motivated only.
5. **ADD INTERACTION** — only if it changes knowledge/access/route.
6. **DEFINE PAYOFF** — what does attention earn?
7. **BUILD LIVE_STILL** — HTML/CSS/SVG/Canvas first.
8. **MOBILE PASS** — 390x844, touch, reduced motion, low-memory fallback.
9. **SEAM PASS** — if part of a sequence, test forward and reverse scroll.
10. **GAUNTLET** — fresh critic compares against locked source + named interaction/motion reference.
11. **REPAIR SINGLE BIGGEST GAP** — repeat until our implementation wins the comparable task.

## Where's Pauli defaults

For Where's Pauli Episode 001:
- monochrome is default;
- intentional color must have clue meaning;
- Pauli remains inferred unless canon explicitly authorizes a reveal;
- surveillance/HUD should remain minimal;
- image/world is the hero;
- liveness should feel physical and cinematic, not like an animated SaaS card;
- all twelve beats should eventually support the same card contract even when some use authored video.

## Gauntlet acceptance

A card passes only when:

1. it preserves the approved image/canon;
2. it is understandable and interactive on 390x844;
3. its motion clearly improves depth/attention/story rather than decorating it;
4. it remains usable with video/WebGL unavailable;
5. it has a meaningful payoff or deliberate forward question;
6. forward/reverse scroll is stable if sequenced;
7. the critic can name no reference-bar advantage that materially hurts the intended task.

Builder does not self-approve.
