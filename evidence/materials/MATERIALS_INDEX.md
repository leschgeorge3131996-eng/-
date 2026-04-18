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

14. [GOLD_SAMPLE_RUNBOOK.md](./GOLD_SAMPLE_RUNBOOK.md)
- 当前锁定 gold-sample candidate 的演示 / 截图 runbook

15. [../reports/gold_sample_qa_compare_latest.md](../reports/gold_sample_qa_compare_latest.md)
- 当前锁定 gold-sample candidate 的双模型比较结论

16. [../reports/gold_sample_replay_real_summary_latest.md](../reports/gold_sample_replay_real_summary_latest.md)
- 当前锁定 gold-sample candidate 的真实 replay 汇总（权威最新版）

17. [../reports/gold_sample_replay_real_latest.md](../reports/gold_sample_replay_real_latest.md)
- 当前锁定 gold-sample candidate 的真实 replay 明细（权威最新版）

18. [../reports/sample_replay_real_summary_latest.md](../reports/sample_replay_real_summary_latest.md)
- 更宽样例覆盖的真实模型复跑汇总（次级参考）

19. [../reports/sample_replay_real_latest.md](../reports/sample_replay_real_latest.md)
- 更宽样例覆盖的真实模型逐条复跑明细（次级参考）

20. [../../deliverables/competition_kit/README.md](../../deliverables/competition_kit/README.md)
- 可打印的 deck / poster HTML 原型说明

## 使用建议

- 报名表 / 作品简介：优先参考 `PROJECT_ONE_PAGER.md`
- 现场展示 / 录屏脚本：优先参考 `DEMO_SCRIPT_3MIN.md`
- 固定演示内容：优先参考 `SAMPLE_SET.md` 与 `GOLD_SAMPLE_RUNBOOK.md`
- 技术路线说明：优先参考 `ARCHITECTURE.md`
- 比赛/评审复跑与证据刷新：优先参考 `GOLD_SAMPLE_CANDIDATE_20260418.json`、`REAL_REPLAY_GUIDE.md` 与 `scripts/run_real_replay.ps1`
- PPT / 视频 / 海报统一资产收口：优先参考 `COMPETITION_ASSET_PACK.md`
- PPT 页面稿：优先参考 `PPT_DECK_6SLIDES.md`
- 视频口播与镜头：优先参考 `VIDEO_SHOTLIST_2MIN.md`
- 海报文案：优先参考 `POSTER_COPY.md`
- 最终打包导出：运行 `powershell -ExecutionPolicy Bypass -File .\scripts\export_competition_asset_pack.ps1`
- 可打印 HTML 成品原型：参考 `deliverables/competition_kit/`
- PDF 导出：运行 `node scripts/export_competition_pdfs.js`
- 当前 PDF 基线：`deliverables/competition_kit/deck.pdf`、`deliverables/competition_kit/poster.pdf`
- 更宽样例补充复跑：参考 `SAMPLE_MANIFEST.json` 与 `scripts/replay_sample_set.py`
- 真实证据收口：优先参考 `REAL_EVIDENCE_REFRESH_CHECKLIST.md`
- 最终提交准备：优先参考 `SUBMISSION_PREP_GUIDE.md`
- QA 模型决策：优先参考 `evidence/reports/gold_sample_qa_compare_latest.md`
- 当前锁定 gold-sample 证据：优先参考 `evidence/reports/gold_sample_replay_real_summary_latest.md`
- 更宽样例的 route-tier / outcome / response-detail / grounding 对比：参考 `evidence/reports/sample_replay_real_summary_latest.md`
- 答辩准备：优先参考 `QA_BRIEF.md`
- 更宽样例的真实模型结果总览：参考 `evidence/reports/sample_replay_real_summary_latest.md`
- 更宽样例的真实模型逐条证据：参考 `evidence/reports/sample_replay_real_latest.md`
- `latest_log_summary.md` 仅作为全历史开发遥测，不作为 replay 权威结论
