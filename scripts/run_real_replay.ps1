$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$pythonPath = Join-Path $root ".venv\\Scripts\\python.exe"

if (-not (Test-Path $pythonPath)) {
    throw "Python virtual environment not found. Run scripts/bootstrap.ps1 first."
}

Set-Location $root

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$reportTimestamped = "evidence\\reports\\sample_replay_real_$timestamp.md"
$summaryTimestamped = "evidence\\reports\\sample_replay_real_summary_$timestamp.md"
$reportLatest = "evidence\\reports\\sample_replay_real_latest.md"
$summaryLatest = "evidence\\reports\\sample_replay_real_summary_latest.md"

& $pythonPath .\scripts\replay_sample_set.py --clear-cache --format md --output $reportTimestamped --summary-output $summaryTimestamped
Copy-Item -LiteralPath $reportTimestamped -Destination $reportLatest -Force
Copy-Item -LiteralPath $summaryTimestamped -Destination $summaryLatest -Force
& $pythonPath .\scripts\export_log_summary.py --format md --output evidence\reports\latest_log_summary.md

Write-Host "Real replay finished."
Write-Host "Authoritative latest replay report: $reportLatest"
Write-Host "Authoritative latest replay summary: $summaryLatest"
Write-Host "Timestamped replay report: $reportTimestamped"
Write-Host "Timestamped replay summary: $summaryTimestamped"
