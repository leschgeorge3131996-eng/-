# 判分式评测（裁判初判）· _overrefusal_docs

> 答题：`deepseek-v4-flash` + 检索回链（真实链路）。裁判：`qwen3-235b-a22b-instruct-2507`（从严，不同模型）。
> **这是裁判初判，须由人复核所有 FAIL + 抽查 PASS 后才作数。**

## 汇总
- 总通过：**20/22（90.9%）**
- 可答题：14/16
- 拒答题：6/6（其中 0 个该拒未拒=潜在编造）
- 标签分布：{'partial': 1, 'correct': 14, 'wrong_answer': 1, 'correct_refusal': 6}

## 全部未通过（人需逐个复核）

| case_id | 题型 | 标签 | 裁判理由 | 系统答案(截断) |
|---|---|---|---|---|
| attention_is_all_you_need:gen_ans_0 | answerable | partial | 系统答案错误地声称解码器层数未明确说明，但原文明确指出解码器也由N=6个相同层组成。 | 编码器由6层相同层组成（N=6）。解码器的层数在提供的文档片段中未明确说明。 |
| attention_is_all_you_need:gen_ans_2 | answerable | wrong_answer | 系统答案错误地声称文档中存在冲突，实际上原文p1明确指出在WMT 2014英法任务上BLEU为41.8，训练3.5天，无矛盾 | 文档中关于WMT 2014英法翻译任务的BLEU分数存在冲突：一个片段报告为41.0（Chunk 2823b35583c40893），另一个片段报告为41.8（ |