# ARCHON X — Character Summary (v1, pending Bambu approval)
Source chats: "Archon X Concept Design" (archon-x, 10 msgs, 22.6k chars; verbatim: part1 file + inline-read tail, export backfills).
IDENTITY NOTE: Archon X is Bambu's own captain-seat persona in the fleet - "THE CAPTAIN: a Black man with a short textured afro in a tall peacock-style wicker chair", viewed from behind on the command bridge. This is the flagship/world-builder identity, not a side character.

## The Archon X world
- Command ship bridge: luxury noir sci-fi, anime-influenced; giant circular viewport (60% of frame) onto a teal-blue spiral galaxy, Earth small but growing (ship approaching Earth); cathedral-arch walls, mechanical pipes, console panels with teal/amber buttons; haze catching teal light.
- TITLE RULES: "ARCHON X" with a SPACE (not "ARCHONX"), glowing teal futuristic sans-serif, X tinted gold. Palette LOCKED: void navy-black #010818; teal/cyan #00c8e8-#00eeff; gold #f5c842 (X only); amber #c07a00 (console accents). Strictly cold teal on black. Mood: oracle's throne room merged with a starship bridge. "The ship runs on meaning, not code."
- SIX MODULE CARDS (his product line): REMOTION (play), TRADING AGENTS (chart), NOTEGEN (microphone), MEDIAGRAWLER (monitor), ML FOR BEGINNERS (globe), DREAMGRAFTED (star).
- Image-iteration lesson (his direction style): preserve the original photo exactly; single-variable edits only ("DO NOT CHANGE ANYTHING ELSE"). The chair-height fight is a documented case of image-model drift on iterative edits.

## THE CHESS ROOM (agent orchestration = the StarNet seat concept's origin)
- Chess board as tactical command bridge: CHESS PIECES ARE AGENTS, watched making moves and working together. Viewing-room/sphere logic referenced from AKASHPORTFOLIO (the Mexico project - READ ONLY reference: sphere layout, observer model, camera behavior).
- Stack: Rust engine (/engine/chess + /agents + /events bus + /state + /voice tts_adapter + /config secrets), Tauri or Bevy web export, event bus (AgentProposedMove/AgentCommittedMove/AgentSpoke/MemoGenerated/BoardUpdated), deterministic test mode, feature flags (ARCHONX_CHESS_ROOM_ENABLED, ARCHONX_TTS_ENABLED default OFF), timeout+token budgets per agent, fail-safe degradation, audit trail per move (timestamp/agent/rationale/result), TTS via 11labs with provider abstraction.
- Repos named: executiveusa/archonx-os (the build), executiveusa/AKASHPORTFOLIO (reference), executiveusa/pauli-sercets-vault- (secrets vault repo).
- Agent behavior model: each agent has confidence_score, risk_score, move_priority, debate_state; supports propose/defend/revise/concede - THIS IS THE COUNCIL/DEBATE PATTERN now live in pauli-command-center.
- His prompt-engineering artifact: "ARCHON X PATCH PROMPT v2.0" - hardened handoff prompt with mandatory 11-section output format, production hardening rules, non-destructive patch discipline. Worth archiving as his canonical handoff-prompt template.

## Relationships
- Archon X = the captain; agents = his pieces. Emerald Tablets (SYNTHIA systems-thinking) is the operating philosophy: stocks/flows/feedback loops/constraints.
- Emerald Tablets doc also lives in YAPPYVERSE-FACTORY governance (EMERALD_TABLETS.md) - same canon spine.

## Assets: 7 images in chat (URLs captured); pull pending (dedicated image run).
