import { AnimatePresence, motion } from "motion/react";
import { useEffect, useState } from "react";
import MarkdownResult from "./MarkdownResult";
import type { ResponseDetailLevel, TaskResult, TaskType } from "../types";

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
  error: string | null;
  loading: boolean;
  loadMessage: string;
  result: TaskResult | null;
  canOpenPdfPreview?: boolean;
  onOpenPdfPage?: (pages: number[], snippet: string) => void;
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
  const stateKey = error ? "error" : loading ? "loading" : result ? result.request_id : "idle";
  const previewableItems = result
    ? result.task_type === "ask"
      ? result.citations
      : result.source_chunks
    : [];

  useEffect(() => {
    setCopyState("idle");
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
            提交任务后，这里会展示完整结果、来源信息和路由详情。
          </motion.p>
        ) : (
          <motion.div
            key={stateKey}
            className="result"
            exit={{ opacity: 0, y: -14 }}
            initial={{ opacity: 0, y: 18 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.32, ease: MOTION_EASE }}
          >
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

            <div className="result-meta-grid">
              <div className="result-meta-card">
                <span>模型</span>
                <strong>{result.model_name}</strong>
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
              <div className="result-meta-card">
                <span>请求 ID</span>
                <strong>{result.request_id}</strong>
              </div>
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
            {result.token_usage?.total_tokens ? (
              <p className="status token-usage">
                Token 用量：输入 {result.token_usage.prompt_tokens ?? 0} / 输出{" "}
                {result.token_usage.completion_tokens ?? 0} / 总计{" "}
                {result.token_usage.total_tokens}
              </p>
            ) : null}

            {previewableItems.length > 0 ? (
              <div className="citation-list">
                {previewableItems.map((item, index) => {
                  const cardContent = (
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
                      {cardContent}
                    </motion.button>
                  ) : (
                    <motion.article
                      key={item.chunk_id}
                      className="citation-card"
                      {...revealMotion(index * 0.04)}
                    >
                      {cardContent}
                    </motion.article>
                  );
                })}
              </div>
            ) : null}

            {result.evidence_quotes.length > 0 ? (
              <div className="evidence-quotes">
                <h3>证据摘录</h3>
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

            <motion.div
              className="terminal-shell"
              initial={{ opacity: 0, scale: 0.985 }}
              animate={{ opacity: 1, scale: 1 }}
              transition={{ duration: 0.28, delay: 0.08, ease: MOTION_EASE }}
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
                </div>
              </div>
              <div className="terminal-output markdown-stage">
                <MarkdownResult content={result.result} />
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>
    </article>
  );
}
