# Extended Evaluation Report — EXTENDED_EVAL_V1

Generated: 2026-06-02 20:39:42

## Overall

- Total cases: **51**
- Passed: **49**
- Overall pass rate: **96.1%**
- Answerable pass rate: **95.3%**
- Refusal precision: **100.0%**
- Citation accuracy (answerable page-hit): **95.3%**
- Declaration rate (evidence_mode=declared on answerable): **100.0%**
- Avg latency: **7195 ms**

## By Category

| Category | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| A1 | 15 | 14 | 93.3% | 6754 |
| A2 | 9 | 8 | 88.9% | 7553 |
| A3 | 7 | 7 | 100.0% | 7799 |
| A4 | 7 | 7 | 100.0% | 5932 |
| A5 | 5 | 5 | 100.0% | 6270 |
| B1 | 5 | 5 | 100.0% | 7479 |
| B2 | 3 | 3 | 100.0% | 10927 |

## By Difficulty

| Difficulty | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| easy | 24 | 23 | 95.8% | 6507 |
| hard | 8 | 8 | 100.0% | 8017 |
| medium | 19 | 18 | 94.7% | 7718 |

## By Document

| Doc | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| attention_is_all_you_need | 20 | 20 | 100.0% | 7763 |
| chinese_llm_spatial_eval | 25 | 23 | 92.0% | 7233 |
| paper_report | 3 | 3 | 100.0% | 5461 |
| research_brief | 3 | 3 | 100.0% | 4823 |

## Failure Attribution

| Failure type | Count |
| --- | ---: |
| wrong_page | 2 |

| Failure stage | Count |
| --- | ---: |
| citation | 2 |

### Failed Case Triage

| Case | Failure type | Stage | Reason |
| --- | --- | --- | --- |
| chinese_llm_spatial_eval:zh_a2_prompt_strategies | wrong_page | citation | pages [4] ∩ [1, 5, 6] empty |
| chinese_llm_spatial_eval:zh_a1_conf_name | wrong_page | citation | pages [11] ∩ [1] empty |

## Case Detail

### [PASS] chinese_llm_spatial_eval:zh_a1_accuracy
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 本研究的总体准确率得分是多少？
- Expected pages: [1, 5, 6] | Expected any of: ['56.20', '56.2']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4195 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 本研究的总体准确率得分为56.20%。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a1_best_model
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 在 1-shot 通用提示词策略下，哪一个模型的表现最好？
- Expected pages: [1, 5, 6] | Expected any of: ['ERNIE-4', 'ERNIE']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5, 6] | citations: 1 | evidence_quotes: 1
- Latency: 9795 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Under the 1-shot vanilla prompt strategy, ERNIE-4 achieved the best performance with an accuracy of 53.88% on the validation set.
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a1_authors
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 论文的作者来自哪所高校？
- Expected pages: [1] | Expected any of: ['北京师范大学', 'Beijing Normal']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3618 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 论文的作者来自北京师范大学。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a2_two_questions
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: 本研究试图回答的两个核心问题是什么？
- Expected pages: [2] | Expected any of: ['理解的程度', '具体分类', '哪些']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1, 2] | citations: 1 | evidence_quotes: 1
- Latency: 4855 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 本研究试图回答的两个核心问题是：1）大模型对空间语义的理解程度如何？2）在理解空间语义的具体任务上，大模型各有哪些优劣？
- Error: (none)

### [FAIL] chinese_llm_spatial_eval:zh_a2_prompt_strategies
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: 论文中提到了哪几种提示词策略？它们的区别是什么？
- Expected pages: [1, 5, 6] | Expected any of: ['通用', '工作流', '思维链']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [4] | citations: 1 | evidence_quotes: 1
- Latency: 7696 ms
- Fail reason: pages [4] ∩ [1, 5, 6] empty
- Failure type: wrong_page | stage: citation
- Answer snippet: 论文中提到了三种提示词策略：普通提示（Vanilla Prompt）、工作流（Workflow）、思维链（Chain of Thought, CoT）。区别如下：普通提示和工作流提示词都采用0-shot、1-shot、3-shot的样本设置，而思维链提示词采用1-shot；思维链提示词的结构分为“想法”和“答案”两部分，使输出更结构化，便于提取。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a3_subtasks
- Category: A3 / Difficulty: medium / Kind: answerable
- Query: SPaCE 2024 数据集包含哪几个子任务？
- Expected pages: [4] | Expected any of: ['实体识别', '角色识别', '异常识别', '方位', '同义']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3, 4] | citations: 2 | evidence_quotes: 1
- Latency: 4683 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: SPaCE 2024 数据集包含五个子任务：空间信息实体识别、空间信息角色识别、空间信息异常识别、空间方位信息推理和空间异形同义识别。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a4_method_summary
- Category: A4 / Difficulty: medium / Kind: answerable
- Query: 请简要总结本论文采用的研究方法。
- Expected pages: [1, 2, 5, 6] | Expected any of: ['提示词', '大语言模型', '空间语义']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5722 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 本论文采用普通提示词、工作流提示词和思维链三种提示词策略来探讨大模型的空间语义理解能力，最终发现ERNIE-4在1-shot的普通提示词上表现最佳。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a4_ranking
- Category: A4 / Difficulty: easy / Kind: answerable
- Query: 作者团队在比赛中最终取得了什么名次？
- Expected pages: [1] | Expected any of: ['第六', '六']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4413 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 作者团队在比赛中最终取得了第六名。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a5_train_count
- Category: A5 / Difficulty: hard / Kind: answerable
- Query: SPaCE 2024 数据集训练集样本总数是多少？
- Expected pages: [4] | Expected any of: ['4483']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3, 4] | citations: 1 | evidence_quotes: 1
- Latency: 4902 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 4483
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_b1_quantum
- Category: B1 / Difficulty: easy / Kind: refusal
- Query: 量子纠缠的物理原理是什么？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 8667 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [FAIL] chinese_llm_spatial_eval:zh_a1_conf_name
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 本论文发表在哪个学术会议上？
- Expected pages: [1] | Expected any of: ['CCL', '中国计算语言学']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [11] | citations: 1 | evidence_quotes: 1
- Latency: 9150 ms
- Fail reason: pages [11] ∩ [1] empty
- Failure type: wrong_page | stage: citation
- Answer snippet: 第二十三届中国计算语言学大会（CCL 2024）
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a1_temperature
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 实验中模型的 temperature 参数设置为多少？
- Expected pages: [5] | Expected any of: ['0.1']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5] | citations: 1 | evidence_quotes: 1
- Latency: 3938 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 实验中模型的 temperature 参数设置为 0.1。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a1_author_count
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 本论文共有几位作者？
- Expected pages: [1] | Expected any of: ['3', '三']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 7058 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 本论文共有三位作者：霍世图、王钰君、吴童杰。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a1_school_department
- Category: A1 / Difficulty: medium / Kind: answerable
- Query: 作者所在的具体学院是哪一所？
- Expected pages: [1] | Expected any of: ['国际中文教育学院']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 10469 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 作者所在的学院是北京师范大学的国际中文教育学院。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a2_ernie_weakness
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: ERNIE-4 在哪一类任务上表现最弱？
- Expected pages: [5, 6, 7, 8, 9] | Expected any of: ['空间推理', '推理']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [6] | citations: 1 | evidence_quotes: 1
- Latency: 6637 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 根据文档描述，所有模型在空间推理任务的表现相对最差，因此ERNIE-4也在空间推理任务上表现最弱。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a2_glm4_best
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: GLM-4 在哪种提示词配置下验证集表现最好？
- Expected pages: [6] | Expected any of: ['工作流', '1-shot', '53.14']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5, 6] | citations: 1 | evidence_quotes: 1
- Latency: 10317 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: GLM-4在验证集表现最好的提示词配置是工作流提示词（Workflow）下的1-shot（单样本），准确率为53.14%。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a3_models_count
- Category: A3 / Difficulty: easy / Kind: answerable
- Query: 本研究共评测了多少个大模型？
- Expected pages: [4, 5, 6] | Expected any of: ['六个', '6']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5, 6] | citations: 1 | evidence_quotes: 1
- Latency: 8695 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 本研究共评测了6个大模型，包括ERNIE-4、GLM-4、GPT-4o、GPT-4 Turbo、Deepseek-V2-chat和Qwen1.5-72B-chat。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a3_opensource
- Category: A3 / Difficulty: medium / Kind: answerable
- Query: 评测的模型中哪些是开源模型？
- Expected pages: [4, 5, 6] | Expected any of: ['Qwen', 'Deepseek']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3, 4] | citations: 1 | evidence_quotes: 1
- Latency: 8576 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 评测中开源的模型是 Qwen1.5-72B-chat（由阿里巴巴开发）和 Deepseek-V2-chat（由深度求索开发）。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a3_context_max
- Category: A3 / Difficulty: medium / Kind: answerable
- Query: 评测模型支持的最大上下文长度是多少？
- Expected pages: [4] | Expected any of: ['12.8', '128']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3, 4] | citations: 1 | evidence_quotes: 1
- Latency: 13910 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 评测模型支持的最大上下文长度为12.8万（即128,000 tokens）。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a4_eval_metric
- Category: A4 / Difficulty: easy / Kind: answerable
- Query: 本研究采用的评测指标是什么？
- Expected pages: [5] | Expected any of: ['准确率', 'Accuracy']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5] | citations: 1 | evidence_quotes: 1
- Latency: 5319 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 本研究的评测指标是准确率（Accuracy）。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a4_cot_sample_source
- Category: A4 / Difficulty: medium / Kind: answerable
- Query: 思维链提示词的样本思考过程由什么生成？
- Expected pages: [5] | Expected any of: ['GPT-4']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [4, 5] | citations: 1 | evidence_quotes: 1
- Latency: 4772 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 思维链提示词的样本思考过程由GPT-4生成。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a5_test_count
- Category: A5 / Difficulty: hard / Kind: answerable
- Query: SPaCE 2024 数据集测试集样本总数是多少？
- Expected pages: [4] | Expected any of: ['4530']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3, 4] | citations: 1 | evidence_quotes: 1
- Latency: 10752 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: SPaCE 2024 数据集测试集样本总数为4530。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a5_val_count
- Category: A5 / Difficulty: hard / Kind: answerable
- Query: SPaCE 2024 数据集验证集样本总数是多少？
- Expected pages: [4] | Expected any of: ['1210']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3, 4] | citations: 1 | evidence_quotes: 1
- Latency: 5146 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: SPaCE 2024 数据集验证集样本总数为1210。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a5_study_period
- Category: A5 / Difficulty: hard / Kind: answerable
- Query: 本研究的开展日期是哪段时间？
- Expected pages: [4, 5] | Expected any of: ['2024年5月']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [4] | citations: 1 | evidence_quotes: 1
- Latency: 4965 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 2024年5月1日至5月17日
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_b1_weather
- Category: B1 / Difficulty: easy / Kind: refusal
- Query: 北京今天的天气怎么样？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 12576 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] attention_is_all_you_need:en_a1_encoder_layers
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: How many identical layers does the Transformer encoder consist of?
- Expected pages: [3] | Expected any of: ['6', 'N = 6', 'N=6']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3] | citations: 1 | evidence_quotes: 1
- Latency: 16677 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The Transformer encoder consists of 6 identical layers.
- Error: (none)

### [PASS] attention_is_all_you_need:en_a1_first_authors
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: Who are the first two listed authors of this paper?
- Expected pages: [1] | Expected any of: ['Vaswani', 'Shazeer']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5459 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The first two listed authors are Ashish Vaswani and Noam Shazeer.
- Error: (none)

### [PASS] attention_is_all_you_need:en_a1_arxiv_id
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: What is the arXiv identifier of this paper?
- Expected pages: [1] | Expected any of: ['1706.03762']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5623 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 1706.03762
- Error: (none)

### [PASS] attention_is_all_you_need:en_a2_why_no_recurrence
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: Why does the Transformer architecture avoid recurrence entirely?
- Expected pages: [2, 3] | Expected any of: ['parallel', 'sequential', 'long', 'dependencies']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1, 2] | citations: 2 | evidence_quotes: 2
- Latency: 6161 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The Transformer architecture avoids recurrence entirely because it relies solely on attention mechanisms to capture global dependencies between input and output, replacing recurrent or convolutional l
- Error: (none)

### [PASS] attention_is_all_you_need:en_a2_scaling_reason
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: Why is the dot product scaled by the square root of d_k in scaled dot-product attention?
- Expected pages: [4] | Expected any of: ['gradient', 'magnitude', 'large', 'softmax']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [4] | citations: 1 | evidence_quotes: 0
- Latency: 19708 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The dot product is scaled by the square root of d_k to prevent the dot products from growing too large in magnitude for large values of d_k, which would push the softmax function into regions with ext
- Error: (none)

### [PASS] attention_is_all_you_need:en_a3_complexity_compare
- Category: A3 / Difficulty: medium / Kind: answerable
- Query: Compare the per-layer computational complexity of self-attention and recurrent layers as shown in the paper.
- Expected pages: [6] | Expected any of: ['n^2', 'n2', 'O(n', 'sequence length']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5, 6] | citations: 1 | evidence_quotes: 1
- Latency: 8110 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: According to Table 1 of the paper, the per-layer computational complexity of self-attention layers is O(n²·d), while recurrent layers have O(n·d²).
- Error: (none)

### [PASS] attention_is_all_you_need:en_a4_contributions
- Category: A4 / Difficulty: medium / Kind: answerable
- Query: What are the main contributions of this paper?
- Expected pages: [1, 2, 3] | Expected any of: ['Transformer', 'attention', 'sequence']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1, 2, 8, 10] | citations: 4 | evidence_quotes: 3
- Latency: 10760 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The main contributions of this paper are: proposing the Transformer, a novel network architecture based solely on attention mechanisms, dispensing with recurrence and convolutions entirely. It achieve
- Error: (none)

### [PASS] attention_is_all_you_need:en_a5_conv_path_length
- Category: A5 / Difficulty: hard / Kind: answerable
- Query: According to Table 1, what is the maximum path length for convolutional layers?
- Expected pages: [6] | Expected any of: ['log', 'O(log']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5, 6] | citations: 1 | evidence_quotes: 1
- Latency: 5589 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: According to Table 1, the maximum path length for convolutional layers is O(log_k(n)).
- Error: (none)

### [PASS] attention_is_all_you_need:en_b1_everest
- Category: B1 / Difficulty: easy / Kind: refusal
- Query: What is the height of Mount Everest?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 6745 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: No relevant information can be found in the provided documents to answer this question.
- Error: (none)

### [PASS] attention_is_all_you_need:en_b2_vaswani_affiliation_now
- Category: B2 / Difficulty: hard / Kind: refusal
- Query: What is Ashish Vaswani's current employer in 2026?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 10543 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题。
- Error: (none)

### [PASS] attention_is_all_you_need:en_a1_decoder_layers
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: How many identical layers does the Transformer decoder consist of?
- Expected pages: [3] | Expected any of: ['6', 'N = 6', 'N=6']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3] | citations: 1 | evidence_quotes: 1
- Latency: 3597 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 6
- Error: (none)

### [PASS] attention_is_all_you_need:en_a1_attention_heads
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: How many attention heads does the base Transformer model use?
- Expected pages: [4, 5] | Expected any of: ['8', 'h = 8', 'h=8']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [4, 5] | citations: 1 | evidence_quotes: 1
- Latency: 4424 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The base Transformer model uses 8 attention heads.
- Error: (none)

### [PASS] attention_is_all_you_need:en_a2_dropout_rate
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: What dropout rate does the base model use during training?
- Expected pages: [7, 8] | Expected any of: ['0.1', 'Pdrop']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [8] | citations: 1 | evidence_quotes: 1
- Latency: 4292 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The base model uses a dropout rate of Pdrop = 0.1 during training.
- Error: (none)

### [PASS] attention_is_all_you_need:en_a2_positional_enc
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: How are positional encodings computed in this paper?
- Expected pages: [5, 6] | Expected any of: ['sine', 'cosine', 'sinusoid']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [6] | citations: 1 | evidence_quotes: 1
- Latency: 4178 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Positional encodings are computed using sine and cosine functions of different frequencies. Specifically, for position pos and dimension i: PE(pos, 2i) = sin(pos / 10000^(2i/d_model)) and PE(pos, 2i+1
- Error: (none)

### [PASS] attention_is_all_you_need:en_a3_training_hardware
- Category: A3 / Difficulty: medium / Kind: answerable
- Query: What hardware was used to train the base Transformer model?
- Expected pages: [7] | Expected any of: ['P100', 'GPU']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [7] | citations: 1 | evidence_quotes: 1
- Latency: 4340 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The base Transformer model was trained on one machine with 8 NVIDIA P100 GPUs.
- Error: (none)

### [PASS] attention_is_all_you_need:en_a3_wmt_tasks
- Category: A3 / Difficulty: medium / Kind: answerable
- Query: On which two machine translation tasks is the model evaluated?
- Expected pages: [1, 7, 8] | Expected any of: ['English-to-German', 'English-to-French', 'WMT']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [8] | citations: 1 | evidence_quotes: 2
- Latency: 6283 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The model is evaluated on the WMT 2014 English-to-German translation task and the WMT 2014 English-to-French translation task.
- Error: (none)

### [PASS] attention_is_all_you_need:en_a4_optimizer
- Category: A4 / Difficulty: easy / Kind: answerable
- Query: Which optimizer is used to train the Transformer?
- Expected pages: [7] | Expected any of: ['Adam']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [7] | citations: 1 | evidence_quotes: 1
- Latency: 5365 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The Adam optimizer is used to train the Transformer.
- Error: (none)

### [PASS] attention_is_all_you_need:en_a4_label_smoothing
- Category: A4 / Difficulty: medium / Kind: answerable
- Query: What label smoothing value was used during training?
- Expected pages: [7, 8] | Expected any of: ['0.1', 'ls']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [8] | citations: 1 | evidence_quotes: 1
- Latency: 5177 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The label smoothing value used during training was ϵls = 0.1.
- Error: (none)

### [PASS] attention_is_all_you_need:en_b2_pytorch_code
- Category: B2 / Difficulty: hard / Kind: refusal
- Query: Does this paper provide PyTorch training code for the Transformer?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 10385 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] attention_is_all_you_need:en_b3_nobel
- Category: B2 / Difficulty: hard / Kind: refusal
- Query: Did Ashish Vaswani receive a Nobel Prize for this work?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 11854 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The provided document does not contain any information regarding Ashish Vaswani receiving a Nobel Prize for this work.
- Error: (none)

### [PASS] paper_report:pr_a1_scenarios
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 研究报告面向哪几类文档阅读场景？
- Expected pages: [1] | Expected any of: ['论文', '制度', '方案']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 2843 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 研究报告面向论文、制度和方案文档的阅读场景。
- Error: (none)

### [PASS] paper_report:pr_a2_pipeline
- Category: A2 / Difficulty: easy / Kind: answerable
- Query: 该项目采用的是什么技术路线？
- Expected pages: [1] | Expected any of: ['端云协同']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4133 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 本项目采用端云协同路线。
- Error: (none)

### [PASS] paper_report:pr_b1_finance
- Category: B1 / Difficulty: easy / Kind: refusal
- Query: 该项目的融资情况如何？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: low_confidence | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 9409 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 文档中没有关于该项目融资情况的任何信息。
- Error: (none)

### [PASS] research_brief:rb_a1_name
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 这个产品的名字是什么？
- Expected pages: [1] | Expected any of: ['研答通']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3953 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 研答通
- Error: (none)

### [PASS] research_brief:rb_a1_upload_types
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 产品支持上传哪些文件类型？
- Expected pages: [1] | Expected any of: ['TXT', 'Markdown', 'PDF']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 10516 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 产品支持上传的文件类型包括 TXT、Markdown 和 PDF。
- Error: (none)

### [PASS] research_brief:rb_b1_price
- Category: B1 / Difficulty: easy / Kind: refusal
- Query: 这个产品的商业定价是多少？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: no_match | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 1 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。
- Error: (none)
