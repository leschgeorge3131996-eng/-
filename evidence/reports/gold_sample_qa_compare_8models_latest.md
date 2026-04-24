# Gold Sample QA Compare

- Candidate ID: gold_sample_candidate_20260418
- Scenario: 中文学术论文 PDF / Gold Sample Candidate
- Document: evidence/samples/chinese_llm_spatial_eval.pdf
- Response detail level: balanced

## Candidate Prompts
### answerable_research_focus
- Kind: answerable
- Prompt: 这篇论文主要研究了什么问题？

### answerable_rank_accuracy
- Kind: answerable
- Prompt: 作者最终的方法排名和总体准确率分别是多少？

### refusal_jupiter_moons
- Kind: refusal
- Prompt: 木星有几颗卫星？

## Model Summary

| Model | All Passed | Passed / Total | Answerable Passed | Refusal Passed | Avg Latency (ms) | Max Latency (ms) |
| --- | --- | --- | --- | --- | ---: | ---: |
| qwen3-235b-a22b-instruct-2507 | True | 3 / 3 | 2 / 2 | 1 / 1 | 2638 | 4104 |
| qwen3-32b | True | 3 / 3 | 2 / 2 | 1 / 1 | 3694 | 7248 |
| qwen3-next-80b-a3b-instruct | True | 3 / 3 | 2 / 2 | 1 / 1 | 1840 | 3072 |
| deepseek-v3.2 | True | 3 / 3 | 2 / 2 | 1 / 1 | 4119 | 8092 |
| deepseek-v3.2-thinking | True | 3 / 3 | 2 / 2 | 1 / 1 | 16942 | 29079 |
| glm-5.1 | True | 3 / 3 | 2 / 2 | 1 / 1 | 7679 | 13100 |
| kimi-k2.6 | True | 3 / 3 | 2 / 2 | 1 / 1 | 25235 | 52135 |
| minimax-m2.7 | True | 3 / 3 | 2 / 2 | 1 / 1 | 7100 | 13193 |

## Detailed Results

### qwen3-235b-a22b-instruct-2507
#### answerable_research_focus
- Kind: answerable
- Prompt: 这篇论文主要研究了什么问题？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 3802
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1, 2]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 2783
- Answer preview: 这篇论文主要研究了大语言模型对空间语义的理解程度以及在具体任务中的优劣，基于第四届中文空间语义理解评测任务（SpaCE2024）进行实验分析，探讨大模型在空间语义理解方面的能力边界。
- Error: None

#### answerable_rank_accuracy
- Kind: answerable
- Prompt: 作者最终的方法排名和总体准确率分别是多少？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 4104
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 2182
- Answer preview: 作者最终的方法排名第六，总体准确率得分为56.20%。
- Error: None

#### refusal_jupiter_moons
- Kind: refusal
- Prompt: 木星有几颗卫星？
- Success: True
- Passed: True
- Outcome: refused
- Latency (ms): 9
- Route tier: none
- Route reason: retrieval_no_match
- Cache hit: False
- Retrieval status: no_match
- Citation count: 0
- Cited pages: []
- Page fetch OK: None
- Render OK: None
- Evidence quote count: 0
- Token total: None
- Answer preview: 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。
- Error: None


### qwen3-32b
#### answerable_research_focus
- Kind: answerable
- Prompt: 这篇论文主要研究了什么问题？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 7248
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1, 2]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 2758
- Answer preview: 这篇论文主要研究了大语言模型对空间语义的理解程度，以及在理解空间语义的具体任务上，大模型的优劣。
- Error: None

#### answerable_rank_accuracy
- Kind: answerable
- Prompt: 作者最终的方法排名和总体准确率分别是多少？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 3826
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 2184
- Answer preview: 作者最终的方法排名第六，总体准确率为56.20%。
- Error: None

#### refusal_jupiter_moons
- Kind: refusal
- Prompt: 木星有几颗卫星？
- Success: True
- Passed: True
- Outcome: refused
- Latency (ms): 9
- Route tier: none
- Route reason: retrieval_no_match
- Cache hit: False
- Retrieval status: no_match
- Citation count: 0
- Cited pages: []
- Page fetch OK: None
- Render OK: None
- Evidence quote count: 0
- Token total: None
- Answer preview: 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。
- Error: None


### qwen3-next-80b-a3b-instruct
#### answerable_research_focus
- Kind: answerable
- Prompt: 这篇论文主要研究了什么问题？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 3072
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1, 2]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 2824
- Answer preview: 这篇论文主要研究大模型对空间语义的理解程度，以及在理解空间语义的具体任务上各模型的优劣。研究基于第四届中文空间语义理解评测任务（SpaCE2024），通过实验分析不同模型的空间语义理解能力，以了解大模型在空间语义理解方面的能力边界。
- Error: None

#### answerable_rank_accuracy
- Kind: answerable
- Prompt: 作者最终的方法排名和总体准确率分别是多少？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 2439
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 2
- Cited pages: [1, 5, 6]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 2
- Token total: 2256
- Answer preview: 作者最终的方法排名第六，总体准确率为56.20%。
- Error: None

#### refusal_jupiter_moons
- Kind: refusal
- Prompt: 木星有几颗卫星？
- Success: True
- Passed: True
- Outcome: refused
- Latency (ms): 9
- Route tier: none
- Route reason: retrieval_no_match
- Cache hit: False
- Retrieval status: no_match
- Citation count: 0
- Cited pages: []
- Page fetch OK: None
- Render OK: None
- Evidence quote count: 0
- Token total: None
- Answer preview: 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。
- Error: None


### deepseek-v3.2
#### answerable_research_focus
- Kind: answerable
- Prompt: 这篇论文主要研究了什么问题？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 8092
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1, 2]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 2449
- Answer preview: 这篇论文主要研究大语言模型对空间语义的理解能力。具体而言，它基于第四届中文空间语义理解评测任务（SpaCE2024），旨在探究两个核心问题：1）大模型对空间语义的理解程度如何？2）在理解空间语义的具体任务上，大模型各有哪些优劣？研究通过实验分析不同模型的空间语义理解能力，以更好地了解大模型在空间语义理解方面的能力边界。
- Error: None

#### answerable_rank_accuracy
- Kind: answerable
- Prompt: 作者最终的方法排名和总体准确率分别是多少？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 4258
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 1881
- Answer preview: 根据文档，作者最终的方法排名第六，总体准确率得分为56.20%。
- Error: None

#### refusal_jupiter_moons
- Kind: refusal
- Prompt: 木星有几颗卫星？
- Success: True
- Passed: True
- Outcome: refused
- Latency (ms): 8
- Route tier: none
- Route reason: retrieval_no_match
- Cache hit: False
- Retrieval status: no_match
- Citation count: 0
- Cited pages: []
- Page fetch OK: None
- Render OK: None
- Evidence quote count: 0
- Token total: None
- Answer preview: 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。
- Error: None


### deepseek-v3.2-thinking
#### answerable_research_focus
- Kind: answerable
- Prompt: 这篇论文主要研究了什么问题？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 29079
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1, 2]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 3231
- Answer preview: 这篇论文主要研究大语言模型对空间语义的理解程度，以及它们在空间语义理解具体任务上的优劣，基于第四届中文空间语义理解评测任务（SpaCE2024）。
- Error: None

#### answerable_rank_accuracy
- Kind: answerable
- Prompt: 作者最终的方法排名和总体准确率分别是多少？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 21741
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 2550
- Answer preview: 作者的方法在评测中排名第六，总体准确率为56.20%。
- Error: None

#### refusal_jupiter_moons
- Kind: refusal
- Prompt: 木星有几颗卫星？
- Success: True
- Passed: True
- Outcome: refused
- Latency (ms): 8
- Route tier: none
- Route reason: retrieval_no_match
- Cache hit: False
- Retrieval status: no_match
- Citation count: 0
- Cited pages: []
- Page fetch OK: None
- Render OK: None
- Evidence quote count: 0
- Token total: None
- Answer preview: 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。
- Error: None


### glm-5.1
#### answerable_research_focus
- Kind: answerable
- Prompt: 这篇论文主要研究了什么问题？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 13100
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1, 2]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 2826
- Answer preview: 这篇论文主要研究了以下两个问题：1）大模型对空间语义的理解程度如何？2）在理解空间语义的具体任务上，大模型各有哪些优劣？旨在更好地了解大模型在空间语义理解方面的能力边界。
- Error: None

#### answerable_rank_accuracy
- Kind: answerable
- Prompt: 作者最终的方法排名和总体准确率分别是多少？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 9929
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 2202
- Answer preview: 作者最终的方法排名为第六，总体准确率为56.20%。
- Error: None

#### refusal_jupiter_moons
- Kind: refusal
- Prompt: 木星有几颗卫星？
- Success: True
- Passed: True
- Outcome: refused
- Latency (ms): 9
- Route tier: none
- Route reason: retrieval_no_match
- Cache hit: False
- Retrieval status: no_match
- Citation count: 0
- Cited pages: []
- Page fetch OK: None
- Render OK: None
- Evidence quote count: 0
- Token total: None
- Answer preview: 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。
- Error: None


### kimi-k2.6
#### answerable_research_focus
- Kind: answerable
- Prompt: 这篇论文主要研究了什么问题？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 52135
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1, 2]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 2
- Token total: 2903
- Answer preview: 这篇论文基于第四届中文空间语义理解评测任务（SpaCE2024），主要探究两个问题：1）大模型对空间语义的理解程度如何；2）在理解空间语义的具体任务上，大模型各有哪些优劣。研究通过实验分析不同模型的空间语义理解能力，并对实验结果进行讨论和分析，以更好地了解大模型在空间语义理解方面的能力边界。
- Error: None

#### answerable_rank_accuracy
- Kind: answerable
- Prompt: 作者最终的方法排名和总体准确率分别是多少？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 23561
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 2165
- Answer preview: 作者最终的方法排名第六，总体准确率得分为56.20%。
- Error: None

#### refusal_jupiter_moons
- Kind: refusal
- Prompt: 木星有几颗卫星？
- Success: True
- Passed: True
- Outcome: refused
- Latency (ms): 10
- Route tier: none
- Route reason: retrieval_no_match
- Cache hit: False
- Retrieval status: no_match
- Citation count: 0
- Cited pages: []
- Page fetch OK: None
- Render OK: None
- Evidence quote count: 0
- Token total: None
- Answer preview: 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。
- Error: None


### minimax-m2.7
#### answerable_research_focus
- Kind: answerable
- Prompt: 这篇论文主要研究了什么问题？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 8099
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1, 2]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 2
- Token total: 2589
- Answer preview: 这篇论文主要研究了以下问题：1）大语言模型对空间语义的理解程度如何？2）在理解空间语义的具体任务上，大语言模型各有哪些优劣？研究基于第四届中文空间语义理解评测任务（SpaCE2024），通过实验分析不同模型的空间语义理解能力，以更好地了解大模型在空间语义理解方面的能力边界。
- Error: None

#### answerable_rank_accuracy
- Kind: answerable
- Prompt: 作者最终的方法排名和总体准确率分别是多少？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 13193
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 1884
- Answer preview: 作者最终的方法排名第六，总体准确率为56.20%。
- Error: None

#### refusal_jupiter_moons
- Kind: refusal
- Prompt: 木星有几颗卫星？
- Success: True
- Passed: True
- Outcome: refused
- Latency (ms): 9
- Route tier: none
- Route reason: retrieval_no_match
- Cache hit: False
- Retrieval status: no_match
- Citation count: 0
- Cited pages: []
- Page fetch OK: None
- Render OK: None
- Evidence quote count: 0
- Token total: None
- Answer preview: 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。
- Error: None
