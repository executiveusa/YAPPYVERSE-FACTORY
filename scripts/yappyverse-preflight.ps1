param(
  [Parameter(Mandatory = $true)]
  [string]$RepoPath
)

$ErrorActionPreference = 'Stop'

function Write-Check([string]$Name, [bool]$Ok, [string]$Detail) {
  $status = if ($Ok) { 'PASS' } else { 'FAIL' }
  Write-Host "[$status] $Name - $Detail"
  return $Ok
}

function Get-CommandPath([string]$Name) {
  $cmd = Get-Command $Name -ErrorAction SilentlyContinue
  if ($null -eq $cmd) { return $null }
  return $cmd.Source
}

$failures = 0

if (-not (Test-Path $RepoPath)) {
  Write-Host "[FAIL] repo - path does not exist: $RepoPath"
  exit 2
}

$resolvedRepo = (Resolve-Path $RepoPath).Path
Write-Host "Yappyverse V1 preflight"
Write-Host "Runtime repo: $resolvedRepo"
Write-Host ''

$git = Get-CommandPath 'git'
if (-not (Write-Check 'git' ($null -ne $git) ($(if ($git) { $git } else { 'not found on PATH' })))) { $failures++ }

$just = Get-CommandPath 'just'
if (-not (Write-Check 'just' ($null -ne $just) ($(if ($just) { $just } else { 'not found on PATH' })))) { $failures++ }

$node = Get-CommandPath 'node'
if (-not (Write-Check 'node' ($null -ne $node) ($(if ($node) { $node } else { 'not found on PATH' })))) { $failures++ }

$pnpm = Get-CommandPath 'pnpm'
if (-not (Write-Check 'pnpm' ($null -ne $pnpm) ($(if ($pnpm) { $pnpm } else { 'not found on PATH' })))) { $failures++ }

$cargo = Get-CommandPath 'cargo'
if (-not (Write-Check 'cargo' ($null -ne $cargo) ($(if ($cargo) { $cargo } else { 'not found on PATH' })))) { $failures++ }

$rustc = Get-CommandPath 'rustc'
if (-not (Write-Check 'rustc' ($null -ne $rustc) ($(if ($rustc) { $rustc } else { 'not found on PATH' })))) { $failures++ }

$hermes = Get-CommandPath 'hermes-acp'
if (-not (Write-Check 'hermes-acp' ($null -ne $hermes) ($(if ($hermes) { $hermes } else { 'not found on PATH; Hermes proof cannot run' })))) { $failures++ }

Push-Location $resolvedRepo
try {
  if ($git) {
    $inside = (& git rev-parse --is-inside-work-tree 2>$null)
    if (-not (Write-Check 'git-worktree' ($inside -eq 'true') 'runtime path is a Git worktree')) { $failures++ }

    if ($inside -eq 'true') {
      $remote = (& git remote get-url origin 2>$null)
      $expectedRepo = $remote -match 'executiveusa/pauli-berd(?:\.git)?$'
      if (-not (Write-Check 'runtime-origin' $expectedRepo ($(if ($remote) { $remote } else { 'origin missing' })))) { $failures++ }

      $branch = (& git branch --show-current 2>$null)
      Write-Check 'runtime-branch' $true ($(if ($branch) { $branch } else { 'detached HEAD' })) | Out-Null

      $head = (& git rev-parse HEAD 2>$null)
      Write-Check 'runtime-head' $true $head | Out-Null

      $dirty = (& git status --porcelain 2>$null)
      if (-not (Write-Check 'clean-worktree' ([string]::IsNullOrWhiteSpace(($dirty -join ''))) ($(if ($dirty) { 'uncommitted changes present' } else { 'clean' })))) { $failures++ }
    }
  }

  $justfile = Test-Path (Join-Path $resolvedRepo 'Justfile')
  if (-not (Write-Check 'Justfile' $justfile 'required for canonical Berd build commands')) { $failures++ }

  $tauriConfig = Test-Path (Join-Path $resolvedRepo 'src-tauri/tauri.conf.json')
  if (-not (Write-Check 'Tauri config' $tauriConfig 'src-tauri/tauri.conf.json')) { $failures++ }
}
finally {
  Pop-Location
}

Write-Host ''
if ($failures -gt 0) {
  Write-Host "PRE-INSTALL BLOCKED: $failures failed check(s)."
  Write-Host 'Do not merge or bundle until these checks are resolved and just ci + Hermes UI round trip are green.'
  exit 1
}

Write-Host 'PRE-INSTALL READY: prerequisites are present.'
Write-Host 'Next commands in the runtime repo:'
Write-Host '  just setup'
Write-Host '  just ci'
Write-Host '  just dev'
Write-Host 'Then complete UI -> Hermes -> UI proof before running just bundle.'
exit 0
