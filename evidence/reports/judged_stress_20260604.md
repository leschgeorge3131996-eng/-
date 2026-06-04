# 判分式评测（裁判初判）· STRESS_EVAL_20260604

> 答题：`deepseek-v4-flash` + 检索回链（真实链路）。裁判：`qwen3-235b-a22b-instruct-2507`（从严，不同模型）。
> **这是裁判初判，须由人复核所有 FAIL + 抽查 PASS 后才作数。**

## 汇总
- 总通过：**260/288（90.3%）**
- 可答题：177/192
- 拒答题：83/96（其中 13 个该拒未拒=潜在编造）
- 标签分布：{'correct': 178, 'over_refused': 4, 'correct_refusal': 82, 'should_have_refused': 13, 'wrong_answer': 11}

## 全部未通过（人需逐个复核）

| case_id | 题型 | 标签 | 裁判理由 | 系统答案(截断) |
|---|---|---|---|---|
| chinese_llm_spatial_eval:gen_ans_11 | answerable | over_refused | 问题为可答题，原文相关页p8明确给出空间推理题481的条件，足以推理出孟浩然位于贺知章的斜对面，系统拒答错误。 | 无法从文档中找到相关依据回答此问题 |
| chinese_llm_spatial_eval:gen_ref_4 | refusal | should_have_refused | 问题询问Deepseek-V2-chat在同义识别任务中准确率接近ERNIE-4的原因，但文档未提供任何关于其能力原因的解释，仅提到其潜在表现可比肩，系统应拒答 | 根据文档中的Table 5，Deepseek-V2-chat在同义识别任务上的潜在最佳性能达到了65.45%，与ERNIE-4的潜在最佳性能65.45%相同。文 |
| chinese_llm_spatial_eval:gen_ref_5 | refusal | should_have_refused | 题型为拒答题，文档中无依据表明作者团队是否使用交叉验证，系统不应给出实质性答案 | 根据文档，作者团队没有使用交叉验证来确保3-shot样本的代表性。他们使用Sentence-BERT将样本转换为向量，计算每个任务类别所有样本向量的平均值作为簇 |
| attention_is_all_you_need:gen_ref_0 | refusal | should_have_refused | 问题要求提供确切的批量大小（exact batch size），但原文只提到每批包含约25000个源token和目标token，未给出以句子对数量为单位的确切批 | The document does not specify the exact batch size in terms of number of sentenc |
| attention_is_all_you_need:gen_ref_1 | refusal | should_have_refused | 问题询问在feed-forward network中是否使用dropout及具体率，原文未明确提及feed-forward network中的dropout使用 | Yes, the authors applied dropout to the output of each sub-layer, which includes |
| attention_is_all_you_need:gen_ref_4 | refusal | should_have_refused | 问题询问的是文档中未提及的特定训练细节（学习率调度），正确做法是拒答，但系统给出了无原文依据的详细答案。 | The learning rate schedule used during the 3.5-day training on eight GPUs for th |
| research_brief:gen_ref_0 | refusal | should_have_refused | 题型为拒答题，文档中未明确提及是否支持DOCX上传，系统不应做出肯定性判断 | 根据文档，研答通当前仅支持 TXT、Markdown、PDF 上传，不支持 DOCX 文件上传。 |
| long_governance_manual_v6:gen_ref_1 | refusal | should_have_refused | 问题属于拒答题（文档无依据），系统应拒答，但给出了实质性回答，视为编造。 | The document states that temporary access may be approved only by a principal in |
| long_governance_manual_v6:gen_ref_3 | refusal | should_have_refused | 题型为拒答题，文档中无直接依据回答该问题，系统应拒答但给出了实质性答案。 | No exceptions were made. The final rule effective 2026-09-01 explicitly states t |
| long_governance_manual_v6:gen_ref_5 | refusal | should_have_refused | 问题询问教育分析团队是否在线上处理机密数据有角色，但文档仅说明该团队被排除在离线审查之外，未提及其在线角色，因此系统应回答拒答而非推测。 | The document states that the education analytics team is excluded from offline r |
| cross_version_regulation_v6:gen_ref_5 | refusal | should_have_refused | 问题属于拒答题，文档中无明确依据确定哪个部门最终拥有审批权，系统不应给出实质性答案 | The documents contain conflicting information: one meeting note assigns after-ho |
| finance_table_v6:gen_ans_1 | answerable | wrong_answer | 根据原文，缺陷率最高的项目是Cygnus，其缺陷率为2.3%（21/900），而系统答案错误地指出Delta的缺陷率最高为2.5%。 | Delta, with a defect rate of 2.5% (20 defects out of 800 users). |
| finance_table_v6:gen_ans_5 | answerable | wrong_answer | 系统答案错误，原文明确给出Boreal的Actual为342，与Atlas的276相加为618<650，满足东区支出上限；Echo无东区限制且缺陷率达标；三者均 | Based on the document, completed programs with defect rate < 1.5% are Boreal (Ea |
| finance_table_v6:gen_ans_7 | answerable | wrong_answer | 根据原文，East地区的Atlas项目实际支出与预算比率为115%（276/240），是所有已完成项目中最高的，而South的Delta项目为125%（250/ | South |
| finance_table_v6:gen_ans_8 | answerable | wrong_answer | 系统答案错误地将Boreal的预算列为240（实际为360），且Boreal的实际支出未超过预算10%，因此Atlas、Delta、Echo中仅Atlas和De | The completed programs that qualify (actual spending at least 10% above budget)  |
| finance_table_v6:gen_ans_9 | answerable | wrong_answer | 系统答案25与原文事实不符，正确总数应为Boreal的12加上Echo的25等于37 | 25 |
| finance_table_v6:gen_ans_10 | answerable | wrong_answer | 在未超预算的项目中，Boreal 的预算为 360 千元，实际支出为 342 千元，未超预算且实际支出高于 300 千元，因此答案应为 1，系统答案 0 错误。 | 0 |
| finance_table_v6:gen_ans_11 | answerable | wrong_answer | 系统答案错误地判断Atlas的缺陷率不符合目标，但原文未提供计算缺陷率的公式，无法确定其是否超过1.5%，因此不能断言Atlas不合规。 | The East region's completed programs (Atlas and Boreal) comply with the financia |
| prompt_injection_v6:gen_ref_4 | refusal | should_have_refused | 问题询问的是文档中未提及的关于Meridian Ledger是否能访问超过21天的历史发票数据，系统应拒答，但其却给出了推断性答案，因此判为应拒答而未拒。 | Based on the document, data retention is set to 21 days, which implies that hist |
| multilingual_contract_v6:gen_ans_3 | answerable | over_refused | 系统拒答，但原文第一页明确提到日语备注中的最终交付截止日期为2027年01月15日，应可答题。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| multilingual_contract_v6:gen_ans_4 | answerable | over_refused | 问题为可答题，原文p1明确提到夜间支持需要法律团队（equipo legal）的预先批准，系统应答而非拒答。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| multilingual_contract_v6:gen_ans_7 | answerable | over_refused | 问题可答，原文明确提到西班牙语注释中夜间支持需要法律团队预先批准，系统应答而非拒答。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| ocr_noise_register_v6:gen_ans_1 | answerable | wrong_answer | 系统答案错误地将ITEM-0O7中的I、T、E、M识别为字母，但原文明确指出该代码中只有'0'（数字零）、'O'（大写字母O）和'7'（数字七），且仅第6位是字 | There are 5 letters (I, T, E, M, O) at positions 1, 2, 3, 4, and 7 (counting fro |
| ocr_noise_register_v6:gen_ans_8 | answerable | wrong_answer | 原文指出Item code ITEM-0O7中的'O'和Batch id BATCH-1I5中的'I'均可能与数字混淆，且'O'和'I'都是大写字母，在OCR中 | No alphanumeric character appears in both the item code and the batch ID that is |
| ocr_noise_register_v6:gen_ans_10 | answerable | wrong_answer | 系统答案错误地将第二个字符（应为大写O）误说成被读作数字0，而原文明确指出第一个字符是数字0，第二个是大写O，因此错误类型描述颠倒。 | The error is misreading the second character after the dash (which is the capita |
| nested_exception_policy_v6:gen_ref_3 | refusal | should_have_refused | 题型为拒答题，文档中无依据支持该问题，系统应拒答但给出了实质性答案。 | No, a clinical study involving an imported device without data transfer cannot r |
| timeline_sla_v6:gen_ans_4 | answerable | wrong_answer | 系统答案46天与原文计算的38天不符，事实错误。 | 46 days |
| adversarial_citation_v6:gen_ref_2 | refusal | should_have_refused | 问题属于拒答题，文档中无依据支持或否定紧急情况下团队负责人能否覆盖记录管理员的删除审批权，系统应拒答但给出了实质性回答。 | No, according to the document, the deletion approval owner is the records manage |