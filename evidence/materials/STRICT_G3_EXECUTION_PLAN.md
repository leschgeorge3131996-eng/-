# 严格版 G3 执行清单

## 目标

把当前“已有 `3` 次 warm-state self-rehearsal 记录”的状态，升级成更能经得住评委追问的严格版 `G3` 证据。

本轮不追求开放域稳定性，只追求锁定 gold-sample judged-demo path 的可复现性。

目标链路：

`upload -> ask -> citation -> PDF -> refusal`

## 通过标准

严格版 `G3` 建议按以下口径验收：

1. 第二操作员执行，不是当前主操作者本人
2. 至少 `3` 次连续成功
3. 每次都完成：
   - answerable 1
   - answerable 2
   - PDF jump / render
   - refusal
4. 每次都记录总时长
5. 至少有一轮接近 fresh 状态：
   - fresh browser
   - 或 fresh upload
6. answerable 结果保持 `declared`
7. fallback 是否触发必须明确记录

## 角色分工

### 你

负责：

1. 锁定环境与 runbook
2. 确认模型、题组、截图集、fallback 规则不再变
3. 现场旁观并记录异常
4. 跑后整理正式实验记录

不要做：

- 不要同时做主操作者
- 不要边演示边改题
- 不要临时切文档

### 第二操作员

负责：

1. 严格按 runbook 操作
2. 不临时发挥
3. 每轮记录开始时间、结束时间、是否成功
4. 发现异常时按 fallback 规则处理

### 记录员

如果人手够，建议单独安排。

负责：

1. 记录 wall-clock 时间
2. 记录 request id
3. 记录 `declared / candidate / retrieval_no_match`
4. 记录是否切到截图 fallback

如果人手不够，记录员由你兼任。

## 演练前冻结项

正式开始前，先锁死这几个点：

1. 样例文档：
   - `evidence/samples/chinese_llm_spatial_eval.pdf`
2. 固定题组：
   - `这篇论文主要研究了什么问题？`
   - `作者最终的方法排名和总体准确率分别是多少？`
   - `木星有几颗卫星？`
3. 主模型：
   - `qwen3-235b-a22b-instruct-2507`
4. 备用模型：
   - `qwen3-32b`
5. fallback 截图集：
   - `20260529_gold_ask_research_focus.png`
   - `20260529_gold_pdf_render.png`
   - `20260529_gold_ask_rank_accuracy.png`
   - `20260529_gold_refusal.png`

如果这些项还在变，就不要开严格版 `G3`。

## 演练矩阵

建议最少做这 `3` 轮：

### Run 1：fresh browser

要求：

- 关闭旧页面
- 新开浏览器
- 重新进入前端
- 重新上传锁定 PDF

目的：

- 验证第二操作员不是只会复用已有页面状态

### Run 2：warm-state judged-demo

要求：

- 按正式答辩最可能的 warmup 方式执行
- 保持题组顺序不变

目的：

- 验证最接近现场主路径的稳定性

### Run 3：repeatability

要求：

- 在同机同环境下再完整跑一轮
- 看是否仍然稳定保持 `declared`

目的：

- 证明不是偶然一次成功

## 每轮操作步骤

1. 打开应用
2. 上传锁定 PDF
3. 提问 Q1：
   - `这篇论文主要研究了什么问题？`
4. 检查：
   - answered
   - citations present
   - evidence visible
5. 打开 citation / PDF
6. 提问 Q2：
   - `作者最终的方法排名和总体准确率分别是多少？`
7. 检查：
   - answered
   - 包含 `第六`
   - 包含 `56.20%`
   - citation present
   - `declared`
8. 提问 refusal：
   - `木星有几颗卫星？`
9. 检查：
   - refused
   - `retrieval_status=no_match`
   - no citations
10. 记录总时长

## 每轮必须记录的字段

每轮至少记这几项：

1. 操作者
2. 机器
3. 浏览器
4. 是否 fresh browser
5. 是否 fresh upload
6. 是否 warmup
7. Q1 是否 `declared`
8. Q2 是否 `declared`
9. PDF jump 是否成功
10. refusal 是否成功
11. 是否使用 fallback
12. 三个 request id
13. 总时长
14. 异常备注

## 失败判定

出现以下任一情况，本轮记为失败：

1. Q1 或 Q2 没有 answered
2. Q2 数值错误
3. Q1 或 Q2 没有 citation
4. PDF jump 失败
5. refusal 没有走 `retrieval_no_match`
6. answerable 明显掉到 `candidate` 且无补救说明
7. 不得不临时改题或换文档

## fallback 规则

满足以下任一情况，立即切截图：

1. 延迟明显过长
2. PDF render 打不开
3. Q2 数值异常
4. answerable 掉到不可接受的证据状态

切图后要求：

1. 口径不变
2. 仍然按锁定题组讲
3. 记录本轮 fallback 原因

## 产出物

严格版 `G3` 跑完后，至少补这几样：

1. 一份新的实验记录文件
   - 建议命名：`evidence/experiments/20260420_g3_strict_rehearsal.md`
2. 一页摘要
   - 可直接并入 `HARD_EVIDENCE_SUMMARY.md`
3. request id 索引
   - 可补到 `PLATFORM_USAGE_EVIDENCE.md`
4. 如果最终环境变化了，刷新四张截图

## 你和组员今天就能做的最小版本

如果今晚只够做一轮，也建议先做这个最小版本：

1. 第二操作员上手
2. fresh browser
3. 重新上传 PDF
4. 完整跑 `Q1 -> PDF -> Q2 -> refusal`
5. 把三条 request id 和总时长记下来

这轮即使还不算严格版 `G3` 封板，也会显著提高你们的答辩底气。

## 跑完后的更新顺序

1. 更新实验记录
2. 更新 `HARD_EVIDENCE_SUMMARY.md`
3. 更新 `PLATFORM_USAGE_EVIDENCE.md`
4. 更新 `QA_BRIEF.md` 里的 G3 口径
5. 如果结果足够稳，再更新 PPT / 视频口径
