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

## 主证据

### 1. 平台已经接入真实主链路

- 当前仓库运行配置已经切到 `Wuwen Xinqiong`
- 当前主 QA 路径使用 `qwen3-235b-a22b-instruct-2507`

主证明来源：

- `evidence/reports/gold_sample_replay_real_summary_latest.md`
- `evidence/reports/gold_sample_qa_compare_latest.md`

### 2. 锁定 gold-sample 已完成双模型验证

`evidence/reports/gold_sample_qa_compare_latest.md` 当前结论：

| 模型 | 通过情况 | 平均延迟 |
| --- | --- | ---: |
| `qwen3-235b-a22b-instruct-2507` | `3 / 3` | `4896 ms` |
| `qwen3-32b` | `3 / 3` | `4396 ms` |

同一锁定题组包括：
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
- 当前最容易被质疑的数值题，不只“答对了”，还在 fresh real rerun 下稳定回到了 declared evidence。

### 5. 当前 strict G3 已完成三次连续通过

`evidence/experiments/20260420_g3_strict_rehearsal.md` 当前结论：

- `3` 次连续通过
- 三轮都是 fresh-upload run，`file_id` 各不相同
- 每轮两次 answerable 都保持 `declared`
- 每轮 refusal 都保持 `retrieval_no_match`
- log-backed spans 分别为：
  - `13.5s`
  - `12.9s`
  - `15.8s`
- fallback：`0 / 3`

## 答辩备用附录

### 备用模型

- 当前已验证的备用 QA 模型：`qwen3-32b`
- 用途：当部署环境延迟明显变紧时，作为同题组、同平台下的备用路径

### 当前 `G3` 口径

- 当前最强 `G3` 记录是按 `STRICT_G3_EXECUTION_PLAN.md` 留痕的 strict `3`-run batch
- 它比 earlier warm-state self-rehearsal 更强，但仍只证明锁定 gold path 的 judged-demo reproducibility
- `20260419_g3_rehearsal_template.md` 现在保留为早期 warm-state 附录，不再作为当前最强口径

### request id 索引

#### Q2 declared fresh rerun

| 用途 | Request ID |
| --- | --- |
| Q2 fresh run 1 | `785bf35b11e5418f942a7e08d5b33351` |
| Q2 fresh run 2 | `1e38cbd263424988a1880bb286a20fcf` |
| Q2 fresh run 3 | `9df441cc64bc487aa90a59fc66275602` |

#### Strict G3 authoritative batch

| Run | 问题 | Request ID |
| --- | --- | --- |
| `1` | answerable 1 | `1f959e23693e4e32acf49b460009ccd7` |
| `1` | answerable 2 | `9bcd0f09b2bd407192ac8461c3a7423c` |
| `1` | refusal | `d44bfdfa4cdf4aec9adc90322ec942c4` |
| `2` | answerable 1 | `77cb7a1a6865446fa66df8d2f01dfc0c` |
| `2` | answerable 2 | `808e42258ae545f9a1f0f2a33ef44549` |
| `2` | refusal | `04220964210d408596541371a6685ff1` |
| `3` | answerable 1 | `5363a0edc7074ef082148f84d6bda839` |
| `3` | answerable 2 | `605fd2f0feae45c193379aba6a02723a` |
| `3` | refusal | `8ec726ccfb5c413ba62bb5e6599373d6` |

附录说明：
- 这些 request id 都能在 `data/logs/call_logs.jsonl` 和 `20260420_g3_strict_rehearsal.md` 中互相对上。
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
3. 当前默认模型、fresh rerun request id 和 strict G3 request id 都能追溯。
4. 所有 judge-facing 截图都来自同一条真实运行路径。

## 不建议直接拿来当主证明的材料

以下材料只适合作为开发遥测或附录，不建议直接当成 judge-facing 主证明：

- `evidence/reports/latest_log_summary.md`
  - 原因：混有历史开发期数据，不是 current real-only gold path 结论
- `stats panel`
  - 原因：容易暴露历史噪声和非 judge-facing 指标
- `api docs`
  - 原因：证明工程存在即可，不应抢主叙事
