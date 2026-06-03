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
| **赛题主题：端侧/云端协同** | 作品是否回应赛题一"端侧/云端协同应用"命题，而非纯云端网页 | `ARCHITECTURE.md`（Edge\|近端\|Cloud 分层图）、`evidence/reports/edge_hybrid_eval.md`、`evidence/reports/token_compression_eval.md` | 近端跑**本地句向量模型（BGE-small-zh-v1.5 ONNX，纯 CPU、零云依赖）**做语义编码与词法+语义混合检索——这是**真实的端侧 ML 算力实体**（小模型在端理解、大模型在云生成），不是纯云端网页。诚实标注：语义检索与已高度调优的词法**持平、零回归**，价值在实体本身与措辞鲁棒性、非检索刷分。Token 压缩（长文 ask 平均省 86.6%）是协同的另一量化收益。 |
| 平台使用 `20` | 是否真实使用无问芯穹平台，而不是口头挂名 | `PLATFORM_USAGE_EVIDENCE.md`、`data/logs/call_logs.jsonl`（含平台 request_id）、`evidence/reports/gold_sample_qa_compare_latest.md`、调用截图 | 我们不是只把平台放进环境变量，而是把主链路真实切到无问芯穹；每次调用都落 token 与**平台 request_id**，可在 infini-ai 控制台逐条对账（本地 request_id 仅作内部追踪）。 |
| 产品能力 `40` | 作品是否围绕清晰场景解决真实问题，是否有稳定、可理解的用户价值 | `PROJECT_ONE_PAGER.md`、`PRODUCT_TECHNICAL_WRITEUP.md`、最终 `3` 页 PPT / `5` 分钟视频、四张核心截图 | 我们解决的是“论文/报告阅读时能答、还能回到证据”的问题，不是泛化聊天。 |
| 技术能力 `40` | 技术链路是否成立，是否有可验证的工程细节与实验支撑 | `HARD_EVIDENCE_SUMMARY.md`、`ARCHITECTURE.md`、`evidence/reports/gold_sample_qa_compare_latest.md`、`evidence/reports/gold_sample_replay_real_summary_latest.md`、`evidence/experiments/20260419_q2_declared_stability_check.md`、`evidence/reports/extended_eval_v1_latest.md` | 主链路是 `upload -> ask -> citation -> PDF -> refusal`，不是只给一个答案，而是把检索、引用、PDF 回链和拒答闸门都做实。 |
| 现场演示 / 答辩 | 是否能稳、能复现、能扛追问 | `GOLD_SAMPLE_RUNBOOK.md`、`QA_BRIEF.md`、`HARD_EVIDENCE_SUMMARY.md`、最终截图集、最终 `3` 页 PPT / `5` 分钟视频 | 演示不现场 improvisation，只走锁定样例、锁定问题和预定备用路径；追问时按证据页和 runbook 回答。 |

## 加分项（各 5 分）

来源：赛题指南第 117-118 页。

| 加分项 | 当前命中情况 | 证据 |
| --- | --- | --- |
| 平台利用率 `5` | 主链路真实跑在无问芯穹 MaaS，多任务多模型路由（QA=`deepseek-v4-flash` / summary·outline=`qwen3-235b` / 验证 fallback），调用留痕含**平台 request_id** 可在 infini-ai 控制台对账 | `PLATFORM_USAGE_EVIDENCE.md`、`data/logs/call_logs.jsonl` |
| 商业化潜力 `5` | 已选定 **B 端高校实验室/课题组席位**为主路径 + C 端答辩季入口，完成市场量级 / 竞品差异 / 单位经济（token 压缩支撑低边际成本）/ 获客论证 | `COMMERCIALIZATION_CASE.md` |
| 大模型与智能体能力 `5` | 主链路使用无问芯穹大模型 + 单层 **agentic 检索循环**（检索→模型自评证据是否充分→不足则改写 query 补检索→2 轮收敛，`agent_iterations/query_rewrites` 落日志）+ 检索/模型双层拒答 | `ARCHITECTURE.md` 设计点 4、`HARD_EVIDENCE_SUMMARY.md` 第 9 节 |
| **Token 消耗压缩 `5`** | **三层预处理流水线，长文档 ask 平均节省 `86.6%`，峰值 `93.1%`（Attention 论文 `10,263 → 704` tokens）；同时是端侧/云端协同的量化收益** | **`evidence/reports/token_compression_eval.md`、`HARD_EVIDENCE_SUMMARY.md` 第 8 节** |

## 平台使用：评委追问点

### 追问 1：你们到底有没有真实用无问芯穹？

优先出示：

- `PLATFORM_USAGE_EVIDENCE.md`
- `evidence/reports/gold_sample_qa_compare_latest.md`
- `evidence/reports/gold_sample_replay_real_summary_latest.md`

补充点：

- 当前默认 QA 模型：`deepseek-v4-flash`（V6 contract-patch holdout 后切换，详见 `evidence/reports/holdout_eval_v6_contract_patch_qwen_vs_flash_20260430.md`）
- rollback fallback：`qwen3-235b-a22b-instruct-2507`（gold sample 双模型 `3 / 3` 验证就是用它跑的，仍是受信任的回滚路径）
- `summary` / `outline` 仍跑在 `qwen3-235b-a22b-instruct-2507`，未单独重测前不切换
- 历史 fast fallback `qwen3-next-80b-a3b-instruct`、历史金标 fallback `qwen3-32b` 仍保留可用
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
- `evidence/screenshots/20260529_gold_ask_research_focus.png`
- `evidence/screenshots/20260529_gold_pdf_render.png`

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
- `evidence/screenshots/20260529_gold_refusal.png`

答法：

1. 页级结构化解析保留 `block / line / bbox`
2. `ask` 先检索再作答，并返回 citation；模型给出逐字 quote 时后端会做原文子串校验
3. citation 可回到 PDF 原页做高亮与旁证展示
4. 检索无命中时显式拒答；关键词命中但无真实依据时 LLM 层二次拒答
5. 量化指标（双层样本量披露）：
   - **锁定 `3` 题 strict G3**：证据声明率 `100%`、引用准确率 `100%`、拒答精确率 `100%`、跨轮一致性 `100%`（详见 `quantitative_eval_metrics.md`）
   - **扩展 `51` 题 full**：旧版 `46/51` 用于暴露边界；rollback 模型 `qwen3-235b-a22b-instruct-2507` 在定向检索/上下文修复后闭环为 `51/51`（拒答精确率/引用页码命中率/证据声明率均 `100%`）。**当前默认 `deepseek-v4-flash` 在同一 51 题固定集为 `48/51`（94.1%）**，并在更难的 V6 extreme holdout 上达 `71/72`、拒答精确率 `100%`、引用准确率 `98.3%`（即"现场实际跑的默认模型"在更严苛集上反而更强；详见 `holdout_eval_v6_contract_patch_qwen_vs_flash_20260430.md`、`extended_eval_v1_*`，范围见 `EXTENDED_EVAL_SCOPE.md`）

### 追问 2：你们怎么证明不是只会演示一题？

优先出示：

- `evidence/reports/gold_sample_qa_compare_latest.md`
- `evidence/reports/gold_sample_replay_real_summary_latest.md`
- `evidence/experiments/20260419_q2_declared_stability_check.md`
- `evidence/reports/extended_eval_v1_latest.md`（`51` 题扩展评测，涵盖中英双语论文 + 中文短文档 × A1-A5 答题 + B1-B2 拒答）
- `evidence/reports/judged_eval_human_review_20260602.md` + `judged_eval_generalization_human_review_20260602.md`（三层判分 + 泛化 176 题 + 人复核）
- `evidence/reports/edge_ab_generalization_20260602.md`（端侧检索开/关 A/B：难文档补召回、固定集零变化）

答法：

- 锁定 `3` 题是 judged-demo path 的最强可复现证据；为了回答"`3` 题 `100%` 是不是小样本幻觉"，我们把样本量从 `3` → `20` → 扩到 `51` 题（中英论文 + 中文短文档）。旧版 `46/51` 暴露 retrieval 边界；rollback 模型 `qwen3-235b` 在定向检索/上下文修复后闭环为 `51/51`，拒答精确率 `100%`、引用页码命中率 `100%`；当前默认 `deepseek-v4-flash` 在同集为 `48/51`（94.1%），并在更难的 V6 holdout 上达 `71/72`（拒答 `100%`、引用 `98.3%`）——口径以现场实际模型为准，不把 rollback 的 51/51 说成默认模型成绩。
- 扩展评测暴露并闭环了两个真实问题：
  1. prompt 强制 `evidence_quotes` 非空导致诱导拒答场景下硬答，拒答精确率一度为 `0%`（commit `7f2713d` 修复）
  2. 元信息类 query（作者 / 主要贡献）召回首页 chunk 不稳，曾有 `3` 道题失败（metadata intent fallback 修复）
- 旧版剩余 `5` 道失败全部落在表格单列数据 / abstract 隐含结论 / 小 markdown 文档上，都是 retrieval 颗粒度真实边界；最终修复选择的是 retrieval/context 工程补丁，而不是更换模型或把 digest 当严格证据。
- 这是"有实验 + 会复盘 + 会修 + 仍说明边界"的具体佐证，不是"3 题 100%"那种只跑一次就包装的数字。注意：`51/51` 是固定扩展评测集回归，不应表述为开放域任意论文 `100%`。
- **再进一步：把评测做成"三层交叉 + 人兜底"（`judged_eval_*_20260602`、`*_human_review_20260602`、`edge_ab_generalization_20260602`）——这才是"可量化、可复现、诚实"的硬证据：**
  1. **判分式**：不止看自动指标（页码 / 关键词命中），让**另一个更强模型（`qwen3-235b`）当裁判**逐题判对错 + 是否有据，**再由人复核每个判错**。过程本身暴露"单一 LLM 裁判也会系统性误判"——初版把对的判错 5 个（一例系统答案竟比我们自己 manifest 参考还准），给裁判喂原文后纠正。**连判官、参考答案都不全信，要交叉 + 人核。**
  2. **泛化测试**：让强模型读 16 份文档**现造 176 道全新（未精选）题**，判分 **88.6%**——比固定集近满分实在，**主动暴露两个真弱点**（英文 / 多语文档"过度拒答"、多行表格算术），公开不藏；48 道拒答陷阱 **0 编造**。
  3. **端侧 A/B**：同一批题端侧语义检索开 / 关对照——难文档**补召回**（过度拒答 `6→1`、0 新增编造），固定集**零变化**（安全）；阈值调优实验还证伪了"靠调参刷分"。
  一句话：**我们把评测当成找自己问题的工具，不是包装分数的工具**——自动指标→判分→泛化→A/B、且层层人核。

### 追问 3：你们有做 Token 消耗压缩吗？

优先出示：

- `evidence/reports/token_compression_eval.md`
- `HARD_EVIDENCE_SUMMARY.md` 第 8 节
- 脚本 `scripts/eval_token_compression.py`（评委现场可复跑）

答法：

- 我们的预处理是三层流水线：解析归一化 → 结构化切块（`ChunkService` 900 字 target / 100 字 overlap）→ 按任务意图的检索/上下文规划（`ContextPlannerService`，`ask` 走 retrieval、`summary/outline` 走 coverage）
- 对长文档 `ask` 任务，4 个样本平均节省 **86.6%**，峰值 **93.1%** —— 比如 Attention 论文从 10,263 tokens 压到 704 tokens（6.9%）；这也是端侧/云端协同的量化收益（端侧只把必要片段上云）
- 短文档场景诚实标注为 `-4%` 左右（单 chunk 加页码/标题 marker 略增），不是所有场景都该压、也不假装都压得动
- baseline 取"解析后全文塞 prompt" vs 实际走 planner 后的 `document_text`，token 数用 tiktoken `cl100k_base` 做统一尺子；无问芯穹底层 Qwen/DeepSeek BPE 会有 ±10% 偏差，但相对节省比稳健
- 报告里 1 个走 `no_match` 拒答路径的样本**明确不计入节省统计**，按 `feedback_eval_honesty` 纪律处理

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
