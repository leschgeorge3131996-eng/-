# Multi-Model Robustness — 无问芯穹 MaaS 跨家族验证

- Manifest: `evidence\materials\EXTENDED_EVAL_V1.json` (long-PDF answerable cases)
- Cases: **10** · Models: **6** · Real MaaS calls: **60**
- 同一检索接地上下文 + 同一 ask 契约，仅 QA 模型不同（`model_name_override`）。每次调用都带真实平台 `request_id`。

## 准确率（expected_any_of 命中）

| 模型 | 家族 | 正确 / 总数 | 准确率 | 错误数 | 样例 request_id |
| --- | --- | :-: | ---: | :-: | --- |
| `deepseek-v4-flash`（默认） | DeepSeek | 10 / 10 | 100.0% | 0 | `chatcmpl-11d54fb1-4874-9908-bc64-4248224a2d1f` |
| `deepseek-v4-pro` | DeepSeek | 10 / 10 | 100.0% | 0 | `chatcmpl-19f041d9-c625-995a-a5bb-ba6c17c770a7` |
| `qwen3-235b-a22b-instruct-2507`（rollback） | Qwen | 10 / 10 | 100.0% | 0 | `chatcmpl-f9f91c3a-d1b6-9e1b-9a5a-3f66acc37876` |
| `qwen3-32b` | Qwen | 10 / 10 | 100.0% | 0 | `chatcmpl-6b4cf9d9-c738-9380-b5a4-6d1637385f60` |
| `kimi-k2.5` | Kimi | 10 / 10 | 100.0% | 0 | `40350fef5ce5415fa51acac8b9cffa5e` |
| `glm-4.6` | GLM | 10 / 10 | 100.0% | 0 | `20260604163722543ab2bc03034ffd` |

## 怎么诚实解读

1. 这是**跨模型验证扫描**，不是「生产用六个模型」。生产默认仍是 `deepseek-v4-flash`、rollback `qwen3-235b`。
2. 价值在于：①真实使用无问芯穹平台 **DeepSeek / Qwen / Kimi / GLM 四大家族**（覆盖评分表点名模型）；②同一套检索接地 + ask 契约**跨厂商都能跑**，说明流水线不是过拟合到单一模型。
3. 每条调用可在控制台用 `request_id` 逐笔对账（见 `multi_model_eval.json`）。
4. 模型间分差只反映「在这组锁定题上的表现」，非泛化排名；不据此宣称某模型「最强」。
