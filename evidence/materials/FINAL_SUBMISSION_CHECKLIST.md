# Final Submission Checklist

## Goal

Turn the current repository into a single clean competition submission package
without reopening scope.

## Background And Target

- Judge this project as a competition work aiming at `national first prize`,
  not as a generic SaaS/platform pitch.
- The strongest current product story is evidence-backed document QA for
  paper/report reading and defense preparation.
- The locked judged-demo path is:
  - `upload -> ask -> citation -> PDF -> refusal`
- As of `2026-04-20`, the main remaining gap is no longer feature work. It is:
  - final native `3`-page PPT production
  - final edited/rendered `5`-minute video production
  - final package and wording consistency

## Status Snapshot (`2026-04-20`)

- [x] strict `G3` evidence recorded in
  `evidence/experiments/20260420_g3_strict_rehearsal.md`
- [x] judge-facing proof pages aligned to the same locked story
- [x] official `3`-page deck source exists in `PPT_DECK_3PAGES_FINAL.md`
- [x] official `5`-minute video source exists in
  `VIDEO_SHOTLIST_5MIN_FINAL.md`
- [x] repo-native `3`-page deck baseline exists in
  `deliverables/competition_kit/deck_3page_final.pdf`
- [x] repo-native `5`-minute subtitle baseline exists in
  `deliverables/competition_kit/video_subtitles_5min_final.srt`
- [ ] final native `3`-page PPT file produced
- [ ] final edited/rendered `5`-minute video produced

## Stop-Ship Items

Do not call the package final if any item below is still open.

- [ ] No final native `3`-page PPT file yet
- [ ] No final `5`-minute video file yet
- [ ] Any high-visibility doc still leads with `PPT_DECK_6SLIDES.md` or
  `VIDEO_SHOTLIST_2MIN.md` instead of the final path
- [ ] The final screenshot set does not match the target demo environment and
  there is no explicit freeze decision
- [ ] Any final material claims broader general stability than the locked
  judged-demo evidence actually proves

## Final Freeze Checklist

### 1. Final Judged Assets

- [ ] Create the final native `3`-page PPT from
  `PPT_DECK_3PAGES_FINAL.md` plus
  `deliverables/competition_kit/deck_3page_final.pdf`
- [ ] Create the final `5`-minute video from
  `VIDEO_SHOTLIST_5MIN_FINAL.md` plus
  `deliverables/competition_kit/video_subtitles_5min_final.srt`
- [ ] Ensure the final PPT/video filenames, cover wording, and version labels
  are stable and do not still look like drafts
- [ ] Ensure no slide/subtitle still shows words such as `draft`, `baseline`,
  `candidate`, `current`, or `next step`

### 2. Evidence And Claim Alignment

- [ ] `PRODUCT_TECHNICAL_WRITEUP.md`, `PLATFORM_USAGE_EVIDENCE.md`,
  `HARD_EVIDENCE_SUMMARY.md`, `SCORING_EVIDENCE_MATRIX.md`, the final PPT,
  and the final video all describe the same product positioning
- [ ] `G3` wording stays at strict fresh-upload `6`-run judged-demo
  (首批 3 + 续 3，fallback 0/6) reproducibility, not open-domain generalization
- [ ] The strongest claim remains evidence-backed `ask`, not generic
  `summary` / `outline`
- [ ] The main story stays `upload -> ask -> citation -> PDF -> refusal`

### 3. Screenshots And Demo Evidence

- [ ] The four core screenshots are current or intentionally frozen:
  - `evidence/screenshots/20260529_gold_ask_research_focus.png`
  - `evidence/screenshots/20260529_gold_pdf_render.png`
  - `evidence/screenshots/20260529_gold_ask_rank_accuracy.png`
  - `evidence/screenshots/20260529_gold_refusal.png`
- [ ] If the target demo environment changed, refresh screenshots before final
  export
- [ ] If screenshots are intentionally reused, keep the spoken story and final
  materials consistent with those exact frozen images

### 4. Material Hygiene

- [ ] `MATERIALS_INDEX.md` and `PRODUCT_TECHNICAL_WRITEUP.md` still point to
  the `3`-page / `5`-minute final path as the primary judged-material route
- [ ] Historical `6`-slide / `2`-minute assets remain archive baselines only
- [ ] No old-provider wording or stale runtime label appears in visible final
  materials
- [ ] `PROJECT_ONE_PAGER.md`, `DEMO_SCRIPT_3MIN.md`,
  `COMPETITION_ASSET_PACK.md`, and `QA_BRIEF.md` all stay aligned with the
  same judged story

### 5. Final Packaging

- [ ] Main submission package contains:
  - final native `3`-page PPT
  - final `5`-minute video
  - `PRODUCT_TECHNICAL_WRITEUP.md`
  - `PLATFORM_USAGE_EVIDENCE.md`
  - `HARD_EVIDENCE_SUMMARY.md`
  - `SCORING_EVIDENCE_MATRIX.md`
  - final screenshot set
  - **平台对账载体（决赛"MaaS API 调用记录"硬约束，勿漏打包）**：
    - `evidence/reports/platform_reconciliation_<封板日>.md` + 同名 `_calls.jsonl` 快照
    - `evidence/reports/baseline_compare_eval.json`（更大样本对账载体）
    - `evidence/screenshots/<封板日>_console_*.png`（控制台汇总 + 时序两张，按 platform_reconciliation H3 口径在代金券号现截；复用 TASK_BOARD 已追踪的"重跑 3 题→新鲜 id→控制台截图"动作）
- [ ] Appendix package contains only supporting evidence and does not replace
  the main judged assets
- [ ] Exported handoff pack still includes the final-source drafts and repo
  baselines for future operators

### 6. 提交包一键验收（codex 复核补：不只查文件在否，还查规格）

- [ ] **3 页 PPT**：文件存在且能在干净机器打开；**页数 ≤ 3**；16:9；封面/版本号不带 `draft`；口径与材料一致（默认 `deepseek-v4-flash`、G3 六轮、4.37×、端侧）
- [ ] **5 分钟视频**：文件存在且可播放；**时长 ≤ 5:00**；旁白/字幕为 strict G3 **六轮**口径；分辨率清晰可读
- [ ] **文件命名 / 大小**：主提交物命名稳定、无乱码、大小在平台上限内
- [ ] **四物口径一致**：PPT / 视频 / 技术文档 / 截图 互不矛盾（模型默认、G3 轮次、token 口径、端侧"持平/补召回"、agentic 不夸"可核验改写"）
- [ ] **平台对账**：`platform_reconciliation_<封板日>` 逐笔 `chatcmpl-` id 无 `None`；控制台截图与逐笔表北京时间时段一致
- [ ] **断网/云 API 异常预案**：明确哪些能力可离线展示（上传/解析/端侧检索/PDF 回链）、哪些必须联网（云端生成），现场断网时的降级话术已备

## Last Pre-Submission Pass

- [ ] Review `SUBMISSION_SPEC_CROSSWALK.md`
- [ ] Review `HANDOFF_PACKAGE_BOUNDARY.md`
- [ ] Review `DEFENSE_DEMO_RISK_CHECKLIST.md`
- [ ] Confirm the package would still make sense to a new operator opening the
  repo cold

## Out Of Scope Right Now

- New features
- OCR rebuilds
- Local-model branch work
- Large UI redesign
- Public SaaS/platform expansion

