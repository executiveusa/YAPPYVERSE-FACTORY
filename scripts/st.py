"""Minimal file-existence check only, no subprocess."""
import os

FACTORY = r"E:\YAPPYVERSE-FACTORY"
lines = []

checks = {
    "CHARACTER_CONFIG.json": r"E:\YAPPYVERSE-FACTORY\assets\pauli\CHARACTER_CONFIG.json",
    "auto_rig.py": r"E:\YAPPYVERSE-FACTORY\scripts\auto_rig.py",
    "scan_assets.py": r"E:\YAPPYVERSE-FACTORY\scripts\scan_assets.py",
    "pipeline.py": r"E:\YAPPYVERSE-FACTORY\scripts\pipeline.py",
    ".env": r"E:\YAPPYVERSE-FACTORY\.env",
    ".git": r"E:\YAPPYVERSE-FACTORY\.git",
    "init_result.txt": r"E:\YAPPYVERSE-FACTORY\init_result.txt",
    "pauli/manifest.json": r"E:\YAPPYVERSE-FACTORY\assets\pauli\manifest.json",
}

for name, path in checks.items():
    lines.append(f"{name}: {'YES' if os.path.exists(path) else 'NO'}")

# Count char dirs
assets = r"E:\YAPPYVERSE-FACTORY\assets"
char_dirs = sorted([d for d in os.listdir(assets) if os.path.isdir(os.path.join(assets, d))])
lines.append(f"char_dirs({len(char_dirs)}): {char_dirs}")

# Pauli asset counts
for cat in ["reference", "mesh", "texture", "rig", "animation", "render", "nft", "audio"]:
    p = os.path.join(assets, "pauli", cat)
    if os.path.exists(p):
        files = [f for f in os.listdir(p) if not f.endswith(".gitkeep")]
        lines.append(f"pauli/{cat}: {len(files)} files")

# init_result content
ir = r"E:\YAPPYVERSE-FACTORY\init_result.txt"
if os.path.exists(ir):
    with open(ir) as f:
        lines.append("=== init_result ===")
        lines.append(f.read()[:800])

with open(r"C:\Users\execu\st.txt", "w") as f:
    f.write("\n".join(lines))
