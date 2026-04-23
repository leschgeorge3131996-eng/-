# 2026-04-23 G3 Continuation Run

本记录延续 `20260420_g3_strict_rehearsal.md` 的严格版 G3 验证，补充三轮新的 fresh-upload 测试。

## 证据边界

- 本文件保留 repo 可验证部分：
  - request ids
  - log-backed timestamps
  - `declared / retrieval_no_match / llm_refused` status
  - fresh-upload signals
  - fallback usage
- 三轮权威运行均来自 `data/logs/call_logs.jsonl` 的最新记录

## 锁定设置

- 记录日期：
  - `2026-04-23`
- Log-backed run date in `UTC+08:00`:
  - `2026-04-21`
- 操作员角色：
  - 第二操作员
- 机器：
  - 本地 Windows 工作站
- 运行时：
  - 本地 frontend + 本地 backend
- 锁定样本：
  - `evidence/samples/chinese_llm_spatial_eval.pdf`
- 锁定路径：
  - `upload -> ask -> citation -> PDF -> refusal`
- 活跃 QA 模型：
  - `qwen3-235b-a22b-instruct-2507`
- Fallback 截图集可用：
  - yes (`evidence/screenshots/20260419_*`)
- Fallback 在权威批次中使用：
  - no

## 为什么这是严格版

- 每轮权威运行都有不同的 `file_id`，符合 fresh upload 而非复用已加载文档状态
- 所有 answerable asks 在三轮中均为 `cache_hit=false`
- 所有 answerable asks 保持 `evidence_mode=declared`
- 所有 refusal asks 走 `retrieval_gate` 或 `llm_refused` 路径
- 无实时请求失败，无截图 fallback 需求
- PDF jump/render 步骤是实时清单的一部分，但该点击不会发射到 `data/logs/call_logs.jsonl`；repo 可验证部分是锁定请求序列加时间戳和 request ids

## 权威运行

| Run | Local Start (`UTC+08`) | Local End (`UTC+08`) | Log-Backed Span | File ID | Q1 Declared | Q2 Declared | Refusal OK | Fallback Used | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | `2026-04-21 23:12:30` | `2026-04-21 23:12:38` | `8.0s` | `c72ca244f079453bb89d6f2d9eb80a2a` | yes | yes | yes | no | fresh upload; both answerable asks uncached; refusal via retrieval_gate |
| 2 | `2026-04-21 23:10:45` | `2026-04-21 23:11:16` | `31.3s` | `321f67cd8ad742978d443f078659dad0` | yes | yes | yes | no | fresh upload; both answerable asks uncached; refusal via llm_refused |
| 3 | `2026-04-21 23:08:01` | `2026-04-21 23:09:04` | `63.5s` | `bbd3daa797264ecd97e0400f9b875262` | yes | yes | yes | no | fresh upload; both answerable asks uncached; refusal via llm_refused |

## Request IDs

- Run 1:
  - answerable 1: `a1b614b8b958444e873313164d2bc630`
  - answerable 2: `8d8533a3685a40d69e8c151f6e8e91e0`
  - refusal: `56518f225a1b457681ed878cf1096bdc`
- Run 2:
  - answerable 1: `e0f86d6983d8417eb86af8588859980f`
  - answerable 2: `41cbeb58175a4cbc94b5621485a4b48e`
  - refusal: `f420752eac5b4af7818c48d9a71668b8`
- Run 3:
  - answerable 1: `38e157176d40474b9dd76c33d4eed14e`
  - answerable 2: `eeac7cd2fbd44bac84c30a479fa0716e`
  - refusal: `51be99cceee54d3ab613eaf58d5372b1`

## Log Cross-Checks

- Run 1:
  - Q1 latency: `3975 ms`
  - Q2 latency: `4034 ms`
  - refusal latency: `1 ms`
  - Q1 citations: `1`
  - Q2 citations: `1`
  - refusal route: `retrieval_no_match`
- Run 2:
  - Q1 latency: `4290 ms`
  - Q2 latency: `4941 ms`
  - refusal latency: `3174 ms`
  - Q1 citations: `1`
  - Q2 citations: `1`
  - refusal route: `llm_refused`
- Run 3:
  - Q1 latency: `5316 ms`
  - Q2 latency: `5634 ms`
  - refusal latency: `3175 ms`
  - Q1 citations: `1`
  - Q2 citations: `1`
  - refusal route: `llm_refused`

## 结果

- `G3` pass / fail:
  - pass
- 最强当前口径：
  - 严格 `6`-run 锁定路径可复现性通过（fresh uploads）
  - 累计：`20260420_g3_strict_rehearsal.md` 的 `3` 轮 + 本次 `3` 轮
- 相比旧记录的改进：
  - 延续了 `20260420_g3_strict_rehearsal.md` 的严格 fresh-upload 标准
  - 累计证据现在覆盖 `6` 轮独立 fresh-upload 运行
- 这仍然不能证明：
  - 这是锁定 gold path 的 judged-demo 可复现性证据，不是开放域产品泛化证明

## 后续材料更新

- 更新 `evidence/materials/HARD_EVIDENCE_SUMMARY.md`
- 更新 `evidence/materials/PLATFORM_USAGE_EVIDENCE.md`
- 更新 `evidence/materials/QA_BRIEF.md`
- 在 judge-facing 源文档中替换残留的 warm-state-only 措辞
