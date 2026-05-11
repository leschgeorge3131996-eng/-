# 研答通产品及技术文档

## 1. 作品概述

研答通是一个面向论文阅读、报告复核、答辩准备的文档助手。当前比赛主链路里，最强能力不是泛化聊天，而是针对 PDF 文档的带证据回链问答：

- 先上传文档
- 再检索相关片段
- 然后返回回答、citation、页码和证据片段
- 最后把用户带回 PDF 原文位置

当前最强演示链路为：

`upload -> ask -> citation -> PDF -> refusal`

## 2. 为什么这不是聊天壳

研答通与普通聊天工具的核心差异，在于“答案必须能回到原文”。

当前链路包含四层约束：

1. 解析层：
   - 保留 PDF 页级结构与文本块
2. 检索层：
   - 先选相关片段，再组织上下文
3. 生成层：
   - ask 路径要求返回结构化 evidence 依据
4. 呈现层：
   - citation 可回到 PDF 页面并显示证据位置

如果检索未命中，系统直接拒答，而不是开放域硬答。

## 3. 使用的无问芯穹平台能力

当前作品真实接入的云端能力来自 `Wuwen Xinqiong` 平台。

当前路径：

- Base URL：`https://cloud.infini-ai.com/maas/v1`
- 默认 QA 模型：`deepseek-v4-flash`（V6 contract-patch holdout 后从 `qwen3-235b-a22b-instruct-2507` 切换）
- rollback QA fallback：`qwen3-235b-a22b-instruct-2507`
- `summary` / `outline` 模型：`qwen3-235b-a22b-instruct-2507`
- 历史验证 fallback：`qwen3-32b`

平台能力在本作品中的落点：

1. ask 任务的主模型推理
2. summary / outline 任务的文档生成
3. judged-demo 路径中的真实 request id、token、latency 记录

平台使用主证明见：

- `PLATFORM_USAGE_EVIDENCE.md`

## 4. 系统结构

### 前端

- React + TypeScript + Vite
- 负责：
  - 会话建立
  - 文件上传
  - 结果展示
  - citation 点击与 PDF 预览

### 后端

- FastAPI
- 负责：
  - 文件接收与解析
  - ask / summary / outline 路由
  - 检索与上下文组织
  - 调用无问芯穹平台
  - 记录 request_id、token、latency、outcome

### 本地处理

- 文档解析
- 文本分块
- 轻量检索
- citation / bbox 附着
- 本地日志与证据目录

## 5. 当前主技术链路

### 5.1 文档解析

- 支持 `PDF / TXT / Markdown`
- PDF 解析保留页级结构，供 citation 与 PDF 回链使用

### 5.2 ask 路径

1. 用户提问
2. 后端检索相关 chunk
3. 组织 ask 上下文
4. 调用无问芯穹模型
5. 提取 `used_chunk_ids / evidence_quotes`
6. 组装 citation
7. 回到 PDF 页面做证据显示

### 5.3 refusal 路径

如果检索结果与问题无关：

- 不调用模型开放域硬答
- 直接返回 `retrieval_no_match`
- 明确告诉用户当前文档中没有足够依据

## 6. 当前最强验证证据

### 6.1 双模型 gold-sample 比较

来源：`evidence/reports/gold_sample_qa_compare_latest.md`

- `235b`：`3 / 3` 通过
- `32b`：`3 / 3` 通过

### 6.2 当前默认模型真实 replay

来源：`evidence/reports/gold_sample_replay_real_summary_latest.md`

- `2 answered + 1 refused`
- `0 error`

### 6.3 数值题 fresh real rerun

来源：`evidence/experiments/20260419_q2_declared_stability_check.md`

- `3 / 3` fresh real runs
- 当前记录的 `3` 次 fresh real runs 均返回 `declared evidence`

### 6.4 judged-demo rehearsal

来源：`evidence/experiments/20260420_g3_strict_rehearsal.md`

- 已有 `3` 次连续 strict fresh-upload 记录
- 两次 answerable 全部保持 `declared`
- refusal 全部保持 `retrieval_no_match`
- 可作为当前更强的 judged-demo reproducibility evidence

### 6.5 judge-facing 截图集

1. `20260419_gold_ask_research_focus.png`
2. `20260419_gold_pdf_render.png`
3. `20260419_gold_ask_rank_accuracy.png`
4. `20260419_gold_refusal.png`

## 7. 当前产品价值

面向的不是开放域聊天，而是答辩和复核中的“说得出处”问题。

当前价值点：

1. 长文阅读时，快速定位核心信息
2. 问答时，答案能回到 PDF 原文
3. 离题问题时，系统显式拒答，避免编造
4. 对答辩准备场景，citation 与 PDF back-link 的价值高于泛化生成

## 8. 当前边界与诚实说明

1. 当前最强、最适合比赛主展示的能力是 `ask`，不是 `summary / outline`
2. `summary / outline` 已支持，但 grounding 语义弱于 `ask`
3. 当前 judged-demo 最强证据是锁定 gold-sample 路径，不是开放域产品泛化证明
4. 当前 `G3` 最强记录已升级为 strict three-run batch，但仍不应包装成开放域泛化证明

## 9. 当前提交物结构

### 主材料

- `PROJECT_ONE_PAGER.md`
- `DEMO_SCRIPT_3MIN.md`
- `PPT_DECK_3PAGES_FINAL.md`
- `VIDEO_SHOTLIST_5MIN_FINAL.md`
- `deliverables/competition_kit/deck_3page_final.pdf`（当前为正式 repo-native 可打印基线）
- `deliverables/competition_kit/video_subtitles_5min_final.srt`（当前为正式 repo-native 字幕 / 旁白基线）
- `POSTER_COPY.md`
- `PLATFORM_USAGE_EVIDENCE.md`
- `HARD_EVIDENCE_SUMMARY.md`

### 归档基线

- `PPT_DECK_6SLIDES.md`（仅作旧压缩结构参考）
- `VIDEO_SHOTLIST_2MIN.md`（仅作旧节奏参考）
- `deliverables/competition_kit/deck.pdf`（旧 `6` 页可打印基线）
- `deliverables/competition_kit/video_subtitles.srt`（旧 `2` 分钟字幕基线）

### 权威证据

- `gold_sample_qa_compare_latest.md`
- `gold_sample_replay_real_summary_latest.md`
- `20260419_q2_declared_stability_check.md`
- `20260420_g3_strict_rehearsal.md`

## 10. 下一步收口方向

后续工作不再以扩功能为主，而以“把现有能力升级为 judge-proof 证据链”为主：

1. `3` 页 PPT 正式成片
2. `5` 分钟视频正式成片
3. 如最终演示环境变化，刷新四张核心截图
4. 导出最终 competition asset pack
5. 保持 judge-facing 文案与 strict `G3` 口径一致
