$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
$venvPath = Join-Path $root ".venv"
$pythonPath = Join-Path $venvPath "Scripts\\python.exe"
$packagePath = Join-Path $root ".python_packages"
$tempPath = Join-Path $root "tmp"
$requirementsPath = Join-Path $root "backend\\requirements.txt"

New-Item -ItemType Directory -Force -Path $tempPath | Out-Null
$env:TEMP = $tempPath
$env:TMP = $tempPath

function Invoke-CheckedCommand {
    param(
        [Parameter(Mandatory = $true)]
        [string]$FilePath,
        [Parameter(Mandatory = $false)]
        [string[]]$Arguments
    )

    & $FilePath @Arguments
    if ($LASTEXITCODE -ne 0) {
        throw "Command failed: $FilePath $($Arguments -join ' ')"
    }
}

try {
    if (-not (Test-Path $pythonPath)) {
        Invoke-CheckedCommand -FilePath "python" -Arguments @("-m", "venv", "$venvPath")
    }

    $pipPath = Join-Path $venvPath "Scripts\\pip.exe"
    if (-not (Test-Path $pipPath)) {
        Invoke-CheckedCommand -FilePath "$pythonPath" -Arguments @("-m", "ensurepip", "--upgrade", "--default-pip")
    }

    Invoke-CheckedCommand -FilePath "$pythonPath" -Arguments @("-m", "pip", "install", "--upgrade", "pip")
    Invoke-CheckedCommand -FilePath "$pythonPath" -Arguments @("-m", "pip", "install", "-r", "$requirementsPath")
}
catch {
    Write-Warning "Virtual environment setup failed. Falling back to .python_packages."
    New-Item -ItemType Directory -Force -Path $packagePath | Out-Null
    Invoke-CheckedCommand -FilePath "python" -Arguments @("-m", "pip", "install", "-r", "$requirementsPath", "--target", "$packagePath", "--upgrade")
}

Push-Location (Join-Path $root "frontend")
try {
    npm install
}
finally {
    Pop-Location
}

Write-Host "Bootstrap completed."
