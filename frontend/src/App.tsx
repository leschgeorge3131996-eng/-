import { useEffect, useRef, useState } from "react";
import { ApiRequestError, fetchLogSummary, runTask, uploadDocument } from "./api";
import type {
  LogSummary,
  RecentDocument,
  RecentResult,
  ResponseDetailLevel,
  TaskResult,
  TaskType,
  UploadMetadata
} from "./types";

const TASK_OPTIONS: Array<{
  value: TaskType;
  label: string;
  placeholder: string;
}> = [
  {
    value: "summary",
    label: "摘要",
    placeholder: "例如：请突出研究背景、方法和创新点"
  },
  {
    value: "ask",
    label: "问答",
    placeholder: "例如：这篇文档的核心方法是什么？"
  },
  {
    value: "outline",
    label: "提纲生成",
    placeholder: "例如：请生成 6 页答辩提纲"
  }
];

const TASK_LABELS: Record<TaskType, string> = {
  summary: "摘要",
  ask: "问答",
  outline: "提纲生成"
};

const DEMO_ACTIONS: Array<{
  label: string;
  description: string;
  taskType: TaskType;
  input: string;
}> = [
  {
    label: "示例摘要",
    description: "快速验证摘要链路",
    taskType: "summary",
    input: "请用 3 条要点总结这个文档。"
  },
  {
    label: "示例问答",
    description: "验证检索与引用",
    taskType: "ask",
    input: "这个项目第一阶段要做什么？"
  },
  {
    label: "示例提纲",
    description: "验证结构化提纲生成",
    taskType: "outline",
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

const RESPONSE_DETAIL_LABELS: Record<ResponseDetailLevel, string> = {
  concise: "简洁",
  balanced: "适中",
  detailed: "详细"
};

type LoadStage = "idle" | "uploading" | "model";
type PendingDocumentSource = "demo" | "local";

const RECENT_DOCUMENTS_KEY = "yandatong_recent_documents";
const RECENT_RESULTS_KEY = "yandatong_recent_results";
const MAX_RECENT_DOCUMENTS = 5;
const MAX_RECENT_RESULTS = 5;
const DEMO_DOCUMENT_NAME = "demo_research_brief.md";
const DEMO_DOCUMENT_CONTENT = `# 项目简介

研答通是一个面向科研与智能办公场景的个人智能文档助理。
第一阶段目标是支持用户上传文档，完成摘要、问答和提纲生成。

系统当前采用端云协同路线，优先保证能跑通、能演示、能扩展。
后续将逐步补充 PDF 结构化解析、文本分块、轻量检索、引用返回和评测闭环。`;

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

function isSameRecentDocument(left: RecentDocument, right: RecentDocument): boolean {
  if (left.document_fingerprint || right.document_fingerprint) {
    return Boolean(
      left.document_fingerprint &&
        right.document_fingerprint &&
        left.document_fingerprint === right.document_fingerprint
    );
  }
  return left.original_name === right.original_name;
}

function describeLoadStage(stage: LoadStage): string {
  if (stage === "uploading") {
    return "正在上传并解析文档...";
  }
  if (stage === "model") {
    return "模型处理中，首次请求可能需要 10 到 40 秒。";
  }
  return "";
}

function describeUploadProgress(stage: LoadStage, progress: number): string {
  if (stage === "uploading") {
    if (progress >= 100) {
      return "文件已上传，正在解析文档...";
    }
    return "正在上传文件...";
  }
  if (stage === "model") {
    return "文档已就绪，正在调用模型...";
  }
  return "等待开始";
}

function resolveVisibleUploadProgress(stage: LoadStage, progress: number): number {
  if (stage === "model") {
    return 100;
  }
  return progress;
}

function normalizeErrorMessage(error: unknown): string {
  if (error instanceof ApiRequestError) {
    if (error.message.includes("请求过快") || error.message.includes("HTTP 429")) {
      return "模型当前较忙，请等待 10 到 30 秒后重试，避免连续点击。";
    }
    if (error.message.includes("超时")) {
      return "模型处理超时，请稍后重试，或换更短的文档内容。";
    }
    return error.message;
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "提交任务失败";
}

function App() {
  const [taskType, setTaskType] = useState<TaskType>("summary");
  const [responseDetailLevel, setResponseDetailLevel] = useState<ResponseDetailLevel>("balanced");
  const [input, setInput] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [pendingDocumentSource, setPendingDocumentSource] = useState<PendingDocumentSource | null>(null);
  const [uploadedMetadata, setUploadedMetadata] = useState<UploadMetadata | null>(null);
  const [result, setResult] = useState<TaskResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadStage, setLoadStage] = useState<LoadStage>("idle");
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [error, setError] = useState<string | null>(null);
  const [recentDocuments, setRecentDocuments] = useState<RecentDocument[]>(() =>
    readStorage<RecentDocument[]>(RECENT_DOCUMENTS_KEY, [])
  );
  const [recentResults, setRecentResults] = useState<RecentResult[]>(() =>
    readStorage<RecentResult[]>(RECENT_RESULTS_KEY, [])
  );
  const [logSummary, setLogSummary] = useState<LogSummary | null>(null);
  const [summaryRefreshTick, setSummaryRefreshTick] = useState(0);
  const fileInputRef = useRef<HTMLInputElement | null>(null);

  const currentOption = TASK_OPTIONS.find((item) => item.value === taskType)!;
  const activeResultTaskType = result?.task_type ?? taskType;
  const pendingDocument = selectedFile && !uploadedMetadata ? selectedFile : null;
  const pendingDocumentType =
    pendingDocument?.name.split(".").pop()?.toLowerCase() ?? pendingDocument?.type ?? "-";
  const visibleUploadProgress = resolveVisibleUploadProgress(loadStage, uploadProgress);
  const canSubmit =
    !loading &&
    Boolean(selectedFile || uploadedMetadata) &&
    (taskType !== "ask" || Boolean(input.trim()));

  useEffect(() => {
    writeStorage(RECENT_DOCUMENTS_KEY, recentDocuments);
  }, [recentDocuments]);

  useEffect(() => {
    writeStorage(RECENT_RESULTS_KEY, recentResults);
  }, [recentResults]);

  useEffect(() => {
    let active = true;

    async function loadSummary() {
      try {
        const summary = await fetchLogSummary();
        if (active) {
          setLogSummary(summary);
        }
      } catch {
        if (active) {
          setLogSummary(null);
        }
      }
    }

    void loadSummary();
    return () => {
      active = false;
    };
  }, [summaryRefreshTick]);

  function upsertRecentDocument(metadata: UploadMetadata) {
    const nextDocument: RecentDocument = {
      file_id: metadata.file_id,
      original_name: metadata.original_name,
      document_fingerprint: metadata.document_fingerprint,
      file_type: metadata.file_type,
      text_chars: metadata.text_chars,
      page_count: metadata.page_count,
      chunk_count: metadata.chunk_count,
      parse_status: metadata.parse_status,
      saved_at: new Date().toISOString()
    };

    setRecentDocuments((current) => {
      const next = [
        nextDocument,
        ...current.filter((item) => !isSameRecentDocument(item, nextDocument))
      ];
      return next.slice(0, MAX_RECENT_DOCUMENTS);
    });
  }

  function pushRecentResult(
    taskResult: TaskResult,
    promptText: string,
    documentSnapshot: UploadMetadata | null
  ) {
    const item: RecentResult = {
      id: taskResult.request_id,
      task_type: taskResult.task_type,
      input: promptText,
      created_at: new Date().toISOString(),
      document_snapshot: documentSnapshot,
      task_result: taskResult
    };

    setRecentResults((current) => [item, ...current].slice(0, MAX_RECENT_RESULTS));
  }

  function findRecentDocument(fileId: string): UploadMetadata | null {
    const matched = recentDocuments.find((item) => item.file_id === fileId);
    if (!matched) {
      return null;
    }
    return {
      file_id: matched.file_id,
      original_name: matched.original_name,
      file_type: matched.file_type,
      size_bytes: 0,
      text_chars: matched.text_chars,
      page_count: matched.page_count,
      chunk_count: matched.chunk_count,
      document_fingerprint: matched.document_fingerprint ?? null,
      parse_status: matched.parse_status
    };
  }

  function loadDemoDocument() {
    const file = new File([DEMO_DOCUMENT_CONTENT], DEMO_DOCUMENT_NAME, {
      type: "text/markdown"
    });
    setSelectedFile(file);
    setPendingDocumentSource("demo");
    setUploadedMetadata(null);
    setResult(null);
    setError(null);
  }

  function applyDemoAction(task: TaskType, value: string) {
    setTaskType(task);
    setInput(value);
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setLoadStage("idle");
    setUploadProgress(0);
    setError(null);

    try {
      let fileId = uploadedMetadata?.file_id ?? "";
      let activeMetadata = uploadedMetadata;

      if (selectedFile) {
        setLoadStage("uploading");
        const upload = await uploadDocument(selectedFile, setUploadProgress);
        setUploadProgress(100);
        setUploadedMetadata(upload.metadata);
        activeMetadata = upload.metadata;
        setPendingDocumentSource(null);
        upsertRecentDocument(upload.metadata);
        fileId = upload.metadata.file_id;
        setSelectedFile(null);
        if (fileInputRef.current) {
          fileInputRef.current.value = "";
        }
      }

      if (!fileId) {
        throw new Error("请先上传一个文档。");
      }

      if (taskType === "ask" && !input.trim()) {
        throw new Error("问答任务必须输入问题。");
      }

      setLoadStage("model");
      const taskResult = await runTask(taskType, fileId, input.trim(), responseDetailLevel);
      setResult(taskResult);
      pushRecentResult(taskResult, input.trim(), activeMetadata ?? null);
      setSummaryRefreshTick((value) => value + 1);
    } catch (submitError) {
      setError(normalizeErrorMessage(submitError));
      setResult(null);
    } finally {
      setLoading(false);
      setLoadStage("idle");
      setUploadProgress(0);
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
              <span className="flow-separator">·</span>
              <span className="flow-step">解析</span>
              <span className="flow-separator">·</span>
              <span className="flow-step">检索</span>
              <span className="flow-separator">·</span>
              <span className="flow-step">生成</span>
            </div>
            <p className="subtitle">
              上传文档，完成摘要、问答和提纲生成，并通过来源片段、引用依据、统计与日志把结果变成可解释的工作流。
            </p>
          </div>
          <div className="hero-pills">
            <span className="hero-pill">页级结构</span>
            <span className="hero-pill">轻量检索</span>
            <span className="hero-pill">证据返回</span>
            <span className="hero-pill">样例复跑</span>
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
            <p className="subtitle compact">
              先填充一份示例文档，再切换摘要、问答和提纲任务，快速演示完整链路。
            </p>
            <div className="demo-actions">
              <button className="hero-button" type="button" disabled={loading} onClick={loadDemoDocument}>
                填充示例文档
              </button>
              {DEMO_ACTIONS.map((action) => (
                <button
                  key={action.label}
                  className="demo-card"
                  type="button"
                  disabled={loading}
                  onClick={() => applyDemoAction(action.taskType, action.input)}
                >
                  <strong>{action.label}</strong>
                  <span>{action.description}</span>
                </button>
              ))}
            </div>
            {pendingDocument ? (
              <p className="demo-feedback">
                {pendingDocumentSource === "demo" ? "已填充示例文档" : "已选择本地文件"}：{pendingDocument.name}
                。点击“提交任务”后会自动上传。
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
                    setPendingDocumentSource(file ? "local" : null);
                    if (file) {
                      setUploadedMetadata(null);
                      setResult(null);
                      setError(null);
                    }
                  }}
                />
              </label>
              {loading && (loadStage === "uploading" || loadStage === "model" || uploadProgress > 0) ? (
                <div className="upload-progress">
                  <div className="upload-progress-meta">
                    <span>{describeUploadProgress(loadStage, uploadProgress)}</span>
                    <strong>{visibleUploadProgress}%</strong>
                  </div>
                  <div className="upload-progress-track" aria-hidden="true">
                    <div
                      className="upload-progress-fill"
                      style={{ width: `${visibleUploadProgress}%` }}
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
                      {option.label} · {option.description}
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
                    <strong>本地已选中文件</strong>
                  </div>
                  <div className="meta-chip">
                    <span>类型</span>
                    <strong>{pendingDocumentType}</strong>
                  </div>
                  <div className="meta-chip">
                    <span>来源</span>
                    <strong>{pendingDocumentSource === "demo" ? "示例文档" : "本地文件"}</strong>
                  </div>
                  <div className="meta-chip">
                    <span>下一步</span>
                    <strong>点击提交后开始上传</strong>
                  </div>
                </div>
              ) : (
                <p className="empty">上传后这里会显示文档规模与结构信息。</p>
              )}
              {uploadedMetadata || pendingDocument ? (
                <div className="inline-actions">
                  <button
                    className="ghost-button"
                    type="button"
                    disabled={loading}
                    onClick={() => {
                      setUploadedMetadata(null);
                      setSelectedFile(null);
                      setPendingDocumentSource(null);
                      if (fileInputRef.current) {
                        fileInputRef.current.value = "";
                      }
                      setResult(null);
                    }}
                  >
                    清空当前文档
                  </button>
                </div>
              ) : null}
            </div>
          </article>

          <article className="panel result-panel">
            <div className="section-head">
              <h2 className="panel-title">{TASK_LABELS[activeResultTaskType]}结果</h2>
            </div>
            {error ? <p className="error">{error}</p> : null}
            {!error && loading ? <p className="status">{describeLoadStage(loadStage)}</p> : null}
            {!error && !loading && !result ? (
              <p className="empty">提交任务后，这里会展示完整结果、来源信息和路由详情。</p>
            ) : null}
            {!error && result ? (
              <div className="result">
                <div className="result-badges">
                  <span className="badge badge-task">{TASK_LABELS[result.task_type]}</span>
                  <span className="badge badge-route">{result.route_tier ?? "default"}</span>
                  <span className="badge badge-outcome">{result.outcome}</span>
                  {result.response_detail_level ? (
                    <span className="badge badge-detail">
                      {RESPONSE_DETAIL_LABELS[result.response_detail_level] ?? result.response_detail_level}
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
                {result.cache_hit ? (
                  <p className="cache-hit">本次结果命中本地缓存，未重复调用云端模型。</p>
                ) : null}
                {result.retrieval_applied ? (
                  <p className="status">
                    已从 {result.retrieved_chunk_count} 个片段构造问答上下文
                    {result.retrieved_pages.length > 0 ? `，涉及页码：${result.retrieved_pages.join(", ")}` : ""}
                    。
                  </p>
                ) : null}
                {!result.retrieval_applied && result.retrieval_status === "no_match" ? (
                  <p className="warning">
                    {result.retrieval_message ?? "当前问题与文档内容相关性不足，系统已避免无依据回答。"}
                  </p>
                ) : null}
                {result.task_type === "ask" &&
                (result.citations.length > 0 ||
                  result.evidence_quotes.length > 0 ||
                  result.evidence_mode === "candidate") ? (
                  <div className="citations">
                    <h3>引用依据</h3>
                    {result.evidence_mode === "declared" && result.used_chunk_ids.length > 0 ? (
                      <p className="citation-helper">
                        模型声明使用了 {result.used_chunk_ids.length} 个证据块。
                      </p>
                    ) : result.evidence_mode === "candidate" ? (
                      <p className="citation-helper">
                        本轮只命中了候选上下文，模型未明确声明实际使用的证据块。
                      </p>
                    ) : null}
                    <div className="citation-list">
                      {result.citations.map((citation) => (
                        <article key={citation.chunk_id} className="citation-card">
                          <p className="citation-meta">页码：{citation.page_numbers.join(", ")}</p>
                          <p>{citation.snippet}</p>
                        </article>
                      ))}
                    </div>
                    {result.evidence_quotes.length > 0 ? (
                      <div className="evidence-quotes">
                        <h3>证据摘录</h3>
                        <div className="citation-list">
                          {result.evidence_quotes.map((quote, index) => (
                            <article key={`${result.request_id}-${quote.chunk_id}-${index}`} className="citation-card">
                              <p className="citation-meta">证据块：{quote.chunk_id}</p>
                              <p>{quote.quote}</p>
                            </article>
                          ))}
                        </div>
                      </div>
                    ) : null}
                  </div>
                ) : null}
                {result.task_type !== "ask" && result.source_chunks.length > 0 ? (
                  <div className="citations">
                    <h3>来源片段</h3>
                    <div className="citation-list">
                      {result.source_chunks.map((chunk) => (
                        <article key={chunk.chunk_id} className="citation-card">
                          <p className="citation-meta">页码：{chunk.page_numbers.join(", ")}</p>
                          <p>{chunk.snippet}</p>
                        </article>
                      ))}
                    </div>
                  </div>
                ) : null}
                {result.context_truncated ? (
                  <p className="warning">
                    {result.truncation_message ??
                      `文档内容过长，后端本次仅发送前 ${result.used_document_chars} / ${result.source_document_chars} 字符。`}
                  </p>
                ) : null}
                {result.token_usage?.total_tokens ? (
                  <p className="status token-usage">
                    Token 用量：输入 {result.token_usage.prompt_tokens ?? 0} · 输出{" "}
                    {result.token_usage.completion_tokens ?? 0} · 总计 {result.token_usage.total_tokens}
                  </p>
                ) : null}
                <pre>{result.result}</pre>
              </div>
            ) : null}
          </article>
        </section>

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
                    onClick={() => {
                      setUploadedMetadata({
                        file_id: item.file_id,
                        original_name: item.original_name,
                        file_type: item.file_type,
                        size_bytes: 0,
                        text_chars: item.text_chars,
                        page_count: item.page_count,
                        chunk_count: item.chunk_count,
                        document_fingerprint: item.document_fingerprint ?? null,
                        parse_status: item.parse_status
                      });
                      setSelectedFile(null);
                      setPendingDocumentSource(null);
                      setResult(null);
                      setError(null);
                    }}
                  >
                    <strong>{item.original_name}</strong>
                    <span>
                      {item.file_type} · {item.page_count} pages · {item.chunk_count} chunks
                    </span>
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
                    onClick={() => {
                      const restoredMetadata =
                        item.document_snapshot ?? findRecentDocument(item.task_result.file_id);
                      setTaskType(item.task_type);
                      if (item.task_result.response_detail_level) {
                        setResponseDetailLevel(item.task_result.response_detail_level);
                      }
                      setInput(item.input);
                      setUploadedMetadata(restoredMetadata);
                      setSelectedFile(null);
                      setPendingDocumentSource(null);
                      setResult(item.task_result);
                      setError(null);
                    }}
                  >
                    <strong>{item.task_type.toUpperCase()}</strong>
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

export default App;
