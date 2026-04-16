import type {
  ApiResponse,
  DocumentPageData,
  LogSummary,
  ResponseDetailLevel,
  TaskResult,
  TaskType,
  UploadResponse
} from "./types";

const rawApiBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim();
const API_BASE_URL = rawApiBaseUrl ? rawApiBaseUrl.replace(/\/+$/, "") : "/api";

export function buildFileContentUrl(fileId: string, page?: number): string {
  const baseUrl = `${API_BASE_URL}/files/${fileId}/content`;
  return page && page > 0 ? `${baseUrl}#page=${page}` : baseUrl;
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

  if (!response.ok || !payload.success || !payload.data) {
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

  if (status < 200 || status >= 300 || !payload.success || !payload.data) {
    throw new ApiRequestError(
      payload.error?.message ?? "请求失败",
      payload.error?.code,
      payload.error?.details ?? null
    );
  }
  return payload.data;
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
  responseDetailLevel: ResponseDetailLevel
): Promise<TaskResult> {
  const endpoint = `${API_BASE_URL}/${taskType}`;
  const payload =
    taskType === "ask"
      ? { file_id: fileId, question: input, response_detail_level: responseDetailLevel }
      : { file_id: fileId, instruction: input || null, response_detail_level: responseDetailLevel };

  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });
  return parseResponse<TaskResult>(response);
}

export async function fetchLogSummary(): Promise<LogSummary> {
  const response = await fetch(`${API_BASE_URL}/logs/summary`);
  return parseResponse<LogSummary>(response);
}

export async function fetchDocumentPage(fileId: string, pageNumber: number): Promise<DocumentPageData> {
  const response = await fetch(`${API_BASE_URL}/files/${fileId}/pages/${pageNumber}`);
  return parseResponse<DocumentPageData>(response);
}

export async function fetchDocumentMetadata(fileId: string): Promise<UploadResponse> {
  const response = await fetch(`${API_BASE_URL}/files/${fileId}/metadata`);
  return parseResponse<UploadResponse>(response);
}
