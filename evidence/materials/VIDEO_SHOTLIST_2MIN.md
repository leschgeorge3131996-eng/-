# 研答通 2 分钟视频分镜稿

## 使用原则

- 优先录真实演示；如现场录制不稳，再用同口径截图补镜头。
- 全片围绕一份文档、一组固定题和一个核心价值点展开。
- 先展示结果，再补一句工程支撑。

## 分镜脚本

### 0-12s

画面：

- 标题页
- 项目名：`研答通`
- 副标题：`让每条回答都能回到 PDF 原文证据`

旁白：

“研答通面向论文阅读、报告复核和答辩准备。它最重要的能力不是生成答案，而是让每条回答都能回到 PDF 原文证据。”

### 12-24s

画面：

- 打开系统
- 展示锁定样例：`chinese_llm_spatial_eval.pdf`

旁白：

“我们用一篇真实中文论文做固定样例，演示路径不靠临场随机发挥，而是靠可复现的证据链。”

### 24-50s

画面：

- 输入：`这篇论文主要研究了什么问题？`
- 展示 `20260529_gold_ask_research_focus.png`

旁白：

“先问一个文档内问题。系统会先检索相关片段，再返回回答、citation 和证据区，所以这不是脱离原文的自由聊天。”

### 50-74s

画面：

- 点击 citation
- 展示 `20260529_gold_pdf_render.png`

旁白：

“点击 citation 后，可以直接回到 PDF 原页。这里不仅看到页码，还能看到证据位置和原文片段，这一步把回答变成可验证。”

### 74-96s

画面：

- 输入：`作者最终的方法排名和总体准确率分别是多少？`
- 展示 `20260529_gold_ask_rank_accuracy.png`

旁白：

“第二个问题验证的是具体数字也能回到原文。当前锁定结果是第六名、56.20%，并且同样带有 citation 和证据。”

### 96-112s

画面：

- 输入：`木星有几颗卫星？`
- 展示 `20260529_gold_refusal.png`

旁白：

“如果问题和文档无关，系统不会编造，而是直接拒答。对文档助手来说，这种边界控制同样重要。”

### 112-120s

画面：

- 结尾页
- 两行结论：
  - `锁定题组：2 answerable + 1 refusal`
  - `默认 QA：qwen3-235b-a22b-instruct-2507`

旁白：

“我们已经在真实运行环境下跑通 upload、ask、citation、PDF 回链和 refusal 闭环。研答通的核心价值，就是让每个结论都指得回原文。”

## 备选素材

- 主截图：
  - `20260529_gold_ask_research_focus.png`
  - `20260529_gold_pdf_render.png`
  - `20260529_gold_ask_rank_accuracy.png`
  - `20260529_gold_refusal.png`
- 内部附录：
  - `20260419_stats_panel.png`
  - `20260419_api_docs.png`
- 支撑报告：
  - `gold_sample_replay_real_summary_latest.md`
  - `gold_sample_qa_compare_latest.md`

## 剪辑注意

- 前 30 秒一定先把核心价值讲出来。
- 主线固定为：`upload -> ask -> citation -> PDF -> refusal`。
- 不要把 `stats panel` 放进主叙事。
- 不要把 broader replay 讲成主证据。
