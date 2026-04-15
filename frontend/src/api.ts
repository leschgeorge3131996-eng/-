import type { ApiResponse, TaskResult, TaskType, UploadResponse } from "./types";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api";

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

export async function uploadDocument(file: File): Promise<UploadResponse> {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch(`${API_BASE_URL}/upload`, {
    method: "POST",
    body: formData
  });
  return parseResponse<UploadResponse>(response);
}

export async function runTask(
  taskType: TaskType,
  fileId: string,
  input: string
): Promise<TaskResult> {
  const endpoint = `${API_BASE_URL}/${taskType}`;
  const payload =
    taskType === "ask"
      ? { file_id: fileId, question: input }
      : { file_id: fileId, instruction: input || null };

  const response = await fetch(endpoint, {
    method: "POST",
    headers: {
      "Content-Type": "application/json"
    },
    body: JSON.stringify(payload)
  });
  return parseResponse<TaskResult>(response);
}
