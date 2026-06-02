# 判分式评测（裁判初判）· GENERALIZATION_EVAL_20260602

> 答题：`deepseek-v4-flash` + 检索回链（真实链路）。裁判：`qwen3-235b-a22b-instruct-2507`（从严，不同模型）。
> **这是裁判初判，须由人复核所有 FAIL + 抽查 PASS 后才作数。**

## 汇总
- 总通过：**156/176（88.6%）**
- 可答题：111/128
- 拒答题：45/48（其中 3 个该拒未拒=潜在编造）
- 标签分布：{'correct': 111, 'wrong_answer': 10, 'correct_refusal': 45, 'over_refused': 6, 'should_have_refused': 4}

## 全部未通过（人需逐个复核）

| case_id | 题型 | 标签 | 裁判理由 | 系统答案(截断) |
|---|---|---|---|---|
| chinese_llm_spatial_eval:gen_ans_3 | answerable | wrong_answer | 系统答案3925与原文表格中空间方位信息推理题目总数（909+468+1509+301+207+531=3925）计算结果一致，但系统给出的训练集、验证集、测试 | 空间方位信息推理题目的总数（训练集+验证集+测试集）是3925（其中训练集共1210题，验证集共675题，测试集共2040题）。 |
| attention_is_all_you_need:gen_ans_0 | answerable | over_refused | 问题为可答题，原文明确指出编码器和解码器均由N=6层组成，系统却拒答，属于过度拒绝 | 无法从文档中找到相关依据回答此问题 |
| attention_is_all_you_need:gen_ans_1 | answerable | over_refused | 问题为可答题，原文明确给出了公式（1），系统应答而非拒答 | 无法从文档中找到相关依据回答此问题 |
| attention_is_all_you_need:gen_ans_2 | answerable | wrong_answer | 系统答案错误地声称文档中存在BLEU分数冲突，实际上原文p1明确且唯一指出WMT 2014英法翻译任务的BLEU分数为41.8，训练时间为3.5天，无矛盾 | 文档中关于WMT 2014英法翻译任务的BLEU分数存在冲突：一个片段报告为41.0（Chunk 2823b35583c40893），另一个片段报告为41.8（ |
| attention_is_all_you_need:gen_ans_3 | answerable | should_have_refused | 系统错误地拒答，原文第6页明确包含表1并提供了自注意力层、循环层和卷积层在最大路径长度上的复杂度信息。 | 文档中未提供表1，因此无法回答自注意力层、循环层和卷积层在最大路径长度上的复杂度。 |
| attention_is_all_you_need:gen_ans_6 | answerable | over_refused | 问题为【可答题】，且原文p3明确提到通过修改解码器中的自注意力子层来防止位置关注后续位置（即使用掩码），因此系统应作答而非拒答。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| research_brief:gen_ans_4 | answerable | wrong_answer | 系统答案错误，将‘下一步’中的增强内容误作‘后续将补充’的功能，而原文明确‘后续将逐步补充’的是PDF结构化解析、文本分块、轻量检索、引用返回和评测闭环。 | 根据文档，后续将补充以下当前尚未完善的功能：1. 检索排序；2. 摘要与提纲的来源说明；3. 固定样例集；4. 演示脚本；5. 比赛材料。共计五项，满足至少四项 |
| cross_version_regulation_v6:gen_ref_1 | refusal | should_have_refused | 问题属于拒答题，文档中无依据表明冲突已被解决，系统不应给出结论性答案而应拒答。 | The document states that the bundle provides no priority rule for this conflict, |
| finance_table_v6:gen_ans_2 | answerable | wrong_answer | 系统答案111千人民币错误，正确应为(276-240)+(250-200)+(525-500)=36+50+25=111，但参考要点提示81，且原文中无计算错误 | 111 thousand yuan |
| finance_table_v6:gen_ans_3 | answerable | wrong_answer | 系统答案错误，Boreal缺陷率为12/1800=0.67%，Echo为25/2500=1%，Boreal更低且唯一，原文可确定最低缺陷率程序为Boreal | There are two programs with the lowest defect rate: Boreal and Echo, both have a |
| finance_table_v6:gen_ans_4 | answerable | wrong_answer | 系统答案计算错误，总实际支出应为1308千万元（276+342+250+525），总用户数为6300，平均为0.2076千元，与原文数据不一致 | The average actual spending per user across all completed programs is approximat |
| finance_table_v6:gen_ans_7 | answerable | wrong_answer | 系统答案中总预算和总实际支出计算错误，正确总预算为1400（240+360+200+500），总实际支出为1493（276+342+250+525），而非118 | The total budget for completed programs is 1,180 thousand yuan (240 + 240 + 200  |
| multilingual_contract_v6:gen_ans_3 | answerable | over_refused | 问题为可答题，原文明确给出日语备注中的最终交付截止日期为2027年01月15日，系统应答而非拒答。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| multilingual_contract_v6:gen_ans_4 | answerable | over_refused | 问题为【可答题】，原文p1明确提到夜间支持需要法律团队的预先批准（el soporte nocturno requiere aprobacion previa  | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| ocr_noise_register_v6:gen_ans_6 | answerable | wrong_answer | 系统答案错误地解释了OCR错误，原文指出'0B'是原始OCR输出，其中'B'是'8'的误识别，但系统称'8'被误识别为'B'，逻辑颠倒且不准确。 | The full corrected date is 2026-08-09. The month's second digit (originally '8') |
| ocr_noise_register_v6:gen_ans_7 | answerable | wrong_answer | 系统答案错误地声称没有字符在两个字段中同时被消歧，但原文明确显示数字0（item code中的'0'）和字母I/O（在各自字段中）存在OCR噪声，而参考要点提示 | In the item code, digit '0' (zero) and capital 'O' are explicitly disambiguated, |
| nested_exception_policy_v6:gen_ref_0 | refusal | should_have_refused | 问题询问涉及国产设备的临床研究，但原文仅说明进口设备有特殊规定，未提及国产设备，默认应适用Exception A，但题型为拒答题且文档无明确依据支持具体天数，系 | 15 business days. |
| timeline_sla_v6:gen_ans_5 | answerable | wrong_answer | 系统答案错误地计算为从5月12日到5月31日共20天，但问题要求的是Phase 1结束（2026-05-11）到Phase 3开始（2026-06-01）之间的 | 20 days (from May 12 to May 31, 2026). |
| timeline_sla_v6:gen_ans_6 | answerable | over_refused | 问题可从原文计算得出，Phase 1共9天、Phase 2共17天、Phase 3共20天，合计46天，系统应答而非拒答。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| adversarial_citation_v6:gen_ref_1 | refusal | should_have_refused | 问题属于拒答题，文档中无依据表明团队负责人是否有权在获得记录经理书面授权时批准删除请求，系统不应给出实质性答案。 | No, a team lead cannot approve deletion requests even with written authorization |