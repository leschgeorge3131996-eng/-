# 国一答辩硬证据摘要

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

## 最重要的五条证据

### 1. 真实平台主路径已经切到无问芯穹

- 当前平台：`Wuwen Xinqiong`
- 当前默认 QA 模型：`qwen3-235b-a22b-instruct-2507`

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

### 5. 严格版 G3 已完成三轮 fresh-upload 连续通过

来源：`evidence/experiments/20260420_g3_strict_rehearsal.md`

- `3 / 3` authoritative runs passed
- 三轮都使用新的 `file_id`，不再复用已加载文档状态
- 两次 answerable 都保持 `evidence_mode=declared`
- refusal 都保持 `retrieval_status=no_match`
- log-backed spans：
  - `13.5s`
  - `12.9s`
  - `15.8s`
- fallback：`0 / 3`

当前结论：
- 当前最强 `G3` 证据已经从 earlier warm-state self-rehearsal 升级为 strict three-run batch，可作为更强的 judged-demo reproducibility evidence

## 当前 judge-facing 截图

1. `20260419_gold_ask_research_focus.png`
2. `20260419_gold_pdf_render.png`
3. `20260419_gold_ask_rank_accuracy.png`
4. `20260419_gold_refusal.png`

## 当前模型决策

为什么默认保留 `235b`：
- 当前 lock 的 gold path 下，两模型都通过
- `235b` 仍是当前主演示链路默认选择

答辩备用：
- `32b` 已验证通过同一锁定题组
- 仅在部署环境明显更紧时作为备用路径使用，不进入主标题叙事

## 当前诚实边界

### 6. 量化评测指标（strict G3 三轮 fresh-upload）

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

## 当前诚实边界

1. 当前最强证据是锁定 gold-sample judged-demo path，不是开放域产品泛化证明。
2. 当前 `G3` 最强记录是 strict three-run batch；它证明 judged-demo path 可复现，但仍不是开放域泛化证明。
3. `ask` 是主卖点；`summary / outline` 已支持，但 grounding 语义弱于 `ask`。

## judge-facing 推荐说法

“我们不是先生成再补页码，而是把答案回到 PDF 原文证据做成了一条硬链路。这条链路已经在无问芯穹真实运行环境里完成双模型验证、fresh rerun 记录和严格版 G3 三连跑记录。”
