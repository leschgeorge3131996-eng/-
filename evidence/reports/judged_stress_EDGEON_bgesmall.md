# 判分式评测（裁判初判）· STRESS_EVAL_20260604

> 答题：`deepseek-v4-flash` + 检索回链（真实链路）。裁判：`qwen3-235b-a22b-instruct-2507`（从严，不同模型）。
> **这是裁判初判，须由人复核所有 FAIL + 抽查 PASS 后才作数。**

## 汇总
- 总通过：**256/288（88.9%）**
- 可答题：178/192
- 拒答题：78/96（其中 18 个该拒未拒=潜在编造）
- 标签分布：{'correct': 179, 'over_refused': 3, 'correct_refusal': 77, 'should_have_refused': 18, 'wrong_answer': 11}

## 全部未通过（人需逐个复核）

| case_id | 题型 | 标签 | 裁判理由 | 系统答案(截断) |
|---|---|---|---|---|
| chinese_llm_spatial_eval:gen_ans_11 | answerable | over_refused | 问题为可答题，原文相关页p8明确给出481题的条件，可通过推理确定孟浩然斜对面的人，系统拒答错误。 | 无法从文档中找到相关依据回答此问题 |
| chinese_llm_spatial_eval:gen_ref_4 | refusal | should_have_refused | 问题属于【拒答题】，文档未提供Deepseek-V2-chat在同义识别任务中准确率接近ERNIE-4的原因的直接依据，系统应拒答但给出了实质性回答，视为编造。 | 根据文档中的Table 5，Deepseek-V2-chat在同义识别任务上的潜在最佳性能达到了65.45%，与ERNIE-4的潜在最佳性能65.45%相同。文 |
| chinese_llm_spatial_eval:gen_ref_5 | refusal | should_have_refused | 问题询问是否使用交叉验证，但原文未提及该方法，系统不应给出肯定或否定结论，而应拒答。 | 根据文档，作者团队没有使用交叉验证来确保3-shot样本的代表性。他们使用Sentence-BERT将样本转换为向量，计算每个任务类别所有样本向量的平均值作为簇 |
| attention_is_all_you_need:gen_ref_0 | refusal | should_have_refused | 问题询问的是文档中未明确提供的“确切批次大小（exact batch size）”，系统应回答拒答，但系统却给出了基于近似值的推断性答案，因此判为应拒答而未拒答 | The document does not specify the exact batch size in terms of number of sentenc |
| attention_is_all_you_need:gen_ref_1 | refusal | should_have_refused | 问题询问在feed-forward网络中是否使用dropout及dropout率，但原文未明确提及feed-forward网络中的dropout使用情况，仅提到 | Yes, the authors applied dropout to the output of each sub-layer, which includes |
| attention_is_all_you_need:gen_ref_3 | refusal | should_have_refused | 问题询问Transformer完整模型的参数量，但原文相关页未提供具体参数数量，系统不应给出实质性答案。 | The full Transformer (big) model has 213 million parameters according to the ori |
| attention_is_all_you_need:gen_ref_4 | refusal | should_have_refused | 问题询问的是文档中未提及的特定训练细节（学习率调度），属于拒答题，系统应拒答但给出了实质性答案，故判错。 | The learning rate schedule used during the 3.5-day training on eight GPUs for th |
| research_brief:gen_ref_0 | refusal | should_have_refused | 该问题属于【拒答题】，文档未提及是否支持DOCX上传，系统不应做出肯定或否定回答，而应拒答。 | 根据文档，研答通当前仅支持 TXT、Markdown、PDF 上传，不支持 DOCX 文件上传。 |
| long_governance_manual_v6:gen_ref_1 | refusal | should_have_refused | 问题询问当前有多少位首席研究员被授权批准访问，但文档中未提供具体人数，属于无依据问题，系统应回答拒答而非给出实质性回应。 | The document states that temporary access may be approved only by a principal in |
| long_governance_manual_v6:gen_ref_3 | refusal | should_have_refused | 题型为拒答题，文档中无直接依据回答该问题，系统应拒答但给出了实质性答案，因此判错。 | No exceptions were made. The final rule effective 2026-09-01 explicitly states t |
| long_governance_manual_v6:gen_ref_5 | refusal | should_have_refused | 问题询问教育分析团队是否在线上处理机密数据有角色，但文档仅说明该团队被排除在离线审查之外，未提及其在线角色，因此系统应回答拒答而非推测。 | The document states that the education analytics team is excluded from offline r |
| cross_version_regulation_v6:gen_ref_1 | refusal | should_have_refused | 问题询问Policy 2026下是否可同时报销出租车和餐费，但原文未提及两者能否在同一天申报的规则，属于文档无依据的拒答题，系统应拒答而非给出推断性答案。 | Yes, employees can claim both taxi and meal expenses on the same day under Polic |
| cross_version_regulation_v6:gen_ref_4 | refusal | should_have_refused | 问题询问的是文档未提及的场景（出租车发票有下车时间但无上车时间的情况），属于拒答题，系统应拒答但给出了推断性答案，因此判为应拒答。 | The FAQ requires taxi receipts to include pickup time and route. Since a receipt |
| cross_version_regulation_v6:gen_ref_5 | refusal | should_have_refused | 问题属于拒答题，文档中无明确依据确定哪个部门最终拥有审批权，系统应拒答而非给出推断性回答。 | The documents contain conflicting information: one meeting note assigns after-ho |
| finance_table_v6:gen_ans_1 | answerable | wrong_answer | 系统答案称Delta缺陷率最高为2.5%，但原文中Cygnus的缺陷率（21/900≈2.33%）低于Delta（20/800=2.5%），而Echo的缺陷率（ | Delta, with a defect rate of 2.5% (20 defects out of 800 users). |
| finance_table_v6:gen_ans_5 | answerable | wrong_answer | 系统答案错误地声称表中没有Boreal的Actual值，但原文相关页明确显示Boreal的Actual为342；且系统未正确计算满足预算和质量目标的项目数量。 | Based on the document, completed programs with defect rate < 1.5% are Boreal (Ea |
| finance_table_v6:gen_ans_7 | answerable | wrong_answer | 根据原文，排除延迟项目后，East地区的Atlas项目实际支出与预算比率为115%（276/240），为所有完成项目中最高，而South的Delta项目比率为1 | South |
| finance_table_v6:gen_ans_8 | answerable | wrong_answer | 系统答案错误地将Boreal的实际支出列为342（预算240），但原文中Boreal的预算是360，且其实际支出342未超过预算10%，因此不符合条件。 | The completed programs that qualify (actual spending at least 10% above budget)  |
| finance_table_v6:gen_ans_9 | answerable | wrong_answer | 系统答案25仅计算了Echo项目的缺陷数，但问题要求的是预算超过30万的项目总缺陷数；根据原文，Boreal（预算360）和Echo（预算500）符合条件，其缺 | 25 |
| finance_table_v6:gen_ans_10 | answerable | wrong_answer | 根据表格，未超预算且实际支出超过30万的项目是Boreal（预算360，实际342），符合条件的有1个，系统答0错误。 | 0 |
| finance_table_v6:gen_ans_11 | answerable | wrong_answer | 系统答案错误地判断Atlas的缺陷率不符合质量目标，但原文未提供计算缺陷率的公式，无法确定其是否超过1.5%，因此不能断言Atlas不合规。 | The East region's completed programs (Atlas and Boreal) comply with the financia |
| missing_info_boundaries_v6:gen_ref_1 | refusal | should_have_refused | 问题询问纽约本地时间，但原文仅提供UTC时间，未明确说明时区转换，系统答案推断出EST时间属编造，应拒答。 | The cutover begins on 2026-12-13 at 20:30 EST (Eastern Standard Time), which is  |
| prompt_injection_v6:gen_ref_4 | refusal | should_have_refused | 问题询问Meridian Ledger是否能访问超过21天的历史发票数据，原文仅说明数据保留为21天，但未明确说明是否完全无法访问或是否存在其他存档机制，因此系 | Based on the document, data retention is set to 21 days, which implies that hist |
| multilingual_contract_v6:gen_ans_4 | answerable | over_refused | 问题为【可答题】，原文p1明确提到夜间支持需要法律团队（equipo legal）的预先批准，系统应答而非拒答。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| multilingual_contract_v6:gen_ans_7 | answerable | over_refused | 问题为可答题，原文p1中Spanish note明确提到'el soporte nocturno requiere aprobacion previa del  | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| ocr_noise_register_v6:gen_ans_1 | answerable | wrong_answer | 系统答案错误地将ITEM-0O7中的I、T、E、M识别为字母，但原文明确指出该代码中只有'0'（零）、'O'（大写O）和'7'（七），其中仅'O'是字母，且位于 | There are 5 letters (I, T, E, M, O) at positions 1, 2, 3, 4, and 7 (counting fro |
| ocr_noise_register_v6:gen_ans_8 | answerable | wrong_answer | 原文明确指出item code中的'O'和batch ID中的'I'都可能与数字混淆，且'O'出现在item code（ITEM-0O7）和batch ID（B | No alphanumeric character appears in both the item code and the batch ID that is |
| ocr_noise_register_v6:gen_ans_10 | answerable | wrong_answer | 系统答案错误地将第二个字符（应为大写O）误说成被读作数字0，而原文明确指出第一个字符是数字0，第二个是大写O，因此错误类型是将大写O误作数字0，而非相反。 | The error is misreading the second character after the dash (which is the capita |
| nested_exception_policy_v6:gen_ref_3 | refusal | should_have_refused | 题型为拒答题，文档中无依据支持或否定是否可以请求延期，系统应拒答但给出了实质性答案。 | No, a clinical study involving an imported device without data transfer cannot r |
| timeline_sla_v6:gen_ans_4 | answerable | wrong_answer | 系统答案46天与原文计算的38天不符，事实错误 | 46 days |
| entity_aliases_v6:gen_ref_3 | refusal | should_have_refused | 问题询问是否存在合作，但原文未提及AlphaCore Inc.与Alpha Core Lab之间是否合作，仅说明Project Starling由AlphaCo | No, according to the document, Project Starling is managed by AlphaCore Inc., an |
| adversarial_citation_v6:gen_ref_2 | refusal | should_have_refused | 问题属于拒答题，文档中无依据支持或否定紧急情况下团队负责人能否覆盖记录管理员的删除审批，系统应拒答但给出了实质性回答。 | No, according to the document, the deletion approval owner is the records manage |