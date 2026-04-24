param(
    [string]$OutputRoot = "."
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
    "PROJECT_CONTEXT.md",
    "REVIEW_BUNDLE_INDEX.md",
    "REVIEW_PROMPT.md",
    "README.md",
    ".env.example",
    "render.yaml",
    "pytest.ini",
    "WORKLOG.md",
    "agent_handoff\COMPETITION_PLAN_V2.md",
    "agent_handoff\CURRENT_STATUS_20260418.md",
    "agent_handoff\FREEZE_FACT_SHEET_20260419.md",
    "agent_handoff\PROJECT_HANDOFF.md",
    "agent_handoff\README.md",
    "agent_handoff\SESSION_LOG.md",
    "agent_handoff\TASK_BOARD.md",
    "agent_handoff\TECHNICAL_OPTIMIZATION_ROADMAP_20260424.md",
    "docs\DEPLOY_RENDER.md",
    "evidence\materials\PROJECT_ONE_PAGER.md",
    "evidence\materials\COMPETITION_ASSET_PACK.md",
    "evidence\materials\SUBMISSION_PREP_GUIDE.md",
    "evidence\materials\SUBMISSION_SPEC_CROSSWALK.md",
    "evidence\materials\HANDOFF_PACKAGE_BOUNDARY.md",
    "evidence\materials\PRODUCT_TECHNICAL_WRITEUP.md",
    "evidence\materials\PLATFORM_USAGE_EVIDENCE.md",
    "evidence\materials\HARD_EVIDENCE_SUMMARY.md",
    "evidence\materials\SCORING_EVIDENCE_MATRIX.md",
    "evidence\materials\PPT_DECK_3PAGES_FINAL.md",
    "evidence\materials\VIDEO_SHOTLIST_5MIN_FINAL.md",
    "evidence\materials\PPT_DECK_6SLIDES.md",
    "evidence\materials\VIDEO_SHOTLIST_2MIN.md",
    "evidence\materials\POSTER_COPY.md",
    "evidence\materials\DEMO_SCRIPT_3MIN.md",
    "evidence\materials\GOLD_SAMPLE_RUNBOOK.md",
    "evidence\materials\FINAL_SUBMISSION_CHECKLIST.md",
    "evidence\materials\DEFENSE_DEMO_RISK_CHECKLIST.md",
    "evidence\materials\GOLD_SAMPLE_CANDIDATE_20260418.json",
    "evidence\materials\ARCHITECTURE.md",
    "evidence\materials\QA_BRIEF.md",
    "evidence\materials\MATERIALS_INDEX.md",
    "evidence\materials\REAL_EVIDENCE_REFRESH_CHECKLIST.md",
    "evidence\materials\REAL_REPLAY_GUIDE.md",
    "evidence\materials\SAMPLE_MANIFEST.json",
    "evidence\materials\SAMPLE_SET.md",
    "evidence\materials\STRICT_G3_EXECUTION_PLAN.md",
    "evidence\materials\EXTENDED_EVAL_V1.json",
    "evidence\materials\EXTENDED_EVAL_V1_REFUSAL_ONLY.json",
    "evidence\materials\EXTENDED_EVAL_SCOPE.md",
    "evidence\experiments\20260418_gold_sample_validation.md",
    "evidence\experiments\20260419_q2_declared_stability_check.md",
    "evidence\experiments\20260419_g3_rehearsal_template.md",
    "evidence\experiments\20260420_g3_strict_rehearsal.md",
    "evidence\experiments\20260423_g3_continuation.md",
    "evidence\reports\gold_sample_replay_real_summary_latest.md",
    "evidence\reports\gold_sample_replay_real_latest.md",
    "evidence\reports\gold_sample_qa_compare_latest.md",
    "evidence\reports\quantitative_eval_metrics.md",
    "evidence\reports\extended_eval_v1_latest.md",
    "evidence\reports\extended_eval_v1_latest.json",
    "evidence\reports\extended_eval_v1_qwen3_235b_a22b_instruct_2507_retrieval_patch.md",
    "evidence\reports\extended_eval_v1_qwen3_235b_a22b_instruct_2507_retrieval_patch.json",
    "evidence\reports\model_selection_evaluation_20260424.md",
    "evidence\reports\gold_regression_b6547cc_latest.md",
    "evidence\reports\gold_regression_b6547cc_summary_latest.md",
    "evidence\screenshots\${latestScreenshotPrefix}_gold_ask_research_focus.png",
    "evidence\screenshots\${latestScreenshotPrefix}_gold_ask_research_focus.json",
    "evidence\screenshots\${latestScreenshotPrefix}_gold_pdf_render.png",
    "evidence\screenshots\${latestScreenshotPrefix}_gold_pdf_render.json",
    "evidence\screenshots\${latestScreenshotPrefix}_gold_ask_rank_accuracy.png",
    "evidence\screenshots\${latestScreenshotPrefix}_gold_ask_rank_accuracy.json",
    "evidence\screenshots\${latestScreenshotPrefix}_gold_refusal.png",
    "evidence\screenshots\${latestScreenshotPrefix}_gold_refusal.json",
    "evidence\samples\chinese_llm_spatial_eval.pdf",
    "evidence\samples\attention_is_all_you_need.pdf",
    "evidence\samples\paper_report.md",
    "evidence\samples\research_brief.md",
    "evidence\samples\README.md",
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
    "backend\requirements.txt",
    "backend\app\main.py",
    "backend\app\api\routes.py",
    "backend\app\core\config.py",
    "backend\app\core\csrf.py",
    "backend\app\core\exceptions.py",
    "backend\app\core\logging_config.py",
    "backend\app\schemas\auth.py",
    "backend\app\schemas\common.py",
    "backend\app\schemas\document.py",
    "backend\app\schemas\log.py",
    "backend\app\schemas\task.py",
    "backend\app\services\auth_service.py",
    "backend\app\services\bbox_matcher.py",
    "backend\app\services\cache_service.py",
    "backend\app\services\chunk_service.py",
    "backend\app\services\context_planner.py",
    "backend\app\services\document_parser.py",
    "backend\app\services\file_service.py",
    "backend\app\services\log_service.py",
    "backend\app\services\model_client.py",
    "backend\app\services\retrieval_service.py",
    "backend\app\services\task_service.py",
    "backend\tests\test_api.py",
    "backend\tests\test_config.py",
    "backend\tests\test_extended_eval.py",
    "backend\tests\test_services.py",
    "frontend\index.html",
    "frontend\package.json",
    "frontend\vite.config.ts",
    "frontend\src\App.tsx",
    "frontend\src\api.ts",
    "frontend\src\api.test.ts",
    "frontend\src\main.tsx",
    "frontend\src\styles.css",
    "frontend\src\types.ts",
    "frontend\src\components\MarkdownResult.tsx",
    "frontend\src\components\PdfPreviewPanel.tsx",
    "frontend\src\components\ResultPanel.tsx",
    "frontend\src\App.smoke.test.tsx",
    "frontend\src\test\setup.ts",
    "scripts\capture_gold_sample_screenshots.js",
    "scripts\compare_qa_models.py",
    "scripts\run_real_replay.ps1",
    "scripts\export_competition_asset_pack.ps1",
    "scripts\export_competition_pdfs.js",
    "scripts\export_review_bundle.ps1",
    "scripts\compute_eval_metrics.py",
    "scripts\extended_eval.py",
    "scripts\predeploy_sanity.py",
    "scripts\gold_retrieval_regression.py"
)

$optionalFiles = @(
    "evidence\screenshots\${latestScreenshotPrefix}_stats_panel.png",
    "evidence\screenshots\${latestScreenshotPrefix}_api_docs.png"
)

$outputRootPath = Resolve-OutputRootPath $OutputRoot
New-Item -ItemType Directory -Path $outputRootPath -Force | Out-Null

$timestamp = Get-Date -Format "yyyyMMdd_HHmmss"
$packageDir = Join-Path $outputRootPath "review_bundle_stage_$timestamp"
$zipPath = Join-Path $outputRootPath "review_bundle_${timestamp}_final_competition_review.zip"
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

$bundleManifestPath = Join-Path $packageDir "BUNDLE_MANIFEST.md"
$generatedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss"

$bundleContextSection = (
    ($copiedRequired |
        Where-Object { $_ -eq 'PROJECT_CONTEXT.md' -or $_ -eq 'REVIEW_BUNDLE_INDEX.md' -or $_ -eq 'REVIEW_PROMPT.md' -or $_ -eq 'README.md' -or $_ -eq 'WORKLOG.md' } |
        ForEach-Object { "- $_" }) -join [Environment]::NewLine
)
$bundleBaselineSection = (
    ($copiedRequired |
        Where-Object { $_ -like 'agent_handoff*' } |
        ForEach-Object { "- $_" }) -join [Environment]::NewLine
)
$bundleMaterialsSection = (
    ($copiedRequired |
        Where-Object { $_ -like 'evidence\materials*' } |
        ForEach-Object { "- $_" }) -join [Environment]::NewLine
)
$bundleEvidenceSection = (
    ($copiedRequired |
        Where-Object {
            $_ -like 'evidence\experiments*' -or
            $_ -like 'evidence\reports*' -or
            $_ -like 'evidence\screenshots*' -or
            $_ -like 'evidence\samples*'
        } |
        ForEach-Object { "- $_" }) -join [Environment]::NewLine
)
$bundleDeliverablesSection = (
    ($copiedRequired |
        Where-Object { $_ -like 'deliverables\competition_kit*' } |
        ForEach-Object { "- $_" }) -join [Environment]::NewLine
)
$bundleCodeSection = (
    ($copiedRequired |
        Where-Object {
            $_ -like 'backend*' -or
            $_ -like 'frontend*' -or
            $_ -like 'scripts*' -or
            $_ -like 'docs*' -or
            $_ -eq '.env.example' -or
            $_ -eq 'render.yaml' -or
            $_ -eq 'pytest.ini'
        } |
        ForEach-Object { "- $_" }) -join [Environment]::NewLine
)
$bundleOptionalSection = if ($copiedOptional.Count -eq 0) {
    "- none"
}
else {
    ($copiedOptional | ForEach-Object { "- $_" }) -join [Environment]::NewLine
}

$bundleManifest = @"
# Review Bundle Manifest

## Read First

- PROJECT_CONTEXT.md
- REVIEW_PROMPT.md
- REVIEW_BUNDLE_INDEX.md
- agent_handoff/FREEZE_FACT_SHEET_20260419.md

## Purpose

This generated bundle packages the current end-to-end review surface for
YanDatong.

The review target is the whole project in its current late-stage competition
state:

- product positioning
- engineering / architecture credibility
- demo path credibility
- evidence chain
- submission material readiness
- remaining last-mile risks

## Current Snapshot (2026-04-24)

- Runtime provider: `Wuwen Xinqiong`
- Primary QA model: `qwen3-235b-a22b-instruct-2507`
- Validated fast fallback: `qwen3-next-80b-a3b-instruct`
- Locked gold-sample document: `evidence/samples/chinese_llm_spatial_eval.pdf`
- Extended eval corpus (4 documents):
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
  - `evidence/samples/attention_is_all_you_need.pdf`
  - `evidence/samples/paper_report.md`
  - `evidence/samples/research_brief.md`
- Strongest judged path: `prepare demo -> digest -> follow-up ask -> citation -> PDF -> refusal`
- Strict `G3` status: fresh-upload `6`-run pass recorded across
  `evidence/experiments/20260420_g3_strict_rehearsal.md` and the 2026-04-23
  continuation notes in handoff/materials
- Quantitative evaluation (updated 2026-04-24):
  - strict G3 (`9` entries): 4 rates at `100%`, avg latency `5521 ms`
    - report: `evidence/reports/quantitative_eval_metrics.md`
  - extended v1 (`51` cases): final default-model replay closed at `51 / 51`
    after targeted retrieval/context patching
    - report: `evidence/reports/extended_eval_v1_qwen3_235b_a22b_instruct_2507_retrieval_patch.md`
  - model selection: `qwen3-235b-a22b-instruct-2507` remains best default QA;
    `kimi-k2.6` was competitive but too slow; `qwen3-next-80b-a3b-instruct`
    is the best fast fallback
    - report: `evidence/reports/model_selection_evaluation_20260424.md`
- Late-stage hardening (2026-04-24):
  - LLM-layer `refused` escape in ask prompt + `llm_refused` branch
  - metadata-intent retrieval fallback (first-chunk pin)
  - `scripts/predeploy_sanity.py` wired as pre-demo must-pass
  - frontend UX polish: confidence bar / clickable citations / refusal card /
    drag-drop upload / research digest workbench / follow-up chips / national
    demo route / concise digest fallback / task timeout fallback
- Repo-native final asset baselines now exist:
  - `deliverables/competition_kit/deck_3page_final.pdf`
  - `deliverables/competition_kit/video_subtitles_5min_final.srt`
- Remaining default open work:
  - final native `PPT` (teammate task)
  - final edited `5`-minute video (teammate task)
  - full rehearsal on target judging environment
  - screenshot refresh only if target environment changes

## Included Files

### 1. Context / Review Instructions

$bundleContextSection

### 2. Baseline / Handoff

$bundleBaselineSection

### 3. Competition Story / Materials

$bundleMaterialsSection

### 4. Evidence / Validation

$bundleEvidenceSection

### 5. Current Deliverables

$bundleDeliverablesSection

### 6. Core Code / Scripts

$bundleCodeSection

## Optional Appendix Files Included

$bundleOptionalSection

## Bundle Generation Metadata

- Generated at: $generatedAt
- Source repo path: $root
- Latest screenshot prefix: $latestScreenshotPrefix
- Stage directory: $packageDir
- Zip path: $zipPath
"@

Set-Content -LiteralPath $bundleManifestPath -Value $bundleManifest -Encoding UTF8

if (Test-Path -LiteralPath $zipPath) {
    Remove-Item -LiteralPath $zipPath -Force
}

Compress-Archive -LiteralPath $packageDir -DestinationPath $zipPath -Force

Write-Host "Review bundle created."
Write-Host "Stage directory: $packageDir"
Write-Host "Zip file: $zipPath"
Write-Host "Bundle manifest: $bundleManifestPath"
