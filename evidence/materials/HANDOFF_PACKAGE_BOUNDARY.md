# 交付包边界说明

## 目的

明确哪些文件属于正式主提交，哪些属于答辩附录，哪些只属于制作与操作材料，避免把 baseline、草稿或内部控制文件误发给评委。

## 三层结构

### 1. 主提交

这一层只放评委应该直接看到的正式材料。

建议包含：

1. final `3` 页 PPT
2. final `5` 分钟方案介绍及演示视频
3. `PRODUCT_TECHNICAL_WRITEUP.md`
4. `PLATFORM_USAGE_EVIDENCE.md`
5. `HARD_EVIDENCE_SUMMARY.md`
6. `SCORING_EVIDENCE_MATRIX.md`
7. 四张最终 gold-sample 截图

规则：

- 不放 `baseline / latest / candidate / draft` 命名的源文件
- 不放脚本、HTML 原型、日志原文件、开发遥测汇总

### 2. 答辩附录

这一层放“评委追问时可以马上出示，但不应该占主叙事”的材料。

建议包含：

1. `evidence/reports/gold_sample_qa_compare_latest.md`
2. `evidence/reports/gold_sample_replay_real_summary_latest.md`
3. `evidence/reports/gold_sample_replay_real_latest.md`
4. `GOLD_SAMPLE_RUNBOOK.md`
5. `QA_BRIEF.md`
6. `evidence/experiments/20260419_q2_declared_stability_check.md`
7. `evidence/experiments/20260419_g3_rehearsal_template.md`
8. appendix-only 截图，如 `stats_panel` / `api_docs`

规则：

- 附录可以回答追问，但不能替代主提交
- 附录里的“warm-state / fallback / request id”信息只在被追问时展开

### 3. 操作与制作材料

这一层只服务于队内制作、排练、导出和版本控制，不直接发评委。

建议包含：

1. `PROJECT_ONE_PAGER.md`
2. `DEMO_SCRIPT_3MIN.md`
3. `COMPETITION_ASSET_PACK.md`
4. `PPT_DECK_6SLIDES.md`
5. `VIDEO_SHOTLIST_2MIN.md`
6. `POSTER_COPY.md`
7. `deliverables/competition_kit/`
8. `scripts/export_competition_asset_pack.ps1`
9. `scripts/export_competition_pdfs.js`

规则：

- 这些文件帮助产出正式材料，但本身不是正式提交物
- 如果对外发送，必须明确标注为 source baseline 或制作资料

## 当前执行口径

1. `SUBMISSION_SPEC_CROSSWALK.md` 负责说明“规格有没有对上”。
2. `SUBMISSION_PREP_GUIDE.md` 负责说明“最后要交什么、如何导出”。
3. 本页负责说明“哪些材料能给评委，哪些只能给队内或操作员”。

## 封板前必查

- 主提交中不再出现 `baseline / draft / candidate / latest / current / next step`
- 附录中的 request id、实验记录、warm-state 说明都有主证据页可回指
- 操作资料不会混入正式主提交目录
