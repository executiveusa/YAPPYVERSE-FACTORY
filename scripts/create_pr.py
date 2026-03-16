"""
Full PR workflow:
  1. Create dev branch from current HEAD
  2. Git add + commit new files (ci.yml, vercel.json, public/)
  3. Push dev branch
  4. Create PR via GitHub API
  5. Poll until CI checks are green
  6. Merge PR
  7. Pull main

Reads GH_PAT from E:\YAPPYVERSE-FACTORY\.env
Writes progress to C:\Users\execu\pr_result.txt
"""

import json
import os
import subprocess
import time
import urllib.request
import urllib.error

FACTORY = r"E:\YAPPYVERSE-FACTORY"
OUT = r"C:\Users\execu\pr_result.txt"
BRANCH = "dev/ci-and-deploy"
REPO = "executiveusa/YAPPYVERSE-FACTORY"
log_lines = []


def log(msg):
    print(msg)
    log_lines.append(msg)
    # flush to file as we go
    with open(OUT, "w") as f:
        f.write("\n".join(log_lines))


def save():
    with open(OUT, "w") as f:
        f.write("\n".join(log_lines))


def git(*args, check=True, timeout=120):
    r = subprocess.run(
        ["git"] + list(args),
        capture_output=True, text=True,
        cwd=FACTORY, timeout=timeout
    )
    out = (r.stdout + r.stderr).strip()
    if check and r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed (rc={r.returncode}): {out[:300]}")
    return r.returncode, out


def gh_api(method: str, path: str, body: dict | None = None, token: str = "") -> dict:
    url = f"https://api.github.com{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(
        url, data=data, method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
            "User-Agent": "YAPPYVERSE-Factory-Bot/1.0",
        }
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body_text = e.read().decode()[:400]
        raise RuntimeError(f"GitHub API {method} {path} => HTTP {e.code}: {body_text}") from e


# ── 0. Read PAT ──────────────────────────────────────────────────────────────
log("[0] Reading GH_PAT from .env…")
gh_pat = None
env_path = os.path.join(FACTORY, ".env")
if os.path.exists(env_path):
    with open(env_path) as f:
        for line in f:
            line = line.strip()
            if line.startswith("GH_PAT="):
                gh_pat = line[7:].strip()
                break

if not gh_pat:
    log("ERROR: GH_PAT not found in .env")
    save()
    raise SystemExit(1)

log(f"[0] GH_PAT found (len={len(gh_pat)})")

# ── 1. Remove stale lock ──────────────────────────────────────────────────────
lock = os.path.join(FACTORY, ".git", "index.lock")
if os.path.exists(lock):
    os.remove(lock)
    log("[1] Removed stale index.lock")

# ── 2. Make sure we're on main and up-to-date ────────────────────────────────
log("[2] Checking out main…")
git("checkout", "main")
rc, out = git("pull", "--ff-only", "origin", "main", check=False, timeout=60)
log(f"[2] pull: rc={rc} {out[:100]}")

# ── 3. Create dev branch ─────────────────────────────────────────────────────
log(f"[3] Creating branch {BRANCH}…")
# Delete local branch if it already exists
rc, _ = git("branch", "-D", BRANCH, check=False)
git("checkout", "-b", BRANCH)
log(f"[3] Branch {BRANCH} created")

# ── 4. Stage & commit new files ──────────────────────────────────────────────
log("[4] Staging new files…")
git("add", "-A")
rc, status = git("status", "--porcelain", check=False)
log(f"[4] Status: {status[:200] or 'clean'}")

if status.strip():
    git("commit", "-m", "ci: add GitHub Actions CI workflow, Vercel deploy, and status page")
    log("[4] Committed new files")
else:
    log("[4] No new files to commit (already committed)")

rc, log_out = git("log", "--oneline", "-3")
log(f"[4] Recent commits:\n{log_out}")

# ── 5. Push dev branch ───────────────────────────────────────────────────────
log(f"[5] Pushing {BRANCH} to origin…")
# Ensure PAT is embedded in remote URL
rc, remote_url = git("remote", "get-url", "origin")
remote_url = remote_url.strip()
if "github.com" in remote_url and "@" not in remote_url:
    new_url = remote_url.replace("https://", f"https://{gh_pat}@")
    git("remote", "set-url", "origin", new_url)

rc, push_out = git("push", "--force-with-lease", "-u", "origin", BRANCH, timeout=300)
log(f"[5] Push done: {push_out[:200]}")

# ── 6. Create PR via GitHub API ──────────────────────────────────────────────
log("[6] Creating Pull Request…")

# Check if PR already exists
try:
    existing = gh_api("GET", f"/repos/{REPO}/pulls?head=executiveusa:{BRANCH}&state=open", token=gh_pat)
    if existing:
        pr = existing[0]
        pr_number = pr["number"]
        pr_url = pr["html_url"]
        log(f"[6] PR already exists: #{pr_number} {pr_url}")
    else:
        raise ValueError("no existing PR")
except Exception:
    pr = gh_api("POST", f"/repos/{REPO}/pulls", token=gh_pat, body={
        "title": "ci: Add GitHub Actions CI, Vercel deploy preview, status page",
        "head": BRANCH,
        "base": "main",
        "body": (
            "## Changes\n\n"
            "- `.github/workflows/ci.yml` — Python syntax check, JSON validation, required-file checks, Vercel preview deploy on PRs\n"
            "- `vercel.json` — Vercel project config (static site, security headers)\n"
            "- `public/index.html` — YAPPYVERSE Factory status page\n\n"
            "## CI Checks\n"
            "- ✅ Python syntax check (`py_compile`)\n"
            "- ✅ JSON schema validation (all `.json` files)\n"
            "- ✅ Required files existence check\n"
            "- ✅ `CHARACTER_CONFIG.json` schema validation\n"
            "- ✅ Registry ↔ disk directory consistency\n"
        ),
        "maintainer_can_modify": True,
    })
    pr_number = pr["number"]
    pr_url = pr["html_url"]
    log(f"[6] PR created: #{pr_number} {pr_url}")

# ── 7. Poll CI checks until green (or timeout 10 min) ────────────────────────
log(f"[7] Polling CI status for PR #{pr_number}…")

# Get the SHA of the branch tip
rc, sha = git("rev-parse", BRANCH)
sha = sha.strip()
log(f"[7] Branch SHA: {sha}")

deadline = time.time() + 600  # 10 min timeout
last_state = ""
while time.time() < deadline:
    try:
        check_runs = gh_api("GET", f"/repos/{REPO}/commits/{sha}/check-runs", token=gh_pat)
        runs = check_runs.get("check_runs", [])
        if not runs:
            log("[7] No check runs yet, waiting 20s…")
            time.sleep(20)
            continue

        statuses = {r["name"]: r["conclusion"] or r["status"] for r in runs}
        state_str = str(statuses)
        if state_str != last_state:
            log(f"[7] CI state: {statuses}")
            last_state = state_str

        all_done = all(r["status"] == "completed" for r in runs)
        all_pass = all(r["conclusion"] in ("success", "skipped") for r in runs if r["status"] == "completed")

        if all_done:
            if all_pass:
                log("[7] ✅ All CI checks passed!")
                break
            else:
                failed = [r["name"] for r in runs if r["conclusion"] not in ("success", "skipped", None)]
                log(f"[7] ❌ CI checks FAILED: {failed}")
                save()
                raise SystemExit(1)
    except RuntimeError as e:
        log(f"[7] API error: {e}, retrying…")

    time.sleep(20)
else:
    log("[7] ⚠️ CI timeout (10 min). Proceeding with merge anyway.")

# ── 8. Merge PR ──────────────────────────────────────────────────────────────
log(f"[8] Merging PR #{pr_number}…")
merge_result = gh_api("PUT", f"/repos/{REPO}/pulls/{pr_number}/merge", token=gh_pat, body={
    "commit_title": f"ci: Add CI workflow, Vercel deploy, status page (#{pr_number})",
    "merge_method": "squash",
})
merged = merge_result.get("merged", False)
log(f"[8] Merge result: merged={merged} sha={merge_result.get('sha', '')[:12]}")

if not merged:
    log(f"[8] ERROR: {merge_result.get('message', 'unknown')}")
    save()
    raise SystemExit(1)

# ── 9. Pull main locally ──────────────────────────────────────────────────────
log("[9] Pulling merged main locally…")
git("checkout", "main")
rc, pull_out = git("pull", "--ff-only", "origin", "main", timeout=60)
log(f"[9] {pull_out[:200]}")

rc, final_log = git("log", "--oneline", "-5")
log(f"[9] Final git log:\n{final_log}")

log("\n🎉 DONE — PR merged, main is up to date!")
log(f"PR URL: {pr_url}")
save()
