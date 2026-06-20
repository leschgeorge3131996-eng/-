import { useEffect, useRef, useState, type FormEvent } from "react";
import {
  ApiRequestError,
  clearStoredSession,
  deleteDocument,
  ensureDemoSession,
  fetchCurrentSession,
  fetchDocumentMetadata,
  fetchLogSummary,
  readStoredSession,
  runTask,
  uploadDocument
} from "./api";
import PdfPreviewPanel from "./components/PdfPreviewPanel";
import ResultPanel from "./components/ResultPanel";
import type {
  AuthSession,
  BBoxRegion,
  Citation,
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
  description: string;
  placeholder: string;
}> = [
  {
    value: "ask",
    label: "问答",
    description: "针对内容提问，回答带证据回链",
    placeholder: "例如：这篇文档的核心方法是什么？"
  },
  {
    value: "summary",
    label: "摘要",
    description: "自动归纳背景、方法与结论",
    placeholder: "例如：请突出研究背景、方法和创新点。"
  },
  {
    value: "outline",
    label: "提纲",
    description: "生成汇报或答辩结构",
    placeholder: "例如：请生成 6 页答辩提纲。"
  }
];

const DETAIL_OPTIONS: Array<{
  value: ResponseDetailLevel;
  label: string;
  description: string;
}> = [
  { value: "concise", label: "简洁", description: "只保留核心结论" },
  { value: "balanced", label: "适中", description: "兼顾完整与可读性" },
  { value: "detailed", label: "详细", description: "补充更多背景与展开" }
];

const RESEARCH_DIGEST_PROMPT = `请生成一份论文速读，必须包含：
1. 研究问题
2. 核心方法
3. 主要贡献
4. 实验结果
5. 局限与不足
6. 建议追问的 5 个问题

要求：
- 每一部分尽量标注对应页码、章节或来源线索。
- 优先提炼对答辩、复现实验和继续追问最有价值的信息。
- 输出为清晰的 Markdown。`;

const TASK_LABELS: Record<TaskType, string> = {
  summary: "摘要",
  ask: "问答",
  outline: "提纲生成"
};

const RECENT_DOCUMENTS_KEY = "yandatong_recent_documents";
const RECENT_RESULTS_KEY = "yandatong_recent_results";

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
  if (error instanceof ApiRequestError && error.code === "UNAUTHORIZED") {
    return "当前试用会话已失效，请刷新页面重新进入。";
  }
  if (error instanceof ApiRequestError && error.code === "TASK_TIMEOUT") {
    return "模型响应较慢，已自动停止等待，请稍后重试当前任务。";
  }
  if (error instanceof ApiRequestError) return error.message;
  if (error instanceof Error) return error.message;
  return "提交任务失败";
}

function normalizeAuthErrorMessage(error: unknown): string {
  if (error instanceof ApiRequestError && error.code === "UNAUTHORIZED") {
    return error.message || "试用会话已失效，请重新进入。";
  }
  if (error instanceof ApiRequestError) return error.message;
  if (error instanceof Error) return error.message;
  return "试用会话初始化失败，请稍后重试。";
}

function normalizeRecordErrorMessage(error: unknown): string {
  if (error instanceof ApiRequestError) {
    if (error.code === "NOT_FOUND") {
      return "对应文档已不存在，记录已从最近列表移除。";
    }
    if (error.code === "FORBIDDEN") {
      return "当前文档访问凭证已失效，无法恢复该记录。";
    }
    if (error.code === "UNAUTHORIZED") {
      return "当前试用会话已失效，请刷新页面后再恢复记录。";
    }
    if (error.code === "NON_JSON_RESPONSE") {
      return "服务返回了异常页面，最近记录恢复失败，请刷新页面或重启本地服务。";
    }
    return error.message;
  }
  if (error instanceof Error) {
    return error.message;
  }
  return "最近记录恢复失败。";
}

function shouldRemoveMissingRecord(error: unknown): boolean {
  return error instanceof ApiRequestError && error.code === "NOT_FOUND";
}

function shouldRemoveInaccessibleRecord(error: unknown): boolean {
  return (
    error instanceof ApiRequestError &&
    (error.code === "NOT_FOUND" || error.code === "FORBIDDEN")
  );
}

function isSessionError(error: unknown): boolean {
  return error instanceof ApiRequestError && error.code === "UNAUTHORIZED";
}

type PreviewReference = {
  page: number;
  pages: number[];
  snippet: string | null;
  snippetPage: number | null;
};

function resolveAccessToken(
  fileId: string,
  ...candidates: Array<string | null | undefined>
): string | null {
  for (const candidate of candidates) {
    if (candidate) {
      return candidate;
    }
  }

  const recentDocuments = readStorage<RecentDocument[]>(RECENT_DOCUMENTS_KEY, []);
  return recentDocuments.find((item) => item.file_id === fileId)?.access_token ?? null;
}

function normalizePreviewPages(pages: number[], fallbackPage = 1): number[] {
  const normalized = Array.from(
    new Set(pages.filter((page) => Number.isInteger(page) && page > 0))
  );
  return normalized.length > 0 ? normalized : [fallbackPage];
}

function findEvidenceQuoteForChunk(
  taskResult: TaskResult,
  chunkId: string | null | undefined
): string | null {
  if (!chunkId) {
    return null;
  }
  return taskResult.evidence_quotes.find((item) => item.chunk_id === chunkId)?.quote ?? null;
}

function resolveAskPreviewSnippet(
  taskResult: TaskResult,
  citation: Pick<Citation, "chunk_id" | "snippet"> | null
): string | null {
  const matchedQuote = findEvidenceQuoteForChunk(taskResult, citation?.chunk_id);
  if (taskResult.evidence_mode === "declared" && matchedQuote) {
    return matchedQuote;
  }
  return citation?.snippet ?? matchedQuote ?? taskResult.evidence_quotes[0]?.quote ?? null;
}

function scrollElementIntoView(selector: string): void {
  if (typeof window === "undefined" || typeof document === "undefined") {
    return;
  }

  window.requestAnimationFrame(() => {
    window.requestAnimationFrame(() => {
      const element = document.querySelector<HTMLElement>(selector);
      if (!element || typeof element.scrollIntoView !== "function") {
        return;
      }
      element.scrollIntoView({ behavior: "smooth", block: "start" });
    });
  });
}

function scrollPreviewIntoView(): void {
  scrollElementIntoView('[data-testid="pdf-preview-panel"]');
}

function buildPreviewReference(taskResult: TaskResult): PreviewReference {
  if (taskResult.task_type === "ask") {
    const primaryReference =
      (taskResult.evidence_mode === "declared"
        ? taskResult.citations?.[0]
        : taskResult.candidate_chunks?.[0]) ?? null;
    const retrievedPages = taskResult.retrieved_pages ?? [];
    const page = primaryReference?.page_numbers[0] ?? retrievedPages[0] ?? 1;
    const pages = normalizePreviewPages(
      primaryReference?.page_numbers ?? retrievedPages,
      page
    );
    const snippet = resolveAskPreviewSnippet(taskResult, primaryReference);
    return {
      page,
      pages,
      snippet,
      snippetPage: snippet ? page : null
    };
  }

  const primaryReference = taskResult.source_chunks?.[0] ?? null;
  const page = primaryReference?.page_numbers[0] ?? 1;
  const pages = normalizePreviewPages(primaryReference?.page_numbers ?? [page], page);
  const snippet = primaryReference?.snippet ?? null;
  return {
    page,
    pages,
    snippet,
    snippetPage: snippet ? page : null
  };
}

function upsertRecentDocument(
  current: RecentDocument[],
  metadata: UploadMetadata
): RecentDocument[] {
  const dedupeKey = metadata.document_fingerprint || metadata.file_id;
  return [
    {
      file_id: metadata.file_id,
      original_name: metadata.original_name,
      access_token: metadata.access_token,
      document_fingerprint: metadata.document_fingerprint,
      file_type: metadata.file_type,
      text_chars: metadata.text_chars,
      page_count: metadata.page_count,
      chunk_count: metadata.chunk_count,
      expires_at: metadata.expires_at,
      parse_status: metadata.parse_status,
      saved_at: new Date().toISOString()
    },
    ...current.filter(
      (item) => (item.document_fingerprint || item.file_id) !== dedupeKey
    )
  ].slice(0, 5);
}

export default function App() {
  const [session, setSession] = useState<AuthSession | null>(() => readStoredSession());
  const [authLoading, setAuthLoading] = useState(true);
  const [authPending, setAuthPending] = useState(false);
  const [authError, setAuthError] = useState<string | null>(null);
  const [taskType, setTaskType] = useState<TaskType>("ask");
  const [responseDetailLevel, setResponseDetailLevel] =
    useState<ResponseDetailLevel>("balanced");
  const [input, setInput] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadedMetadata, setUploadedMetadata] = useState<UploadMetadata | null>(null);
  const [result, setResult] = useState<RecentResult["task_result"] | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadStage, setLoadStage] = useState<"idle" | "uploading" | "model">("idle");
  const [uploadProgress, setUploadProgress] = useState(0);
  const [error, setError] = useState<string | null>(null);
  const [notice, setNotice] = useState<string | null>(null);
  const [previewOpen, setPreviewOpen] = useState(false);
  const [previewPage, setPreviewPage] = useState(1);
  const [previewPages, setPreviewPages] = useState<number[]>([1]);
  const [previewSnippet, setPreviewSnippet] = useState<string | null>(null);
  const [previewSnippetPage, setPreviewSnippetPage] = useState<number | null>(null);
  const [previewBboxes, setPreviewBboxes] = useState<BBoxRegion[]>([]);
  const [recentDocuments, setRecentDocuments] = useState<RecentDocument[]>(() =>
    readStorage(RECENT_DOCUMENTS_KEY, [])
  );
  const [recentResults, setRecentResults] = useState<RecentResult[]>(() =>
    readStorage(RECENT_RESULTS_KEY, [])
  );
  const [logSummary, setLogSummary] = useState<LogSummary | null>(null);
  const [statsExpanded, setStatsExpanded] = useState(false);
  const [settingsExpanded, setSettingsExpanded] = useState(false);
  const fileInputRef = useRef<HTMLInputElement | null>(null);
  const hadStoredSessionRef = useRef(Boolean(readStoredSession()));
  const taskInFlightRef = useRef(false);
  const [dragOver, setDragOver] = useState(false);

  const isAuthenticated = Boolean(session);
  const currentOption = TASK_OPTIONS.find((item) => item.value === taskType)!;
  const pendingDocument = selectedFile && !uploadedMetadata ? selectedFile : null;
  const pendingDocumentType =
    pendingDocument?.name.split(".").pop()?.toLowerCase() ?? pendingDocument?.type ?? "-";
  const canSubmit =
    isAuthenticated &&
    !loading &&
    Boolean(selectedFile || uploadedMetadata) &&
    (taskType !== "ask" || Boolean(input.trim()));
  const previewMetadata = uploadedMetadata?.file_type === "pdf" ? uploadedMetadata : null;
  const interactionLocked = loading || authPending || authLoading;
  const digestPresetActive =
    taskType === "summary" &&
    responseDetailLevel === "detailed" &&
    input.trim() === RESEARCH_DIGEST_PROMPT.trim();

  useEffect(() => {
    writeStorage(RECENT_DOCUMENTS_KEY, recentDocuments);
  }, [recentDocuments]);

  useEffect(() => {
    writeStorage(RECENT_RESULTS_KEY, recentResults);
  }, [recentResults]);

  useEffect(() => {
    if (!isAuthenticated) {
      setLogSummary(null);
      return;
    }
    void fetchLogSummary().then(setLogSummary).catch(() => setLogSummary(null));
  }, [isAuthenticated, result]);

  useEffect(() => {
    setAuthLoading(true);
    let cancelled = false;

    async function tryEnsureDemoSession(retriesLeft: number): Promise<AuthSession | null> {
      try {
        return await ensureDemoSession();
      } catch {
        if (retriesLeft <= 0 || cancelled) return null;
        await new Promise((resolve) => setTimeout(resolve, 800));
        if (cancelled) return null;
        return tryEnsureDemoSession(retriesLeft - 1);
      }
    }

    void (async () => {
      if (cancelled) return;

      try {
        const currentSession = await fetchCurrentSession();
        if (cancelled) return;
        hadStoredSessionRef.current = true;
        setSession(currentSession);
        setAuthError(null);
        return;
      } catch (sessionError) {
        if (cancelled) return;

        const demoSession = await tryEnsureDemoSession(2);
        if (cancelled) return;
        if (demoSession) {
          hadStoredSessionRef.current = true;
          setSession(demoSession);
          setAuthError(null);
          return;
        }

        clearStoredSession();
        setSession(null);
        setRecentDocuments([]);
        setRecentResults([]);
        setUploadedMetadata(null);
        setSelectedFile(null);
        setResult(null);
        setError(null);
        setNotice(null);
        setPreviewOpen(false);
        setPreviewPage(1);
        setPreviewPages([1]);
        setPreviewSnippet(null);
        setPreviewSnippetPage(null);
        setPreviewBboxes([]);
        setAuthError(
          hadStoredSessionRef.current ? normalizeAuthErrorMessage(sessionError) : null
        );
      }
    })().finally(() => {
      if (!cancelled) setAuthLoading(false);
    });
    return () => {
      cancelled = true;
    };
  }, []);

  function applyActiveDocument(metadata: UploadMetadata | null, preview?: PreviewReference) {
    const nextPage = preview?.page ?? 1;
    const nextPages = preview?.pages ?? [nextPage];
    setUploadedMetadata(metadata);
    setSelectedFile(null);
    setPreviewPage(nextPage);
    setPreviewPages(nextPages.length > 0 ? nextPages : [nextPage]);
    setPreviewOpen(Boolean(metadata && metadata.file_type === "pdf"));
    if (!metadata || metadata.file_type !== "pdf") {
      setPreviewSnippet(null);
      setPreviewSnippetPage(null);
      setPreviewBboxes([]);
    } else {
      setPreviewSnippet(preview?.snippet ?? null);
      setPreviewSnippetPage(preview?.snippetPage ?? null);
      setPreviewBboxes([]);
    }
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  }

  function clearCurrentDocument() {
    setUploadedMetadata(null);
    setSelectedFile(null);
    setResult(null);
    setError(null);
    setNotice(null);
    setPreviewOpen(false);
    setPreviewPage(1);
    setPreviewPages([1]);
    setPreviewSnippet(null);
    setPreviewSnippetPage(null);
    setPreviewBboxes([]);
    if (fileInputRef.current) {
      fileInputRef.current.value = "";
    }
  }

  function removeDocumentRecords(fileId: string) {
    setRecentDocuments((current) => current.filter((item) => item.file_id !== fileId));
    setRecentResults((current) => current.filter((item) => item.task_result.file_id !== fileId));
  }

  function clearSessionWorkspace() {
    clearStoredSession();
    setSession(null);
    setRecentDocuments([]);
    setRecentResults([]);
    clearCurrentDocument();
  }

  function handleSessionExpired(error: unknown): boolean {
    if (!isSessionError(error)) {
      return false;
    }
    clearSessionWorkspace();
    setAuthError(normalizeAuthErrorMessage(error));
    return true;
  }

  function handleRetryDemoSession() {
    setAuthPending(true);
    setAuthError(null);
    void ensureDemoSession()
      .then((demoSession) => {
        hadStoredSessionRef.current = true;
        setSession(demoSession);
      })
      .catch((retryError) => {
        setAuthError(normalizeAuthErrorMessage(retryError));
      })
      .finally(() => {
        setAuthPending(false);
      });
  }

  function restoreRecentDocument(document: RecentDocument) {
    void (async () => {
      setNotice(null);
      try {
        const metadata = (
          await fetchDocumentMetadata(document.file_id, document.access_token)
        ).metadata;
        applyActiveDocument(metadata);
        setResult(null);
        setError(null);
      } catch (restoreError) {
        if (handleSessionExpired(restoreError)) {
          return;
        }
        if (shouldRemoveInaccessibleRecord(restoreError)) {
          removeDocumentRecords(document.file_id);
        }
        setError(normalizeRecordErrorMessage(restoreError));
      }
    })();
  }

  function restoreRecentResult(item: RecentResult) {
    void (async () => {
      setNotice(null);
      try {
        const accessToken = resolveAccessToken(
          item.task_result.file_id,
          item.document_snapshot?.access_token
        );
        const metadata = (
          await fetchDocumentMetadata(item.task_result.file_id, accessToken)
        ).metadata;
        const preview = buildPreviewReference(item.task_result);

        setTaskType(item.task_type);
        if (item.task_result.response_detail_level) {
          setResponseDetailLevel(item.task_result.response_detail_level);
        }
        setInput(item.input);
        setResult(item.task_result);
        setError(null);
        applyActiveDocument(metadata, preview);
      } catch (restoreError) {
        if (handleSessionExpired(restoreError)) {
          return;
        }
        if (shouldRemoveInaccessibleRecord(restoreError)) {
          setRecentResults((current) => current.filter((entry) => entry.id !== item.id));
          removeDocumentRecords(item.task_result.file_id);
        }
        setError(normalizeRecordErrorMessage(restoreError));
      }
    })();
  }

  function handleDeleteCurrentDocument() {
    if (!uploadedMetadata?.file_id) {
      setNotice(null);
      setError("当前没有可删除的文档。");
      return;
    }

    if (!window.confirm(`确认删除文档“${uploadedMetadata.original_name}”吗？此操作不可撤销。`)) {
      return;
    }

    setLoading(true);
    setError(null);
    setNotice(null);
    void deleteDocument(uploadedMetadata.file_id, uploadedMetadata.access_token)
      .then(() => {
        const deletedName = uploadedMetadata.original_name;
        removeDocumentRecords(uploadedMetadata.file_id);
        clearCurrentDocument();
        setNotice(`文档“${deletedName}”已删除，最近记录已同步清理。`);
      })
      .catch((deleteError) => {
        if (handleSessionExpired(deleteError)) {
          return;
        }
        if (shouldRemoveInaccessibleRecord(deleteError)) {
          removeDocumentRecords(uploadedMetadata.file_id);
          clearCurrentDocument();
        }
        setError(normalizeErrorMessage(deleteError));
      })
      .finally(() => {
        setLoading(false);
      });
  }

  function applyResearchDigestPreset() {
    setTaskType("summary");
    setResponseDetailLevel("detailed");
    setInput(RESEARCH_DIGEST_PROMPT);
    setNotice("已切换到论文速读：上传论文后可直接生成结构化速读结果。");
    setError(null);
  }

  function applyFollowUpQuestion(question: string) {
    setTaskType("ask");
    setResponseDetailLevel("balanced");
    setInput(question);
    setNotice("已填入速读追问：点击提交任务后会进入问答与证据回链。");
    setError(null);
    scrollElementIntoView('[data-testid="task-input"]');
  }

  async function submitCurrentTask() {
    if (taskInFlightRef.current) {
      return;
    }
    taskInFlightRef.current = true;
    setLoading(true);
    setLoadStage("idle");
    setError(null);
    setNotice(null);
    let uploadedSelectedFile = false;

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
        uploadedSelectedFile = true;
        setRecentDocuments((current) => upsertRecentDocument(current, nextMetadata));
      }

      if (!fileId) {
        throw new Error("请先上传一个文档。");
      }

      setLoadStage("model");
      const taskResult = await runTask(
        taskType,
        fileId,
        input.trim(),
        responseDetailLevel,
        metadata?.access_token
      );
      setResult(taskResult);
      if (metadata?.file_type === "pdf") {
        applyActiveDocument(metadata, buildPreviewReference(taskResult));
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
      if (handleSessionExpired(submitError)) {
        return;
      }
      setError(normalizeErrorMessage(submitError));
      setResult(null);
    } finally {
      taskInFlightRef.current = false;
      setLoading(false);
      setLoadStage("idle");
      setUploadProgress(0);
      if (fileInputRef.current && (uploadedSelectedFile || !selectedFile)) {
        fileInputRef.current.value = "";
      }
    }
  }

  async function handleSubmit(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    await submitCurrentTask();
  }

  return (
    <div className="page">
      <main className="container">
        <section className="hero">
          <div className="hero-copy">
            <p className="eyebrow">引用可核验 · 论文/答辩文档助手</p>
            <h1 className="brandmark">研答通</h1>
            <div className="hero-flow" aria-label="文档任务流程" data-stage={loadStage} data-completed={result ? "true" : "false"}>
              <span className="flow-step" data-step="1">上传</span>
              <span className="flow-separator" aria-hidden="true" />
              <span className="flow-step" data-step="2">解析</span>
              <span className="flow-separator" aria-hidden="true" />
              <span className="flow-step" data-step="3">检索</span>
              <span className="flow-separator" aria-hidden="true" />
              <span className="flow-step" data-step="4">生成</span>
            </div>
            <p className="subtitle">
              面向论文与报告阅读、答辩准备的文档助手，每一条回答都能跳回 PDF 原文证据。
            </p>
          </div>
          <aside
            className={`hero-status${logSummary?.error_count ? " has-errors" : ""}${statsExpanded ? " expanded" : ""}`}
            data-testid="hero-status"
          >
            <div className="hero-status-head">
              <span className="stats-dot" aria-hidden="true" />
              <strong>运行状态</strong>
            </div>
            <p>
              {logSummary
                ? logSummary.error_count > 0
                  ? `运行中 · 有效 ${logSummary.answered_count} / 总计 ${logSummary.total_requests}`
                  : `系统正常 · 已完成 ${logSummary.total_requests} 次任务`
                : authLoading
                  ? "正在准备试用环境"
                  : "等待首次任务"}
            </p>
            {logSummary ? (
              <button
                className="ghost-button stats-toggle"
                data-testid="stats-toggle"
                type="button"
                aria-expanded={statsExpanded}
                onClick={() => setStatsExpanded((prev) => !prev)}
              >
                {statsExpanded ? "收起详情" : "查看详情"}
              </button>
            ) : null}
            {logSummary && statsExpanded ? (
              <div className="stats-grid hero-stats-grid" data-testid="stats-grid">
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
            ) : null}
          </aside>
        </section>

        <section className="workspace primary-workspace">
          <article className="panel control-panel">
            <div className="section-head">
              <h2 className="panel-title">上传文献并提问</h2>
              {session ? (
                <span className="session-chip" data-testid="session-chip">
                  免登录试用
                </span>
              ) : null}
            </div>
            {!isAuthenticated ? (
                <div className="auth-panel-card">
                  {authLoading ? (
                    <p className="status status-card">正在准备试用环境...</p>
                  ) : (
                    <>
                      <p className="error status-card" data-testid="auth-error">
                        {authError ?? "试用会话暂时无法创建，请稍后重试。"}
                      </p>
                      <div className="control-actions">
                        <button
                          className="submit"
                          type="button"
                          disabled={authPending}
                          onClick={handleRetryDemoSession}
                        >
                          {authPending ? "正在重试..." : "重新进入试用"}
                        </button>
                      </div>
                    </>
                  )}
                </div>
            ) : (
              <>
                <form className="form" onSubmit={handleSubmit}>
              <div className="field upload-field">
                <span>1. 上传文献</span>
                <div
                  className={`drop-zone${dragOver ? " drop-zone-active" : ""}${loading ? " drop-zone-disabled" : ""}`}
                  onDragOver={(e) => { e.preventDefault(); if (!loading) setDragOver(true); }}
                  onDragLeave={() => setDragOver(false)}
                  onDrop={(e) => {
                    e.preventDefault();
                    setDragOver(false);
                    if (loading) return;
                    const file = e.dataTransfer.files?.[0] ?? null;
                    if (!file) return;
                    setSelectedFile(file);
                    setUploadedMetadata(null);
                    setResult(null);
                    setError(null);
                    setNotice(null);
                    setPreviewOpen(false);
                    setPreviewPage(1);
                    setPreviewPages([1]);
                    setPreviewSnippet(null);
                    setPreviewSnippetPage(null);
                    setPreviewBboxes([]);
                  }}
                  onClick={() => !loading && fileInputRef.current?.click()}
                >
                  <span className="drop-zone-label">
                    {selectedFile
                      ? selectedFile.name
                      : "拖拽文件到此处，或点击选择"}
                  </span>
                  <span className="drop-zone-hint">支持 PDF、TXT、Markdown</span>
                </div>
                <p className="drop-zone-footnote">
                  上传的文档仅绑定当前会话，会话过期会自动清理；请勿使用敏感资料。
                </p>
                <input
                  data-testid="file-input"
                  ref={fileInputRef}
                  type="file"
                  accept=".txt,.md,.pdf,text/plain,text/markdown,application/pdf"
                  disabled={loading}
                  style={{ display: "none" }}
                  onChange={(event) => {
                    const file = event.target.files?.[0] ?? null;
                    setSelectedFile(file);
                    if (file) {
                      setUploadedMetadata(null);
                      setResult(null);
                      setError(null);
                      setNotice(null);
                      setPreviewOpen(false);
                      setPreviewPage(1);
                      setPreviewPages([1]);
                      setPreviewSnippet(null);
                      setPreviewSnippetPage(null);
                      setPreviewBboxes([]);
                    }
                  }}
                />
              </div>
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

              <div className={`field question-field${settingsExpanded ? " settings-open" : ""}`}>
                <div className="question-field-head">
                  <span>2. 输入你的问题</span>
                  <div className="question-tools">
                    <button
                      className="ghost-button settings-toggle-button"
                      data-testid="settings-toggle-button"
                      type="button"
                      aria-expanded={settingsExpanded}
                      onClick={() => setSettingsExpanded((current) => !current)}
                    >
                      {settingsExpanded ? "收起设置" : "处理设置"}
                    </button>
                    <button
                      className="ghost-button clear-question-button"
                      data-testid="clear-question-button"
                      type="button"
                      disabled={loading || !input}
                      onClick={() => setInput("")}
                    >
                      清空问题
                    </button>
                  </div>
                </div>
                <div className="question-input-row">
                  <textarea
                    data-testid="task-input"
                    rows={7}
                    value={input}
                    placeholder={currentOption.placeholder}
                    disabled={loading}
                    onChange={(event) => setInput(event.target.value)}
                  />
                    <aside
                      className="question-settings"
                      data-testid="question-settings"
                      hidden={!settingsExpanded}
                    >
                      <div className="field compact-setting-field">
                        <span>处理方式</span>
                        <div className="control-option-grid compact-options">
                          {TASK_OPTIONS.map((option) => (
                            <button
                              key={option.value}
                              data-testid={`task-option-${option.value}`}
                              aria-pressed={taskType === option.value}
                              className={`option-card${taskType === option.value ? " active" : ""}`}
                              type="button"
                              disabled={loading}
                              onClick={() => setTaskType(option.value)}
                            >
                              <strong>{option.label}</strong>
                              <small>{option.description}</small>
                            </button>
                          ))}
                        </div>
                      </div>
                      <div className="field compact-setting-field">
                        <span>回答长度</span>
                        <div className="control-detail-grid compact-details">
                          {DETAIL_OPTIONS.map((option) => (
                            <button
                              key={option.value}
                              data-testid={`detail-option-${option.value}`}
                              aria-pressed={responseDetailLevel === option.value}
                              className={`detail-card${responseDetailLevel === option.value ? " active" : ""}`}
                              type="button"
                              disabled={loading}
                              onClick={() => setResponseDetailLevel(option.value)}
                            >
                              <strong>{option.label}</strong>
                              <small>{option.description}</small>
                            </button>
                          ))}
                        </div>
                      </div>
                    </aside>
                </div>
                <div className="control-actions primary-submit-row">
                  <button
                    className="submit"
                    data-testid="submit-task-button"
                    type="submit"
                    disabled={!canSubmit}
                  >
                    {loading ? "处理中..." : "开始处理"}
                  </button>
                  <p className="control-hint">
                    当前：{currentOption.label} / {DETAIL_OPTIONS.find((item) => item.value === responseDetailLevel)?.label}
                  </p>
                </div>
              </div>

              <div className={`digest-workbench${digestPresetActive ? " active" : ""}`}>
                <div>
                  <span className="digest-kicker">一键操作</span>
                  <strong>论文速读</strong>
                  <p>
                    一键生成研究问题、方法、贡献、实验、局限和追问清单，适合答辩前快速吃透论文。
                  </p>
                  <ol className="digest-flow" aria-label="论文速读流程">
                    <li>生成速读</li>
                    <li>点击追问</li>
                    <li>查看证据回链</li>
                  </ol>
                </div>
                <button
                  className="ghost-button digest-button"
                  data-testid="research-digest-preset"
                  type="button"
                  disabled={interactionLocked}
                  onClick={applyResearchDigestPreset}
                >
                  {digestPresetActive ? "已启用" : "生成论文速读"}
                </button>
              </div>

            </form>

            {notice ? (
              <p className="status status-card success-status" data-testid="notice-banner">
                {notice}
              </p>
            ) : null}

            <div className="document-brief">
              <div className="section-head compact-head">
                <p className="section-kicker">当前文档</p>
                <h3 data-testid="current-document-name">
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
                  {uploadedMetadata.expires_at ? (
                    <div className="meta-chip">
                      <span>保留至</span>
                      <strong>{new Date(uploadedMetadata.expires_at).toLocaleString()}</strong>
                    </div>
                  ) : null}
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
                    <strong>本地文件</strong>
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
                      data-testid="open-pdf-preview-button"
                      type="button"
                      disabled={loading}
                      onClick={() => {
                        setPreviewOpen(true);
                        scrollPreviewIntoView();
                      }}
                    >
                      打开 PDF 预览
                    </button>
                  ) : null}
                  {uploadedMetadata ? (
                    <button
                      className="ghost-button danger-button"
                      data-testid="delete-current-document-button"
                      type="button"
                      disabled={loading}
                      onClick={handleDeleteCurrentDocument}
                    >
                      删除当前文档
                    </button>
                  ) : null}
                  <button className="ghost-button" type="button" disabled={loading} onClick={clearCurrentDocument}>
                    清空当前文档
                  </button>
                </div>
              ) : null}
            </div>
              </>
            )}
          </article>

          <ResultPanel
            activeTaskType={taskType}
            error={error}
            loading={loading}
            loadMessage={describeLoadStage(loadStage)}
            result={result}
            documentTotalChars={uploadedMetadata?.text_chars ?? null}
            canOpenPdfPreview={Boolean(previewMetadata)}
            canRetry={canSubmit}
            onOpenPdfPage={(citation) => {
              const nextPages = normalizePreviewPages(citation.page_numbers);
              const nextPrimaryPage = nextPages[0] ?? 1;
              const nextSnippet = result ? resolveAskPreviewSnippet(result, citation) : citation.snippet;
              setPreviewPages(nextPages);
              setPreviewPage(nextPrimaryPage);
              setPreviewSnippet(nextSnippet);
              setPreviewSnippetPage(nextSnippet ? nextPrimaryPage : null);
              setPreviewBboxes(citation.bbox_regions ?? []);
              setPreviewOpen(true);
              scrollPreviewIntoView();
            }}
            onAskFollowUp={applyFollowUpQuestion}
            onRetry={() => void submitCurrentTask()}
          />
        </section>

        {previewMetadata && previewOpen ? (
          <PdfPreviewPanel
            documentName={previewMetadata.original_name}
            fileId={previewMetadata.file_id}
            accessToken={previewMetadata.access_token}
            page={previewPage}
            availablePages={previewPages}
            highlightText={previewPage === previewSnippetPage ? previewSnippet : null}
            bboxRegions={previewBboxes.filter((region) => region.page === previewPage)}
            onSelectPage={(page) => setPreviewPage(page)}
            onClose={() => setPreviewOpen(false)}
          />
        ) : null}

        <section className="grid secondary-grid history-section">
          <article className="panel">
            <div className="section-head compact-head">
              <h2 className="panel-title">最近文档</h2>
            </div>
            {!isAuthenticated ? (
              <p className="empty">试用会话准备好后会显示当前会话下的最近文档。</p>
            ) : recentDocuments.length === 0 ? (
              <p className="empty">最近上传的文档会显示在这里，便于复用。</p>
            ) : (
              <div className="history-list">
                {recentDocuments.map((item) => (
                  <button
                    key={item.file_id}
                    data-testid={`recent-document-${item.file_id}`}
                    className="history-card"
                    type="button"
                    disabled={interactionLocked}
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
            {!isAuthenticated ? (
              <p className="empty">试用会话准备好后会显示当前会话下的最近结果。</p>
            ) : recentResults.length === 0 ? (
              <p className="empty">最近 5 次任务结果会显示在这里，方便回看。</p>
            ) : (
              <div className="history-list">
                {recentResults.map((item) => (
                  <button
                    key={item.id}
                    data-testid={`recent-result-${item.id}`}
                    className="history-card"
                    type="button"
                    disabled={interactionLocked}
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
        <footer className="site-footer" aria-label="备案信息">
          <a href="https://beian.miit.gov.cn/" target="_blank" rel="noreferrer">
            浙ICP备2026043125号
          </a>
          <a
            href="https://beian.mps.gov.cn/#/query/webSearch?code=33038202005010"
            target="_blank"
            rel="noreferrer"
          >
            浙公网安备33038202005010号
          </a>
        </footer>
      </main>
    </div>
  );
}
