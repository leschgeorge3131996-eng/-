import { AnimatePresence, motion } from "motion/react";
import { useEffect, useMemo, useState } from "react";
import MarkdownResult from "./MarkdownResult";
import type { ResponseDetailLevel, TaskResult, TaskType, UploadMetadata } from "../types";

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

type ResultPanelProps = {
  activeTaskType: TaskType;
  currentDocument?: UploadMetadata | null;
  error: string | null;
  loading: boolean;
  loadMessage: string;
  result: TaskResult | null;
  canOpenPdfPreview?: boolean;
  onOpenPdfPage?: (pages: number[], snippet: string) => void;
};

export default function ResultPanel({
  activeTaskType,
  currentDocument = null,
  error,
  loading,
  loadMessage,
  result,
  canOpenPdfPreview = false,
  onOpenPdfPage
}: ResultPanelProps) {
  const [copyState, setCopyState] = useState<"idle" | "done" | "error">("idle");
  const stateKey = error ? "error" : loading ? "loading" : result ? result.request_id : "idle";
  const evidenceItems = result
    ? result.task_type === "ask"
      ? result.citations
      : result.source_chunks
    : [];

  useEffect(() => {
    setCopyState("idle");
  }, [result?.request_id]);

  const usedEvidenceCount = useMemo(() => {
    if (!result) {
      return 0;
    }
    if (result.task_type === "ask") {
      return result.used_chunk_ids.length || result.citations.length;
    }
    return result.source_chunks.length;
  }, [result]);

  const compressionRate = useMemo(() => {
    if (!result || result.source_document_chars <= 0 || result.used_document_chars <= 0) {
      return null;
    }
    return Math.max(
      0,
      Math.round((1 - result.used_document_chars / result.source_document_chars) * 100)
    );
  }, [result]);

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

  function renderEvidenceCard(
    item: { chunk_id: string; page_numbers: number[]; snippet: string },
    index: number
  ) {
    const content = (
      <>
        <p className="citation-meta">页码：{item.page_numbers.join(", ")}</p>
        <p>{item.snippet}</p>
      </>
    );

    return canOpenPdfPreview && onOpenPdfPage ? (
      <motion.button
        key={item.chunk_id}
        className="citation-card citation-button"
        type="button"
        onClick={() => onOpenPdfPage(item.page_numbers, item.snippet)}
        {...revealMotion(index * 0.04)}
      >
        {content}
      </motion.button>
    ) : (
      <motion.article
        key={item.chunk_id}
        className="citation-card"
        {...revealMotion(index * 0.04)}
      >
        {content}
      </motion.article>
    );
  }

  return (
    <article className="panel result-panel">
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
          <motion.p
            key={stateKey}
            className="status status-card"
            exit={{ opacity: 0, y: -10 }}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.22, ease: MOTION_EASE }}
          >
            {loadMessage}
          </motion.p>
        ) : !result ? (
          <motion.p
            key={stateKey}
            className="empty status-card"
            exit={{ opacity: 0, y: -10 }}
            initial={{ opacity: 0, y: 12 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.22, ease: MOTION_EASE }}
          >
            提交任务后，这里会展示结果、证据、路由和请求指标。
          </motion.p>
        ) : (
          <motion.div
            key={stateKey}
            className="result-stage"
            exit={{ opacity: 0, y: -14 }}
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.32, ease: MOTION_EASE }}
          >
            <div className="result-stage-head">
              <div className="result-stage-copy">
                <p className="result-kicker">结果舞台</p>
                <h3>{TASK_LABELS[result.task_type]}输出</h3>
                <p className="result-stage-subtitle">
                  当前回答围绕文档证据链展开，你可以直接查看来源片段并回到 PDF 原页。
                </p>
              </div>
              <div className="result-badges">
                <span className="badge badge-task">{TASK_LABELS[result.task_type]}</span>
                <span className="badge badge-route">{result.route_tier ?? "default"}</span>
                <span className="badge badge-outcome">{result.outcome}</span>
                {result.response_detail_level ? (
                  <span className="badge badge-detail">
                    {RESPONSE_DETAIL_LABELS[result.response_detail_level] ??
                      result.response_detail_level}
                  </span>
                ) : null}
              </div>
            </div>

            <div className="result-path-grid">
              <div className="result-path-card">
                <label>源文档</label>
                <strong>{currentDocument?.page_count ?? result.retrieved_pages.length}</strong>
                <span>
                  {currentDocument
                    ? `${currentDocument.chunk_count} 个分块 / ${currentDocument.file_type.toUpperCase()}`
                    : result.document_name}
                </span>
              </div>
              <div className="result-path-card">
                <label>检索结果</label>
                <strong>{result.retrieved_chunk_count}</strong>
                <span>
                  {result.retrieved_pages.length > 0
                    ? `页码：${result.retrieved_pages.join(", ")}`
                    : "未使用检索"}
                </span>
              </div>
              <div className="result-path-card">
                <label>使用证据</label>
                <strong>{usedEvidenceCount}</strong>
                <span>
                  {result.task_type === "ask"
                    ? `evidence mode: ${result.evidence_mode ?? "none"}`
                    : "来源片段已选出"}
                </span>
              </div>
              <div className="result-path-card">
                <label>输出控制</label>
                <strong>
                  {result.response_detail_level
                    ? RESPONSE_DETAIL_LABELS[result.response_detail_level]
                    : "默认"}
                </strong>
                <span>{result.route_reason ?? "按当前策略路由"}</span>
              </div>
            </div>

            <div className="result-surface">
              <section className="answer-stage">
                <div className="answer-stage-head">
                  <div>
                    <h4>模型结果</h4>
                    <p>当前输出已经过结构化展示和可复制收口。</p>
                  </div>
                  <button className="copy-button stage-copy-button" type="button" onClick={handleCopyResult}>
                    {copyState === "done"
                      ? "已复制"
                      : copyState === "error"
                        ? "复制失败"
                        : "复制结果"}
                  </button>
                </div>

                <div className="answer-output">
                  <MarkdownResult content={result.result} />
                </div>

                {result.cache_hit ? <p className="cache-hit">本次结果命中本地缓存。</p> : null}
                {result.retrieval_applied ? (
                  <p className="status">
                    已从 {result.retrieved_chunk_count} 个片段构造上下文
                    {result.retrieved_pages.length > 0
                      ? `，涉及页码：${result.retrieved_pages.join(", ")}`
                      : ""}
                    。
                  </p>
                ) : null}
                {!result.retrieval_applied && result.retrieval_status === "no_match" ? (
                  <p className="warning">
                    {result.retrieval_message ?? "当前问题与文档内容相关性不足，系统已避免无依据回答。"}
                  </p>
                ) : null}
                {result.context_truncated ? (
                  <p className="warning">
                    {result.truncation_message ??
                      `文档内容过长，后端本次仅发送前 ${result.used_document_chars} / ${result.source_document_chars} 字符。`}
                  </p>
                ) : null}
              </section>

              <aside className="result-rail">
                <div className="rail-card">
                  <h4>{result.task_type === "ask" ? "引用依据" : "来源片段"}</h4>
                  {evidenceItems.length > 0 ? (
                    <div className="citation-list">
                      {evidenceItems.map((item, index) => renderEvidenceCard(item, index))}
                    </div>
                  ) : (
                    <p className="empty">当前结果没有可展示的来源片段。</p>
                  )}
                </div>

                {result.evidence_quotes.length > 0 ? (
                  <div className="rail-card">
                    <h4>证据摘录</h4>
                    <div className="citation-list">
                      {result.evidence_quotes.map((quote, index) => (
                        <motion.article
                          key={`${result.request_id}-${quote.chunk_id}-${index}`}
                          className="citation-card"
                          {...revealMotion(index * 0.04)}
                        >
                          <p className="citation-meta">证据块：{quote.chunk_id}</p>
                          <p>{quote.quote}</p>
                        </motion.article>
                      ))}
                    </div>
                  </div>
                ) : null}
              </aside>
            </div>

            <div className="result-metrics-grid">
              <div className="result-metric-card">
                <label>请求耗时</label>
                <strong>{result.latency_ms} ms</strong>
                <span>本次任务端到端耗时</span>
              </div>
              <div className="result-metric-card">
                <label>Token 用量</label>
                <strong>{result.token_usage?.total_tokens ?? 0}</strong>
                <span>
                  输入 {result.token_usage?.prompt_tokens ?? 0} / 输出{" "}
                  {result.token_usage?.completion_tokens ?? 0}
                </span>
              </div>
              <div className="result-metric-card">
                <label>请求追踪</label>
                <strong>{result.request_id}</strong>
                <span>可对齐日志与回放材料</span>
              </div>
              <div className="result-metric-card">
                <label>上下文压缩</label>
                <strong>
                  {result.source_document_chars > 0 && result.used_document_chars > 0
                    ? `${Math.max(
                        0,
                        Math.round(
                          (1 - result.used_document_chars / result.source_document_chars) * 100
                        )
                      )}%`
                    : "未压缩"}
                </strong>
                <span>
                  {result.used_document_chars} / {result.source_document_chars} 字符送模
                </span>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </article>
  );
}
