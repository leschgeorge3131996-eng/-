# 判分式评测（裁判初判）· EDGE_AB_MULTILINGUAL_20260604

> 答题：`deepseek-v4-flash` + 检索回链（真实链路）。裁判：`qwen3-235b-a22b-instruct-2507`（从严，不同模型）。
> **这是裁判初判，须由人复核所有 FAIL + 抽查 PASS 后才作数。**

## 汇总
- 总通过：**39/48（81.2%）**
- 可答题：23/32
- 拒答题：16/16（其中 0 个该拒未拒=潜在编造）
- 标签分布：{'correct': 23, 'over_refused': 9, 'correct_refusal': 16}

## 全部未通过（人需逐个复核）

| case_id | 题型 | 标签 | 裁判理由 | 系统答案(截断) |
|---|---|---|---|---|
| multilingual_contract_v6:r1_gen_ans_3 | answerable | over_refused | 系统拒答，但原文第一页明确提到日语备注中的最终交付截止日期是2027年01月15日，应可回答。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| multilingual_contract_v6:r1_gen_ans_4 | answerable | over_refused | 问题为可答题，原文p1明确提到夜间支持需要法律团队的预先批准，系统应答而非拒答。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| multilingual_contract_v6:r1_gen_ans_7 | answerable | over_refused | 问题可答，原文明确提到西班牙语注释中夜间支持需要法律团队预先批准，系统应答而非拒答。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| multilingual_contract_v6:r2_gen_ans_3 | answerable | over_refused | 问题为可答题，原文明确提到日语备忘录中的最终交付截止日期为2027年01月15日，系统应答而非拒答。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| multilingual_contract_v6:r2_gen_ans_4 | answerable | over_refused | 问题为【可答题】，原文p1明确提到夜间支持需要法律团队的预先批准，系统应答而非拒答。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| multilingual_contract_v6:r2_gen_ans_7 | answerable | over_refused | 问题为【可答题】，原文p1中Spanish note明确提到夜间支持需要法律团队的事先批准，系统应据此作答而非拒答。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| multilingual_contract_v6:r2_gen_ans_11 | answerable | over_refused | 问题为【可答题】，原文p1中明确有西班牙语描述夜间支持要求的关键词'el soporte nocturno requiere aprobacion previa | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| multilingual_contract_v6:r2_gen_ans_16 | answerable | over_refused | 文档中明确提到了英语、中文、日语和西班牙语的内容，系统应答出这四种语言而非拒答。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| multilingual_contract_v6:r2_gen_ans_17 | answerable | over_refused | 问题可答，答案在原文p1的English clause部分明确提到紧急支持响应时间要求。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |