# Extended Evaluation Report — EXTENDED_EVAL_V1_REFUSAL_ONLY

Generated: 2026-04-21 22:29:50

## Overall

- Total cases: **3**
- Passed: **3**
- Overall pass rate: **100.0%**
- Answerable pass rate: **0.0%**
- Refusal precision: **100.0%**
- Citation accuracy (answerable page-hit): **0.0%**
- Declaration rate (evidence_mode=declared on answerable): **0.0%**
- Avg latency: **3920 ms**

## By Category

| Category | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| B1 | 2 | 2 | 100.0% | 4383 |
| B2 | 1 | 1 | 100.0% | 2993 |

## By Difficulty

| Difficulty | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| easy | 2 | 2 | 100.0% | 4383 |
| hard | 1 | 1 | 100.0% | 2993 |

## By Document

| Doc | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| attention_is_all_you_need | 2 | 2 | 100.0% | 4261 |
| chinese_llm_spatial_eval | 1 | 1 | 100.0% | 3237 |

## Case Detail

### [PASS] chinese_llm_spatial_eval:zh_b1_quantum
- Category: B1 / Difficulty: easy / Kind: refusal
- Query: 量子纠缠的物理原理是什么？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 3237 ms
- Fail reason: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] attention_is_all_you_need:en_b1_everest
- Category: B1 / Difficulty: easy / Kind: refusal
- Query: What is the height of Mount Everest?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 5530 ms
- Fail reason: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] attention_is_all_you_need:en_b2_vaswani_affiliation_now
- Category: B2 / Difficulty: hard / Kind: refusal
- Query: What is Ashish Vaswani's current employer in 2026?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 2993 ms
- Fail reason: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)
