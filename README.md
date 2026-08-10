# YAPPYVERSE Character Factory

Graph-based multi-agent character factory built on MAS-Factory (Vibe Graphing).

## North Star

Yappyverse exists so the owner can **direct outcomes instead of managing tasks** while an owned network of agents turns ideas, client needs, and intellectual property into verified media, software, campaigns, and revenue.

Governance sources:

- `EMERALD_TABLETS.md` — original constitutional operating system
- `EMERALD_TABLETS_AMENDMENT_01.md` — August 2026 North Star / Digital Cofounder / mandatory Beads amendment; later owner directive controls where provisions conflict
- `docs/NORTH_STAR.md` — governing goal and measurable definition of success
- `docs/BEADS_POLICY.md` — mandatory work-tracking policy

## Pauliverse operating layer

`Pauliverse` is an internal systems term for the connected portfolio of repositories, agents, IP, commercial systems, and social-purpose work. For cross-repository work, read:

- `docs/pauliverse/PAULIVERSE-OPERATING-CONTRACT.md` — repo-as-node model, ICM portability, master ontology, signal/noise filter, adversarial decision passes, and portfolio triage.
- `docs/pauliverse/PAULIS-PLACE-FINANCIAL-HANDOFF.md` — mandatory routing contract for financial opportunities to Pauli's Place.
- `docs/pauliverse/MISSION-001-PAULIVERSE-COMMAND-WORLD.md` — active gauntlet mission for the extended working prototype, hardened cross-node connections, and Pauli's Place 3D observation cockpit.

YAPPYVERSE-FACTORY remains the character/media factory; it does not become the canonical financial ledger or the authoritative home for every portfolio fact.

## Structure

```text
E:\YAPPYVERSE-FACTORY\
├── assets/                    # Canonical character assets
│   ├── registry.json          # Master asset registry
│   └── pauli/                 # Per-character directories
│       ├── CHARACTER_CONFIG.json
│       ├── reference/
│       ├── mesh/
│       ├── texture/
│       ├── rig/
│       ├── animation/
│       ├── render/
│       ├── nft/
│       └── audio/
├── docs/
│   ├── NORTH_STAR.md
│   └── BEADS_POLICY.md
├── scripts/
│   ├── auto_rig.py            # Blender headless auto-rig
│   ├── scan_assets.py         # Scan & tag existing images
│   ├── pipeline.py            # Full character pipeline implementation
│   ├── run_pipeline_with_bead.py # Required production entrypoint
│   ├── beads_guard.py         # Fail-closed active-Bead validation
│   ├── bootstrap_beads.ps1    # Windows Beads bootstrap
│   ├── bootstrap_beads.sh     # Linux/macOS/WSL Beads bootstrap
│   └── graph_config.json      # MAS-Factory graph definition
├── masf-src2/                 # MAS-Factory source (reference)
└── .env                       # Environment variables (git-ignored)
```

## First-time setup: Beads

Beads is mandatory for substantive Yappyverse work.

### Windows

```powershell
powershell -ExecutionPolicy Bypass -File scripts/bootstrap_beads.ps1
```

### Linux / macOS / WSL

```bash
bash scripts/bootstrap_beads.sh
```

The bootstrap initializes `.beads/`, configures supported agent integrations, and seeds the Yappyverse North Star plus the first autonomous ASC3ND Reel acceptance milestone.

## Production quick start

Set or pass an active Bead ID. Production work should use the guarded entrypoint:

```powershell
$env:BEAD_ID = "<active-bead-id>"
python scripts/run_pipeline_with_bead.py --character pauli
```

or:

```powershell
python scripts/run_pipeline_with_bead.py --bead-id <active-bead-id> --character pauli
```

The guard refuses mutating execution when `bd` is missing, `.beads/` is not initialized, or the supplied Bead ID cannot be resolved.

## Dependencies

- Python 3.13+
- masfactory 1.0.1
- Blender 5.0
- Beads (`bd`) for all production work
- Nano Banana 2 Blender addon where that workflow is used