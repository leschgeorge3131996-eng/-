import { motion } from "motion/react";
import { useEffect, useRef, useState, type FormEvent } from "react";
import {
  ApiRequestError,
  clearStoredSession,
  deleteDocument,
  ensureDemoSession,
  fetchCurrentSession,
  fetchDemoMode,
  fetchDocumentMetadata,
  fetchLogSummary,
  loginSession,
  logoutSession,
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
    value: "summary",
    label: "摘要",
    description: "自动归纳背景、方法与结论",
    placeholder: "例如：请突出研究背景、方法和创新点。"
  },
  {
    value: "ask",
    label: "问答",
    description: "先检索证据，再回答问题",
    placeholder: "例如：这篇文档的核心方法是什么？"
  },
  {
    value: "outline",
    label: "提纲生成",
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

const HERO_PILLS = ["页级结构", "轻量检索", "证据回链", "样例复跑"];

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

const RESEARCH_DIGEST_PROMPT = `请生成一份论文速读工作台，必须包含：
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

const CONCISE_RESEARCH_DIGEST_PROMPT = `请生成一份精简论文速读，必须包含：
1. 研究问题
2. 核心方法
3. 最关键结论
4. 建议追问的 3 个问题

要求：每部分不超过 2 条要点，尽量标注页码或来源线索，输出 Markdown。`;

const DEMO_WHITELIST_ACTIONS = [
  {
    label: "推荐追问 1",
    description: "验证证据问答",
    input: "这个项目的核心能力是什么？"
  },
  {
    label: "推荐追问 2",
    description: "验证端到端价值",
    input: "系统为什么强调证据回链？"
  },
  {
    label: "拒答边界",
    description: "验证不胡编",
    input: "这篇文档有没有给出 2028 年全国部署预算？"
  }
];

const TASK_LABELS: Record<TaskType, string> = {
  summary: "摘要",
  ask: "问答",
  outline: "提纲生成"
};

const RECENT_DOCUMENTS_KEY = "yandatong_recent_documents";
const RECENT_RESULTS_KEY = "yandatong_recent_results";
const DEMO_DOCUMENT_NAME = "demo_research_brief.md";
const DEMO_DOCUMENT_CONTENT = `# 项目简介

研答通是一个面向论文与报告阅读、答辩准备的文档助手。
核心能力是带证据回链的问答——每一条回答都能跳回 PDF 原文证据。
第一阶段目标是支持用户上传文档，完成摘要、问答和提纲生成。
系统当前采用端云协同路线，优先保证能跑通、能演示、能扩展。`;

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
  if (stage === "model") return "模型处理中，首次请求可能需要 10 到 40 秒；如现场网络较慢，可改用精简速读兜底。";
  return "";
}

function normalizeErrorMessage(error: unknown): string {
  if (error instanceof ApiRequestError && error.code === "UNAUTHORIZED") {
    return "当前试用会话已失效，请重新登录。";
  }
  if (error instanceof ApiRequestError && error.code === "TASK_TIMEOUT") {
    return "模型响应较慢，已自动停止等待。建议先点击“精简速读兜底”快速跑通演示，或稍后重试当前任务。";
  }
  if (error instanceof ApiRequestError) return error.message;
  if (error instanceof Error) return error.message;
  return "提交任务失败";
}

function normalizeAuthErrorMessage(error: unknown): string {
  if (error instanceof ApiRequestError && error.code === "UNAUTHORIZED") {
    return error.message || "邀请码无效或试用会话已失效。";
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
      return "当前试用会话已失效，请重新登录后再恢复记录。";
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
  const [demoMode, setDemoMode] = useState(false);
  const [inviteCode, setInviteCode] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [authError, setAuthError] = useState<string | null>(null);
  const [authNotice, setAuthNotice] = useState<string | null>(null);
  const [taskType, setTaskType] = useState<TaskType>("summary");
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
    void (async () => {
      const isDemo = await fetchDemoMode();
      if (cancelled) return;
      setDemoMode(isDemo);

      try {
        const currentSession = await fetchCurrentSession();
        if (cancelled) return;
        hadStoredSessionRef.current = true;
        setSession(currentSession);
        setAuthError(null);
        return;
      } catch (sessionError) {
        if (cancelled) return;

        if (isDemo) {
          try {
            const demoSession = await ensureDemoSession();
            if (cancelled) return;
            hadStoredSessionRef.current = true;
            setSession(demoSession);
            setAuthError(null);
            return;
          } catch {
            // fall through to reset + show error
          }
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
    setAuthNotice(null);
    return true;
  }

  function handleLogin(event: FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setAuthPending(true);
    setAuthError(null);
    setAuthNotice(null);

    void loginSession(inviteCode.trim(), displayName.trim())
      .then((nextSession) => {
        setSession(nextSession);
        setInviteCode("");
        setDisplayName("");
        setRecentDocuments([]);
        setRecentResults([]);
        clearCurrentDocument();
        setAuthNotice(`已进入试用会话：${nextSession.label}`);
      })
      .catch((loginError) => {
        setAuthError(normalizeAuthErrorMessage(loginError));
      })
      .finally(() => {
        setAuthPending(false);
      });
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

  function handleLogout() {
    setAuthPending(true);
    setAuthError(null);
    setAuthNotice(null);
    void logoutSession()
      .catch(() => undefined)
      .finally(() => {
        clearSessionWorkspace();
        setAuthNotice("已退出当前试用会话。");
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
    setNotice("已切换到论文速读工作台：上传论文后可直接生成结构化速读结果。");
    setError(null);
  }

  function applyConciseDigestPreset() {
    setTaskType("summary");
    setResponseDetailLevel("concise");
    setInput(CONCISE_RESEARCH_DIGEST_PROMPT);
    setNotice("已切换到精简速读：适合现场网络慢或需要快速兜底时使用。");
    setError(null);
  }

  function prepareNationalDemo() {
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
    setPreviewSnippetPage(null);
    setPreviewBboxes([]);
    setTaskType("summary");
    setResponseDetailLevel("detailed");
    setInput(RESEARCH_DIGEST_PROMPT);
    setNotice("国一演示路线已准备：先提交生成速读，再点击推荐追问或拒答边界。手动上传真实论文时同样适用。");
  }

  function applyWhitelistedDemoQuestion(question: string) {
    setTaskType("ask");
    setResponseDetailLevel("balanced");
    setInput(question);
    setNotice("已填入白名单演示问题：点击提交任务后验证证据问答或拒答边界。");
    setError(null);
    scrollElementIntoView('[data-testid="task-input"]');
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
            <p className="subtitle">
              面向论文与报告阅读、答辩准备的文档助手，每一条回答都能跳回 PDF 原文证据。
            </p>
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
            <div className="section-head stats-head">
              <h2 className="panel-title">当前系统状态</h2>
              {logSummary ? (
                <button
                  className="ghost-button stats-toggle"
                  data-testid="stats-toggle"
                  type="button"
                  aria-expanded={statsExpanded}
                  onClick={() => setStatsExpanded((prev) => !prev)}
                >
                  {statsExpanded ? "收起 ▴" : "展开详情 ▾"}
                </button>
              ) : null}
            </div>
            {logSummary ? (
              <>
                <div
                  className={`stats-summary${logSummary.error_count > 0 ? " has-errors" : ""}`}
                  data-testid="stats-summary"
                >
                  <span className="stats-dot" aria-hidden="true" />
                  <span className="stats-summary-text">
                    {logSummary.error_count > 0
                      ? `运行中 · 有效 ${logSummary.answered_count} / 总计 ${logSummary.total_requests}`
                      : `系统正常 · 已完成 ${logSummary.total_requests} 次任务`}
                  </span>
                </div>
                {statsExpanded ? (
                  <div className="stats-grid" data-testid="stats-grid">
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
              </>
            ) : (
              <p className="empty">当前暂无统计数据，完成一次任务后会自动刷新。</p>
            )}
          </article>

          <article className="panel demo-panel">
            <div className="section-head">
              <h2 className="panel-title">一键演示入口</h2>
            </div>
            <p className="subtitle compact">优先走国一演示路线：速读、追问、证据回链、拒答边界一次讲清。</p>
            <div className="national-demo-card">
              <div>
                <span className="demo-kicker">推荐主线</span>
                <strong>国一演示路线</strong>
                <p>自动准备示例文档和论文速读任务，再用白名单追问验证证据问答与拒答边界。</p>
              </div>
              <button
                className="hero-button national-demo-button"
                data-testid="prepare-national-demo"
                type="button"
                disabled={!isAuthenticated || interactionLocked}
                onClick={prepareNationalDemo}
              >
                一键准备演示
              </button>
            </div>
            <div className="demo-whitelist" aria-label="演示白名单问题">
              {DEMO_WHITELIST_ACTIONS.map((action, index) => (
                <button
                  key={action.label}
                  className="demo-whitelist-chip"
                  data-testid={`demo-whitelist-${index}`}
                  type="button"
                  disabled={!isAuthenticated || interactionLocked}
                  onClick={() => applyWhitelistedDemoQuestion(action.input)}
                >
                  <strong>{action.label}</strong>
                  <span>{action.description}</span>
                </button>
              ))}
            </div>
            <div className="demo-actions">
              <button
                className="hero-button"
                type="button"
                disabled={!isAuthenticated || interactionLocked}
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
                  setPreviewSnippetPage(null);
                  setPreviewBboxes([]);
                }}
              >
                填充示例文档
              </button>
              {DEMO_ACTIONS.map((action) => (
                <button
                  key={action.label}
                  className="demo-card"
                  type="button"
                  disabled={!isAuthenticated || interactionLocked}
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
            <div className="trial-boundary-card">
              <strong>
                {demoMode ? "演示模式" : "受控 Alpha"}
                {session ? ` / ${session.label}` : ""}
              </strong>
              <span>
                {demoMode
                  ? "当前为演示环境，上传的文档仅用于现场体验，会话过期后会自动清理；请勿使用敏感资料。"
                  : "当前版本仅面向邀请码试用，上传、检索、预览和删除都会绑定到当前试用会话；请仅使用非敏感文档。"}
              </span>
              {session && !demoMode ? (
                <div className="inline-actions">
                  <button
                    className="ghost-button"
                    data-testid="logout-button"
                    type="button"
                    disabled={interactionLocked}
                    onClick={handleLogout}
                  >
                    退出会话
                  </button>
                </div>
              ) : null}
            </div>
            {!isAuthenticated ? (
              demoMode ? (
                <div className="auth-panel-card">
                  {authLoading ? (
                    <p className="status status-card">正在准备演示环境...</p>
                  ) : (
                    <>
                      <p className="error status-card" data-testid="auth-error">
                        {authError ?? "演示会话暂时无法创建，请稍后重试。"}
                      </p>
                      <div className="control-actions">
                        <button
                          className="submit"
                          type="button"
                          disabled={authPending}
                          onClick={handleRetryDemoSession}
                        >
                          {authPending ? "正在重试..." : "重新进入演示"}
                        </button>
                      </div>
                    </>
                  )}
                </div>
              ) : (
              <div className="auth-panel-card">
                <div className="section-head compact-head">
                  <p className="section-kicker">邀请码登录</p>
                  <h3>先登录再开始试用</h3>
                </div>
                <p className="subtitle compact">
                  输入邀请码后，系统会创建一个短期试用会话，并把当前浏览器里的文档访问权限绑定到该会话。
                </p>
                {authError ? (
                  <p className="error status-card" data-testid="auth-error">
                    {authError}
                  </p>
                ) : null}
                {authNotice ? (
                  <p className="status status-card success-status" data-testid="auth-notice">
                    {authNotice}
                  </p>
                ) : null}
                {authLoading ? (
                  <p className="status status-card">正在校验试用会话...</p>
                ) : null}
                <form className="form" onSubmit={handleLogin}>
                  <label className="field">
                    <span>邀请码</span>
                    <input
                      data-testid="invite-code-input"
                      type="password"
                      value={inviteCode}
                      disabled={authPending || authLoading}
                      onChange={(event) => setInviteCode(event.target.value)}
                    />
                  </label>
                  <label className="field">
                    <span>显示名称（可选）</span>
                    <input
                      data-testid="display-name-input"
                      type="text"
                      value={displayName}
                      disabled={authPending || authLoading}
                      onChange={(event) => setDisplayName(event.target.value)}
                    />
                  </label>
                  <div className="control-actions">
                    <button
                      className="submit"
                      data-testid="login-submit-button"
                      type="submit"
                      disabled={authPending || authLoading || !inviteCode.trim()}
                    >
                      {authPending ? "正在登录..." : "登录试用"}
                    </button>
                  </div>
                </form>
              </div>
              )
            ) : (
              <>
                <form className="form" onSubmit={handleSubmit}>
              <label className="field">
                <span>上传文档</span>
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

              <div className="field">
                <span>任务类型</span>
                <div className="control-option-grid">
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

              <div className="field">
                <span>回答粒度</span>
                <div className="control-detail-grid">
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

              <div className={`digest-workbench${digestPresetActive ? " active" : ""}`}>
                <div>
                  <span className="digest-kicker">产品化速读</span>
                  <strong>论文速读工作台</strong>
                  <p>
                    一键生成研究问题、方法、贡献、实验、局限和追问清单，适合答辩前快速吃透论文。
                  </p>
                  <ol className="digest-flow" aria-label="论文速读演示路径">
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
                <button
                  className="ghost-button digest-button"
                  data-testid="concise-digest-preset"
                  type="button"
                  disabled={interactionLocked}
                  onClick={applyConciseDigestPreset}
                >
                  精简速读兜底
                </button>
              </div>

              <label className="field">
                <span>问题或指令</span>
                <textarea
                  data-testid="task-input"
                  rows={6}
                  value={input}
                  placeholder={currentOption.placeholder}
                  disabled={loading}
                  onChange={(event) => setInput(event.target.value)}
                />
              </label>

              <div className="control-actions">
                <button
                  className="submit"
                  data-testid="submit-task-button"
                  type="submit"
                  disabled={!canSubmit}
                >
                  {loading ? "处理中..." : "提交任务"}
                </button>
                <p className="control-hint">建议先用 Demo 模式体验完整链路，再换真实文档。</p>
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
              <p className="empty">登录后才会显示当前试用会话下的最近文档。</p>
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
              <p className="empty">登录后才会显示当前试用会话下的最近结果。</p>
            ) : recentResults.length === 0 ? (
              <p className="empty">最近 5 次任务结果会显示在这里，方便回看演示。</p>
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
      </main>
    </div>
  );
}
