$ErrorActionPreference = "Stop"

# Start backend + frontend + cloudflared quick tunnel, then print the public
# URL that can be shared with someone for demo/trial. All three processes run
# as background jobs; Ctrl+C in this window stops all of them cleanly.
#
# Prerequisites:
#   - scripts\bootstrap.ps1 has been run (backend venv ready)
#   - frontend\node_modules installed (npm install)
#   - cloudflared on PATH (winget install Cloudflare.cloudflared)
#   - backend .env has DEMO_MODE=true if you want the invite-code gate hidden
#   - backend .env CORS_ORIGINS includes `https://*.trycloudflare.com` so the
#     CSRF middleware accepts the tunnel subdomain (the default .env.example
#     already has this)

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$pythonPath = Join-Path $root ".venv\Scripts\python.exe"
$tempPath = Join-Path $root "tmp"
$cloudflaredLog = Join-Path $tempPath "cloudflared_share.log"

New-Item -ItemType Directory -Force -Path $tempPath | Out-Null
if (Test-Path $cloudflaredLog) { Remove-Item $cloudflaredLog -Force }

if (-not (Test-Path $pythonPath)) {
    throw "Backend venv not found at $pythonPath. Run scripts\bootstrap.ps1 first."
}

$cloudflared = Get-Command cloudflared -ErrorAction SilentlyContinue
if (-not $cloudflared) {
    throw "cloudflared not on PATH. Install with: winget install Cloudflare.cloudflared"
}

Write-Host ""
Write-Host "=== yandatong share ===" -ForegroundColor Cyan
Write-Host "Starting backend (uvicorn :8000)..." -ForegroundColor DarkGray

$backendJob = Start-Job -Name "yandatong-share-backend" -ScriptBlock {
    param($projectRoot, $pythonExe, $tmpPath)
    Set-Location $projectRoot
    $env:PYTHONPATH = $projectRoot
    $env:TEMP = $tmpPath
    $env:TMP = $tmpPath
    & $pythonExe -m uvicorn backend.app.main:app --host 0.0.0.0 --port 8000
} -ArgumentList $root, $pythonPath, $tempPath

Start-Sleep -Seconds 2

Write-Host "Starting frontend (vite :5173)..." -ForegroundColor DarkGray
$frontendJob = Start-Job -Name "yandatong-share-frontend" -ScriptBlock {
    param($projectRoot)
    Set-Location (Join-Path $projectRoot "frontend")
    npm run dev
} -ArgumentList $root

Start-Sleep -Seconds 3

Write-Host "Starting cloudflared quick tunnel -> http://localhost:5173 ..." -ForegroundColor DarkGray
$tunnelJob = Start-Job -Name "yandatong-share-tunnel" -ScriptBlock {
    param($logPath)
    & cloudflared tunnel --no-autoupdate --url http://localhost:5173 2>&1 | Tee-Object -FilePath $logPath
} -ArgumentList $cloudflaredLog

Write-Host "Waiting for tunnel URL..." -ForegroundColor DarkGray

$publicUrl = $null
$deadline = (Get-Date).AddSeconds(45)
while ((Get-Date) -lt $deadline -and -not $publicUrl) {
    Start-Sleep -Milliseconds 800
    if (Test-Path $cloudflaredLog) {
        $logText = Get-Content $cloudflaredLog -Raw -ErrorAction SilentlyContinue
        if ($logText) {
            $match = [regex]::Match($logText, "https://[a-z0-9-]+\.trycloudflare\.com")
            if ($match.Success) {
                $publicUrl = $match.Value
            }
        }
    }
}

Write-Host ""
if ($publicUrl) {
    Write-Host "==============================================" -ForegroundColor Green
    Write-Host "  PUBLIC URL:  $publicUrl" -ForegroundColor Green
    Write-Host "==============================================" -ForegroundColor Green
    Write-Host ""
    Write-Host "Share that URL. Press Ctrl+C here to stop everything." -ForegroundColor DarkGray
}
else {
    Write-Host "Failed to detect a cloudflared URL within 45s." -ForegroundColor Yellow
    Write-Host "Check log: $cloudflaredLog" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press Ctrl+C to stop backend + frontend + tunnel." -ForegroundColor DarkGray

try {
    while ($true) {
        Start-Sleep -Seconds 2
        foreach ($job in @($backendJob, $frontendJob, $tunnelJob)) {
            if ($job.State -eq "Failed" -or $job.State -eq "Completed") {
                Write-Host "Job '$($job.Name)' exited with state $($job.State). Stopping." -ForegroundColor Red
                throw "share process exited"
            }
        }
    }
}
finally {
    Write-Host ""
    Write-Host "Stopping share processes..." -ForegroundColor DarkGray
    foreach ($job in @($tunnelJob, $frontendJob, $backendJob)) {
        if ($job) {
            Stop-Job $job -ErrorAction SilentlyContinue | Out-Null
            Remove-Job $job -Force -ErrorAction SilentlyContinue
        }
    }
    Write-Host "Done." -ForegroundColor DarkGray
}
