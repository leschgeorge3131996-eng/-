# 智能体真实遥测（加分项③做实）· 2026-06-03

> 目的：把"大模型与智能体能力"(加分项③) 从"宣称/空字段"做实成"真实、可量化、可对账"。
> 数据源：`data/logs/call_logs.jsonl`（真实无问芯穹平台调用，带 `platform_request_id`）。

## 一句话

`ask` 主链路是受控 agentic 循环：**每次作答前模型自评证据是否充分，不足则有界二次重试（`iter≤2`）**。
真实平台日志中 **823 笔 ask、197 笔（约 24%）真实触发了二轮自评**——不是 mock、不是口头。

## 真实事件（两个有代表性的，带 request_id 可对账）

| platform_request_id | 轮次 | 结果 | 含义 |
|---|---|---|---|
| `chatcmpl-2b1a068f-53df-91f7-8cd9-e5aceb5fc8d0` | iter=2 | answered / declared | 首轮自评证据不足 → 二次检索 → 第二轮确认证据后**答出**（命中页 1/5/6/7/8） |
| `chatcmpl-678cf141-9a15-9dee-bf8b-5c6d4dbbb48b` | iter=2 | refused（`llm_refused`） | 首轮自评不足 → 二次检索 → 仍无逐字证据 → **诚实拒答、不编造**（命中页 1/5/6/8/9） |

> 这恰是"智能体"该有的样子：**不是一问一答，而是自评不确定时再试一轮；证据在就答、不在就拒，拒答契约贯穿两轮全程。**

## 诚实边界（主动说，不刷分）

- 二次检索分支里"**改写 query 补检索新片段**"（`query_rewrites`）在生产日志中**多为空**——经实测（828 条生产日志 + 针对长论文埋深细节的 8 道定向问题）确认：**我们的检索 top-k 已包含答案 chunk，二轮再检索捞不到"新"片段**，故 `query_rewrites` 记录为空。该分支**已实现且单测覆盖**（`test_agentic_ask_reretrieves_with_followup_query`），只是被"检索质量好"这件事**天然抑制**。
- 我们**不**通过调小 top-k / 调差检索去人为触发它（那是刷分）。对外口径：**智能体能力 = 证据自评 + 有界二轮重试（24% 真实触发） + 双层拒答契约**，改写补检索是"已实现的备用分支"，不当作"现场可逐条核验"的卖点。

## 复现

```
# 统计真实 iter=2 占比
.venv/Scripts/python.exe -c "import json;from pathlib import Path;r=[json.loads(l) for l in Path('data/logs/call_logs.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()];real=[x for x in r if x.get('platform_request_id')];it2=[x for x in real if ((x.get('extra') or {}).get('agent_iterations') or 1)>=2];print(len(it2),'/',len(real))"
```
代码：`backend/app/services/task_service.py::_run_agentic_ask`。
