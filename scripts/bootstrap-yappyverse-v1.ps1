param(
  [Parameter(Mandatory = $false)]
  [string]$InstallRoot = "$HOME\Yappyverse",

  [Parameter(Mandatory = $false)]
  [string]$RuntimeBranch = "feature/yappyverse-hermes-wire-v1"
)

$ErrorActionPreference = 'Stop'

$factoryRepo = 'https://github.com/executiveusa/YAPPYVERSE-FACTORY.git'
$runtimeRepo = 'https://github.com/executiveusa/pauli-berd.git'

$factoryPath = Join-Path $InstallRoot 'YAPPYVERSE-FACTORY'
$runtimePath = Join-Path $InstallRoot 'pauli-berd'

function Require-Command([string]$Name) {
  $cmd = Get-Command $Name -ErrorAction SilentlyContinue
  if ($null -eq $cmd) {
    throw "Required command '$Name' is not available on PATH."
  }
}

Require-Command 'git'

New-Item -ItemType Directory -Force -Path $InstallRoot | Out-Null

if (-not (Test-Path $factoryPath)) {
  git clone $factoryRepo $factoryPath
} else {
  Push-Location $factoryPath
  try {
    git fetch origin
    git checkout main
    git pull --ff-only origin main
  }
  finally { Pop-Location }
}

if (-not (Test-Path $runtimePath)) {
  git clone $runtimeRepo $runtimePath
}

Push-Location $runtimePath
try {
  git fetch origin
  git checkout $RuntimeBranch
  git pull --ff-only origin $RuntimeBranch
  Write-Host "Runtime branch: $RuntimeBranch"
  Write-Host "Runtime HEAD: $(git rev-parse HEAD)"
}
finally { Pop-Location }

$preflight = Join-Path $factoryPath 'scripts\yappyverse-preflight.ps1'
if (-not (Test-Path $preflight)) {
  throw "Preflight script missing from factory checkout: $preflight"
}

& powershell -ExecutionPolicy Bypass -File $preflight -RepoPath $runtimePath
if ($LASTEXITCODE -ne 0) {
  throw 'Yappyverse preflight failed. Resolve the reported prerequisite(s) before continuing.'
}

Write-Host ''
Write-Host 'BOOTSTRAP COMPLETE.'
Write-Host "Factory: $factoryPath"
Write-Host "Runtime: $runtimePath"
Write-Host ''
Write-Host 'Next, from the runtime directory:'
Write-Host '  just setup'
Write-Host '  just ci'
Write-Host '  just dev'
Write-Host ''
Write-Host 'Then perform the real Yappyverse UI -> Hermes -> UI round trip.'
Write-Host 'Do NOT merge or bundle before that proof is green.'
