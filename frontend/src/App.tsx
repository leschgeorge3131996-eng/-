import { motion } from "motion/react";
import { useEffect, useRef, useState, type FormEvent } from "react";
import {
  ApiRequestError,
  buildFileContentUrl,
  fetchLogSummary,
  runTask,
  uploadDocument
} from "./api";
import PdfPreviewPanel from "./components/PdfPreviewPanel";
import ResultPanel from "./components/ResultPanel";
import type {
  LogSummary,
  RecentDocument,
  RecentResult,
  ResponseDetailLevel,
  TaskType,
  UploadMetadata
} from "./types";

const TASK_OPTIONS: Array<{ value: TaskType; label: string; placeholder: string }> = [
  { value: "summary", label: "摘要", placeholder: "例如：请突出研究背景、方法和创新点。" },
  { value: "ask", label: "问答", placeholder: "例如：这篇文档的核心方法是什么？" },
  { value: "outline", label: "提纲生成", placeholder: "例如：请生成 6 页答辩提纲。" }
];

const DEMO_ACTIONS = [
  {
    label: "示例摘要",
    description: "快速验证摘要链路",
    taskType: "summary" as const,
    input: "请用 3 条要点总结这个文档。"
  },
  {
    label: "示例问答",
    description: "验证检索与引用",
    taskType: "ask" as const,
    input: "这个项目第一阶段要做什么？"
  },
  {
    label: "示例提纲",
    description: "验证结构化提纲生成",
    taskType: "outline" as const,
    input: "请生成一个 5 页汇报提纲。"
  }
];

const RESPONSE_DETAIL_OPTIONS: Array<{
  value: ResponseDetailLevel;
  label: string;
  description: string;
}> = [
  { value: "concise", label: "简洁", description: "只保留核心结论" },
  { value: "balanced", label: "适中", description: "兼顾完整与可读性" },
  { value: "detailed", label: "详细", description: "补充更多背景与展开" }
];

const TASK_LABELS: Record<TaskType, string> = {
  summary: "摘要",
  ask: "问答",
  outline: "提纲生成"
};

const HERO_PILLS = ["页级结构", "轻量检索", "证据回链", "样例复跑"];
const RECENT_DOCUMENTS_KEY = "yandatong_recent_documents";
const RECENT_RESULTS_KEY = "yandatong_recent_results";
const DEMO_DOCUMENT_NAME = "demo_research_brief.md";
const DEMO_DOCUMENT_CONTENT = `# 项目简介

研答通是一个面向科研与智能办公场景的个人智能文档助理。
第一阶段目标是支持用户上传文档，完成摘要、问答和提纲生成。`;

function readStorage<T>(key: string, fallback: T): T {
  try {
    const raw = window.localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
}

function writeStorage<T>(key: string, value: T): void {
  window.localStorage.setItem(key, JSON.stringify(value));
}

function describeLoadStage(stage: "idle" | "uploading" | "model"): string {
  if (stage === "uploading") return "正在上传并解析文档...";
  if (stage === "model") return "模型处理中，首次请求可能需要 10 到 40 秒。";
  return "";
}

function normalizeErrorMessage(error: unknown): string {
  if (error instanceof ApiRequestError) return error.message;
  if (error instanceof Error) return error.message;
  return "提交任务失败";
}

function toUploadMetadata(document: RecentDocument): UploadMetadata {
  return {
    file_id: document.file_id,
    original_name: document.original_name,
    file_type: document.file_type,
    size_bytes: 0,
    text_chars: document.text_chars,
    page_count: document.page_count,
    chunk_count: document.chunk_count,
    document_fingerprint: document.document_fingerprint ?? null,
    parse_status: document.parse_status
  };
}

export default function App() {
  const [taskType, setTaskType] = useState<TaskType>("summary");
  const [responseDetailLevel, setResponseDetailLevel] = useState<ResponseDetailLevel>("balanced");
  const [input, setInput] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadedMetadata, setUploadedMetadata] = useState<UploadMetadata | null>(null);
  const [result, setResult] = useState<RecentResult["task_result"] | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadStage, setLoadStage] = useState<"idle" | "uploading" | "model">("idle");
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [previewOpen, setPreviewOpen] = useState(false);
  const [previewPage, setPreviewPage] = useState(1);
  const [previewPages, setPreviewPages] = useState<number[]>([1]);
  const [previewSnippet, setPreviewSnippet] = useState<string | null>(null);
  const [recentDocuments, setRecentDocuments] = useState<RecentDocument[]>(() =>
    readStorage(RECENT_DOCUMENTS_KEY, [])
  );
  const [recentResults, setRecentResults] = useState<RecentResult[]>(() =>
    readStorage(RECENT_RESULTS_KEY, [])
  );
  const [logSummary, setLogSummary] = useState<LogSummary | null>(null);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const currentOption = TASK_OPTIONS.find((item) => item.value === taskType)!;
  const pendingDocument = selectedFile && !uploadedMetadata ? selectedFile : null;
  const pendingDocumentType =
    pendingDocument?.name.split(".").pop()?.toLowerCase() ?? pendingDocument?.type ?? "-";
  const canSubmit =
    !loading &&
    Boolean(selectedFile || uploadedMetadata) &&
    (taskType !== "ask" || Boolean(input.trim()));
  const previewMetadata = uploadedMetadata?.file_type === "pdf" ? uploadedMetadata : null;

  useEffect(() => {
    writeStorage(RECENT_DOCUMENTS_KEY, recentDocuments);
  }, [recentDocuments]);

  useEffect(() => {
    writeStorage(RECENT_RESULTS_KEY, recentResults);
  }, [recentResults]);

  useEffect(() => {
    void fetchLogSummary().then(setLogSummary).catch(() => setLogSummary(null));
  }, [result]);

  function applyActiveDocument(metadata: UploadMetadata | null, page = 1, pages: number[] = [page]) {
    setUploadedMetadata(metadata);
    setSelectedFile(null);
    setPreviewPage(page);
    setPreviewPages(pages.length > 0 ? pages : [page]);
    setPreviewOpen(Boolean(metadata && metadata.file_type === "pdf"));
    if (!metadata || metadata.file_type !== "pdf") {
      setPreviewSnippet(null);
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  }

  function restoreRecentDocument(document: RecentDocument) {
    setPreviewSnippet(null);
    applyActiveDocument(toUploadMetadata(document), 1, [1]);
    setResult(null);
    setError(null);
  }

  function restoreRecentResult(item: RecentResult) {
    const fallbackDocument = recentDocuments.find(
      (document) => document.file_id === item.task_result.file_id
    );
    const restoredMetadata =
      item.document_snapshot ?? (fallbackDocument ? toUploadMetadata(fallbackDocument) : null);
    const firstPage =
      (item.task_result.task_type === "ask"
        ? item.task_result.citations[0]?.page_numbers[0] ?? item.task_result.retrieved_pages[0]
        : item.task_result.source_chunks[0]?.page_numbers[0]) ?? 1;
    const firstSnippet =
      (item.task_result.task_type === "ask"
        ? item.task_result.citations[0]?.snippet ?? item.task_result.evidence_quotes[0]?.quote
        : item.task_result.source_chunks[0]?.snippet) ?? null;
    const candidatePages =
      (item.task_result.task_type === "ask"
        ? item.task_result.citations[0]?.page_numbers ?? item.task_result.retrieved_pages
        : item.task_result.source_chunks[0]?.page_numbers) ?? [firstPage];

    setTaskType(item.task_type);
    if (item.task_result.response_detail_level) {
      setResponseDetailLevel(item.task_result.response_detail_level);
    }
    setInput(item.input);
    setResult(item.task_result);
    setError(null);
    setPreviewSnippet(firstSnippet);
    setPreviewPages(candidatePages.length > 0 ? candidatePages : [firstPage]);
    applyActiveDocument(restoredMetadata, firstPage, candidatePages);
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setLoadStage("idle");
    setError(null);

    try {
      let metadata = uploadedMetadata;
      let fileId = metadata?.file_id ?? "";

      if (selectedFile) {
        setLoadStage("uploading");
        const upload = await uploadDocument(selectedFile, setUploadProgress);
        const nextMetadata = upload.metadata;
        metadata = nextMetadata;
        fileId = nextMetadata.file_id;
        setUploadedMetadata(nextMetadata);
        setSelectedFile(null);
        setRecentDocuments((current) =>
          [
            {
              file_id: nextMetadata.file_id,
              original_name: nextMetadata.original_name,
              document_fingerprint: nextMetadata.document_fingerprint,
              file_type: nextMetadata.file_type,
              text_chars: nextMetadata.text_chars,
              page_count: nextMetadata.page_count,
              chunk_count: nextMetadata.chunk_count,
              parse_status: nextMetadata.parse_status,
              saved_at: new Date().toISOString()
            },
            ...current.filter((item) => item.file_id !== nextMetadata.file_id)
          ].slice(0, 5)
        );
      }

      if (!fileId) throw new Error("请先上传一个文档。");

      setLoadStage("model");
      const taskResult = await runTask(taskType, fileId, input.trim(), responseDetailLevel);
      setResult(taskResult);
      if (metadata?.file_type === "pdf") {
        const defaultSnippet =
          taskResult.task_type === "ask"
            ? taskResult.citations[0]?.snippet ?? taskResult.evidence_quotes[0]?.quote ?? null
            : taskResult.source_chunks[0]?.snippet ?? null;
        const defaultPages =
          (taskResult.task_type === "ask"
            ? taskResult.citations[0]?.page_numbers ?? taskResult.retrieved_pages
            : taskResult.source_chunks[0]?.page_numbers) ?? [1];
        setPreviewSnippet(defaultSnippet);
        setPreviewPages(defaultPages.length > 0 ? defaultPages : [1]);
        setPreviewOpen(true);
      }
      setRecentResults((current) =>
        [
          {
            id: taskResult.request_id,
            task_type: taskResult.task_type,
            input: input.trim(),
            created_at: new Date().toISOString(),
            document_snapshot: metadata,
            task_result: taskResult
          },
          ...current
        ].slice(0, 5)
      );
    } catch (submitError) {
      setError(normalizeErrorMessage(submitError));
      setResult(null);
    } finally {
      setLoading(false);
      setLoadStage("idle");
      setUploadProgress(0);
      if (fileInputRef.current && !selectedFile) {
        fileInputRef.current.value = "";
      }
    }
  }

  return (
    <div className="page">
      <main className="container">
        <section className="hero">
          <div className="hero-copy">
            <p className="eyebrow">面向科研与智能办公的文档工作台</p>
            <h1 className="brandmark">研答通</h1>
            <div className="hero-flow" aria-label="文档任务流程">
              <span className="flow-step">上传</span>
              <span className="flow-separator" aria-hidden="true" />
              <span className="flow-step">解析</span>
              <span className="flow-separator" aria-hidden="true" />
              <span className="flow-step">检索</span>
              <span className="flow-separator" aria-hidden="true" />
              <span className="flow-step">生成</span>
            </div>
            <p className="subtitle">上传文档，完成摘要、问答和提纲生成，并把结果变成可解释的工作流。</p>
          </div>
          <div className="hero-pills">
            {HERO_PILLS.map((pill) => (
              <motion.span key={pill} className="hero-pill">
                {pill}
              </motion.span>
            ))}
          </div>
        </section>

        <section className="dashboard-grid">
          <article className="panel stats-panel">
            <div className="section-head">
              <h2 className="panel-title">当前系统状态</h2>
            </div>
            {logSummary ? (
              <div className="stats-grid">
                <div className="stat-card">
                  <span>总请求数</span>
                  <strong>{logSummary.total_requests}</strong>
                </div>
                <div className="stat-card">
                  <span>有效回答数</span>
                  <strong>{logSummary.answered_count}</strong>
                </div>
                <div className="stat-card">
                  <span>拒答数</span>
                  <strong>{logSummary.refused_count}</strong>
                </div>
                <div className="stat-card">
                  <span>错误数</span>
                  <strong>{logSummary.error_count}</strong>
                </div>
                <div className="stat-card">
                  <span>平均延迟</span>
                  <strong>{logSummary.average_latency_ms} ms</strong>
                </div>
                <div className="stat-card">
                  <span>P95 延迟</span>
                  <strong>{logSummary.p95_latency_ms} ms</strong>
                </div>
              </div>
            ) : (
              <p className="empty">当前暂无统计数据，完成一次任务后会自动刷新。</p>
            )}
          </article>

          <article className="panel demo-panel">
            <div className="section-head">
              <h2 className="panel-title">一键演示入口</h2>
            </div>
            <p className="subtitle compact">先填入示例文档，再切换任务，快速演示完整链路。</p>
            <div className="demo-actions">
              <button
                className="hero-button"
                type="button"
                disabled={loading}
                onClick={() => {
                  const file = new File([DEMO_DOCUMENT_CONTENT], DEMO_DOCUMENT_NAME, {
                    type: "text/markdown"
                  });
                  setSelectedFile(file);
                  setUploadedMetadata(null);
                  setResult(null);
                  setError(null);
                  setPreviewOpen(false);
                  setPreviewPage(1);
                  setPreviewPages([1]);
                  setPreviewSnippet(null);
                }}
              >
                填充示例文档
              </button>
              {DEMO_ACTIONS.map((action) => (
                <button
                  key={action.label}
                  className="demo-card"
                  type="button"
                  disabled={loading}
                  onClick={() => {
                    setTaskType(action.taskType);
                    setInput(action.input);
                  }}
                >
                  <strong>{action.label}</strong>
                  <span>{action.description}</span>
                </button>
              ))}
            </div>
            {pendingDocument ? (
              <p className="demo-feedback">
                已填入待处理文档：{pendingDocument.name}。点击“提交任务”后会自动上传并执行。
              </p>
            ) : null}
          </article>
        </section>

        <section className="workspace">
          <article className="panel control-panel">
            <div className="section-head">
              <h2 className="panel-title">上传文档并启动任务</h2>
            </div>
            <form className="form" onSubmit={handleSubmit}>
              <label className="field">
                <span>上传文档</span>
                <input
                  ref={fileInputRef}
                  type="file"
                  accept=".txt,.md,.pdf,text/plain,text/markdown,application/pdf"
                  disabled={loading}
                  onChange={(event) => {
                    const file = event.target.files?.[0] ?? null;
                    setSelectedFile(file);
                    if (file) {
                      setUploadedMetadata(null);
                      setResult(null);
                      setError(null);
                      setPreviewOpen(false);
                      setPreviewPage(1);
                      setPreviewPages([1]);
                      setPreviewSnippet(null);
                    }
                  }}
                />
              </label>
              {loading && (loadStage === "uploading" || loadStage === "model" || uploadProgress > 0) ? (
                <div className="upload-progress">
                  <div className="upload-progress-meta">
                    <span>{describeLoadStage(loadStage)}</span>
                    <strong>{loadStage === "model" ? 100 : uploadProgress}%</strong>
                  </div>
                  <div className="upload-progress-track" aria-hidden="true">
                    <div
                      className="upload-progress-fill"
                      style={{ width: `${loadStage === "model" ? 100 : uploadProgress}%` }}
                    />
                  </div>
                </div>
              ) : null}
              <label className="field">
                <span>任务类型</span>
                <select
                  value={taskType}
                  disabled={loading}
                  onChange={(event) => setTaskType(event.target.value as TaskType)}
                >
                  {TASK_OPTIONS.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label}
                    </option>
                  ))}
                </select>
              </label>
              <label className="field">
                <span>回答粒度</span>
                <select
                  value={responseDetailLevel}
                  disabled={loading}
                  onChange={(event) =>
                    setResponseDetailLevel(event.target.value as ResponseDetailLevel)
                  }
                >
                  {RESPONSE_DETAIL_OPTIONS.map((option) => (
                    <option key={option.value} value={option.value}>
                      {option.label} / {option.description}
                    </option>
                  ))}
                </select>
              </label>
              <label className="field">
                <span>问题或指令</span>
                <textarea
                  rows={6}
                  value={input}
                  placeholder={currentOption.placeholder}
                  disabled={loading}
                  onChange={(event) => setInput(event.target.value)}
                />
              </label>
              <div className="control-actions">
                <button className="submit" type="submit" disabled={!canSubmit}>
                  {loading ? "处理中..." : "提交任务"}
                </button>
                <p className="control-hint">建议先用 Demo 模式体验完整链路，再换真实文档。</p>
              </div>
            </form>

            <div className="document-brief">
              <div className="section-head compact-head">
                <p className="section-kicker">当前文档</p>
                <h3>
                  {uploadedMetadata
                    ? uploadedMetadata.original_name
                    : pendingDocument
                      ? pendingDocument.name
                      : "暂无文档"}
                </h3>
              </div>
              {uploadedMetadata ? (
                <div className="meta-grid">
                  <div className="meta-chip">
                    <span>类型</span>
                    <strong>{uploadedMetadata.file_type}</strong>
                  </div>
                  <div className="meta-chip">
                    <span>字符数</span>
                    <strong>{uploadedMetadata.text_chars}</strong>
                  </div>
                  <div className="meta-chip">
                    <span>页数</span>
                    <strong>{uploadedMetadata.page_count}</strong>
                  </div>
                  <div className="meta-chip">
                    <span>分块数</span>
                    <strong>{uploadedMetadata.chunk_count}</strong>
                  </div>
                </div>
              ) : pendingDocument ? (
                <div className="meta-grid">
                  <div className="meta-chip">
                    <span>状态</span>
                    <strong>待上传</strong>
                  </div>
                  <div className="meta-chip">
                    <span>类型</span>
                    <strong>{pendingDocumentType}</strong>
                  </div>
                  <div className="meta-chip">
                    <span>来源</span>
                    <strong>{pendingDocument.name === DEMO_DOCUMENT_NAME ? "示例文档" : "本地文件"}</strong>
                  </div>
                  <div className="meta-chip">
                    <span>下一步</span>
                    <strong>点击提交开始处理</strong>
                  </div>
                </div>
              ) : (
                <p className="empty">上传后这里会显示当前文档的规模与结构信息。</p>
              )}
              {uploadedMetadata || pendingDocument ? (
                <div className="inline-actions">
                  {previewMetadata && !previewOpen ? (
                    <button
                      className="ghost-button"
                      type="button"
                      disabled={loading}
                      onClick={() => setPreviewOpen(true)}
                    >
                      打开 PDF 预览
                    </button>
                  ) : null}
                  <button
                    className="ghost-button"
                    type="button"
                    disabled={loading}
                    onClick={() => {
                      setUploadedMetadata(null);
                      setSelectedFile(null);
                      setResult(null);
                      setError(null);
                      setPreviewOpen(false);
                      setPreviewPage(1);
                      setPreviewPages([1]);
                      setPreviewSnippet(null);
                      if (fileInputRef.current) {
                        fileInputRef.current.value = "";
                      }
                    }}
                  >
                    清空当前文档
                  </button>
                </div>
              ) : null}
            </div>
          </article>

          <ResultPanel
            activeTaskType={taskType}
            error={error}
            loading={loading}
            loadMessage={describeLoadStage(loadStage)}
            result={result}
            canOpenPdfPreview={Boolean(previewMetadata)}
            onOpenPdfPage={(pages, snippet) => {
              const nextPages = pages.length > 0 ? pages : [1];
              setPreviewPages(nextPages);
              setPreviewPage(nextPages[0] ?? 1);
              setPreviewSnippet(snippet);
              setPreviewOpen(true);
            }}
          />
        </section>

        {previewMetadata && previewOpen ? (
          <PdfPreviewPanel
            documentName={previewMetadata.original_name}
            fileId={previewMetadata.file_id}
            page={previewPage}
            availablePages={previewPages}
            src={buildFileContentUrl(previewMetadata.file_id, previewPage)}
            highlightText={previewSnippet}
            onSelectPage={(page) => setPreviewPage(page)}
            onClose={() => setPreviewOpen(false)}
          />
        ) : null}

        <section className="grid secondary-grid history-section">
          <article className="panel">
            <div className="section-head compact-head">
              <h2 className="panel-title">最近文档</h2>
            </div>
            {recentDocuments.length === 0 ? (
              <p className="empty">最近上传的文档会显示在这里，便于复用。</p>
            ) : (
              <div className="history-list">
                {recentDocuments.map((item) => (
                  <button
                    key={item.file_id}
                    className="history-card"
                    type="button"
                    disabled={loading}
                    onClick={() => restoreRecentDocument(item)}
                  >
                    <strong>{item.original_name}</strong>
                    <span>{item.file_type} / {item.page_count} pages / {item.chunk_count} chunks</span>
                  </button>
                ))}
              </div>
            )}
          </article>
          <article className="panel">
            <div className="section-head compact-head">
              <h2 className="panel-title">最近结果</h2>
            </div>
            {recentResults.length === 0 ? (
              <p className="empty">最近 5 次任务结果会显示在这里，方便回看演示。</p>
            ) : (
              <div className="history-list">
                {recentResults.map((item) => (
                  <button
                    key={item.id}
                    className="history-card"
                    type="button"
                    disabled={loading}
                    onClick={() => restoreRecentResult(item)}
                  >
                    <strong>{TASK_LABELS[item.task_type]}</strong>
                    <span>{item.task_result.document_name}</span>
                    <span>{item.input || "无附加输入"}</span>
                  </button>
                ))}
              </div>
            )}
          </article>
        </section>
      </main>
    </div>
  );
}
