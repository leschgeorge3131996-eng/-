# 无问芯穹平台使用证据页

## 目的

把“研答通”对无问芯穹平台的使用方式、真实运行证据和 judge-facing 索引收成一页主证明，供：

- `3` 页 PPT
- 产品及技术文档
- 决赛日志包
- 答辩时的平台使用说明

## 当前平台路径

| 项目 | 当前值 |
| --- | --- |
| 平台 | `Wuwen Xinqiong` |
| Base URL | `https://cloud.infini-ai.com/maas/v1` |
| 当前默认 QA 模型 | `qwen3-235b-a22b-instruct-2507` |
| 当前 judged-demo 主链路 | `upload -> ask -> citation -> PDF -> refusal` |

说明：

- 真正的 API Key 仅保存在本地 `.env`，不进入仓库。
- judge-facing 材料只展示平台使用结果、模型名、request id 和证据截图，不展示密钥。

## 主证明

### 1. 平台已接入真实主链路

- 当前仓库运行配置已经切到 `Wuwen Xinqiong`
- 当前主 QA 路径使用 `qwen3-235b-a22b-instruct-2507`

主证明来源：

- `evidence/reports/gold_sample_replay_real_summary_latest.md`
- `evidence/reports/gold_sample_qa_compare_latest.md`

### 2. 锁定 gold-sample 在真实平台上已完成双模型验证

`evidence/reports/gold_sample_qa_compare_latest.md` 当前结论：

| 模型 | 通过情况 | 平均延迟 |
| --- | --- | ---: |
| `qwen3-235b-a22b-instruct-2507` | `3 / 3` | `4896 ms` |
| `qwen3-32b` | `3 / 3` | `4396 ms` |

同一锁定题组包含：

1. 文档内问题：`这篇论文主要研究了什么问题？`
2. 文档内数值问题：`作者最终的方法排名和总体准确率分别是多少？`
3. 离题拒答：`木星有几颗卫星？`

### 3. 当前主模型在真实 replay 中已跑通完整主链路

`evidence/reports/gold_sample_replay_real_summary_latest.md` 当前结论：

- 总记录数：`3`
- `ask`：`3`
- `answered`：`2`
- `refused`：`1`
- `errors`：`0`
- 平均延迟：`5386 ms`

这组结果对应的正是当前 judge-facing 主链路：

- `ask`
- `citation`
- `PDF render`
- `refusal`

### 4. 最危险的数值题已经做过 fresh real rerun

`evidence/experiments/20260419_q2_declared_stability_check.md` 当前结论：

- `3 / 3` fresh real runs
- 全部返回：
  - `evidence_mode=declared`
  - `used_chunk_count=2`
  - `evidence_quote_count=2`
  - `citation_count=2`

结论：

- 当前最容易被质疑的数值题，不只是“答对了”，还在 fresh real rerun 下稳定回到了 declared evidence。

### 5. 当前 judged-demo 已完成三次连续 rehearsal

`evidence/experiments/20260419_g3_rehearsal_template.md` 当前结论：

- `3` 次连续通过
- 每次都完成：
  - answerable 1
  - answerable 2
  - PDF jump
  - refusal
- 计时分别为：
  - `56s`
  - `67s`
  - `24s`

## 答辩备用附录

### 备用模型

- 当前已验证的备用 QA 模型：`qwen3-32b`
- 用途：当部署环境延迟明显变紧时，作为同题组、同平台下的备用路径

### 当前 `G3` 口径

- 当前 `G3` 是 warm-state operator rehearsal pass
- 不是更严格的 cold-start / second-machine pass

### request id 索引

#### Q2 declared fresh rerun

| 用途 | Request ID |
| --- | --- |
| Q2 fresh run 1 | `785bf35b11e5418f942a7e08d5b33351` |
| Q2 fresh run 2 | `1e38cbd263424988a1880bb286a20fcf` |
| Q2 fresh run 3 | `9df441cc64bc487aa90a59fc66275602` |

#### G3 judged-demo rehearsal

| Run | 问题 | Request ID |
| --- | --- | --- |
| `1` | answerable 1 | `692bda1f05684649a9585d72e8e3901e` |
| `1` | answerable 2 | `b552670d1e424225a2af7b36de0091dd` |
| `1` | refusal | `befcb8116ccf42a198f4f3ac6c1fc282` |
| `2` | answerable 1 | `8d41e5339676485194a8b17dd9fea760` |
| `2` | answerable 2 | `f006c65103c94eb881aad9d4c40cdc80` |
| `2` | refusal | `f4375cb1829f49e7b52b21c52603cff4` |
| `3` | answerable 1 | `83e7f541e8204324b19d42d809152942` |
| `3` | answerable 2 | `a4de68c753454a33b68388f99f0c9855` |
| `3` | refusal | `2768299a88054e8aa13427d91356a0be` |

附录说明：

- 这些 request id 都能在 `data/logs/call_logs.jsonl` 和对应实验文档中互相对上。
- refusal 使用的是 `retrieval_gate`，用于证明“问题与文档无关时不再调用模型硬答”。

## judge-facing 截图索引

主截图：

1. `evidence/screenshots/20260419_gold_ask_research_focus.png`
2. `evidence/screenshots/20260419_gold_pdf_render.png`
3. `evidence/screenshots/20260419_gold_ask_rank_accuracy.png`
4. `evidence/screenshots/20260419_gold_refusal.png`

附录截图：

1. `evidence/screenshots/20260419_stats_panel.png`
2. `evidence/screenshots/20260419_api_docs.png`

## 如何在答辩中使用这一页

推荐口径：

1. 我们不是只在 PPT 里说“接了平台”，而是已经把无问芯穹接进真实主链路。
2. 当前锁定题组在真实平台上完成了双模型 `3 / 3` 验证。
3. 当前默认模型、fresh rerun request id 和答辩备用索引都能追溯。
4. 所有 judge-facing 截图都来自同一条真实运行路径。

## 不建议直接拿来当主证明的材料

以下材料只适合作为开发遥测或附录，不建议直接当成 judge-facing 主证明：

- `evidence/reports/latest_log_summary.md`
  - 原因：混有历史开发期数据，不是 current real-only gold path 结论
- `stats panel`
  - 原因：容易暴露历史噪声和非 judge-facing 指标
- `api docs`
  - 原因：证明工程存在即可，不应抢主叙事
