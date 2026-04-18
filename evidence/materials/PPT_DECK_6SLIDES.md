# 研答通 PPT 六页稿

## 使用原则

- 全程只讲当前锁定的 gold-sample 路径
- 默认主叙事是“带证据回链的文档问答”，不是泛化聊天
- 一页只保留一个结论，少讲历史分支与试验过程

## Slide 1: 问题与定位

标题：

`研答通：带证据回链的论文/报告问答助手`

页面文案：

- 长文阅读慢，答辩和复核更需要“说得出处”
- 普通聊天工具能回答，但很难证明答案来自文档
- 我们把“答案必须能跳回原文”做成一条完整链路

建议配图：

- 项目名
- 一句话定义
- 如需副标题，可直接复用 `PROJECT_ONE_PAGER.md` 开头两段

讲述口径：

“我们不是做一个普通聊天壳，而是做一个面向论文与报告阅读、答辩准备的文档助手。最关键的不是生成得多流畅，而是每一条回答都能回到 PDF 原文证据。”

## Slide 2: 系统路径

标题：

`最短可验证链路`

页面文案：

- 上传文档
- 解析页级结构
- 检索相关片段
- 问答返回 citation
- 点击 citation 跳回 PDF 原文
- 纯离题问题直接拒答

建议配图：

- 可画成 `upload -> parse -> retrieve -> answer -> citation -> PDF -> refusal`
- 如需一张工程支撑页，附录再放 `20260418_api_docs.png`

讲述口径：

“这条路径不是概念图，而是已经在真实运行环境里验证通过的主链路。”

## Slide 3: 文档内问题回答

标题：

`问题 1：论文主要研究什么？`

页面文案：

- 当前锁定问题：`这篇论文主要研究了什么问题？`
- 回答和 citation 同时出现
- 证据片段来自文档，不是事后补页码

建议配图：

- `evidence/screenshots/20260418_gold_ask_research_focus.png`

讲述口径：

“先看 answerable 问题。系统并不是直接让模型自由回答，而是先找相关片段，再给出回答和引用页码、证据片段。”

## Slide 4: PDF 证据回链

标题：

`点击引用，回到 PDF 原文`

页面文案：

- citation 可直接打开对应页
- 页面内显示证据高亮
- 高亮旁同时保留原文片段文本

建议配图：

- `evidence/screenshots/20260418_gold_pdf_render.png`

讲述口径：

“我们强调的不是‘回答后再附一个页码’，而是能直接回到原 PDF 页面，看到对应证据位置和原文内容。”

## Slide 5: 数值问题与模型决策

标题：

`问题 2：具体结果也能稳定回链`

页面文案：

- 当前锁定问题：`作者最终的方法排名和总体准确率分别是多少？`
- 返回明确数值：`第六`、`56.20%`
- `qwen3-235b-a22b-instruct-2507` 作为主模型
- `qwen3-32b` 已验证可作为 fallback

建议配图：

- `evidence/screenshots/20260418_gold_ask_rank_accuracy.png`
- 如需支撑表格，可引用 `gold_sample_qa_compare_latest.md`

讲述口径：

“我们还专门比较了两种 QA 模型。两者都通过了这组固定题，但 235b 在广义问题上的 grounding 更完整，所以当前保持为默认。”

## Slide 6: 可靠性与结论

标题：

`离题不编造，才叫可靠`

页面文案：

- 当前锁定拒答问题：`木星有几颗卫星？`
- 检索未命中时直接拒答
- 当前真实 replay 结果：`2 answered + 1 refused`
- 核心差异点：证据回链的文档问答

建议配图：

- `evidence/screenshots/20260418_gold_refusal.png`

讲述口径：

“最后用纯离题问题验证可靠性。系统不是硬答，而是明确拒答。对评审来说，这比‘什么都能说一点’更重要。”

## 可选附录

### 附录 A: 统计/工程支撑

- `evidence/screenshots/20260418_stats_panel.png`
- `evidence/screenshots/20260418_api_docs.png`

### 附录 B: 权威报告

- `evidence/reports/gold_sample_replay_real_summary_latest.md`
- `evidence/reports/gold_sample_qa_compare_latest.md`

## 现场注意

- 不要临时替换样例文档
- 不要现场改固定题集
- 不要把更宽样例 replay 当成主证据
- 不要把登录/邀请码讲成产品亮点
