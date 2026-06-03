# 判分式评测（裁判初判）· GENERALIZATION_EVAL_20260602

> 答题：`deepseek-v4-flash` + 检索回链（真实链路）。裁判：`qwen3-235b-a22b-instruct-2507`（从严，不同模型）。
> **这是裁判初判，须由人复核所有 FAIL + 抽查 PASS 后才作数。**

## 汇总
- 总通过：**157/176（89.2%）**
- 可答题：114/128
- 拒答题：43/48（其中 5 个该拒未拒=潜在编造）
- 标签分布：{'correct': 114, 'wrong_answer': 11, 'correct_refusal': 43, 'should_have_refused': 6, 'partial': 1, 'over_refused': 1}

## 全部未通过（人需逐个复核）

| case_id | 题型 | 标签 | 裁判理由 | 系统答案(截断) |
|---|---|---|---|---|
| chinese_llm_spatial_eval:gen_ans_3 | answerable | wrong_answer | 系统答案错误，原文表1显示空间方位信息推理题目总数为（909+301）+（468+207）+（1509+531）=1210+675+2040=4025，而非39 | 空间方位信息推理题目的总数（训练集+验证集+测试集）是3925（其中训练集共1210题，验证集共675题，测试集共2040题）。 |
| chinese_llm_spatial_eval:gen_ref_2 | refusal | should_have_refused | 问题询问SpaceEval 2013中运动关系标注的类别数量，但原文未提供具体数目，系统应拒答而未拒答。 | 文档提到SpaceEval 2013引入了运动关系（Movelink）和运动标签，用于注释运动动词或名词性运动事件及其类别并从空间语义的角度来分类事件，但未明确 |
| attention_is_all_you_need:gen_ans_0 | answerable | partial | 系统答案称解码器层数未明确说明，但原文明确指出解码器也由N=6层组成，因此答案不完整且部分错误。 | 编码器由6层相同层组成（N=6）。解码器的层数在提供的文档片段中未明确说明。 |
| attention_is_all_you_need:gen_ans_2 | answerable | wrong_answer | 系统答案错误地声称文档中存在BLEU分数冲突，实际上原文p1明确指出WMT 2014英法翻译任务上模型达到41.8 BLEU，且训练3.5天，无矛盾 | 文档中关于WMT 2014英法翻译任务的BLEU分数存在冲突：一个片段报告为41.0（Chunk 2823b35583c40893），另一个片段报告为41.8（ |
| attention_is_all_you_need:gen_ans_6 | answerable | should_have_refused | 问题为【可答题】且原文相关页[p3]明确提到解码器通过修改自注意力子层并使用掩码（masking）防止当前位置关注后续位置，系统应基于此作答而非拒答。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| paper_report:gen_ref_2 | refusal | should_have_refused | 题型为拒答题，文档中无直接依据说明本地模块是否具备独立生成摘要的能力，系统不应做出明确判断 | 根据文档，端云协同路线中，文档经过页级解析与分块后，最终调用云端模型生成结果，因此本地模块不具备独立生成摘要的能力，摘要生成依赖云端模型。 |
| research_brief:gen_ans_4 | answerable | wrong_answer | 系统答案列举的是‘下一步’计划增强的内容，但问题问的是‘后续将补充哪些当前尚未完善的功能’，根据原文，应指‘PDF结构化解析、文本分块、轻量检索、引用返回、评测 | 根据文档，后续将补充以下当前尚未完善的功能：1. 检索排序；2. 摘要与提纲的来源说明；3. 固定样例集；4. 演示脚本；5. 比赛材料。共计五项，满足至少四项 |
| cross_version_regulation_v6:gen_ref_1 | refusal | should_have_refused | 问题属于拒答题，文档中无依据表明冲突已被解决或由谁解决，系统不应给出实质性答案 | The document states that the bundle provides no priority rule for this conflict, |
| finance_table_v6:gen_ans_2 | answerable | wrong_answer | 系统答案111千人民币错误，正确应为(276-240)+(250-200)+(525-500)=36+50+25=111，但参考要点提示81，且原文中East区 | 111 thousand yuan |
| finance_table_v6:gen_ans_3 | answerable | wrong_answer | 系统答案错误，Boreal缺陷数为12，缺陷率1%；Echo缺陷数为25，缺陷率1%；两者缺陷率相同但Boreal缺陷数更低，原文中Boreal是唯一最低缺陷数 | There are two programs with the lowest defect rate: Boreal and Echo, both have a |
| finance_table_v6:gen_ans_4 | answerable | wrong_answer | 系统答案计算错误，总实际支出应为1308千万元（276+342+250+525），总用户数为6300，平均为0.2076千元，与原文数据不一致 | The average actual spending per user across all completed programs is approximat |
| finance_table_v6:gen_ans_7 | answerable | wrong_answer | 系统答案中总预算和总实际支出计算错误，正确总预算为1400（240+360+200+500），总实际支出为1493（276+342+250+525），而非其声称 | The total budget for completed programs is 1,180 thousand yuan (240 + 240 + 200  |
| multilingual_contract_v6:gen_ans_4 | answerable | over_refused | 问题为可答题，原文p1明确提到夜间支持需要法律团队（equipo legal）的预先批准，系统应答而非拒答。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| ocr_noise_register_v6:gen_ans_6 | answerable | wrong_answer | 系统答案错误地解释了OCR错误，原文指出'0B'是原始OCR输出，其中'B'是错误识别的字符，但并未说明原本应为'8'；实际被误识别的是整个'0B'部分，而非单 | The full corrected date is 2026-08-09. The month's second digit (originally '8') |
| ocr_noise_register_v6:gen_ans_7 | answerable | wrong_answer | 系统答案错误地声称没有字符在两个字段中同时被消歧，但原文明确显示 digit zero 和 capital O 在 item code 中被消歧，而 digit | In the item code, digit '0' (zero) and capital 'O' are explicitly disambiguated, |
| nested_exception_policy_v6:gen_ref_0 | refusal | should_have_refused | 问题询问涉及国产设备的临床研究，但原文未提及国产设备的例外情况，系统应拒答而非推断为15天 | 15 business days. |
| timeline_sla_v6:gen_ans_5 | answerable | wrong_answer | 系统答案错误地计算为从5月12日到5月31日共20天，但问题要求的是Phase 1结束（2026-05-11）到Phase 3开始（2026-06-01）之间的 | 20 days (from May 12 to May 31, 2026). |
| timeline_sla_v6:gen_ans_6 | answerable | wrong_answer | 系统答案46天与原文三个阶段实际总天数37天不符，计算错误。 | 46 calendar days |
| adversarial_citation_v6:gen_ref_1 | refusal | should_have_refused | 问题属于拒答题，文档中无依据说明团队领导是否有权批准删除请求，即使有记录经理的书面授权，因此系统不应给出实质性答案。 | No, a team lead cannot approve deletion requests even with written authorization |