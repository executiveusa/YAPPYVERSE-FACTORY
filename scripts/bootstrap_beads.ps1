$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Set-Location $Root

$NorthTitle = "Yappyverse North Star — owner directs outcomes, agents execute verified work"
$MilestoneTitle = "Milestone 1 — autonomous ASC3ND Why We Started Reel acceptance run"

if (-not (Get-Command bd -ErrorAction SilentlyContinue)) {
    Write-Error @"
[beads] bd is not installed.
Install Beads from an official, checksum-verified gastownhall/beads release,
then re-run this script. Do not pipe mutable remote installer content to PowerShell.
Official releases: https://github.com/gastownhall/beads/releases
"@
    exit 2
}

bd version

if (-not (Test-Path (Join-Path $Root ".beads"))) {
    Write-Host "[beads] initializing repository..."
    bd init --quiet
}

try { bd setup codex | Out-Null } catch {}
try { bd setup claude | Out-Null } catch {}

function Get-BeadByTitle([string]$Title) {
    $items = bd list --json | ConvertFrom-Json
    return @($items) | Where-Object { $_.title -eq $Title } | Select-Object -First 1
}

function New-Bead([string]$Title, [int]$Priority = 0, [string]$Parent = "") {
    if ($Parent) {
        $obj = bd create $Title -p $Priority --parent $Parent --json | ConvertFrom-Json
    }
    else {
        $obj = bd create $Title -p $Priority -t epic --json | ConvertFrom-Json
    }
    if ($obj -is [System.Array]) { return $obj[0] }
    return $obj
}

Write-Host "[beads] reconciling North Star graph..."
$North = Get-BeadByTitle $NorthTitle
if (-not $North) { $North = New-Bead $NorthTitle 0 }
$NorthId = $North.id

$Milestone = Get-BeadByTitle $MilestoneTitle
if (-not $Milestone) { $Milestone = New-Bead $MilestoneTitle 0 $NorthId }
$MilestoneId = $Milestone.id

bd update $NorthId --description "MODE: operating-system transformation. OUTCOME: owner directs outcomes instead of routing tasks. TARGET: autonomous, sovereign Yappyverse agent network. CONSTRAINTS: Beads mandatory; evidence before claims; cost governed; human gates for publishing/irreversible/high-consequence actions. PROOF: repeated end-to-end verified commercial or mission outcomes without owner task routing. COMMERCIAL VALUE: operating leverage, reusable IP, client delivery, revenue."

bd update $MilestoneId --description "MODE: production acceptance test. OUTCOME: prepare ASC3ND Wednesday 'Why We Started' Reel end-to-end without owner routing. TARGET: review-ready final MP4 + story/timestamp/cost/QA receipts. CONSTRAINTS: real footage/voice only; no publish before approval; Opus costs tracked; builders cannot self-approve. PROOF: final review MP4, independent taste + truth/privacy verdict, Opus credit delta, caption/post proposal. COMMERCIAL VALUE: proves Yappyverse can autonomously fulfill repeatable client media work."

# Reconcile relation type. Earlier bootstrap logic used the default `blocks`
# dependency, which would keep the milestone off `bd ready` while the North Star
# remains open. Parent-child preserves hierarchy without turning the governing
# outcome into a sequential prerequisite.
try { bd dep remove $MilestoneId $NorthId | Out-Null } catch {}
bd dep add $MilestoneId $NorthId --type parent-child

Write-Host "[beads] North Star: $NorthId"
Write-Host "[beads] First milestone: $MilestoneId"
Write-Host "[beads] Claim the milestone when execution begins: bd update $MilestoneId --claim"

bd prime
bd ready --json
Write-Host "[beads] bootstrap complete. Beads is now the mandatory task system for this repo."
