# 判分式评测（裁判初判）· EXTENDED_EVAL_V1

> 答题：`deepseek-v4-flash` + 检索回链（真实链路）。裁判：`qwen3-235b-a22b-instruct-2507`（从严，不同模型）。
> **这是裁判初判，须由人复核所有 FAIL + 抽查 PASS 后才作数。**

## 汇总
- 总通过：**46/51（90.2%）**
- 可答题：38/43
- 拒答题：8/8（其中 0 个该拒未拒=潜在编造）
- 标签分布：{'correct': 38, 'wrong_answer': 3, 'correct_refusal': 8, 'judge_error': 1, 'ungrounded': 1}

## 全部未通过（人需逐个复核）

| case_id | 题型 | 标签 | 裁判理由 | 系统答案(截断) |
|---|---|---|---|---|
| chinese_llm_spatial_eval:zh_a2_prompt_strategies | answerable | wrong_answer | 系统答案将‘普通提示’称为‘Vanilla Prompt’，但参考要点中未提此名称，且区别描述超出证据范围，与参考要点不一致 | 论文中提到了三种提示词策略：普通提示（Vanilla Prompt）、工作流（Workflow）和思维链（Chain of Thought, CoT）。它们的区 |
| chinese_llm_spatial_eval:zh_a1_conf_name | answerable | judge_error | 裁判异常 <urlopen error [SSL: UNEXPECTED_EOF_WHILE_READING] EOF occurred in violatio | 本论文发表在第二十三届中国计算语言学大会（CCL 2024）上。 |
| chinese_llm_spatial_eval:zh_a5_study_period | answerable | ungrounded | 系统答案未被引用证据支撑，且参考要点仅提及'2024年5月'，无法支持具体日期范围。 | 本研究开展日期为2024年5月1日至5月17日。 |
| attention_is_all_you_need:en_a3_complexity_compare | answerable | wrong_answer | 系统答案中给出的自注意力复杂度O(n²·d)与引用证据中的O(n²)不一致，且未准确反映参考要点中强调的序列长度n的平方关系。 | Self-attention layers have a per-layer computational complexity of O(n²·d), whil |
| attention_is_all_you_need:en_a5_conv_path_length | answerable | wrong_answer | 系统答案O(log_k(n))与参考要点log；O(log不一致，且表中实际为O(logk(n))，表述错误 | According to Table 1, the maximum path length for convolutional layers is O(log_ |