# YAPPYVERSE — Pauli Gravity & Mission Cell Canon

## Status
LOCKED SHARED STORY RULE

## Core rule
The Yappyverse characters may be discovered. **Pauli must be inferred.**

Pauli is the singular mystery character at the center of the universe. Other Yappyverse characters may be visually and emotionally revealed much sooner. Their personalities, relationships, humor, fears, skills, and individual missions can become legible to the audience while Pauli remains unresolved.

Every major Yappyverse character eventually reveals another edge of the Pauli graph.

## Pauli Gravity Rule
Each major Yappyverse character must satisfy three conditions:

1. They are interesting enough to carry scenes without Pauli.
2. Their existence reinforces the Pauli mystery without explaining it.
3. They possess at least one hidden relationship to Pauli that is revealed later.

Pauli may mean something different to each character:
- recruiter;
- rumor;
- rescuer;
- strategist;
- voice on a line;
- myth;
- threat;
- benefactor;
- anonymous handler;
- person they never knowingly met;
- organization they mistakenly believe exists;
- someone whose instructions arrived through another intermediary.

Different characters can hold mutually incompatible beliefs about Pauli and still each possess part of the truth.

## Mission Cell Rule
The Yappyverse mission is intentionally compartmentalized.

The future-origin team was not briefed as one unified group. Each operative or small cell was selected, contacted, trained, and debriefed separately on a strict need-to-know basis.

Reason inside canon:
- capture of one operative must not expose the whole mission;
- interrogation or coercion must not compromise unrelated cells;
- no single field character should be able to identify every other operative;
- no single field character should know the complete plan;
- some characters may not know Pauli was the person who selected or activated them;
- some may receive instructions through aliases, dead drops, intermediaries, recordings, objects, coded locations, or future systems;
- some may believe they were recruited by entirely different people or organizations.

This is not merely a security procedure. It is a story engine.

## The Hidden Connection Twist
At first, the audience should read the cast as independent characters with separate stories.

Over time, repeated motifs, behaviors, objects, locations, phrases, mission outcomes, and impossible coincidences reveal hidden edges between them.

The eventual realization is:

> They were never random people moving through separate stories. They were individually selected pieces of the same mission.

The deeper realization may come later:

> Several of them did not know Pauli had selected them at all.

## Public Graph vs Canon Graph
Story planning must track two simultaneous graphs.

### Public graph
What the audience currently knows or reasonably believes.

Example:
```json
{
  "source": "character_a",
  "edge": "SEEN_AT",
  "target": "pioneer_square",
  "visibility": "public",
  "revealed_episode": 2
}
```

### Canon graph
What is actually true in the story room.

Example:
```json
{
  "source": "character_a",
  "edge": "PROTECTS",
  "target": "pauli",
  "visibility": "secret",
  "reveal_window": "later"
}
```

Every important hidden relationship should also track the audience's current interpretation.

Example:
```json
{
  "source": "character_a",
  "target": "pauli",
  "true_relationship": "PROTECTS",
  "audience_interpretation": "HUNTING",
  "introduced_episode": 3,
  "truth_reveal_episode": null
}
```

## Character opacity hierarchy
### Pauli
- maximum mystery;
- no conventional early reveal;
- contradictory descriptions encouraged;
- motives and origin remain partially unresolved even after first verified sighting.

### Core Yappyverse characters
- may be visually revealed early;
- personalities and individual stakes should become understandable;
- their connection to Pauli remains hidden longer than their identity.

### Secondary Yappyverse characters
- may be more immediately legible;
- provide humor, warmth, conflict, testimony, misdirection, and regional texture.

### Humans
- generally provide the clearest audience anchors;
- often misunderstand future-origin or shapeshifter behavior.

### Opposition network
- individual agents may become visible;
- the institution, command structure, and future agenda remain harder to identify.

## Compartmentalized Truth Rule
No major operative receives the complete truth at recruitment.

Each character should have:
- a mission they believe they are performing;
- a reason they accepted it;
- a limited set of known allies;
- at least one incorrect assumption;
- at least one withheld fact;
- at least one later revelation showing how their assignment connected to someone else's.

This allows characters to truthfully deny knowledge of Pauli, one another, or the full mission.

## Misdirection & Magic Rule
The universe may use the structural pleasures of stage magic and caper mysteries:
- attention is directed toward the wrong detail while the important action happens elsewhere;
- an apparent failure may be a planned success;
- an apparent coincidence may later reveal coordination;
- separate actions may be parts of one larger operation;
- a character who appears to be the target may actually be the distraction;
- the audience should be able to replay earlier episodes and see that the evidence was present.

The magic is in **misdirection, timing, concealment, staging, perception, and reveal** — not supernatural exposition for its own sake.

Do not copy plots, dialogue, characters, tricks, scenes, or distinctive expression from existing films. Use only general principles of misdirection, ensemble coordination, compartmentalized knowledge, delayed revelation, and recontextualization.

## Sasquatch / Pauli distinction
Real-world Sasquatch witness material primarily enriches the Pauli mystery graph. It should not force every Yappyverse character into the same cryptid-research framework.

Pauli carries the strongest real-world cryptid parallel:
- contradictory eyewitness descriptions;
- physical traces;
- disputed sightings;
- folklore;
- official skepticism;
- unexplained evidence;
- belief revision.

Other Yappyverse characters may draw from different animal, regional, historical, cultural, scientific, or folkloric source banks.

## Production requirement
For every major character, maintain:
- `public_identity`
- `true_identity`
- `public_relationship_to_pauli`
- `true_relationship_to_pauli`
- `who_recruited_them_as_they_understand_it`
- `who_actually_recruited_them`
- `mission_they_believe_they_have`
- `actual_mission_role`
- `known_allies`
- `unknown_allies`
- `false_assumption`
- `withheld_fact`
- `reveal_window`
- `recontextualized_episode`

## North-star line
> The Yappyverse characters may be discovered. Pauli must be inferred.

And:

> Every major character eventually reveals another edge of the Pauli graph.
