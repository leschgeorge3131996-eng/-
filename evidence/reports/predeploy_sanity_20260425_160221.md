# Predeploy Sanity Report — 20260425_160221

**Status:** READY

- Gold cases: `3/3` passed
- Risk checks: `11/11` passed

## Log hygiene

- Live `call_logs.jsonl` was already empty; no archive needed

## Gold cases

| Case | Kind | Pass | Outcome | Retrieval | Evidence | Pages | Latency | Note |
| --- | --- | --- | --- | --- | --- | --- | ---: | --- |
| answerable_research_focus | answerable | PASS | answered | matched | declared | [1, 2] | 6998 | - |
| answerable_rank_accuracy | answerable | PASS | answered | matched | declared | [1] | 4994 | - |
| refusal_jupiter_moons | refusal | PASS | refused | no_match | none | [] | 9 | - |

## Risk checks

| Check | Pass | Detail |
| --- | --- | --- |
| runtime_config | PASS | provider=infinigence_ai; qa=qwen3-235b-a22b-instruct-2507 |
| uploads_dir_writable | PASS | C:\Users\Administrator\Desktop\project\data\uploads |
| parsed_dir_writable | PASS | C:\Users\Administrator\Desktop\project\data\parsed |
| logs_dir_writable | PASS | C:\Users\Administrator\Desktop\project\data\logs |
| cache_dir_writable | PASS | C:\Users\Administrator\Desktop\project\data\cache |
| gold_pdf_present | PASS | C:\Users\Administrator\Desktop\project\evidence\samples\chinese_llm_spatial_eval.pdf (1035562 bytes) |
| upload_parse_metadata | PASS | status=parsed; pages=11; chunks=35; chars=22960 |
| page_text_fetch | PASS | page=1; chars=1746 |
| answerable_citation_presence | PASS | answerable_cases=2; cited_pages=[1, 2] |
| pdf_page_render | PASS | page=1; bytes=320041 |
| recent_log_summary | PASS | total=3; errors=0; p95=4994ms |

## Per-case answer snippets

### answerable_research_focus
- **Passed:** True
- **Answer snippet:** 这篇论文主要研究了大语言模型对空间语义的理解程度及其在具体任务中的优劣，基于第四届中文空间语义理解评测任务（SpaCE2024）进行实验分析，探讨大模型在空间语义理解方面的能力边界。

### answerable_rank_accuracy
- **Passed:** True
- **Answer snippet:** 作者最终的方法排名第六，总体准确率得分为56.20%。

### refusal_jupiter_moons
- **Passed:** True
- **Answer snippet:** 未在文档中检索到足够依据来回答这个问题。请换一个更贴近文档内容的问题，或上传更相关的文档。

## What to do if status is BLOCKED

1. Check backend env: `WUQIONG_BASE_URL` / `WUQIONG_API_KEY` / `MODEL_QA`.
2. Re-run this script after fixing env vars.
3. If still failing: fall back to the locked screenshot set (`evidence/screenshots/20260419_gold_*.png`) and use the spoken story unchanged — see `DEFENSE_DEMO_RISK_CHECKLIST.md`.
