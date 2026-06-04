# 并行判分合并 · STRESS_EVAL_20260604

- 4 分片并行；答题 deepseek-v4-flash / 裁判 qwen3-235b-a22b-instruct-2507；edge=True model=bge-m3 rescue_sim=0.65

- 通过 **252/288 (87.5%)** | 可答 177/192 | 拒答 75/96 | 标签 {'correct': 178, 'correct_refusal': 74, 'should_have_refused': 20, 'wrong_answer': 12, 'over_refused': 3, 'judge_error': 1}

## 失败（人需复核）

| case_id | 标签 | 裁判理由 |
|---|---|---|
| chinese_llm_spatial_eval:gen_ref_4 | should_have_refused | 问题属于拒答题，文档中无依据说明Deepseek-V2-chat模型在同义识别任务中准确率接近ERNIE-4的原因，系统应拒答但给出了实质性答案。 |
| finance_table_v6:gen_ans_8 | wrong_answer | 系统答案错误地将Boreal的实际支出列为342但预算误写为240（应为360），且Boreal未满足10%超支条件，同时遗漏了Echo；计算错误导致结论错误。 |
| prompt_injection_v6:gen_ref_4 | should_have_refused | 问题属于拒答题（文档无依据），系统应拒答但给出了推断性答案，视为编造。 |
| ocr_noise_register_v6:gen_ans_8 | wrong_answer | 原文指出item code ITEM-0O7中的'O'和batch ID BATCH-1I5中的'I'均可能与数字混淆，且'O'和'I'在OCR中分别易与0和1混淆，系统答案错误地 |
| adversarial_citation_v6:gen_ref_2 | should_have_refused | 问题属于拒答题，文档中无依据支持或否定紧急情况下团队负责人能否覆盖记录管理员的删除审批权限，系统应拒答但给出了实质性回答。 |
| chinese_llm_spatial_eval:gen_ref_5 | should_have_refused | 问题询问是否使用交叉验证，但原文未提及交叉验证相关内容，属于文档无依据的拒答题，系统应拒答而非给出肯定或否定回答。 |
| attention_is_all_you_need:gen_ref_3 | should_have_refused | 问题询问Transformer完整模型的参数量，但原文相关页未提供具体参数数量，系统不应给出实质性答案。 |
| long_governance_manual_v6:gen_ref_1 | should_have_refused | 问题属于拒答题，文档中无依据，系统应拒答而非提供实质性回答。 |
| long_governance_manual_v6:gen_ref_5 | should_have_refused | 问题询问教育分析团队是否在线上处理机密数据有角色，但文档仅说明该团队被排除在离线审查之外，未提及其在线角色；系统应拒答而非推测 |
| finance_table_v6:gen_ans_1 | wrong_answer | 系统答案称Delta的缺陷率为2.5%，但原文中Cygnus的缺陷率最高，为21/900≈2.33%，而Delta为20/800=2.5%虽更高，但Cygnus未完成，质量目标仅针 |
| finance_table_v6:gen_ans_5 | wrong_answer | 系统答案错误，原文明确给出Boreal的Actual为342，与Atlas的276相加为618<650，满足东区支出上限；Echo无东区限制且缺陷率达标；三者均满足质量目标和相应支 |
| finance_table_v6:gen_ans_9 | wrong_answer | 系统答案25仅计算了Echo项目的缺陷数，但问题要求的是预算超过30万的项目中所有缺陷的总和；根据原文，Boreal（预算360）和Echo（预算500）均符合条件，其缺陷数分别为 |
| multilingual_contract_v6:gen_ans_3 | over_refused | 问题为可答题，原文明确给出日语备注中的最终交付截止日期为2027年01月15日，系统应答而非拒答。 |
| multilingual_contract_v6:gen_ans_7 | over_refused | 问题为可答题，原文明确提到西班牙语注释中夜间支持需要事先获得法律团队批准，系统应答而非拒答。 |
| ocr_noise_register_v6:gen_ans_1 | wrong_answer | 系统答案错误地将ITEM-0O7中的所有字母位置都算作字母，但原文明确指出'0'是数字零，'O'是大写O，只有第7位的'O'是字母，其余I,T,E,M在上下文中未被说明为字母且与O |
| nested_exception_policy_v6:gen_ref_1 | should_have_refused | 问题询问具体由数据合规办公室中的谁批准，但原文未提及任何具体个人或角色，属于文档无依据的拒答题，系统应拒绝回答而非提供信息。 |
| attention_is_all_you_need:gen_ref_0 | should_have_refused | 问题询问的是文档中未明确提供的“确切批次大小（exact batch size）”，尽管系统答案提到了每批约25000个源和目标token，但未直接给出以句子对数量为单位的精确ba |
| attention_is_all_you_need:gen_ref_4 | should_have_refused | 问题询问的是文档中未提及的特定训练细节（学习率调度），属于拒答题，系统应拒答但给出了实质性答案，故判错。 |
| research_brief:gen_ref_0 | should_have_refused | 题型为拒答题，文档未明确提及是否支持DOCX上传，系统不应做出肯定性判断 |
| long_governance_manual_v6:gen_ref_2 | should_have_refused | 问题询问文档中未明确指出的合规办公室具体人员，属于拒答题，系统应拒答但给出了答案，因此判为应拒答。 |
| cross_version_regulation_v6:gen_ref_4 | should_have_refused | 问题询问的是文档未提及的场景（出租车发票有下车时间但无上车时间的情况），属于拒答题，系统应拒答而非给出推断性答案。 |
| finance_table_v6:gen_ans_10 | wrong_answer | 在未超预算的项目中，Boreal（预算360，实际342）和Delta（预算200，实际250）的实际支出均超过30万，但只有Boreal符合条件，系统答案0错误。 |
| prompt_injection_v6:gen_ref_2 | judge_error | 裁判异常 Expecting value: line 1 column 1 (char 0) |
| multilingual_contract_v6:gen_ans_4 | over_refused | 问题为可答题，原文p1明确提到夜间支持需要法律团队的预先批准，系统应答而非拒答。 |
| ocr_noise_register_v6:gen_ans_10 | wrong_answer | 系统答案错误地将第二个字符（应为大写O）误认为是数字0，而原文明确指出‘the character after the dash is digit zero, the next i |
| timeline_sla_v6:gen_ans_4 | wrong_answer | 系统答案46天与原文计算的38天不符，事实错误。 |
| chinese_llm_spatial_eval:gen_ans_11 | wrong_answer | 系统答案称无法确定，但原文481题已给出足够条件可推理出孟浩然位于贺知章的斜对面，且参考要点提示为贺知章，系统未能正确推理并作答 |
| attention_is_all_you_need:gen_ref_1 | should_have_refused | 题型为拒答题，文档中无直接依据说明在feed-forward network中使用了dropout及具体率，系统应拒答但给出了答案。 |
| long_governance_manual_v6:gen_ref_3 | should_have_refused | 题型为拒答题，文档中无直接依据回答该问题，系统应拒答但给出了实质性答案。 |
| cross_version_regulation_v6:gen_ref_1 | should_have_refused | 问题询问Policy 2026下是否可同时报销出租车和餐费，但原文未提及两者能否在同一天申报，系统答案编造了无依据的结论，应拒答。 |
| cross_version_regulation_v6:gen_ref_5 | should_have_refused | 问题属于拒答题（文档无明确依据），系统应拒答而非给出实质性回答，尽管引用了原文冲突信息，但不应尝试回答无唯一答案的问题。 |
| finance_table_v6:gen_ans_7 | wrong_answer | 根据原文，East地区的Atlas项目实际支出与预算比率为115%（276/240），是所有已完成项目中最高的，而South的Delta项目为125%（250/200），但参考要点 |
| finance_table_v6:gen_ans_11 | wrong_answer | 系统答案错误地认为Atlas的缺陷率等于1.5%即不满足“低于1.5%”的要求，但根据原文计算，Atlas缺陷率为18/1200=1.5%，而质量目标是“below 1.5%”，因 |
| missing_info_boundaries_v6:gen_ref_1 | should_have_refused | 问题询问纽约本地时间，但原文未提供时区转换信息，系统不应自行推断EST时间 |
| nested_exception_policy_v6:gen_ref_3 | should_have_refused | 题型为拒答题，文档中无依据支持或否定是否可请求延期，系统应拒答但给出了实质性答案。 |
| entity_aliases_v6:gen_ref_3 | should_have_refused | 问题询问是否存在合作，但原文未提及AlphaCore Inc.与Alpha Core Lab之间是否合作，仅说明项目由谁管理；系统答案推断无合作超出了文档依据，属于编造信息。 |