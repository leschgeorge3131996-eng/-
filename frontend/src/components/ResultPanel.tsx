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

type ResultPanelProps = {
  activeTaskType: TaskType;
  error: string | null;
  loading: boolean;
  loadMessage: string;
  result: TaskResult | null;
  canOpenPdfPreview?: boolean;
  onOpenPdfPage?: (citation: Citation) => void;
};

export default function ResultPanel({
  activeTaskType,
  error,
  loading,
  loadMessage,
  result,
  canOpenPdfPreview = false,
  onOpenPdfPage
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
  const isRetrievalGate = result ? isRetrievalGateResult(result) : false;
  const modelMetaLabel = isRetrievalGate ? "执行路径" : "模型";
  const modelMetaValue = isRetrievalGate
    ? "retrieval_gate（未调用模型）"
    : (result?.model_name ?? "-");

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
          <motion.p
            key={stateKey}
            className="error status-card"
            exit={{ opacity: 0, y: -10 }}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.22, ease: MOTION_EASE }}
          >
            {error}
          </motion.p>
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

            {evidenceSummary ? (
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

            {result.outcome === "refused" ? (
              <motion.div
                className="refusal-card"
                data-testid="refusal-card"
                initial={{ opacity: 0, scale: 0.97 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.32, delay: 0.5, ease: MOTION_EASE }}
              >
                <div className="refusal-icon" aria-hidden="true">
                  <span /><span /><span />
                </div>
                <div className="refusal-body">
                  <strong>检索无命中，拒绝回答</strong>
                  <p>{result.result}</p>
                  <span className="refusal-reason">
                    系统在文档中未找到与该问题相关的片段，已在检索阶段拦截，未调用模型生成。
                  </span>
                </div>
              </motion.div>
            ) : (
              <motion.div
                className="terminal-shell terminal-shell-sweep"
                initial={{ opacity: 0, scale: 0.985 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.32, delay: 0.5, ease: MOTION_EASE }}
              >
                <div className="terminal-head">
                  <div className="terminal-lights" aria-hidden="true">
                    <span />
                    <span />
                    <span />
                  </div>
                  <div className="terminal-actions">
                    <span className="terminal-label">{TASK_LABELS[result.task_type]}输出</span>
                    <button className="copy-button" type="button" onClick={handleCopyResult}>
                      {copyState === "done"
                        ? "已复制"
                        : copyState === "error"
                          ? "复制失败"
                          : "复制结果"}
                    </button>
                    <button className="copy-button" type="button" onClick={handleExportResult}>
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
          </motion.div>
        )}
      </AnimatePresence>
    </article>
  );
}
