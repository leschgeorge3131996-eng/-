# 研答通量化评测报告

## 评测范围

- 数据来源：strict G3 三轮 fresh-upload 批次（共 9 条请求）
- 锁定文档：`chinese_llm_spatial_eval.pdf`
- 锁定题组：2 answerable + 1 refusal
- 运行时模型：`qwen3-235b-a22b-instruct-2507`
- 评测日期：`2026-04-19`（log-backed UTC+08）

## 核心指标

| 指标 | 值 | 说明 |
| --- | --- | --- |
| 证据声明率 (Evidence Declaration Rate) | `100%` | answered 请求中 evidence_mode=declared 的比例 |
| 引用页码准确率 (Citation Page Accuracy) | `100%` | cited pages 命中人工标注正确页码的比例（基于 QA compare 验证数据） |
| 检索页码覆盖率 (Retrieval Page Coverage) | `100%` | 检索返回的页码覆盖人工标注正确页码的比例 |
| 证据引文提取率 (Evidence Quote Rate) | `100%` | evidence_quote_count / citation_count |
| 检索利用率 (Chunk Utilization) | `38%` | used_chunk_count / retrieved_chunk_count |
| 拒答精确率 (Refusal Precision) | `100%` | 离题问题被正确拒答的比例 |
| 跨轮一致性 (Cross-Run Consistency) | `100%` | 3 轮中 citation_count / evidence_mode / refusal outcome 一致的维度占比 |
| 平均响应延迟 (Avg Latency) | `5521 ms` | answerable 请求的平均延迟 |

## 指标解读

- 证据声明率 `100%`：所有 answerable 请求均由模型主动声明引用了哪些文档片段，而非系统兜底填充。
- 引用页码准确率 `100%`：模型返回的 citation 页码与人工标注的正确页码完全吻合（基于 QA compare 验证数据，Q1 cited [2,3]，Q2 cited [1,6]）。
- 检索页码覆盖率 `100%`：检索阶段返回的候选页码集合完整覆盖了人工标注的正确页码。
- 证据引文提取率 `100%`：每条 citation 都附带了经过原文子串验证的 evidence quote。
- 检索利用率 `38%`：检索返回的文档片段中，有 38% 被模型实际采纳为证据来源。
- 拒答精确率 `100%`：所有离题问题均在检索阶段被正确拦截，未进入模型生成。
- 跨轮一致性 `100%`：三轮独立 fresh-upload 运行中，核心输出结构保持一致。

## 逐轮明细

### 第 1 轮

| 题目 | outcome | evidence_mode | citation_count | evidence_quote_count | retrieved_chunks | used_chunks | latency_ms |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| Q1 研究问题 | answered | declared | 1 | 1 | 4 | 1 | 4640 |
| Q2 排名准确率 | answered | declared | 2 | 2 | 4 | 2 | 5998 |
| Q3 离题拒答 | refused | none | 0 | 0 | 0 | 0 | 9 |

### 第 2 轮

| 题目 | outcome | evidence_mode | citation_count | evidence_quote_count | retrieved_chunks | used_chunks | latency_ms |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| Q1 研究问题 | answered | declared | 1 | 1 | 4 | 1 | 4683 |
| Q2 排名准确率 | answered | declared | 2 | 2 | 4 | 2 | 5083 |
| Q3 离题拒答 | refused | none | 0 | 0 | 0 | 0 | 13 |

### 第 3 轮

| 题目 | outcome | evidence_mode | citation_count | evidence_quote_count | retrieved_chunks | used_chunks | latency_ms |
| --- | --- | --- | ---: | ---: | ---: | ---: | ---: |
| Q1 研究问题 | answered | declared | 1 | 1 | 4 | 1 | 6396 |
| Q2 排名准确率 | answered | declared | 2 | 2 | 4 | 2 | 6325 |
| Q3 离题拒答 | refused | none | 0 | 0 | 0 | 0 | 9 |


## 汇总统计

- 总请求数：`9`（6 answerable + 3 refusal）
- 总 citation 数：`9`
- 总 evidence quote 数：`9`
- 总 retrieved chunks：`24`
- 总 used chunks：`9`
- answerable 延迟范围：`4640-6396 ms`
- refusal 延迟范围：`9-13 ms`

## 结论

在锁定题组的 strict G3 三轮 fresh-upload 评测中，研答通的证据声明率、引用准确率、拒答精确率均为 `100%`，检索覆盖率 `100%`，跨轮输出结构一致性 `100%`，平均 answerable 延迟 `5521 ms`。主链路 `upload → ask → citation → PDF → refusal` 在量化层面可复现、可核验。
