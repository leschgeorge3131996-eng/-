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

function Get-LatestScreenshotPrefix {
    $screenshotDir = Join-Path $root "evidence\screenshots"
    $latestFocusShot = Get-ChildItem -LiteralPath $screenshotDir -Filter "*_gold_ask_research_focus.png" -File |
        Sort-Object Name -Descending |
        Select-Object -First 1

    if (-not $latestFocusShot) {
        throw "No gold-sample screenshots found under evidence\\screenshots"
    }

    if ($latestFocusShot.BaseName -match '^(?<prefix>\d{8})_gold_ask_research_focus$') {
        return $Matches.prefix
    }

    throw "Could not parse screenshot date prefix from $($latestFocusShot.Name)"
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

$latestScreenshotPrefix = Get-LatestScreenshotPrefix

$requiredFiles = @(
    "agent_handoff\FREEZE_FACT_SHEET_20260419.md",
    "evidence\materials\PROJECT_ONE_PAGER.md",
    "evidence\materials\DEMO_SCRIPT_3MIN.md",
    "evidence\materials\PRODUCT_TECHNICAL_WRITEUP.md",
    "evidence\materials\PLATFORM_USAGE_EVIDENCE.md",
    "evidence\materials\HARD_EVIDENCE_SUMMARY.md",
    "evidence\materials\SCORING_EVIDENCE_MATRIX.md",
    "evidence\materials\HANDOFF_PACKAGE_BOUNDARY.md",
    "evidence\materials\GOLD_SAMPLE_RUNBOOK.md",
    "evidence\materials\COMPETITION_ASSET_PACK.md",
    "evidence\materials\PPT_DECK_3PAGES_FINAL.md",
    "evidence\materials\VIDEO_SHOTLIST_5MIN_FINAL.md",
    "evidence\materials\PPT_DECK_6SLIDES.md",
    "evidence\materials\VIDEO_SHOTLIST_2MIN.md",
    "evidence\materials\POSTER_COPY.md",
    "evidence\materials\QA_BRIEF.md",
    "evidence\materials\SUBMISSION_PREP_GUIDE.md",
    "evidence\materials\FINAL_SUBMISSION_CHECKLIST.md",
    "evidence\materials\DEFENSE_DEMO_RISK_CHECKLIST.md",
    "evidence\materials\SUBMISSION_SPEC_CROSSWALK.md",
    "evidence\materials\MATERIALS_INDEX.md",
    "evidence\materials\GOLD_SAMPLE_CANDIDATE_20260418.json",
    "evidence\reports\gold_sample_replay_real_summary_latest.md",
    "evidence\reports\gold_sample_replay_real_latest.md",
    "evidence\reports\gold_sample_qa_compare_latest.md",
    "evidence\screenshots\${latestScreenshotPrefix}_gold_ask_research_focus.png",
    "evidence\screenshots\${latestScreenshotPrefix}_gold_ask_research_focus.json",
    "evidence\screenshots\${latestScreenshotPrefix}_gold_pdf_render.png",
    "evidence\screenshots\${latestScreenshotPrefix}_gold_pdf_render.json",
    "evidence\screenshots\${latestScreenshotPrefix}_gold_ask_rank_accuracy.png",
    "evidence\screenshots\${latestScreenshotPrefix}_gold_ask_rank_accuracy.json",
    "evidence\screenshots\${latestScreenshotPrefix}_gold_refusal.png",
    "evidence\screenshots\${latestScreenshotPrefix}_gold_refusal.json",
    "evidence\samples\chinese_llm_spatial_eval.pdf",
    "deliverables\competition_kit\README.md",
    "deliverables\competition_kit\deck_3page_final.html",
    "deliverables\competition_kit\deck.html",
    "deliverables\competition_kit\poster.html",
    "deliverables\competition_kit\styles.css",
    "deliverables\competition_kit\deck_3page_final.pdf",
    "deliverables\competition_kit\deck.pdf",
    "deliverables\competition_kit\poster.pdf",
    "deliverables\competition_kit\video_subtitles_5min_final.srt",
    "deliverables\competition_kit\video_subtitles.srt",
    "scripts\export_competition_asset_pack.ps1",
    "scripts\export_competition_pdfs.js"
)

$optionalFiles = @(
    "evidence\screenshots\${latestScreenshotPrefix}_stats_panel.png",
    "evidence\screenshots\${latestScreenshotPrefix}_api_docs.png"
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
$indexLines.Add("- Package boundary guide: evidence/materials/HANDOFF_PACKAGE_BOUNDARY.md")
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
$indexLines.Add("## Package Boundary")
$indexLines.Add("- Main submission: final 3-page PPT, final 5-minute video, PRODUCT_TECHNICAL_WRITEUP.md, PLATFORM_USAGE_EVIDENCE.md, HARD_EVIDENCE_SUMMARY.md, SCORING_EVIDENCE_MATRIX.md, final screenshots")
$indexLines.Add("- Appendix: replay reports, experiment notes, GOLD_SAMPLE_RUNBOOK.md, QA_BRIEF.md, appendix-only screenshots")
$indexLines.Add("- Ops/source: PROJECT_ONE_PAGER.md, DEMO_SCRIPT_3MIN.md, COMPETITION_ASSET_PACK.md, FINAL_SUBMISSION_CHECKLIST.md, DEFENSE_DEMO_RISK_CHECKLIST.md, PPT_DECK_3PAGES_FINAL.md, VIDEO_SHOTLIST_5MIN_FINAL.md, PPT_DECK_6SLIDES.md, VIDEO_SHOTLIST_2MIN.md, POSTER_COPY.md, deliverables/competition_kit/, export scripts")
$indexLines.Add("")
$indexLines.Add("## Recommended Build Order")
$indexLines.Add("1. Read evidence/materials/HANDOFF_PACKAGE_BOUNDARY.md, evidence/materials/SUBMISSION_SPEC_CROSSWALK.md, and evidence/materials/FINAL_SUBMISSION_CHECKLIST.md")
$indexLines.Add("2. Lock judge-facing wording from PRODUCT_TECHNICAL_WRITEUP.md, PLATFORM_USAGE_EVIDENCE.md, HARD_EVIDENCE_SUMMARY.md, and SCORING_EVIDENCE_MATRIX.md")
$indexLines.Add("3. Use evidence/materials/PPT_DECK_3PAGES_FINAL.md plus deliverables/competition_kit/deck_3page_final.html and deck_3page_final.pdf as the repo-native judged-deck baseline; keep PPT_DECK_6SLIDES.md only as the compression baseline")
$indexLines.Add("4. Use deliverables/competition_kit/deck.pdf and poster.pdf only as supporting printable baselines, not as official substitutes for the judged deck")
$indexLines.Add("5. Record or edit the final video from evidence/materials/VIDEO_SHOTLIST_5MIN_FINAL.md with deliverables/competition_kit/video_subtitles_5min_final.srt as the timing baseline; keep VIDEO_SHOTLIST_2MIN.md only as the pacing baseline")
$indexLines.Add("6. Before a live slot, run evidence/materials/DEFENSE_DEMO_RISK_CHECKLIST.md together with GOLD_SAMPLE_RUNBOOK.md on the target machine")
$indexLines.Add("7. Keep wording aligned with PROJECT_ONE_PAGER.md, DEMO_SCRIPT_3MIN.md, and QA_BRIEF.md")

Set-Content -LiteralPath $indexPath -Value $indexLines -Encoding UTF8

Write-Host "Competition export pack created."
Write-Host "Package directory: $packageDir"
Write-Host "Index: $indexPath"
