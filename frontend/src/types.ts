export type TaskType = "summary" | "ask" | "outline";

export interface ApiError {
  code: string;
  message: string;
  details?: Record<string, unknown> | null;
}

export interface ApiResponse<T> {
  success: boolean;
  data: T | null;
  error: ApiError | null;
  request_id?: string | null;
}

export interface UploadMetadata {
  file_id: string;
  original_name: string;
  file_type: string;
  size_bytes: number;
  text_chars: number;
  parse_status: string;
}

export interface UploadResponse {
  metadata: UploadMetadata;
}

export interface TokenUsage {
  prompt_tokens?: number | null;
  completion_tokens?: number | null;
  total_tokens?: number | null;
}

export interface TaskResult {
  request_id: string;
  task_type: TaskType;
  file_id: string;
  document_name: string;
  model_name: string;
  latency_ms: number;
  result: string;
  cache_hit: boolean;
  context_truncated: boolean;
  token_usage?: TokenUsage | null;
}

export interface RecentDocument {
  file_id: string;
  original_name: string;
  file_type: string;
  text_chars: number;
  parse_status: string;
  saved_at: string;
}

export interface RecentResult {
  id: string;
  task_type: TaskType;
  input: string;
  created_at: string;
  task_result: TaskResult;
}
