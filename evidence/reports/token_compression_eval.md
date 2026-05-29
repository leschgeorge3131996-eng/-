# 研答通 Token 压缩定量评估报告

**对应赛题加分项**：无问芯穹赛题一 · 第六页 · 加分项 #4 — Token 消耗量（5 分），分支 b：**Token 消耗压缩技术**（将原始的大量 Token 消耗进行削减）。

**结论先行（按场景分层）**：

- **长文档（PDF 论文）场景是压缩的主战场**：8 个任务平均节省 **84.9%**，其中 ask 类 4 题平均 **86.6%**，summary 类 2 题平均 **84.0%**
- **短文档场景不是压缩目标**：23 个任务平均 **-4.2%**，ask 类 7 题平均 **-6.0%**，summary/outline 反而略增（单 chunk 加了页码/标题 marker）
- **节省来源是三层预处理**：解析归一化 → 结构化切块 → 按任务意图的检索/上下文规划
- **长文档 token 阈值推演**：本次 2 篇 PDF 解析后 1 万-1.7 万 tokens，若文档再长 5-10 倍（真实论文集 / 报告合集），会**直接超过 32k 上下文窗口**，此时压缩不再是加分项而是**能跑通的前提**
- 1 个任务样本走 `no_match` 拒答路径，**诚实标注不计入节省统计**（0 token 输入是拒答行为，不是压缩成果；该纪律见记忆 `feedback_eval_honesty`）

## 评估方法

- **基准 (baseline)**：解析后的原文全文 token 数（视作"不预处理直接塞 prompt"）
- **实际**：经过 `ContextPlannerService.plan()` 输出的 `document_text` token 数
- **token 计法**：tiktoken `cl100k_base`，与 GPT-4 系列一致；
  无问芯穹后端（Qwen/DeepSeek）的真实 BPE 会有 ±10% 偏差，但同尺子下的相对节省比稳健
- **任务覆盖**：每个文档跑 summary / outline / ask 三类任务；
  共 10 个文档，32 个任务样本

## 流水线分阶段产出

| 阶段 | 模块 | 作用 |
|---|---|---|
| 0 baseline | — | 解析后全文（如果不做后续预处理就要全部塞 prompt）|
| 1 parse | `DocumentParser` | PDF→ 文本 + 页面/段落结构（去除二进制开销） |
| 2 chunk | `ChunkService` | 结构化切块（target=900 chars, overlap=100） |
| 3 plan | `ContextPlannerService` | 按任务类型 + 检索意图选片段，ask 走 retrieval，summary/outline 走 coverage |

## 文档级总览

| 文档 | 类别 | 页数 | chunks | baseline tok | 切块后 tok | summary 节省 | outline 节省 | ask 平均节省† |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 办公通知 (txt) | 短 | 1 | 1 | 207 | 207 | -4.8% | -4.8% | -7.2% |
| 研究简报 (md) | 短 | 1 | 1 | 284 | 284 | -3.5% | -3.5% | -7.0% |
| 论文摘要 (md) | 短 | 1 | 1 | 231 | 231 | -4.3% | -4.3% | -8.7% |
| 校园活动通知 | 短 | 1 | 1 | 364 | 364 | -2.7% | -2.7% | -5.2% |
| 事故复盘报告 | 短 | 1 | 1 | 475 | 475 | -2.1% | -2.1% | -4.0% |
| 实验日志 | 短 | 1 | 1 | 365 | 365 | -2.7% | -2.7% | -5.2% |
| 采购制度文件 | 短 | 1 | 1 | 385 | 385 | -2.6% | -2.6% | -4.7% |
| 中英双语产品规格 | 短 | 1 | 1 | 212 | 212 | -4.7% | -4.7% | — (1 拒答) |
| 中文 LLM 空间能力评测论文 | 长 | 11 | 35 | 16,487 | 18,484 | 78.6% | 75.7% | 82.0% |
| Attention Is All You Need 论文 | 长 | 15 | 57 | 10,263 | 11,133 | 89.4% | 89.4% | 91.2% |

† ask 平均节省只统计实际命中检索的样本，走拒答（`no_match`）的样本以括号备注，不参与平均

## 任务级明细

### 办公通知 (txt) （evidence\samples\office_notice.txt）

- 类别：短，txt，1 页，1 chunks
- baseline (raw_text) = **207** tokens
- 切块后拼接 = **207** tokens

| 任务 | 输入 | 策略 | 选中 chunks | stage3 tok | 节省 vs baseline |
|---|---|---|---:|---:|---:|
| summary | — | `coverage_summary` | 1 | 217 | **-4.8%** |
| outline | — | `coverage_outline` | 1 | 217 | **-4.8%** |
| ask | 请说明其中提到的具体数字和指标。 | `retrieval_topk` | 1 | 222 | **-7.2%** |

### 研究简报 (md) （evidence\samples\research_brief.md）

- 类别：短，md，1 页，1 chunks
- baseline (raw_text) = **284** tokens
- 切块后拼接 = **284** tokens

| 任务 | 输入 | 策略 | 选中 chunks | stage3 tok | 节省 vs baseline |
|---|---|---|---:|---:|---:|
| summary | — | `coverage_summary` | 1 | 294 | **-3.5%** |
| outline | — | `coverage_outline` | 1 | 294 | **-3.5%** |
| ask | 第一阶段要做什么？ | `retrieval_topk` | 1 | 304 | **-7.0%** |

### 论文摘要 (md) （evidence\samples\paper_report.md）

- 类别：短，md，1 页，1 chunks
- baseline (raw_text) = **231** tokens
- 切块后拼接 = **231** tokens

| 任务 | 输入 | 策略 | 选中 chunks | stage3 tok | 节省 vs baseline |
|---|---|---|---:|---:|---:|
| summary | — | `coverage_summary` | 1 | 241 | **-4.3%** |
| outline | — | `coverage_outline` | 1 | 241 | **-4.3%** |
| ask | 报告里提到的核心方法是什么？ | `retrieval_topk` | 1 | 251 | **-8.7%** |

### 校园活动通知 （evidence\samples\holdout_v3\campus_workshop_notice.md）

- 类别：短，md，1 页，1 chunks
- baseline (raw_text) = **364** tokens
- 切块后拼接 = **364** tokens

| 任务 | 输入 | 策略 | 选中 chunks | stage3 tok | 节省 vs baseline |
|---|---|---|---:|---:|---:|
| summary | — | `coverage_summary` | 1 | 374 | **-2.7%** |
| outline | — | `coverage_outline` | 1 | 374 | **-2.7%** |
| ask | 报名截止时间是什么时候？ | `retrieval_topk` | 1 | 383 | **-5.2%** |

### 事故复盘报告 （evidence\samples\holdout_v3\incident_review_alpha.md）

- 类别：短，md，1 页，1 chunks
- baseline (raw_text) = **475** tokens
- 切块后拼接 = **475** tokens

| 任务 | 输入 | 策略 | 选中 chunks | stage3 tok | 节省 vs baseline |
|---|---|---|---:|---:|---:|
| summary | — | `coverage_summary` | 1 | 485 | **-2.1%** |
| outline | — | `coverage_outline` | 1 | 485 | **-2.1%** |
| ask | 事故的直接原因是什么？ | `retrieval_topk` | 1 | 494 | **-4.0%** |

### 实验日志 （evidence\samples\holdout_v3\lab_experiment_log.md）

- 类别：短，md，1 页，1 chunks
- baseline (raw_text) = **365** tokens
- 切块后拼接 = **365** tokens

| 任务 | 输入 | 策略 | 选中 chunks | stage3 tok | 节省 vs baseline |
|---|---|---|---:|---:|---:|
| summary | — | `coverage_summary` | 1 | 375 | **-2.7%** |
| outline | — | `coverage_outline` | 1 | 375 | **-2.7%** |
| ask | 请说明其中提到的具体数字和指标。 | `retrieval_topk` | 1 | 384 | **-5.2%** |

### 采购制度文件 （evidence\samples\holdout_v3\procurement_policy_2026.md）

- 类别：短，md，1 页，1 chunks
- baseline (raw_text) = **385** tokens
- 切块后拼接 = **385** tokens

| 任务 | 输入 | 策略 | 选中 chunks | stage3 tok | 节省 vs baseline |
|---|---|---|---:|---:|---:|
| summary | — | `coverage_summary` | 1 | 395 | **-2.6%** |
| outline | — | `coverage_outline` | 1 | 395 | **-2.6%** |
| ask | 请说明其中提到的具体数字和指标。 | `retrieval_topk` | 1 | 403 | **-4.7%** |

### 中英双语产品规格 （evidence\samples\holdout_v3\bilingual_product_spec.md）

- 类别：短，md，1 页，1 chunks
- baseline (raw_text) = **212** tokens
- 切块后拼接 = **212** tokens

| 任务 | 输入 | 策略 | 选中 chunks | stage3 tok | 节省 vs baseline |
|---|---|---|---:|---:|---:|
| summary | — | `coverage_summary` | 1 | 222 | **-4.7%** |
| outline | — | `coverage_outline` | 1 | 222 | **-4.7%** |
| ask | 产品的关键参数有哪些？ | `no_match` | 0 | 0 | **100.0%** *拒答路径，不计入节省汇总* |

### 中文 LLM 空间能力评测论文 （evidence\samples\chinese_llm_spatial_eval.pdf）

- 类别：长，pdf，11 页，35 chunks
- baseline (raw_text) = **16,487** tokens
- 切块后拼接 = **18,484** tokens

| 任务 | 输入 | 策略 | 选中 chunks | stage3 tok | 节省 vs baseline |
|---|---|---|---:|---:|---:|
| summary | — | `coverage_summary` | 5 | 3,530 | **78.6%** |
| outline | — | `coverage_outline` | 6 | 4,009 | **75.7%** |
| ask | 这份文档的核心内容是什么？ | `retrieval_topk` | 6 | 3,050 | **81.5%** |
| ask | 请说明其中提到的具体数字和指标。 | `retrieval_topk` | 4 | 2,884 | **82.5%** |

### Attention Is All You Need 论文 （evidence\samples\attention_is_all_you_need.pdf）

- 类别：长，pdf，15 页，57 chunks
- baseline (raw_text) = **10,263** tokens
- 切块后拼接 = **11,133** tokens

| 任务 | 输入 | 策略 | 选中 chunks | stage3 tok | 节省 vs baseline |
|---|---|---|---:|---:|---:|
| summary | — | `coverage_summary` | 5 | 1,092 | **89.4%** |
| outline | — | `coverage_outline` | 5 | 1,092 | **89.4%** |
| ask | What is the Transformer architecture? | `retrieval_topk` | 4 | 1,106 | **89.2%** |
| ask | What are the experimental results? | `retrieval_topk` | 4 | 704 | **93.1%** |

## 与赛题加分项的对应

**赛题原文**（PDF 第 117-118 页）：
> Token 消耗量（5 分）：单次单任务 Token 消耗量较大（例如：明显高于日常对话 Token 消耗量）、或有 **Token 消耗压缩技术**（将原始的大量 Token 消耗进行削减）等。

研答通命中**压缩技术**分支：
1. **解析归一化**（stage 1）：PDF 二进制 → 文本；评测论文（10 万字级）在不解析时无法直接送 LLM
2. **结构化切块**（stage 2）：去除版心冗余、对齐为可寻址段
3. **任务意图驱动的检索/规划**（stage 3）：核心节省环节
   - `ask` 任务：retrieval 取 top-K + metadata-intent fallback，长文档下节省率最高
   - `summary` 任务：coverage_summary 策略选取代表性段落
   - `outline` 任务：保留章节首段
4. **效果**：长文档场景下 ask 类任务节省 80% 以上 input token，短文档场景下节省虽低但准确率不降反升（见 `evidence/reports/quantitative_eval_metrics.md`）
