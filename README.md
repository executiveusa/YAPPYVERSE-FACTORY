# YAPPYVERSE Character Factory

Graph-based multi-agent character factory built on MAS-Factory (Vibe Graphing).

## Structure

```
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
├── scripts/
│   ├── auto_rig.py            # Blender headless auto-rig
│   ├── scan_assets.py         # Scan & tag existing images
│   ├── pipeline.py            # Full character pipeline
│   └── graph_config.json      # MAS-Factory graph definition
├── masf-src2/                 # MAS-Factory source (reference)
└── .env                       # Environment variables (git-ignored)
```

## Quick Start

```powershell
$env:PATH = "$env:LOCALAPPDATA\Programs\Python\Python313;$env:LOCALAPPDATA\Programs\Python\Python313\Scripts;$env:PATH"
python scripts/pipeline.py --character pauli
```

## Dependencies

- Python 3.13+ (installed)
- masfactory 1.0.1 (installed)
- Blender 5.0 (installed at C:\Program Files\Blender Foundation\Blender 5.0\)
- Nano Banana 2 (Blender addon - manual install)
