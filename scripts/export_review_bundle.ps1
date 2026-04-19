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
    "README.md",
    ".env.example",
    "render.yaml",
    "pytest.ini",
    "WORKLOG.md",
    "agent_handoff\COMPETITION_PLAN_V2.md",
    "agent_handoff\CURRENT_STATUS_20260418.md",
    "agent_handoff\FREEZE_FACT_SHEET_20260419.md",
    "agent_handoff\PROJECT_HANDOFF.md",
    "agent_handoff\SESSION_LOG.md",
    "agent_handoff\TASK_BOARD.md",
    "docs\DEPLOY_RENDER.md",
    "evidence\materials\PROJECT_ONE_PAGER.md",
    "evidence\materials\COMPETITION_ASSET_PACK.md",
    "evidence\materials\SUBMISSION_PREP_GUIDE.md",
    "evidence\materials\PPT_DECK_6SLIDES.md",
    "evidence\materials\VIDEO_SHOTLIST_2MIN.md",
    "evidence\materials\POSTER_COPY.md",
    "evidence\materials\DEMO_SCRIPT_3MIN.md",
    "evidence\materials\GOLD_SAMPLE_RUNBOOK.md",
    "evidence\materials\GOLD_SAMPLE_CANDIDATE_20260418.json",
    "evidence\materials\ARCHITECTURE.md",
    "evidence\materials\QA_BRIEF.md",
    "evidence\materials\MATERIALS_INDEX.md",
    "evidence\materials\REAL_EVIDENCE_REFRESH_CHECKLIST.md",
    "evidence\materials\REAL_REPLAY_GUIDE.md",
    "evidence\materials\SAMPLE_MANIFEST.json",
    "evidence\materials\SAMPLE_SET.md",
    "evidence\experiments\20260418_gold_sample_validation.md",
    "evidence\experiments\20260419_q2_declared_stability_check.md",
    "evidence\experiments\20260419_g3_rehearsal_template.md",
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
    "deliverables\competition_kit\deck.html",
    "deliverables\competition_kit\poster.html",
    "deliverables\competition_kit\styles.css",
    "deliverables\competition_kit\deck.pdf",
    "deliverables\competition_kit\poster.pdf",
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
    "backend\app\services\model_client.py",
    "backend\app\services\context_planner.py",
    "backend\app\services\document_parser.py",
    "backend\app\services\retrieval_service.py",
    "backend\app\services\task_service.py",
    "backend\app\services\file_service.py",
    "backend\app\services\log_service.py",
    "backend\tests\test_api.py",
    "backend\tests\test_config.py",
    "backend\tests\test_services.py",
    "frontend\index.html",
    "frontend\package.json",
    "frontend\vite.config.ts",
    "frontend\src\App.tsx",
    "frontend\src\api.ts",
    "frontend\src\main.tsx",
    "frontend\src\styles.css",
    "frontend\src\types.ts",
    "frontend\src\components\MarkdownResult.tsx",
    "frontend\src\components\ResultPanel.tsx",
    "frontend\src\components\PdfPreviewPanel.tsx",
    "frontend\src\App.smoke.test.tsx",
    "frontend\src\test\setup.ts",
    "scripts\capture_gold_sample_screenshots.js",
    "scripts\compare_qa_models.py",
    "scripts\run_real_replay.ps1",
    "scripts\export_competition_asset_pack.ps1",
    "scripts\export_competition_pdfs.js",
    "scripts\export_review_bundle.ps1"
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

$bundleIndexPath = Join-Path $packageDir "BUNDLE_INDEX.md"
$projectContextPath = Join-Path $packageDir "PROJECT_CONTEXT.md"
$reviewPromptPath = Join-Path $packageDir "REVIEW_PROMPT.md"
$generatedAt = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
$bundleBaselineSection = (
    ($copiedRequired |
        Where-Object { $_ -like 'agent_handoff*' -or $_ -eq 'README.md' -or $_ -eq 'WORKLOG.md' } |
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

$projectContext = @"
# Project Context

## One-Paragraph Summary

YanDatong is a competition-focused document QA project for paper/report reading
and defense preparation. The core differentiator is not "generic chat over
PDFs", but an evidence-backed ask flow that can answer from retrieved document
evidence, expose the supporting citation blocks, jump back into the PDF, and
refuse unsupported off-topic questions.

## Why This Project Exists

The team is preparing a late-stage competition submission and judging demo.
They do **not** need a broad SaaS product review. They need a hard review of
whether the current project story, evidence, and materials are strong enough to
survive judging.

The current strategy is intentionally narrow:

- center the demo on ask -> citation -> PDF back-link -> refusal
- emphasize evidence credibility over feature breadth
- keep summary / outline as supporting capabilities rather than the main story
- avoid expanding scope this late in the cycle

## Current Background

- Runtime provider has been switched to Wuwen Xinqiong and validated in the
  real in-project path.
- The team locked a Chinese paper as the current gold-sample demo document:
  - evidence/samples/chinese_llm_spatial_eval.pdf
- The locked judging path currently uses:
  - 2 answerable asks
  - 1 refusal ask
- The current primary QA model is:
  - qwen3-235b-a22b-instruct-2507
- A validated fallback also exists:
  - qwen3-32b

## What Has Already Been Done

- Real provider path is live in-project.
- Gold-sample replay reports, screenshots, and PDF evidence exist.
- Q2 fresh declared-evidence instability was fixed and rechecked.
- G3 operator rehearsal is recorded as pass in the current handoff.
- The competition material chain was rebuilt from clean source docs after an
  external review identified corruption in the earlier printable baseline.
- The current printable baseline has already been regenerated and rechecked:
  - deliverables/competition_kit/deck.pdf -> 6 pages
  - deliverables/competition_kit/poster.pdf -> 1 page
- The latest screenshot sidecars now explicitly record:
  - attempt
  - evidence_mode
  - cache_hit

## What "Pass" Currently Means

- G1:
  - real provider path is live and the main ask/citation/PDF/refusal flow works
- G2:
  - the locked gold-sample path now has answerable evidence plus refusal proof
- G3:
  - a warm-state operator rehearsal on the locked sample path passed for 3
    consecutive runs

Important caveat:

- current G3 evidence is **not** a stricter cold-start upload-from-zero pass
- it is a warm-state judged-demo rehearsal after warmup on the locked document

## What File Should Override Older Historical Notes

If the reviewer sees older statements that conflict with the latest state,
prefer:

1. agent_handoff/FREEZE_FACT_SHEET_20260419.md
2. agent_handoff/CURRENT_STATUS_20260418.md
3. the latest screenshot sidecars under evidence/screenshots/
4. the current printable deliverables under deliverables/competition_kit/

Historical notes are still useful, but they should not outweigh the current
freeze-fact layer.

## Real Goal Of This Review

The reviewer should judge whether the current project is genuinely close to
submission freeze, not whether it could become a much broader product someday.

The highest-value questions are:

1. Is the competition story clear, memorable, and honest?
2. Is the evidence-backed ask path convincing enough for judges?
3. Are the current screenshots / replay reports / deck / poster / video script
   internally consistent?
4. Are there still any "this could embarrass the team live" risks?
5. Are the current G1/G2/G3 pass claims actually defensible?

## What Not To Optimize For

Do not optimize this review for:

- broad product pivots
- new task types
- OCR-heavy redesigns
- local-model strategy branches
- generic SaaS reframing
- large visual rewrites

This bundle is for **final-stage competition judgment**, not long-range product
exploration.

## Recommended Reading Order

1. PROJECT_CONTEXT.md
2. REVIEW_PROMPT.md
3. BUNDLE_INDEX.md
4. agent_handoff/FREEZE_FACT_SHEET_20260419.md
5. agent_handoff/CURRENT_STATUS_20260418.md
6. agent_handoff/PROJECT_HANDOFF.md
7. evidence/materials/COMPETITION_ASSET_PACK.md
8. evidence/experiments/20260419_q2_declared_stability_check.md
9. evidence/experiments/20260419_g3_rehearsal_template.md
10. current deck / poster / video-script materials
11. code paths only where needed to verify a claim
"@

$bundleIndex = @"
# Final Review Bundle

## Read This First

- PROJECT_CONTEXT.md
- REVIEW_PROMPT.md
- BUNDLE_INDEX.md

## Purpose

This bundle is for a fresh external AI review of the **current** competition
state of YanDatong.

This is not an early exploratory review. It is a **late-stage final-review
bundle** after the following have already happened:

- the real provider path is live
- the locked gold-sample path is in place
- the fresh Q2 declared-evidence regression has been fixed
- G3 has been recorded as pass in the current handoff
- the competition material chain has been rebuilt from clean sources
- the current printable baseline has been regenerated with sanity checks

The goal is to catch the remaining high-value risks before final submission /
judging material freeze.

## Current Snapshot

- Project: YanDatong
- Positioning: evidence-backed document QA for paper/report reading and defense prep
- Primary demo path: ask -> citation -> PDF back-link -> refusal
- Runtime: Wuwen Xinqiong
- Primary QA model: qwen3-235b-a22b-instruct-2507
- Validated fallback: qwen3-32b
- Claimed gate status in the current bundle:
  - G1: pass
  - G2: pass
  - G3: pass
- Important caveat already documented by the team:
  - current G3 evidence is a warm-state reproducibility pass after warmup on
    the locked sample document, not a stricter cold-start upload-from-zero pass
- Current freeze-fact file:
  - agent_handoff/FREEZE_FACT_SHEET_20260419.md

## What Changed Since The Previous External Review

- Q2 fresh ask evidence instability was investigated and fixed
- backend/app/services/task_service.py now includes an internal one-step ask
  evidence retry when structured evidence is missing
- regression coverage was added in backend/tests/test_services.py
- fresh Q2 re-check was recorded in:
  - evidence/experiments/20260419_q2_declared_stability_check.md
- G3 rehearsal was recorded in:
  - evidence/experiments/20260419_g3_rehearsal_template.md
- the competition material chain was rebuilt and current printable outputs now
  pass the intended page-count sanity check:
  - deck.pdf -> 6 pages
  - poster.pdf -> 1 page
- the latest screenshot sidecars now include cache_hit so the reviewer can
  distinguish fresh results from cached results

## Review Focus

The reviewer should focus on:

1. final competition strategy coherence
2. demo / screenshot / PDF-evidence credibility
3. submission-material consistency across deck / poster / video script
4. hidden implementation risks that could still hurt judging
5. whether the current "pass" claims are truly defensible

Do **not** spend most of the review re-reporting already-fixed old issues unless
the current bundle still proves they remain open.

## Included Sections

### 1. Baseline / Status / Handoff

$bundleBaselineSection

### 2. Competition Story / Materials

$bundleMaterialsSection

### 3. Evidence / Validation

$bundleEvidenceSection

### 4. Current Deliverables

$bundleDeliverablesSection

### 5. Core Code / Scripts

$bundleCodeSection

## Optional Appendix Files Included

$bundleOptionalSection

## Recommended Review Order

1. Read PROJECT_CONTEXT.md
2. Read REVIEW_PROMPT.md
3. Read agent_handoff/FREEZE_FACT_SHEET_20260419.md
4. Read agent_handoff/CURRENT_STATUS_20260418.md
5. Read agent_handoff/PROJECT_HANDOFF.md
6. Read evidence/materials/COMPETITION_ASSET_PACK.md
7. Read evidence/experiments/20260419_q2_declared_stability_check.md
8. Read evidence/experiments/20260419_g3_rehearsal_template.md
9. Inspect the current deck/poster/video deliverables
10. Inspect the current ask/evidence code path only if needed

## Generation Metadata

- Generated at: $generatedAt
- Source repo path: $root
- Bundle directory: $packageDir
- Zip path: $zipPath
"@

$reviewPrompt = @"
# Final External Review Prompt

You are reviewing a **late-stage competition submission bundle** for
YanDatong.

Before writing any judgment, first read:

1. PROJECT_CONTEXT.md
2. REVIEW_PROMPT.md
3. BUNDLE_INDEX.md
4. agent_handoff/FREEZE_FACT_SHEET_20260419.md
5. agent_handoff/CURRENT_STATUS_20260418.md
6. agent_handoff/PROJECT_HANDOFF.md

## Your Role

Act as a strict final reviewer across:

- competition strategy
- demo / evidence credibility
- submission-material readiness
- implementation risks that could still damage judging

Do not waste time on generic praise. Prioritize contradictions, weak claims,
remaining blockers, and "this could still embarrass the team live" risks.

## Important Context

- This is a **second-pass** external review, not an early exploration review.
- Some earlier problems were already identified and then fixed by the team.
- In particular, the team now claims the following are already addressed:
  - fresh Q2 declared-evidence instability
  - refusal semantics (retrieval_gate)
  - screenshot evidence consistency
  - G3 recorded as pass
  - printable material corruption in the earlier deck/poster baseline
- Do **not** spend most of the review repeating stale historical findings unless
  the current files still show those problems are still open.
- If you find historical contradictions, explicitly distinguish:
  - stale historical artifact
  - current blocker

## Project Context

- Product framing:
  - evidence-backed document QA for paper/report reading and defense prep
- Primary demo path:
  - ask -> citation -> PDF back-link -> refusal
- Current target:
  - top 20% of the topic and qualification for national finals
- Scope is intentionally frozen.
- Do not recommend broad pivots into:
  - new task types
  - OCR-heavy direction
  - local-model branch
  - public SaaS reframing
  - large frontend redesign

## What To Review

### 1. Final Strategy / Narrative

- Is the current competition story coherent and memorable?
- Is the "evidence-backed ask" positioning strong enough?
- Is anything still overclaimed, weakly framed, or internally inconsistent?
- Does the current G1/G2/G3 narrative sound honest and defensible?

### 2. Demo / Evidence / Material Readiness

- Are the current screenshots, replay reports, PDF evidence, and deliverables
  convincing enough for judges?
- Are the current deck / poster / video-script materials aligned?
- Is anything obviously still in "draft mode" rather than "submission mode"?
- If the team froze materials today, what would still be risky?

### 3. Technical / Product Risk

- What implementation risks could still break trust or weaken the demo?
- Which current code/design decisions are strongest?
- What remaining weaknesses are most dangerous under judging conditions?
- If you challenge a claimed fix, point to the current file evidence directly.

### 4. Final Competition Readiness

- Give a realistic completion estimate based on the current bundle.
- Decide whether G1, G2, and G3 are actually passed **on current evidence**.
- Pay special attention to whether the current G3 evidence is strong enough,
  given that it is documented as a warm-state operator rehearsal.
- Pay special attention to whether the reviewer now has enough context to
  fairly judge the project end-to-end without guessing missing background.
- Identify the minimum remaining work before confident final submission /
  judging freeze.

## Output Format

Use this exact structure:

### A. Top Findings

List the most important findings first, ordered by severity.
For each finding include:

- severity: critical / high / medium / low
- concise title
- why it matters
- file references
- concrete recommendation

### B. Gate Assessment

State whether each gate is truly:

- G1: pass / borderline / fail
- G2: pass / borderline / fail
- G3: pass / borderline / fail

Keep the explanation brief and evidence-based.

### C. Completion Estimate

Give your own completion percentage for:

- engineering / demo path
- competition materials
- final competition readiness
- overall total

### D. Best Next Actions

Give the top 5 remaining actions with the highest leverage before formal
submission / judging.

### E. Optional Strategic Challenge

If the team is still making one major wrong assumption, say it directly.

## Review Standard

Assume the team does not need encouragement. They need a high-signal final
review that reflects the **current** state of the project and helps them avoid
avoidable mistakes in the final stretch.
"@

Set-Content -LiteralPath $projectContextPath -Value $projectContext -Encoding UTF8
Set-Content -LiteralPath $bundleIndexPath -Value $bundleIndex -Encoding UTF8
Set-Content -LiteralPath $reviewPromptPath -Value $reviewPrompt -Encoding UTF8

if (Test-Path -LiteralPath $zipPath) {
    Remove-Item -LiteralPath $zipPath -Force
}

Compress-Archive -LiteralPath $packageDir -DestinationPath $zipPath -Force

Write-Host "Review bundle created."
Write-Host "Stage directory: $packageDir"
Write-Host "Zip file: $zipPath"
Write-Host "Prompt file: $reviewPromptPath"
