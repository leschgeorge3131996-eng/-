# Extended Evaluation Report — HOLDOUT_EVAL_V3_20260429

Generated: 2026-04-29 22:46:22

## Overall

- Total cases: **75**
- Passed: **73**
- Overall pass rate: **97.3%**
- Answerable pass rate: **98.6%**
- Refusal precision: **80.0%**
- Citation accuracy (answerable page-hit): **100.0%**
- Declaration rate (evidence_mode=declared on answerable): **100.0%**
- Avg latency: **5290 ms**

## By Category

| Category | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| V3_BOUNDARY | 4 | 4 | 100.0% | 5097 |
| V3_DATE | 6 | 6 | 100.0% | 4426 |
| V3_FACT | 19 | 19 | 100.0% | 5004 |
| V3_NUMERIC | 17 | 17 | 100.0% | 4791 |
| V3_REASONING | 24 | 23 | 95.8% | 5824 |
| V3_REFUSAL | 5 | 4 | 80.0% | 6704 |

## By Difficulty

| Difficulty | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| easy | 39 | 39 | 100.0% | 4757 |
| hard | 19 | 18 | 94.7% | 5767 |
| medium | 17 | 16 | 94.1% | 5980 |

## By Document

| Doc | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| campus_workshop_v3 | 15 | 13 | 86.7% | 4897 |
| incident_review_v3 | 15 | 15 | 100.0% | 4848 |
| lab_experiment_v3 | 15 | 15 | 100.0% | 5356 |
| orion_spec_v3 | 15 | 15 | 100.0% | 5665 |
| procurement_policy_v3 | 15 | 15 | 100.0% | 5684 |

## Failure Attribution

| Failure type | Count |
| --- | ---: |
| answer_missing_expected_term | 1 |
| refusal_escape | 1 |

| Failure stage | Count |
| --- | ---: |
| answer | 1 |
| safety_gate | 1 |

### Failed Case Triage

| Case | Failure type | Stage | Reason |
| --- | --- | --- | --- |
| campus_workshop_v3:campus_meal_refusal | refusal_escape | safety_gate | expected refusal but outcome=answered retrieval_status=matched |
| campus_workshop_v3:campus_total_duration | answer_missing_expected_term | answer | answer missing any of ['3.5', '3 小时 30 分钟', '三个半小时'] |

## Case Detail

### [PASS] procurement_policy_v3:proc_scope_departments
- Category: V3_FACT / Difficulty: easy / Kind: answerable
- Query: 本说明适用于哪些业务发起部门？
- Expected pages: [1] | Expected any of: ['研发部', '市场部', '行政部']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5261 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 本说明适用于研发部、市场部和行政部在2026年第二季度发起的低风险采购。
- Error: (none)

### [PASS] procurement_policy_v3:proc_fast_limit
- Category: V3_NUMERIC / Difficulty: easy / Kind: answerable
- Query: 快速审批流程的单笔金额上限是多少？
- Expected pages: [1] | Expected any of: ['48000']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4321 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 快速审批流程的单笔金额上限是48000元。
- Error: (none)

### [PASS] procurement_policy_v3:proc_three_quotes
- Category: V3_NUMERIC / Difficulty: medium / Kind: answerable
- Query: 什么金额区间的采购需要补充三家供应商报价？
- Expected pages: [1] | Expected any of: ['120000']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4845 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 超过 48000 元但不超过 120000 元的采购需要补充三家供应商报价。
- Error: (none)

### [PASS] procurement_policy_v3:proc_fast_sla
- Category: V3_FACT / Difficulty: easy / Kind: answerable
- Query: 快速审批流程目标完成时间是多少？
- Expected pages: [1] | Expected any of: ['2 个工作日', '2个工作日']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5095 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 快速审批流程的目标完成时间是 2 个工作日。
- Error: (none)

### [PASS] procurement_policy_v3:proc_cities
- Category: V3_FACT / Difficulty: easy / Kind: answerable
- Query: 本轮合规试点覆盖了哪几个城市？
- Expected pages: [1] | Expected any of: ['杭州', '成都', '苏州']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4746 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 本轮合规试点覆盖了杭州、成都和苏州。
- Error: (none)

### [PASS] procurement_policy_v3:proc_system_owner
- Category: V3_FACT / Difficulty: easy / Kind: answerable
- Query: 采购系统配置负责人是谁？
- Expected pages: [1] | Expected any of: ['周岚']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5062 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 采购系统配置负责人是周岚。
- Error: (none)

### [PASS] procurement_policy_v3:proc_review_date
- Category: V3_DATE / Difficulty: easy / Kind: answerable
- Query: 试点复盘报告的提交日期是什么时候？
- Expected pages: [1] | Expected any of: ['2026 年 7 月 12 日', '2026年7月12日']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4176 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 试点复盘报告的提交日期是2026年7月12日。
- Error: (none)

### [PASS] procurement_policy_v3:proc_shenzhen_refusal
- Category: V3_BOUNDARY / Difficulty: medium / Kind: answerable
- Query: 深圳是否进入了本轮合规试点？请只依据文档回答。
- Expected pages: [1] | Expected any of: ['不', '没有', '未']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 8381 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 深圳没有进入本轮合规试点。
- Error: (none)

### [PASS] procurement_policy_v3:proc_stock_refusal
- Category: V3_REFUSAL / Difficulty: easy / Kind: refusal
- Query: 根据本说明，哪家供应商的股票会涨？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 7853 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] procurement_policy_v3:proc_meal_refusal
- Category: V3_REFUSAL / Difficulty: medium / Kind: refusal
- Query: 专项评审会是否提供午餐？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 7389 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] procurement_policy_v3:proc_90000_route
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: 如果一笔采购金额为 90000 元，应该走哪类要求？
- Expected pages: [1] | Expected any of: ['三家供应商报价', '补充三家']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4705 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 金额为 90000 元的采购超过 48000 元但不超过 120000 元，需要补充三家供应商报价。
- Error: (none)

### [PASS] procurement_policy_v3:proc_130000_route
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: 如果采购金额为 130000 元，是否还能只补充三家报价？应该进入什么流程？
- Expected pages: [1] | Expected any of: ['专项评审会', '超过 120000']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5618 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 采购金额为 130000 元时，不能只补充三家报价，必须进入专项评审会流程。
- Error: (none)

### [PASS] procurement_policy_v3:proc_deadline_rule
- Category: V3_REASONING / Difficulty: medium / Kind: answerable
- Query: 专项评审会材料提交截止时间和会议日期之间相隔多久？
- Expected pages: [1] | Expected any of: ['5 个工作日', '5个工作日']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5866 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 专项评审会材料提交截止时间和会议日期之间相隔5个工作日。
- Error: (none)

### [PASS] procurement_policy_v3:proc_excluded_major_cities
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: 北京和上海在本说明中的处理方式与杭州、成都、苏州有什么不同？
- Expected pages: [1] | Expected any of: ['保留原有审批流程', '不进入本轮试点']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 2
- Latency: 6095 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 北京和上海保留原有审批流程，不进入本轮合规试点；而杭州、成都和苏州是本轮合规试点覆盖的城市。
- Error: (none)

### [PASS] procurement_policy_v3:proc_roles_compare
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: 财务部和法务专员在文档中的角色有什么区别？
- Expected pages: [1] | Expected any of: ['预算复核', '供应商黑名单复核']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 2
- Latency: 5858 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 财务部仅参与预算复核，不作为业务发起部门；法务专员邹宁负责供应商黑名单复核。
- Error: (none)

### [PASS] incident_review_v3:inc_date
- Category: V3_DATE / Difficulty: easy / Kind: answerable
- Query: Alpha 服务异常发生在哪一天？
- Expected pages: [1] | Expected any of: ['2026 年 3 月 18 日', '2026年3月18日']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4835 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Alpha 服务异常发生在2026年3月18日。
- Error: (none)

### [PASS] incident_review_v3:inc_alert_time
- Category: V3_NUMERIC / Difficulty: easy / Kind: answerable
- Query: 监控在几点发出黄色告警？
- Expected pages: [1] | Expected any of: ['09:47']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4636 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 监控在10:16解除告警，发出黄色告警的时间是09:47。
- Error: (none)

### [PASS] incident_review_v3:inc_clear_time
- Category: V3_NUMERIC / Difficulty: easy / Kind: answerable
- Query: 告警解除时间是什么时候？
- Expected pages: [1] | Expected any of: ['10:16']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4431 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 告警解除时间是10:16。
- Error: (none)

### [PASS] incident_review_v3:inc_affected_queues
- Category: V3_FACT / Difficulty: medium / Kind: answerable
- Query: 受影响的是哪两个队列？
- Expected pages: [1] | Expected any of: ['PDF 解析队列', '截图生成队列']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4432 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 受影响的是 PDF 解析队列和截图生成队列。
- Error: (none)

### [PASS] incident_review_v3:inc_max_queue
- Category: V3_NUMERIC / Difficulty: easy / Kind: answerable
- Query: 高峰期间最大排队长度是多少？
- Expected pages: [1] | Expected any of: ['317']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5124 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 高峰期间最大排队长度为 317 个任务。
- Error: (none)

### [PASS] incident_review_v3:inc_root_limit_wrong
- Category: V3_NUMERIC / Difficulty: easy / Kind: answerable
- Query: 误操作后渲染工作池上限被调整成多少？
- Expected pages: [1] | Expected any of: ['6']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4668 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 误操作后渲染工作池上限被调整成6。
- Error: (none)

### [PASS] incident_review_v3:inc_owner_script
- Category: V3_FACT / Difficulty: easy / Kind: answerable
- Query: 误用旧参数的值班员是谁？
- Expected pages: [1] | Expected any of: ['罗澈']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3727 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 误用旧参数的值班员是罗澈。
- Error: (none)

### [PASS] incident_review_v3:inc_threshold_owner
- Category: V3_FACT / Difficulty: medium / Kind: answerable
- Query: 谁负责把队列长度阈值从 300 调整到 180？
- Expected pages: [1] | Expected any of: ['沈玥']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5220 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 沈玥负责把队列长度阈值从 300 调整到 180。
- Error: (none)

### [PASS] incident_review_v3:inc_data_loss
- Category: V3_BOUNDARY / Difficulty: easy / Kind: answerable
- Query: 本次事件是否造成用户数据丢失？
- Expected pages: [1] | Expected any of: ['没有', '未']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3653 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 本次事件没有造成用户数据丢失。
- Error: (none)

### [PASS] incident_review_v3:inc_payment_refusal
- Category: V3_REFUSAL / Difficulty: medium / Kind: refusal
- Query: 支付系统故障导致了多少笔退款？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 6133 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] incident_review_v3:inc_alert_duration
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: 从黄色告警发出到告警解除，大约经过了多少分钟？
- Expected pages: [1] | Expected any of: ['29']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5114 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 从黄色告警发出到告警解除，大约经过了29分钟。
- Error: (none)

### [PASS] incident_review_v3:inc_restore_duration
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: 从恢复渲染工作池上限到队列恢复到 20 个任务以内，经过了多久？
- Expected pages: [1] | Expected any of: ['14']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 2
- Latency: 5025 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 从恢复渲染工作池上限到队列恢复到 20 个任务以内，经过了 14 分钟。
- Error: (none)

### [PASS] incident_review_v3:inc_wrong_parameter_delta
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: 渲染工作池上限被误调后，比正确值少了多少？
- Expected pages: [1] | Expected any of: ['18']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5189 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 渲染工作池上限被误调后，比正确值少了18。
- Error: (none)

### [PASS] incident_review_v3:inc_first_and_last_action
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: 三个后续动作中，最早截止和最晚截止的负责人分别是谁？
- Expected pages: [1] | Expected any of: ['沈玥', '赵珩']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 2
- Latency: 5481 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 最早截止的负责人是沈玥，最晚截止的负责人是赵珩。
- Error: (none)

### [PASS] incident_review_v3:inc_unaffected_uploads
- Category: V3_REASONING / Difficulty: medium / Kind: answerable
- Query: 哪些上传链路保持正常，和受影响队列形成对比？
- Expected pages: [1] | Expected any of: ['TXT', 'Markdown']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 2
- Latency: 5063 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: TXT 与 Markdown 上传链路保持正常，与受影响的 PDF 解析队列和截图生成队列形成对比。
- Error: (none)

### [PASS] lab_experiment_v3:lab_goal
- Category: V3_FACT / Difficulty: easy / Kind: answerable
- Query: 本次实验比较了哪两种排序方法？
- Expected pages: [1] | Expected any of: ['baseline', 'hybrid-rerank']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5431 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 本次实验比较了 baseline 排序和 hybrid-rerank 排序两种方法。
- Error: (none)

### [PASS] lab_experiment_v3:lab_zh_docs
- Category: V3_NUMERIC / Difficulty: easy / Kind: answerable
- Query: 实验使用了多少份中文制度文档？
- Expected pages: [1] | Expected any of: ['96']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5358 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 实验使用了96份中文制度文档。
- Error: (none)

### [PASS] lab_experiment_v3:lab_en_docs
- Category: V3_NUMERIC / Difficulty: easy / Kind: answerable
- Query: 实验使用了多少份英文技术说明？
- Expected pages: [1] | Expected any of: ['64']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4517 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 实验使用了64份英文技术说明。
- Error: (none)

### [PASS] lab_experiment_v3:lab_total_questions
- Category: V3_NUMERIC / Difficulty: easy / Kind: answerable
- Query: 总问题数是多少？
- Expected pages: [1] | Expected any of: ['1120']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4004 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 总问题数为 1120 个。
- Error: (none)

### [PASS] lab_experiment_v3:lab_rerank_features
- Category: V3_FACT / Difficulty: medium / Kind: answerable
- Query: hybrid-rerank 使用了哪些分数？
- Expected pages: [1] | Expected any of: ['BM25', '向量召回', '标题匹配']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 7365 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: hybrid-rerank 使用了 BM25 分数、向量召回分数和标题匹配分数。
- Error: (none)

### [PASS] lab_experiment_v3:lab_candidates
- Category: V3_NUMERIC / Difficulty: easy / Kind: answerable
- Query: 重排阶段最多保留多少个候选块？
- Expected pages: [1] | Expected any of: ['12']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5253 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 重排阶段最多保留 12 个候选块。
- Error: (none)

### [PASS] lab_experiment_v3:lab_baseline_page_hit
- Category: V3_NUMERIC / Difficulty: easy / Kind: answerable
- Query: baseline 的页命中率是多少？
- Expected pages: [1] | Expected any of: ['87.4']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5188 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: baseline 的页命中率是 87.4%。
- Error: (none)

### [PASS] lab_experiment_v3:lab_hybrid_latency
- Category: V3_NUMERIC / Difficulty: easy / Kind: answerable
- Query: hybrid-rerank 的平均延迟是多少毫秒？
- Expected pages: [1] | Expected any of: ['2310']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3734 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: hybrid-rerank 的平均延迟是 2310 毫秒。
- Error: (none)

### [PASS] lab_experiment_v3:lab_refusal_precision
- Category: V3_NUMERIC / Difficulty: easy / Kind: answerable
- Query: 拒答精度提升到了多少？
- Expected pages: [1] | Expected any of: ['96.5']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 6638 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 拒答精度提升到了96.5%。
- Error: (none)

### [PASS] lab_experiment_v3:lab_asr_refusal
- Category: V3_BOUNDARY / Difficulty: medium / Kind: answerable
- Query: 本次实验评估了语音识别准确率吗？
- Expected pages: [1] | Expected any of: ['不', '没有', '未']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4258 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 本次实验没有评估语音识别准确率。
- Error: (none)

### [PASS] lab_experiment_v3:lab_total_docs
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: 实验一共使用了多少份文档？
- Expected pages: [1] | Expected any of: ['160']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5433 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 实验一共使用了160份文档。
- Error: (none)

### [PASS] lab_experiment_v3:lab_questions_per_doc
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: 每份文档一共抽取多少个问题？
- Expected pages: [1] | Expected any of: ['7']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5965 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 每份文档一共抽取7个问题。
- Error: (none)

### [PASS] lab_experiment_v3:lab_page_hit_gain
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: hybrid-rerank 相比 baseline 的页命中率提高了多少个百分点？
- Expected pages: [1] | Expected any of: ['5.7']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 2
- Latency: 5352 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: hybrid-rerank 相比 baseline 的页命中率提高了 5.7 个百分点。
- Error: (none)

### [PASS] lab_experiment_v3:lab_latency_cost
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: hybrid-rerank 相比 baseline 平均延迟增加了多少毫秒？
- Expected pages: [1] | Expected any of: ['470']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 2
- Latency: 6619 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: hybrid-rerank 相比 baseline 平均延迟增加了 470 毫秒。
- Error: (none)

### [PASS] lab_experiment_v3:lab_bad_network_choice
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: 如果现场演示网络较差，文档建议临时退回哪种排序？为什么？
- Expected pages: [1] | Expected any of: ['baseline', '更低延迟']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5230 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 如果现场演示网络较差，文档建议临时退回 baseline 排序，以换取更低延迟。
- Error: (none)

### [PASS] orion_spec_v3:orion_positioning
- Category: V3_FACT / Difficulty: easy / Kind: answerable
- Query: What kind of assistant is Orion Note?
- Expected pages: [1] | Expected any of: ['meeting-note', 'bilingual']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3707 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Orion Note is a bilingual meeting-note assistant for small research teams.
- Error: (none)

### [PASS] orion_spec_v3:orion_pilot_cities
- Category: V3_FACT / Difficulty: easy / Kind: answerable
- Query: Which two locations are planned for the first public pilot?
- Expected pages: [1] | Expected any of: ['Singapore', 'Taipei']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 6040 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The two locations planned for the first public pilot are Singapore and Taipei.
- Error: (none)

### [PASS] orion_spec_v3:orion_mvp_features
- Category: V3_FACT / Difficulty: easy / Kind: answerable
- Query: Name one MVP feature from the spec.
- Expected pages: [1] | Expected any of: ['transcript cleanup', 'action-item', 'bilingual summary']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 6824 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: One MVP feature from the spec is live transcript cleanup.
- Error: (none)

### [PASS] orion_spec_v3:orion_offline_limitation
- Category: V3_FACT / Difficulty: medium / Kind: answerable
- Query: What does offline mode not support?
- Expected pages: [1] | Expected any of: ['speech transcription']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 7191 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Offline mode does not support new speech transcription.
- Error: (none)

### [PASS] orion_spec_v3:orion_duration
- Category: V3_NUMERIC / Difficulty: easy / Kind: answerable
- Query: What is the maximum meeting duration in the pilot plan?
- Expected pages: [1] | Expected any of: ['90']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4722 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The maximum meeting duration in the pilot plan is 90 minutes.
- Error: (none)

### [PASS] orion_spec_v3:orion_audio_retention
- Category: V3_NUMERIC / Difficulty: easy / Kind: answerable
- Query: After how many days are audio files deleted by default?
- Expected pages: [1] | Expected any of: ['14']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4422 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Audio files are deleted by default after 14 days.
- Error: (none)

### [PASS] orion_spec_v3:orion_beta_date
- Category: V3_DATE / Difficulty: easy / Kind: answerable
- Query: When does private beta start?
- Expected pages: [1] | Expected any of: ['2026-05-20']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4283 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Private beta starts on 2026-05-20.
- Error: (none)

### [PASS] orion_spec_v3:orion_release_owner
- Category: V3_FACT / Difficulty: easy / Kind: answerable
- Query: Who owns the release checklist?
- Expected pages: [1] | Expected any of: ['Mei Tan']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4374 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The owner of the release checklist is Mei Tan.
- Error: (none)

### [PASS] orion_spec_v3:orion_price
- Category: V3_NUMERIC / Difficulty: easy / Kind: answerable
- Query: What is the pilot monthly price per active user?
- Expected pages: [1] | Expected any of: ['19 USD']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4352 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The pilot monthly price per active user is 19 USD.
- Error: (none)

### [PASS] orion_spec_v3:orion_annual_refusal
- Category: V3_REFUSAL / Difficulty: medium / Kind: refusal
- Query: What is the annual contract price?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 8184 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] orion_spec_v3:orion_shortest_retention
- Category: V3_REASONING / Difficulty: medium / Kind: answerable
- Query: What is the shortest audio retention period users can choose according to the spec?
- Expected pages: [1] | Expected any of: ['3 days']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 8470 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The shortest audio retention period users can choose is 3 days.
- Error: (none)

### [PASS] orion_spec_v3:orion_beta_to_pilot_gap
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: Roughly how many days are there between private beta start and public pilot start?
- Expected pages: [1] | Expected any of: ['42']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 2
- Latency: 5231 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: There are roughly 42 days between the private beta start and public pilot start.
- Error: (none)

### [PASS] orion_spec_v3:orion_education_discount_price
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: If the 40% education discount applies to the 19 USD pilot price, what monthly price remains?
- Expected pages: [1] | Expected any of: ['11.4']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 2
- Latency: 6305 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The monthly price after applying the 40% education discount to the 19 USD pilot price is 11.40 USD.
- Error: (none)

### [PASS] orion_spec_v3:orion_not_for_high_stakes
- Category: V3_BOUNDARY / Difficulty: medium / Kind: answerable
- Query: Name one high-stakes use case the product is explicitly not designed for.
- Expected pages: [1] | Expected any of: ['medical diagnosis', 'legal representation']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4099 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The product is explicitly not designed for medical diagnosis.
- Error: (none)

### [PASS] orion_spec_v3:orion_offline_vs_live
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: Contrast offline mode with the live transcription capability described in the MVP.
- Expected pages: [1] | Expected any of: ['saved notes', 'speech transcription']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 2
- Latency: 6784 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Offline mode supports reading saved notes but does not support new speech transcription, whereas the MVP's live transcription capability includes live transcript cleanup, action-item extraction, and b
- Error: (none)

### [PASS] campus_workshop_v3:campus_theme
- Category: V3_FACT / Difficulty: easy / Kind: answerable
- Query: 本次工作坊主题是什么？
- Expected pages: [1] | Expected any of: ['可信文档问答', '证据回链']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4078 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 本次工作坊主题是“可信文档问答与证据回链”。
- Error: (none)

### [PASS] campus_workshop_v3:campus_date
- Category: V3_DATE / Difficulty: easy / Kind: answerable
- Query: 工作坊日期是哪一天？
- Expected pages: [1] | Expected any of: ['2026 年 5 月 14 日', '2026年5月14日']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4192 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 工作坊日期是2026年5月14日。
- Error: (none)

### [PASS] campus_workshop_v3:campus_room
- Category: V3_FACT / Difficulty: easy / Kind: answerable
- Query: 活动地点在哪个房间？
- Expected pages: [1] | Expected any of: ['A301']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3746 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 活动地点在图书馆三层 A301 研讨室。
- Error: (none)

### [PASS] campus_workshop_v3:campus_deadline
- Category: V3_DATE / Difficulty: easy / Kind: answerable
- Query: 报名截止时间是什么时候？
- Expected pages: [1] | Expected any of: ['2026 年 5 月 10 日 18:00', '2026年5月10日18:00']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3885 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 报名截止时间是 2026 年 5 月 10 日 18:00。
- Error: (none)

### [PASS] campus_workshop_v3:campus_capacity
- Category: V3_NUMERIC / Difficulty: easy / Kind: answerable
- Query: 名额上限是多少人？
- Expected pages: [1] | Expected any of: ['80']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5240 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 名额上限为 80 人。
- Error: (none)

### [PASS] campus_workshop_v3:campus_hands_on_time
- Category: V3_DATE / Difficulty: easy / Kind: answerable
- Query: 系统实操安排在哪个时间段？
- Expected pages: [1] | Expected any of: ['14:20', '15:40']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5189 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 系统实操安排在14:20至15:40。
- Error: (none)

### [PASS] campus_workshop_v3:campus_browser
- Category: V3_FACT / Difficulty: easy / Kind: answerable
- Query: 通知建议提前安装什么浏览器？
- Expected pages: [1] | Expected any of: ['Chrome']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4410 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 通知建议提前安装最新版 Chrome 浏览器。
- Error: (none)

### [PASS] campus_workshop_v3:campus_contact
- Category: V3_FACT / Difficulty: easy / Kind: answerable
- Query: 活动联系人是谁？
- Expected pages: [1] | Expected any of: ['林若琪']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4282 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 活动联系人是林若琪。
- Error: (none)

### [PASS] campus_workshop_v3:campus_email
- Category: V3_FACT / Difficulty: easy / Kind: answerable
- Query: 咨询邮箱是什么？
- Expected pages: [1] | Expected any of: ['aiworkshop@example.edu.cn']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4088 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 咨询邮箱是 aiworkshop@example.edu.cn。
- Error: (none)

### [FAIL] campus_workshop_v3:campus_meal_refusal
- Category: V3_REFUSAL / Difficulty: medium / Kind: refusal
- Query: 本通知是否提供餐饮补贴金额？
- Expected pages: [] | Expected any of: []
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3962 ms
- Fail reason: expected refusal but outcome=answered retrieval_status=matched
- Failure type: refusal_escape | stage: safety_gate
- Answer snippet: 本通知没有提供餐饮补贴信息。
- Error: (none)

### [FAIL] campus_workshop_v3:campus_total_duration
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: 工作坊从开始到结束总共持续多久？
- Expected pages: [1] | Expected any of: ['3.5', '3 小时 30 分钟', '三个半小时']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3820 ms
- Fail reason: answer missing any of ['3.5', '3 小时 30 分钟', '三个半小时']
- Failure type: answer_missing_expected_term | stage: answer
- Answer snippet: 工作坊从开始到结束总共持续3小时30分钟。
- Error: (none)

### [PASS] campus_workshop_v3:campus_discussion_duration
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: 分组讨论环节持续多少分钟？
- Expected pages: [1] | Expected any of: ['50']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4257 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 分组讨论环节持续50分钟。
- Error: (none)

### [PASS] campus_workshop_v3:campus_after_practice
- Category: V3_REASONING / Difficulty: medium / Kind: answerable
- Query: 系统实操结束后，下一个正式环节是什么，几点开始？
- Expected pages: [1] | Expected any of: ['分组讨论', '15:50']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 6344 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 系统实操结束后，下一个正式环节是分组讨论，于15:50开始。
- Error: (none)

### [PASS] campus_workshop_v3:campus_privacy_boundary
- Category: V3_REASONING / Difficulty: hard / Kind: answerable
- Query: 通知如何降低参与者上传个人隐私材料的风险？
- Expected pages: [1] | Expected any of: ['提供测试文档', '不要求学生上传个人隐私材料']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 11492 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 通知通过明确不要求学生上传个人隐私材料，并由主办方提供测试文档，从而降低参与者上传个人隐私材料的风险。
- Error: (none)

### [PASS] campus_workshop_v3:campus_waitlist_condition
- Category: V3_REASONING / Difficulty: medium / Kind: answerable
- Query: 什么情况下报名者会进入候补名单？
- Expected pages: [1] | Expected any of: ['满额', '候补名单']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4471 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 当报名人数达到80人上限时，后续报名者将进入候补名单。
- Error: (none)
