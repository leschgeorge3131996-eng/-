# Baseline Comparison — RAG (检索接地) vs Full-Context (全文喂入)

- Manifest: `evidence\materials\EXTENDED_EVAL_V1.json` (long-PDF answerable cases only)
- Cases: **22** · Real MaaS calls: **44** · Model: `deepseek-v4-flash`
- Same ask prompt/contract on both sides; only `document_text` differs.

## Headline

| Metric | RAG (检索片段) | Full-Context (全文) |
| --- | ---: | ---: |
| 正确率 (expected_any_of 命中) | **100.0%** (22/22) | 100.0% (22/22) |
| 平均 input tokens (真实平台计数) | **2240** | 9778 |
| 中位 input tokens | 2300 | 9779 |
| 合计 input tokens | 49273 | 215113 |

**结论:** 在同一批长文档可回答题上,RAG 在正确率**持平**(100.0% vs 100.0%)的前提下,只用 **4.37×** 更少的 input token(全文/RAG = 215113/49273)。

**怎么诚实解读这组数(决赛口径):**
1. 不是 RAG 更准,而是同等准确度下显著更省——这批可回答题两边都答对,量化提升点是 **4.37× 的 token / 成本 / 延迟下降**,即端云协同的直接收益。
2. 全文喂入不可 scale:本批 **11/22** 例全文已被 `MAX_DOCUMENT_CHARS=30000` 截断;文档一旦超出上下文预算,全文路线会开始丢内容、掉准确率,而检索接地只取必要片段、不随文档变长而劣化。故本表的 token 倍数是**保守下限**,真实完整全文会更贵。
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

## 可核验性

每次调用都记录了真实平台 `platform_request_id`(见 `baseline_compare_eval.json`),可在无问芯穹控制台对账。样例:
- `chinese_llm_spatial_eval:zh_a1_accuracy`: RAG `chatcmpl-790bf2bc-243b-9308-b31f-bfa282b74263` · FULL `chatcmpl-9be74c5e-0ff7-9581-9a09-b42ea9523d55`
- `chinese_llm_spatial_eval:zh_a1_best_model`: RAG `chatcmpl-6a64bf2b-73f3-9d44-b49b-ecbc133b8a88` · FULL `chatcmpl-efaf8905-2ae6-961b-ba6a-6abda7464098`
- `chinese_llm_spatial_eval:zh_a1_authors`: RAG `chatcmpl-3209c58e-aeca-9bf4-9d1a-da7087a86223` · FULL `chatcmpl-315386ba-e664-964e-9579-6979c52a8d01`
