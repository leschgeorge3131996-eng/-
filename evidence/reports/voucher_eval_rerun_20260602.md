# 代金券号复测 · 招牌评测复跑 + 全天平台用量 · 2026-06-02

> 目的：代金券号（领 200 元代金券的无问芯穹账号）API 通道打通后，在**该账号上**用当前 HEAD 代码把两套招牌评测各重跑一遍——既复核 `48/51`、`71/72` 是否站得住（诚实出数、不刷分），又把真实计费集中到代金券号、形成大批可对账调用。模型与现场默认一致：`deepseek-v4-flash`（QA）/ `qwen3-235b-a22b-instruct-2507`（rollback）。

## 一、复测结果（vs 文档保守口径）

| 评测集 | 本次代金券号复跑 | 文档保守口径 | 拒答精确率 | 证据声明率 |
|---|---|---|---|---|
| EXTENDED_EVAL_V1（51 题：43 答 + 8 拒） | **49 / 51（96.1%）** | 48 / 51（94.1%） | 8/8 = **100%** | **100%** |
| HOLDOUT_EVAL_V6 极限集（72 题：59 答 + 13 拒） | **72 / 72（100%）** | 71 / 72 | 13/13 = **100%** | **100%** |

两套**都达到或略高于文档口径**（各 +1）。原始报告：`extended_eval_v1_voucher_20260602.{md,json}`、`holdout_v6_voucher_20260602.{md,json}`。

## 二、诚实口径（关键，避免刷分）

- **文档对外口径仍保守取 `48/51`、`71/72`，不因这一次复跑而上调到 `49`、`72`。** 单次复跑高 1 分，更可能是「智能体自评-再检索 + 低置信复核」上线后修好了边界例，或跑间波动——不足以把它当稳定的新成绩。
- **V6 这次是 `72/72`，但绝不把它当「100%」卖点。** 它是固定 holdout 集上的回归复现，不等于开放域任意论文 100%；按既定纪律「诚实展示边界 > 刷 100%」，对外不喊 100%。
- 本页的价值是：**招牌数在另一个账号、当前代码上被独立复现（≥ 文档），可复跑、可对账**——这比把数字往上抬更可信。

### V1 那 2 个「失败」逐个核查 = 非真失败

| case_id | 类别 | 答案对不对（snippet_hit） | 引用页 vs manifest 期望页 | 定性 |
|---|---|---|---|---|
| `chinese_llm_spatial_eval:zh_a1_conf_name` | A1 | **对**（true） | 引用 [11] / 期望 [1] | 答对，引用页超出 manifest 期望集 |
| `chinese_llm_spatial_eval:zh_a2_prompt_strategies` | A2 | **对**（true） | 引用 [4] / 期望 [1,5,6] | 答对，引用页超出 manifest 期望集 |

两个都是 `declared=true`、`snippet_hit=true`（答案命中期望文本）、`retrieval_status=matched`——**不是错答、不是编造、不是拒答失败**，是「答对但引用页落在 manifest 写的期望页集之外」的引用颗粒度边界。**按诚实纪律仍计为失败、不反手判 manifest 写窄来刷成 51/51。**

## 三、全天平台用量（真实计费到代金券号）

复跑把大量真实调用集中到代金券号（来源：`call_logs.jsonl`，快照见 `voucher_eval_rerun_20260602_calls.jsonl`）：

| 指标 | 当日累计 |
|---|---|
| 带平台 `chatcmpl-…` id 的真实问答 | **132 笔** |
| 底层模型调用（Σ `agent_iterations`，含智能体二轮） | **158 次** |
| 日志侧 token 合计（控制台合计更高，见下） | **210,453** |
| 触发智能体二轮（`agent_iterations≥2`）的问答 | **26 笔** |
| 失败 | **0** |

- **26 笔 agentic 二轮**：相比初探批只有 3 笔，这次在 132 笔评测里有 26 笔触发了「自评证据不足 → 再检索 → 再答/拒」，是智能体循环在规模上真实激活的强证据（遥测落 `extra.agent_iterations`）。
- **控制台对账**：当日「用量统计」会显示约 `158 次底层调用 + 1 次 key 验证 ≈ 159 次`、token 合计高于日志侧 210,453（拒答/二轮 token 未全落 per-ask 日志，**以控制台为准**）。逐笔 `chatcmpl-…` id 的「已对到具体问答」的样例见 `platform_reconciliation_20260602.md`（那份与初探批 14 次控制台截图精确匹配，作为「单笔 id ↔ 控制台」的样板保留不动）。

## 四、产物清单

- 复测报告：`extended_eval_v1_voucher_20260602.{md,json}`、`holdout_v6_voucher_20260602.{md,json}`
- 全天调用快照：`voucher_eval_rerun_20260602_calls.jsonl`（132 笔带平台 id，无问答正文/无密钥）
- 单笔对账样板：`platform_reconciliation_20260602.md`（14 次，与控制台截图精确对账）

## 五、可复现

```
.venv/Scripts/python.exe scripts/extended_eval.py \
  --manifest evidence/materials/EXTENDED_EVAL_V1.json \
  --output evidence/reports/extended_eval_v1_voucher_<date>.md \
  --json-output evidence/reports/extended_eval_v1_voucher_<date>.json
# 把 manifest 换成 HOLDOUT_EVAL_V6_EXTREME_FULL_20260430.json 即复跑 72 题集
```
（脚本默认清缓存 → 真实调用；`.env` 用代金券号 key 即计费到该号。）
