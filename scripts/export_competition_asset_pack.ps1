param(
    [string]$OutputRoot = "evidence\exports"
)

$ErrorActionPreference = "Stop"

$root = Resolve-Path (Join-Path $PSScriptRoot "..")
Set-Location $root

function Resolve-OutputRootPath([string]$PathValue) {
    if ([System.IO.Path]::IsPathRooted($PathValue)) {
        return $PathValue
    }
    return Join-Path $root $PathValue
}

function Copy-RelativeFile(
    [string]$RelativePath,
    [string]$PackageDir,
    [bool]$Required
) {
    $sourcePath = Join-Path $root $RelativePath
    if (-not (Test-Path -LiteralPath $sourcePath)) {
        if ($Required) {
            throw "Required file is missing: $RelativePath"
        }
        return $false
    }

    $destinationPath = Join-Path $PackageDir $RelativePath
    $destinationDir = Split-Path -Parent $destinationPath
    if ($destinationDir) {
        New-Item -ItemType Directory -Path $destinationDir -Force | Out-Null
    }

    Copy-Item -LiteralPath $sourcePath -Destination $destinationPath -Force
    return $true
}

$requiredFiles = @(
    "evidence\materials\PROJECT_ONE_PAGER.md",
    "evidence\materials\DEMO_SCRIPT_3MIN.md",
    "evidence\materials\GOLD_SAMPLE_RUNBOOK.md",
    "evidence\materials\COMPETITION_ASSET_PACK.md",
    "evidence\materials\PPT_DECK_6SLIDES.md",
    "evidence\materials\VIDEO_SHOTLIST_2MIN.md",
    "evidence\materials\POSTER_COPY.md",
    "evidence\materials\QA_BRIEF.md",
    "evidence\materials\SUBMISSION_PREP_GUIDE.md",
    "evidence\materials\MATERIALS_INDEX.md",
    "evidence\materials\GOLD_SAMPLE_CANDIDATE_20260418.json",
    "evidence\reports\gold_sample_replay_real_summary_latest.md",
    "evidence\reports\gold_sample_replay_real_latest.md",
    "evidence\reports\gold_sample_qa_compare_latest.md",
    "evidence\screenshots\20260418_gold_ask_research_focus.png",
    "evidence\screenshots\20260418_gold_pdf_render.png",
    "evidence\screenshots\20260418_gold_ask_rank_accuracy.png",
    "evidence\screenshots\20260418_gold_refusal.png",
    "evidence\samples\chinese_llm_spatial_eval.pdf",
    "deliverables\competition_kit\README.md",
    "deliverables\competition_kit\deck.html",
    "deliverables\competition_kit\poster.html",
    "deliverables\competition_kit\styles.css",
    "deliverables\competition_kit\deck.pdf",
    "deliverables\competition_kit\poster.pdf",
    "scripts\export_competition_asset_pack.ps1",
    "scripts\export_competition_pdfs.js"
)

$optionalFiles = @(
    "evidence\screenshots\20260418_stats_panel.png",
    "evidence\screenshots\20260418_api_docs.png"
)

$outputRootPath = Resolve-OutputRootPath $OutputRoot
New-Item -ItemType Directory -Path $outputRootPath -Force | Out-Null

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$packageDir = Join-Path $outputRootPath "competition_asset_pack_$timestamp"
New-Item -ItemType Directory -Path $packageDir -Force | Out-Null

$copiedRequired = New-Object System.Collections.Generic.List[string]
$copiedOptional = New-Object System.Collections.Generic.List[string]

foreach ($relativePath in $requiredFiles) {
    [void](Copy-RelativeFile -RelativePath $relativePath -PackageDir $packageDir -Required $true)
    $copiedRequired.Add($relativePath)
}

foreach ($relativePath in $optionalFiles) {
    if (Copy-RelativeFile -RelativePath $relativePath -PackageDir $packageDir -Required $false) {
        $copiedOptional.Add($relativePath)
    }
}

$indexPath = Join-Path $packageDir "PACK_CONTENTS.md"
$generatedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$indexLines = New-Object System.Collections.Generic.List[string]

$indexLines.Add("# Competition Export Pack")
$indexLines.Add("")
$indexLines.Add("- Generated at: $generatedAt")
$indexLines.Add("- Source repo path: $root")
$indexLines.Add("- Locked sample: evidence/samples/chinese_llm_spatial_eval.pdf")
$indexLines.Add("- Locked prompts: 2 answerable + 1 refusal from GOLD_SAMPLE_CANDIDATE_20260418.json")
$indexLines.Add("- Current primary QA model: qwen3-235b-a22b-instruct-2507")
$indexLines.Add("- Validated fallback QA model: qwen3-32b")
$indexLines.Add("")
$indexLines.Add("## Required Files")
foreach ($relativePath in $copiedRequired) {
    $indexLines.Add("- $relativePath")
}

$indexLines.Add("")
$indexLines.Add("## Optional Files Included")
if ($copiedOptional.Count -eq 0) {
    $indexLines.Add("- None")
}
else {
    foreach ($relativePath in $copiedOptional) {
        $indexLines.Add("- $relativePath")
    }
}

$indexLines.Add("")
$indexLines.Add("## Recommended Build Order")
$indexLines.Add("1. Read evidence/materials/COMPETITION_ASSET_PACK.md")
$indexLines.Add("2. Draft slides from evidence/materials/PPT_DECK_6SLIDES.md")
$indexLines.Add("3. Use deliverables/competition_kit/deck.pdf and poster.pdf as the current printable baselines")
$indexLines.Add("4. If visual polish is needed, edit deliverables/competition_kit/*.html and rerun scripts/export_competition_pdfs.js")
$indexLines.Add("5. Record or edit video using evidence/materials/VIDEO_SHOTLIST_2MIN.md")
$indexLines.Add("6. Keep wording aligned with PROJECT_ONE_PAGER.md and QA_BRIEF.md")

Set-Content -LiteralPath $indexPath -Value $indexLines -Encoding UTF8

Write-Host "Competition export pack created."
Write-Host "Package directory: $packageDir"
Write-Host "Index: $indexPath"
