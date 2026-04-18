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
| qwen3-235b-a22b-instruct-2507 | True | 3 / 3 | 2 / 2 | 1 / 1 | 4896 | 8352 |
| qwen3-32b | True | 3 / 3 | 2 / 2 | 1 / 1 | 4396 | 7549 |

## Detailed Results

### qwen3-235b-a22b-instruct-2507
#### answerable_research_focus
- Kind: answerable
- Prompt: 这篇论文主要研究了什么问题？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 8352
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 2
- Cited pages: [2, 3]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 2
- Token total: 2481
- Answer preview: 这篇论文主要研究了大语言模型对空间语义的理解程度及其在具体任务中的优劣，基于第四届中文空间语义理解评测任务（SpaCE2024），通过实验分析不同模型的空间语义理解能力，并探讨其能力边界。
- Error: None

#### answerable_rank_accuracy
- Kind: answerable
- Prompt: 作者最终的方法排名和总体准确率分别是多少？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 6329
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 2
- Cited pages: [1, 6]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 2
- Token total: 1963
- Answer preview: 作者最终的方法排名第六，总体准确率为56.20%。
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


### qwen3-32b
#### answerable_research_focus
- Kind: answerable
- Prompt: 这篇论文主要研究了什么问题？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 7549
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [2]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 2351
- Answer preview: 这篇论文主要研究了大语言模型在空间语义理解方面的能力，具体包括其对空间语义的理解程度以及在理解空间语义的具体任务上的优劣。
- Error: None

#### answerable_rank_accuracy
- Kind: answerable
- Prompt: 作者最终的方法排名和总体准确率分别是多少？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 5631
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 1880
- Answer preview: 作者最终的方法排名第六，总体准确率为56.20%。
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
