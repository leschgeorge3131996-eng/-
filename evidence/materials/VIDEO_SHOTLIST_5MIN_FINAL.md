# 研答通 5分钟正式视频分镜稿

## 使用原则

- 优先录真实运行路径；若现场录屏不稳，再用同口径截图补镜头。
- 全片只围绕一份文档、一组固定问题和一条主链路展开。
- 主线固定为：`upload -> ask -> citation -> PDF -> refusal`。
- `strict G3` 只作为片尾可信度证据，不拍成长串日志操作。
- 不把登录、邀请码、`stats panel`、`api docs` 放进主叙事。

## 锁定素材

- 样例文档：`evidence/samples/chinese_llm_spatial_eval.pdf`
- 问题 1：`这篇论文主要研究了什么问题？`
- 问题 2：`作者最终的方法排名和总体准确率分别是多少？`
- refusal：`木星有几颗卫星？`
- 核心截图：
  - `20260419_gold_ask_research_focus.png`
  - `20260419_gold_pdf_render.png`
  - `20260419_gold_ask_rank_accuracy.png`
  - `20260419_gold_refusal.png`

## 分镜脚本

### 0-20s 开场

画面：

- 标题页
- 项目名：`研答通`
- 副标题：`让每条回答都能回到 PDF 原文证据`

旁白：

“研答通面向论文阅读、报告复核和答辩准备。它最核心的能力不是生成答案，而是让每条回答都能回到 PDF 原文证据。”

### 20-50s 场景痛点

画面：

- 简单图形或关键词动画：
  - 长文阅读慢
  - 普通聊天难举证
  - 答辩需要说出依据

旁白：

“在论文和报告场景里，真正的痛点不是答不出来，而是说不出依据。普通聊天工具能给结论，却很难证明结论来自原文，这会直接影响复核和答辩的可信度。”

### 50-85s 产品定位与主链路

画面：

- 流程图：
  - `upload`
  - `ask`
  - `citation`
  - `PDF`
  - `refusal`

旁白：

“所以我们把最短可验证链路固定成五步：上传文档、提问、返回 citation、跳回 PDF、离题拒答。评委看到的不是概念图，而是一条当前真实运行环境里已经跑通的路径。”

### 85-125s 锁定样例与问题 1

画面：

- 展示锁定文档
- 输入问题 1
- 切到 `20260419_gold_ask_research_focus.png`

旁白：

“正式演示时我们只用一份锁定样例文档，避免临场换题。先问第一个文档内问题：这篇论文主要研究了什么问题。系统不是直接把问题丢给模型，而是先检索相关片段，再返回回答、citation 和证据片段。”

### 125-160s citation 回链到 PDF

画面：

- 点击 citation
- 展示 `20260419_gold_pdf_render.png`

旁白：

“点击 citation 以后，界面会直接回到 PDF 原页。这里重要的不是多了一个页码，而是用户能在同一视图内看到证据位置和原文片段。对论文阅读和答辩场景来说，这一步把‘能回答’变成了‘能验证’。”

### 160-205s 问题 2：具体数值能否回原文

画面：

- 输入问题 2
- 展示 `20260419_gold_ask_rank_accuracy.png`

旁白：

“第二个问题验证的是具体数值能不能稳定回到原文。当前锁定结果是第六名、总体准确率 56.20%。这一步说明系统不只会回答概括类问题，也能把明确结论和 citation 一起落回原文。”

### 205-235s refusal：离题问题不编造

画面：

- 输入 refusal 问题
- 展示 `20260419_gold_refusal.png`

旁白：

“如果问题和文档完全无关，系统不会为了看起来聪明而硬答，而是直接拒答。这里 refusal 走的是 `retrieval_no_match`，说明边界控制也是主链路的一部分。”

### 235-265s 平台与模型决策

画面：

- 两行对比卡片：
  - `qwen3-235b-a22b-instruct-2507: 3 / 3`
  - `qwen3-32b: 3 / 3`
- 底部两行：
  - `default = deepseek-v4-flash`（V6 contract-patch holdout 后切换）
  - `rollback = qwen3-235b-a22b-instruct-2507`

旁白：

“当前锁定题组已经完成双模型 `3 / 3` 验证，证明平台路径真实可跑。我们在这之后又跑了一轮 V6 contract-patch holdout，`deepseek-v4-flash` 在 `72` 道题上拿到 `71`，超过 `qwen3-235b` 的 `56`，所以当前默认 QA 切到 Flash；`235b` 保留为 rollback fallback，summary 和 outline 仍跑在 `235b`。”

### 265-290s strict G3 复现证据

画面：

- 简洁数据页：
  - `strict G3: 3 / 3`
  - `fresh-upload`
  - `13.5s / 12.9s / 15.8s`
  - `fallback: 0 / 3`

旁白：

“在锁定样例和锁定题组下，我们还做了 strict G3 三连跑。三轮都是 fresh-upload 条件，三轮全部通过，两次 answerable 都保持 declared，离题都保持 retrieval_no_match，并且没有触发 fallback。”

### 290-300s 收尾

画面：

- 收尾页
- 关键词：
  - `evidence-backed QA`
  - `return to PDF`
  - `reproducible judged-demo path`

旁白：

“研答通的差异点不是更会聊天，而是把 evidence-backed QA 做成了可演示、可复现、可追溯的闭环。谢谢各位评审。”

## 剪辑建议

- 前 `60` 秒一定先把问题和价值讲清楚，不要一上来就堆功能。
- 中段把 `Q1 -> PDF` 做成一口气的连续动作，这是最强记忆点。
- `Q2` 和 `refusal` 只要够清楚，不要剪得过长。
- `strict G3` 页只保留四个数字，不展示长日志。

## 备用镜头

- 如果 live 录屏延迟明显偏高，优先保留：
  - `20260419_gold_ask_research_focus.png`
  - `20260419_gold_pdf_render.png`
  - `20260419_gold_ask_rank_accuracy.png`
  - `20260419_gold_refusal.png`
- 如果需要补一张可信度页，再使用：
  - `gold_sample_qa_compare_latest.md`
  - `20260420_g3_strict_rehearsal.md`
