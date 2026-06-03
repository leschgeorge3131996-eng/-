# 🤝 团队交接总索引（谁做什么）

> 离交付约 2 周。代码/材料侧已收口（口径统一、证据量化、全推 GitHub）。**剩下的全是"产出文件"和"现场"，不在代码里。**

## 谁做什么

| 负责人 | 任务 | 详细接收文档 | 建议截止 |
|---|---|---|---|
| 组员 A | **3 页 PPT 成片（.pptx）** | **`agent_handoff/HANDOFF_PPT.md`** | 06-10 |
| 组员 B | **5 分钟演示视频成片（.mp4）** | **`agent_handoff/HANDOFF_VIDEO.md`** | 06-12 |
| 你（队长） | ① 代金券号控制台用量截图 ② 核 deepseek-v4-flash 真实折后价 | 见下 | 封板前 |

> **这两件成片是阻断项**：不产出文件 = 整作品无法提交、0 分。源稿和基线全齐，缺的只是"做成文件"。

## 你（队长）的两件小事

1. **控制台截图**（决赛 MaaS 调用记录硬约束）：登领 200 代金券那个号 → 大模型服务平台 → 用量统计 → 统计周期选 `2026-06-02` → 截两张（汇总页 + 该模型详情时序图）存 `evidence/screenshots/20260602_console_*.png`。口径见 `evidence/reports/platform_reconciliation_20260602.md`。
2. **核单价**：`COMMERCIALIZATION_CASE.md` 里已按 ¥1/百万 token 估算，封板前用代金券号控制台当日折后价复核一下即可（结论稳，单价只会更低）。

## 全队共享的"诚实红线"（PPT/视频/答辩都要守）

- 成绩按**不混评测集**：默认 Flash `48/51`、V6 `71/72`、rollback `51/51`；**不说开放域 100%**。
- strict G3 = **六轮**（不是三轮）。
- 默认模型 = **`deepseek-v4-flash`**；`235b` 是 rollback。
- 端侧"持平/补召回"，**不说"显著提升"**；智能体讲"有界自评重试"，**不说"可现场核验改写"**。
- 4.37× / 86.6% **连"准确率持平"**一起说。
- 定位 = "引用可核验的**论文/答辩**助手"，**不说**"通用 SaaS / 智能办公工具"。

## 答辩前必看
- `evidence/materials/JUDGE_SCORING_MAP.md` —— 每个评分维度→在哪看+一句话证据
- `evidence/materials/QA_FLASHCARD.md` —— 口径速记卡

## 完整提交包
- **初赛**：3页PPT + 5min视频 + `PRODUCT_TECHNICAL_WRITEUP.md` + 支撑（`PLATFORM_USAGE_EVIDENCE`/`HARD_EVIDENCE_SUMMARY`/`SCORING_EVIDENCE_MATRIX` + 4 张金标截图）
- **决赛额外**：答辩PPT + MaaS 调用记录（`platform_reconciliation_20260602.*` + 控制台截图）
- 封板照 `evidence/materials/FINAL_SUBMISSION_CHECKLIST.md` 勾一遍（含 §6 提交验收清单）
