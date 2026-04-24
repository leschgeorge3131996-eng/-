# 评分项与证据映射

## 目的

把官方评分线和仓库里的实际材料一一对齐，避免答辩时只能“概括性地说做了很多”，却拿不出对应证据。

本页按 `2026-03-11` 发布的赛题清单理解整理：

- 平台使用：`20`
- 产品能力：`40`
- 技术能力：`40`
- 决赛阶段额外看现场答辩与演示效果

官方源：`https://www.cie.org.cn/static/upload/file/20260311/1773194947123865.pdf`

## 总表

| 评分线 | 评委想看什么 | 当前主证据 | 答辩时怎么讲 |
| --- | --- | --- | --- |
| 平台使用 `20` | 是否真实使用无问芯穹平台，而不是口头挂名 | `PLATFORM_USAGE_EVIDENCE.md`、`evidence/reports/gold_sample_qa_compare_latest.md`、`evidence/reports/gold_sample_replay_real_summary_latest.md`、真实 request id 与截图 | 我们不是只把平台放进环境变量，而是把主链路真实切到无问芯穹，并保留了模型、请求记录、截图和 replay 证据。 |
| 产品能力 `40` | 作品是否围绕清晰场景解决真实问题，是否有稳定、可理解的用户价值 | `PROJECT_ONE_PAGER.md`、`PRODUCT_TECHNICAL_WRITEUP.md`、最终 `3` 页 PPT / `5` 分钟视频、四张核心截图 | 我们解决的是“论文/报告阅读时能答、还能回到证据”的问题，不是泛化聊天。 |
| 技术能力 `40` | 技术链路是否成立，是否有可验证的工程细节与实验支撑 | `HARD_EVIDENCE_SUMMARY.md`、`ARCHITECTURE.md`、`evidence/reports/gold_sample_qa_compare_latest.md`、`evidence/reports/gold_sample_replay_real_summary_latest.md`、`evidence/experiments/20260419_q2_declared_stability_check.md`、`evidence/reports/extended_eval_v1_latest.md` | 主链路是 `upload -> ask -> citation -> PDF -> refusal`，不是只给一个答案，而是把检索、引用、PDF 回链和拒答闸门都做实。 |
| 现场演示 / 答辩 | 是否能稳、能复现、能扛追问 | `GOLD_SAMPLE_RUNBOOK.md`、`QA_BRIEF.md`、`HARD_EVIDENCE_SUMMARY.md`、最终截图集、最终 `3` 页 PPT / `5` 分钟视频 | 演示不现场 improvisation，只走锁定样例、锁定问题和预定备用路径；追问时按证据页和 runbook 回答。 |

## 平台使用：评委追问点

### 追问 1：你们到底有没有真实用无问芯穹？

优先出示：

- `PLATFORM_USAGE_EVIDENCE.md`
- `evidence/reports/gold_sample_qa_compare_latest.md`
- `evidence/reports/gold_sample_replay_real_summary_latest.md`

补充点：

- 当前默认 QA 模型：`qwen3-235b-a22b-instruct-2507`
- 已验证 fast fallback：`qwen3-next-80b-a3b-instruct`（`qwen3-32b` 保留为历史 gold-sample fallback）
- 有真实 request id、截图、replay 结果，而不是只说“接口已经接通”

### 追问 2：平台使用如何影响作品得分？

答法：

- 平台不是背景板，而是主 QA 路径的真实运行底座。
- 我们保留了模型决策、request id、真实 replay 和调用截图，能把“用了平台”讲成“用了平台并留下可核验证据”。

## 产品能力：评委追问点

### 追问 1：你们和普通文档问答有什么区别？

优先出示：

- `PROJECT_ONE_PAGER.md`
- `DEMO_SCRIPT_3MIN.md`
- `evidence/screenshots/20260419_gold_ask_research_focus.png`
- `evidence/screenshots/20260419_gold_pdf_render.png`

答法：

- 差异点不是“能回答”，而是“回答能回到 PDF 原文证据”。
- 对论文阅读和答辩准备场景来说，`citation -> PDF` 比“更像聊天”更有价值。

### 追问 2：为什么不主讲摘要和提纲？

答法：

- `summary / outline` 是支持能力，但当前最强、最可核验的能力是 `ask`。
- 我们主动把主卖点收束到证据最强的一条链路，是为了提高可信度，而不是为了炫功能数量。

## 技术能力：评委追问点

### 追问 1：你们的技术亮点是什么？

优先出示：

- `ARCHITECTURE.md`
- `HARD_EVIDENCE_SUMMARY.md`
- `evidence/screenshots/20260419_gold_refusal.png`

答法：

1. 页级结构化解析保留 `block / line / bbox`
2. `ask` 先检索再作答，并返回 citation；模型给出逐字 quote 时后端会做原文子串校验
3. citation 可回到 PDF 原页做高亮与旁证展示
4. 检索无命中时显式拒答；关键词命中但无真实依据时 LLM 层二次拒答
5. 量化指标（双层样本量披露）：
   - **锁定 `3` 题 strict G3**：证据声明率 `100%`、引用准确率 `100%`、拒答精确率 `100%`、跨轮一致性 `100%`（详见 `quantitative_eval_metrics.md`）
   - **扩展 `51` 题 full**：旧版 `46/51` 用于暴露边界；最终默认模型 + 定向检索/上下文修复后为 `51/51`，**拒答精确率 `100%`**、引用页码命中率 `100%`、证据声明率 `100%`（详见 `extended_eval_v1_latest.md`、范围见 `EXTENDED_EVAL_SCOPE.md`）

### 追问 2：你们怎么证明不是只会演示一题？

优先出示：

- `evidence/reports/gold_sample_qa_compare_latest.md`
- `evidence/reports/gold_sample_replay_real_summary_latest.md`
- `evidence/experiments/20260419_q2_declared_stability_check.md`
- `evidence/reports/extended_eval_v1_latest.md`（`51` 题扩展评测，涵盖中英双语论文 + 中文短文档 × A1-A5 答题 + B1-B2 拒答）

答法：

- 锁定 `3` 题是 judged-demo path 的最强可复现证据；为了回答"`3` 题 `100%` 是不是小样本幻觉"，我们把样本量从 `3` → `20` → 扩到 `51` 题（中英论文 + 中文短文档）。旧版 `46/51` 暴露 retrieval 边界；最终默认模型在定向检索/上下文修复后闭环为 `51/51`，拒答精确率 `100%`、引用页码命中率 `100%`。
- 扩展评测暴露并闭环了两个真实问题：
  1. prompt 强制 `evidence_quotes` 非空导致诱导拒答场景下硬答，拒答精确率一度为 `0%`（commit `7f2713d` 修复）
  2. 元信息类 query（作者 / 主要贡献）召回首页 chunk 不稳，曾有 `3` 道题失败（metadata intent fallback 修复）
- 旧版剩余 `5` 道失败全部落在表格单列数据 / abstract 隐含结论 / 小 markdown 文档上，都是 retrieval 颗粒度真实边界；最终修复选择的是 retrieval/context 工程补丁，而不是更换模型或把 digest 当严格证据。
- 这是"有实验 + 会复盘 + 会修 + 仍说明边界"的具体佐证，不是"3 题 100%"那种只跑一次就包装的数字。注意：`51/51` 是固定扩展评测集回归，不应表述为开放域任意论文 `100%`。

## 现场演示与答辩：评委追问点

### 追问 1：如果现场延迟高或者 live 失手怎么办？

优先出示：

- `GOLD_SAMPLE_RUNBOOK.md`
- `QA_BRIEF.md`
- 最终四张核心截图

答法：

- 主链路、题组、fallback 模型、截图切换顺序都是预先锁定的。
- live 是第一选择，但不是唯一证据。我们的提交包和答辩包都能独立证明主链路已经真实跑通。

### 追问 2：你们如何保证材料之间口径一致？

优先出示：

- `SUBMISSION_SPEC_CROSSWALK.md`
- `COMPETITION_ASSET_PACK.md`
- 本页

答法：

- 规格对账页负责“交什么”，资产包负责“怎么统一说”，评分映射页负责“每一分拿什么证据去对”。

## 使用顺序建议

1. 开场先用 `PROJECT_ONE_PAGER.md` 定位场景与价值。
2. 随后用 `HARD_EVIDENCE_SUMMARY.md` 讲最强主链路。
3. 评委一问到“是否真实使用无问芯穹”，立刻切 `PLATFORM_USAGE_EVIDENCE.md`。
4. 评委追问“这项分数怎么拿”，立刻切本页。
