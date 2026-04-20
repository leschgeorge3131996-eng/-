# Materials Index

## 当前材料

1. [PROJECT_ONE_PAGER.md](./PROJECT_ONE_PAGER.md)
- 一页式项目说明

2. [DEMO_SCRIPT_3MIN.md](./DEMO_SCRIPT_3MIN.md)
- 3 分钟演示脚本

3. [SAMPLE_SET.md](./SAMPLE_SET.md)
- 固定样例集与演示建议

4. [ARCHITECTURE.md](./ARCHITECTURE.md)
- 架构说明与设计原则

5. [SAMPLE_MANIFEST.json](./SAMPLE_MANIFEST.json)
- 更宽样例覆盖的固定样例清单，供补充复跑使用

6. [REAL_EVIDENCE_REFRESH_CHECKLIST.md](./REAL_EVIDENCE_REFRESH_CHECKLIST.md)
- 真实模型复跑后的证据刷新清单

7. [SUBMISSION_PREP_GUIDE.md](./SUBMISSION_PREP_GUIDE.md)
- 参赛提交准备说明

8. [COMPETITION_ASSET_PACK.md](./COMPETITION_ASSET_PACK.md)
- 把 gold-sample 截图、报告和口径收成 PPT / 视频 / 海报统一资产包

9. [PPT_DECK_6SLIDES.md](./PPT_DECK_6SLIDES.md)
- 六页 PPT 现成页面稿

10. [VIDEO_SHOTLIST_2MIN.md](./VIDEO_SHOTLIST_2MIN.md)
- 2 分钟视频分镜与口播稿

11. [POSTER_COPY.md](./POSTER_COPY.md)
- 海报版面文案稿

12. [REAL_REPLAY_GUIDE.md](./REAL_REPLAY_GUIDE.md)
- 真实模型复跑说明

13. [QA_BRIEF.md](./QA_BRIEF.md)
- 常见答辩问答提纲

14. [SUBMISSION_SPEC_CROSSWALK.md](./SUBMISSION_SPEC_CROSSWALK.md)
- 官方提交规格与当前仓库资产的逐项对账表

15. [PLATFORM_USAGE_EVIDENCE.md](./PLATFORM_USAGE_EVIDENCE.md)
- 无问芯穹平台使用的 judge-facing 证据页

16. [HARD_EVIDENCE_SUMMARY.md](./HARD_EVIDENCE_SUMMARY.md)
- 当前最强 judge-proof 证据摘要

17. [PRODUCT_TECHNICAL_WRITEUP.md](./PRODUCT_TECHNICAL_WRITEUP.md)
- 正式产品及技术文档

18. [SCORING_EVIDENCE_MATRIX.md](./SCORING_EVIDENCE_MATRIX.md)
- 官方评分项与当前 judge-facing 证据的对照页

19. [HANDOFF_PACKAGE_BOUNDARY.md](./HANDOFF_PACKAGE_BOUNDARY.md)
- 主提交、答辩附录与操作资料的边界说明

20. [STRICT_G3_EXECUTION_PLAN.md](./STRICT_G3_EXECUTION_PLAN.md)
- 严格版 G3 的角色分工、操作步骤、记录字段与验收标准

21. [GOLD_SAMPLE_RUNBOOK.md](./GOLD_SAMPLE_RUNBOOK.md)
- 当前锁定 gold-sample candidate 的演示 / 截图 runbook

22. [../reports/gold_sample_qa_compare_latest.md](../reports/gold_sample_qa_compare_latest.md)
- 当前锁定 gold-sample candidate 的双模型比较结论

23. [../reports/gold_sample_replay_real_summary_latest.md](../reports/gold_sample_replay_real_summary_latest.md)
- 当前锁定 gold-sample candidate 的真实 replay 汇总

24. [../reports/gold_sample_replay_real_latest.md](../reports/gold_sample_replay_real_latest.md)
- 当前锁定 gold-sample candidate 的真实 replay 明细

25. [../reports/sample_replay_real_summary_latest.md](../reports/sample_replay_real_summary_latest.md)
- 更宽样例覆盖的真实模型复跑汇总（次级参考）

26. [../reports/sample_replay_real_latest.md](../reports/sample_replay_real_latest.md)
- 更宽样例覆盖的真实模型逐条复跑明细（次级参考）

27. [../../deliverables/competition_kit/README.md](../../deliverables/competition_kit/README.md)
- 可打印的 deck / poster HTML 原型说明

28. [../experiments/20260420_g3_strict_rehearsal.md](../experiments/20260420_g3_strict_rehearsal.md)
- 严格版 `G3` 三轮权威记录，包含 request id、log-backed 时长与 fallback 结论

## 使用建议

- 报名表 / 作品简介：优先参考 `PROJECT_ONE_PAGER.md`
- 官方提交规格对账：优先参考 `SUBMISSION_SPEC_CROSSWALK.md`
- 平台使用说明：优先参考 `PLATFORM_USAGE_EVIDENCE.md`
- judge-facing 强证据摘要：优先参考 `HARD_EVIDENCE_SUMMARY.md`
- 正式产品 / 技术说明：优先参考 `PRODUCT_TECHNICAL_WRITEUP.md`
- 官方评分项对照：优先参考 `SCORING_EVIDENCE_MATRIX.md`
- 主提交 / 附录 / 操作资料边界：优先参考 `HANDOFF_PACKAGE_BOUNDARY.md`
- 严格版 G3 执行：优先参考 `STRICT_G3_EXECUTION_PLAN.md`
- 严格版 G3 实验记录：优先参考 `evidence/experiments/20260420_g3_strict_rehearsal.md`
- 现场展示 / 录屏脚本：优先参考 `DEMO_SCRIPT_3MIN.md`
- 固定演示内容：优先参考 `SAMPLE_SET.md` 与 `GOLD_SAMPLE_RUNBOOK.md`
- 技术路线说明：优先参考 `ARCHITECTURE.md`
- 比赛 / 评审复跑与证据刷新：优先参考 `GOLD_SAMPLE_CANDIDATE_20260418.json`、`REAL_REPLAY_GUIDE.md` 与 `scripts/run_real_replay.ps1`
- PPT / 视频 / 海报统一资产收口：优先参考 `COMPETITION_ASSET_PACK.md`
- PPT 页面稿：优先参考 `PPT_DECK_6SLIDES.md`
- 视频口播与镜头：优先参考 `VIDEO_SHOTLIST_2MIN.md`
- 海报文案：优先参考 `POSTER_COPY.md`
- 最终打包导出：运行 `powershell -ExecutionPolicy Bypass -File .\scripts\export_competition_asset_pack.ps1`
- 可打印 HTML 成品原型：参考 `deliverables/competition_kit/`
- PDF 导出：运行 `node scripts/export_competition_pdfs.js`
- 当前 PDF 基线：`deliverables/competition_kit/deck.pdf`、`deliverables/competition_kit/poster.pdf`
- 视频字幕基线：`deliverables/competition_kit/video_subtitles.srt`
- 更宽样例补充复跑：参考 `SAMPLE_MANIFEST.json` 与 `scripts/replay_sample_set.py`
- 真实证据收口：优先参考 `REAL_EVIDENCE_REFRESH_CHECKLIST.md`
- 最终提交准备：优先参考 `SUBMISSION_PREP_GUIDE.md`
- QA 模型决策：优先参考 `evidence/reports/gold_sample_qa_compare_latest.md`
- 当前锁定 gold-sample 证据：优先参考 `evidence/reports/gold_sample_replay_real_summary_latest.md`
- 更宽样例的 route-tier / outcome / response-detail / grounding 对比：参考 `evidence/reports/sample_replay_real_summary_latest.md`
- 答辩准备：优先参考 `QA_BRIEF.md`
- `latest_log_summary.md` 仅作为全历史开发遥测，不作为 replay 权威结论
