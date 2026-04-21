# Extended Evaluation Report — EXTENDED_EVAL_V1

Generated: 2026-04-21 22:35:30

## Overall

- Total cases: **20**
- Passed: **17**
- Overall pass rate: **85.0%**
- Answerable pass rate: **82.4%**
- Refusal precision: **100.0%**
- Citation accuracy (answerable page-hit): **82.4%**
- Declaration rate (evidence_mode=declared on answerable): **82.4%**
- Avg latency: **6223 ms**

## By Category

| Category | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| A1 | 6 | 4 | 66.7% | 4904 |
| A2 | 4 | 4 | 100.0% | 9618 |
| A3 | 2 | 2 | 100.0% | 7464 |
| A4 | 3 | 2 | 66.7% | 6233 |
| A5 | 2 | 2 | 100.0% | 6196 |
| B1 | 2 | 2 | 100.0% | 3089 |
| B2 | 1 | 1 | 100.0% | 4375 |

## By Difficulty

| Difficulty | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| easy | 9 | 7 | 77.8% | 4699 |
| hard | 3 | 3 | 100.0% | 5589 |
| medium | 8 | 7 | 87.5% | 8176 |

## By Document

| Doc | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| attention_is_all_you_need | 10 | 8 | 80.0% | 5021 |
| chinese_llm_spatial_eval | 10 | 9 | 90.0% | 7426 |

## Case Detail

### [PASS] chinese_llm_spatial_eval:zh_a1_accuracy
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 本研究的总体准确率得分是多少？
- Expected pages: [1, 5, 6] | Expected any of: ['56.20', '56.2']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5, 6] | citations: 1 | evidence_quotes: 1
- Latency: 4393 ms
- Fail reason: (none)
- Answer snippet: 本研究的总体准确率得分为56.20%。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a1_best_model
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 在 1-shot 通用提示词策略下，哪一个模型的表现最好？
- Expected pages: [1, 5, 6] | Expected any of: ['ERNIE-4', 'ERNIE']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5, 6] | citations: 1 | evidence_quotes: 1
- Latency: 6150 ms
- Fail reason: (none)
- Answer snippet: 在 1-shot 通用提示词策略下，ERNIE-4 的表现最好，得分为 53.88。
- Error: (none)

### [FAIL] chinese_llm_spatial_eval:zh_a1_authors
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 论文的作者来自哪所高校？
- Expected pages: [1] | Expected any of: ['北京师范大学', 'Beijing Normal']
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 4164 ms
- Fail reason: pages [] ∩ [1] empty; evidence_mode=none; answer missing any of ['北京师范大学', 'Beijing Normal']
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a2_two_questions
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: 本研究试图回答的两个核心问题是什么？
- Expected pages: [2] | Expected any of: ['理解的程度', '具体分类', '哪些']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1, 2] | citations: 1 | evidence_quotes: 1
- Latency: 6797 ms
- Fail reason: (none)
- Answer snippet: 本研究试图回答的两个核心问题是：1）大模型对空间语义的理解程度如何？2）在理解空间语义的具体任务上，大模型各有哪些优劣？
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a2_prompt_strategies
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: 论文中提到了哪几种提示词策略？它们的区别是什么？
- Expected pages: [1, 5, 6] | Expected any of: ['通用', '工作流', '思维链']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 0
- Latency: 19352 ms
- Fail reason: (none)
- Answer snippet: 论文中提到了三种提示词策略：普通提示（Vanilla Prompt）、工作流（Workflow）和思维链（Chain of Thought, CoT）。普通提示和工作流提示采用0-shot、1-shot、3-shot的方式构建，而思维链提示仅采用1-shot方式，并参考了Wei (2022)的提示词设计，将其分为“想法”和“答案”两部分，以使输出更结构化，便于提取思维过程和答案。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a3_subtasks
- Category: A3 / Difficulty: medium / Kind: answerable
- Query: SPaCE 2024 数据集包含哪几个子任务？
- Expected pages: [4] | Expected any of: ['实体识别', '角色识别', '异常识别', '方位', '同义']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3, 4] | citations: 1 | evidence_quotes: 1
- Latency: 8850 ms
- Fail reason: (none)
- Answer snippet: SPaCE 2024数据集包含五个子任务：空间信息实体识别、空间信息角色识别、空间信息异常识别、空间方位信息推理和空间异形同义识别。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a4_method_summary
- Category: A4 / Difficulty: medium / Kind: answerable
- Query: 请简要总结本论文采用的研究方法。
- Expected pages: [1, 2, 5, 6] | Expected any of: ['提示词', '大语言模型', '空间语义']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1, 2] | citations: 1 | evidence_quotes: 1
- Latency: 9311 ms
- Fail reason: (none)
- Answer snippet: 本论文基于第四届中文空间语义理解评测任务（SpaCE2024），首先介绍空间语义评测的背景和相关研究，然后通过实验分析不同模型的空间语义理解能力，最后对实验结果进行讨论和分析，以探究大模型对空间语义的理解程度及其在具体任务上的优劣。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a4_ranking
- Category: A4 / Difficulty: easy / Kind: answerable
- Query: 作者团队在比赛中最终取得了什么名次？
- Expected pages: [1] | Expected any of: ['第六', '六']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 6691 ms
- Fail reason: (none)
- Answer snippet: 作者团队在比赛中最终取得了第六名。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a5_train_count
- Category: A5 / Difficulty: hard / Kind: answerable
- Query: SPaCE 2024 数据集训练集样本总数是多少？
- Expected pages: [4] | Expected any of: ['4483']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3, 4] | citations: 1 | evidence_quotes: 1
- Latency: 5886 ms
- Fail reason: (none)
- Answer snippet: SPaCE 2024 数据集训练集样本总数是4483。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_b1_quantum
- Category: B1 / Difficulty: easy / Kind: refusal
- Query: 量子纠缠的物理原理是什么？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 2669 ms
- Fail reason: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] attention_is_all_you_need:en_a1_encoder_layers
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: How many identical layers does the Transformer encoder consist of?
- Expected pages: [3] | Expected any of: ['6', 'N = 6', 'N=6']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3] | citations: 1 | evidence_quotes: 1
- Latency: 5297 ms
- Fail reason: (none)
- Answer snippet: The Transformer encoder consists of 6 identical layers.
- Error: (none)

### [FAIL] attention_is_all_you_need:en_a1_first_authors
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: Who are the first two listed authors of this paper?
- Expected pages: [1] | Expected any of: ['Vaswani', 'Shazeer']
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 3091 ms
- Fail reason: pages [] ∩ [1] empty; evidence_mode=none; answer missing any of ['Vaswani', 'Shazeer']
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] attention_is_all_you_need:en_a1_arxiv_id
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: What is the arXiv identifier of this paper?
- Expected pages: [1] | Expected any of: ['1706.03762']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 6330 ms
- Fail reason: (none)
- Answer snippet: The arXiv identifier of this paper is arXiv:1706.03762v7.
- Error: (none)

### [PASS] attention_is_all_you_need:en_a2_why_no_recurrence
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: Why does the Transformer architecture avoid recurrence entirely?
- Expected pages: [2, 3] | Expected any of: ['parallel', 'sequential', 'long', 'dependencies']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1, 2] | citations: 2 | evidence_quotes: 2
- Latency: 4849 ms
- Fail reason: (none)
- Answer snippet: The Transformer architecture avoids recurrence entirely because it relies solely on an attention mechanism to draw global dependencies between input and output, dispensing with recurrence and convolut
- Error: (none)

### [PASS] attention_is_all_you_need:en_a2_scaling_reason
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: Why is the dot product scaled by the square root of d_k in scaled dot-product attention?
- Expected pages: [4] | Expected any of: ['gradient', 'magnitude', 'large', 'softmax']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [4] | citations: 2 | evidence_quotes: 2
- Latency: 7477 ms
- Fail reason: (none)
- Answer snippet: The dot product is scaled by the square root of d_k to prevent the softmax function from having extremely small gradients due to large magnitude dot products for large values of d_k. Scaling counterac
- Error: (none)

### [PASS] attention_is_all_you_need:en_a3_complexity_compare
- Category: A3 / Difficulty: medium / Kind: answerable
- Query: Compare the per-layer computational complexity of self-attention and recurrent layers as shown in the paper.
- Expected pages: [6] | Expected any of: ['n^2', 'n2', 'O(n', 'sequence length']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5, 6] | citations: 1 | evidence_quotes: 1
- Latency: 6078 ms
- Fail reason: (none)
- Answer snippet: The per-layer computational complexity of self-attention layers is O(n²·d), whereas that of recurrent layers is O(n·d²).
- Error: (none)

### [FAIL] attention_is_all_you_need:en_a4_contributions
- Category: A4 / Difficulty: medium / Kind: answerable
- Query: What are the main contributions of this paper?
- Expected pages: [1, 2, 3] | Expected any of: ['Transformer', 'attention', 'sequence']
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 2697 ms
- Fail reason: pages [] ∩ [1, 2, 3] empty; evidence_mode=none; answer missing any of ['Transformer', 'attention', 'sequence']
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] attention_is_all_you_need:en_a5_conv_path_length
- Category: A5 / Difficulty: hard / Kind: answerable
- Query: According to Table 1, what is the maximum path length for convolutional layers?
- Expected pages: [6] | Expected any of: ['log', 'O(log']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5, 6] | citations: 1 | evidence_quotes: 1
- Latency: 6506 ms
- Fail reason: (none)
- Answer snippet: The maximum path length for convolutional layers is O(logk(n)).
- Error: (none)

### [PASS] attention_is_all_you_need:en_b1_everest
- Category: B1 / Difficulty: easy / Kind: refusal
- Query: What is the height of Mount Everest?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 3510 ms
- Fail reason: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] attention_is_all_you_need:en_b2_vaswani_affiliation_now
- Category: B2 / Difficulty: hard / Kind: refusal
- Query: What is Ashish Vaswani's current employer in 2026?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 4375 ms
- Fail reason: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)
