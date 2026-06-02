# 平台调用对账证据 · 20260602

> 由 `scripts/build_platform_reconciliation.py` 从真实 `call_logs.jsonl` 生成，未手工编辑数字。原始日志快照见同目录 `platform_reconciliation_20260602_calls.jsonl`。

## 概览

- 证据问答（每笔带可引用的平台 request id）：**10 笔**
- 对应底层模型调用（Σ `agent_iterations`，含智能体二轮）：**13 次**（控制台按「每次模型调用」计数，故控制台次数会 ≥ 问答笔数；另含应用外的 key 验证调用）
- 模型：deepseek-v4-flash
- 日志侧累计 token（仅含返回 usage 的问答）：**31440**（注：拒答 / 二轮调用的 token 未全部落本地日志，**以控制台合计为准**，见下节）
- 触发智能体二轮（`agent_iterations≥2`）：**3 笔**
- 计费账户：领取 200 代金券的无问芯穹账号（请在该账号控制台核对下表 id/时间）。

## 控制台实测对账（权威合计）

无问芯穹控制台「用量统计」当日（20260602，北京时间）实测，作权威口径：

| 控制台指标 | 实测值 |
|---|---|
| 调用服务总次数 | **14** |
| 调用 token 总数 | **48383**（输入 33468 / 输出 14915） |
| 失败数 | **0** |
| 模型 | deepseek-v4-flash |

**对账逻辑（无差错）**：本报告 10 笔证据问答 → 底层模型调用 Σ`agent_iterations` = **13** 次；控制台另计入应用外的 key 验证调用（`verify_maas_key.py`，绕过应用日志）。`13 + 验证调用 ≈ 14`（控制台实测），失败数两侧均为 0。（差额 1 即验证/探测类调用）

> 诚实口径：控制台合计 token 高于上面「逐笔对账表」的日志侧求和，因为拒答调用与智能体二轮调用的 token 未全部落本地 per-ask 日志——**token 一律以控制台合计为准**，本地表仅用于把单笔 `chatcmpl-…` id 对到具体问答。

## 逐笔对账表

时间为**北京时间(UTC+8)**，与控制台一致；request id 可在控制台调用记录/账单逐条核对。

| # | 北京时间 | endpoint | 模型 | platform_request_id | 延迟ms | tok_in/out | agent轮次 | 结果 | 命中页 |
|---|---|---|---|---|---|---|---|---|---|
| 1 | 2026-06-02 19:51:48 | /api/ask | deepseek-v4-flash | `chatcmpl-60404072-c3a0-98ca-b5f9-e1f03c0ae356` | 5094 | 2538/489 | 1 | answered | [1, 2, 3, 11] |
| 2 | 2026-06-02 19:51:53 | /api/ask | deepseek-v4-flash | `chatcmpl-5e6db863-0e07-90c9-b896-ec52131bf66a` | 6072 | 2124/436 | 1 | answered | [1, 2, 5, 6] |
| 3 | 2026-06-02 19:54:14 | /api/ask | deepseek-v4-flash | `chatcmpl-444105a8-7cfb-92c6-bc80-3231eaf47ef8` | 17044 | 2477/2076 | 1 | answered | [1, 5, 6] |
| 4 | 2026-06-02 19:54:31 | /api/ask | deepseek-v4-flash | `chatcmpl-14062ead-86e2-931c-9eb6-0e14c484a689` | 19268 | 2638/2502 | 1 | answered | [1, 2, 5, 6, 8] |
| 5 | 2026-06-02 19:54:51 | /api/ask | deepseek-v4-flash | `chatcmpl-24004538-7ac4-97a4-a6ab-9120dd1fe405` | 10713 | 2726/1225 | 1 | answered | [1, 2, 3, 8] |
| 6 | 2026-06-02 19:56:03 | /api/ask | deepseek-v4-flash | `chatcmpl-b4f6bc1d-1494-9eec-9d16-5bf9ce549d43` | 20482 | None/None | 2 | refused | [1, 3, 7, 8] |
| 7 | 2026-06-02 19:56:23 | /api/ask | deepseek-v4-flash | `chatcmpl-341afb86-cbcc-90e1-ac9b-d6a3f65e4c54` | 16827 | 2597/1946 | 1 | answered | [1, 2, 5, 6, 8] |
| 8 | 2026-06-02 20:04:19 | /api/ask | deepseek-v4-flash | `chatcmpl-f8a7f432-3771-976e-98b8-828a0b256708` | 12358 | 2300/1092 | 1 | answered | [1, 2, 3] |
| 9 | 2026-06-02 20:04:31 | /api/ask | deepseek-v4-flash | `chatcmpl-4bffde9a-e9a5-94d0-8e74-2df618630440` | 12722 | None/None | 2 | refused | [1, 2, 3] |
| 10 | 2026-06-02 20:04:44 | /api/ask | deepseek-v4-flash | `chatcmpl-a70484b4-496e-9897-9664-b736e6d6e6eb` | 30084 | 2646/1628 | 2 | answered | [1, 3, 4, 5] |

## 智能体（自评-再检索）真实遥测

以下为 `agent_iterations=2` 的真实调用——模型在首轮自评「证据可能不足」后，系统自动二次检索再问一次（遥测落 `extra.agent_iterations`）：

- `chatcmpl-b4f6bc1d-1494-9eec-9d16-5bf9ce549d43`：iters=2，二轮仍无逐字证据 → 诚实拒答（不编造）。
- `chatcmpl-4bffde9a-e9a5-94d0-8e74-2df618630440`：iters=2，二轮仍无逐字证据 → 诚实拒答（不编造）。
- `chatcmpl-a70484b4-496e-9897-9664-b736e6d6e6eb`：iters=2，二轮确认证据 → declared 答出。

> 诚实口径：本批 `agent_iterations=2` 的样本里 `query_rewrites` 多为空——并非循环没跑，而是首轮检索已把相关片段捞全，二轮没有捞到**新**片段；这与我们「词法检索已高度饱和」的离线结论一致（见 `edge_hybrid_eval.md`）。循环的价值在于：证据真不在时即使升级仍**拒答不编**，在时则二轮确认后答出——拒答契约全程不变。带新片段的改写路径由单测 `test_agentic_ask_reretrieves_with_followup_query` 覆盖。

## 怎么核对（H3：控制台截图）

1. 登录领 200 代金券的无问芯穹账号 → 控制台 → 调用记录 / 用量账单。
2. 按上表「北京时间」定位时段，逐条核对 `chatcmpl-...` request id 与 token。
3. 截图即为「真实跑在平台 + 计费到代金券号」的决赛对账硬证据。
