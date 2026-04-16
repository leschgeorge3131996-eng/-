export type TaskType = "summary" | "ask" | "outline";
export type ResponseDetailLevel = "concise" | "balanced" | "detailed";
export type EvidenceMode = "declared" | "candidate" | "none";
export type PdfPreviewMatchState =
  | "exact_match"
  | "fragment_match"
  | "not_found"
  | "no_snippet";

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

export interface SessionInfo {
  session_id: string;
  label: string;
  created_at: string;
  expires_at: string;
}

export type AuthSession = SessionInfo;

export interface UploadMetadata {
  file_id: string;
  original_name: string;
  access_token?: string | null;
  file_type: string;
  size_bytes: number;
  text_chars: number;
  page_count: number;
  chunk_count: number;
  document_fingerprint?: string | null;
  expires_at?: string | null;
  parse_status: string;
}

export interface UploadResponse {
  metadata: UploadMetadata;
}

export interface DocumentPageData {
  page_number: number;
  char_count: number;
  text: string;
}

export interface TokenUsage {
  prompt_tokens?: number | null;
  completion_tokens?: number | null;
  total_tokens?: number | null;
}

export interface Citation {
  chunk_id: string;
  page_numbers: number[];
  snippet: string;
}

export interface EvidenceQuote {
  chunk_id: string;
  quote: string;
}

export interface TaskResult {
  request_id: string;
  task_type: TaskType;
  file_id: string;
  document_name: string;
  document_fingerprint?: string | null;
  model_name: string;
  route_tier?: string | null;
  route_model?: string | null;
  route_reason?: string | null;
  response_detail_level?: ResponseDetailLevel | null;
  latency_ms: number;
  result: string;
  outcome: string;
  cache_hit: boolean;
  retrieval_status: string;
  retrieval_message?: string | null;
  retrieval_applied: boolean;
  evidence_mode?: EvidenceMode;
  retrieved_chunk_count: number;
  retrieved_pages: number[];
  used_chunk_ids: string[];
  evidence_quotes: EvidenceQuote[];
  citations: Citation[];
  candidate_chunks: Citation[];
  source_chunks: Citation[];
  source_document_chars: number;
  used_document_chars: number;
  truncation_message?: string | null;
  context_truncated: boolean;
  token_usage?: TokenUsage | null;
}

export interface RecentDocument {
  file_id: string;
  original_name: string;
  access_token?: string | null;
  document_fingerprint?: string | null;
  file_type: string;
  text_chars: number;
  page_count: number;
  chunk_count: number;
  expires_at?: string | null;
  parse_status: string;
  saved_at: string;
}

export interface RecentResult {
  id: string;
  task_type: TaskType;
  input: string;
  created_at: string;
  document_snapshot?: UploadMetadata | null;
  task_result: TaskResult;
}

export interface LogSummary {
  total_requests: number;
  success_count: number;
  failure_count: number;
  success_rate: number;
  answered_count: number;
  refused_count: number;
  error_count: number;
  answered_rate: number;
  refused_rate: number;
  average_latency_ms: number;
  p95_latency_ms: number;
  cache_hit_count: number;
  retrieval_applied_count: number;
  citation_count_sum: number;
  token_total_sum: number;
  time_range?: {
    first_timestamp?: string | null;
    last_timestamp?: string | null;
  };
  by_task: Record<string, number>;
  by_model: Record<string, number>;
  by_outcome: Record<string, number>;
  by_response_detail_level?: Record<string, number>;
  by_retrieval_status: Record<string, number>;
  error_types: Record<string, number>;
}
