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
| 当前默认 QA 模型 | `deepseek-v4-flash` |
| rollback QA fallback | `qwen3-235b-a22b-instruct-2507` |
| `summary` / `outline` 模型 | `qwen3-235b-a22b-instruct-2507` |
| 当前 judged-demo 主链路 | `upload -> ask -> citation -> PDF -> refusal` |

说明：
- 真正的 API Key 仅保存在本地 `.env`，不进入仓库。
- judge-facing 材料只展示平台使用结果、模型名、request id 和证据截图，不展示密钥。

## 主证据

### 1. 平台已经接入真实主链路

- 当前仓库运行配置已经切到 `Wuwen Xinqiong`
- 当前主 QA 路径使用 `deepseek-v4-flash`（V6 contract-patch holdout 后从 `qwen3-235b-a22b-instruct-2507` 切换为默认，原模型保留为 rollback fallback）
- `summary` / `outline` 仍跑在 `qwen3-235b-a22b-instruct-2507`，未单独重测前不切换

主证明来源：

- `evidence/reports/gold_sample_replay_real_summary_latest.md`
- `evidence/reports/gold_sample_qa_compare_latest.md`
- `evidence/reports/holdout_eval_v6_contract_patch_qwen_vs_flash_20260430.md`（QA 默认切换依据）

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

### 5. 当前 strict G3 已完成六次连续通过

来源：
- `evidence/experiments/20260420_g3_strict_rehearsal.md` (首批 3 轮)
- `evidence/experiments/20260423_g3_continuation.md` (续 3 轮)

- `6` 次连续通过
- 六轮都是 fresh-upload run，`file_id` 各不相同
- 每轮两次 answerable 都保持 `declared`
- 每轮 refusal 都走 `retrieval_gate` 或 `llm_refused` 路径
- log-backed spans 分别为：
  - 首批 3 轮：`13.5s`, `12.9s`, `15.8s`
  - 续 3 轮：`8.0s`, `31.3s`, `63.5s`
- fallback：`0 / 6`

## 答辩备用附录

### 备用模型

- 当前已验证的备用 QA 模型：`qwen3-32b`
- 用途：当部署环境延迟明显变紧时，作为同题组、同平台下的备用路径

### 当前 `G3` 口径

- 当前最强 `G3` 记录是按 `STRICT_G3_EXECUTION_PLAN.md` 留痕的 strict `6`-run batch
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

首批 3 轮（来源：`20260420_g3_strict_rehearsal.md`）：

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

续 3 轮（来源：`20260423_g3_continuation.md`）：

| Run | 问题 | Request ID |
| --- | --- | --- |
| `4` | answerable 1 | `a1b614b8b958444e873313164d2bc630` |
| `4` | answerable 2 | `8d8533a3685a40d69e8c151f6e8e91e0` |
| `4` | refusal | `56518f225a1b457681ed878cf1096bdc` |
| `5` | answerable 1 | `e0f86d6983d8417eb86af8588859980f` |
| `5` | answerable 2 | `41cbeb58175a4cbc94b5621485a4b48e` |
| `5` | refusal | `f420752eac5b4af7818c48d9a71668b8` |
| `6` | answerable 1 | `38e157176d40474b9dd76c33d4eed14e` |
| `6` | answerable 2 | `eeac7cd2fbd44bac84c30a479fa0716e` |
| `6` | refusal | `51be99cceee54d3ab613eaf58d5372b1` |

附录说明（诚实口径）：
- 上表这些 id 是系统的**本地 request_id**（`task_service` 生成的 `uuid4`），用于在各次实验记录内部交叉追踪，**仅作内部追溯**；它们记录在对应的实验 `.md`（`20260419_q2_*` / `20260420_g3_*` / `20260423_g3_*`）里。
- `data/logs/call_logs.jsonl` 会随运行滚动归档（最近一次归档于 2026-05-29，见 `data/logs/archive/`），因此历史 id 不保证都在当前 live log 内逐条留存——它们以带时间戳的实验记录为准做交叉佐证，而非以原始 raw log 复核。
- 首批 3 轮的 refusal 使用 `retrieval_gate`，续 3 轮中 Run 4 使用 `retrieval_gate`，Run 5-6 使用 `llm_refused`。

### 决赛"MaaS API 调用记录"正解（可控台对账）

- 从 2026-05-29 起，每次真实调用都额外捕获**无问芯穹平台返回的 request id**（`platform_request_id`，取自 MaaS response 的 `id`（`chatcmpl-…`）/ `x-request-id` 响应头），与本地 `request_id` 并存写入 `call_logs.jsonl`（代码：`model_client.py` 捕获 → `task_service.py` 落库）。
- 这个 `platform_request_id` **可在 infini-ai 控制台逐条对账**，是决赛"MaaS API 调用记录等证明材料"应提交的权威载体。
- **现成且已就绪的权威对账载体**：`evidence/reports/baseline_compare_eval.json`（受控对照实验的 **44 次真实调用**，每条都带平台返回的 `chatcmpl-…` request id，且模型字段与现场默认 `deepseek-v4-flash` 自洽）——这是当前**最直接**的"用了平台"铁证，可现场打开与 infini-ai 控制台逐条对账。注：上文 request id 索引里的本地 `uuid4` 仅作内部追溯、非平台对账载体，对账一律以平台 `chatcmpl-…` id 为准。
- 推荐流程：决赛前在演示机按 `GOLD_SAMPLE_RUNBOOK.md` 重跑锁定题 → `call_logs.jsonl` 落下一批带 `platform_request_id` 的新鲜记录；提交时**直接提供 `call_logs.jsonl` 逐行 + `baseline_compare_eval.json`** 作为对账载体（不要依赖 `export_log_summary.py`，它只产出聚合统计、不含 request id），并对其中 2-3 条配 infini-ai 控制台同一 id 记录的并排截图。这样"用了平台"就从"口说真实"升级为"可现场对账"。

## judge-facing 截图索引

主截图：

1. `evidence/screenshots/20260529_gold_ask_research_focus.png`
2. `evidence/screenshots/20260529_gold_pdf_render.png`
3. `evidence/screenshots/20260529_gold_ask_rank_accuracy.png`
4. `evidence/screenshots/20260529_gold_refusal.png`

附录截图：

1. `evidence/screenshots/20260529_stats_panel.png`
2. `evidence/screenshots/20260529_api_docs.png`

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
