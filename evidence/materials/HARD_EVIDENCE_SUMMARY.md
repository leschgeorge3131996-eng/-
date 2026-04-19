# 国一答辩硬证据摘要

## 一句话结论

研答通当前最强、最可信的能力，不是“泛化生成”，而是已经在无问芯穹真实运行环境里反复验证过的：

`upload -> ask -> citation -> PDF -> refusal`

## 锁定输入

- 文档：
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
- 锁定问题：
  1. `这篇论文主要研究了什么问题？`
  2. `作者最终的方法排名和总体准确率分别是多少？`
  3. `木星有几颗卫星？`

## 最重要的五条证据

### 1. 真实平台路径已经切到无问芯穹

- 当前平台：`Wuwen Xinqiong`
- 当前默认 QA 模型：`qwen3-235b-a22b-instruct-2507`

### 2. 双模型在锁定题组三题全部通过

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

### 4. 数值题 fresh rerun 的当前记录均回到 declared evidence

来源：`evidence/experiments/20260419_q2_declared_stability_check.md`

- `3 / 3` fresh real runs
- 每次都返回：
  - `evidence_mode=declared`
  - `used_chunk_count=2`
  - `evidence_quote_count=2`
  - `citation_count=2`

### 5. 当前 judged-demo 已完成三次连续 rehearsal

来源：`evidence/experiments/20260419_g3_rehearsal_template.md`

- Run 1：`56s`
- Run 2：`67s`
- Run 3：`24s`

当前结论：

- 已有 `3` 次 warm-state self-rehearsal 记录，可作为 judged-demo 预演证据

## 当前 judge-facing 截图

1. `20260419_gold_ask_research_focus.png`
2. `20260419_gold_pdf_render.png`
3. `20260419_gold_ask_rank_accuracy.png`
4. `20260419_gold_refusal.png`

## 当前模型决策

为什么默认保留 `235b`：

- 当前 lock 的 gold path 下，两模型都过
- `235b` 仍是当前主演示链默认选择

答辩备用：

- `32b` 已验证通过同一锁定题组
- 仅在部署环境更紧时作为备用路径使用，不进入主标题叙事

## 当前诚实边界

1. 当前最强证据是锁定 gold-sample judged-demo path，不是开放域产品泛化证明。
2. 当前 `G3` 是 warm-state operator rehearsal pass，不是更严格的 cold-start second-machine pass。
3. `ask` 是主卖点；`summary / outline` 已支持，但 grounding 语义弱于 `ask`。

## judge-facing 推荐说法

“我们不是先生成再补页码，而是把答案回到 PDF 原文证据做成了一条硬链路。这条链路已经在无问芯穹真实运行环境里完成双模型验证、fresh rerun 记录和连续 rehearsal 记录。”
