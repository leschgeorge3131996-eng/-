# Extended Evaluation Report — targeted_refusal_recovery

Generated: 2026-04-24 15:39:12

## Overall

- Total cases: **4**
- Passed: **4**
- Overall pass rate: **100.0%**
- Answerable pass rate: **100.0%**
- Refusal precision: **0.0%**
- Citation accuracy (answerable page-hit): **100.0%**
- Declaration rate (evidence_mode=declared on answerable): **100.0%**
- Avg latency: **5990 ms**

## By Category

| Category | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| A1 | 1 | 1 | 100.0% | 4095 |
| A3 | 1 | 1 | 100.0% | 5140 |
| A4 | 1 | 1 | 100.0% | 9559 |
| A5 | 1 | 1 | 100.0% | 5169 |

## By Difficulty

| Difficulty | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| easy | 1 | 1 | 100.0% | 4095 |
| hard | 1 | 1 | 100.0% | 5169 |
| medium | 2 | 2 | 100.0% | 7349 |

## By Document

| Doc | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| attention_is_all_you_need | 2 | 2 | 100.0% | 6827 |
| chinese_llm_spatial_eval | 2 | 2 | 100.0% | 5154 |

## Failure Attribution

| Failure type | Count |
| --- | ---: |
| (none) | 0 |

| Failure stage | Count |
| --- | ---: |
| (none) | 0 |

### Failed Case Triage

No failed cases.

## Case Detail

### [PASS] chinese_llm_spatial_eval:zh_a3_opensource
- Category: A3 / Difficulty: medium / Kind: answerable
- Query: 评测的模型中哪些是开源模型？
- Expected pages: [4, 5, 6] | Expected any of: ['Qwen', 'Deepseek']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3, 4] | citations: 1 | evidence_quotes: 1
- Latency: 5140 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 评测的模型中，开源模型是Qwen1.5-72B-chat和Deepseek-V2-chat。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a5_val_count
- Category: A5 / Difficulty: hard / Kind: answerable
- Query: SPaCE 2024 数据集验证集样本总数是多少？
- Expected pages: [4] | Expected any of: ['1210']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3, 4] | citations: 1 | evidence_quotes: 1
- Latency: 5169 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: SPaCE 2024 数据集验证集样本总数是1210。
- Error: (none)

### [PASS] attention_is_all_you_need:en_a4_contributions
- Category: A4 / Difficulty: medium / Kind: answerable
- Query: What are the main contributions of this paper?
- Expected pages: [1, 2, 3] | Expected any of: ['Transformer', 'attention', 'sequence']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1, 8, 10] | citations: 3 | evidence_quotes: 3
- Latency: 9559 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The main contributions of this paper are the proposal of the Transformer, a new model architecture for sequence transduction that relies entirely on attention mechanisms and dispenses with recurrence 
- Error: (none)

### [PASS] attention_is_all_you_need:en_a1_attention_heads
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: How many attention heads does the base Transformer model use?
- Expected pages: [4, 5] | Expected any of: ['8', 'h = 8', 'h=8']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [4, 5] | citations: 1 | evidence_quotes: 1
- Latency: 4095 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The base Transformer model uses 8 attention heads.
- Error: (none)
