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

## 4. 系统结构（端云分层协同）

研答通是**端云分层协同**架构，正面回应赛题一"端侧/云端协同应用"命题：解析、切块、**本地语义编码**、混合检索、上下文压缩、证据定位等"重而可本地化"的工作在端侧/近端完成——其中**近端跑一个本地句向量模型（BGE-small-zh-v1.5 ONNX，纯 CPU、零云依赖）**，是真实的端侧 ML 算力实体（小模型在端理解、大模型在云生成）；只把命中任务意图的**必要片段**上云交无问芯穹 MaaS **生成**。详见 `ARCHITECTURE.md`（Edge | 近端 | Cloud 分层图）。

### 端侧（浏览器，React + TypeScript + Vite）

- 会话建立（HttpOnly cookie 本地态）、文件上传、任务输入、结果展示
- **PDF 证据渲染层**：citation 点击 → bbox 高亮叠加、坐标映射、缩放翻页
- **手动标注与标注页导出**（证据呈现 + 交互计算在端侧完成）

### 近端服务（FastAPI 后端，部署节点本地，非云端大模型）

- 文件接收与 PDF 解析（PyMuPDF 保留页级 block/line/bbox）
- 文本分块、**本地句向量编码（BGE-small-zh-v1.5 ONNX，CPU）** + 词法/语义混合检索（双语 hint + 意图 fallback；缺模型/失败自动回退纯词法）
- **上下文规划与 Token 压缩**（按任务意图选片段，是协同的核心节省环节）
- bbox 子串定位、逐字证据校验、citation 附着
- 记录本地 request_id、**平台 platform_request_id**、token、latency、outcome 到 JSONL

### 云端（无问芯穹 MaaS）

- `ask / summary / outline` 大模型**生成**；端侧/近端只上送必要片段

> 诚实标注（一）：PDF 页面图像由近端服务用 PyMuPDF 栅格化后下发，端侧负责坐标映射与高亮/标注交互，不夸大为"端侧大模型推理"。协同的量化收益见第 7 节 Token 压缩。
>
> 诚实标注（二）：近端的本地句向量模型是真实在本机 CPU 上的 ML 前向推理、零云依赖、物理可下沉边缘；但它与已高度调优的词法检索在固定基准上**持平、零回归**（见 `evidence/reports/edge_hybrid_eval.md`），价值在端侧实体与措辞鲁棒性，**不包装为"检索显著提升"**。

## 5. 当前主技术链路

### 5.1 文档解析

- 支持 `PDF / TXT / Markdown`
- PDF 解析保留页级结构，供 citation 与 PDF 回链使用

### 5.2 ask 路径（单层 agentic 检索循环）

1. 用户提问
2. 近端检索相关 chunk
3. 组织 ask 上下文
4. 调用无问芯穹模型
5. **模型自评证据是否充分**：若不足，模型给出 `need_more=true` + `followup_query`
6. **不足则用 `followup_query` 补检索新片段（排除已用 chunk）并再问一次**，最多 2 轮收敛（`agent_iterations / query_rewrites` 落日志）
7. 提取 `used_chunk_ids / evidence_quotes`，对每条 quote 做原文子串校验（校验不过即丢弃，引用不可伪造）
8. 组装 citation，回到 PDF 页面做 bbox 证据显示

> 全程不改变拒答与证据契约：干净拒答仍拒答；模型不索要补充时退化为单轮。代码 `task_service.py::_run_agentic_ask`，测试 `test_agentic_ask_reretrieves_with_followup_query`。

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

来源：`evidence/experiments/20260420_g3_strict_rehearsal.md`（首批 3 轮）+ `evidence/experiments/20260423_g3_continuation.md`（续 3 轮）

- 已累计 `6` 轮连续 strict fresh-upload 记录（`6 / 6` 通过，每轮使用新 `file_id`）
- 两次 answerable 全部保持 `declared`
- refusal 全部保持 `retrieval_gate` 或 `llm_refused`，fallback `0 / 6`
- 可作为当前更强的 judged-demo reproducibility evidence

### 6.5 judge-facing 截图集

当前界面于 2026-05-29 重拍（旧 `20260419_*` 为历史界面）：

1. `20260529_gold_ask_research_focus.png`
2. `20260529_gold_pdf_render.png`
3. `20260529_gold_ask_rank_accuracy.png`
4. `20260529_gold_refusal.png`

## 7. 当前产品价值

面向的不是开放域聊天，而是答辩和复核中的“说得出处”问题。

当前价值点：

1. 长文阅读时，快速定位核心信息
2. 问答时，答案能回到 PDF 原文
3. 离题问题时，系统显式拒答，避免编造
4. 对答辩准备场景，citation 与 PDF back-link 的价值高于泛化生成

### 7.1 端云协同与 Token 压缩（加分项 #4）

端侧/近端三层预处理（解析 → 切块 → 按任务意图选片段）让只有必要上下文上云：长文档 `ask` 平均节省 **86.6%** input token、峰值 **93.1%**（Attention 论文 `10,263 → 704` tokens）。脚本 `scripts/eval_token_compression.py` 评委现场可复跑（`tiktoken` 已入 `requirements.txt`）。短文档诚实标注为非压缩目标（约 -4%）。这条既命中 Token 压缩加分项，又是端侧/云端协同的量化收益。详见 `evidence/reports/token_compression_eval.md`。

### 7.2 商业化潜力（加分项 #2）

主打 **B 端高校实验室/课题组席位订阅** + C 端答辩季入口。差异化不是"答得流畅"而是"答得可验证"（bbox 级回链 + 逐字校验 + 离题拒答），契合学术场景"说得出处"的刚需；毛利侧由 token 压缩支撑（每次问答边际推理成本压低近一个数量级）。完整市场量级 / 竞品差异 / 单位经济 / 获客论证见 `COMMERCIALIZATION_CASE.md`。

## 8. 当前边界与诚实说明

1. 当前最强、最适合比赛主展示的能力是 `ask`，不是 `summary / outline`
2. `summary / outline` 已支持，但 grounding 语义弱于 `ask`
3. 当前 judged-demo 最强证据是锁定 gold-sample 路径，不是开放域产品泛化证明
4. 当前 `G3` 最强记录已升级为 strict six-run batch（`6 / 6`），但仍不应包装成开放域泛化证明

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
