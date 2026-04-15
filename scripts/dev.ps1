$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$pythonPath = Join-Path $root ".venv\\Scripts\\python.exe"
$packagePath = Join-Path $root ".python_packages"
$tempPath = Join-Path $root "tmp"

New-Item -ItemType Directory -Force -Path $tempPath | Out-Null

$venvReady = $false
if (Test-Path $pythonPath) {
    & $pythonPath -c "import fastapi, uvicorn" 2>$null
    if ($LASTEXITCODE -eq 0) {
        $venvReady = $true
    }
}

if ($venvReady) {
    $backendPython = $pythonPath
    $pythonLibPath = $root
}
elseif (Test-Path $packagePath) {
    $backendPython = "python"
    $pythonLibPath = "$root;$packagePath"
}
else {
    throw "Backend dependencies were not found. Run scripts/bootstrap.ps1 first."
}

$backendJob = Start-Job -Name "yandatong-backend" -ScriptBlock {
    param($projectRoot, $pythonExe, $pythonPathEnv, $tmpPath)
    Set-Location $projectRoot
    $env:PYTHONPATH = $pythonPathEnv
    $env:TEMP = $tmpPath
    $env:TMP = $tmpPath
    & $pythonExe -m uvicorn backend.app.main:app --reload --host 0.0.0.0 --port 8000
} -ArgumentList $root, $backendPython, $pythonLibPath, $tempPath

Write-Host "Backend started in background job: $($backendJob.Id)"
Write-Host "Frontend dev server is starting..."

Push-Location (Join-Path $root "frontend")
try {
    npm run dev
}
finally {
    Stop-Job $backendJob -ErrorAction SilentlyContinue | Out-Null
    Remove-Job $backendJob -Force -ErrorAction SilentlyContinue
    Pop-Location
}
