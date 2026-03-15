"""Wire env + cleanup temp files + git init + push."""
import json
import os
import subprocess
import sys

FACTORY = r"E:\YAPPYVERSE-FACTORY"

# ---- 1. Wire .env from master.env ----
MASTER_ENV = r"E:\THE PAULI FILES\master.env"
KEY_MAP = {
    "ANTHROPIC_API_KEY": "ANTHROPIC_API_KEY",
    "OPENAI_API_KEY": "OPENAI_API_KEY",
    "GOOGLE_API_KEY": "GOOGLE_API_KEY",
    "OPEN_ROUTER_API": "OPEN_ROUTER_API",
    "HUGGINGFACE_TOKEN": "HUGGINGFACE_TOKEN",
    "READYPLAYERME_TOKEN": "READYPLAYERME_TOKEN",
    "REPLICATE_API_KEY": "REPLICATE_API_KEY",
    "VERCEL_TOKEN": "VERCEL_TOKEN",
    "GH_PAT": "GH_PAT",
    "SUPABASE_URL": "SUPABASE_URL",
    "SUPABASE_SERVICE_ROLE_KEY_2": "SUPABASE_SERVICE_ROLE_KEY",
}

master_vars = {}
if os.path.exists(MASTER_ENV):
    with open(MASTER_ENV, "r") as f:
        for line in f:
            line = line.strip()
            if "=" in line and not line.startswith("#"):
                k, v = line.split("=", 1)
                master_vars[k.strip()] = v.strip()

env_path = os.path.join(FACTORY, ".env")
with open(env_path, "w") as f:
    f.write("# YAPPYVERSE-FACTORY Environment (auto-generated)\n")
    f.write(f"BLENDER_PATH=C:\\Program Files\\Blender Foundation\\Blender 5.0\\blender.exe\n")
    for src_key, dst_key in KEY_MAP.items():
        val = master_vars.get(src_key, "")
        if val:
            f.write(f"{dst_key}={val}\n")
print(f"[1] .env written: {env_path}")

# ---- 2. Clean temp files ----
TEMPS = [
    "setup_check.py", "test_simple.py", "do_install.py", "download_install.py",
    "extract_install.py", "verify_masf.py", "check.txt", "verify.txt",
    "setup_results.json", "test_out.txt", "pip_install.log", "dir_check.txt",
    "mkdirs_result.txt", "mkdirs2.txt", "scan_pauli.txt",
    "scripts/mkdirs.py", "scripts/mkdirs2.py", "scripts/check_dirs.py", "scripts/list_dirs.py",
]
removed = 0
for t in TEMPS:
    p = os.path.join(FACTORY, t)
    if os.path.exists(p):
        os.remove(p)
        removed += 1
print(f"[2] Cleaned {removed} temp files")

# ---- 3. Git init ----
os.chdir(FACTORY)
def run(cmd):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=FACTORY)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

if not os.path.isdir(os.path.join(FACTORY, ".git")):
    rc, out, err = run(["git", "init"])
    print(f"[3] git init: rc={rc}")
else:
    print("[3] git already initialized")

rc, out, err = run(["git", "add", "-A"])
print(f"[4] git add: rc={rc}")

rc, out, err = run(["git", "commit", "-m", "Initial commit: YAPPYVERSE-FACTORY scaffold + Pauli assets"])
print(f"[5] git commit: rc={rc} {out[:200] if out else err[:200]}")

# ---- 4. Create GitHub repo + push ----
gh_pat = master_vars.get("GH_PAT", "")
if not gh_pat:
    print("[6] SKIP: No GH_PAT found, cannot push to remote")
else:
    import urllib.request
    import urllib.error

    repo_name = "YAPPYVERSE-FACTORY"
    api_url = "https://api.github.com/user/repos"

    data = json.dumps({
        "name": repo_name,
        "description": "YAPPYVERSE Character Factory - MAS-Factory pipeline for 31 characters",
        "private": False,
        "auto_init": False,
    }).encode("utf-8")

    req = urllib.request.Request(api_url, data=data, method="POST")
    req.add_header("Authorization", f"token {gh_pat}")
    req.add_header("Content-Type", "application/json")
    req.add_header("Accept", "application/vnd.github.v3+json")

    try:
        resp = urllib.request.urlopen(req)
        resp_data = json.loads(resp.read())
        clone_url = resp_data.get("clone_url", "")
        print(f"[6] Created GitHub repo: {clone_url}")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        if "already exists" in body.lower():
            print(f"[6] Repo already exists on GitHub")
        else:
            print(f"[6] GitHub API error: {e.code} {body[:200]}")
            clone_url = None

    # Get username
    try:
        req2 = urllib.request.Request("https://api.github.com/user")
        req2.add_header("Authorization", f"token {gh_pat}")
        resp2 = urllib.request.urlopen(req2)
        user = json.loads(resp2.read()).get("login", "")
    except Exception:
        user = ""

    if user:
        remote_url = f"https://{gh_pat}@github.com/{user}/{repo_name}.git"
        # Check if remote exists
        rc, out, err = run(["git", "remote", "get-url", "origin"])
        if rc != 0:
            run(["git", "remote", "add", "origin", remote_url])
        else:
            run(["git", "remote", "set-url", "origin", remote_url])

        rc, out, err = run(["git", "branch", "-M", "main"])
        rc, out, err = run(["git", "push", "-u", "origin", "main"])
        print(f"[7] git push: rc={rc} {out[:200] if out else err[:200]}")
    else:
        print("[7] Could not determine GitHub username")

# Write summary
summary = os.path.join(FACTORY, "init_result.txt")
with open(summary, "w") as f:
    f.write("OK\n")
    f.write(f"env={os.path.exists(env_path)}\n")
    f.write(f"git={os.path.isdir(os.path.join(FACTORY, '.git'))}\n")
    # list files in root
    for item in sorted(os.listdir(FACTORY)):
        if not item.startswith("."):
            f.write(f"  {item}\n")
print("Done. See init_result.txt")
