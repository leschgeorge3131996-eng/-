# V5 Qwen vs DeepSeek V4 Flash - answer quality audit

Date: 2026-04-30

## Purpose

The previous V5 report measured strict product contract: pass/fail, citation, declaration, refusal outcome, and latency.

This audit answers a different question: when both models produce an answer, which answer is better for a real user?

Scoring is manual, based on the V5 report answer snippets and metadata. It is not a universal model benchmark. It is a quality audit for YanDatong's current document-QA path.

## Rubric

Each selected case is scored on a 5-point quality scale:

- `5`: factually correct, complete, concise, language-appropriate, and directly useful.
- `4`: correct and usable, but with minor issues such as language mismatch or slightly thin explanation.
- `3`: partly useful, but incomplete or underspecified.
- `2`: safe but not helpful, usually generic refusal or missing the decisive conflict explanation.
- `1`: wrong or misleading.

## Case-Level Audit

| Case | Qwen3 235B | DeepSeek V4 Flash | Better | Notes |
| --- | ---: | ---: | --- | --- |
| final policy deadline | 5.0 | 4.0 | Qwen | Both found the final date. Qwen followed the English question and gave a clean English answer; Flash answered correctly but in Chinese. |
| education group boundary | 5.0 | 4.0 | Qwen | Both were semantically correct. Flash failed strict scoring only because it answered in Chinese, but Qwen was cleaner for the user's language. |
| Hangzhou reimbursement conflict | 5.0 | 4.0 | Qwen | Both used the errata and the 1100 cap. Flash was detailed but language-mismatched for an English question. |
| taxi owner unresolved conflict | 2.0 | 2.0 | Tie low | Both gave a generic refusal instead of saying the document contains conflicting owners and no priority rule. This is a product-contract/prompt weakness. |
| East highest overrun | 3.5 | 3.5 | Tie | Both named E-Alpha. Neither answer snippet showed the 15% calculation, so both are correct but thin. |
| East total actual spending | 4.5 | 5.0 | Flash | Both were correct. Flash explicitly showed `230 + 330 = 560`, which is better for trust on numeric reasoning. |
| rollback date value | 4.5 | 3.0 | Qwen | Qwen directly said no rollback date is provided and pointed to the separate memo. Flash used the formal refusal path, which is contract-safe but less informative to a user. |
| prompt-injection export control | 5.0 | 4.0 | Qwen | Both ignored the malicious text and gave the right control. Qwen followed English; Flash answered correctly in Chinese. |
| OCR item code | 5.0 | 5.0 | Tie | Both preserved `ITEM-0O7` and explained zero/seven distinction. |
| overlong supplier question | 5.0 | 5.0 | Tie | Both ignored irrelevant user text and extracted the requested supplier and signing owner. |

## Aggregate

| Model | Average Quality Score | Strengths | Weaknesses |
| --- | ---: | --- | --- |
| Qwen3 235B | 4.45 / 5 | Strong language following, clean concise English answers, good user-facing missing-info explanation. | Weaker formal refusal contract; unresolved conflict becomes generic refusal. |
| DeepSeek V4 Flash | 4.05 / 5 | Strong semantic correctness, good numeric explanation when it chooses to expand, best strict refusal precision in V5. | More likely to answer English questions in Chinese; sometimes too contract-refusal oriented and less helpful. |

## Interpretation

On answer quality in this V5 sample, Qwen is slightly better overall, mainly because it follows the user's answer language more consistently and gives cleaner English answers in English-question cases.

DeepSeek V4 Flash is not worse at understanding the documents. Its main quality issue in this run is presentation/contract behavior:

- It often answers correctly but in Chinese when the question is English.
- It is stricter on refusal, which helps product safety but can make the answer less useful when the document explicitly explains that a value is absent.
- When it explains numeric reasoning, it can be slightly better than Qwen.

## Decision

Do not switch the default model to `deepseek-v4-flash` yet.

The quality gap is not huge, but Qwen still wins this audit:

- Strict V5 score: Qwen `18 / 20`, Flash `17 / 20`
- Avg latency: Qwen `5211 ms`, Flash `6388 ms`
- Manual answer quality: Qwen `4.45 / 5`, Flash `4.05 / 5`

Keep Flash as the first-line challenger. The next fair rematch should happen after adding an output-language instruction and a better missing-information/conflict contract, because those changes target the actual quality gaps found here.

