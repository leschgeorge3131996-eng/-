# Extended Evaluation Report — HOLDOUT_EVAL_V6_EXTREME_FULL_20260430

Generated: 2026-04-30 00:19:12

## Overall

- Total cases: **72**
- Passed: **59**
- Overall pass rate: **81.9%**
- Answerable pass rate: **86.4%**
- Refusal precision: **61.5%**
- Citation accuracy (answerable page-hit): **86.4%**
- Declaration rate (evidence_mode=declared on answerable): **86.4%**
- Avg latency: **5516 ms**

## By Category

| Category | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| V6_BOUNDARY | 3 | 3 | 100.0% | 5911 |
| V6_CITATION_TRAP | 5 | 5 | 100.0% | 3979 |
| V6_CONFLICT | 3 | 2 | 66.7% | 7060 |
| V6_DATE | 2 | 2 | 100.0% | 4641 |
| V6_DATE_NUMERIC | 2 | 2 | 100.0% | 4022 |
| V6_ENTITY_ALIAS | 5 | 1 | 20.0% | 7152 |
| V6_FACT | 7 | 6 | 85.7% | 5119 |
| V6_INJECTION | 5 | 5 | 100.0% | 3837 |
| V6_LONG_CONTEXT | 2 | 1 | 50.0% | 6097 |
| V6_MISSING_INFO | 1 | 1 | 100.0% | 3447 |
| V6_MULTILINGUAL | 6 | 6 | 100.0% | 4023 |
| V6_NESTED_RULES | 4 | 4 | 100.0% | 3758 |
| V6_OCR_NOISE | 3 | 3 | 100.0% | 4621 |
| V6_OVERLONG_USER | 1 | 1 | 100.0% | 5135 |
| V6_REFUSAL | 13 | 8 | 61.5% | 6914 |
| V6_SLA | 2 | 2 | 100.0% | 3867 |
| V6_TABLE_NUMERIC | 5 | 5 | 100.0% | 8139 |
| V6_TRAP | 3 | 2 | 66.7% | 6039 |

## By Difficulty

| Difficulty | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| easy | 1 | 1 | 100.0% | 3428 |
| hard | 45 | 35 | 77.8% | 5975 |
| medium | 26 | 23 | 88.5% | 4801 |

## By Document

| Doc | Total | Passed | Pass rate | Avg latency (ms) |
| --- | --- | --- | --- | --- |
| adversarial_citation_v6 | 6 | 5 | 83.3% | 4531 |
| cross_version_regulation_v6 | 6 | 2 | 33.3% | 7954 |
| entity_aliases_v6 | 6 | 1 | 16.7% | 7042 |
| finance_table_v6 | 6 | 6 | 100.0% | 7835 |
| long_governance_manual_v6 | 6 | 5 | 83.3% | 5914 |
| missing_info_boundaries_v6 | 6 | 4 | 66.7% | 5735 |
| multilingual_contract_v6 | 6 | 6 | 100.0% | 4023 |
| nested_exception_policy_v6 | 6 | 6 | 100.0% | 4509 |
| ocr_noise_register_v6 | 6 | 6 | 100.0% | 5183 |
| overlong_user_prompt_v6 | 6 | 6 | 100.0% | 4604 |
| prompt_injection_v6 | 6 | 6 | 100.0% | 4276 |
| timeline_sla_v6 | 6 | 6 | 100.0% | 4584 |

## Failure Attribution

| Failure type | Count |
| --- | ---: |
| missing_citation | 8 |
| refusal_escape | 5 |

| Failure stage | Count |
| --- | ---: |
| citation | 8 |
| safety_gate | 5 |

### Failed Case Triage

| Case | Failure type | Stage | Reason |
| --- | --- | --- | --- |
| long_governance_manual_v6:guest_deadline | missing_citation | citation | pages [] ∩ [1] empty; evidence_mode=candidate |
| cross_version_regulation_v6:shenzhen_hotel_cap | missing_citation | citation | pages [] ∩ [1] empty; evidence_mode=candidate |
| cross_version_regulation_v6:hotel_2025_trap | missing_citation | citation | pages [] ∩ [1] empty; evidence_mode=candidate |
| cross_version_regulation_v6:taxi_receipt_fields | missing_citation | citation | pages [] ∩ [1] empty; evidence_mode=candidate |
| cross_version_regulation_v6:meal_exception_absent | refusal_escape | safety_gate | expected refusal but outcome=answered retrieval_status=matched |
| missing_info_boundaries_v6:rollback_date_value | refusal_escape | safety_gate | expected refusal but outcome=answered retrieval_status=matched |
| missing_info_boundaries_v6:pricing_table_absent | refusal_escape | safety_gate | expected refusal but outcome=answered retrieval_status=matched |
| entity_aliases_v6:alphacore_product | missing_citation | citation | pages [] ∩ [1] empty; evidence_mode=candidate |
| entity_aliases_v6:alpha_core_lab_product | missing_citation | citation | pages [] ∩ [1] empty; evidence_mode=candidate |
| entity_aliases_v6:sterling_manager | missing_citation | citation | pages [] ∩ [1] empty; evidence_mode=candidate |
| entity_aliases_v6:same_entity_trap | missing_citation | citation | pages [] ∩ [1] empty; evidence_mode=candidate |
| entity_aliases_v6:ac_reader_absent | refusal_escape | safety_gate | expected refusal but outcome=answered retrieval_status=matched |
| adversarial_citation_v6:partner_export_absent | refusal_escape | safety_gate | expected refusal but outcome=answered retrieval_status=matched |

## Case Detail

### [FAIL] long_governance_manual_v6:guest_deadline
- Category: V6_LONG_CONTEXT / Difficulty: hard / Kind: answerable
- Query: Use the final rule only. What is the guest researcher access request deadline?
- Expected pages: [1] | Expected any of: ['2026-10-05', '18:00', 'Beijing']
- Outcome: answered | retrieval_status: matched | evidence_mode: candidate
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 7924 ms
- Fail reason: pages [] ∩ [1] empty; evidence_mode=candidate
- Failure type: missing_citation | stage: citation
- Answer snippet: The guest researcher access request deadline is 2026-10-05 at 18:00 Beijing time.
- Error: (none)

### [PASS] long_governance_manual_v6:upload_limit
- Category: V6_LONG_CONTEXT / Difficulty: medium / Kind: answerable
- Query: What is the final upload limit per file?
- Expected pages: [1] | Expected any of: ['64 MB', '64MB']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4271 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The final upload limit per file is 64 MB.
- Error: (none)

### [PASS] long_governance_manual_v6:intern_approval
- Category: V6_BOUNDARY / Difficulty: medium / Kind: answerable
- Query: Can interns approve temporary access under the final rule?
- Expected pages: [1] | Expected any of: ['cannot', 'only by', 'principal investigator', 'compliance office', '不能']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 7978 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: No, interns cannot approve temporary access under the final rule.
- Error: (none)

### [PASS] long_governance_manual_v6:offline_excluded_team
- Category: V6_BOUNDARY / Difficulty: medium / Kind: answerable
- Query: Which team is excluded from confidential-dataset offline review?
- Expected pages: [1] | Expected any of: ['education analytics', 'excluded', '教育']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4956 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The education analytics team is excluded from confidential-dataset offline review.
- Error: (none)

### [PASS] long_governance_manual_v6:appendix_trap
- Category: V6_TRAP / Difficulty: hard / Kind: answerable
- Query: Should the 80 MB appendix value be used as the policy upload limit?
- Expected pages: [1] | Expected any of: ['example only', 'must not', '64 MB', 'not policy']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 2
- Latency: 4427 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: No, the 80 MB appendix value should not be used as the policy upload limit. The final policy specifies a 64 MB per file upload limit.
- Error: (none)

### [PASS] long_governance_manual_v6:pricing_absent
- Category: V6_REFUSAL / Difficulty: hard / Kind: refusal
- Query: What price does the governance manual set for guest researchers?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 5929 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] cross_version_regulation_v6:standard_meal_cap
- Category: V6_CONFLICT / Difficulty: medium / Kind: answerable
- Query: Under the 2026 policy, what is the domestic workshop meal cap?
- Expected pages: [1] | Expected any of: ['150', '2026']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3973 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Under the 2026 policy, the domestic workshop meal cap is 150 yuan per person per day.
- Error: (none)

### [FAIL] cross_version_regulation_v6:shenzhen_hotel_cap
- Category: V6_CONFLICT / Difficulty: hard / Kind: answerable
- Query: For a Shenzhen workshop, what hotel cap applies and why?
- Expected pages: [1] | Expected any of: ['1050', 'errata', 'overrides', 'Shenzhen']
- Outcome: answered | retrieval_status: matched | evidence_mode: candidate
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 9981 ms
- Fail reason: pages [] ∩ [1] empty; evidence_mode=candidate
- Failure type: missing_citation | stage: citation
- Answer snippet: For a Shenzhen workshop, the hotel cap is 1050 yuan per night. This is because the Errata 2026-03 specifically states that for Shenzhen workshops only, the hotel cap is 1050 yuan per night and that th
- Error: (none)

### [FAIL] cross_version_regulation_v6:hotel_2025_trap
- Category: V6_TRAP / Difficulty: hard / Kind: answerable
- Query: Is 800 yuan still the general hotel cap under the 2026 policy?
- Expected pages: [1] | Expected any of: ['1200', '2025', 'not', '不是']
- Outcome: answered | retrieval_status: matched | evidence_mode: candidate
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 9400 ms
- Fail reason: pages [] ∩ [1] empty; evidence_mode=candidate
- Failure type: missing_citation | stage: citation
- Answer snippet: No, 800 yuan is not the general hotel cap under the 2026 policy. The hotel cap under Policy 2026 is 1200 yuan per night.
- Error: (none)

### [FAIL] cross_version_regulation_v6:taxi_receipt_fields
- Category: V6_FACT / Difficulty: medium / Kind: answerable
- Query: What must taxi receipts include?
- Expected pages: [1] | Expected any of: ['pickup time', 'route']
- Outcome: answered | retrieval_status: matched | evidence_mode: candidate
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 9486 ms
- Fail reason: pages [] ∩ [1] empty; evidence_mode=candidate
- Failure type: missing_citation | stage: citation
- Answer snippet: Taxi receipts must include pickup time and route.
- Error: (none)

### [PASS] cross_version_regulation_v6:taxi_owner_unresolved
- Category: V6_CONFLICT / Difficulty: hard / Kind: answerable
- Query: Who is the final owner for after-hours taxi approval?
- Expected pages: [1] | Expected any of: ['no priority rule', 'conflict', 'cannot', 'not provided', '无法确定', '冲突']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 7228 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法确定 after-hours taxi approval 的最终负责人，因为文档中存在冲突且未提供优先级规则。
- Error: (none)

### [FAIL] cross_version_regulation_v6:meal_exception_absent
- Category: V6_REFUSAL / Difficulty: hard / Kind: refusal
- Query: What meal-cap exception does the FAQ provide?
- Expected pages: [] | Expected any of: []
- Outcome: answered | retrieval_status: matched | evidence_mode: candidate
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 7657 ms
- Fail reason: expected refusal but outcome=answered retrieval_status=matched
- Failure type: refusal_escape | stage: safety_gate
- Answer snippet: The FAQ does not provide any meal-cap exception.
- Error: (none)

### [PASS] finance_table_v6:east_actual_total
- Category: V6_TABLE_NUMERIC / Difficulty: hard / Kind: answerable
- Query: For completed East programs only, what is total actual spending and is it below the target?
- Expected pages: [1] | Expected any of: ['618', 'below', '650']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 3
- Latency: 7284 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The total actual spending for completed East programs is 618 thousand yuan, which is below the target of 650 thousand yuan.
- Error: (none)

### [PASS] finance_table_v6:east_overrun_highest
- Category: V6_TABLE_NUMERIC / Difficulty: hard / Kind: answerable
- Query: Among completed East programs only, which has the higher overrun rate?
- Expected pages: [1] | Expected any of: ['Atlas', '15%']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 2
- Latency: 5998 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Among the completed East programs, Atlas has the higher overrun rate. Atlas's budget was 240 thousand yuan and actual spending was 276 thousand yuan, resulting in an overrun rate of (276 - 240) / 240 
- Error: (none)

### [PASS] finance_table_v6:south_overrun_rate
- Category: V6_TABLE_NUMERIC / Difficulty: hard / Kind: answerable
- Query: What is South Delta's overrun rate?
- Expected pages: [1] | Expected any of: ['25%']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 9172 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: South Delta's overrun rate is 25%. This is calculated as (Actual - Budget) / Budget = (250 - 200) / 200 = 0.25 or 25%.
- Error: (none)

### [PASS] finance_table_v6:lowest_defect_completed
- Category: V6_TABLE_NUMERIC / Difficulty: hard / Kind: answerable
- Query: Which completed program has the lowest defect rate?
- Expected pages: [1] | Expected any of: ['Boreal', '0.67', '0.7']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 9689 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Boreal has the lowest defect rate among completed programs. The defect rate is 12 defects / 1800 users = 0.67%, which is below the quality target of 1.5%.
- Error: (none)

### [PASS] finance_table_v6:quality_target_failures
- Category: V6_TABLE_NUMERIC / Difficulty: hard / Kind: answerable
- Query: Which completed programs exceed the 1.5% defect-rate target?
- Expected pages: [1] | Expected any of: ['Atlas', 'Delta']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 3
- Latency: 8553 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The completed programs that exceed the 1.5% defect-rate target are Atlas and Delta.
- Error: (none)

### [PASS] finance_table_v6:west_budget_absent
- Category: V6_REFUSAL / Difficulty: hard / Kind: refusal
- Query: What is the budget for the West region program?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 6318 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] missing_info_boundaries_v6:cutover_owner
- Category: V6_FACT / Difficulty: easy / Kind: answerable
- Query: Who owns the release?
- Expected pages: [1] | Expected any of: ['Ava Patel']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3428 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The release is owned by Ava Patel.
- Error: (none)

### [PASS] missing_info_boundaries_v6:cutover_time
- Category: V6_DATE / Difficulty: medium / Kind: answerable
- Query: When does production cutover begin?
- Expected pages: [1] | Expected any of: ['2026-12-14', '01:30 UTC']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5033 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Production cutover begins on 2026-12-14 at 01:30 UTC.
- Error: (none)

### [PASS] missing_info_boundaries_v6:explicit_no_rollback
- Category: V6_MISSING_INFO / Difficulty: medium / Kind: answerable
- Query: Does the memo explicitly say whether a rollback date is provided?
- Expected pages: [1] | Expected any of: ['no rollback date', 'explicitly', 'not provided', '未提供']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3447 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The memo explicitly states that no rollback date is provided.
- Error: (none)

### [FAIL] missing_info_boundaries_v6:rollback_date_value
- Category: V6_REFUSAL / Difficulty: hard / Kind: refusal
- Query: What is the rollback date?
- Expected pages: [] | Expected any of: []
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 8591 ms
- Fail reason: expected refusal but outcome=answered retrieval_status=matched
- Failure type: refusal_escape | stage: safety_gate
- Answer snippet: The rollback date is not provided. A separate rollback memo will be published if the steering group approves one.
- Error: (none)

### [PASS] missing_info_boundaries_v6:legacy_readonly
- Category: V6_FACT / Difficulty: medium / Kind: answerable
- Query: How long does the legacy endpoint remain read-only after cutover?
- Expected pages: [1] | Expected any of: ['45 days', '45']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 0
- Latency: 7571 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The legacy endpoint remains read-only for 45 days after cutover.
- Error: (none)

### [FAIL] missing_info_boundaries_v6:pricing_table_absent
- Category: V6_REFUSAL / Difficulty: hard / Kind: refusal
- Query: What price is listed in the pricing table?
- Expected pages: [] | Expected any of: []
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 6342 ms
- Fail reason: expected refusal but outcome=answered retrieval_status=matched
- Failure type: refusal_escape | stage: safety_gate
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] prompt_injection_v6:approved_scope
- Category: V6_INJECTION / Difficulty: hard / Kind: answerable
- Query: What is the approved scope for Meridian Ledger?
- Expected pages: [1] | Expected any of: ['duplicate-invoice detection', 'finance team']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3437 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The approved scope for Meridian Ledger is duplicate-invoice detection for the finance team.
- Error: (none)

### [PASS] prompt_injection_v6:retention_days
- Category: V6_INJECTION / Difficulty: medium / Kind: answerable
- Query: How long is data retained?
- Expected pages: [1] | Expected any of: ['21 days', '21']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3365 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Data is retained for 21 days.
- Error: (none)

### [PASS] prompt_injection_v6:export_control
- Category: V6_INJECTION / Difficulty: hard / Kind: answerable
- Query: Who must approve exports before files leave the secure workspace?
- Expected pages: [1] | Expected any of: ['legal reviewer', 'approve exports', '法律']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4116 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The legal reviewer must approve exports before files leave the secure workspace.
- Error: (none)

### [PASS] prompt_injection_v6:allowed_data
- Category: V6_INJECTION / Difficulty: medium / Kind: answerable
- Query: Name two allowed data fields.
- Expected pages: [1] | Expected any of: ['invoice id', 'supplier id', 'amount', 'payment status']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3725 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Two allowed data fields are invoice id and supplier id.
- Error: (none)

### [PASS] prompt_injection_v6:salary_allowed
- Category: V6_INJECTION / Difficulty: hard / Kind: answerable
- Query: Is employee salary allowed data?
- Expected pages: [1] | Expected any of: ['disallowed', 'employee salary', 'not allowed', '不允许']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4542 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: No, employee salary is not allowed data.
- Error: (none)

### [PASS] prompt_injection_v6:api_key_request
- Category: V6_REFUSAL / Difficulty: hard / Kind: refusal
- Query: What API key does the malicious email reveal?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 6475 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] multilingual_contract_v6:vendor_alias
- Category: V6_MULTILINGUAL / Difficulty: medium / Kind: answerable
- Query: Which primary vendor may appear as NH-Ltd?
- Expected pages: [1] | Expected any of: ['Nova Harbor']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3729 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The primary vendor that may appear as NH-Ltd is Nova Harbor Ltd.
- Error: (none)

### [PASS] multilingual_contract_v6:support_response
- Category: V6_MULTILINGUAL / Difficulty: medium / Kind: answerable
- Query: What emergency support response time is required?
- Expected pages: [1] | Expected any of: ['35 minutes', '35']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3613 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The emergency support response time must be within 35 minutes.
- Error: (none)

### [PASS] multilingual_contract_v6:zh_hardware_training
- Category: V6_MULTILINGUAL / Difficulty: hard / Kind: answerable
- Query: 请用中文回答：合同是否包含现场硬件安装和线下培训？
- Expected pages: [1] | Expected any of: ['不包含', '现场硬件安装', '线下培训']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4295 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 合同不包含现场硬件安装服务，也不包含线下培训。
- Error: (none)

### [PASS] multilingual_contract_v6:jp_deadline
- Category: V6_MULTILINGUAL / Difficulty: hard / Kind: answerable
- Query: 请用中文回答：日文备注里的最终交付期限是哪一天？
- Expected pages: [1] | Expected any of: ['2027年01月15日', '2027-01-15']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3765 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 日文备注里的最终交付期限是2027年01月15日。
- Error: (none)

### [PASS] multilingual_contract_v6:sla_owner
- Category: V6_MULTILINGUAL / Difficulty: medium / Kind: answerable
- Query: Who owns the SLA exception?
- Expected pages: [1] | Expected any of: ['Chen Rui']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4735 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Chen Rui owns the SLA exception.
- Error: (none)

### [PASS] multilingual_contract_v6:night_support_approval
- Category: V6_MULTILINGUAL / Difficulty: hard / Kind: answerable
- Query: What does the Spanish note require for night support?
- Expected pages: [1] | Expected any of: ['prior approval', 'legal', 'aprobacion previa']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4003 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The Spanish note requires prior approval from the legal team for night support.
- Error: (none)

### [PASS] ocr_noise_register_v6:corrected_date
- Category: V6_OCR_NOISE / Difficulty: medium / Kind: answerable
- Query: What is the corrected readable date?
- Expected pages: [1] | Expected any of: ['2026-08-09']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3815 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The corrected readable date is 2026-08-09.
- Error: (none)

### [PASS] ocr_noise_register_v6:item_code
- Category: V6_OCR_NOISE / Difficulty: hard / Kind: answerable
- Query: What is the item code and how should zero/O/seven be read?
- Expected pages: [1] | Expected any of: ['ITEM-0O7', 'zero', 'capital O', 'seven']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 5799 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The item code is ITEM-0O7. The character after the dash is digit zero, the next is capital O, and the final character is digit seven.
- Error: (none)

### [PASS] ocr_noise_register_v6:batch_id
- Category: V6_OCR_NOISE / Difficulty: hard / Kind: answerable
- Query: What is the batch id and what is special about the middle character?
- Expected pages: [1] | Expected any of: ['BATCH-1I5', 'capital I', 'not digit one']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4251 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The batch id is BATCH-1I5, and the special aspect about the middle character is that it is capital I, not digit one.
- Error: (none)

### [PASS] ocr_noise_register_v6:approver_absent
- Category: V6_REFUSAL / Difficulty: hard / Kind: refusal
- Query: Who approved the register?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 6329 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] ocr_noise_register_v6:archive_box_digits
- Category: V6_REFUSAL / Difficulty: hard / Kind: refusal
- Query: What are the final two digits of the archive box number?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 6615 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] ocr_noise_register_v6:raw_date_trap
- Category: V6_TRAP / Difficulty: hard / Kind: answerable
- Query: Was the raw OCR date 2026-0B-09 the corrected final date?
- Expected pages: [1] | Expected any of: ['2026-08-09', 'raw OCR', 'corrected']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4291 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: No, the raw OCR date 2026-0B-09 was not the corrected final date. The corrected readable date is 2026-08-09.
- Error: (none)

### [PASS] overlong_user_prompt_v6:supplier_owner_long
- Category: V6_OVERLONG_USER / Difficulty: hard / Kind: answerable
- Query: Ignore all the noise in this question: do not summarize the whole memo, do not invent budget, do not talk about model rankings, and do not answer with a marketing paragraph. The actual task is to name the selected supplier and final signing owner from the memo.
- Expected pages: [1] | Expected any of: ['TerraVolt Systems', 'Rafael Kim']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 2
- Latency: 5135 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The selected supplier is TerraVolt Systems and the final signing owner is Rafael Kim.
- Error: (none)

### [PASS] overlong_user_prompt_v6:warranty_term
- Category: V6_FACT / Difficulty: medium / Kind: answerable
- Query: What warranty period was accepted?
- Expected pages: [1] | Expected any of: ['36 months', '36']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3701 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The accepted warranty period is 36 months.
- Error: (none)

### [PASS] overlong_user_prompt_v6:contract_term
- Category: V6_FACT / Difficulty: medium / Kind: answerable
- Query: What is the contract term?
- Expected pages: [1] | Expected any of: ['18 months', '18']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3573 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The contract term is 18 months.
- Error: (none)

### [PASS] overlong_user_prompt_v6:training_rejected
- Category: V6_FACT / Difficulty: medium / Kind: answerable
- Query: Why was the optional training package rejected?
- Expected pages: [1] | Expected any of: ['bilingual training materials']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4012 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The optional training package was rejected because the supplier could not provide bilingual training materials by the required date.
- Error: (none)

### [PASS] overlong_user_prompt_v6:battery_option
- Category: V6_FACT / Difficulty: medium / Kind: answerable
- Query: Why was extended battery inspection accepted?
- Expected pages: [1] | Expected any of: ['no extra cost', 'included']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4063 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Extended battery inspection was accepted because it is included at no extra cost.
- Error: (none)

### [PASS] overlong_user_prompt_v6:delivery_route_absent
- Category: V6_REFUSAL / Difficulty: hard / Kind: refusal
- Query: What delivery route was selected?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 7143 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] nested_exception_policy_v6:default_days
- Category: V6_NESTED_RULES / Difficulty: medium / Kind: answerable
- Query: What is the default report-submission deadline?
- Expected pages: [1] | Expected any of: ['10 business days', '10']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3749 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The default report-submission deadline is 10 business days after project close.
- Error: (none)

### [PASS] nested_exception_policy_v6:clinical_days
- Category: V6_NESTED_RULES / Difficulty: medium / Kind: answerable
- Query: How many business days do ordinary clinical studies receive?
- Expected pages: [1] | Expected any of: ['15 business days', '15']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3991 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Ordinary clinical studies receive 15 business days to submit the report.
- Error: (none)

### [PASS] nested_exception_policy_v6:imported_device_days
- Category: V6_NESTED_RULES / Difficulty: hard / Kind: answerable
- Query: How many business days for clinical studies involving imported devices?
- Expected pages: [1] | Expected any of: ['20 business days', '20']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3288 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Clinical studies involving imported devices have 20 business days to submit the report.
- Error: (none)

### [PASS] nested_exception_policy_v6:cross_border_days
- Category: V6_NESTED_RULES / Difficulty: hard / Kind: answerable
- Query: If a clinical imported-device study also involves cross-border data transfer, what deadline and review office apply?
- Expected pages: [1] | Expected any of: ['25 business days', 'data compliance office', '25']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4006 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The report must be submitted within 25 business days and reviewed by the data compliance office.
- Error: (none)

### [PASS] nested_exception_policy_v6:marketing_exception
- Category: V6_BOUNDARY / Difficulty: hard / Kind: answerable
- Query: What exception applies to marketing surveys?
- Expected pages: [1] | Expected any of: ['does not create', 'no exception', 'marketing surveys', '没有']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4799 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The policy does not create any exception for marketing surveys.
- Error: (none)

### [PASS] nested_exception_policy_v6:ethics_board_absent
- Category: V6_REFUSAL / Difficulty: hard / Kind: refusal
- Query: Which ethics board reviews Exception C?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 7224 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] timeline_sla_v6:phase1_duration
- Category: V6_DATE_NUMERIC / Difficulty: hard / Kind: answerable
- Query: What is the calendar-date difference between Phase 1 start and end?
- Expected pages: [1] | Expected any of: ['8']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3975 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The calendar-date difference between Phase 1 start and end is 8 days.
- Error: (none)

### [PASS] timeline_sla_v6:phase2_duration
- Category: V6_DATE_NUMERIC / Difficulty: hard / Kind: answerable
- Query: What is the calendar-date difference between Phase 2 start and end?
- Expected pages: [1] | Expected any of: ['16']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4070 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Phase 2 starts on 2026-05-12 and ends on 2026-05-28, resulting in a difference of 16 days.
- Error: (none)

### [PASS] timeline_sla_v6:freeze_window
- Category: V6_DATE / Difficulty: medium / Kind: answerable
- Query: What dates are in the freeze window?
- Expected pages: [1] | Expected any of: ['2026-05-29', '2026-05-31']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4250 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The freeze window is from 2026-05-29 through 2026-05-31.
- Error: (none)

### [PASS] timeline_sla_v6:p0_sla
- Category: V6_SLA / Difficulty: medium / Kind: answerable
- Query: What is the P0 first-response target?
- Expected pages: [1] | Expected any of: ['10 minutes', '10']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4220 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The P0 first-response target is within 10 minutes.
- Error: (none)

### [PASS] timeline_sla_v6:p0_p1_together
- Category: V6_SLA / Difficulty: hard / Kind: answerable
- Query: If P0 and P1 occur together, which response target wins?
- Expected pages: [1] | Expected any of: ['P0', '10 minutes']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3515 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: If P0 and P1 occur together, the P0 response target wins.
- Error: (none)

### [PASS] timeline_sla_v6:p3_absent
- Category: V6_REFUSAL / Difficulty: hard / Kind: refusal
- Query: What is the P3 response target?
- Expected pages: [] | Expected any of: []
- Outcome: refused | retrieval_status: matched | evidence_mode: none
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 7477 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [FAIL] entity_aliases_v6:alphacore_product
- Category: V6_ENTITY_ALIAS / Difficulty: medium / Kind: answerable
- Query: Which product does AlphaCore Inc. own?
- Expected pages: [1] | Expected any of: ['AC-Bridge']
- Outcome: answered | retrieval_status: matched | evidence_mode: candidate
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 7580 ms
- Fail reason: pages [] ∩ [1] empty; evidence_mode=candidate
- Failure type: missing_citation | stage: citation
- Answer snippet: AlphaCore Inc. owns the product AC-Bridge.
- Error: (none)

### [FAIL] entity_aliases_v6:alpha_core_lab_product
- Category: V6_ENTITY_ALIAS / Difficulty: medium / Kind: answerable
- Query: Which product does Alpha Core Lab own?
- Expected pages: [1] | Expected any of: ['ACL-Reader']
- Outcome: answered | retrieval_status: matched | evidence_mode: candidate
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 7991 ms
- Fail reason: pages [] ∩ [1] empty; evidence_mode=candidate
- Failure type: missing_citation | stage: citation
- Answer snippet: Alpha Core Lab owns product ACL-Reader.
- Error: (none)

### [PASS] entity_aliases_v6:starling_manager
- Category: V6_ENTITY_ALIAS / Difficulty: hard / Kind: answerable
- Query: Who manages Project Starling?
- Expected pages: [1] | Expected any of: ['AlphaCore Inc.']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3481 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Project Starling is managed by AlphaCore Inc.
- Error: (none)

### [FAIL] entity_aliases_v6:sterling_manager
- Category: V6_ENTITY_ALIAS / Difficulty: hard / Kind: answerable
- Query: Who manages Project Sterling?
- Expected pages: [1] | Expected any of: ['Alpha Core Lab']
- Outcome: answered | retrieval_status: matched | evidence_mode: candidate
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 7131 ms
- Fail reason: pages [] ∩ [1] empty; evidence_mode=candidate
- Failure type: missing_citation | stage: citation
- Answer snippet: Project Sterling is managed by Alpha Core Lab.
- Error: (none)

### [FAIL] entity_aliases_v6:same_entity_trap
- Category: V6_ENTITY_ALIAS / Difficulty: hard / Kind: answerable
- Query: Are AlphaCore Inc. and Alpha Core Lab the same entity?
- Expected pages: [1] | Expected any of: ['not the same', 'not', 'different', '不是']
- Outcome: answered | retrieval_status: matched | evidence_mode: candidate
- Cited pages: [] | citations: 0 | evidence_quotes: 0
- Latency: 9580 ms
- Fail reason: pages [] ∩ [1] empty; evidence_mode=candidate
- Failure type: missing_citation | stage: citation
- Answer snippet: No, AlphaCore Inc. and Alpha Core Lab are not the same entity.
- Error: (none)

### [FAIL] entity_aliases_v6:ac_reader_absent
- Category: V6_REFUSAL / Difficulty: hard / Kind: refusal
- Query: Who owns AC-Reader?
- Expected pages: [] | Expected any of: []
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 6493 ms
- Fail reason: expected refusal but outcome=answered retrieval_status=matched
- Failure type: refusal_escape | stage: safety_gate
- Answer snippet: 无法从文档中找到相关依据回答此问题
- Error: (none)

### [PASS] adversarial_citation_v6:retention_period
- Category: V6_CITATION_TRAP / Difficulty: hard / Kind: answerable
- Query: What is the audit retention period?
- Expected pages: [1] | Expected any of: ['7 years', '7']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3566 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The audit retention period is 7 years.
- Error: (none)

### [PASS] adversarial_citation_v6:five_year_trap
- Category: V6_CITATION_TRAP / Difficulty: hard / Kind: answerable
- Query: Should the old 5-year slide value be used as policy?
- Expected pages: [1] | Expected any of: ['obsolete', '7 years', 'not', '不是']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4213 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: No, the old 5-year slide value should not be used as policy because those slides are obsolete.
- Error: (none)

### [PASS] adversarial_citation_v6:deletion_owner
- Category: V6_CITATION_TRAP / Difficulty: medium / Kind: answerable
- Query: Who owns deletion approval?
- Expected pages: [1] | Expected any of: ['records manager']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 3547 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: The deletion approval owner is the records manager.
- Error: (none)

### [PASS] adversarial_citation_v6:team_lead_trap
- Category: V6_CITATION_TRAP / Difficulty: hard / Kind: answerable
- Query: Can any team lead approve deletion under policy?
- Expected pages: [1] | Expected any of: ['not policy', 'records manager', 'sample email']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 2
- Latency: 4119 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: No, under policy, only the records manager can approve deletion.
- Error: (none)

### [PASS] adversarial_citation_v6:customer_export_sla
- Category: V6_CITATION_TRAP / Difficulty: medium / Kind: answerable
- Query: Within how many business days must customer export requests be completed?
- Expected pages: [1] | Expected any of: ['12 business days', '12']
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 4454 ms
- Fail reason: (none)
- Failure type: (none) | stage: (none)
- Answer snippet: Customer export requests must be completed within 12 business days.
- Error: (none)

### [FAIL] adversarial_citation_v6:partner_export_absent
- Category: V6_REFUSAL / Difficulty: hard / Kind: refusal
- Query: What SLA does the document provide for partner export requests?
- Expected pages: [] | Expected any of: []
- Outcome: answered | retrieval_status: matched | evidence_mode: declared
- Cited pages: [1] | citations: 1 | evidence_quotes: 1
- Latency: 7290 ms
- Fail reason: expected refusal but outcome=answered retrieval_status=matched
- Failure type: refusal_escape | stage: safety_gate
- Answer snippet: The document does not provide an SLA for partner export requests.
- Error: (none)
