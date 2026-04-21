# Sample Replay Report

## gold_sample_candidate_20260418:answerable_research_focus / ask
- Scenario: 中文学术论文 PDF / Gold Sample Candidate
- File: evidence/samples/chinese_llm_spatial_eval.pdf
- Input: 这篇论文主要研究了什么问题？
- Response detail level: balanced
- Success: True
- Outcome: answered
- Latency (ms): 4986
- Model: qwen3-235b-a22b-instruct-2507
- Route tier: task_specific
- Route model: qwen3-235b-a22b-instruct-2507
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Used chunk count: 1
- Evidence quote count: 1
- Citation count: 1
- Source chunk count: 0
- Error: None

## gold_sample_candidate_20260418:answerable_rank_accuracy / ask
- Scenario: 中文学术论文 PDF / Gold Sample Candidate
- File: evidence/samples/chinese_llm_spatial_eval.pdf
- Input: 作者最终的方法排名和总体准确率分别是多少？
- Response detail level: balanced
- Success: True
- Outcome: answered
- Latency (ms): 3371
- Model: qwen3-235b-a22b-instruct-2507
- Route tier: task_specific
- Route model: qwen3-235b-a22b-instruct-2507
- Route reason: configured_ask_model
- Cache hit: False
- Retrieval status: matched
- Used chunk count: 1
- Evidence quote count: 1
- Citation count: 1
- Source chunk count: 0
- Error: None

## gold_sample_candidate_20260418:refusal_jupiter_moons / ask
- Scenario: 中文学术论文 PDF / Gold Sample Candidate
- File: evidence/samples/chinese_llm_spatial_eval.pdf
- Input: 木星有几颗卫星？
- Response detail level: balanced
- Success: True
- Outcome: refused
- Latency (ms): 9
- Model: retrieval_gate
- Route tier: none
- Route model: None
- Route reason: retrieval_no_match
- Cache hit: False
- Retrieval status: no_match
- Used chunk count: 0
- Evidence quote count: 0
- Citation count: 0
- Source chunk count: 0
- Error: None
