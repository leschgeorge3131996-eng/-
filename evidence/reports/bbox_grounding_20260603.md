# bbox 证据回链端到端量化 · 2026-06-03

> 产品立身点是"引用可核验"——bbox 回链是 demo 第二页唯一要证明"证据是真的"的环节。
> `scripts/bbox_grounding_eval.py`（只读、作答可命中缓存）对固定 51 题集的 43 道可答题逐条跑真实 `ask`，
> 统计系统产出的 citation 里有多少**成功把证据 quote 定位到 PDF 页面的行级 bbox**。

## 结果

| 口径 | 数值 |
|---|---|
| 答题用例 / 有 citation | 43 / 43 |
| 总 citation | 53 |
| **行级可定位（≥1 行）** | **47 → 可定位率 88.7%** |
| 回退（无行级匹配） | 6 → 11.3% |
| 已定位条平均覆盖行数 | 3.3 行 |

**按文档类型拆（关键）：**

| 文档 | 类型 | 可定位/总 |
|---|---|---|
| `chinese_llm_spatial_eval` | PDF | 25/27 |
| `attention_is_all_you_need` | PDF | 22/22 |
| `paper_report` | Markdown | 0/2 |
| `research_brief` | Markdown | 0/2 |

- **在 PDF 文档上（bbox 行级回链真正适用的场景）：47/49 = `95.9%` 可定位**——这是产品立身点的硬数。
- **Markdown 文档 0/4 是预期回退**：md 是纯文本、无 PDF 页面行 bbox，引用退化为"页/片段级"而非"行级高亮"，不是 bug。

## 诚实口径

- **"可定位率" ≠ "命中正确行的准确率"**：本库无人工标注的 gold 行，脚本只证明 quote 能否落到 ≥1 行 + 回退依赖度。
- 但有一层**已有的强约束**：系统对每条 quote 做**逐字原文子串校验**（引用不可伪造，校验不过即丢弃）——因此被定位的 bbox 是"**包含该逐字 quote 的行**"，对学术论文里通常唯一的句子，可定位 ≈ 命中正确行。要把这点钉成数字，可对 ~10 条做人工抽查、与自动可定位率分开列（留作可选）。
- 回退率（11.3%，其中 8% 来自 markdown 无行结构）本身是诚实信号，不藏。

## 复现

```
.venv/Scripts/python.exe scripts/bbox_grounding_eval.py
```
代码：`backend/app/services/bbox_matcher.py::match_snippet_to_line_bboxes`（零改动，仅事后测量）。
