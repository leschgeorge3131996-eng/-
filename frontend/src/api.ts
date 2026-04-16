import type {
  ApiResponse,
  LogSummary,
  ResponseDetailLevel,
  TaskResult,
  TaskType,
  UploadResponse
} from "./types";

const rawApiBaseUrl = import.meta.env.VITE_API_BASE_URL?.trim();
const API_BASE_URL = rawApiBaseUrl ? rawApiBaseUrl.replace(/\/+$/, "") : "/api";

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

async function parseResponse<T>(response: Response): Promise<T> {
  const payload = (await response.json()) as ApiResponse<T>;
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
  const payload = JSON.parse(text) as ApiResponse<T>;
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
