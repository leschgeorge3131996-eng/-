import type {
  ApiResponse,
  AuthSession,
  DocumentPageData,
  LogSummary,
  ResponseDetailLevel,
  SessionInfo,
  TaskResult,
  TaskType,
  UploadResponse
} from "./types";

const rawApiBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim();
const API_BASE_URL = rawApiBaseUrl ? rawApiBaseUrl.replace(/\/+$/, "") : "/api";
const AUTH_SESSION_STORAGE_KEY = "yandatong_auth_session";
const TASK_REQUEST_TIMEOUT_MS = 90_000;

type LoginPayload = {
  session: SessionInfo;
};

type CurrentSessionPayload = {
  session: SessionInfo;
};

function readSessionStorage(): AuthSession | null {
  try {
    const raw = window.localStorage.getItem(AUTH_SESSION_STORAGE_KEY);
    return raw ? (JSON.parse(raw) as AuthSession) : null;
  } catch {
    return null;
  }
}

function writeSessionStorage(session: AuthSession | null): void {
  if (session) {
    window.localStorage.setItem(AUTH_SESSION_STORAGE_KEY, JSON.stringify(session));
    return;
  }
  window.localStorage.removeItem(AUTH_SESSION_STORAGE_KEY);
}

function buildProtectedFileUrl(fileId: string, accessToken?: string | null, suffix = ""): string {
  const baseUrl = `${API_BASE_URL}/files/${fileId}${suffix}`;
  if (!accessToken) {
    return baseUrl;
  }

  const query = new URLSearchParams();
  query.set("access_token", accessToken);
  return `${baseUrl}?${query.toString()}`;
}

export function buildFileContentUrl(
  fileId: string,
  accessToken?: string | null,
  page?: number
): string {
  const baseUrl = buildProtectedFileUrl(fileId, accessToken, "/content");
  return page && page > 0 ? `${baseUrl}#page=${page}` : baseUrl;
}

export const PDF_PAGE_RENDER_DPI = 144;

export function buildPdfPageRenderUrl(
  fileId: string,
  pageNumber: number,
  accessToken?: string | null,
  dpi: number = PDF_PAGE_RENDER_DPI
): string {
  const query = new URLSearchParams();
  query.set("dpi", String(dpi));
  if (accessToken) {
    query.set("access_token", accessToken);
  }
  return `${API_BASE_URL}/files/${fileId}/pages/${pageNumber}/render?${query.toString()}`;
}

export class ApiRequestError extends Error {
  code?: string;
  details?: Record<string, unknown> | null;

  constructor(message: string, code?: string, details?: Record<string, unknown> | null) {
    super(message);
    this.name = "ApiRequestError";
    this.code = code;
    this.details = details;
  }
}

function looksLikeHtmlDocument(text: string): boolean {
  return /^\s*<(?:!DOCTYPE|html|head|body)/i.test(text);
}

function buildNonJsonResponseError(status: number, text: string): ApiRequestError {
  const preview = text.slice(0, 140).trim();
  const message = looksLikeHtmlDocument(text)
    ? "服务返回了页面而不是接口数据，请刷新页面或重启本地服务后重试。"
    : "服务返回了无法识别的数据格式，请稍后重试。";

  return new ApiRequestError(message, "NON_JSON_RESPONSE", {
    status,
    preview
  });
}

function isAbortError(error: unknown): boolean {
  return error instanceof DOMException && error.name === "AbortError";
}

async function fetchWithTimeout(
  input: RequestInfo | URL,
  init: RequestInit,
  timeoutMs: number
): Promise<Response> {
  const controller = new AbortController();
  const timeoutId = window.setTimeout(() => controller.abort(), timeoutMs);

  try {
    return await fetch(input, {
      ...init,
      signal: controller.signal
    });
  } catch (error) {
    if (isAbortError(error)) {
      throw new ApiRequestError(
        "模型响应超过 90 秒。现场演示可先切换“精简速读兜底”，或稍后重试当前任务。",
        "TASK_TIMEOUT",
        { timeout_ms: timeoutMs }
      );
    }
    throw error;
  } finally {
    window.clearTimeout(timeoutId);
  }
}

async function parseResponse<T>(response: Response): Promise<T> {
  const text = await response.text();
  if (!text.trim()) {
    throw new ApiRequestError("服务未返回数据，请稍后重试。", "EMPTY_RESPONSE");
  }

  let payload: ApiResponse<T>;
  try {
    payload = JSON.parse(text) as ApiResponse<T>;
  } catch {
    throw buildNonJsonResponseError(response.status, text);
  }

  if (!response.ok || !payload.success || payload.data === null || payload.data === undefined) {
    throw new ApiRequestError(
      payload.error?.message ?? "请求失败",
      payload.error?.code,
      payload.error?.details ?? null
    );
  }
  return payload.data;
}

function parsePayloadText<T>(text: string, status: number): T {
  let payload: ApiResponse<T>;
  try {
    payload = JSON.parse(text) as ApiResponse<T>;
  } catch {
    throw buildNonJsonResponseError(status, text);
  }

  if (status < 200 || status >= 300 || !payload.success || payload.data === null || payload.data === undefined) {
    throw new ApiRequestError(
      payload.error?.message ?? "请求失败",
      payload.error?.code,
      payload.error?.details ?? null
    );
  }
  return payload.data;
}

export async function loginSession(
  inviteCode: string,
  displayName: string
): Promise<AuthSession> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify({
      invite_code: inviteCode,
      display_name: displayName || null
    })
  });
  const payload = await parseResponse<LoginPayload>(response);
  const session: AuthSession = payload.session;
  writeSessionStorage(session);
  return session;
}

export async function ensureDemoSession(): Promise<AuthSession> {
  const response = await fetch(`${API_BASE_URL}/auth/demo-session`, {
    method: "POST",
    credentials: "include"
  });
  const payload = await parseResponse<LoginPayload>(response);
  const session: AuthSession = payload.session;
  writeSessionStorage(session);
  return session;
}

export async function fetchDemoMode(): Promise<boolean> {
  try {
    const response = await fetch(`${API_BASE_URL}/health`, { credentials: "include" });
    const payload = await parseResponse<{ demo_mode?: boolean }>(response);
    return Boolean(payload.demo_mode);
  } catch {
    return false;
  }
}

export async function fetchCurrentSession(): Promise<AuthSession> {
  const response = await fetch(`${API_BASE_URL}/auth/session`, {
    credentials: "include"
  });
  const payload = await parseResponse<CurrentSessionPayload>(response);
  const session: AuthSession = payload.session;
  writeSessionStorage(session);
  return session;
}

export async function logoutSession(): Promise<void> {
  try {
    const response = await fetch(`${API_BASE_URL}/auth/logout`, {
      method: "POST",
      credentials: "include"
    });
    await parseResponse<{ logged_out: boolean }>(response);
  } finally {
    clearStoredSession();
  }
}

export async function uploadDocument(
  file: File,
  onProgress?: (progress: number) => void
): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  return new Promise<UploadResponse>((resolve, reject) => {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", `${API_BASE_URL}/upload`);
    xhr.withCredentials = true;

    xhr.upload.onprogress = (event) => {
      if (event.lengthComputable && onProgress) {
        onProgress(Math.min(100, Math.round((event.loaded / event.total) * 100)));
      }
    };

    xhr.onerror = () => {
      reject(new ApiRequestError("上传失败，请检查网络连接或服务状态。"));
    };

    xhr.onload = () => {
      try {
        const data = parsePayloadText<UploadResponse>(xhr.responseText, xhr.status);
        if (onProgress) {
          onProgress(100);
        }
        resolve(data);
      } catch (error) {
        reject(error);
      }
    };

    xhr.send(formData);
  });
}

export async function runTask(
  taskType: TaskType,
  fileId: string,
  input: string,
  responseDetailLevel: ResponseDetailLevel,
  accessToken?: string | null
): Promise<TaskResult> {
  const endpoint = `${API_BASE_URL}/${taskType}`;
  const payload =
    taskType === "ask"
      ? {
          file_id: fileId,
          question: input,
          document_access_token: accessToken ?? null,
          response_detail_level: responseDetailLevel
        }
      : {
          file_id: fileId,
          instruction: input || null,
          document_access_token: accessToken ?? null,
          response_detail_level: responseDetailLevel
        };

  const response = await fetchWithTimeout(endpoint, {
    method: "POST",
    credentials: "include",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  }, TASK_REQUEST_TIMEOUT_MS);
  return parseResponse<TaskResult>(response);
}

export async function fetchLogSummary(): Promise<LogSummary> {
  const response = await fetch(`${API_BASE_URL}/logs/summary`, {
    credentials: "include"
  });
  return parseResponse<LogSummary>(response);
}

export function readStoredSession(): AuthSession | null {
  return readSessionStorage();
}

export function clearStoredSession(): void {
  writeSessionStorage(null);
}

export async function fetchDocumentPage(
  fileId: string,
  pageNumber: number,
  accessToken?: string | null
): Promise<DocumentPageData> {
  const response = await fetch(buildProtectedFileUrl(fileId, accessToken, `/pages/${pageNumber}`), {
    credentials: "include"
  });
  return parseResponse<DocumentPageData>(response);
}

export async function fetchDocumentMetadata(
  fileId: string,
  accessToken?: string | null
): Promise<UploadResponse> {
  const response = await fetch(buildProtectedFileUrl(fileId, accessToken, "/metadata"), {
    credentials: "include"
  });
  return parseResponse<UploadResponse>(response);
}

export async function deleteDocument(
  fileId: string,
  accessToken?: string | null
): Promise<{ deleted: boolean; file_id: string; original_name: string }> {
  const response = await fetch(buildProtectedFileUrl(fileId, accessToken), {
    method: "DELETE",
    credentials: "include"
  });
  return parseResponse<{ deleted: boolean; file_id: string; original_name: string }>(response);
}
