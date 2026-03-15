"""Push YAPPYVERSE-FACTORY to GitHub. Writes result to C:/Users/execu/push_result.txt."""
import subprocess, os

FACTORY = r"E:\YAPPYVERSE-FACTORY"
OUT = r"C:\Users\execu\push_result.txt"
lines = []

def run(cmd, **kw):
    r = subprocess.run(cmd, capture_output=True, text=True, cwd=FACTORY, **kw)
    return r.returncode, r.stdout.strip(), r.stderr.strip()

# Read GH_PAT from .env
gh_pat = None
env_path = os.path.join(FACTORY, ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("GH_PAT="):
                gh_pat = line[7:].strip()
                break

lines.append(f"GH_PAT present: {'YES (len=' + str(len(gh_pat)) + ')' if gh_pat else 'NO'}")

# Check remote URL
rc, remote_url, _ = run(["git", "remote", "get-url", "origin"])
lines.append(f"remote: {remote_url}")

# Embed PAT in remote URL if missing
if gh_pat and remote_url and "github.com" in remote_url and "@" not in remote_url:
    new_url = remote_url.replace("https://", f"https://{gh_pat}@")
    run(["git", "remote", "set-url", "origin", new_url])
    lines.append("embedded PAT in remote URL")

# Remove stale lock
lock = os.path.join(FACTORY, ".git", "index.lock")
if os.path.exists(lock):
    os.remove(lock)
    lines.append("removed stale index.lock")

# Stage pipeline.py and any other new files
rc, out, err = run(["git", "add", "-A"])
lines.append(f"git add rc={rc}")

# Commit if needed
rc, staged, _ = run(["git", "status", "--porcelain"])
if staged.strip():
    rc, out, err = run(["git", "commit", "-m", "Add pipeline.py and remaining factory scripts"])
    lines.append(f"git commit rc={rc}: {out[:120] or err[:120]}")
else:
    lines.append("git commit: nothing new to commit")

# Log last 3 commits
rc, log, _ = run(["git", "log", "--oneline", "-3"])
lines.append(f"git log:\n{log}")

# Push
rc, out, err = run(["git", "push", "-u", "origin", "main"], timeout=300)
lines.append(f"git push rc={rc}")
lines.append(f"stdout: {out[:500]}")
lines.append(f"stderr: {err[:500]}")

with open(OUT, "w") as f:
    f.write("\n".join(lines))
print("done, see", OUT)
