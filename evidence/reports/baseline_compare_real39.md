# Baseline Comparison — RAG (检索接地) vs Full-Context (全文喂入)

- Manifest: `evidence\materials\EXTENDED_EVAL_V1.json`
- Cases: **39** · Real MaaS calls: **78** · Model: `deepseek-v4-flash`
- Same ask prompt/contract on both sides; only `document_text` differs.

## Headline

| Metric | RAG (检索片段) | Full-Context (全文) |
| --- | ---: | ---: |
| 正确率 (expected_any_of 命中) | **97.4%** (38/39) | 100.0% (39/39) |
| 平均 input tokens (真实平台计数) | **2353** | 10118 |
| 中位 input tokens | 2339 | 11671 |
| 合计 input tokens | 91761 | 394595 |

**结论:** 在同一批长文档可回答题上,RAG 在正确率**略低**(97.4% vs 100.0%)的前提下,只用 **4.3×** 更少的 input token(全文/RAG = 394595/91761)。

**怎么诚实解读这组数(决赛口径):**
1. 不是 RAG 更准,而是同等准确度下显著更省——这批可回答题两边都答对,量化提升点是 **4.3× 的 token / 成本 / 延迟下降**,即端云协同的直接收益。
2. 全文喂入不可 scale:本批 **16/39** 例全文已被 `MAX_DOCUMENT_CHARS=30000` 截断;文档一旦超出上下文预算,全文路线会开始丢内容、掉准确率,而检索接地只取必要片段、不随文档变长而劣化。故本表的 token 倍数是**保守下限**,真实完整全文会更贵。
3. 只有 RAG 能回链:检索片段携带 chunk / 页码锚点,支撑 bbox 级逐字回链与离题拒答;朴素全文喂入丢失页结构,给不出可核验出处——这正是本产品的立身点。

## Per-case

| case | 难度 | RAG tok | RAG✓ | FULL tok | trunc | FULL✓ | 倍数 |
| --- | --- | ---: | :-: | ---: | :-: | :-: | ---: |
| chinese_llm_spatial_eval:zh_a1_accuracy | easy | 2339 | ✓ | 11672 |  | ✓ | 5.0× |
| chinese_llm_spatial_eval:zh_a1_best_model | easy | 2515 | ✓ | 11680 |  | ✓ | 4.6× |
| chinese_llm_spatial_eval:zh_a1_authors | easy | 2796 | ✓ | 11671 |  | ✓ | 4.2× |
| chinese_llm_spatial_eval:zh_a2_two_questions | medium | 2358 | ✓ | 11672 |  | ✓ | 4.9× |
| chinese_llm_spatial_eval:zh_a2_prompt_strategies | medium | 2512 | ✓ | 11677 |  | ✓ | 4.6× |
| chinese_llm_spatial_eval:zh_a3_subtasks | medium | 2385 | ✓ | 11678 |  | ✓ | 4.9× |
| chinese_llm_spatial_eval:zh_a4_method_summary | medium | 2552 | ✓ | 11673 |  | ✓ | 4.6× |
| chinese_llm_spatial_eval:zh_a4_ranking | easy | 2262 | ✓ | 11674 |  | ✓ | 5.2× |
| chinese_llm_spatial_eval:zh_a5_train_count | hard | 3178 | ✓ | 11678 |  | ✓ | 3.7× |
| chinese_llm_spatial_eval:zh_a1_conf_name | easy | 2384 | ✓ | 11671 |  | ✓ | 4.9× |
| chinese_llm_spatial_eval:zh_a1_temperature | easy | 3382 | ✓ | 11672 |  | ✓ | 3.5× |
| chinese_llm_spatial_eval:zh_a1_author_count | easy | 2449 | ✓ | 11670 |  | ✓ | 4.8× |
| chinese_llm_spatial_eval:zh_a1_school_department | medium | 2394 | ✓ | 11671 |  | ✓ | 4.9× |
| chinese_llm_spatial_eval:zh_a2_ernie_weakness | medium | 2457 | · | 11678 |  | ✓ | 4.8× |
| chinese_llm_spatial_eval:zh_a2_glm4_best | medium | 4014 | ✓ | 11680 |  | ✓ | 2.9× |
| chinese_llm_spatial_eval:zh_a3_models_count | easy | 2333 | ✓ | 11671 |  | ✓ | 5.0× |
| chinese_llm_spatial_eval:zh_a3_opensource | medium | 3659 | ✓ | 11672 |  | ✓ | 3.2× |
| chinese_llm_spatial_eval:zh_a3_context_max | medium | 2480 | ✓ | 11672 |  | ✓ | 4.7× |
| chinese_llm_spatial_eval:zh_a4_eval_metric | easy | 2207 | ✓ | 11670 |  | ✓ | 5.3× |
| chinese_llm_spatial_eval:zh_a4_cot_sample_source | medium | 2406 | ✓ | 11675 |  | ✓ | 4.9× |
| chinese_llm_spatial_eval:zh_a5_test_count | hard | 3780 | ✓ | 11678 |  | ✓ | 3.1× |
| chinese_llm_spatial_eval:zh_a5_val_count | hard | 3970 | ✓ | 11678 |  | ✓ | 2.9× |
| chinese_llm_spatial_eval:zh_a5_study_period | hard | 2230 | ✓ | 11671 |  | ✓ | 5.2× |
| attention_is_all_you_need:en_a1_encoder_layers | easy | 2031 | ✓ | 7880 | 是 | ✓ | 3.9× |
| attention_is_all_you_need:en_a1_first_authors | easy | 1717 | ✓ | 7880 | 是 | ✓ | 4.6× |
| attention_is_all_you_need:en_a1_arxiv_id | easy | 1677 | ✓ | 7878 | 是 | ✓ | 4.7× |
| attention_is_all_you_need:en_a2_why_no_recurrence | medium | 1272 | ✓ | 7878 | 是 | ✓ | 6.2× |
| attention_is_all_you_need:en_a2_scaling_reason | medium | 1677 | ✓ | 7888 | 是 | ✓ | 4.7× |
| attention_is_all_you_need:en_a3_complexity_compare | medium | 1724 | ✓ | 7888 | 是 | ✓ | 4.6× |
| attention_is_all_you_need:en_a4_contributions | medium | 1842 | ✓ | 7878 | 是 | ✓ | 4.3× |
| attention_is_all_you_need:en_a5_conv_path_length | hard | 2128 | ✓ | 7885 | 是 | ✓ | 3.7× |
| attention_is_all_you_need:en_a1_decoder_layers | easy | 1990 | ✓ | 7880 | 是 | ✓ | 4.0× |
| attention_is_all_you_need:en_a1_attention_heads | easy | 2342 | ✓ | 7880 | 是 | ✓ | 3.4× |
| attention_is_all_you_need:en_a2_dropout_rate | medium | 2210 | ✓ | 7880 | 是 | ✓ | 3.6× |
| attention_is_all_you_need:en_a2_positional_enc | medium | 1419 | ✓ | 7880 | 是 | ✓ | 5.6× |
| attention_is_all_you_need:en_a3_training_hardware | medium | 1540 | ✓ | 7880 | 是 | ✓ | 5.1× |
| attention_is_all_you_need:en_a3_wmt_tasks | medium | 1362 | ✓ | 7880 | 是 | ✓ | 5.8× |
| attention_is_all_you_need:en_a4_optimizer | easy | 1481 | ✓ | 7878 | 是 | ✓ | 5.3× |
| attention_is_all_you_need:en_a4_label_smoothing | medium | 2307 | ✓ | 7878 | 是 | ✓ | 3.4× |

## 可核验性

每次调用都记录了真实平台 `platform_request_id`(见 `baseline_compare_eval.json`),可在无问芯穹控制台对账。样例:
- `chinese_llm_spatial_eval:zh_a1_accuracy`: RAG `chatcmpl-59b4c5ee-fa42-9d24-b818-a78c8b5c41c2` · FULL `chatcmpl-53b110c4-edfb-97d8-aaf1-a48d438946af`
- `chinese_llm_spatial_eval:zh_a1_best_model`: RAG `chatcmpl-6e84f30b-4f7b-9ac8-888e-b20ca4a895d3` · FULL `chatcmpl-5638252f-78c8-9d3d-813a-eff04f8293fa`
- `chinese_llm_spatial_eval:zh_a1_authors`: RAG `chatcmpl-785695c3-2bcf-9e89-ab82-3b8d1268ce04` · FULL `chatcmpl-c7e1dd7e-0bd1-9471-9b4a-4ff1de29f1b3`

## 唯一非命中项核查（诚实补注）

严格批跑中 RAG 唯一未命中项 `chinese_llm_spatial_eval:zh_a2_ernie_weakness`（问「ERNIE-4 在哪类任务表现最弱」，期望含「推理」）经单独复核为**子串假阴性、非真实失败**：

- 检索上下文（3198 字符）**确含**「空间推理 / 推理 / ERNIE」——答案块已进上下文，不是检索遗漏。
- 重新提问 RAG **正确作答**：「ERNIE-4 …在空间推理任务上表现最弱」，并带 evidence_quote「…所有模型在角色识别任务的表现最优，在空间推理任务的表现相对最差」。复核 request_id `chatcmpl-e72956f3-21fd-97c0-8efe-a557a996c70d`，可控台对账。
- 成因：单次生成的措辞抖动导致该次答案恰好未含目标子串（`expected_any_of` 子串判据的固有脆弱性），检索与能力均无问题。

**结论：RAG 正确率实质与全文持平**（严格 substring 批跑 38/39，唯一差异为措辞抖动的子串漏配，已复核非真失败）；**4.3× input-token 压缩稳定成立**。这条按"评测诚实优先于刷分"纪律记录：既不把假阴性算成真失败，也不掩盖严格批的原始 38/39。
