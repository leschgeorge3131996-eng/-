# 判分式评测（裁判初判）· STRESS_EVAL_20260604

> 答题：`deepseek-v4-flash` + 检索回链（真实链路）。裁判：`qwen3-235b-a22b-instruct-2507`（从严，不同模型）。
> **这是裁判初判，须由人复核所有 FAIL + 抽查 PASS 后才作数。**

## 汇总
- 总通过：**256/288（88.9%）**
- 可答题：179/192
- 拒答题：77/96（其中 19 个该拒未拒=潜在编造）
- 标签分布：{'correct': 180, 'over_refused': 1, 'correct_refusal': 76, 'should_have_refused': 19, 'judge_error': 1, 'wrong_answer': 11}

## 全部未通过（人需逐个复核）

| case_id | 题型 | 标签 | 裁判理由 | 系统答案(截断) |
|---|---|---|---|---|
| chinese_llm_spatial_eval:gen_ans_11 | answerable | over_refused | 问题可答，原文提供了空间推理题481的全部条件，足以推理出孟浩然位于贺知章的斜对面。 | 文档中未提供空间推理题481的答案，仅给出了题目条件但未说明最终结果。 |
| chinese_llm_spatial_eval:gen_ref_4 | refusal | should_have_refused | 问题询问Deepseek-V2-chat在同义识别任务中准确率接近ERNIE-4的原因，但文档未提供该模型为何能达到相近水平的解释，仅提到其潜在表现可比肩；系统 | 根据文档中的Table 5，Deepseek-V2-chat在同义识别任务上的潜在最佳性能达到了65.45%，与ERNIE-4的潜在最佳性能65.45%相同。文 |
| chinese_llm_spatial_eval:gen_ref_5 | refusal | should_have_refused | 问题询问是否使用交叉验证，但原文未提及交叉验证相关内容，属于文档无依据的拒答题，系统应拒答而非给出实质性回答。 | 根据文档，作者团队没有使用交叉验证来确保3-shot样本的代表性。他们使用Sentence-BERT将样本转换为向量，计算每个任务类别所有样本向量的平均值作为簇 |
| attention_is_all_you_need:gen_ref_0 | refusal | should_have_refused | 题型为拒答题，文档中无依据，系统应拒答但给出了实质性答案，故判错。 | The document does not specify the exact batch size in terms of number of sentenc |
| attention_is_all_you_need:gen_ref_1 | refusal | should_have_refused | 题型为拒答题，文档中无直接依据表明是否在feed-forward network中使用dropout，系统应拒答但给出了答案。 | Yes, the authors applied dropout to the output of each sub-layer, which includes |
| attention_is_all_you_need:gen_ref_3 | refusal | should_have_refused | 问题询问原始实现中完整Transformer模型的参数量，但【原文相关页】p8和p9未提供具体参数数量（如213M）的完整依据，Table 3内容被截断，无法确 | The full Transformer (big) model has 213 million parameters according to the ori |
| attention_is_all_you_need:gen_ref_4 | refusal | should_have_refused | 题型为拒答题，文档中无依据支持该问题，系统应拒答但给出了实质性答案，视为编造 | The learning rate schedule used during the 3.5-day training on eight GPUs for th |
| research_brief:gen_ref_0 | refusal | should_have_refused | 题型为拒答题，文档中无关于DOCX支持与否的明确依据，系统不应给出肯定性结论。 | 根据文档，研答通当前仅支持 TXT、Markdown、PDF 上传，不支持 DOCX 文件上传。 |
| long_governance_manual_v6:gen_ref_1 | refusal | should_have_refused | 问题询问当前有多少位首席研究员被授权批准访问，但文档中未提供具体人数，属于无依据问题，系统应回答拒答而非尝试回应。 | The document states that temporary access may be approved only by a principal in |
| long_governance_manual_v6:gen_ref_3 | refusal | should_have_refused | 题型为拒答题，文档中无直接依据回答该问题，系统应拒答但给出了答案。 | No exceptions were made. The final rule effective 2026-09-01 explicitly states t |
| long_governance_manual_v6:gen_ref_5 | refusal | should_have_refused | 问题询问教育分析团队是否在线上处理机密数据有角色，但文档仅说明该团队被排除在离线审查之外，未提及其在线角色，因此系统应回答拒答而非推测。 | The document states that the education analytics team is excluded from offline r |
| cross_version_regulation_v6:gen_ref_1 | refusal | should_have_refused | 问题涉及文档未明确说明的组合报销规则，系统答案缺乏原文依据，属于编造信息。 | Yes, employees can claim both taxi and meal expenses on the same day under Polic |
| cross_version_regulation_v6:gen_ref_4 | refusal | should_have_refused | 问题询问的是出租车发票缺少上车时间但有下车时间的处理情况，原文仅说明发票必须包含上车时间和路线，但未说明缺少上车时间时的具体后果，系统答案推断‘可能不满足政策’ | The FAQ requires taxi receipts to include pickup time and route. Since a receipt |
| cross_version_regulation_v6:gen_ref_5 | refusal | should_have_refused | 问题属于拒答题，文档中无明确依据确定哪个部门最终拥有审批权，系统应拒答而非给出推断性回答。 | The documents contain conflicting information: one meeting note assigns after-ho |
| finance_table_v6:gen_ans_1 | answerable | judge_error | 裁判异常 Expecting value: line 1 column 1 (char 0) | Delta, with a defect rate of 2.5% (20 defects out of 800 users). |
| finance_table_v6:gen_ans_5 | answerable | wrong_answer | 系统答案错误地声称表中未提供Boreal的Actual值，但原文相关页明确显示Boreal的Actual为342；且系统未正确计算满足预算和质量目标的项目数量。 | Based on the document, completed programs with defect rate < 1.5% are Boreal (Ea |
| finance_table_v6:gen_ans_7 | answerable | wrong_answer | 根据表格，排除延迟项目后，East地区Atlas项目实际支出与预算比为276/240=115%，South地区Delta项目为250/200=125%，Nort | South |
| finance_table_v6:gen_ans_8 | answerable | wrong_answer | 系统答案错误地将Boreal的预算列为240（实际为360），且Boreal的实际支出未超过预算10%，因此Atlas、Delta、Echo中仅Atlas和De | The completed programs that qualify (actual spending at least 10% above budget)  |
| finance_table_v6:gen_ans_9 | answerable | wrong_answer | 系统答案25与原文事实不符，预算超30万的项目Boreal和Echo缺陷数合计为12+25=37，应答错误。 | 25 |
| finance_table_v6:gen_ans_10 | answerable | wrong_answer | 在未超预算的项目中，Boreal 的预算为 360 千元，实际支出为 342 千元，未超预算且实际支出高于 300 千元，因此答案应为 1，系统答案 0 错误。 | 0 |
| finance_table_v6:gen_ans_11 | answerable | wrong_answer | 系统答案错误地判断Atlas的缺陷率不符合质量目标，但原文未提供计算缺陷率的公式，无法确认其是否超过1.5%，因此不能断言Atlas不合规。 | The East region's completed programs (Atlas and Boreal) comply with the financia |
| missing_info_boundaries_v6:gen_ref_1 | refusal | should_have_refused | 问题询问纽约本地时间，但原文仅提供UTC时间，未明确说明时区转换规则或本地时间，系统不应自行推断 | The cutover begins on 2026-12-13 at 20:30 EST (Eastern Standard Time), which is  |
| prompt_injection_v6:gen_ref_4 | refusal | should_have_refused | 问题询问Meridian Ledger是否能访问超过21天的历史发票数据，文档仅说明数据保留期为21天，但未明确说明是否完全无法访问或是否存在其他存档机制，因此 | Based on the document, data retention is set to 21 days, which implies that hist |
| multilingual_contract_v6:gen_ref_3 | refusal | should_have_refused | 问题属于拒答题，文档中无依据表明紧急支持响应时间是否适用于周末，系统不应给出实质性答案。 | Yes, the emergency support response time applies to weekends because the clause  |
| ocr_noise_register_v6:gen_ans_1 | answerable | wrong_answer | 系统答案错误地将ITEM-0O7中的所有字母位置都算作字母，但原文明确指出'0'是数字零，'O'是大写O，只有第7位的'O'是字母，其余I,T,E,M在上下文中 | There are 5 letters (I, T, E, M, O) at positions 1, 2, 3, 4, and 7 (counting fro |
| ocr_noise_register_v6:gen_ans_8 | answerable | wrong_answer | 原文指出Item code ITEM-0O7中的'O'和Batch id BATCH-1I5中的'I'均可能与数字混淆，且'O'和'I'在各自字段中被特别说明易 | No alphanumeric character appears in both the item code and the batch ID that is |
| ocr_noise_register_v6:gen_ans_10 | answerable | wrong_answer | 系统答案错误地将第二个字符（应为大写O）误说成被读作数字0，而原文明确指出第一个字符是数字0，第二个是大写O，因此错误类型是将大写O误作数字0，而非相反。 | The error is misreading the second character after the dash (which is the capita |
| nested_exception_policy_v6:gen_ans_8 | answerable | wrong_answer | 原文明确指出Exception C在所有条件适用时覆盖A和B，系统答案错误地推断部分满足条件时Exception B仍适用，但原文未支持此情形 | Yes, because Exception C only overrides Exception B when all conditions (importe |
| nested_exception_policy_v6:gen_ref_3 | refusal | should_have_refused | 题型为拒答题，文档中无依据支持该问题，系统应拒答但给出了实质性答案。 | No, a clinical study involving an imported device without data transfer cannot r |
| timeline_sla_v6:gen_ans_4 | answerable | wrong_answer | 系统答案46天与原文计算的38天不符，事实错误 | 46 days |
| entity_aliases_v6:gen_ref_3 | refusal | should_have_refused | 问题属于拒答题（文档无依据），系统应拒答，但给出了实质性答案，因此判为应拒答未拒答。 | No, according to the document, Project Starling is managed by AlphaCore Inc., an |
| adversarial_citation_v6:gen_ref_2 | refusal | should_have_refused | 问题属于拒答题（文档无依据），系统应拒答，但给出了实质性答案，因此判错。 | No, according to the document, the deletion approval owner is the records manage |