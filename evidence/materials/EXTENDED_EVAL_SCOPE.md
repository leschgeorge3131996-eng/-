# 扩展评测集 V1 Scope（离国一的最大短板补救）

## 动机

当前 judge-facing 的量化指标（`evidence/reports/quantitative_eval_metrics.md`）基于 3 道金标题，`declaration rate = 100%`、`citation accuracy = 100%`、`refusal precision = 100%` 看着漂亮，但**样本量太小**，懂行评委会直接问"3 题的 100% 不等于 300 题的 100%"。

本评测集目的：**把样本量从 3 扩到 50+，在可保留的通过率下让指标有统计学可信度**。不追求"全题 100%"，追求"在更大分布上 ≥85%"。

## 不做的事

- 不引入公开 benchmark（CMRC / DuReader / RAGTruth）—— 引入会涉及数据集授权、文档替换、评审口径变更，时间不够
- 不改 retrieval / LLM 层 —— 本评测只衡量当前 HEAD 的表现，不是算法迭代
- 不做人工精细评分 —— 用可自动判定的字段（页码命中、拒答命中、答案是否 declared）作为代理指标；答案语义对错只抽查

## 题型分桶 & 目标数量

**共 55 题**，按桶目标：

| 桶 | 代号 | 目标数 | 判定 | 期望通过率 |
|---|---|---|---|---|
| 事实性答题（定义/数字/名词直摘） | A1 | 12 | cited page ∈ 期望页集 且 declared | ≥ 90% |
| 推理性答题（跨章节综合） | A2 | 8 | cited page ∈ 期望页集 且 declared | ≥ 75% |
| 比较性答题（表格/对比类） | A3 | 6 | cited page ∈ 期望页集 且 declared | ≥ 80% |
| 总结性答题（章节主旨 / 摘要类） | A4 | 8 | declared 且 至少 1 citation | ≥ 85% |
| 边界正例（文档里但很偏僻） | A5 | 6 | cited page ∈ 期望页集 | ≥ 60% |
| 纯离题拒答 | B1 | 6 | `retrieval_status=no_match` | = 100% |
| 诱导拒答（提到文档实体但无法答） | B2 | 5 | 拒答 或 declared=false | ≥ 60% |
| 半相关边界拒答（领域相关但文档没讲） | B3 | 4 | 拒答 或 declared=false | ≥ 75% |

**综合目标**：整体通过率 ≥ 82%，refusal precision ≥ 90%，citation accuracy ≥ 85%。这个数字放出来比"3 题 100%"有说服力得多。

## 文档来源

`evidence/samples/` 内已有文档：

| 文档 | 类型 | 题目承载数（预估） |
|---|---|---|
| `chinese_llm_spatial_eval.pdf` | 中文学术论文 11 页 | ~25 题（主力） |
| `attention_is_all_you_need.pdf` | 英文经典论文 | ~20 题 |
| `paper_report.md` | 报告型 md | ~5 题 |
| `research_brief.md` | 简报型 md | ~5 题 |

## 难度分布

每道题标 `difficulty ∈ {easy, medium, hard}`：
- easy：一个 chunk 内直接找到答案（12 题 A1 的多数）
- medium：需要读懂段落上下文（A2、A3、A4 的多数）
- hard：跨章节 / 需要推理 / 容易被噪声 chunk 干扰（A5 全部、B2 多数）

## 产出

- **manifest JSON**：`evidence/materials/EXTENDED_EVAL_V1.json` —— 复用 `scripts/replay_sample_set.py` 可读的 `{prompts: [...]}` 格式，每题补 `expected_pages` / `category` / `difficulty` 扩展字段
- **批量评测脚本**：`scripts/extended_eval.py` —— 基于 `replay_sample_set.py` 框架，额外生成分桶 / 分文档 / 分难度的聚合报告
- **报告**：`evidence/reports/extended_eval_v1.md` —— 进 `HARD_EVIDENCE_SUMMARY.md` 主表

## 判定边界（避免答辩被挑毛病）

1. "citation accuracy" 定义：期望页集合 ∩ 实际 cited 页集合 ≠ ∅ 即算命中（不是严格相等），这是标准 RAG QA benchmark 口径
2. "declared" 来自 `evidence_mode=declared`，不是人工看有没有引号
3. refusal 判定只看 `retrieval_status=no_match`（retrieval gate 拦）或答案显式说"无法回答"
4. 答案正确性：**抽样人工核查 10 题**，其余依赖 declared + citation 代理指标

## 风险

- 批量调用 API 产生费用：预估 55 题 × 两题答题 ~5k tokens + 拒答 ~0 tokens ≈ ¥2–5
- 通过率若低于预期（如 <70%），说明当前 HEAD 在广分布下召回不稳，此时**不改代码**，只把真实数字诚实公开，比"藏着 3 题 100%"对评委更可信
