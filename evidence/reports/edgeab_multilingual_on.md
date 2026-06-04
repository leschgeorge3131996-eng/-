# 判分式评测（裁判初判）· EDGE_AB_MULTILINGUAL_20260604

> 答题：`deepseek-v4-flash` + 检索回链（真实链路）。裁判：`qwen3-235b-a22b-instruct-2507`（从严，不同模型）。
> **这是裁判初判，须由人复核所有 FAIL + 抽查 PASS 后才作数。**

## 汇总
- 总通过：**42/48（87.5%）**
- 可答题：26/32
- 拒答题：16/16（其中 0 个该拒未拒=潜在编造）
- 标签分布：{'correct': 26, 'over_refused': 6, 'correct_refusal': 16}

## 全部未通过（人需逐个复核）

| case_id | 题型 | 标签 | 裁判理由 | 系统答案(截断) |
|---|---|---|---|---|
| multilingual_contract_v6:r1_gen_ans_4 | answerable | over_refused | 问题为可答题，原文p1明确提到夜间支持需要法律团队（equipo legal）的预先批准，系统拒答错误。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| multilingual_contract_v6:r1_gen_ans_7 | answerable | over_refused | 问题可答，原文明确提到西班牙语注释中夜间支持需要法律团队预先批准，系统应答而非拒答。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| multilingual_contract_v6:r2_gen_ans_4 | answerable | over_refused | 问题为可答题，原文p1明确提到夜间支持需要法律团队的预先批准，系统拒答错误。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| multilingual_contract_v6:r2_gen_ans_7 | answerable | over_refused | 原文相关页[p1]明确提到夜间支持需要获得法律团队的预先批准（el soporte nocturno requiere aprobacion previa de | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| multilingual_contract_v6:r2_gen_ans_11 | answerable | over_refused | 问题为可答题，原文相关页明确包含西班牙语描述夜间支持要求的关键词 'soporte nocturno' 和 'aprobacion previa'，系统应答而非 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |
| multilingual_contract_v6:r2_gen_ans_16 | answerable | over_refused | 文档中明确提到了英语、中文、日本語和西班牙语的内容，系统应答出这四种语言而非拒答。 | 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。 |