$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$pythonPath = Join-Path $root ".venv\\Scripts\\python.exe"

if (-not (Test-Path $pythonPath)) {
    throw "Python virtual environment not found. Run scripts/bootstrap.ps1 first."
}

Set-Location $root

& $pythonPath .\scripts\replay_sample_set.py --clear-cache --format md --output evidence\reports\sample_replay_real.md --summary-output evidence\reports\sample_replay_real_summary.md --timestamped
& $pythonPath .\scripts\export_log_summary.py --format md --output evidence\reports\latest_log_summary.md

Write-Host "Real replay finished."
Write-Host "Check evidence/reports/ for the latest replay and summary reports."

