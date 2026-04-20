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
| 技术能力 `40` | 技术链路是否成立，是否有可验证的工程细节与实验支撑 | `HARD_EVIDENCE_SUMMARY.md`、`ARCHITECTURE.md`、`evidence/reports/gold_sample_qa_compare_latest.md`、`evidence/reports/gold_sample_replay_real_summary_latest.md`、`evidence/experiments/20260419_q2_declared_stability_check.md` | 主链路是 `upload -> ask -> citation -> PDF -> refusal`，不是只给一个答案，而是把检索、引用、PDF 回链和拒答闸门都做实。 |
| 现场演示 / 答辩 | 是否能稳、能复现、能扛追问 | `GOLD_SAMPLE_RUNBOOK.md`、`QA_BRIEF.md`、`HARD_EVIDENCE_SUMMARY.md`、最终截图集、最终 `3` 页 PPT / `5` 分钟视频 | 演示不现场 improvisation，只走锁定样例、锁定问题和预定备用路径；追问时按证据页和 runbook 回答。 |

## 平台使用：评委追问点

### 追问 1：你们到底有没有真实用无问芯穹？

优先出示：

- `PLATFORM_USAGE_EVIDENCE.md`
- `evidence/reports/gold_sample_qa_compare_latest.md`
- `evidence/reports/gold_sample_replay_real_summary_latest.md`

补充点：

- 当前默认 QA 模型：`qwen3-235b-a22b-instruct-2507`
- 已验证 fallback：`qwen3-32b`
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
2. `ask` 先检索再作答，并返回 citation 与 evidence quotes
3. citation 可回到 PDF 原页做高亮与旁证展示
4. 检索无命中时显式拒答，而不是编造
5. 量化指标：证据声明率 `100%`、引用准确率 `100%`、拒答精确率 `100%`、跨轮一致性 `100%`（strict G3 三轮 fresh-upload 评测，详见 `quantitative_eval_metrics.md`）

### 追问 2：你们怎么证明不是只会演示一题？

优先出示：

- `evidence/reports/gold_sample_qa_compare_latest.md`
- `evidence/reports/gold_sample_replay_real_summary_latest.md`
- `evidence/experiments/20260419_q2_declared_stability_check.md`

答法：

- 当前最强 judge-facing 证据是锁定题组。
- 其中不仅有 `2 answerable + 1 refusal`，还有对数值题的单独 fresh rerun。
- 我们不会把 broader replay 伪装成主证据，但会把它作为次级覆盖说明。

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
