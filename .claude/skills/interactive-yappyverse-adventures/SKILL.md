---
name: interactive-yappyverse-adventures
description: >
  Builds interactive Pauli/Yappyverse characters, avatars, and choose-your-own-adventure
  digital flipbooks by adapting the high-level interaction model demonstrated by
  mshumer/interactive-sora. Use when turning approved Yappyverse canon, character bibles,
  episodes, clues, or educational/social-purpose content into explorable experiences where
  a player follows characters, inspects evidence, makes choices, and unlocks new media.
  Preserves canon integrity, character visual continuity, provenance, cost controls, and
  human approval gates. Never copies source code or copyrighted story expression from the
  reference project; it extracts only reusable product and systems patterns.
alwaysApply: false
---

# Interactive Yappyverse Adventures

## Source inspiration
Reference implementation: `https://github.com/mshumer/interactive-sora`

The reference demonstrates a useful product pattern: a planner maintains story state, the
player selects a next action, and a fresh cinematic sequence is produced for that branch.
It also supports pre-rendering preset trees so common paths do not need to be generated live.
We use those ideas as architecture inspiration only. Do not copy its code, prompts, UI,
story content, or protected expression.

## Prime directive

Turn a Yappyverse character from a static asset into a **persistent interactive story agent**.
The character may speak, guide, react, reveal evidence, move between scenes, and present
choices, while remaining bound to its approved character bible and the canon/public-knowledge
boundary.

The experience should feel like a living comic, cinematic flipbook, gamebook, and character
conversation merged into one interface.

## Highest-leverage Yappyverse pattern

### The interactive case-file flipbook

Use a digital flipbook as the base container, then make selected pages interactive.

Each experience contains:

1. **Cover / mission card** — one clear question or objective.
2. **Cinematic pages** — approved art, panels, short loops, ambient motion, narration.
3. **Living character pages** — Pauli/Yappyverse avatar can speak, react, or answer within its knowledge boundary.
4. **Evidence pages** — images, maps, receipts, surveillance, witness testimony, objects, clues.
5. **Choice pages** — 2–4 meaningful actions, never decorative buttons.
6. **Branch scenes** — pre-rendered where likely; generated on demand only when useful.
7. **Convergence points** — branches may reveal different evidence while protecting the same locked canon.
8. **Exit question** — every installment ends with a forward mystery or next mission.

## Yappyverse-specific canon rule

**Choice changes the route through the story, not approved truth.**

Maintain two separate graphs:

- `canon_truth_graph` — what is actually true in the Yappyverse.
- `player_knowledge_graph` — what this player has discovered, inferred, misunderstood, or missed.

A choice can change:
- which witness is encountered;
- which character becomes the guide;
- which evidence appears first;
- which clue is missed or unlocked;
- which emotional interpretation becomes likely;
- which optional scene is generated;
- which collectible or replay path becomes available.

A choice must NOT silently change:
- Pauli canon;
- locked character identity;
- approved mission truth;
- established relationships;
- episode outcomes already marked canonical.

Any branch that would mutate canon is `PROPOSED` until human approval.

## Character continuity contract

Before generating an interactive avatar or scene, load the character's authoritative bible.
Minimum continuity state:

```yaml
character_id:
canonical_name:
visual_authority:
voice_authority:
personality_traits:
current_goal:
known_facts:
unknown_facts:
forbidden_reveals:
relationships:
current_location:
wardrobe_or_form:
props:
injuries_or_state:
public_identity_state:
canon_version:
```

Never ask a media model to recreate the character from memory when approved reference assets
exist. Attach or reference the authoritative image/turnaround/style source whenever the
selected generation system supports it.

## Interactive avatar behavior

The avatar is not a generic chatbot wearing a character skin.

It must have:
- bounded knowledge;
- a current scene objective;
- memory of player discoveries;
- emotional state appropriate to the scene;
- explicit things it cannot reveal yet;
- permitted actions/tools;
- consistent voice and visual form;
- a reason for every player choice it offers.

For Pauli specifically, preserve the governing rule:

> The Yappyverse characters may be discovered. Pauli must be inferred.

Do not use this skill as a loophole to produce an early clean Pauli reveal.

## Interaction loop

```text
LOAD CANON
  -> LOAD CHARACTER STATE
  -> LOAD PLAYER KNOWLEDGE
  -> DEFINE CURRENT STORY PRESSURE
  -> GENERATE / SELECT 2–4 MEANINGFUL CHOICES
  -> PLAYER CHOOSES
  -> UPDATE PLAYER-KNOWLEDGE GRAPH
  -> SELECT OR GENERATE NEXT MEDIA BEAT
  -> CHARACTER REACTS
  -> VERIFY CONTINUITY + CANON
  -> RECORD RECEIPT
  -> NEXT PAGE / CONVERGENCE / EXIT QUESTION
```

## Pressure Progression integration

Every branch should still obey the Yappyverse pressure engine:

`Establish Value -> Irregularity -> Restrict Information -> Force Interpretation -> Add Constraint -> Require Decision -> Create Cost -> Partial Progress -> Change Danger/Meaning -> Forward Question`

A branch is weak when the choice is merely navigation. A strong branch changes what the
player risks, knows, believes, loses, or must decide.

## Media strategy: hybrid, not all-live

Do not generate every page live.

Use three layers:

### Layer A — authored / approved
Use for:
- covers;
- hero frames;
- core canon scenes;
- character turnarounds;
- important evidence;
- mandatory story beats.

### Layer B — pre-rendered branches
Use for:
- top likely player choices;
- major witness routes;
- known replay paths;
- mobile/offline-friendly scenes.

### Layer C — generated on demand
Use for:
- uncommon branches;
- optional character reactions;
- personalized connective shots;
- cosmetic/environmental variations that do not change canon.

This preserves cost, latency, visual continuity, and replayability.

## Digital flipbook UI rules

The flipbook is a story surface, not a PDF viewer.

Preferred interaction hierarchy:

1. Full-bleed page or spread.
2. One obvious primary interaction.
3. Character or clue can be touched/clicked only when it matters.
4. Choice tray appears only at decision points.
5. Page-turn motion is fast and interruptible.
6. Audio is optional and user-controlled.
7. Reduced-motion mode must retain all information.
8. Mobile thumb reach and portrait layouts are first-class.
9. Never hide core story comprehension behind tiny hotspots.
10. Replays should expose previously discovered branches without cluttering first play.

## Output modes

This skill may produce:

- interactive Pauli/Yappyverse digital comic;
- choose-your-own-adventure flipbook;
- animated character storybook;
- interactive mystery/case file;
- character-led onboarding experience;
- nonprofit educational adventure;
- sponsor/brand activation story;
- collectible puzzle companion;
- branching social episode;
- interactive children's learning story;
- playable product catalog or fundraising story.

## Commercial pattern

A single authored story can become several products without duplicating canon work:

```text
CANON EPISODE
  -> WEB CINEMATIC
  -> INTERACTIVE FLIPBOOK
  -> SHORT-FORM BRANCH CLIPS
  -> PRINT PUZZLE / BOOK
  -> COLLECTIBLE CLUE CARDS
  -> CHARACTER CHAT / AVATAR EXPERIENCE
  -> SCHOOL / NONPROFIT EDITION
```

The same character bible, story graph, evidence graph, and approved media should power all
surfaces.

## Telemetry worth capturing

Capture only useful product signals:

- branch selected;
- page completed;
- clue inspected;
- replay started;
- character followed;
- abandonment point;
- optional media generated;
- conversion / preorder / donation / signup event when applicable.

Do not invent engagement metrics. Store real events with timestamps and experience/version IDs.

## Cost and latency guardrails

Before live media generation:

1. Check whether an approved or cached branch already exists.
2. Prefer short connective media over long regenerated scenes.
3. Preserve the same first/last visual anchors across a generated continuation.
4. Set a per-session generation budget.
5. Provide a graceful authored fallback if generation fails.
6. Never block the whole story on a media job.
7. Cache successful branch media when rights and privacy allow.

## Acceptance test

An interactive adventure is not complete until all are true:

- [ ] authoritative character bible loaded;
- [ ] canon truth and player knowledge remain separate;
- [ ] every choice has a story consequence;
- [ ] no locked reveal is leaked;
- [ ] visual continuity survives branch transitions;
- [ ] a generation failure has a usable fallback;
- [ ] mobile path is usable;
- [ ] reduced-motion path preserves meaning;
- [ ] branch state can be resumed;
- [ ] event receipts are real, not mock data;
- [ ] replay exposes alternate paths cleanly;
- [ ] final beat creates a forward question or outcome;
- [ ] public/canon changes are human-approved.

## Recommended first Yappyverse implementation

Build **Where's Pauli: Case File 001** as an interactive noir flipbook.

The audience acts as an investigator rather than controlling Pauli. At key pages they choose
which evidence or witness to follow. Yappyverse characters can appear as guides/witnesses and
become increasingly legible, while Pauli remains inferred through evidence. Different paths
reveal different fragments, then converge on the locked episode ending. The player's own
knowledge graph becomes the save state and replay engine.

This is the preferred first implementation because it strengthens the mystery instead of
turning Pauli into a generic game avatar, reuses existing story/art/clue assets, supports the
"audience as Cell 12" concept, creates replay value, and can later become both a paid digital
product and a companion to physical puzzles/collectibles.
