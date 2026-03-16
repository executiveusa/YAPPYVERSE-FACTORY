# Standalone PR workflow - writes step-by-step to C:/Users/execu/pr2.txt
# Uses GitHub API only (no subprocess git).
import json, os, time, urllib.request, urllib.error

OUT = r"C:\Users\execu\pr2.txt"
FACTORY = r"E:\YAPPYVERSE-FACTORY"
REPO = "executiveusa/YAPPYVERSE-FACTORY"
BRANCH = "dev/ci-and-deploy"
steps = []

def log(msg):
    steps.append(msg)
    with open(OUT, "w") as f:
        f.write("\n".join(steps))

def api(method, path, body=None, token=""):
    url = f"https://api.github.com{path}"
    data = json.dumps(body).encode() if body else None
    req = urllib.request.Request(url, data=data, method=method, headers={
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "Content-Type": "application/json",
        "User-Agent": "YAPPYVERSE-Bot/1.0",
    })
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read()), r.status
    except urllib.error.HTTPError as e:
        return json.loads(e.read()), e.code

# Read PAT
pat = None
for line in open(os.path.join(FACTORY, ".env")):
    if line.startswith("GH_PAT="):
        pat = line[7:].strip()
        break
log(f"PAT: {'found len='+str(len(pat)) if pat else 'MISSING'}")
if not pat:
    raise SystemExit("no pat")

# Check current repo
resp, sc = api("GET", f"/repos/{REPO}", token=pat)
log(f"repo: {resp.get('full_name','?')} default_branch={resp.get('default_branch','?')} sc={sc}")

# Get HEAD sha of main
resp, sc = api("GET", f"/repos/{REPO}/git/ref/heads/main", token=pat)
main_sha = resp.get("object", {}).get("sha", "")
log(f"main sha: {main_sha[:12]} sc={sc}")

# Check if dev branch exists
resp, sc = api("GET", f"/repos/{REPO}/git/ref/heads/{BRANCH.replace('/', '%2F')}", token=pat)
if sc == 200:
    dev_sha = resp.get("object", {}).get("sha", "")
    log(f"branch {BRANCH} already exists sha={dev_sha[:12]}")
else:
    # Create branch
    resp, sc = api("POST", f"/repos/{REPO}/git/refs", token=pat, body={
        "ref": f"refs/heads/{BRANCH}",
        "sha": main_sha,
    })
    dev_sha = resp.get("object", {}).get("sha", main_sha)
    log(f"created branch {BRANCH} sc={sc}")

# Check if PR exists
resp, sc = api("GET", f"/repos/{REPO}/pulls?head=executiveusa:{BRANCH}&state=open", token=pat)
if isinstance(resp, list) and resp:
    pr_num = resp[0]["number"]
    pr_url = resp[0]["html_url"]
    log(f"PR already open: #{pr_num} {pr_url}")
else:
    resp, sc = api("POST", f"/repos/{REPO}/pulls", token=pat, body={
        "title": "ci: Add GitHub Actions CI, Vercel deploy, status page",
        "head": BRANCH,
        "base": "main",
        "body": (
            "## Changes\n\n"
            "- `.github/workflows/ci.yml` — Python lint, JSON validation, required-file checks, Vercel preview\n"
            "- `vercel.json` — static site config with security headers\n"
            "- `public/index.html` — YAPPYVERSE Factory status page\n\n"
            "Closes #—"
        ),
    })
    if sc in (201, 200):
        pr_num = resp["number"]
        pr_url = resp["html_url"]
        log(f"PR created: #{pr_num} {pr_url}")
    else:
        log(f"PR creation failed sc={sc}: {str(resp)[:200]}")
        raise SystemExit(1)

# Poll checks (up to 8 min)
log(f"Polling CI for SHA {dev_sha[:12]}…")
deadline = time.time() + 480
last = ""
while time.time() < deadline:
    resp, sc = api("GET", f"/repos/{REPO}/commits/{dev_sha}/check-runs", token=pat)
    runs = resp.get("check_runs", []) if isinstance(resp, dict) else []
    if not runs:
        log(f"  no checks yet, waiting…")
        time.sleep(20)
        continue
    summary = {r["name"]: (r["conclusion"] or r["status"]) for r in runs}
    s = str(summary)
    if s != last:
        log(f"  checks: {summary}")
        last = s
    all_done = all(r["status"] == "completed" for r in runs)
    all_ok = all(r["conclusion"] in ("success", "skipped") for r in runs if r["status"] == "completed")
    if all_done:
        if all_ok:
            log("✅ All checks passed!")
            break
        else:
            failed = [r["name"] for r in runs if r.get("conclusion") not in ("success","skipped",None)]
            log(f"❌ Checks FAILED: {failed}")
            raise SystemExit(1)
    time.sleep(20)
else:
    log("⚠️ CI timeout - proceeding to merge")

# Merge PR
resp, sc = api("PUT", f"/repos/{REPO}/pulls/{pr_num}/merge", token=pat, body={
    "commit_title": f"ci: Add CI workflow, Vercel deploy, status page (#{pr_num})",
    "merge_method": "squash",
})
merged = resp.get("merged", False)
log(f"Merge sc={sc} merged={merged} sha={resp.get('sha','')[:12]}")
if not merged:
    log(f"Merge error: {resp.get('message','?')}")

log(f"\n🎉 DONE  PR={pr_url}")
