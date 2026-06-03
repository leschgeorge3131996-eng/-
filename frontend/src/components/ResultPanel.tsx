import { AnimatePresence, motion } from "motion/react";
import { useEffect, useState } from "react";
import type { Citation, EvidenceMode, ResponseDetailLevel, TaskResult, TaskType } from "../types";
import MarkdownResult from "./MarkdownResult";

const MOTION_EASE: [number, number, number, number] = [0.22, 1, 0.36, 1];

const TASK_LABELS: Record<TaskType, string> = {
  summary: "摘要",
  ask: "问答",
  outline: "提纲生成"
};

const RESPONSE_DETAIL_LABELS: Record<ResponseDetailLevel, string> = {
  concise: "简洁",
  balanced: "适中",
  detailed: "详细"
};

const EVIDENCE_MODE_LABELS: Record<EvidenceMode, string> = {
  declared: "模型声明证据",
  candidate: "检索上下文",
  none: "未返回可验证证据"
};

function revealMotion(delay = 0) {
  return {
    initial: { opacity: 0, y: 14 },
    animate: { opacity: 1, y: 0 },
    transition: { duration: 0.28, delay, ease: MOTION_EASE }
  };
}

async function copyText(text: string): Promise<void> {
  if (navigator.clipboard?.writeText) {
    await navigator.clipboard.writeText(text);
    return;
  }

  const textarea = document.createElement("textarea");
  textarea.value = text;
  textarea.setAttribute("readonly", "true");
  textarea.style.position = "absolute";
  textarea.style.left = "-9999px";
  document.body.appendChild(textarea);
  textarea.select();
  document.execCommand("copy");
  document.body.removeChild(textarea);
}

function downloadText(filename: string, content: string): void {
  const blob = new Blob([content], { type: "text/plain;charset=utf-8" });
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
}

function getEvidenceMode(result: TaskResult): EvidenceMode {
  return result.task_type === "ask" ? result.evidence_mode ?? "none" : "declared";
}

function getEvidenceItems(result: TaskResult, evidenceMode: EvidenceMode): Citation[] {
  if (result.task_type === "ask") {
    if (evidenceMode === "declared") {
      return result.citations ?? [];
    }
    if (evidenceMode === "candidate") {
      return result.candidate_chunks ?? [];
    }
    return [];
  }
  return result.source_chunks ?? [];
}

function getEvidenceSummary(result: TaskResult, evidenceMode: EvidenceMode): {
  tone: EvidenceMode;
  title: string;
  description: string;
} {
  if (result.task_type !== "ask") {
    return {
      tone: "candidate",
      title: "来源片段",
      description: "以下片段用于说明 summary / outline 的上下文来源，不等同于模型逐条声明使用的证据。"
    };
  }

  if (evidenceMode === "declared") {
    return {
      tone: "declared",
      title: "模型声明证据",
      description: "以下片段来自模型声明实际使用的证据块，可用于回看依据。"
    };
  }

  if (evidenceMode === "candidate") {
    return {
      tone: "candidate",
      title: "检索上下文",
      description: "以下片段仅代表本轮检索命中的候选上下文，模型未完成证据声明。"
    };
  }

  return {
    tone: "none",
    title: "未返回可验证证据",
    description: "本次回答未返回可验证的证据块，请谨慎使用结论。"
  };
}

function getEvidenceSectionTitle(result: TaskResult, evidenceMode: EvidenceMode): string {
  if (result.task_type !== "ask") {
    return "来源片段";
  }
  if (evidenceMode === "declared") {
    return "引用依据";
  }
  if (evidenceMode === "candidate") {
    return "检索上下文（未完成证据声明）";
  }
  return "证据状态";
}

function getConfidenceBar(result: TaskResult, evidenceMode: EvidenceMode): {
  level: "high" | "partial" | "none";
  label: string;
  detail: string;
} | null {
  if (result.task_type !== "ask") return null;
  if (result.outcome === "refused") return null;

  const citationCount = (result.citations ?? []).length;
  const quoteCount = (result.evidence_quotes ?? []).length;

  if (evidenceMode === "declared" && citationCount > 0) {
    return {
      level: "high",
      label: "原文证据支撑",
      detail: `基于 ${citationCount} 条原文引用${quoteCount > 0 ? `，含 ${quoteCount} 段逐字摘录` : ""}`
    };
  }
  if (evidenceMode === "candidate") {
    return {
      level: "partial",
      label: "检索上下文参考",
      detail: "模型未完成证据声明，答案基于检索候选片段"
    };
  }
  return {
    level: "none",
    label: "无可验证证据",
    detail: "本次回答缺乏原文依据，请谨慎使用"
  };
}

function isRetrievalGateResult(result: TaskResult): boolean {
  return result.route_reason === "retrieval_no_match" || result.model_name === "retrieval_gate";
}

function buildExportLines(
  result: TaskResult,
  evidenceMode: EvidenceMode,
  evidenceItems: Citation[]
): string[] {
  const retrievedPages = result.retrieved_pages ?? [];
  const isRetrievalGate = isRetrievalGateResult(result);
  const modelExportLine = isRetrievalGate
    ? "- 执行路径：retrieval_gate（未调用模型）"
    : `- 模型：${result.model_name}`;
  const lines: string[] = [
    `# ${TASK_LABELS[result.task_type]}结果`,
    "",
    `- 文档：${result.document_name}`,
    ...(isRetrievalGate ? [] : [`- 请求 ID：${result.request_id}`]),
    modelExportLine,
    `- 路由：${result.route_tier ?? "default"}`,
    result.route_reason ? `- 路由原因：${result.route_reason}` : null,
    result.response_detail_level
      ? `- 粒度：${RESPONSE_DETAIL_LABELS[result.response_detail_level] ?? result.response_detail_level}`
      : null,
    result.task_type === "ask"
      ? `- 证据模式：${EVIDENCE_MODE_LABELS[evidenceMode]}`
      : "- 证据说明：来源片段（provenance hint）",
    `- 检索状态：${result.retrieval_status}`,
    `- 检索页码：${retrievedPages.length > 0 ? retrievedPages.join(", ") : "无"}`,
    result.token_usage?.total_tokens !== null && result.token_usage?.total_tokens !== undefined
      ? `- Token：输入 ${result.token_usage.prompt_tokens ?? 0} / 输出 ${result.token_usage.completion_tokens ?? 0} / 总计 ${result.token_usage.total_tokens}`
      : null,
    "",
    "## 正文",
    "",
    result.result
  ].filter((item): item is string => Boolean(item));

  if (evidenceItems.length > 0) {
    lines.push("", `## ${getEvidenceSectionTitle(result, evidenceMode)}`, "");
    evidenceItems.forEach((item) => {
      lines.push(`- ${item.chunk_id} | pages: ${item.page_numbers.join(", ")} | ${item.snippet}`);
    });
  }

  if ((result.evidence_quotes ?? []).length > 0) {
    lines.push("", "## 证据摘录", "");
    (result.evidence_quotes ?? []).forEach((quote) => {
      lines.push(`- ${quote.chunk_id} | ${quote.quote}`);
    });
  }

  return lines;
}

function cleanFollowUpQuestion(rawLine: string): string {
  return rawLine
    .replace(/^\s*(?:[-*•]|\d+[.)、]|[（(]?\d+[）)])\s*/, "")
    .replace(/^\s*(?:问题|追问)\s*\d*\s*[:：、.-]?\s*/, "")
    .replace(/\s+$/, "")
    .trim();
}

function extractResearchDigestQuestions(result: TaskResult | null): string[] {
  if (!result || result.task_type !== "summary" || result.outcome === "refused") {
    return [];
  }

  const lines = result.result.split(/\r?\n/);
  const questions: string[] = [];
  let inFollowUpSection = false;

  for (const line of lines) {
    const trimmed = line.trim();
    if (!trimmed) continue;

    const headingText = trimmed.replace(/^#{1,6}\s*/, "");
    if (/建议追问|追问问题|后续问题|可追问/.test(headingText)) {
      inFollowUpSection = true;
      continue;
    }

    if (inFollowUpSection && /^#{1,6}\s+/.test(trimmed)) {
      break;
    }

    const cleaned = cleanFollowUpQuestion(trimmed);
    const looksLikeQuestion = /[？?]$/.test(cleaned) || /^(为什么|如何|是否|哪些|什么|能否|怎样|哪里|哪一|是否可以)/.test(cleaned);
    if (inFollowUpSection && looksLikeQuestion && cleaned.length >= 4) {
      questions.push(cleaned);
    }
  }

  return Array.from(new Set(questions)).slice(0, 5);
}

function isResearchDigestResult(result: TaskResult | null, followUpQuestions: string[]): boolean {
  if (!result || result.task_type !== "summary" || result.outcome === "refused") {
    return false;
  }
  return result.result.includes("论文速读") || followUpQuestions.length > 0;
}

type ResultPanelProps = {
  activeTaskType: TaskType;
  error: string | null;
  loading: boolean;
  loadMessage: string;
  result: TaskResult | null;
  documentTotalChars?: number | null;
  canOpenPdfPreview?: boolean;
  canRetry?: boolean;
  onOpenPdfPage?: (citation: Citation) => void;
  onAskFollowUp?: (question: string) => void;
  onRetry?: () => void;
};

export default function ResultPanel({
  activeTaskType,
  error,
  loading,
  loadMessage,
  result,
  documentTotalChars,
  canOpenPdfPreview = false,
  canRetry = false,
  onOpenPdfPage,
  onAskFollowUp,
  onRetry
}: ResultPanelProps) {
  const [copyState, setCopyState] = useState<"idle" | "done" | "error">("idle");
  const [evidenceCopyState, setEvidenceCopyState] = useState<string | null>(null);
  const [exportState, setExportState] = useState<"idle" | "done" | "error">("idle");
  const stateKey = error ? "error" : loading ? "loading" : result ? result.request_id : "idle";
  const evidenceMode = result ? getEvidenceMode(result) : "none";
  const evidenceItems = result ? getEvidenceItems(result, evidenceMode) : [];
  const evidenceSummary = result ? getEvidenceSummary(result, evidenceMode) : null;
  const confidenceBar = result ? getConfidenceBar(result, evidenceMode) : null;
  const retrievedPages = result?.retrieved_pages ?? [];
  const citationCount = (result?.citations ?? []).length;
  const isRetrievalGate = result ? isRetrievalGateResult(result) : false;
  const modelMetaLabel = isRetrievalGate ? "执行路径" : "模型";
  const modelMetaValue = isRetrievalGate
    ? "retrieval_gate（未调用模型）"
    : (result?.model_name ?? "-");
  const followUpQuestions = extractResearchDigestQuestions(result);
  const showDigestEvidenceCard = isResearchDigestResult(result, followUpQuestions);
  const sourcePageCount = new Set(evidenceItems.flatMap((item) => item.page_numbers)).size;
  const showEvidenceSummary =
    evidenceSummary !== null && (result?.outcome !== "refused" || evidenceItems.length > 0);
  // Demo-only 端云协同 ledger, gated behind a hidden `?ledger=1` entrance so real
  // users never see it. Reads only fields already returned by the backend —
  // zero new computation. (Near-end vs cloud latency split is intentionally
  // omitted: agentic ask makes up to 2 cloud calls and cache hits zero latency,
  // so any subtraction would be misleading.)
  const ledgerEnabled =
    typeof window !== "undefined" &&
    new URLSearchParams(window.location.search).has("ledger");
  // Compression is full-document → context actually sent. For ask, source_document_chars
  // is already the post-retrieval size (== used_document_chars), so the real saving only
  // shows up against the full-document total, which comes from the upload metadata.
  const ledgerSentChars = result?.used_document_chars ?? 0;
  const ledgerFullChars = documentTotalChars ?? 0;
  const ledgerHasCompression =
    ledgerFullChars > 0 && ledgerSentChars > 0 && ledgerSentChars <= ledgerFullChars;
  const ledgerUploadPct = ledgerHasCompression
    ? (ledgerSentChars / ledgerFullChars) * 100
    : null;
  const ledgerPromptTokens = result?.token_usage?.prompt_tokens;
  const ledgerPlatformId = result?.platform_request_id ?? null;

  useEffect(() => {
    setCopyState("idle");
    setExportState("idle");
    setEvidenceCopyState(null);
  }, [result?.request_id]);

  async function handleCopyResult() {
    if (!result?.result) {
      return;
    }

    try {
      await copyText(result.result);
      setCopyState("done");
      window.setTimeout(() => setCopyState("idle"), 1800);
    } catch {
      setCopyState("error");
      window.setTimeout(() => setCopyState("idle"), 2200);
    }
  }

  async function handleCopyEvidence(id: string, text: string) {
    try {
      await copyText(text);
      setEvidenceCopyState(id);
      window.setTimeout(() => setEvidenceCopyState(null), 1800);
    } catch {
      setEvidenceCopyState(`error:${id}`);
      window.setTimeout(() => setEvidenceCopyState(null), 2200);
    }
  }

  function handleExportResult() {
    if (!result?.result) {
      return;
    }

    try {
      const lines = buildExportLines(result, evidenceMode, evidenceItems);
      downloadText(`yandatong-${result.task_type}-${result.request_id}.md`, lines.join("\n"));
      setExportState("done");
      window.setTimeout(() => setExportState("idle"), 1800);
    } catch {
      setExportState("error");
      window.setTimeout(() => setExportState("idle"), 2200);
    }
  }

  function renderEvidenceCard(item: Citation, index: number, baseDelay = 0) {
    const copyId = `${item.chunk_id}-${index}`;
    const copyLabel =
      evidenceCopyState === copyId
        ? "已复制"
        : evidenceCopyState === `error:${copyId}`
          ? "复制失败"
          : "复制";

    const cardContent = (
      <>
        <p className="citation-meta">页码：{item.page_numbers.join(", ")}</p>
        <p>{item.snippet}</p>
      </>
    );

    return (
      <motion.article
        key={`${item.chunk_id}-${index}`}
        className="citation-card"
        {...revealMotion(baseDelay + index * 0.05)}
      >
        {canOpenPdfPreview && onOpenPdfPage ? (
          <button
            data-testid={`open-pdf-${item.chunk_id}-${index}`}
            className="citation-button"
            type="button"
            onClick={() => onOpenPdfPage(item)}
          >
            {cardContent}
          </button>
        ) : (
          cardContent
        )}
        <div className="citation-actions">
          <button
            className="mini-action-button"
            type="button"
            onClick={() => handleCopyEvidence(copyId, item.snippet)}
          >
            {copyLabel}
          </button>
        </div>
      </motion.article>
    );
  }

  function renderEvidenceQuote(
    quote: { chunk_id: string; quote: string },
    index: number,
    requestId: string,
    baseDelay = 0
  ) {
    const copyId = `${quote.chunk_id}-${index}`;
    const copyLabel =
      evidenceCopyState === copyId
        ? "已复制"
        : evidenceCopyState === `error:${copyId}`
          ? "复制失败"
          : "复制";

    return (
      <motion.article
        key={`${requestId}-${quote.chunk_id}-${index}`}
        className="citation-card"
        {...revealMotion(baseDelay + index * 0.05)}
      >
        <p className="citation-meta">证据块：{quote.chunk_id}</p>
        <p>{quote.quote}</p>
        <div className="citation-actions">
          <button
            className="mini-action-button"
            type="button"
            onClick={() => handleCopyEvidence(copyId, quote.quote)}
          >
            {copyLabel}
          </button>
        </div>
      </motion.article>
    );
  }

  return (
    <article className="panel result-panel" data-testid="result-panel">
      <div className="section-head">
        <h2 className="panel-title">{TASK_LABELS[result?.task_type ?? activeTaskType]}结果</h2>
      </div>
      <AnimatePresence mode="wait" initial={false}>
        {error ? (
          <motion.div
            key={stateKey}
            className="error status-card result-error-card"
            exit={{ opacity: 0, y: -10 }}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.22, ease: MOTION_EASE }}
          >
            <span>{error}</span>
            {canRetry && onRetry ? (
              <button
                className="ghost-button result-retry-button"
                data-testid="retry-task-button"
                type="button"
                onClick={onRetry}
              >
                重试当前任务
              </button>
            ) : null}
          </motion.div>
        ) : loading ? (
          <motion.div
            key={stateKey}
            className="result-skeleton"
            exit={{ opacity: 0, y: -10 }}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.26, ease: MOTION_EASE }}
          >
            <div className="skeleton-status">
              <span className="skeleton-pulse" aria-hidden="true" />
              <span className="skeleton-status-text">{loadMessage || "正在处理..."}</span>
            </div>
            <div className="skeleton-badges">
              <span className="skeleton skeleton-badge" style={{ width: 64 }} />
              <span className="skeleton skeleton-badge" style={{ width: 52 }} />
              <span className="skeleton skeleton-badge" style={{ width: 72 }} />
            </div>
            <div className="skeleton-meta-grid">
              <div className="skeleton skeleton-meta-card" />
              <div className="skeleton skeleton-meta-card" />
              <div className="skeleton skeleton-meta-card" />
              <div className="skeleton skeleton-meta-card" />
            </div>
            <div className="skeleton-terminal">
              <div className="skeleton-terminal-head" aria-hidden="true">
                <span />
                <span />
                <span />
              </div>
              <div className="skeleton-terminal-body">
                <span className="skeleton skeleton-line" style={{ width: "92%" }} />
                <span className="skeleton skeleton-line" style={{ width: "78%" }} />
                <span className="skeleton skeleton-line" style={{ width: "88%" }} />
                <span className="skeleton skeleton-line" style={{ width: "64%" }} />
                <span className="skeleton skeleton-line" style={{ width: "84%" }} />
                <span className="skeleton skeleton-line" style={{ width: "42%" }} />
              </div>
            </div>
          </motion.div>
        ) : !result ? (
          <motion.div
            key={stateKey}
            className="empty-state"
            exit={{ opacity: 0, y: -10 }}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.22, ease: MOTION_EASE }}
          >
            <div className="empty-state-glyph" aria-hidden="true">
              <span />
              <span />
              <span />
            </div>
            <p className="empty-state-title">等待你的第一次提问</p>
            <p className="empty-state-hint">
              提交任务后，这里会展示完整结果、模型路由、以及可回跳 PDF 的证据片段。
            </p>
          </motion.div>
        ) : (
          <motion.div
            key={stateKey}
            className="result"
            exit={{ opacity: 0, y: -14 }}
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.32, ease: MOTION_EASE }}
          >
            {result.outcome === "refused" ? (
              <motion.div
                className="refusal-card primary-answer-card"
                data-testid="refusal-card"
                data-route-reason={result.route_reason ?? "unknown"}
                initial={{ opacity: 0, scale: 0.97 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.32, delay: 0.04, ease: MOTION_EASE }}
              >
                <div className="refusal-icon" aria-hidden="true">
                  <span /><span /><span />
                </div>
                <div className="refusal-body">
                  <strong>
                    {result.route_reason === "llm_refused"
                      ? "模型判断无直接依据，拒绝回答"
                      : "检索无命中，拒绝回答"}
                  </strong>
                  <p>{result.result}</p>
                  <span className="refusal-reason">
                    {result.route_reason === "llm_refused"
                      ? "系统检索到相关片段，但模型判断证据不足以直接支撑回答。"
                      : "系统在文档中未找到与该问题相关的片段。"}
                  </span>
                </div>
              </motion.div>
            ) : (
              <motion.div
                className="terminal-shell terminal-shell-sweep primary-answer-card"
                initial={{ opacity: 0, scale: 0.985 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.32, delay: 0.04, ease: MOTION_EASE }}
              >
                <div className="terminal-head">
                  <div className="terminal-lights" aria-hidden="true">
                    <span />
                    <span />
                    <span />
                  </div>
                  <div className="terminal-actions">
                    <span className="terminal-label">{TASK_LABELS[result.task_type]}输出</span>
                    <button
                      className="copy-button"
                      data-state={copyState}
                      type="button"
                      onClick={handleCopyResult}
                    >
                      {copyState === "done"
                        ? "已复制"
                        : copyState === "error"
                          ? "复制失败"
                          : "复制结果"}
                    </button>
                    <button
                      className="copy-button"
                      data-state={exportState}
                      type="button"
                      onClick={handleExportResult}
                    >
                      {exportState === "done"
                        ? "已导出"
                        : exportState === "error"
                          ? "导出失败"
                          : "导出 Markdown"}
                    </button>
                  </div>
                </div>
                <div className="terminal-output markdown-stage" data-testid="result-output">
                  <MarkdownResult content={result.result} />
                </div>
              </motion.div>
            )}

            {result.task_type === "ask" ? (
              <motion.div
                className="contrast-anchor"
                data-testid="contrast-anchor"
                {...revealMotion(0.06)}
              >
                <div className="contrast-col contrast-col-plain">
                  <span className="contrast-kicker">普通问答</span>
                  <span className="contrast-text">
                    {result.outcome === "refused"
                      ? "多半会硬编一个看似合理的答案"
                      : "只给结论，难核验、可能编造"}
                  </span>
                </div>
                <span className="contrast-arrow" aria-hidden="true">→</span>
                <div className="contrast-col contrast-col-ours">
                  <span className="contrast-kicker">研答通</span>
                  <span className="contrast-text">
                    {result.outcome === "refused"
                      ? "检索无依据 → 主动拒答，绝不编造"
                      : `${citationCount > 0 ? `${citationCount} 条原文引用` : "逐字原文校验"}${
                          retrievedPages.length > 0
                            ? ` · 可点回 PDF 第 ${retrievedPages.join("、")} 页`
                            : ""
                        } · 离题自动拒答`}
                  </span>
                </div>
              </motion.div>
            ) : null}

            {confidenceBar ? (
              <motion.div
                className={`confidence-bar confidence-bar-${confidenceBar.level}`}
                data-testid="confidence-bar"
                {...revealMotion(0.08)}
              >
                <div className="confidence-bar-indicator" aria-hidden="true">
                  <span className="confidence-dot" />
                  <span className="confidence-dot" />
                  <span className="confidence-dot" />
                </div>
                <div className="confidence-bar-text">
                  <strong>{confidenceBar.label}</strong>
                  <span>{confidenceBar.detail}</span>
                </div>
              </motion.div>
            ) : null}

            {showEvidenceSummary && evidenceSummary ? (
              <motion.div
                className={`evidence-mode-card evidence-mode-${evidenceSummary.tone}`}
                data-testid={`evidence-mode-card-${evidenceSummary.tone}`}
                data-evidence-mode={evidenceSummary.tone}
                {...revealMotion(0.2)}
              >
                <strong>{evidenceSummary.title}</strong>
                <span>{evidenceSummary.description}</span>
              </motion.div>
            ) : null}

            {evidenceItems.length > 0 ? (
              <motion.div className="citations" {...revealMotion(0.34)}>
                <h3>{getEvidenceSectionTitle(result, evidenceMode)}</h3>
                <p className="citation-helper">{evidenceSummary?.description}</p>
                <div className="citation-list">
                  {evidenceItems.map((item, index) => renderEvidenceCard(item, index, 0.4))}
                </div>
              </motion.div>
            ) : null}

            {(result.evidence_quotes ?? []).length > 0 ? (
              <motion.div className="evidence-quotes" {...revealMotion(0.42)}>
                <h3>证据摘录</h3>
                <div className="citation-list">
                  {(result.evidence_quotes ?? []).map((quote, index) =>
                    renderEvidenceQuote(quote, index, result.request_id, 0.48)
                  )}
                </div>
              </motion.div>
            ) : null}

            {showDigestEvidenceCard ? (
              <motion.div className="digest-evidence-card" data-testid="digest-evidence-card" {...revealMotion(0.46)}>
                <div>
                  <span>速读可信度提示</span>
                  <strong>已保留来源片段，可继续追问回链</strong>
                </div>
                <div className="digest-evidence-metrics">
                  <span>{evidenceItems.length} 个来源片段</span>
                  <span>{sourcePageCount > 0 ? `覆盖 ${sourcePageCount} 页` : "页码待补充"}</span>
                  <span>{followUpQuestions.length} 个可追问问题</span>
                </div>
              </motion.div>
            ) : null}

            {result.task_type === "ask" && ledgerEnabled ? (
              <motion.div
                className="duanyun-ledger"
                data-testid="duanyun-ledger"
                {...revealMotion(0.5)}
              >
                <div className="duanyun-ledger-head">
                  <span className="duanyun-ledger-kicker">端云协同 · 本次账本</span>
                  <strong>近端就近压缩，云端只接收必要上下文</strong>
                </div>
                <div className="result-meta-grid">
                  <div className="result-meta-card">
                    <span>上下文压缩（按字符）</span>
                    <strong>
                      {ledgerUploadPct !== null ? `仅上送 ${ledgerUploadPct.toFixed(1)}%` : "—"}
                    </strong>
                  </div>
                  <div className="result-meta-card">
                    <span>平台 input token</span>
                    <strong>
                      {typeof ledgerPromptTokens === "number"
                        ? ledgerPromptTokens.toLocaleString()
                        : "—"}
                    </strong>
                  </div>
                  <div className="result-meta-card">
                    <span>命中证据</span>
                    <strong>
                      {result.retrieved_chunk_count} 片段 / {retrievedPages.length} 页
                    </strong>
                  </div>
                  <div className="result-meta-card">
                    <span>平台 request id</span>
                    <strong>{ledgerPlatformId ?? "—"}</strong>
                  </div>
                  <div className="result-meta-card">
                    <span>智能体自评</span>
                    <strong>
                      {(result.agent_iterations ?? 1) > 1
                        ? "二轮（自评证据不足 → 再检索确认）"
                        : "单轮收敛"}
                    </strong>
                  </div>
                </div>
                <p className="duanyun-ledger-note">
                  {ledgerHasCompression
                    ? `原文 ${ledgerFullChars.toLocaleString()} 字符 → 实际上送约 ${ledgerSentChars.toLocaleString()} 字符（按字符口径，省约 ${Math.max(0, 100 - (ledgerUploadPct ?? 0)).toFixed(1)}%）。`
                    : "本次文档规模未知或未启用上下文压缩。"}
                  {result.cache_hit ? " 命中本地缓存，本次未实际调用云端。" : ""}
                  {ledgerPlatformId ? " 平台 request id 可在无问芯穹控制台逐条对账。" : ""}
                </p>
              </motion.div>
            ) : null}

            <details className="result-details" data-testid="result-details">
              <summary>
                <span>查看运行细节</span>
                <small>{`${result.latency_ms} ms`}</small>
              </summary>

              <motion.div className="result-badges" {...revealMotion(0.04)}>
                <span className="badge badge-task">{TASK_LABELS[result.task_type]}</span>
                <span className="badge badge-route">{result.route_tier ?? "default"}</span>
                <span className="badge badge-outcome">{result.outcome}</span>
                {result.response_detail_level ? (
                  <span className="badge badge-detail">
                    {RESPONSE_DETAIL_LABELS[result.response_detail_level] ??
                      result.response_detail_level}
                  </span>
                ) : null}
                {result.task_type === "ask" ? (
                  <span
                    className="badge badge-evidence"
                    data-testid={`evidence-mode-${evidenceMode}`}
                    data-evidence-mode={evidenceMode}
                  >
                    {EVIDENCE_MODE_LABELS[evidenceMode]}
                  </span>
                ) : null}
              </motion.div>

              <motion.div className="result-meta-grid" {...revealMotion(0.12)}>
                <div className="result-meta-card">
                  <span>{modelMetaLabel}</span>
                  <strong>{modelMetaValue}</strong>
                </div>
                {result.route_reason ? (
                  <div className="result-meta-card">
                    <span>路由原因</span>
                    <strong>{result.route_reason}</strong>
                  </div>
                ) : null}
                <div className="result-meta-card">
                  <span>耗时</span>
                  <strong>{result.latency_ms} ms</strong>
                </div>
                {!isRetrievalGate ? (
                  <div className="result-meta-card">
                    <span>请求 ID</span>
                    <strong>{result.request_id}</strong>
                  </div>
                ) : null}
              </motion.div>

              {result.cache_hit ? (
                <motion.p className="cache-hit" {...revealMotion(0.24)}>
                  本次结果命中本地缓存。
                </motion.p>
              ) : null}
              {result.retrieval_applied ? (
                <motion.p className="status" {...revealMotion(0.26)}>
                  已从 {result.retrieved_chunk_count} 个片段构造上下文
                  {retrievedPages.length > 0
                    ? `，涉及页码：${retrievedPages.join(", ")}`
                    : ""}
                  。
                </motion.p>
              ) : null}
              {!result.retrieval_applied && result.retrieval_status === "no_match" ? (
                <motion.p className="warning" {...revealMotion(0.26)}>
                  {result.retrieval_message ?? "当前问题与文档内容相关性不足，系统已避免无依据回答。"}
                </motion.p>
              ) : null}
              {result.context_truncated ? (
                <motion.p className="warning" {...revealMotion(0.28)}>
                  {result.truncation_message ??
                    `文档内容过长，后端本次仅发送前 ${result.used_document_chars} / ${result.source_document_chars} 字符。`}
                </motion.p>
              ) : null}
              {result.token_usage?.total_tokens !== null &&
              result.token_usage?.total_tokens !== undefined ? (
                <motion.p className="status token-usage" {...revealMotion(0.3)}>
                  Token 用量：输入 {result.token_usage.prompt_tokens ?? 0} / 输出{" "}
                  {result.token_usage.completion_tokens ?? 0} / 总计 {result.token_usage.total_tokens}
                </motion.p>
              ) : null}
            </details>

            {followUpQuestions.length > 0 && onAskFollowUp ? (
              <motion.div className="follow-up-panel" {...revealMotion(0.56)}>
                <div className="follow-up-head">
                  <span>速读后的下一步</span>
                  <strong>一键追问并回到原文证据</strong>
                </div>
                <div className="follow-up-list">
                  {followUpQuestions.map((question, index) => (
                    <button
                      key={question}
                      className="follow-up-chip"
                      data-testid={`follow-up-question-${index}`}
                      type="button"
                      onClick={() => onAskFollowUp(question)}
                    >
                      {question}
                    </button>
                  ))}
                </div>
              </motion.div>
            ) : null}
          </motion.div>
        )}
      </AnimatePresence>
    </article>
  );
}
