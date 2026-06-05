const fs = require("fs");
const {
  Document, Packer, Paragraph, TextRun, Table, TableRow, TableCell,
  Header, Footer, AlignmentType, LevelFormat, TableOfContents, HeadingLevel,
  BorderStyle, WidthType, ShadingType, VerticalAlign, PageNumber, PageBreak
} = require("docx");

// ---- brand / style constants ----
const FONT = "宋体";
const HFONT = "黑体";
const ACCENT = "C0392B";   // warm brand red
const ACCENT2 = "B9772E";  // warm amber
const DARK = "222222";
const GRAY = "666666";
const CW = 9026;           // A4 content width (1" margins)

// ---- helpers ----
const run = (text, o = {}) => new TextRun({ text, ...o });
const b = (text) => run(text, { bold: true });
const ba = (text) => run(text, { bold: true, color: ACCENT });
function P(children, o = {}) {
  if (typeof children === "string") children = [run(children)];
  return new Paragraph({ children, spacing: { after: 120, line: 312 }, ...o });
}
function CENTER(children, o = {}) {
  if (typeof children === "string") children = [run(children)];
  return new Paragraph({ children, alignment: AlignmentType.CENTER, spacing: { after: 120, line: 312 }, ...o });
}
const H1 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_1, children: [run(text)], spacing: { before: 260, after: 140 } });
const H2 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_2, children: [run(text)], spacing: { before: 180, after: 90 } });
const H3 = (text) => new Paragraph({ heading: HeadingLevel.HEADING_3, children: [run(text)], spacing: { before: 130, after: 70 } });
function BUL(children) {
  if (typeof children === "string") children = [run(children)];
  return new Paragraph({ numbering: { reference: "bul", level: 0 }, children, spacing: { after: 60, line: 300 } });
}
function NUM(children, ref) {
  if (typeof children === "string") children = [run(children)];
  return new Paragraph({ numbering: { reference: ref, level: 0 }, children, spacing: { after: 60, line: 300 } });
}
function NOTE(children) {
  if (typeof children === "string") children = [run(children)];
  return new Paragraph({
    children,
    spacing: { before: 80, after: 120, line: 300 },
    indent: { left: 360 },
    border: { left: { style: BorderStyle.SINGLE, size: 18, color: ACCENT2, space: 12 } },
  });
}

// ---- table helpers ----
const cb = { style: BorderStyle.SINGLE, size: 1, color: "BBBBBB" };
const cbs = { top: cb, bottom: cb, left: cb, right: cb };
function cell(content, w, opts = {}) {
  const arr = Array.isArray(content) ? content : [content];
  const kids = arr.map((c) =>
    typeof c === "string"
      ? new Paragraph({ children: [run(c, { size: 19 })], spacing: { after: 0, line: 252 } })
      : c
  );
  return new TableCell({
    borders: cbs,
    width: { size: w, type: WidthType.DXA },
    margins: { top: 60, bottom: 60, left: 110, right: 110 },
    shading: opts.fill ? { fill: opts.fill, type: ShadingType.CLEAR } : undefined,
    verticalAlign: VerticalAlign.CENTER,
    children: kids,
  });
}
function hcell(text, w) {
  return new TableCell({
    borders: cbs,
    width: { size: w, type: WidthType.DXA },
    margins: { top: 60, bottom: 60, left: 110, right: 110 },
    shading: { fill: ACCENT, type: ShadingType.CLEAR },
    verticalAlign: VerticalAlign.CENTER,
    children: [new Paragraph({ children: [run(text, { size: 19, bold: true, color: "FFFFFF" })], spacing: { after: 0, line: 252 } })],
  });
}
function row(cells) { return new TableRow({ children: cells }); }
function table(colWidths, rows) {
  return new Table({ width: { size: colWidths.reduce((a, c) => a + c, 0), type: WidthType.DXA }, columnWidths: colWidths, rows });
}

// =========================================================================
// CONTENT
// =========================================================================
const body = [];

// ---------- Cover ----------
for (let i = 0; i < 5; i++) body.push(new Paragraph({ children: [run("")], spacing: { after: 0 } }));
body.push(CENTER([run("研答通", { bold: true, size: 72, color: ACCENT, font: HFONT })], { spacing: { after: 80 } }));
body.push(CENTER([run("产品及技术文档", { bold: true, size: 40, color: DARK, font: HFONT })], { spacing: { after: 200 } }));
body.push(CENTER([run("带证据回链的文档问答助手", { size: 26, color: GRAY })], { spacing: { after: 600 } }));
body.push(CENTER([run("无问芯穹 · 赛题一：端侧 / 云端协同应用", { size: 26, bold: true, color: DARK })], { spacing: { after: 100 } }));
body.push(CENTER([run("upload → ask → citation → PDF → refusal", { size: 22, color: ACCENT2 })], { spacing: { after: 500 } }));
body.push(CENTER([run("版本日期：2026-06-05", { size: 22, color: GRAY })], { spacing: { after: 40 } }));
body.push(CENTER([run("作者：研答通项目组", { size: 22, color: GRAY })]));
body.push(new Paragraph({ children: [new PageBreak()] }));

// ---------- TOC ----------
body.push(new Paragraph({ children: [run("目录", { bold: true, size: 30, font: HFONT, color: DARK })], spacing: { after: 160 } }));
body.push(new TableOfContents("Table of Contents", { hyperlink: true, headingStyleRange: "1-3" }));
body.push(new Paragraph({ children: [new PageBreak()] }));

// ---------- 1. 作品概述 ----------
body.push(H1("1. 作品概述"));
body.push(P([
  run("研答通是一个面向"), b("论文阅读、报告复核、答辩准备"),
  run("的文档助手。它的核心能力不是泛化聊天，而是"),
  ba("带证据回链的 PDF 文档问答"),
  run("——产品的立身点只有一句话："), b("答案必须能回到原文证据。"),
]));
body.push(P("围绕这条立身点，研答通把一次问答拆成可核验的四步主链路："));
body.push(table([1700, 7326], [
  row([hcell("环节", 1700), hcell("做了什么", 7326)]),
  row([cell("upload", 1700), cell("上传 PDF / TXT / Markdown，近端解析并保留页级结构（block / line / bbox）", 7326)]),
  row([cell("ask", 1700), cell("近端先检索相关片段、组织上下文，再调用无问芯穹云端大模型作答", 7326)]),
  row([cell("citation", 1700), cell("回答附带 used_chunk_ids 与逐字 evidence_quotes，后端对每条引用做原文子串校验", 7326)]),
  row([cell("PDF", 1700), cell("点击 citation 跳回 PDF 原页，bbox 高亮定位证据所在位置", 7326)]),
  row([cell("refusal", 1700), cell("检索未命中 / 无真实依据时显式拒答，不做开放域硬答、不编造", 7326)]),
]));
body.push(P([
  run("一句话定位："),
  ba("让每一个回答都能落回 PDF 原文的、可核验的文档问答助手"),
  run("——面向学术与答辩场景"), b("「说得出处」"), run("的刚需。"),
]));

// ---------- 2. 产品能力 ----------
body.push(H1("2. 产品能力"));
body.push(H2("2.1 解决的真实问题"));
body.push(P("论文与长报告的阅读复核，痛点不在「能不能给个答案」，而在「这个答案凭什么、出处在哪」。普通聊天工具会流畅作答，却说不出依据，也无法被核验——这在学术阅读、报告审核、答辩准备里恰恰是致命的。研答通正面解决这个问题：答得出，更要指得到原文。"));

body.push(H2("2.2 为什么这不是「聊天壳」"));
body.push(P("研答通与套壳聊天工具的本质差异，是一条贯穿全链路的四层约束："));
body.push(NUM([b("解析层："), run("保留 PDF 页级结构与文本块，证据有坐标可定位")], "num1"));
body.push(NUM([b("检索层："), run("先选相关片段、再组织上下文，离题内容在生成前就被拦下")], "num1"));
body.push(NUM([b("生成层："), run("ask 路径要求模型返回结构化 evidence 依据，引用须逐字可校验")], "num1"));
body.push(NUM([b("呈现层："), run("citation 回到 PDF 页面并高亮证据位置，用户可一眼复核")], "num1"));
body.push(P([run("只要检索未命中，系统"), b("直接拒答"), run("，而不是开放域硬答——这是产品可信度的底线。")]));

body.push(H2("2.3 核心用户价值"));
body.push(BUL("长文阅读时，快速定位核心信息，省去逐页翻找"));
body.push(BUL("问答时，答案能回到 PDF 原文证据，可核验、可追溯"));
body.push(BUL("离题或无依据问题，系统显式拒答，避免「一本正经地编造」"));
body.push(BUL("对答辩准备场景，citation → PDF 回链的价值高于泛化生成"));

body.push(H2("2.4 目标场景"));
body.push(P([
  run("主路径为"), b("B 端高校实验室 / 课题组席位订阅"),
  run("，辅以"), b("C 端答辩季入口"),
  run("。差异化不是「答得流畅」，而是「答得可验证」——契合学术场景对「说得出处」的刚需（详见第 8 节商业化）。"),
]));

// ---------- 3. 系统架构 ----------
body.push(H1("3. 系统架构：端云分层协同"));
body.push(P([
  run("研答通是"), ba("端云分层协同"),
  run("架构，正面回应赛题一「端侧 / 云端协同应用」命题：解析、切块、"),
  b("本地语义编码"), run("、混合检索、上下文压缩、证据定位等「重而可本地化」的计算放在端侧 / 近端完成；只把命中任务意图的"),
  b("必要片段"), run("上云，交由无问芯穹 MaaS 大模型"), b("生成"),
  run("；回答再回到端侧做 PDF 内证据回链。核心范式是"),
  ba("小模型在端理解、大模型在云生成。"),
]));

body.push(H2("3.1 三层职责划分"));
body.push(table([1500, 2400, 5126], [
  row([hcell("层", 1500), hcell("位置", 2400), hcell("职责", 5126)]),
  row([
    cell("端侧", 1500),
    cell("浏览器 / 客户端", 2400),
    cell("文件上传与任务输入、结果展示、PDF 证据 bbox 高亮叠加与坐标映射、手动标注与标注页导出、缩放翻页、本地会话态（HttpOnly cookie）", 5126),
  ]),
  row([
    cell("近端服务", 1500),
    cell("应用后端（部署节点本地，纯 CPU、零云依赖）", 2400),
    cell("PDF 解析（PyMuPDF 保留页级 block/line/bbox）、结构化切块、本地句向量编码（BGE-small-zh-v1.5 ONNX）、词法 + 语义混合检索、上下文规划与 Token 压缩、bbox 子串定位与逐字证据校验、JSONL 调用日志", 5126),
  ]),
  row([
    cell("云端", 1500),
    cell("无问芯穹 MaaS", 2400),
    cell("ask / summary / outline 大模型生成；端侧 / 近端只上送必要片段", 5126),
  ]),
]));

body.push(H2("3.2 真实的端侧 ML 算力实体"));
body.push(P([
  run("近端跑一个"), ba("本地句向量模型（BGE-small-zh-v1.5 ONNX）"),
  run("做语义编码与混合检索，这是真实在本机 CPU 上运行的 ML 前向推理，"),
  b("零云依赖、物理上可下沉到端侧 / 边缘节点"),
  run("。本机实测："), b("权重 90.4 MB、每查询编码约 9 ms、纯 CPU"),
  run("（建索引为一次性 / 文档级成本，走 warmup 预建）。模型缺失或失败时"),
  b("自动回退纯词法"), run("，现场绝不因端侧组件崩盘。"),
]));

body.push(H2("3.3 诚实标注（口径自律）"));
body.push(NOTE([
  b("标注一："), run("PDF 页面图像由近端用 PyMuPDF 栅格化后下发，端侧负责坐标映射与高亮 / 标注交互——端侧做的是「证据呈现 + 交互计算」，不夸大为「端侧大模型推理」。"),
]));
body.push(NOTE([
  b("标注二："), run("本地语义检索与我们高度调优的词法检索在固定基准上"),
  b("持平、零回归"), run("；其价值在于①真实的端侧 ML 算力实体；②对未知 / 改写措辞、词法弱区（英文公式、多语混排）的语义补召回。我们"),
  b("不"), run("把它包装为「检索显著提升」。"),
]));

// ---------- 4. 核心技术链路 ----------
body.push(H1("4. 核心技术链路"));
body.push(H2("4.1 文档解析"));
body.push(BUL("支持 PDF / TXT / Markdown 三类输入"));
body.push(BUL("PDF 解析保留页级结构（block / line / bbox），供 citation 与 PDF 回链使用"));
body.push(BUL("结构化切块：ChunkService 以 900 字为 target、100 字 overlap"));

body.push(H2("4.2 ask 路径：单层 agentic 检索循环"));
body.push(NUM("用户提问", "num2"));
body.push(NUM("近端检索相关 chunk", "num2"));
body.push(NUM("组织 ask 上下文，调用无问芯穹模型", "num2"));
body.push(NUM([b("模型自评证据是否充分"), run("：不足则给出 need_more=true（并在需要新证据时给 followup_query）")], "num2"));
body.push(NUM([b("有界二次重试（iter ≤ 2）"), run("：用 followup_query 补检索新片段（排除已用 chunk）再问一次；agent_iterations 落日志")], "num2"));
body.push(NUM([run("提取 used_chunk_ids / evidence_quotes，对每条 quote 做"), b("原文子串校验"), run("（校验不过即丢弃）")], "num2"));
body.push(NUM("组装 citation，回到 PDF 页面做 bbox 证据显示", "num2"));
body.push(NOTE([
  b("诚实口径："), run("改写补检索分支已实现且有单测覆盖，但固定 demo 集上模型多为单轮收敛、触发的二轮也多为同上下文复核，故生产日志 query_rewrites 多为空——我们定位为「有界自评重试」，不当作「现场可逐条核验改写」的卖点。"),
]));

body.push(H2("4.3 引用不可伪造"));
body.push(P([
  run("ask 返回的每条 evidence_quote，后端都会回到原文做"), b("逐字子串校验"),
  run("，校验不通过的引用直接丢弃——"), ba("引用无法被模型编造"),
  run("。这是「答案能回到证据」从口号变成工程契约的关键一环。"),
]));

body.push(H2("4.4 refusal：检索 / 模型双层拒答"));
body.push(BUL([b("检索层："), run("无命中 → retrieval_gate 直接拒答，离题问题在生成前被拦截（同时省 token）")]));
body.push(BUL([b("模型层："), run("检索命中但模型判定无依据 → llm_refused 二次拒答；低置信候选交模型复核，未给可验证证据则拒答")]));

body.push(H2("4.5 上下文规划与 Token 压缩"));
body.push(P([
  run("ContextPlannerService 按任务意图选片段（ask 走 retrieval、summary / outline 走 coverage），让"),
  b("只有必要上下文上云"), run("。这既是协同的核心节省环节，也直接对应加分项（详见第 6 节）。"),
]));

// ---------- 5. 平台使用 ----------
body.push(H1("5. 无问芯穹平台使用"));
body.push(P("研答通的主问答链路真实运行在无问芯穹 MaaS 之上，而非把平台「放进环境变量挂个名」。"));
body.push(H2("5.1 接入与模型路由"));
body.push(table([2600, 6426], [
  row([hcell("项", 2600), hcell("取值", 6426)]),
  row([cell("Base URL", 2600), cell("https://cloud.infini-ai.com/maas/v1", 6426)]),
  row([cell("默认 QA 模型", 2600), cell([new Paragraph({ children: [run("deepseek-v4-flash", { size: 19, bold: true }), run("（V6 contract-patch holdout 后从 qwen3-235b 切换）", { size: 19 })], spacing: { after: 0, line: 252 } })], 6426)]),
  row([cell("QA rollback", 2600), cell("qwen3-235b-a22b-instruct-2507（受信任回滚路径，gold-sample 双模型 3/3 即用它跑）", 6426)]),
  row([cell("summary / outline", 2600), cell("qwen3-235b-a22b-instruct-2507", 6426)]),
  row([cell("历史 fallback", 2600), cell("qwen3-32b / qwen3-next-80b-a3b-instruct（保留可用）", 6426)]),
]));

body.push(H2("5.2 真实留痕、可控台对账"));
body.push(P([
  run("每次调用都把 token、latency、本地 request_id 与"),
  ba("无问芯穹平台 request_id"),
  run("落到 JSONL 日志（data/logs/call_logs.jsonl），可在 infini-ai 控制台"),
  b("逐条对账"), run("——「用了平台」因此能讲成「用了平台并留下可核验证据」。"),
]));

body.push(H2("5.3 多模型平台广度"));
body.push(P([
  run("同一检索流水线下"), ba("跨 DeepSeek / Qwen / Kimi / GLM 四大家族实测"),
  run("：6 模型 × 10 题 = "), b("60 次真实调用、均带 request_id、全部答对"),
  run("（multi_model_eval.md），证明真实深度使用平台、非单模型挂名。"),
]));

// ---------- 6. 加分项 ----------
body.push(H1("6. 关键技术亮点与加分项"));
body.push(H2("6.1 Token 消耗压缩"));
body.push(P([
  run("近端「解析 → 切块 → 按任务意图选片段」三层预处理，让只有必要上下文上云："),
  ba("长文档 ask 平均节省 86.6% input token、峰值 93.1%"),
  run("（Attention 论文 10,263 → 704 tokens）。"),
]));
body.push(P([
  run("更硬的口径（"), b("真实平台 token，非 tiktoken 估算"),
  run("）：受控对照「直接喂全文」，唯一变量是检索接地 vs 全文——"),
  b("22 题集省 4.37×"), run("（49,273 vs 215,113，准确率 22/22 持平）；扩到 "),
  b("39 题真实论文集省 4.3×"), run("（RAG 38/39，唯一子串漏配已核验非真失败），每条调用带真实 chatcmpl- id 可对账。"),
]));
body.push(NOTE([
  b("诚实标注："), run("口径是「同等准确度下省 4.3–4.4× + 能 scale + 能 bbox 回链」，不是「RAG 更准」；短文档场景如实标注为约 -4%（单 chunk 加页码 / 标题 marker 略增），不假装所有场景都压得动。"),
]));
body.push(H2("6.2 大模型与智能体能力"));
body.push(P("主链路使用无问芯穹大模型 + 单层 agentic 检索循环（检索 → 模型自评证据是否充分 → 有界二次重试 iter ≤ 2，需新证据时改写 followup_query 补检索）+ 检索 / 模型双层拒答；agent_iterations 落日志（真实日志中约 1/4 的 ask 触发了二轮自评）。"));
body.push(H2("6.3 商业化潜力"));
body.push(P([
  run("主打 "), b("B 端高校实验室 / 课题组席位订阅"),
  run(" + C 端答辩季入口。差异化是「答得可验证」（bbox 级回链 + 逐字校验 + 离题拒答）；毛利侧由 token 压缩支撑（每次问答边际推理成本压低近一个数量级）。完整市场量级 / 竞品差异 / 单位经济见 COMMERCIALIZATION_CASE.md。"),
]));

// ---------- 7. 验证与评测体系 ----------
body.push(H1("7. 验证与评测体系"));
body.push(P([
  run("我们把评测当成"), ba("找自己问题的工具，而不是包装分数的工具"),
  run("。验证从锁定小样本一路放大到 3 万级对抗压测，且层层人复核："),
]));
body.push(table([2550, 1500, 4976], [
  row([hcell("层级", 2550), hcell("规模", 1500), hcell("结果与口径", 4976)]),
  row([cell("gold-sample 双模型", 2550), cell("3 题", 1500), cell("235b 3/3、32b 3/3，最强可复现 demo 证据", 4976)]),
  row([cell("strict G3 复现", 2550), cell("6 轮", 1500), cell("6/6 连续 strict fresh-upload，每轮新 file_id，fallback 0/6", 4976)]),
  row([cell("扩展评测", 2550), cell("51 题", 1500), cell([new Paragraph({ children: [run("默认 deepseek-v4-flash 48/51（94.1%）；V6 extreme holdout 71/72、拒答精确率 100%、引用 98.3%；rollback qwen3-235b 51/51", { size: 19 })], spacing: { after: 0, line: 252 } })], 4976)]),
  row([cell("judged 三层交叉 + 人复核", 2550), cell("176 题泛化", 1500), cell("强模型现造全新题判分 88.6%，48 道拒答陷阱 0 编造，主动暴露弱点", 4976)]),
  row([cell("端侧 A/B", 2550), cell("176 题", 1500), cell("端侧语义检索把过度拒答 6→1（0 新增编造），固定集零变化", 4976)]),
  row([cell("大规模压测 + 5 轮优化", 2550), cell("33,838 题", 1500), cell("整体 91.0% 初判通过，16 类文档 14 类 89–99%", 4976)]),
  row([cell("多模型广度", 2550), cell("60 次", 1500), cell("DeepSeek / Qwen / Kimi / GLM 四家族同流水线全过", 4976)]),
]));

body.push(H2("7.1 大规模压测 + 5 轮优化（2026-06-05）"));
body.push(P([
  run("用代金券把「找短板 → 验证 → 优化迭代」跑到底：累计 "),
  b("33,838 道全新对抗题"), run("（真实计费、request_id 可对账），其中 "),
  b("7000+ 道经强模型判分式严格评测"), run("（≈ 1.4 万次真实调用）。方法是：强模型现造题 → 真实生产链路作答 → 强模型带原文页判分 → "),
  b("人逐个复核 FAIL"), run("。"),
]));
body.push(P([run("针对发现的「过度拒答」短板，做了 "), b("5 轮提召回实验"), run("（端侧 bge-small / 云端 bge-m3 / 调救援阈值 / 短文档全文兜底），结论跨方案一致：")]));
body.push(NOTE([
  run("任何「检索空时给模型更多上下文」的方案，都会让模型在对抗性无依据题上过度推断 → "),
  b("幻觉上升"), run("。所以"), ba("「检索空就拒答」是精度 / 召回权衡的安全侧，是本产品「证据可核验、不编造」立身点的正确选择"),
  run("，验证为对、保持默认不动。这不是没优化成，是有意不塞伤害产品的改动。"),
]));

body.push(H2("7.2 评测诚实优先"));
body.push(P([
  run("过程本身暴露了一个方法论发现："),
  b("强模型裁判在难数值题上自己也会算错"),
  run("（finance 类失败约一半是裁判误判），所以 90% 初判通过率被低估、真实系统质量更高。结论："),
  ba("judged-eval 必须人复核，不能直接拿 pass-rate 当系统准确率。"),
]));

// ---------- 8. 已知边界 ----------
body.push(H1("8. 已知边界与诚实说明"));
body.push(P("我们不说「没有短板」，而是主动找到、量化短板，并证明当前设计是正确取舍。两个真短板在 3 万题尺度上稳定复现，且都不在锁定 demo 主链路（中文论文问答）上。"));
body.push(H2("8.1 短板一：多语言内容 → 过度拒答"));
body.push(BUL([b("现象："), run("词法检索对非中英文召回弱 → 检索空 → 拒答（multilingual 类约 80%、254 道过度拒答）")]));
body.push(BUL([b("取舍："), run("已用 5 轮实验证明全局提召回会增幻觉，故保持安全默认")]));
body.push(BUL([b("可选修复："), run("在确为弱词法 / 多语言场景，端侧语义检索能干净补召回（专项 A/B 9→0、零新幻觉）——这是端云协同的真实价值，作选项不作默认")]));
body.push(H2("8.2 短板二：多步表格数值推理"));
body.push(BUL([b("现象："), run("finance 类多行 / 多条件表格算术会误读单元格 / 漏行（约 59%）")]));
body.push(BUL([b("定性："), run("属大模型自身能力边界——连我们的强裁判 qwen3-235b 在同类题上也算错，非检索 / 配置可修")]));
body.push(BUL([b("后续路线："), run("结构化表格解析 + 受约束计算器 + 单元格级溯源（让模型调工具算，而非脑算）。这是加功能、不是赛前 prompt 热补，列为 roadmap")]));

// ---------- 9. 结语 ----------
body.push(H1("9. 结语与后续工作"));
body.push(P([
  run("研答通用一条"), b("可核验的主链路"),
  run("（upload → ask → citation → PDF → refusal）+ 一个"),
  b("真实的端侧 ML 实体"),
  run("，把「端云协同」从叙事做成了可演示、可复现、可追溯的工程事实。后续不再以扩功能为主，而以把现有能力升级为证据链为主："),
]));
body.push(NUM("3 页 PPT 与 5 分钟视频正式成片", "num3"));
body.push(NUM("如最终演示环境变化，刷新四张核心截图", "num3"));
body.push(NUM("多语言召回：端侧语义检索可选开关（已验证干净），默认关以保安全", "num3"));
body.push(NUM("表格数值：后续接结构化表格解析 + 计算器工具链", "num3"));
body.push(NUM("保持各材料与 strict G3 / 默认模型口径一致", "num3"));
body.push(new Paragraph({ children: [run("")], spacing: { before: 200 } }));
body.push(CENTER([run("evidence-backed QA · 可演示 · 可复现 · 可追溯", { size: 22, color: ACCENT, bold: true })]));

// =========================================================================
// DOCUMENT
// =========================================================================
const doc = new Document({
  creator: "研答通项目组",
  title: "研答通产品及技术文档",
  description: "无问芯穹赛题一 端侧/云端协同应用",
  styles: {
    default: { document: { run: { font: FONT, size: 22, color: DARK } } },
    paragraphStyles: [
      { id: "Heading1", name: "Heading 1", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 32, bold: true, font: HFONT, color: ACCENT },
        paragraph: { spacing: { before: 260, after: 140 }, outlineLevel: 0,
          border: { bottom: { style: BorderStyle.SINGLE, size: 8, color: ACCENT, space: 6 } } } },
      { id: "Heading2", name: "Heading 2", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 26, bold: true, font: HFONT, color: DARK },
        paragraph: { spacing: { before: 180, after: 90 }, outlineLevel: 1 } },
      { id: "Heading3", name: "Heading 3", basedOn: "Normal", next: "Normal", quickFormat: true,
        run: { size: 23, bold: true, font: HFONT, color: "444444" },
        paragraph: { spacing: { before: 130, after: 70 }, outlineLevel: 2 } },
    ],
  },
  numbering: {
    config: [
      { reference: "bul", levels: [{ level: 0, format: LevelFormat.BULLET, text: "•", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 600, hanging: 300 } } } }] },
      { reference: "num1", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 600, hanging: 300 } } } }] },
      { reference: "num2", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 600, hanging: 300 } } } }] },
      { reference: "num3", levels: [{ level: 0, format: LevelFormat.DECIMAL, text: "%1.", alignment: AlignmentType.LEFT, style: { paragraph: { indent: { left: 600, hanging: 300 } } } }] },
    ],
  },
  sections: [{
    properties: {
      titlePage: true,
      page: { size: { width: 11906, height: 16838 }, margin: { top: 1440, right: 1440, bottom: 1440, left: 1440 } },
    },
    headers: {
      first: new Header({ children: [new Paragraph({ children: [run("")] })] }),
      default: new Header({ children: [new Paragraph({ alignment: AlignmentType.RIGHT, children: [run("研答通 · 产品及技术文档", { size: 16, color: GRAY })], border: { bottom: { style: BorderStyle.SINGLE, size: 4, color: "DDDDDD", space: 4 } } })] }),
    },
    footers: {
      first: new Footer({ children: [new Paragraph({ children: [run("")] })] }),
      default: new Footer({ children: [new Paragraph({ alignment: AlignmentType.CENTER, children: [run("— ", { size: 16, color: GRAY }), new TextRun({ children: [PageNumber.CURRENT], size: 16, color: GRAY }), run(" —", { size: 16, color: GRAY })] })] }),
    },
    children: body,
  }],
});

Packer.toBuffer(doc).then((buf) => {
  fs.writeFileSync("研答通产品及技术文档.docx", buf);
  console.log("WROTE 研答通产品及技术文档.docx", buf.length, "bytes");
});
