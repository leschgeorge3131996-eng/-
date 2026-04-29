# Extended Evaluation Report — HOLDOUT_EVAL_V2_20260429

Generated: 2026-04-29 22:29:43

## Overall

- Total cases: **13**
- Passed: **13**
- Overall pass rate: **100.0%**
- Answerable pass rate: **100.0%**
- Refusal precision: **100.0%**
- Citation accuracy (answerable page-hit): **100.0%**
- Declaration rate (evidence_mode=declared on answerable): **100.0%**
- Avg latency: **5979 ms**

## By Category

| Category | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| H1 | 6 | 6 | 100.0% | 5230 |
| H2 | 4 | 4 | 100.0% | 6051 |
| H3 | 3 | 3 | 100.0% | 7380 |

## By Difficulty

| Difficulty | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| easy | 9 | 9 | 100.0% | 5946 |
| medium | 4 | 4 | 100.0% | 6051 |

## By Document

| Doc | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| office_notice_holdout | 5 | 5 | 100.0% | 3837 |
| paper_report_holdout | 4 | 4 | 100.0% | 8645 |
| research_brief_holdout | 4 | 4 | 100.0% | 5990 |

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

### [PASS] office_notice_holdout:office_leave_normal_process
- Category: H1 / Difficulty: easy / Kind: answerable
- Query: 普通请假需要提前多久提交申请，谁审批后才生效？
- Expected pages: [1] | Expected any of: ['提前一天', '直属主管']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4125 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 普通请假需要至少提前一天提交申请，经直属主管审批后才生效。
- Error: (none)

### [PASS] office_notice_holdout:office_leave_emergency_makeup
- Category: H2 / Difficulty: medium / Kind: answerable
- Query: 如果遇到紧急情况，制度要求员工怎么处理请假手续？
- Expected pages: [1] | Expected any of: ['电话', '即时通讯', '补交正式申请']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5006 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 如果遇到紧急情况，员工应先通过电话或即时通讯说明原因，并在返岗后补交正式请假申请。
- Error: (none)

### [PASS] office_notice_holdout:office_trip_reimbursement_deadline
- Category: H1 / Difficulty: easy / Kind: answerable
- Query: 出差结束后，报销和总结最迟应在什么时间内完成？
- Expected pages: [1] | Expected any of: ['三个工作日', '3个工作日']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5638 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 出差结束后三个工作日内需要完成报销与总结提交。
- Error: (none)

### [PASS] office_notice_holdout:office_training_owner
- Category: H1 / Difficulty: easy / Kind: answerable
- Query: 这次制度变化的内部培训由哪个部门组织？
- Expected pages: [1] | Expected any of: ['行政部门']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4415 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 这次制度变化的内部培训由行政部门组织。
- Error: (none)

### [PASS] office_notice_holdout:office_stock_refusal
- Category: H3 / Difficulty: easy / Kind: refusal
- Query: 根据这份通知，下周哪只股票会涨？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: no_match | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 1 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。
- Error: (none)

### [PASS] paper_report_holdout:report_pipeline_steps
- Category: H2 / Difficulty: medium / Kind: answerable
- Query: 文档里描述的端云协同处理路线包含哪些关键步骤？
- Expected pages: [1] | Expected any of: ['页级解析', '分块', '云端模型']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 6368 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 文档里描述的端云协同处理路线包含以下关键步骤：先对文档进行页级解析与分块，再根据任务类型选择不同的上下文策略，最后调用云端模型生成结果。
- Error: (none)

### [PASS] paper_report_holdout:report_finished_tasks
- Category: H1 / Difficulty: easy / Kind: answerable
- Query: 固定样例集上，系统已经实现了哪三类任务？
- Expected pages: [1] | Expected any of: ['摘要', '问答', '提纲']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5135 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 在固定样例集上，系统已经实现了摘要、问答、提纲生成三类任务。
- Error: (none)

### [PASS] paper_report_holdout:report_vs_chat_shell
- Category: H2 / Difficulty: medium / Kind: answerable
- Query: 为什么报告说这个方案比普通聊天壳更适合文档场景？
- Expected pages: [1] | Expected any of: ['文档理解', '可解释回答']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 2
- Latency: 7820 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 因为该方案采用端云协同路线，先对文档进行页级解析与分块，再根据任务类型选择不同的上下文策略，最后调用云端模型生成结果，相较于普通聊天壳更适合文档理解与可解释回答场景。
- Error: (none)

### [PASS] paper_report_holdout:report_weather_refusal
- Category: H3 / Difficulty: easy / Kind: refusal
- Query: 这份研究报告有没有说明明天会不会下雨？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 15258 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] research_brief_holdout:brief_first_stage_goal
- Category: H1 / Difficulty: easy / Kind: answerable
- Query: 第一阶段的目标具体覆盖哪些用户动作和任务？
- Expected pages: [1] | Expected any of: ['上传文档', '摘要', '问答', '提纲']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5563 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 第一阶段的目标具体覆盖用户上传文档，并完成摘要、问答和提纲生成。
- Error: (none)

### [PASS] research_brief_holdout:brief_upload_formats
- Category: H1 / Difficulty: easy / Kind: answerable
- Query: 当前能力中支持上传哪些文件类型？
- Expected pages: [1] | Expected any of: ['TXT', 'Markdown', 'PDF']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 6504 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 当前支持上传 TXT、Markdown、PDF 文件类型。
- Error: (none)

### [PASS] research_brief_holdout:brief_future_improvements
- Category: H2 / Difficulty: medium / Kind: answerable
- Query: 下一步计划增强哪些能力？
- Expected pages: [1] | Expected any of: ['检索排序', '来源说明', '固定样例集']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5013 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 下一步计划增强检索排序、摘要与提纲的来源说明，并完善固定样例集、演示脚本与比赛材料。
- Error: (none)

### [PASS] research_brief_holdout:brief_unlisted_price_refusal
- Category: H3 / Difficulty: easy / Kind: refusal
- Query: 研答通现在的收费价格是多少？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 6881 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)
