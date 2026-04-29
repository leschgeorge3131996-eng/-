# Extended Evaluation Report — HOLDOUT_EVAL_V4_20260429

Generated: 2026-04-29 23:19:44

## Overall

- Total cases: **50**
- Passed: **48**
- Overall pass rate: **96.0%**
- Answerable pass rate: **97.8%**
- Refusal precision: **80.0%**
- Citation accuracy (answerable page-hit): **100.0%**
- Declaration rate (evidence_mode=declared on answerable): **100.0%**
- Avg latency: **5482 ms**

## By Category

| Category | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| V4_BOUNDARY | 5 | 5 | 100.0% | 4255 |
| V4_DATE | 6 | 6 | 100.0% | 5842 |
| V4_FACT | 15 | 15 | 100.0% | 4633 |
| V4_NUMERIC | 7 | 7 | 100.0% | 5824 |
| V4_REASONING | 12 | 11 | 91.7% | 5245 |
| V4_REFUSAL | 5 | 4 | 80.0% | 8916 |

## By Difficulty

| Difficulty | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| easy | 25 | 25 | 100.0% | 4794 |
| hard | 12 | 11 | 91.7% | 5245 |
| medium | 13 | 12 | 92.3% | 7025 |

## By Document

| Doc | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| api_migration_v4 | 10 | 9 | 90.0% | 5211 |
| grant_rules_v4 | 10 | 9 | 90.0% | 6559 |
| quality_metrics_v4 | 10 | 10 | 100.0% | 4868 |
| security_upgrade_v4 | 10 | 10 | 100.0% | 4985 |
| warehouse_rollout_v4 | 10 | 10 | 100.0% | 5788 |

## Failure Attribution

| Failure type | Count |
| --- | ---: |
| missing_evidence_quote | 1 |
| refusal_escape | 1 |

| Failure stage | Count |
| --- | ---: |
| evidence | 1 |
| safety_gate | 1 |

### Failed Case Triage

| Case | Failure type | Stage | Reason |
| --- | --- | --- | --- |
| grant_rules_v4:grant_amount_gap | missing_evidence_quote | evidence | answer missing any of ['7 万元', '7万元'] |
| api_migration_v4:api_rollback_refusal | refusal_escape | safety_gate | expected refusal but outcome=answered retrieval_status=matched |

## Case Detail

### [PASS] security_upgrade_v4:sec_scope
- Category: V4_FACT / Difficulty: easy / Kind: answerable
- Query: 本次终端安全升级覆盖哪些组织？
- Expected pages: [1] | Expected any of: ['研发中心', '财务共享中心', '华南销售大区']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4302 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 本次终端安全升级覆盖研发中心、财务共享中心和华南销售大区。
- Error: (none)

### [PASS] security_upgrade_v4:sec_excluded_center
- Category: V4_BOUNDARY / Difficulty: easy / Kind: answerable
- Query: 客服中心是否纳入本次灰度范围？
- Expected pages: [1] | Expected any of: ['暂不纳入', '不纳入', '没有纳入']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4245 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 客服中心暂不纳入本次灰度范围。
- Error: (none)

### [PASS] security_upgrade_v4:sec_second_batch_duration
- Category: V4_REASONING / Difficulty: hard / Kind: answerable
- Query: 第二批升级持续多长时间？
- Expected pages: [1] | Expected any of: ['2.5', '2 小时 30 分钟', '2小时30分钟', '两个半小时']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5892 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 第二批升级持续2小时30分钟（从20:00到22:30）。
- Error: (none)

### [PASS] security_upgrade_v4:sec_password_delta
- Category: V4_REASONING / Difficulty: hard / Kind: answerable
- Query: 密码最短长度增加了几位？
- Expected pages: [1] | Expected any of: ['4']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4113 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 密码最短长度增加了4位（从8位调整为12位）。
- Error: (none)

### [PASS] security_upgrade_v4:sec_lock_rule
- Category: V4_NUMERIC / Difficulty: easy / Kind: answerable
- Query: 连续输错密码多少次后会锁定多久？
- Expected pages: [1] | Expected any of: ['5 次', '5次', '15 分钟', '15分钟']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3892 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 连续输错密码5次后，账号将被锁定15分钟。
- Error: (none)

### [PASS] security_upgrade_v4:sec_storage_write
- Category: V4_FACT / Difficulty: medium / Kind: answerable
- Query: 外接存储设备如果需要写入，应如何申请？
- Expected pages: [1] | Expected any of: ['工单系统', '临时授权申请']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4485 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 外接存储设备默认只读，确需写入时需要在工单系统提交临时授权申请。
- Error: (none)

### [PASS] security_upgrade_v4:sec_lab_exception
- Category: V4_DATE / Difficulty: easy / Kind: answerable
- Query: 实验室离线采集设备的暂缓期限到什么时候？
- Expected pages: [1] | Expected any of: ['2026 年 7 月 1 日', '2026年7月1日', '2026-07-01']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4173 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 实验室离线采集设备的暂缓期限到2026年7月1日。
- Error: (none)

### [PASS] security_upgrade_v4:sec_demo_whitelist
- Category: V4_FACT / Difficulty: medium / Kind: answerable
- Query: 销售演示机可以申请多久的临时白名单，需要登记什么？
- Expected pages: [1] | Expected any of: ['7 天', '7天', '设备编号', '责任人']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 6353 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 销售演示机可以申请7天临时白名单，需要登记设备编号和责任人。
- Error: (none)

### [PASS] security_upgrade_v4:sec_total_owner
- Category: V4_FACT / Difficulty: easy / Kind: answerable
- Query: 本次升级总负责人是谁？
- Expected pages: [1] | Expected any of: ['孟知远']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4290 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 本次升级总负责人是孟知远。
- Error: (none)

### [PASS] security_upgrade_v4:sec_vpn_refusal
- Category: V4_REFUSAL / Difficulty: medium / Kind: refusal
- Query: 通知是否说明了 VPN 价格调整？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 8114 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] grant_rules_v4:grant_types
- Category: V4_FACT / Difficulty: easy / Kind: answerable
- Query: 青年创新基金分为哪三个方向？
- Expected pages: [1] | Expected any of: ['探索类', '应用类', '交叉类']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4318 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 青年创新基金分为探索类、应用类和交叉类三个方向。
- Error: (none)

### [PASS] grant_rules_v4:grant_cross_amount
- Category: V4_NUMERIC / Difficulty: easy / Kind: answerable
- Query: 交叉类项目每项资助多少万元，周期多久？
- Expected pages: [1] | Expected any of: ['15 万元', '15万元', '24 个月', '24个月']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 0
- Latency: 16852 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 交叉类项目每项资助 8 万元，周期 24 个月。
- Error: (none)

### [FAIL] grant_rules_v4:grant_amount_gap
- Category: V4_REASONING / Difficulty: hard / Kind: answerable
- Query: 交叉类比探索类多资助多少万元？
- Expected pages: [1] | Expected any of: ['7 万元', '7万元']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 0
- Latency: 10006 ms
- Fail reason: answer missing any of ['7 万元', '7万元']
- Failure type: missing_evidence_quote | stage: evidence
- Answer snippet: 交叉类项目每项资助24万元，探索类项目每项资助8万元，因此交叉类比探索类多资助16万元。
- Error: (none)

### [PASS] grant_rules_v4:grant_duration_gap
- Category: V4_REASONING / Difficulty: hard / Kind: answerable
- Query: 应用类项目周期比探索类长多久？
- Expected pages: [1] | Expected any of: ['6 个月', '6个月']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4904 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 应用类项目周期比探索类长6个月。
- Error: (none)

### [PASS] grant_rules_v4:grant_age_rule
- Category: V4_FACT / Difficulty: easy / Kind: answerable
- Query: 申请人的年龄限制是什么？
- Expected pages: [1] | Expected any of: ['不超过 35 周岁', '不超过35周岁']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4381 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 申请人年龄不超过35周岁。
- Error: (none)

### [PASS] grant_rules_v4:grant_duplicate_rule
- Category: V4_BOUNDARY / Difficulty: medium / Kind: answerable
- Query: 已经担任在研校级重点项目负责人还能作为本基金负责人重复申报吗？
- Expected pages: [1] | Expected any of: ['不能', '不可以', '不能作为']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3744 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 不能。根据申报条件，已经担任在研校级重点项目负责人的申请人，不能作为本基金负责人重复申报。
- Error: (none)

### [PASS] grant_rules_v4:grant_score_components
- Category: V4_REASONING / Difficulty: hard / Kind: answerable
- Query: 评分规则中占比最高和最低的指标分别是什么？
- Expected pages: [1] | Expected any of: ['创新性', '经费合理性']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4499 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 评分规则中占比最高的指标是创新性（40分），占比最低的指标是经费合理性（10分）。
- Error: (none)

### [PASS] grant_rules_v4:grant_no_panel_threshold
- Category: V4_NUMERIC / Difficulty: easy / Kind: answerable
- Query: 总分低于多少分不进入会评？
- Expected pages: [1] | Expected any of: ['70']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4328 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 总分低于70分的项目不进入会评。
- Error: (none)

### [PASS] grant_rules_v4:grant_result_date
- Category: V4_DATE / Difficulty: easy / Kind: answerable
- Query: 立项名单预计什么时候公布？
- Expected pages: [1] | Expected any of: ['2026 年 5 月 20 日', '2026年5月20日', '2026-05-20']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4495 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 立项名单预计在2026年5月20日公布。
- Error: (none)

### [PASS] grant_rules_v4:grant_location_refusal
- Category: V4_REFUSAL / Difficulty: medium / Kind: refusal
- Query: 学校会评的答辩地点在哪里？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 8064 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] warehouse_rollout_v4:wh_warehouses
- Category: V4_FACT / Difficulty: easy / Kind: answerable
- Query: 本次试点覆盖哪些仓库？
- Expected pages: [1] | Expected any of: ['南京一号仓', '武汉二号仓', '西安备件仓']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5247 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 本次试点覆盖南京一号仓、武汉二号仓和西安备件仓。
- Error: (none)

### [PASS] warehouse_rollout_v4:wh_excluded
- Category: V4_FACT / Difficulty: easy / Kind: answerable
- Query: 广州冷链仓为什么不参加本次试点？
- Expected pages: [1] | Expected any of: ['温控系统改造延期']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4664 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 广州冷链仓因温控系统改造延期，不参加本次试点。
- Error: (none)

### [PASS] warehouse_rollout_v4:wh_stage_order
- Category: V4_FACT / Difficulty: medium / Kind: answerable
- Query: 三个上线阶段依次是什么？
- Expected pages: [1] | Expected any of: ['盘点机器人部署', '货位推荐算法启用', '异常出库预警启用']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5866 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 第一阶段为盘点机器人部署（2026年8月3日至8月9日），第二阶段为货位推荐算法启用（2026年8月10日至8月17日），第三阶段为异常出库预警启用（2026年8月18日至8月24日）。
- Error: (none)

### [PASS] warehouse_rollout_v4:wh_total_period
- Category: V4_DATE / Difficulty: medium / Kind: answerable
- Query: 从第一阶段开始到第三阶段结束，整个试点上线跨越哪段日期？
- Expected pages: [1] | Expected any of: ['2026 年 8 月 3 日', '2026年8月3日', '2026 年 8 月 24 日', '2026年8月24日']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 12494 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 整个试点上线从2026年8月3日开始，到2026年8月24日结束。
- Error: (none)

### [PASS] warehouse_rollout_v4:wh_pick_time_delta
- Category: V4_REASONING / Difficulty: hard / Kind: answerable
- Query: 平均拣货时长目标相比原来的 11.2 分钟至少要降低多少分钟？
- Expected pages: [1] | Expected any of: ['1.7']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5004 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 平均拣货时长目标是从11.2分钟降到9.5分钟以内，因此至少要降低1.7分钟。
- Error: (none)

### [PASS] warehouse_rollout_v4:wh_false_alarm
- Category: V4_NUMERIC / Difficulty: easy / Kind: answerable
- Query: 异常出库预警误报率上限是多少？
- Expected pages: [1] | Expected any of: ['4%']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3682 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 异常出库预警误报率上限为4%。
- Error: (none)

### [PASS] warehouse_rollout_v4:wh_nanjing_owner
- Category: V4_FACT / Difficulty: easy / Kind: answerable
- Query: 南京一号仓现场负责人是谁？
- Expected pages: [1] | Expected any of: ['韩予']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4830 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 南京一号仓现场负责人是韩予。
- Error: (none)

### [PASS] warehouse_rollout_v4:wh_pause_condition
- Category: V4_REASONING / Difficulty: hard / Kind: answerable
- Query: 什么情况下仓库需要暂停进入下一阶段？
- Expected pages: [1] | Expected any of: ['连续两天', '低于 97%', '低于97%']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3912 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 如果任一仓库连续两天盘点准确率低于 97%，该仓库需要暂停进入下一阶段。
- Error: (none)

### [PASS] warehouse_rollout_v4:wh_uav_refusal
- Category: V4_BOUNDARY / Difficulty: medium / Kind: answerable
- Query: 本计划是否包含无人机巡检内容？
- Expected pages: [1] | Expected any of: ['没有包含', '不包含', '未包含']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4009 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 本计划没有包含无人机巡检内容。
- Error: (none)

### [PASS] warehouse_rollout_v4:wh_budget_refusal
- Category: V4_REFUSAL / Difficulty: medium / Kind: refusal
- Query: 本计划给出的项目总预算是多少？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 8178 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] api_migration_v4:api_scope
- Category: V4_FACT / Difficulty: easy / Kind: answerable
- Query: Which three request areas are affected by the Atlas API v2 migration?
- Expected pages: [1] | Expected any of: ['upload', 'parse-status', 'page-render', '上传', '解析状态', '页面渲染']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3778 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The three request areas affected by the Atlas API v2 migration are upload, parse-status polling, and page-render requests.
- Error: (none)

### [PASS] api_migration_v4:api_not_affected
- Category: V4_BOUNDARY / Difficulty: easy / Kind: answerable
- Query: Name one area that is not affected by the migration.
- Expected pages: [1] | Expected any of: ['billing exports', 'user invitation codes', '计费导出', '邀请码']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4045 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Billing exports are not affected by the migration.
- Error: (none)

### [PASS] api_migration_v4:api_testing_window
- Category: V4_REASONING / Difficulty: hard / Kind: answerable
- Query: How long is the partner integration testing window?
- Expected pages: [1] | Expected any of: ['15', '14', 'two weeks', '2 weeks', '两周']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5853 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Partner integration testing runs from 2026-09-09 to 2026-09-23, which is a 15-day window.
- Error: (none)

### [PASS] api_migration_v4:api_cutover_time
- Category: V4_DATE / Difficulty: easy / Kind: answerable
- Query: When is production cutover scheduled?
- Expected pages: [1] | Expected any of: ['2026-10-06', '01:00 UTC']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3945 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Production cutover is scheduled for 2026-10-06 at 01:00 UTC.
- Error: (none)

### [PASS] api_migration_v4:api_readonly_after
- Category: V4_NUMERIC / Difficulty: easy / Kind: answerable
- Query: How long will the v1 endpoint remain read-only after cutover?
- Expected pages: [1] | Expected any of: ['30 days', '30 天', '30天']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3853 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The v1 endpoint will remain read-only for 30 days after cutover.
- Error: (none)

### [PASS] api_migration_v4:api_upload_increase
- Category: V4_REASONING / Difficulty: hard / Kind: answerable
- Query: By how many MB does the maximum upload size increase?
- Expected pages: [1] | Expected any of: ['30 MB', '30MB']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4547 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The maximum upload size increases by 30 MB (from 20 MB to 50 MB).
- Error: (none)

### [PASS] api_migration_v4:api_dpi
- Category: V4_NUMERIC / Difficulty: easy / Kind: answerable
- Query: What default DPI value remains unchanged?
- Expected pages: [1] | Expected any of: ['144']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4544 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 默认DPI值保持为144。
- Error: (none)

### [PASS] api_migration_v4:api_signature_change
- Category: V4_FACT / Difficulty: medium / Kind: answerable
- Query: How do webhook signatures change?
- Expected pages: [1] | Expected any of: ['SHA-1', 'SHA-256']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4561 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Webhook signatures change from SHA-1 to SHA-256.
- Error: (none)

### [PASS] api_migration_v4:api_owner
- Category: V4_FACT / Difficulty: easy / Kind: answerable
- Query: Who owns the migration?
- Expected pages: [1] | Expected any of: ['Priya Nair']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3974 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The migration owner is Priya Nair.
- Error: (none)

### [FAIL] api_migration_v4:api_rollback_refusal
- Category: V4_REFUSAL / Difficulty: medium / Kind: refusal
- Query: What rollback date does the note provide?
- Expected pages: [] | Expected any of: []
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 13012 ms
- Fail reason: expected refusal but outcome=answered retrieval_status=matched
- Failure type: refusal_escape | stage: safety_gate
- Answer snippet: 该说明没有提供回滚日期。
- Error: (none)

### [PASS] quality_metrics_v4:qm_sample_total
- Category: V4_REASONING / Difficulty: hard / Kind: answerable
- Query: 本月一共抽检了多少条样本？
- Expected pages: [1] | Expected any of: ['1100']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3641 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 本月一共抽检了 1100 条样本（420 通电话工单 + 680 条在线聊天记录）。
- Error: (none)

### [PASS] quality_metrics_v4:qm_time_range
- Category: V4_DATE / Difficulty: easy / Kind: answerable
- Query: 抽检时间范围是什么？
- Expected pages: [1] | Expected any of: ['2026 年 2 月 1 日', '2026年2月1日', '2026 年 2 月 28 日', '2026年2月28日']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4973 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 抽检时间范围是2026年2月1日至2026年2月28日。
- Error: (none)

### [PASS] quality_metrics_v4:qm_queues
- Category: V4_FACT / Difficulty: easy / Kind: answerable
- Query: 样本来自哪三个队列？
- Expected pages: [1] | Expected any of: ['售前咨询', '售后维修', '投诉处理']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4157 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 样本来自售前咨询、售后维修和投诉处理三个队列。
- Error: (none)

### [PASS] quality_metrics_v4:qm_resolution_gap
- Category: V4_REASONING / Difficulty: hard / Kind: answerable
- Query: 电话工单一次解决率比在线聊天高多少个百分点？
- Expected pages: [1] | Expected any of: ['5.4']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5612 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 电话工单一次解决率比在线聊天高5.4个百分点。
- Error: (none)

### [PASS] quality_metrics_v4:qm_response_gap
- Category: V4_REASONING / Difficulty: hard / Kind: answerable
- Query: 在线聊天平均响应时间比电话慢多少秒？
- Expected pages: [1] | Expected any of: ['13']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4963 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 在线聊天平均响应时间比电话慢13秒。
- Error: (none)

### [PASS] quality_metrics_v4:qm_lowest_satisfaction
- Category: V4_NUMERIC / Difficulty: easy / Kind: answerable
- Query: 满意度最低的是哪个队列，数值是多少？
- Expected pages: [1] | Expected any of: ['投诉处理', '88.4%']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3623 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 满意度最低的是投诉处理队列，数值为 88.4%。
- Error: (none)

### [PASS] quality_metrics_v4:qm_issue_top
- Category: V4_FACT / Difficulty: easy / Kind: answerable
- Query: 出现次数最多的主要问题是什么，出现了多少次？
- Expected pages: [1] | Expected any of: ['维修进度解释不清', '37']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4292 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 出现次数最多的主要问题是维修进度解释不清，出现了37次。
- Error: (none)

### [PASS] quality_metrics_v4:qm_actions_order
- Category: V4_DATE / Difficulty: easy / Kind: answerable
- Query: 3 月 10 日前需要完成什么改进动作？
- Expected pages: [1] | Expected any of: ['优惠政策知识库统一']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4977 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 3 月 10 日前需要完成优惠政策知识库统一。
- Error: (none)

### [PASS] quality_metrics_v4:qm_salary_refusal
- Category: V4_BOUNDARY / Difficulty: medium / Kind: answerable
- Query: 这份月报是否包含客服人员薪酬信息？
- Expected pages: [1] | Expected any of: ['不包含', '没有包含', '不统计']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5233 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 不包含。月报明确说明不包含客服人员薪酬信息。
- Error: (none)

### [PASS] quality_metrics_v4:qm_store_refusal
- Category: V4_REFUSAL / Difficulty: medium / Kind: refusal
- Query: 线下门店服务的一次解决率是多少？
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 7213 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)
