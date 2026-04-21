# Extended Evaluation Report — EXTENDED_EVAL_V1

Generated: 2026-04-21 23:12:41

## Overall

- Total cases: **51**
- Passed: **46**
- Overall pass rate: **90.2%**
- Answerable pass rate: **88.4%**
- Refusal precision: **100.0%**
- Citation accuracy (answerable page-hit): **88.4%**
- Declaration rate (evidence_mode=declared on answerable): **88.4%**
- Avg latency: **5484 ms**

## By Category

| Category | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| A1 | 15 | 13 | 86.7% | 5294 |
| A2 | 9 | 9 | 100.0% | 7675 |
| A3 | 7 | 6 | 85.7% | 6871 |
| A4 | 7 | 6 | 85.7% | 5475 |
| A5 | 5 | 4 | 80.0% | 4799 |
| B1 | 5 | 5 | 100.0% | 2318 |
| B2 | 3 | 3 | 100.0% | 3064 |

## By Difficulty

| Difficulty | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| easy | 24 | 22 | 91.7% | 4921 |
| hard | 8 | 7 | 87.5% | 4148 |
| medium | 19 | 17 | 89.5% | 6758 |

## By Document

| Doc | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| attention_is_all_you_need | 20 | 18 | 90.0% | 5240 |
| chinese_llm_spatial_eval | 25 | 23 | 92.0% | 6533 |
| paper_report | 3 | 3 | 100.0% | 2670 |
| research_brief | 3 | 2 | 66.7% | 1184 |

## Case Detail

### [PASS] chinese_llm_spatial_eval:zh_a1_accuracy
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 本研究的总体准确率得分是多少？
- Expected pages: [1, 5, 6] | Expected any of: ['56.20', '56.2']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5, 6] | citations: 1 | evidence_quotes: 1
- Latency: 5316 ms
- Fail reason: (none)
- Answer snippet: 本研究的总体准确率得分为56.20%。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a1_best_model
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 在 1-shot 通用提示词策略下，哪一个模型的表现最好？
- Expected pages: [1, 5, 6] | Expected any of: ['ERNIE-4', 'ERNIE']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5, 6] | citations: 1 | evidence_quotes: 1
- Latency: 5634 ms
- Fail reason: (none)
- Answer snippet: 在 1-shot 通用提示词策略下，ERNIE-4 的表现最好，得分为 53.88。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a1_authors
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 论文的作者来自哪所高校？
- Expected pages: [1] | Expected any of: ['北京师范大学', 'Beijing Normal']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3861 ms
- Fail reason: (none)
- Answer snippet: 论文的作者来自北京师范大学。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a2_two_questions
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: 本研究试图回答的两个核心问题是什么？
- Expected pages: [2] | Expected any of: ['理解的程度', '具体分类', '哪些']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1, 2] | citations: 1 | evidence_quotes: 1
- Latency: 4359 ms
- Fail reason: (none)
- Answer snippet: 本研究试图回答的两个核心问题是：1）大模型对空间语义的理解程度如何？2）在理解空间语义的具体任务上，大模型各有哪些优劣？
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a2_prompt_strategies
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: 论文中提到了哪几种提示词策略？它们的区别是什么？
- Expected pages: [1, 5, 6] | Expected any of: ['通用', '工作流', '思维链']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1, 5, 6] | citations: 2 | evidence_quotes: 0
- Latency: 19830 ms
- Fail reason: (none)
- Answer snippet: 论文中提到了三种提示词策略：普通提示（Vanilla Prompt）、工作流（Workflow）和思维链（Chain of Thought, CoT）。在提示样本构建上，普通提示词和工作流提示词都采用了0-shot、1-shot、3-shot的方式，而思维链提示词仅采用1-shot。对于思维链提示词，研究参考了Wei (2022)的提示词设计，将其改为“想法”和“答案”两部分，以使输出更结构化，便
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a3_subtasks
- Category: A3 / Difficulty: medium / Kind: answerable
- Query: SPaCE 2024 数据集包含哪几个子任务？
- Expected pages: [4] | Expected any of: ['实体识别', '角色识别', '异常识别', '方位', '同义']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3, 4] | citations: 1 | evidence_quotes: 1
- Latency: 9384 ms
- Fail reason: (none)
- Answer snippet: SPaCE 2024数据集包含五个子任务：空间信息实体识别、空间信息角色识别、空间信息异常识别、空间方位信息推理和空间异形同义识别。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a4_method_summary
- Category: A4 / Difficulty: medium / Kind: answerable
- Query: 请简要总结本论文采用的研究方法。
- Expected pages: [1, 2, 5, 6] | Expected any of: ['提示词', '大语言模型', '空间语义']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1, 2] | citations: 1 | evidence_quotes: 1
- Latency: 5260 ms
- Fail reason: (none)
- Answer snippet: 本研究基于第四届中文空间语义理解评测任务（SpaCE2024），首先介绍空间语义评测的背景和相关研究，然后通过实验分析不同模型的空间语义理解能力，最后对实验结果进行讨论和分析，以探究大模型对空间语义的理解程度及其在具体任务上的优劣。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a4_ranking
- Category: A4 / Difficulty: easy / Kind: answerable
- Query: 作者团队在比赛中最终取得了什么名次？
- Expected pages: [1] | Expected any of: ['第六', '六']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4207 ms
- Fail reason: (none)
- Answer snippet: 作者团队在比赛中最终取得了第六名。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a5_train_count
- Category: A5 / Difficulty: hard / Kind: answerable
- Query: SPaCE 2024 数据集训练集样本总数是多少？
- Expected pages: [4] | Expected any of: ['4483']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3, 4] | citations: 1 | evidence_quotes: 1
- Latency: 5596 ms
- Fail reason: (none)
- Answer snippet: SPaCE 2024 数据集训练集样本总数是4483。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_b1_quantum
- Category: B1 / Difficulty: easy / Kind: refusal
- Query: 量子纠缠的物理原理是什么？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 3175 ms
- Fail reason: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a1_conf_name
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 本论文发表在哪个学术会议上？
- Expected pages: [1] | Expected any of: ['CCL', '中国计算语言学']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1, 2, 6, 7, 8, 11] | citations: 4 | evidence_quotes: 1
- Latency: 6835 ms
- Fail reason: (none)
- Answer snippet: 本论文发表在第二十三届中国计算语言学大会。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a1_temperature
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 实验中模型的 temperature 参数设置为多少？
- Expected pages: [5] | Expected any of: ['0.1']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5] | citations: 1 | evidence_quotes: 1
- Latency: 5159 ms
- Fail reason: (none)
- Answer snippet: 实验中模型的 temperature 参数设置为0.1。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a1_author_count
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 本论文共有几位作者？
- Expected pages: [1] | Expected any of: ['3', '三']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4936 ms
- Fail reason: (none)
- Answer snippet: 本论文共有三位作者。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a1_school_department
- Category: A1 / Difficulty: medium / Kind: answerable
- Query: 作者所在的具体学院是哪一所？
- Expected pages: [1] | Expected any of: ['国际中文教育学院']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 6289 ms
- Fail reason: (none)
- Answer snippet: 国际中文教育学院
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a2_ernie_weakness
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: ERNIE-4 在哪一类任务上表现最弱？
- Expected pages: [5, 6, 7, 8, 9] | Expected any of: ['空间推理', '推理']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5, 6] | citations: 2 | evidence_quotes: 1
- Latency: 7750 ms
- Fail reason: (none)
- Answer snippet: ERNIE-4 在空间推理任务上表现最弱。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a2_glm4_best
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: GLM-4 在哪种提示词配置下验证集表现最好？
- Expected pages: [6] | Expected any of: ['工作流', '1-shot', '53.14']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5, 6] | citations: 1 | evidence_quotes: 1
- Latency: 8654 ms
- Fail reason: (none)
- Answer snippet: GLM-4 在1-shot的工作流提示词配置下验证集表现最好，准确率为53.14%。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a3_models_count
- Category: A3 / Difficulty: easy / Kind: answerable
- Query: 本研究共评测了多少个大模型？
- Expected pages: [4, 5, 6] | Expected any of: ['六个', '6']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5, 6] | citations: 1 | evidence_quotes: 1
- Latency: 11306 ms
- Fail reason: (none)
- Answer snippet: 本研究共评测了6个大模型。
- Error: (none)

### [FAIL] chinese_llm_spatial_eval:zh_a3_opensource
- Category: A3 / Difficulty: medium / Kind: answerable
- Query: 评测的模型中哪些是开源模型？
- Expected pages: [4, 5, 6] | Expected any of: ['Qwen', 'Deepseek']
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 3893 ms
- Fail reason: pages [] ∩ [4, 5, 6] empty; evidence_mode=none; answer missing any of ['Qwen', 'Deepseek']
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a3_context_max
- Category: A3 / Difficulty: medium / Kind: answerable
- Query: 评测模型支持的最大上下文长度是多少？
- Expected pages: [4] | Expected any of: ['12.8', '128']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3, 4] | citations: 1 | evidence_quotes: 1
- Latency: 7754 ms
- Fail reason: (none)
- Answer snippet: 评测模型支持的最大上下文长度是12.8万。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a4_eval_metric
- Category: A4 / Difficulty: easy / Kind: answerable
- Query: 本研究采用的评测指标是什么？
- Expected pages: [5] | Expected any of: ['准确率', 'Accuracy']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5] | citations: 1 | evidence_quotes: 1
- Latency: 9592 ms
- Fail reason: (none)
- Answer snippet: 本研究采用的评测指标是准确率（Accuracy），即模型答对的题目数量占所有题目的百分比。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a4_cot_sample_source
- Category: A4 / Difficulty: medium / Kind: answerable
- Query: 思维链提示词的样本思考过程由什么生成？
- Expected pages: [5] | Expected any of: ['GPT-4']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [4, 5] | citations: 1 | evidence_quotes: 1
- Latency: 7105 ms
- Fail reason: (none)
- Answer snippet: 思维链提示词的样本思考过程由GPT-4生成。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a5_test_count
- Category: A5 / Difficulty: hard / Kind: answerable
- Query: SPaCE 2024 数据集测试集样本总数是多少？
- Expected pages: [4] | Expected any of: ['4530']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3, 4] | citations: 1 | evidence_quotes: 1
- Latency: 3958 ms
- Fail reason: (none)
- Answer snippet: SPaCE 2024数据集测试集样本总数是4530。
- Error: (none)

### [FAIL] chinese_llm_spatial_eval:zh_a5_val_count
- Category: A5 / Difficulty: hard / Kind: answerable
- Query: SPaCE 2024 数据集验证集样本总数是多少？
- Expected pages: [4] | Expected any of: ['1210']
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 4951 ms
- Fail reason: pages [] ∩ [4] empty; evidence_mode=none; answer missing any of ['1210']
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_a5_study_period
- Category: A5 / Difficulty: hard / Kind: answerable
- Query: 本研究的开展日期是哪段时间？
- Expected pages: [4, 5] | Expected any of: ['2024年5月']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [4] | citations: 1 | evidence_quotes: 1
- Latency: 5143 ms
- Fail reason: (none)
- Answer snippet: 本研究的开展日期为2024年5月1日至5月17日。
- Error: (none)

### [PASS] chinese_llm_spatial_eval:zh_b1_weather
- Category: B1 / Difficulty: easy / Kind: refusal
- Query: 北京今天的天气怎么样？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 3382 ms
- Fail reason: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] attention_is_all_you_need:en_a1_encoder_layers
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: How many identical layers does the Transformer encoder consist of?
- Expected pages: [3] | Expected any of: ['6', 'N = 6', 'N=6']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3] | citations: 1 | evidence_quotes: 1
- Latency: 4290 ms
- Fail reason: (none)
- Answer snippet: The Transformer encoder consists of 6 identical layers.
- Error: (none)

### [PASS] attention_is_all_you_need:en_a1_first_authors
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: Who are the first two listed authors of this paper?
- Expected pages: [1] | Expected any of: ['Vaswani', 'Shazeer']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4941 ms
- Fail reason: (none)
- Answer snippet: The first two listed authors of this paper are Ashish Vaswani and Noam Shazeer.
- Error: (none)

### [PASS] attention_is_all_you_need:en_a1_arxiv_id
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: What is the arXiv identifier of this paper?
- Expected pages: [1] | Expected any of: ['1706.03762']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4246 ms
- Fail reason: (none)
- Answer snippet: The arXiv identifier of this paper is arXiv:1706.03762v7.
- Error: (none)

### [PASS] attention_is_all_you_need:en_a2_why_no_recurrence
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: Why does the Transformer architecture avoid recurrence entirely?
- Expected pages: [2, 3] | Expected any of: ['parallel', 'sequential', 'long', 'dependencies']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1, 2] | citations: 2 | evidence_quotes: 2
- Latency: 7237 ms
- Fail reason: (none)
- Answer snippet: The Transformer architecture avoids recurrence entirely because it relies solely on an attention mechanism to draw global dependencies between input and output, dispensing with recurrence and convolut
- Error: (none)

### [PASS] attention_is_all_you_need:en_a2_scaling_reason
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: Why is the dot product scaled by the square root of d_k in scaled dot-product attention?
- Expected pages: [4] | Expected any of: ['gradient', 'magnitude', 'large', 'softmax']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [4] | citations: 1 | evidence_quotes: 1
- Latency: 5226 ms
- Fail reason: (none)
- Answer snippet: The dot product is scaled by the square root of d_k to prevent the softmax function from having extremely small gradients due to large magnitude dot products for large values of d_k.
- Error: (none)

### [PASS] attention_is_all_you_need:en_a3_complexity_compare
- Category: A3 / Difficulty: medium / Kind: answerable
- Query: Compare the per-layer computational complexity of self-attention and recurrent layers as shown in the paper.
- Expected pages: [6] | Expected any of: ['n^2', 'n2', 'O(n', 'sequence length']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5, 6] | citations: 1 | evidence_quotes: 2
- Latency: 5330 ms
- Fail reason: (none)
- Answer snippet: The per-layer computational complexity of self-attention layers is O(n²·d), whereas that of recurrent layers is O(n·d²), according to the paper.
- Error: (none)

### [FAIL] attention_is_all_you_need:en_a4_contributions
- Category: A4 / Difficulty: medium / Kind: answerable
- Query: What are the main contributions of this paper?
- Expected pages: [1, 2, 3] | Expected any of: ['Transformer', 'attention', 'sequence']
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 3174 ms
- Fail reason: pages [] ∩ [1, 2, 3] empty; evidence_mode=none; answer missing any of ['Transformer', 'attention', 'sequence']
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] attention_is_all_you_need:en_a5_conv_path_length
- Category: A5 / Difficulty: hard / Kind: answerable
- Query: According to Table 1, what is the maximum path length for convolutional layers?
- Expected pages: [6] | Expected any of: ['log', 'O(log']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [5, 6] | citations: 1 | evidence_quotes: 1
- Latency: 4348 ms
- Fail reason: (none)
- Answer snippet: The maximum path length for convolutional layers is O(logk(n)).
- Error: (none)

### [PASS] attention_is_all_you_need:en_b1_everest
- Category: B1 / Difficulty: easy / Kind: refusal
- Query: What is the height of Mount Everest?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 5031 ms
- Fail reason: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] attention_is_all_you_need:en_b2_vaswani_affiliation_now
- Category: B2 / Difficulty: hard / Kind: refusal
- Query: What is Ashish Vaswani's current employer in 2026?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 3914 ms
- Fail reason: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] attention_is_all_you_need:en_a1_decoder_layers
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: How many identical layers does the Transformer decoder consist of?
- Expected pages: [3] | Expected any of: ['6', 'N = 6', 'N=6']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [3] | citations: 1 | evidence_quotes: 1
- Latency: 16309 ms
- Fail reason: (none)
- Answer snippet: The Transformer decoder consists of 6 identical layers.
- Error: (none)

### [FAIL] attention_is_all_you_need:en_a1_attention_heads
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: How many attention heads does the base Transformer model use?
- Expected pages: [4, 5] | Expected any of: ['8', 'h = 8', 'h=8']
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 4076 ms
- Fail reason: pages [] ∩ [4, 5] empty; evidence_mode=none; answer missing any of ['8', 'h = 8', 'h=8']
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] attention_is_all_you_need:en_a2_dropout_rate
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: What dropout rate does the base model use during training?
- Expected pages: [7, 8] | Expected any of: ['0.1', 'Pdrop']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [8] | citations: 1 | evidence_quotes: 1
- Latency: 6498 ms
- Fail reason: (none)
- Answer snippet: The base model uses a dropout rate of Pdrop = 0.1 during training.
- Error: (none)

### [PASS] attention_is_all_you_need:en_a2_positional_enc
- Category: A2 / Difficulty: medium / Kind: answerable
- Query: How are positional encodings computed in this paper?
- Expected pages: [5, 6] | Expected any of: ['sine', 'cosine', 'sinusoid']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [6] | citations: 1 | evidence_quotes: 1
- Latency: 5493 ms
- Fail reason: (none)
- Answer snippet: In this paper, positional encodings are computed using sine and cosine functions of different frequencies. Specifically, PE(pos,2i) = sin(pos/10000^(2i/d_model)) and PE(pos,2i+1) = cos(pos/10000^(2i/d
- Error: (none)

### [PASS] attention_is_all_you_need:en_a3_training_hardware
- Category: A3 / Difficulty: medium / Kind: answerable
- Query: What hardware was used to train the base Transformer model?
- Expected pages: [7] | Expected any of: ['P100', 'GPU']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [7] | citations: 1 | evidence_quotes: 1
- Latency: 3766 ms
- Fail reason: (none)
- Answer snippet: The base Transformer model was trained on one machine with 8 NVIDIA P100 GPUs.
- Error: (none)

### [PASS] attention_is_all_you_need:en_a3_wmt_tasks
- Category: A3 / Difficulty: medium / Kind: answerable
- Query: On which two machine translation tasks is the model evaluated?
- Expected pages: [1, 7, 8] | Expected any of: ['English-to-German', 'English-to-French', 'WMT']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1, 8] | citations: 2 | evidence_quotes: 1
- Latency: 6666 ms
- Fail reason: (none)
- Answer snippet: The model is evaluated on the WMT 2014 English-to-German and English-to-French translation tasks.
- Error: (none)

### [PASS] attention_is_all_you_need:en_a4_optimizer
- Category: A4 / Difficulty: easy / Kind: answerable
- Query: Which optimizer is used to train the Transformer?
- Expected pages: [7] | Expected any of: ['Adam']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [7] | citations: 1 | evidence_quotes: 1
- Latency: 4252 ms
- Fail reason: (none)
- Answer snippet: The Adam optimizer is used to train the Transformer.
- Error: (none)

### [PASS] attention_is_all_you_need:en_a4_label_smoothing
- Category: A4 / Difficulty: medium / Kind: answerable
- Query: What label smoothing value was used during training?
- Expected pages: [7, 8] | Expected any of: ['0.1', 'ls']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [8] | citations: 1 | evidence_quotes: 1
- Latency: 4738 ms
- Fail reason: (none)
- Answer snippet: The label smoothing value used during training was ϵls = 0.1.
- Error: (none)

### [PASS] attention_is_all_you_need:en_b2_pytorch_code
- Category: B2 / Difficulty: hard / Kind: refusal
- Query: Does this paper provide PyTorch training code for the Transformer?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 2165 ms
- Fail reason: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] attention_is_all_you_need:en_b3_nobel
- Category: B2 / Difficulty: hard / Kind: refusal
- Query: Did Ashish Vaswani receive a Nobel Prize for this work?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 3115 ms
- Fail reason: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] paper_report:pr_a1_scenarios
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 研究报告面向哪几类文档阅读场景？
- Expected pages: [1] | Expected any of: ['论文', '制度', '方案']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3975 ms
- Fail reason: (none)
- Answer snippet: 研究报告面向论文、制度和方案文档的阅读场景。
- Error: (none)

### [PASS] paper_report:pr_a2_pipeline
- Category: A2 / Difficulty: easy / Kind: answerable
- Query: 该项目采用的是什么技术路线？
- Expected pages: [1] | Expected any of: ['端云协同']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4034 ms
- Fail reason: (none)
- Answer snippet: 该项目采用的是端云协同路线。
- Error: (none)

### [PASS] paper_report:pr_b1_finance
- Category: B1 / Difficulty: easy / Kind: refusal
- Query: 该项目的融资情况如何？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: low_confidence | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 1 ms
- Fail reason: (none)
- Answer snippet: 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。
- Error: (none)

### [FAIL] research_brief:rb_a1_name
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 这个产品的名字是什么？
- Expected pages: [1] | Expected any of: ['研答通']
- Outcome: refused | retrieval_status: no_match | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 9 ms
- Fail reason: pages [] ∩ [1] empty; evidence_mode=none; answer missing any of ['研答通']
- Answer snippet: 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。
- Error: (none)

### [PASS] research_brief:rb_a1_upload_types
- Category: A1 / Difficulty: easy / Kind: answerable
- Query: 产品支持上传哪些文件类型？
- Expected pages: [1] | Expected any of: ['TXT', 'Markdown', 'PDF']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3542 ms
- Fail reason: (none)
- Answer snippet: 产品支持上传 TXT、Markdown、PDF 文件类型。
- Error: (none)

### [PASS] research_brief:rb_b1_price
- Category: B1 / Difficulty: easy / Kind: refusal
- Query: 这个产品的商业定价是多少？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: no_match | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 1 ms
- Fail reason: (none)
- Answer snippet: 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。
- Error: (none)
