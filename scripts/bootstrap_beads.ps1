$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Root

if (-not (Get-Command bd -ErrorAction SilentlyContinue)) {
    Write-Host "[beads] bd not found; installing official gastownhall/beads release..."
    irm https://raw.githubusercontent.com/gastownhall/beads/main/install.ps1 | iex
}

bd version

if (-not (Test-Path (Join-Path $Root ".beads"))) {
    Write-Host "[beads] initializing repository..."
    bd init --quiet
}

try { bd setup codex | Out-Null } catch {}
try { bd setup claude | Out-Null } catch {}

$existing = $null
try { $existing = bd list --json | ConvertFrom-Json } catch {}
$northExists = $false
if ($existing) {
    $northExists = @($existing) | Where-Object { $_.title -like "Yappyverse North Star*" } | ForEach-Object { $true } | Select-Object -First 1
}

if ($northExists) {
    Write-Host "[beads] North Star already seeded; no duplicate created."
}
else {
    Write-Host "[beads] seeding North Star graph..."

    $northRaw = bd create "Yappyverse North Star — owner directs outcomes, agents execute verified work" -p 0 --json
    $northObj = $northRaw | ConvertFrom-Json
    if ($northObj -is [System.Array]) { $northObj = $northObj[0] }
    $NorthId = $northObj.id

    $milestoneRaw = bd create "Milestone 1 — autonomous ASC3ND Why We Started Reel acceptance run" -p 0 --json
    $milestoneObj = $milestoneRaw | ConvertFrom-Json
    if ($milestoneObj -is [System.Array]) { $milestoneObj = $milestoneObj[0] }
    $MilestoneId = $milestoneObj.id

    bd dep add $MilestoneId $NorthId

    bd update $NorthId --description "MODE: operating-system transformation. OUTCOME: owner directs outcomes instead of routing tasks. TARGET: autonomous, sovereign Yappyverse agent network. CONSTRAINTS: Beads mandatory; evidence before claims; cost governed; human gates for publishing/irreversible/high-consequence actions. PROOF: repeated end-to-end verified commercial or mission outcomes without owner task routing. COMMERCIAL VALUE: operating leverage, reusable IP, client delivery, revenue."

    bd update $MilestoneId --description "MODE: production acceptance test. OUTCOME: prepare ASC3ND Wednesday 'Why We Started' Reel end-to-end without owner routing. TARGET: review-ready final MP4 + story/timestamp/cost/QA receipts. CONSTRAINTS: real footage/voice only; no publish before approval; Opus costs tracked; builders cannot self-approve. PROOF: final review MP4, independent taste + truth/privacy verdict, Opus credit delta, caption/post proposal. COMMERCIAL VALUE: proves Yappyverse can autonomously fulfill repeatable client media work."

    Write-Host "[beads] North Star: $NorthId"
    Write-Host "[beads] First milestone: $MilestoneId"
    Write-Host "[beads] Claim the milestone when execution begins: bd update $MilestoneId --claim"
}

bd prime
bd ready --json
Write-Host "[beads] bootstrap complete. Beads is now the mandatory task system for this repo."
