# 国一答辩硬证据摘要

## 核心差异点

研答通是一个引用可核验的文档问答系统，三个维度的差异：

1. **不是生成后补页码，而是检索-引用-回链的硬链路**：每个回答都先检索、再作答、返回结构化 citation，可以跳转回 PDF 原页证据
2. **不是小样本演示，而是 51 题真实评测**：覆盖中英论文与中文短文档；旧版 46/51 暴露边界，rollback 模型 `qwen3-235b` 经定向检索修复闭环到 51/51（引用页码命中率与拒答精确率均 100%），当前默认 `deepseek-v4-flash` 在同集 48/51（94.1%）、在更难的 V6 holdout 上 71/72
3. **不是口头声称，而是平台 request_id 可对账**：每次调用都有 `data/logs/call_logs.jsonl` 留痕，含无问芯穹平台返回的 `platform_request_id`，可在 infini-ai 控制台逐条对账（本地 request_id 仅作内部追踪）

## 一句话结论

研答通当前最强、最可核验的能力，不是泛化生成，而是已经在无问芯穹真实运行环境里完成多轮留痕验证的：

`upload -> ask -> citation -> PDF -> refusal`

## 锁定输入

- 文档：
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
- 锁定问题：
  1. `这篇论文主要研究了什么问题？`
  2. `作者最终的方法排名和总体准确率分别是多少？`
  3. `木星有几颗卫星？`

## 最重要的证据

### 1. 真实平台主路径已经切到无问芯穹

- 当前平台：`Wuwen Xinqiong`
- 当前默认 QA 模型：`deepseek-v4-flash`
- rollback fallback：`qwen3-235b-a22b-instruct-2507`
- 切换依据：`evidence/reports/holdout_eval_v6_contract_patch_qwen_vs_flash_20260430.md`（contract-patch holdout `71 / 72` vs `56 / 72`，并通过 predeploy sanity `3 / 3` 与 `11 / 11` 门控 READY）
- `summary` / `outline` 任务仍由 `qwen3-235b-a22b-instruct-2507` 承担，未单独重测前不切换

### 2. 锁定题组已经完成双模型 `3 / 3` 验证

来源：`evidence/reports/gold_sample_qa_compare_latest.md`

| 模型 | Passed / Total | Avg Latency (ms) |
| --- | --- | ---: |
| `qwen3-235b-a22b-instruct-2507` | `3 / 3` | `4896` |
| `qwen3-32b` | `3 / 3` | `4396` |

### 3. 当前默认模型的真实 replay 已跑通 `2 answered + 1 refused`

来源：`evidence/reports/gold_sample_replay_real_summary_latest.md`

- `answered`：`2`
- `refused`：`1`
- `errors`：`0`
- 平均延迟：`5386 ms`

### 4. 数值题 fresh rerun 已稳定回到 declared evidence

来源：`evidence/experiments/20260419_q2_declared_stability_check.md`

- `3 / 3` fresh real runs
- 每次都返回：
  - `evidence_mode=declared`
  - `used_chunk_count=2`
  - `evidence_quote_count=2`
  - `citation_count=2`

### 5. 严格版 G3 已完成六轮 fresh-upload 连续通过

来源：
- `evidence/experiments/20260420_g3_strict_rehearsal.md` (首批 3 轮)
- `evidence/experiments/20260423_g3_continuation.md` (续 3 轮)

- `6 / 6` authoritative runs passed
- 六轮都使用新的 `file_id`，不再复用已加载文档状态
- 所有 answerable 都保持 `evidence_mode=declared`
- 所有 refusal 都走 `retrieval_gate` 或 `llm_refused` 路径
- log-backed spans：
  - 首批 3 轮：`13.5s`, `12.9s`, `15.8s`
  - 续 3 轮：`8.0s`, `31.3s`, `63.5s`
- fallback：`0 / 6`

当前结论：
- 当前最强 `G3` 证据已累计 6 轮 strict fresh-upload batch，可作为更强的 judged-demo reproducibility evidence

## 当前 judge-facing 截图

> 当前界面版本（免登录试用 + 多档缩放 PDF 预览 + 答案对照锚点）于 2026-05-29 重拍，旧版 `20260419_*` 为历史界面，已被取代。

1. `20260529_gold_ask_research_focus.png`
2. `20260529_gold_pdf_render.png`
3. `20260529_gold_ask_rank_accuracy.png`
4. `20260529_gold_refusal.png`

## 当前模型决策

当前现场默认 QA：`deepseek-v4-flash`
- V6 extreme holdout `71/72`、拒答精确率 `100%`、引用准确率 `98.3%`
- 决赛交 MaaS 调用记录时 model 字段=`deepseek-v4-flash`，与本文件第 7 节口径一致

rollback fallback：`qwen3-235b-a22b-instruct-2507`
- 在 51 题固定集回归为 `51/51`，作为更慢但更稳的回退路径，不是现场默认
- 历史 fallback `qwen3-32b` 已验证通过同一锁定题组，仅作更早期备用，不进入主叙事

## 当前诚实边界

### 6. 量化评测指标（strict G3 六轮 fresh-upload）

来源：`evidence/reports/quantitative_eval_metrics.md`

| 指标 | 值 |
| --- | --- |
| 证据声明率 | `100%` |
| 引用页码准确率 | `100%` |
| 检索页码覆盖率 | `100%` |
| 证据引文提取率 | `100%` |
| 检索利用率 | `38%` |
| 拒答精确率 | `100%` |
| 跨轮一致性 | `100%` |
| 平均 answerable 延迟 | `5521 ms` |

检索利用率 `38%` 说明模型从 `4` 个候选片段中选择性引用了 `1-2` 个最相关片段，而非全盘接受检索结果。

### 7. 扩展评测 V1（`51` 题 full，真实 API 端到端）

来源：`evidence/reports/extended_eval_v1_latest.md` · canonical final report `evidence/reports/extended_eval_v1_qwen3_235b_a22b_instruct_2507_retrieval_patch.md` · 脚本 `scripts/extended_eval.py` · 范围 `evidence/materials/EXTENDED_EVAL_SCOPE.md`

样本从最初的 `3` 题 gold-sample → `20` 题 seed → 扩到 **`51` 题 full**（中英论文 + 中文短文档 × A1-A5 答题 + B1-B2 拒答），在同一条真实 API 主链路上端到端跑完。旧版 `46/51` 用于暴露 retrieval 边界；**rollback 模型 `qwen3-235b-a22b-instruct-2507`** 在 2026-04-24 定向检索/上下文 patch 后闭环为 `51/51`。

> 口径对齐（重要）：下表 `51/51` 是 **rollback 模型 `qwen3-235b`** 的固定集回归。**当前现场默认 QA 模型是 `deepseek-v4-flash`**：它在同一 51 题集为 `48/51`（94.1%、拒答精确率 100%、声明率 100%），并在更难的 V6 extreme holdout 上达 `71/72`、拒答精确率 100%、引用准确率 98.3%（见 `holdout_eval_v6_contract_patch_qwen_vs_flash_20260430.md`、`evidence/reports/extended_eval_v1_deepseek_v4_flash_20260429.md`）。决赛交 MaaS 调用记录时 model 字段=`deepseek-v4-flash`，与此口径一致；不要把 rollback 的 51/51 说成默认模型成绩。

| 指标（rollback `qwen3-235b`，51 题固定集） | 值 |
| --- | --- |
| 总通过率 | `100.0%` (`51/51`) |
| 答题通过率 | `100.0%` (`43/43`) |
| **拒答精确率** | **`100%`** (`8/8`) |
| 引用页码准确率 (page-hit) | `100.0%` |
| 证据声明率 (evidence_mode=declared on answerable) | `100.0%` |
| 平均延迟 | `5697 ms`（含 evidence-retry 的端到端口径） |

按文档分层：中文论文、Transformer 论文、研究报告、项目简介四类样本在 rollback 模型回归中均通过；当前默认 `deepseek-v4-flash` 的 3 个未过题集中在表格尾列/隐含结论类难例，属已知 retrieval 颗粒度边界。

**三次定位 + 三次修复**：

1. 初跑 `20` 题时 `refusal precision = 0%`，`3` 道拒答题全部被硬答。定位到 `ask` prompt 原写法强制 `evidence_quotes` 非空、配合 retry loop 二次施压，主动诱导 LLM 在无依据时编造证据。已在 prompt 层加 `refused=true` 出口 + `TaskService` 接入 `llm_refused` 分支修复（commit `7f2713d`）。其中 `en_b2_vaswani_affiliation_now`（"Vaswani 在 2026 年的雇主"——关键词在文档但答案不在）这种 retrieval 层拦不住的诱导拒答，也被 LLM 层正确拒答。
2. 修复 prompt 后 `20` 题通过率 `85%`，`3` 道答题失败集中在论文首页元信息（作者、单位、主要贡献）。定位到 BM25+IDF 召回对元信息类 query 不稳——首页 chunk 权重不够。在 `RetrievalService` 加 metadata-intent 检测 + pin 首 chunk 的 fallback，零改动现有 answerable / refusal 行为。修复后 `20` 题通过率回到 `95%`。
3. 扩到 `51` 题后旧版通过率为 `46/51`，暴露出表格尾列、参数单元格、abstract 隐含贡献和小 markdown 文档元信息等真实边界。
4. 2026-04-24 没有更换默认模型，而是做了针对 retrieval/context 的工程修复：表格/参数 query expansion、neighbor chunks、contribution/head chunks、matched-retrieval self-refusal 的一次严格 retry。最终默认模型回归闭环为 `51/51`。

**诚实边界**：`51/51` 是固定扩展评测集上的最终回归结果，不等于任意文档/任意问题开放域 `100%`。系统核心承诺是：模型声明使用的片段可回链到页码/原文片段；当模型提供逐字 quote 时，后端会做原文子串校验。不要把它表述成“每个回答都有逐字 quote”。

### 8. Token 压缩定量评估（对应加分项 #4）

来源：`evidence/reports/token_compression_eval.md` · 脚本 `scripts/eval_token_compression.py` · 机读 `evidence/reports/token_compression_eval.json`

**对应赛题原文**（PDF 第 117-118 页）：
> Token 消耗量（5 分）：…… 或有 **Token 消耗压缩技术**（将原始的大量 Token 消耗进行削减）等。

流水线三层压缩：`DocumentParser` → `ChunkService` → `ContextPlannerService`。其中第 3 层按任务意图走 retrieval（ask）或 coverage（summary/outline），是核心节省环节。

**结论（按场景分层）**：

| 场景 | 样本数 | 平均节省 | 峰值 |
| --- | ---: | ---: | ---: |
| **长文档（PDF 论文）ask** | 4 | **86.6%** | **93.1%** |
| **长文档 summary / outline** | 4 | **83.2%** | 89.4% |
| **短文档（MD / TXT）所有任务** | 23 | -4.2% | — |

- 长文档 2 篇合计 8 个任务平均节省 **84.9%**；峰值出现在 Attention 论文的 `ask What are the experimental results?` — 10,263 → 704 tokens，**压到原文的 6.9%**
- 短文档 token 本来就少，context_planner 加页码/标题 marker 后略增（-3% 左右）；**诚实标注短文档不是压缩目标场景**
- 1 个任务样本走 `no_match` 拒答路径，不计入节省统计（遵循 `feedback_eval_honesty` 纪律）
- 数字以当前代码 `python scripts/eval_token_compression.py` 现场可复跑为准（`tiktoken` 已入 `requirements.txt`）；2026-05-29 复跑后长文 ask 由 89.1%→86.6%（近期 overview 检索改为多 pin 一段 head-context，更稳健但略增 token），峰值 93.1% 不变

**答辩口径**：对**长文档 ask 任务**（论文速读 / 报告问答的主场景），研答通把 input token 从万级压到千级，**平均节省约 87%**，峰值 93%。这同时是**端侧/云端协同**的量化收益——端侧/近端只把必要片段上云推理。

#### 8.1 受控对照：检索接地 vs 直接喂全文（对应技术能力「可量化显著提升 + 可复现」p.264）

来源：`evidence/reports/baseline_compare_eval.md` · 脚本 `scripts/baseline_compare_eval.py`（`--report-only` 可从机读 JSON 重建）· 机读 `evidence/reports/baseline_compare_eval.json`

把上面的「节省」做成**同条件受控对照**：同一批 22 道长 PDF 可回答题、同一套 ask 契约与判分，唯一变量是喂给模型的内容——RAG 只喂检索片段，基线喂**带页码标记的全文**（给全文路线最公平的 grounding 机会）。44 次真实 MaaS 调用，每次都记录真实平台 `platform_request_id` 可在控制台对账。

| 指标 | RAG（检索片段） | Full-Context（全文） |
| --- | ---: | ---: |
| 正确率（expected_any_of 命中） | **100%** (22/22) | 100% (22/22) |
| 平均 input tokens（真实平台计数） | **2,240** | 9,778 |
| 合计 input tokens | 49,273 | 215,113 |

**诚实口径（关键）**：这不是「RAG 更准」——两边都答对——而是**同等准确度下 input token 降到 1/4.37（约节省 77%）**。且全文条件有 **11/22** 例因超 `MAX_DOCUMENT_CHARS=30000` 被截断，意味着全文路线在更长文档上会**喂不全、掉准确率**，而检索接地不随文档变长而劣化；故 4.37× 是**保守下限**。最后，只有 RAG 携带 chunk/页码锚点支撑 bbox 级回链与离题拒答，全文喂入丢失页结构、给不出可核验出处——这正是产品立身点。

### 9. 单层 Agentic 检索循环（对应加分项 #3 大模型与智能体能力）

来源：`backend/app/services/task_service.py::_run_agentic_ask` · 测试 `backend/tests/test_services.py::test_agentic_ask_reretrieves_with_followup_query`

`ask` 主链路不是单轮 RAG，而是一个**受控 agentic 循环**：

1. 检索 → 把命中片段交模型作答；
2. **模型自评证据是否充分**：若不足，模型在同一次结构化输出里给出 `need_more=true` 与 `followup_query`（一个更聚焦的补充检索查询词）；
3. 系统用 `followup_query` **补检索新片段**（排除已展示过的 chunk），把新证据并入上下文**再问一次**；
4. **有界二次重试**（`iter≤2`）：`agent_iterations` 落 `call_logs.jsonl`，真实日志中约 1/4 的 `ask` 触发了二轮自评。

边界与安全：这是大模型 + agent 技术的有效组合（证据自评 + 有界重试 + 收敛，self-RAG 雏形），但**完全不改变拒答与证据回链契约**——干净拒答仍拒答，逐字 quote 仍做原文子串校验，模型不索要补充时退化为单轮。改写补检索分支已实现且单测覆盖：`test_agentic_ask_reretrieves_with_followup_query` 证明首轮证据不足时系统用 `followup_query` 检索到**全新片段**并据其再答；`test_validated_quotes_drop_fabricated_text` 证明伪造 quote 被丢弃。

> **诚实口径（主动说）**：在固定 demo 集上，模型多为**单轮收敛**，触发的二轮也多为**同上下文证据复核**而非改写补检索，故生产日志 `query_rewrites` 多为空。我们把它定位为"**有界自评重试**（机制已实现+单测覆盖）"，**不**宣称"现场可逐条核验 query 改写"，避免把空字段当卖点。

**答辩口径**：`ask` 主链路是受控 agentic RAG——检索后模型自评证据，不足则有界重试(≤2 轮)，全程不破坏拒答与证据回链；`agent_iterations` 有日志可查。诚实说：改写补检索分支已实现+单测覆盖，但固定集上多单轮收敛，`query_rewrites` 多为空，我们不夸成"现场可核验改写"。

## 当前诚实边界

1. 当前最强证据是锁定 gold-sample judged-demo path，不是开放域产品泛化证明。
2. 当前 `G3` 最强记录是 strict six-run batch；它证明 judged-demo path 可复现，但仍不是开放域泛化证明。
3. `ask` 是主卖点；`summary / outline` 已支持，但 grounding 语义弱于 `ask`。

## judge-facing 推荐说法

“我们不是先生成再补页码，而是把答案回到 PDF 原文证据做成了一条硬链路。这条链路已经在无问芯穹真实运行环境里完成双模型验证、fresh rerun 记录和严格版 G3 六连跑记录。”
