"""Full status check - writes to C:/Users/execu/full_status.txt to avoid E: drive issues."""
import os, subprocess, json

out = []

def chk(label, path):
    out.append(f"{label}: {'YES' if os.path.exists(path) else 'NO'}")

# Key files
chk("registry.json", r"E:\YAPPYVERSE-FACTORY\assets\registry.json")
chk("pauli/CHARACTER_CONFIG.json", r"E:\YAPPYVERSE-FACTORY\assets\pauli\CHARACTER_CONFIG.json")
chk("auto_rig.py", r"E:\YAPPYVERSE-FACTORY\scripts\auto_rig.py")
chk("scan_assets.py", r"E:\YAPPYVERSE-FACTORY\scripts\scan_assets.py")
chk("pipeline.py", r"E:\YAPPYVERSE-FACTORY\scripts\pipeline.py")
chk("graph_config.json", r"E:\YAPPYVERSE-FACTORY\scripts\graph_config.json")
chk(".env", r"E:\YAPPYVERSE-FACTORY\.env")
chk(".git dir", r"E:\YAPPYVERSE-FACTORY\.git")
chk("init_result.txt", r"E:\YAPPYVERSE-FACTORY\init_result.txt")
chk("pauli/manifest.json", r"E:\YAPPYVERSE-FACTORY\assets\pauli\manifest.json")

# Count pauli assets
pauli_ref = r"E:\YAPPYVERSE-FACTORY\assets\pauli\reference"
pauli_anim = r"E:\YAPPYVERSE-FACTORY\assets\pauli\animation"
pauli_audio = r"E:\YAPPYVERSE-FACTORY\assets\pauli\audio"
pauli_nft = r"E:\YAPPYVERSE-FACTORY\assets\pauli\nft"

for cat, p in [("pauli/reference", pauli_ref), ("pauli/animation", pauli_anim), ("pauli/audio", pauli_audio), ("pauli/nft", pauli_nft)]:
    if os.path.exists(p):
        files = [f for f in os.listdir(p) if not f.startswith('.') and not f.endswith('.json')]
        out.append(f"{cat} files: {len(files)}")

# Count total char dirs
assets = r"E:\YAPPYVERSE-FACTORY\assets"
char_dirs = [d for d in os.listdir(assets) if os.path.isdir(os.path.join(assets, d))]
out.append(f"total char dirs: {len(char_dirs)}")
out.append(f"chars: {sorted(char_dirs)}")

# Git status
try:
    r = subprocess.run(["git", "-C", r"E:\YAPPYVERSE-FACTORY", "log", "--oneline", "-3"], capture_output=True, text=True, timeout=10)
    out.append(f"git log: {r.stdout.strip() or r.stderr.strip()}")
except Exception as e:
    out.append(f"git log error: {e}")

try:
    r = subprocess.run(["git", "-C", r"E:\YAPPYVERSE-FACTORY", "remote", "-v"], capture_output=True, text=True, timeout=10)
    out.append(f"git remote: {r.stdout.strip() or 'none'}")
except Exception as e:
    out.append(f"git remote error: {e}")

try:
    r = subprocess.run(["git", "-C", r"E:\YAPPYVERSE-FACTORY", "status", "--short"], capture_output=True, text=True, timeout=10)
    lines = r.stdout.strip().splitlines()
    out.append(f"git status: {len(lines)} uncommitted changes")
    if lines:
        out.append(f"  first few: {lines[:5]}")
except Exception as e:
    out.append(f"git status error: {e}")

# init_result content
if os.path.exists(r"E:\YAPPYVERSE-FACTORY\init_result.txt"):
    with open(r"E:\YAPPYVERSE-FACTORY\init_result.txt") as f:
        out.append("=== init_result.txt ===")
        out.append(f.read()[:1000])

with open(r"C:\Users\execu\full_status.txt", "w") as f:
    f.write("\n".join(out))
