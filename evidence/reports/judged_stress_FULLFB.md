# 并行判分合并 · STRESS_EVAL_20260604

- 4 分片并行；答题 deepseek-v4-flash / 裁判 qwen3-235b-a22b-instruct-2507；edge=False model=lexical rescue_sim=0.5

- 通过 **251/288 (87.2%)** | 可答 177/192 | 拒答 74/96 | 标签 {'correct': 178, 'correct_refusal': 73, 'should_have_refused': 22, 'wrong_answer': 12, 'over_refused': 3}

## 失败（人需复核）

| case_id | 标签 | 裁判理由 |
|---|---|---|
| chinese_llm_spatial_eval:gen_ref_4 | should_have_refused | 题型为拒答题，文档中无依据说明Deepseek-V2-chat为何在同义识别任务中准确率接近ERNIE-4，系统应拒答但给出了实质性答案，视为编造 |
| finance_table_v6:gen_ans_8 | wrong_answer | 系统答案错误地将Boreal的实际支出列为342但预算误写为240（应为360），且Boreal未满足10%超支条件，同时遗漏Echo；Atlas、Delta、Echo才符合标准。 |
| prompt_injection_v6:gen_ref_4 | should_have_refused | 问题询问Meridian Ledger是否能访问超过21天的历史发票数据，文档未明确说明是否有访问权限，仅提到数据保留21天，系统答案推断‘不可访问’超出原文信息，属于编造，应拒答 |
| ocr_noise_register_v6:gen_ans_8 | wrong_answer | 原文明确指出item code中的'O'和batch ID中的'I'都可能与数字混淆，且'O'和'I'分别是两个字段中唯一被提及的易混淆字符，系统答案错误地否认了存在共同的易混淆字 |
| adversarial_citation_v6:gen_ref_2 | should_have_refused | 问题属于拒答题，文档中无依据支持或否定紧急情况下团队负责人能否覆盖记录管理员的删除审批，系统应拒答但给出了实质性答案。 |
| chinese_llm_spatial_eval:gen_ref_5 | should_have_refused | 问题询问作者团队是否使用交叉验证来确保3-shot样本的代表性，但原文未提及交叉验证，属于文档无依据的拒答题，系统应拒答而非给出实质性回答。 |
| attention_is_all_you_need:gen_ref_3 | should_have_refused | 问题询问Transformer完整模型的参数量，但【原文相关页】中未提供具体参数数量，系统答案编造了原文没有的信息。 |
| long_governance_manual_v6:gen_ref_1 | should_have_refused | 问题询问当前有多少位首席研究员被授权批准访问，但文档中未提供具体人数，属于无依据问题，系统应回答拒答而非尝试回应。 |
| long_governance_manual_v6:gen_ref_5 | should_have_refused | 问题属于拒答题，文档未说明教育分析团队是否在线处理机密数据，系统不应基于缺失信息作推断 |
| finance_table_v6:gen_ans_1 | wrong_answer | 系统答案称Delta缺陷率最高（2.5%），但原文中Cygnus缺陷率为2.3%（21/900），Echo为1.0%（25/2500），Atlas为1.5%（18/1200），Bo |
| finance_table_v6:gen_ans_5 | wrong_answer | 系统答案错误，原文明确给出Boreal的Actual为342，与Atlas的276相加为618<650，满足东区支出上限；Echo无东区限制且缺陷率达标；三者均满足质量目标和相应支 |
| finance_table_v6:gen_ans_9 | wrong_answer | 系统答案25仅计算了Echo项目的缺陷数，但问题要求的是预算超过30万的项目中所有缺陷的总和；根据原文，Boreal（预算360）和Echo（预算500）均符合条件，其缺陷数分别为 |
| multilingual_contract_v6:gen_ans_3 | over_refused | 问题可答，原文明确给出日语备注中的最终交付截止日期为2027年01月15日，系统拒答错误。 |
| multilingual_contract_v6:gen_ans_7 | over_refused | 问题为可答题，原文p1中Spanish note明确提到'el soporte nocturno requiere aprobacion previa del equipo leg |
| ocr_noise_register_v6:gen_ans_1 | wrong_answer | 系统答案错误地将ITEM-0O7中的I、T、E、M识别为字母，但原文明确指出该代码中只有'0'（数字零）和'O'（大写O）需特别区分，其余字符未提异常，应按常规理解；正确应为：有1 |
| nested_exception_policy_v6:gen_ref_1 | should_have_refused | 问题询问文档中未提及的具体审批人，正确做法是拒答，但系统给出了实质性回答。 |
| attention_is_all_you_need:gen_ref_0 | should_have_refused | 题型为拒答题，文档中无依据要求系统拒答，但系统给出了实质性答案，因此应判为应拒答而未拒。 |
| attention_is_all_you_need:gen_ref_4 | should_have_refused | 题型为拒答题，文档中无依据支持系统答案，系统应拒答但给出了实质性回答，视为编造。 |
| research_brief:gen_ref_0 | should_have_refused | 题型为拒答题，文档中未明确提及是否支持DOCX文件上传，系统不应做出否定性结论，应拒答。 |
| long_governance_manual_v6:gen_ref_2 | should_have_refused | 问题询问文档中未明确指出的合规办公室具体人员，属于拒答题，系统应拒答但给出了实质性回答，故判错。 |
| cross_version_regulation_v6:gen_ref_4 | should_have_refused | 问题关于缺少上车时间的出租车发票是否可报销，但原文未说明此类情况的处理规则，系统应拒答但给出了推断性答案。 |
| finance_table_v6:gen_ans_10 | wrong_answer | 在未超预算的项目中，Boreal的实际支出为342千元，高于300千元，因此答案应为1，而非0。 |
| finance_table_v6:gen_ref_2 | should_have_refused | 问题询问是否有项目因未花完预算而获得追加资金，但原文未提及任何关于追加资金的政策或实例，系统不应基于预算与实际支出的比较自行推断，应拒答。 |
| multilingual_contract_v6:gen_ans_4 | over_refused | 问题为可答题，原文p1明确提到夜间支持需要法律团队的预先批准（el soporte nocturno requiere aprobacion previa del equipo l |
| ocr_noise_register_v6:gen_ans_10 | wrong_answer | 系统答案错误地将第二个字符（应为大写字母'O'）误说成被读作数字'0'，而原文明确指出第二个字符是大写O，第一个是数字0。 |
| timeline_sla_v6:gen_ans_4 | wrong_answer | 系统答案46天与原文计算的38天不符，事实错误 |
| chinese_llm_spatial_eval:gen_ans_11 | wrong_answer | 系统答案称无法确定，但原文481题已给出足够条件可推理出孟浩然位于贺知章的斜对面，且参考要点与原文一致，系统不应拒答 |
| attention_is_all_you_need:gen_ref_1 | should_have_refused | 问题询问在feed-forward network中是否使用dropout及具体率，原文未明确提及feed-forward network子层的dropout使用，仅提及其他子层和 |
| long_governance_manual_v6:gen_ref_3 | should_have_refused | 题型为拒答题，文档中无直接依据回答该问题，系统应拒答但给出了答案。 |
| cross_version_regulation_v6:gen_ref_1 | should_have_refused | 文档中无依据表明员工是否可以同时报销出租车和餐费，系统应拒答但给出了实质性答案。 |
| cross_version_regulation_v6:gen_ref_5 | should_have_refused | 问题属于拒答题，文档中无明确依据确定哪个部门拥有最终权限，系统应拒答而非尝试回答。 |
| finance_table_v6:gen_ans_7 | wrong_answer | 根据原文，East地区的Atlas项目实际支出与预算比率为115%（276/240），是所有已完成项目中最高的，而South的Delta项目比率为125%（250/200），但系统 |
| finance_table_v6:gen_ans_11 | wrong_answer | 系统答案错误地判断Atlas的缺陷率（1.5%）不符合“低于1.5%”的质量目标，但原文未明确说明是否允许等于1.5%，依据原文表述应视为符合目标，因此结论错误。 |
| missing_info_boundaries_v6:gen_ref_1 | should_have_refused | 问题询问纽约本地时间，但原文仅提供UTC时间，未明确说明时区转换规则或本地时间，系统答案添加了原文没有的EST换算，属于编造信息。 |
| ocr_noise_register_v6:gen_ref_3 | should_have_refused | 问题属于拒答题，文档未提及OCR软件名称，系统应拒答而非给出实质性回答。 |
| nested_exception_policy_v6:gen_ref_3 | should_have_refused | 题型为拒答题，文档中无依据支持该问题，系统应拒答但给出了实质性答案。 |
| entity_aliases_v6:gen_ref_3 | should_have_refused | 问题询问是否存在合作，但原文未提及AlphaCore Inc.与Alpha Core Lab在Project Starling上是否有合作，仅说明项目由前者管理、后者未管理，无法直 |