param(
  [Parameter(Mandatory = $true)]
  [string]$RepoPath,

  [Parameter(Mandatory = $true)]
  [ValidateSet('pass','fail')]
  [string]$JustCi,

  [Parameter(Mandatory = $true)]
  [ValidateSet('pass','fail')]
  [string]$HermesRoundTrip,

  [Parameter(Mandatory = $false)]
  [ValidateSet('pass','fail','not-run')]
  [string]$Bundle = 'not-run',

  [Parameter(Mandatory = $false)]
  [string]$Notes = ''
)

$ErrorActionPreference = 'Stop'

if (-not (Test-Path $RepoPath)) {
  Write-Error "Repo path does not exist: $RepoPath"
  exit 2
}

$resolvedRepo = (Resolve-Path $RepoPath).Path
Push-Location $resolvedRepo
try {
  $origin = (& git remote get-url origin 2>$null)
  $branch = (& git branch --show-current 2>$null)
  $head = (& git rev-parse HEAD 2>$null)
  $dirty = (& git status --porcelain 2>$null)
}
finally {
  Pop-Location
}

$receiptDir = Join-Path $PSScriptRoot '..\evidence\yappyverse'
$receiptDir = [System.IO.Path]::GetFullPath($receiptDir)
New-Item -ItemType Directory -Force -Path $receiptDir | Out-Null

$stamp = Get-Date -Format 'yyyyMMdd-HHmmss'
$receiptPath = Join-Path $receiptDir "acceptance-$stamp.json"

$receipt = [ordered]@{
  schemaVersion = 1
  product = 'Yappyverse'
  slice = 'Hermes-first V1'
  capturedAt = (Get-Date).ToString('o')
  runtime = [ordered]@{
    repoPath = $resolvedRepo
    origin = $origin
    branch = $branch
    head = $head
    cleanWorktree = [string]::IsNullOrWhiteSpace(($dirty -join ''))
  }
  gates = [ordered]@{
    justCi = $JustCi
    hermesRoundTrip = $HermesRoundTrip
    bundle = $Bundle
  }
  acceptance = [ordered]@{
    installReady = (($JustCi -eq 'pass') -and ($HermesRoundTrip -eq 'pass') -and ($Bundle -eq 'pass'))
    mergeReady = (($JustCi -eq 'pass') -and ($HermesRoundTrip -eq 'pass'))
  }
  notes = $Notes
}

$receipt | ConvertTo-Json -Depth 8 | Set-Content -Path $receiptPath -Encoding UTF8

Write-Host "Receipt written: $receiptPath"
Write-Host "Runtime HEAD: $head"
Write-Host "Merge ready: $($receipt.acceptance.mergeReady)"
Write-Host "Install ready: $($receipt.acceptance.installReady)"

if (-not $receipt.acceptance.mergeReady) {
  exit 1
}

exit 0
