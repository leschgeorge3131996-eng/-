# 研答通 · 赛前优化审计（ultracode workflow · 2026-06-03）

> 56 个 agent 按 10 个评分维度并行审计 → 对抗式核验每条发现 → 综合。原始 45 条发现，核验后 **39 条真实优化点**。全程钉死「诚实>刷分、不碰核心、不过度工程、2周可落地」。

（按比赛分值排序 · 2026-06-03）

## 1. 一句话总评

**这是一个核心已做实、诚实度模范、远超同类的作品——技术能力(检索接地4.37×/Token压缩86.6%/三层评测)、平台对账(逐笔chatcmpl-id落库)、端侧实体(真ONNX前向+持久化索引+回退)三大硬维度都已是强项；剩下的几乎全是"最后一公里"的提交物兑现与口径收尾，唯一的真实技术硬伤是被自家828条日志证伪的`query_rewrites`全空（self-RAG差异化路径从未真实触发，需诚实降级而非刷分）。** 当前最大单点风险不在能力，而在**两件官方硬交付物(.pptx成片 + 5分钟视频成片)至今不存在为文件、且无人被追踪截止日**——源稿全齐，文件交不出就是0分。

我已亲核全部关键事实：828条`call_logs.jsonl`中`agent_iterations`={1:620, 2:195}、`query_rewrites`非空**0条**；全仓**无任何.pptx/.mp4/.mov/.webm**；`evidence/screenshots/`只有0418/0419/0529三批，**无20260602控制台截图**；eyebrow(App.tsx:695)确为"面向科研与智能办公的文档工作台"；srt:35确写"strict G3三连跑"而deck_3page_final.html:241写"六轮"；competition_kit对**agentic与商业化均0提及**、poster对**token压缩0提及**；`bbox_grounding`/`edge_latency`报告均不存在；COMPETITION_ASSET_PACK自身L102(flash默认)与L160(235b主选)打架。

---

## 2. P0 必做（高分影响 + 2 周可落地 + 低/中风险）

> 按对总分边际收益排序。P0 = 不做则直接丢分或交不出。

### P0-1 · 产出两件官方硬交付物的文件，并立即建立带截止日的单点追踪
- **动作**：① 在 `agent_handoff/TASK_BOARD.md` 的 `## Now` 顶部新增一行 live 追踪（非塞进 reviews/ 的 JSON）：`提交硬交付物：PPTX成片=组员X/截止06-10；5min视频成片=组员Y/截止06-12`——把散落在 SESSION_LOG(06-02) 与 two_week_plan JSON 里**无具名无日期**的工作项提升为有日期的单点追踪。② 在 `FINAL_SUBMISSION_CHECKLIST.md` 那条 PPT stop-ship 旁加兜底事实：`deck_3page_final.pdf 已实测3页16:9(1152×648)、含4.37×/deepseek-v4-flash/strict G3 6/6，必要时可直接当PDF版PPT提交`（已核实为真，是按时交付的安全网）。③ 给视频写明最小可交路径：`若来不及精剪→video_subtitles_5min_final.srt + 20260529_* 四张金标图 + 本机录屏出最小成片`。
- **评分项**：初赛主提交物 1、2（3页内PPT + 5分钟演示视频）——SUBMISSION_SPEC_CROSSWALK 列为硬性。
- **工作量**：低（纯文档，当天可完成追踪；成片本身是组员工作，但本条只补"无人被追踪"这一管理缺口）。
- **为什么值得做**：我已 Glob 全仓确认这两个二进制文件**不存在**。源稿再好，文件不产出=整张作品交不出，是 2 周窗口里收益最高的一动。

---

## 3. P1 应做

> 按对总分边际收益 + 维度分值排序。每条均已亲核为真实缺口。

### 平台对账(20分，全项目最硬维度之一——锁满分就差这几条)

**P1-A · 补 infini-ai 控制台截图（H3 的唯一裸缺证据）**
- 我已确认 `evidence/screenshots/` 无任何 20260602 控制台图。**需用户亲自登代金券号操作**（Claude 无法自完成）：登"大模型服务平台→用量统计→统计周期选2026-06-02当日"，截两张存 `evidence/screenshots/`：`20260602_console_usage_summary.png`(总次数/输入·输出token/失败数/模型名)、`20260602_console_usage_timeseries.png`(尖峰19:51–20:16)。
- **关键约束**：`platform_reconciliation_20260602.md` 的 H3 节(L63)已有正确诚实口径——"控制台只展示聚合+时间序列、UI不逐条暴露chatcmpl-id，故H3=控制台聚合×我方持有逐条id两者合证"。**务必保留这段，截图只佐证聚合量与时段，不要让文案暗示截图能逐条对上id**。② 引用替换要么直接改提交用的 `.md`、要么改 `build_platform_reconciliation.py` 模板再重跑（脚本会覆盖手改）。
- **收益高、成本风险极低**；但因逐条 chatcmpl-id + `_calls.jsonl` 文本证据已强（我核实 platform_reconciliation jsonl 11行中10行带chatcmpl-id），截图是视觉收口，P1 不到 P0。

**P1-B · 把平台对账三件套写进 FINAL_SUBMISSION_CHECKLIST 打包清单**
- 在 §5 主包清单补"平台对账载体"小组四行：`platform_reconciliation_<封板日>.md`、同名 `_calls.jsonl` 快照、`baseline_compare_eval.json`、`<封板日>_console_*.png`。用 `<封板日>` 占位（截图当前不存在），复用 TASK_BOARD 已追踪的"重跑3题→新鲜id→控制台并排截图"动作。纯文本补项，防"封板按字面 bullet 执行漏打包"。

**P1-C · 多模型路由 claim 诚实降级（5分加分①·平台利用率）**
- 我未单独核 summary/outline 调用数，但审计实证 live 日志 0 笔非-ask 留痕。**必做(5分钟)**：把 `SCORING_EVIDENCE_MATRIX.md` 与 `PLATFORM_USAGE_EVIDENCE.md` 措辞改为"QA主链路真实留痕含chatcmpl-id可对账；summary/outline多模型路由已在代码+config实现，现场主打ask"——**不要把"多模型"与"含request_id可对账"绑成同一句**。可选(封板时)：用领券账号在封板那次跑1次summary+1次outline，让chatcmpl-id落进同一份jsonl。

### 技术能力(40分，已远超同类——补这两处补齐最薄的证据腿)

**P1-D · agentic `query_rewrites` 全空的诚实降级【唯一被生产日志证伪的硬伤】**
- 我已亲核：828条日志 `agent_iterations`={1:620, 2:195}，195条 iter=2 的 `query_rewrites` **100%为空**（嵌套在`extra`字段里，递归查证非空0条）。"自评不足→改写query→补检索新片段"这条差异化路径**只活在 mock 单测里**。评委按 SCORING_MATRIX 提示"现场核验query_rewrites"会当场翻出0条。
- **第一步·必做·零风险(~1小时)**：`HARD_EVIDENCE_SUMMARY §9` / `ARCHITECTURE 设计点4` / `SCORING_MATRIX 加分项③` 措辞改为诚实分层——"证据自评+有界二次重试(iter≤2，195/815条触发二轮)；改写补检索分支已实现且单测覆盖，固定demo集上模型多单轮收敛，故生产日志query_rewrites多为空"，并**删除"可现场核验query_rewrites"这类把空字段当卖点的提示**。
- **第二步·可选·不刷分才做**：用真实API跑出1笔带platform_request_id的真·非空留痕。**避开两坑**：① 首轮须converged=False(召回chunk但模型给不出逐字quote)，否则L843双门不触发；② 须cache miss(L236缓存路径绕过`_run_agentic_ask`)。**红线**：绝不为逼出need_more改prompt/调阈值/调窄检索；试1-2道造不出就**停在第一步**。

**P1-E · bbox 证据回链端到端量化（产品立身点最薄的一环）**
- evidence-back-linking 是 canonical 一句话，但只有"某quote能否定位到行"的单测，无"N条真实citation有多少落到正确页正确行"的覆盖率。我已确认 `evidence/reports/` 无任何 bbox-grounding 报告。
- **动作**：写**只读**离线脚本 `scripts/bbox_grounding_eval.py` → `evidence/reports/bbox_grounding_eval.md`，复用 `judged_eval.py` 装配，对51题固定集逐条调 `match_snippet_to_line_bboxes`，统计三个真离线指标：①quote→bbox行级**可定位率** ②平均覆盖行数 ③片段回退触发率。**诚实护栏**：(a) 措辞用"可定位率"非"命中正确行准确率"（无人工gold行）；要声称"定位到正确行"需对~10条人工抽查、分开列；(b) 回退触发的**不计满分命中**，回退率本身是有用的诚实信号。零token、不碰 bbox_matcher/校验/回链/拒答任何核心。

### 端侧/云端协同(赛题核心主题，已诚实模范——补"可见性/可信闭环")

**P1-F · 端侧实体在隐藏账本可见（最高杠杆的端侧呈现）**
- 现状 UI 只有压缩(支柱二)可见，本地BGE模型(支柱一)完全活在文档/口头。**档1(立即可做，S)**：后端 TaskResult 加 `dense_retrieval_active: bool=False`，由 `retrieval_service.dense_enabled` 填充（routes注入期已确定，不碰retrieve/排序/拒答）；前端 ResultPanel 仅在 `?ledger=1` 分支加 meta-card：`端侧语义检索·本地BGE-small-zh CPU·{已启用/未启用(现场打开)}`。真实用户零感知。**档2(可选，M)**：再加 `dense_contributed_chunk_count` 展示"补召回N段"，需在 `_dense_augment_chunks` 去重前数 dense 独有chunk数透传——只读已发生的合并，不改主排序/阈值/拒答。

**P1-G · 端侧延迟/内存/体积实测（"可下沉边缘"从口号变硬数）**
- 现只有体积(91MB文档值)硬，延迟/内存全空。**动作**：写 `scripts/edge_latency_probe.py`（或在 edge_live_smoke 末尾加**独立计时块**，不要把 perf_counter 塞进 `EmbeddingService.encode` 生产热路径）→ `evidence/reports/edge_latency_<date>.md`：冷启ms/暖编码单条ms/暖编码批ms/DenseIndex.build ms、psutil量进程RSS增量MB、`getsize`量model.onnx实测字节。每项3次取中位，记录CPU型号/核数/线程。**诚实护栏**：① 标"本机/演示机代表值"，**不外推成"任意边缘节点"**；② 与既有5521ms端到端QA延迟明确区分；③ 只测了bge-small时**不得**凭空补bge-m3对比数。落地后 ARCHITECTURE 端侧表补一行。

**P1-H · 把 edge_live_smoke + EDGE flag 纳入彩排 must-pass（现场开端侧的计划当前只活在散文）**
- 我已确认 `predeploy_sanity.py` 对 edge_live_smoke / EDGE_EMBEDDING_ENABLED / 端侧 **零覆盖**——predeploy "READY" 是必要不充分，现场翻 flag 走的是从未验证过的代码路径(ONNX加载+warmup+DenseIndex首查懒建)。
- **动作(零代码)**：`GOLD_SAMPLE_RUNBOOK.md` 的 Pre-Demo Warmup + `DEFENSE_DEMO_RISK_CHECKLIST.md` 的 Pre-Demo Must Pass 各加端侧步骤：① 确认权重在位(`models/bge-small-zh-v1.5/onnx/model.onnx_data`~90MB，缺则离线下载 `onnx-community/bge-small-zh-v1.5-ONNX`)；② 设 `EDGE_EMBEDDING_ENABLED=true` 跑 `.venv/Scripts/python.exe scripts/edge_live_smoke.py`，全PASS(14/14)→现场可放心开端侧；任一FAIL→**降级为"词法+云端跑金标(固定集A/B已证开=关同分)+端侧走预录截图"**，不在台上硬开。**关键**：把它做成 best-effort 软门，不要变成能卡死整场demo的硬阻塞。

### 现场演示与答辩就绪(已强——补两个新增 live 表面的兜底)

**P1-I · 按新UI补拍6张 fallback 截图（含账本+端侧态）**
- 现4张兜底图是 20260529 旧UI，缺 `?ledger=1` 账本与端侧态。合并进 SESSION_LOG 已立项的"重拍4张gold图"——一次彩排录屏产6张(4主链路新UI + `20260603_ledger.png` + 端侧开启金标结果页)，命名 `20260603_gold_*`。账本图走 `scripts/dev.ps1` 起 `localhost:5173/?ledger=1` 手动截（绕开此前 Preview-MCP 30s超时坑）。注意账本"压缩%"分母bug已在 commit 5b46da6 修复，截图须显示"仅上送~12%"非旧"100%"。

**P1-J · 刷新"上场前30秒"自检清单到当前演示形态（3份一致）**
- `QA_FLASHCARD.md`(L72-79) + `DEFENSE_DEMO_RISK_CHECKLIST.md`(Pre-Demo Must Pass L27-39，我已确认它同样止步 predeploy exit 0) 各加两条勾项：`端侧flag已确定——演端侧则edge_live_smoke全PASS`、`若展示账本：?ledger=1面板platform request id非—`。同步刷新 `project_demo_prep` 记忆并标注 Flash 已是默认。纯文案。

### 产品能力(40分，无结构性缺口——只动这一行字)

**P1-K · 改首屏 eyebrow（评委读到的第一行字）**
- 我已确认 App.tsx:695 = "面向科研与智能办公的文档工作台"——"智能办公"正是定位备忘录点名要避免的泛化口径，且在视觉最高位(uppercase pill)。**只改这一行**为与 deck/poster 一致的差异化口径，如"引用可核验·论文/答辩文档助手"。可顺手清 README.md:166 同样残留（非UI、低优先）；**勿动** backend/tests 与 evidence/samples 里的"面向科研与智能办公场景"（那是测试夹具/demo正文，不是定位文案）。

### 加分项·智能体(5分，主看物完全缺位——这是5分加分项的最大杠杆)

**P1-L · deck + poster 补一行 agentic（评委主看物当前0提及）**
- 我已确认 competition_kit **全部文件对 agentic 零提及**。`deck_3page_final.html`(238-243行"锁定判断"列表) + `poster.html` 补一条，文案：`单层agentic检索循环：检索→模型自评证据是否充分→不足则改写query补检索再问，≤2轮收敛；agent_iterations/query_rewrites落call_logs.jsonl可对账`。**口径红线**：①数字只用已落档的（10笔/3笔触发，或只给定性+"日志可对账"），**绝不写132/26**（与P1-D诚实降级一致）；②附"证据饱和时二轮确认即答、不在时升级仍拒答不编"；③小字不挤答案区。**改完须重导 deck_3page_final.pdf / poster.pdf**(当前PDF时间戳06-02)。

**P1-M · agentic 现场UI可见（隐藏账本徽标）+ 接强遥测进材料**
- ① ResultPanel ledger 区按 `result.agent_iterations>1` 渲染只读徽标"智能体二轮：自评证据不足→再检索确认"。**事实修正**：types.ts(TaskResult接口L110后)需先补 `agent_iterations?: number; query_rewrites?: string[];`（后端JSON已出参但TS类型未声明）。徽标按实际值显示、不写死"二轮"、不暗示"二轮=必答出"。② `SCORING_EVIDENCE_MATRIX.md L34` + `HARD_EVIDENCE_SUMMARY §9` 追加指向 `voucher_eval_rerun_20260602.md`，措辞写"26笔触发二轮自评"而非"26次成功改写"（与P1-D一致）；③ `QA_BRIEF.md` 加一条"大模型+智能体"追问应答。

### 加分项·商业化(5分，论证已强但评委看不到)+ Token压缩(5分，证据最扎实)

**P1-N · 商业化论证搬进评委视野 + 补一行人民币换算**
- 我已确认 competition_kit **对商业化0提及**——整套叙事只活在不进主交付包的 `COMMERCIALIZATION_CASE.md`。且我已确认 §四单位经济止于"边际成本压低近一个数量级"，**无token→RMB那一行**。动作：① 把已写好的论证搬进 deck/poster/QA_BRIEF 至少一处（5分项按评委看到打分）；② COMMERCIALIZATION_CASE.md §四补一行可见算术：去无问芯穹官网核当日 deepseek-v4-flash input 单价(注明取价日期+"按公开报价估算、非成交价")× 实测2240 token = 单次云端input成本≈¥0.0X，× 月均次数对¥19定价给占比。**红线**：取真实当日价、不许为对齐结论挑价；若算出超个位数百分点应改旧断言而非调价。

**P1-O · Token压缩中文子集真实平台比 + 真实计数口径前置**
- ① `baseline_compare_eval.md` Headline 下补"按语言子集"小表（保留4.37×合计）：中文子集(11例全文未截断)真实平台 RAG/FULL=128418/28663=**4.48×**；英文子集(11例全文被MAX_DOCUMENT_CHARS=30000截断)=86695/20610=**4.21×(系保守下限)**。诚实标注"中文4.48×是完整全文真比值，英文偏小因FULL侧被截断"。复用 `--report-only` 纯读JSON分组，不发新调用。回填到 HARD_EVIDENCE_SUMMARY §8。② `SCORING_EVIDENCE_MATRIX.md`"追问3"(L138-143)当前**完全没有4.37×**，必补真实平台口径以便现场照念。

### 诚实口径一致性(横切，防一问就塌)

**P1-P · 修 strict-G3 三轮↔六轮自相矛盾【judge-facing双资产对照即露】**
- 我已确认 srt:35 写"三连跑/三轮"，deck_3page_final.html:241 写"六轮"。把 srt:35 改为照 `VIDEO_SHOTLIST_5MIN_FINAL.md`(已是六轮口径)的"strict G3六轮fresh-upload(首批3+续3)全通过…fallback 0/6"。顺手把 `FINAL_SUBMISSION_CHECKLIST.md` 残留的 `3`-run 改 `6`-run。**务必在录最终视频前改掉，别进成片。** 不要误改 `quantitative_eval_metrics.md`/HARD_EVIDENCE L104 的"strict G3三轮(9条请求)"——那是合法标注的量化评测子集，与稳定性主张是两件事。

**P1-Q · 修 COMPETITION_ASSET_PACK 自身打架（一致性总闸内部矛盾）**
- 我已确认 L102(默认flash) 与 L160("`235b` remains the primary choice") 冲突。L160 改为与 Fixed Demo Fact #4 一致："默认deepseek-v4-flash；两模型在锁定3题组3/3仅证明平台路径可跑，现场默认经V6 holdout(71/72)选定，235b为更稳rollback"。顺手统一 L40-41 截图编号为 20260529_*。纯文字、改完重跑 `export_competition_asset_pack.ps1`。

---

## 4. P2 可选 / 锦上添花

> 低成本、tail-risk 或非评分关键。时间紧可全部押后到彩排/部署卫生那一轮顺手做。

- **P2-a · predeploy 现场重跑防丢平台id**：在 GOLD_SAMPLE_RUNBOOK 加硬步骤"对账重跑前先 `move data/cache` 再跑 predeploy_sanity，跑后用 build_platform_reconciliation 人工确认3条 platform_request_id 均 chatcmpl-开头无None"。真正交付载体已有硬守卫兜底，故 P2。
- **P2-b · 冷启动彩排 SOP**：端侧/账本两个新增 live 表面在与正式演示**同一进程会话**下先 warmup 一次（端侧懒建落 `data/vectors/<file_id>.npz`）。纯文字，收益边界诚实标注（仅当现场主动展示时才兑现）。
- **P2-c · CAC/LTV 量级锚点**：COMMERCIALIZATION_CASE §四后加半页"LTV/CAC量级(假设区间)"，复用已有 ¥600-1200/席·年 × 续费率区间 × 试用年数给量级，CAC 走 land-and-expand 定性论证。标"假设区间非实测"。
- **P2-d · 竞品对比加来源脚注**：第三节表下加"2026-06口径自测/公开资料整理、非逐项实测"，贬损措辞软化为可证伪表述（"弱"→"未见稳定提供bbox级逐字校验回链"）。**只改这一处材料**，勿连带改PPT/poster以免引入资产不一致。
- **P2-e · Poster 补 Token 压缩卡**：我已确认 poster.html 对 token/86.6/4.37 **0匹配**。加1张card："长文ask平均省86.6%(峰值93%)；对照喂全文4.37×更省、准确率持平"。4.37× 必须连"准确率持平(100% vs 100%)"出现。改完重导 poster.pdf 确认仍1页。
- **P2-f · handoff 残留旧数 89.1%→86.6%**：`PROJECT_HANDOFF.md:335/337`、`TASK_BOARD.md:55`。**只改 handoff/board 当前态索引；SESSION_LOG 历史留痕不动**(项目"历史数字保留"惯例)。
- **P2-g · 86.6%(tiktoken) vs 4.37×(真实计数)口径前置**：HARD_EVIDENCE §8 把真实平台口径提到头条，SCORING_MATRIX 追问3补 4.37×。
- **P2-h · 归档资产口径清理**：deck.html(6页) 加"非提交版"banner 并从 `export_competition_pdfs.js` JOBS 移除其导出job（首选，与SESSION_LOG L45"故意保留"一致，不必维护不打算提交的归档）；VIDEO_SHOTLIST_2MIN.md / PPT_DECK_6SLIDES.md 加历史基线注记。回勾 FINAL_SUBMISSION_CHECKLIST L92。
- **P2-i · 封板控制文档脱期刷新**：FINAL_SUBMISSION_CHECKLIST Status Snapshot 重标到 2026-06-03、回写已完成项；README.md:72 的 20260419_* 改 20260529_*。内部文档、无评分影响。
- **P2-j · 拒答标签轻微漂移**：松开"strict G3 refusal都保持retrieval_no_match"的过窄绑定（srt:35 / deck:184 / PLATFORM_USAGE_EVIDENCE:158），改为"检索闸门或LLM兜底，均不编造"。以"代码+金标报告 retrieval_no_match"为demo主口径，禁止反向改金标。
- **P2-k · 重导最新 asset pack + 旧zip归档**：交付前重跑 `export_competition_asset_pack.ps1` 生成 20260603 新包；删/归档根目录 `review_bundle_20260424/27_*.zip`。**勿**去 MATERIALS_INDEX/SUBMISSION_PREP_GUIDE 改"指向旧包的指针"——它们根本没有指向 exports 的指针(误报)。

### P3（仅在全部就绪后顺手）
- 三任务切换首屏可见性：折叠头旁加极小静态说明"支持 问答/摘要/提纲·默认问答"（纯文案1处）。
- 冷启动 `?demo=1` 一键载入锁定样例：首选只做 runbook"不要刷新页面/保持热状态"文字补充；按钮版需给前端供锁定PDF，非纯查询参数小改，时间紧不做。

---

## 5. 明确"不要做"（防止白费力气 / 碰核心高风险 / 已够好）

1. **不要动核心检索/回链/拒答内核**——`task_service._run_agentic_ask`、`bbox_matcher`、`dense_rescue_sim` 阈值、融合/拒答判定全部**只读不改**。所有上述建议无一需要改这些。
2. **不要为抬高 agentic 触发率改 prompt / 调阈值 / 调窄检索**——那是刷分，违反诚实铁律。`query_rewrites` 全空的正确解法是**诚实降级措辞**(P1-D第一步)，不是逼模型。试1-2道造不出真实非空留痕就停。
3. **不要把默认 `.env` 的 EDGE_EMBEDDING_ENABLED 翻 true**——会让未下权重的克隆首查触发加载路径(虽有回退但徒增现场变量)；以"现场显式 export + 文档硬步骤"为准。
4. **不要把 edge_live_smoke 做成 predeploy 的硬阻断**——锁定中文金标开/关都安全，演示机若未下权重，硬失败会无谓挡住整场demo；做 soft 警示或藏在 `--require-edge` 后。
5. **不要重做任何已强项**：产品UI已过专业a11y审计(0 critical/0 high)、可见改动极小是设计使然——**别为凑数重做/重设计首屏布局**(答案区位置是硬约束)；Token压缩证据已最扎实(双线计分)、**别再造新评测**；端侧技术核心已诚实模范、**两周内绝不该动**。
6. **不要外推端侧实测数字**为"任意边缘节点"——只能说"该规格CPU实测"；不要凭空补 bge-m3 性能对比数(本轮只测 bge-small)。
7. **不要改历史留痕数字**：SESSION_LOG 的 89.1%→86.6% 历史记录、quantitative_eval 的"strict G3三轮(9条请求)"量化子集，都是当时真实留痕，按惯例保留。
8. **不要维护不打算提交的归档**：deck.html(6页) 走 banner+移除导出job，别花力气逐字改它的旧模型口径(轻度过度工程)。
9. **不要去改不存在的"指针"**：MATERIALS_INDEX/SUBMISSION_PREP_GUIDE 没有指向 exports 包的指针(已核实)，把它当指针错误去修是误报。

---

## 6. 若只做 3–5 件事（最高性价比 top 清单）

| # | 动作 | 评分项 | 为什么是最高 ROI |
|---|------|--------|------------------|
| **1** | **产出 .pptx + 5min视频成片文件，并在 TASK_BOARD 建带截止日的单点追踪**(P0-1) | 初赛主提交物1、2 | 文件不存在=整作品交不出。源稿全齐，唯一缺的是"产出+追踪"。零分风险 vs 满盘皆活。 |
| **2** | **agentic `query_rewrites` 全空诚实降级**(P1-D第一步，~1小时) | 加分③(5) + 技术40可信度 | 唯一被自家828条日志证伪的硬伤、评委一grep即翻出0条；最便宜的文案降级即可堵死，且是诚实人设的体现。 |
| **3** | **修两处 judge-facing 口径冲突：srt三轮↔deck六轮 + COMPETITION_ASSET_PACK 自打架**(P1-P, P1-Q) | 诚实一致性(乘数项) | 双资产对照即露、授人以柄削弱最强卖点(可复现+默认模型)；纯文字几分钟，必须在录最终视频前改。 |
| **4** | **改首屏 eyebrow + deck/poster补一行agentic + 商业化搬进评委视野**(P1-K, P1-L, P1-N) | 产品40 + 加分③(5) + 加分商业化(5) | 三处都是"已做好但评委看不到/第一眼降格"，纯文案/搬运即把已有强项变现到评委视野；agentic与商业化在主看物当前**0提及**。 |
| **5** | **端侧三件套纳入彩排 must-pass + 隐藏账本端侧可见**(P1-H, P1-F档1) | 赛题核心·端云协同 | predeploy 不覆盖端侧路径(已核实)，现场翻flag走未验证路径有冷启动盲区；档1让支柱一首次"看得见"，低风险高杠杆补主题命中。 |

**关键路径提示**：第1件是组员依赖项，越早建追踪越安全；第2-4件 Claude/用户当天即可完成（纯文档/前端小改）；第5件需在演示机彩排时拍板。所有 top-5 均不碰核心、不刷分、2周内可落地。

---

**已亲核的关键文件路径**（供后续落地直接定位）：
- `C:\Users\Administrator\Desktop\project\frontend\src\App.tsx`:695（eyebrow 待改）
- `C:\Users\Administrator\Desktop\project\data\logs\call_logs.jsonl`（828行，`extra.agent_iterations`={1:620,2:195}，`query_rewrites`非空0条）
- `C:\Users\Administrator\Desktop\project\evidence\reports\platform_reconciliation_20260602.md`:54/63（已有诚实caveat，须保留）
- `C:\Users\Administrator\Desktop\project\deliverables\competition_kit\video_subtitles_5min_final.srt`:35（"三连跑"待改六轮）
- `C:\Users\Administrator\Desktop\project\deliverables\competition_kit\deck_3page_final.html`:224/240/241（默认模型正确、六轮口径、agentic待补）
- `C:\Users\Administrator\Desktop\project\deliverables\competition_kit\poster.html`（token压缩+agentic+商业化均0，待补）
- `C:\Users\Administrator\Desktop\project\evidence\materials\COMPETITION_ASSET_PACK.md`:102/160（自相矛盾，待对齐）
- `C:\Users\Administrator\Desktop\project\evidence\materials\COMMERCIALIZATION_CASE.md`:49-55（缺token→RMB行）
- `C:\Users\Administrator\Desktop\project\scripts\predeploy_sanity.py`（0覆盖端侧路径，确认必要不充分）
- `C:\Users\Administrator\Desktop\project\evidence\screenshots\`（无20260602控制台图）；`evidence\exports\` latest=20260427（stale）
- 缺失报告（待新建）：`evidence\reports\bbox_grounding_eval.md`、`evidence\reports\edge_latency_<date>.md`

---

## 附：全部已核验优化点（按维度）

### 平台使用与对账

| 优先级 | 优化点 | 评分项 | 工作量/风险/分值影响 |
|---|---|---|---|
| P1 | H3 控制台截图仓库里一张都没有——'已对账'只活在转述的 markdown 数字里，决赛权威载体缺失 | 平台使用(20) + 决赛'MaaS API 调用记录等证明材料'硬约束 + 加分①平台利用率(5) | 低/低/高 |
| P2 | predeploy_sanity 默认热缓存 → 现场重跑的金标3问会悄悄丢平台 request_id，H4'predeploy 兼作决赛调用记录'按默认跑法不成立 | 平台使用(20) 决赛对账闭环 + 现场稳定性背书 | 低/低/中 |
| P1 | 材料反复声称的'多任务多模型路由(QA flash / summary·outline qwen3-235b)'作平台利用率证据，但整个 live 日志 0 笔 summary/outline 真实调用——深度 claim 无 request_id 兑现 | 加分①平台利用率(5) | 低/低/中 |
| P1 | 决赛'调用记录'载体没写进 FINAL_SUBMISSION_CHECKLIST 的打包清单——描述在 A 文件、打包在 B 文件，存在漏打包风险 | 决赛提交物完整性 + 口径一致(乘数项) | 低/低/中 |

### 产品能力(40分)

| 优先级 | 优化点 | 评分项 | 工作量/风险/分值影响 |
|---|---|---|---|
| P1 | 首屏 eyebrow 写的是"智能办公的文档工作台"，与产品canonical定位(论文/答辩·端云协同·引用可核验)冲突，是评委读到的第一行字 | 产品能力(40)—场景是否清晰、定位是否一致 | 低/低/中 |
| P1 | 端云协同的量化账本(Token压缩%/平台request_id/命中片段)做好了，却藏在 ?ledger=1 隐藏入口，正常评委演示根本看不到 | 产品能力(40)+对应赛题一协同命题与Token压缩加分项的可见性 | 低/低/中 |
| P2 | 冷启动评委面对空状态无从下手："示例问答"入口已移除(对真实用户是对的)，但现场缺一个一键载入锁定样例的隐藏抓手 | 产品能力(40)—产品完整度 / 现场可演示性 | 中/中/低 |
| P3 | 三种任务(问答/摘要/提纲)的切换被收进"处理设置"折叠面板，首屏看起来像只会ask，弱化产品完整度观感 | 产品能力(40)—产品完整度的呈现 | 低/低/低 |

### 技术能力(40分)

| 优先级 | 优化点 | 评分项 | 工作量/风险/分值影响 |
|---|---|---|---|
| P1 | 加分项#3「agentic 检索循环」的差异化分支在 828 条真实日志中从未触发，只有单测撑着 | 加分项 #3 大模型与智能体能力（5 分）/ 技术亮点可复现 | 低/低/高 |
| P1 | 产品立身点 bbox 证据回链：有单测+丰富定性，但零端到端量化命中率 | 技术能力—bbox 回链可量化 / 技术亮点可复现 | 中/低/中 |
| P1 | 端侧 ML 算力实体缺一个 CPU 推理延迟数字——回应『端侧/云端协同』主题的最后一块拼图 | 赛题主题端侧协同 / 技术亮点可量化 | 低/低/中 |
| P1 | 默认模型 deepseek-v4-flash 的泛化弱点（英文/多语公式表格过度拒答）已诊断但现场默认未开缓解 | 技术能力—评测严谨性闭环 / 现场鲁棒性 | 低/低/中 |

### 端侧/云端协同(赛题核心主题)

| 优先级 | 优化点 | 评分项 | 工作量/风险/分值影响 |
|---|---|---|---|
| P1 | 端侧实体在现场零可见：唯一的端云账本只讲压缩(支柱二)，不讲本地BGE模型(支柱一) | 赛题主题·端侧/云端协同（也关联技术能力40） | 中/低/高 |
| P1 | ‘真·可下沉到边缘节点’只有准确率A/B，没有一个端侧延迟/内存/体积数字——可信闭环缺口已被自己点名 | 赛题主题·端侧/云端协同 + 技术能力40 | 低/低/高 |
| P1 | 最强‘端侧活体证明’edge_live_smoke.py 与 EDGE_EMBEDDING_ENABLED=true 没进任何彩排/预检清单，现场开端侧的计划只活在报告散文里 | 现场演示/答辩 + 赛题主题·端侧/云端协同 | 低/低/中 |

### 现场演示与答辩就绪

| 优先级 | 优化点 | 评分项 | 工作量/风险/分值影响 |
|---|---|---|---|
| P1 | 演示要现场开端侧开关，但 predeploy 闸门根本不走端侧路径——'READY'是必要不充分 | 端云协同应用（端侧实体）+ 现场演示稳定性 | 低/低/高 |
| P1 | 四张 fallback 截图是 20260529 旧 UI，缺端侧态与 ?ledger=1 账本面板——失手时无法兜住新卖点 | 现场演示失手兜底 / 端云协同可视化 | 低/低/中 |
| P2 | 端侧/账本两个新增 live 表面没进入 predeploy 的 warmup，首次点开有冷启动风险 | 现场演示稳定性（冷启动/延迟） | 低/低/中 |
| P1 | 口径卡'上场前30秒'清单仍把'predeploy exit 0'当唯一就绪证明，未随端侧/Flash 现状更新 | 答辩口径一致性 / 演示就绪自检 | 低/低/中 |

### 加分项·智能体(5分)

| 优先级 | 优化点 | 评分项 | 工作量/风险/分值影响 |
|---|---|---|---|
| P1 | 全仓真实日志 query_rewrites 永远为空——self-RAG 的差异化路径（再检索拿到新片段）从未真实触发，只活在 mock 单测里 | 加分项③ 大模型与智能体能力（5分） | 中/低/高 |
| P1 | 最强的真实 agentic 遥测（26 笔二轮@132题）还没被接进 SCORING_MATRIX / deck——证据已升级，叙事还停在旧口径 | 加分项③ 大模型与智能体能力（5分） | 低/低/中 |
| P1 | agentic 循环在现场 UI 完全不可见——后端返回了 agent_iterations/query_rewrites，前端一处不渲染，judge 看不到「它在多轮」 | 加分项③ 大模型与智能体能力（5分） | 中/低/中 |
| P1 | 3 页 deck 与海报对 agentic 零提及——5 分加分项在评委主看物里完全缺位 | 加分项③ 大模型与智能体能力（5分） | 低/低/中 |

### 加分项·商业化潜力(5分)

| 优先级 | 优化点 | 评分项 | 工作量/风险/分值影响 |
|---|---|---|---|
| P1 | 单位经济缺最后一行人民币换算——'算得过账'是断言不是算出来的 | 加分项·商业化潜力（5分） | 低/低/中 |
| P2 | CAC/LTV 只有定性形容词，缺一个哪怕粗略的留存或LTV锚点 | 加分项·商业化潜力（5分） | 低/低/低 |
| P2 | 竞品对比列对 ChatPDF/Readpaper/知网的判断无标注来源，存被追问风险 | 加分项·商业化潜力（5分） | 低/低/低 |

### 加分项·Token压缩(5分)

| 优先级 | 优化点 | 评分项 | 工作量/风险/分值影响 |
|---|---|---|---|
| P2 | handoff 文档残留旧数 89.1%，与全部 judge-facing 材料已更新的 86.6% 冲突（口径漂移） | 加分项 #4 Token 压缩（5分）/ 跨材料口径一致性 | 低/低/中 |
| P2 | Poster 完全没有 Token 压缩内容，5 分加分项在海报维度缺位 | 加分项 #4 Token 压缩（5分）/ 答辩呈现覆盖 | 低/低/中 |
| P2 | 最被反复引用的 86.6% 是 tiktoken 估算口径，更可信的'真实平台计数'压缩比未被提成同等显眼的头条 | 加分项 #4 Token 压缩（5分）/ 证据可信度排序 | 低/低/中 |
| P1 | baseline_compare 的 4.37× 把中/英文混在一起，未给出中文实测的单独压缩比（评委可能专问中文场景） | 加分项 #4 Token 压缩（5分）/ 中文实测口径 | 低/低/中 |

### 交付物完整度与提交就绪

| 优先级 | 优化点 | 评分项 | 工作量/风险/分值影响 |
|---|---|---|---|
| P0 | 两件官方硬性交付物(原生3页PPT文件 + 5分钟录制视频成片)仍不存在为文件,且无被追踪的负责人/截止日 | 初赛提交规格——'3页内PPT'+'5分钟内方案介绍及演示视频'(官方 SUBMISSION_SPEC_CROSSWALK 列为主提交物 1、2) | 低/低/高 |
| P1 | 同一 competition_kit 文件夹内 strict G3 轮次自相矛盾:deck 写'六轮 6/6'、视频字幕仍写'三连跑/三轮' | 提交物一致性/答辩可信度(Asset Mismatch,DEFENSE_DEMO_RISK_CHECKLIST §2 明确列为'judges read this as not actually frozen') | 低/低/中 |
| P2 | '最新导出包/复审包'已过期:latest 是 20260427,早于 06-01/06-02 的 4.37×、端侧叙事、20260529 截图、deepseek 默认口径 | 提交包组装与可交付性(SUBMISSION_PREP_GUIDE 一键导出 / HANDOFF_PACKAGE_BOUNDARY 三层包边界) | 低/低/中 |
| P2 | 封板控制文档自身 stale:FINAL_SUBMISSION_CHECKLIST/快照仍停在 2026-04-20,未反映 06 月已完成项 | 提交就绪自检/封板纪律(FINAL_SUBMISSION_CHECKLIST + SUBMISSION_SPEC_CROSSWALK 是封板前最后一关) | 低/低/低 |

### 诚实口径一致性(横切，防一问就塌)

| 优先级 | 优化点 | 评分项 | 工作量/风险/分值影响 |
|---|---|---|---|
| P1 | 正式 5 分钟视频字幕把 G3 写成『三连跑/三轮全部通过』，与全仓库 6 轮主口径冲突，且自我矮化最强证据 | 现场演示/答辩 + 技术能力 40（可复现性证据） | 低/低/中 |
| P2 | 归档版 deck.html（6 页）仍标旧默认模型 qwen3-235b/qwen3-32b 并引用已被取代的 20260419 截图 | 平台使用 20 / 现场演示（材料口径一致） | 低/低/中 |
| P1 | 被指定为『统一口径单一来源』的 COMPETITION_ASSET_PACK 自身打架：同文件一处说默认 Flash、另一处说『235b 仍是主选择』 | 现场演示/答辩（追问2：材料口径一致性） | 低/低/中 |
| P3 | 归档 VIDEO_SHOTLIST_2MIN.md + 仍随包发布的 video_subtitles.srt 残留旧默认 QA『qwen3-235b』 | 平台使用 20 / 材料口径一致 | 低/低/低 |
| P2 | 拒答路径标签轻微漂移：同一道锁定『木星』拒答，HARD_EVIDENCE_SUMMARY 在 G3 第5-6轮记为 llm_refused，而 demo 材料/代码/金标报告均为 retrieval_no_match | 技术能力 40（拒答闸门可核验性） | 低/低/低 |
