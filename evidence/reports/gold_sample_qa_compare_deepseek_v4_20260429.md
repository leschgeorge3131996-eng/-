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
| qwen3-235b-a22b-instruct-2507 | True | 3 / 3 | 2 / 2 | 1 / 1 | 5047 | 8021 |
| deepseek-v4-flash | True | 3 / 3 | 2 / 2 | 1 / 1 | 4210 | 6655 |
| deepseek-v4-pro | True | 3 / 3 | 2 / 2 | 1 / 1 | 8960 | 15087 |

## Detailed Results

### qwen3-235b-a22b-instruct-2507
#### answerable_research_focus
- Kind: answerable
- Prompt: 这篇论文主要研究了什么问题？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 7113
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
- Answer preview: 这篇论文主要研究了大语言模型对空间语义的理解程度及其在具体任务中的优劣，基于第四届中文空间语义理解评测任务（SpaCE2024）进行实验分析，探讨大模型在空间语义理解方面的能力边界。
- Error: None

#### answerable_rank_accuracy
- Kind: answerable
- Prompt: 作者最终的方法排名和总体准确率分别是多少？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 8021
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 2180
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


### deepseek-v4-flash
#### answerable_research_focus
- Kind: answerable
- Prompt: 这篇论文主要研究了什么问题？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 6655
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1, 2]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 2498
- Answer preview: 本研究主要探究大语言模型对空间语义的理解程度，以及不同模型在理解空间语义的具体任务上各自的优劣。
- Error: None

#### answerable_rank_accuracy
- Kind: answerable
- Prompt: 作者最终的方法排名和总体准确率分别是多少？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 5965
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 1963
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


### deepseek-v4-pro
#### answerable_research_focus
- Kind: answerable
- Prompt: 这篇论文主要研究了什么问题？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 11785
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1, 2]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 2478
- Answer preview: 这篇论文主要研究大模型对空间语义的理解程度，以及在理解空间语义的具体任务上大模型各自的优劣。
- Error: None

#### answerable_rank_accuracy
- Kind: answerable
- Prompt: 作者最终的方法排名和总体准确率分别是多少？
- Success: True
- Passed: True
- Outcome: answered
- Latency (ms): 15087
- Route tier: task_specific
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Citation count: 1
- Cited pages: [1]
- Page fetch OK: True
- Render OK: True
- Evidence quote count: 1
- Token total: 2108
- Answer preview: 作者的方法最终排名第六，总体准确率为56.20%。
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
