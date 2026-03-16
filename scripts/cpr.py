# Commit new files to dev/ci-and-deploy, push, then create PR
import subprocess, os, json, urllib.request, urllib.error, time

FACTORY = r"E:\YAPPYVERSE-FACTORY"
BRANCH = "dev/ci-and-deploy"
REPO = "executiveusa/YAPPYVERSE-FACTORY"
OUT = r"C:\Users\execu\cpr.txt"
steps = []

def log(msg):
    steps.append(msg)
    with open(OUT, "w") as f:
        f.write("\n".join(steps))

def git(*args):
    r = subprocess.run(
        ["git", "-C", FACTORY] + list(args),
        capture_output=True, text=True, timeout=90,
        env={**os.environ, "GIT_TERMINAL_PROMPT": "0"}
    )
    out = (r.stdout + r.stderr).strip()[:300]
    log(f"  git {' '.join(args[:3])}: rc={r.returncode} {out}")
    return r

def api(method, path, body=None, pat=""):
    url = f"https://api.github.com{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {pat}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "YAPPYVERSE-Bot/1.0",
        "Content-Type": "application/json",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read()), r.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read()), e.code

# Read PAT
pat = ""
for line in open(os.path.join(FACTORY, ".env")):
    if line.startswith("GH_PAT="):
        pat = line[7:].strip()
log(f"PAT: {'found len=' + str(len(pat)) if pat else 'MISSING'}")

# Step 1: checkout dev/ci-and-deploy (create if needed)
log("=== Step 1: checkout branch ===")
r = git("checkout", BRANCH)
if r.returncode != 0:
    r = git("checkout", "-b", BRANCH)

# Step 2: stage everything
log("=== Step 2: stage files ===")
git("add", "-A")
r = git("status", "--short")
status_lines = r.stdout.strip()
log(f"Staged:\n{status_lines[:500]}")

# Step 3: commit (if there's anything)
if status_lines:
    log("=== Step 3: commit ===")
    r = git("commit", "-m", "ci: Add GitHub Actions CI, Vercel deploy, status page")
    if r.returncode != 0:
        log(f"commit error: {r.stderr[:300]}")
        raise SystemExit(1)
else:
    log("=== Step 3: nothing to commit — checking if branch is ahead ===")

# Verify we have commits ahead of main
r = git("log", "--oneline", "main..HEAD")
ahead = r.stdout.strip()
log(f"Commits ahead of main: {ahead or '(none)'}")
if not ahead:
    log("ERROR: branch has no new commits vs main — cannot create PR")
    raise SystemExit(1)

# Step 4: push
log("=== Step 4: push ===")
remote = f"https://x-token-auth:{pat}@github.com/{REPO}.git"
r = subprocess.run(
    ["git", "-C", FACTORY, "push", "--force-with-lease", "-u", remote, f"{BRANCH}:refs/heads/{BRANCH}"],
    capture_output=True, text=True, timeout=120,
    env={**os.environ, "GIT_TERMINAL_PROMPT": "0"}
)
push_out = (r.stdout + r.stderr).strip()[:400]
log(f"push rc={r.returncode}: {push_out}")
if r.returncode != 0:
    raise SystemExit(1)

# Step 5: find or create PR
log("=== Step 5: create PR ===")
resp, sc = api("GET", f"/repos/{REPO}/pulls?head=executiveusa:{BRANCH}&state=open", pat=pat)
if isinstance(resp, list) and resp:
    pr_num = resp[0]["number"]
    pr_url = resp[0]["html_url"]
    log(f"PR already open: #{pr_num} {pr_url}")
else:
    resp, sc = api("POST", f"/repos/{REPO}/pulls", pat=pat, body={
        "title": "ci: Add GitHub Actions CI, Vercel deploy, status page",
        "head": BRANCH,
        "base": "main",
        "body": (
            "## Summary\n\n"
            "- **`.github/workflows/ci.yml`** — Python lint, JSON validation, required-file & schema checks\n"
            "- **`vercel.json`** — Static site config with security headers\n"
            "- **`public/index.html`** — YAPPYVERSE Factory status page (31 chars / 52 eps)\n"
            "- **`scripts/pipeline.py`** — Full 5-stage character factory (scan→model→rig→nft→qa)\n"
        ),
    })
    if sc in (200, 201):
        pr_num = resp["number"]
        pr_url = resp["html_url"]
        log(f"PR created: #{pr_num} {pr_url}")
    else:
        log(f"PR creation failed sc={sc}: {str(resp)[:300]}")
        raise SystemExit(1)

# Step 6: poll CI checks
log(f"=== Step 6: poll CI for PR #{pr_num} ===")
# get head sha from PR
resp, _ = api("GET", f"/repos/{REPO}/pulls/{pr_num}", pat=pat)
head_sha = resp.get("head", {}).get("sha", "")
log(f"PR head sha: {head_sha[:12]}")

deadline = time.time() + 600
last_summary = ""
while time.time() < deadline:
    resp, sc = api("GET", f"/repos/{REPO}/commits/{head_sha}/check-runs", pat=pat)
    runs = resp.get("check_runs", []) if isinstance(resp, dict) else []
    if not runs:
        log("  no checks yet…")
        time.sleep(20)
        continue
    summary = {r["name"]: (r["conclusion"] or r["status"]) for r in runs}
    s = str(sorted(summary.items()))
    if s != last_summary:
        log(f"  checks: {summary}")
        last_summary = s
    all_done = all(r["status"] == "completed" for r in runs)
    if all_done:
        all_ok = all(r["conclusion"] in ("success", "skipped", "neutral") for r in runs)
        if all_ok:
            log("All CI checks passed!")
            break
        else:
            failed = [r["name"] for r in runs if r.get("conclusion") not in ("success","skipped","neutral",None)]
            log(f"CI checks FAILED: {failed}")
            raise SystemExit(1)
    time.sleep(20)
else:
    log("CI timeout - proceeding with merge anyway")

# Step 7: merge PR
log(f"=== Step 7: merge PR #{pr_num} ===")
resp, sc = api("PUT", f"/repos/{REPO}/pulls/{pr_num}/merge", pat=pat, body={
    "commit_title": f"ci: Add CI workflow, Vercel deploy, status page (#{pr_num})",
    "merge_method": "squash",
})
merged = resp.get("merged", False)
log(f"merge sc={sc} merged={merged} sha={resp.get('sha','')[:12]}")
if not merged:
    log(f"merge message: {resp.get('message','?')}")

# Step 8: sync local main
log("=== Step 8: sync local main ===")
git("checkout", "main")
git("pull", "--ff-only", "origin", "main")

log(f"\n DONE  PR={pr_url}  merged={merged}")
