import { fireEvent, render, screen, waitFor } from "@testing-library/react";
import React from "react";
import { describe, expect, it, beforeEach, vi } from "vitest";
import App from "./App";
import type {
  AuthSession,
  Citation,
  LogSummary,
  RecentDocument,
  RecentResult,
  TaskResult,
  UploadMetadata
} from "./types";
import {
  ApiRequestError,
  buildFileContentUrl,
  fetchCurrentSession,
  deleteDocument,
  fetchDocumentMetadata,
  fetchDocumentPage,
  fetchLogSummary,
  loginSession,
  logoutSession,
  runTask,
  uploadDocument
} from "./api";

vi.mock("motion/react", async () => {
  const ReactModule = await import("react");

  const motion = new Proxy(
    {},
    {
      get: (_target, tag: string) =>
        ReactModule.forwardRef<HTMLElement, React.HTMLAttributes<HTMLElement>>(
          ({ children, ...props }, ref) =>
            ReactModule.createElement(tag, { ...props, ref }, children)
        )
    }
  );

  return {
    AnimatePresence: ({ children }: { children: React.ReactNode }) =>
      ReactModule.createElement(ReactModule.Fragment, null, children),
    motion
  };
});

vi.mock("./api", async () => {
  const actual = await vi.importActual<typeof import("./api")>("./api");

  return {
    ...actual,
    uploadDocument: vi.fn(),
    runTask: vi.fn(),
    loginSession: vi.fn(),
    fetchCurrentSession: vi.fn(),
    logoutSession: vi.fn(),
    fetchLogSummary: vi.fn(),
    fetchDocumentMetadata: vi.fn(),
    fetchDocumentPage: vi.fn(),
    deleteDocument: vi.fn(),
    buildFileContentUrl: vi.fn(
      (fileId: string, accessToken?: string | null, page?: number) =>
        `/mock/${fileId}/content${accessToken ? `?access_token=${accessToken}` : ""}${page ? `#page=${page}` : ""}`
    )
  };
});

const uploadDocumentMock = vi.mocked(uploadDocument);
const runTaskMock = vi.mocked(runTask);
const loginSessionMock = vi.mocked(loginSession);
const fetchCurrentSessionMock = vi.mocked(fetchCurrentSession);
const logoutSessionMock = vi.mocked(logoutSession);
const fetchLogSummaryMock = vi.mocked(fetchLogSummary);
const fetchDocumentMetadataMock = vi.mocked(fetchDocumentMetadata);
const fetchDocumentPageMock = vi.mocked(fetchDocumentPage);
const deleteDocumentMock = vi.mocked(deleteDocument);
const buildFileContentUrlMock = vi.mocked(buildFileContentUrl);

function makeLogSummary(overrides: Partial<LogSummary> = {}): LogSummary {
  return {
    total_requests: 0,
    success_count: 0,
    failure_count: 0,
    success_rate: 0,
    answered_count: 0,
    refused_count: 0,
    error_count: 0,
    answered_rate: 0,
    refused_rate: 0,
    average_latency_ms: 0,
    p95_latency_ms: 0,
    cache_hit_count: 0,
    retrieval_applied_count: 0,
    citation_count_sum: 0,
    token_total_sum: 0,
    by_task: {},
    by_model: {},
    by_outcome: {},
    by_response_detail_level: {},
    by_retrieval_status: {},
    error_types: {},
    ...overrides
  };
}

function makeAuthSession(overrides: Partial<AuthSession> = {}): AuthSession {
  return {
    session_id: "session-1",
    label: "alpha-user",
    created_at: "2026-04-16T08:00:00Z",
    expires_at: "2026-04-23T08:00:00Z",
    ...overrides
  };
}

function makeMetadata(overrides: Partial<UploadMetadata> = {}): UploadMetadata {
  return {
    file_id: "file-1",
    original_name: "alpha.md",
    access_token: "token-1",
    file_type: "md",
    size_bytes: 256,
    text_chars: 240,
    page_count: 1,
    chunk_count: 2,
    document_fingerprint: "fingerprint-1",
    expires_at: "2026-04-19T08:00:00Z",
    parse_status: "parsed",
    ...overrides
  };
}

function makeCitation(overrides: Partial<Citation> = {}): Citation {
  return {
    chunk_id: "chunk-1",
    page_numbers: [1],
    snippet: "source snippet",
    ...overrides
  };
}

function makeTaskResult(overrides: Partial<TaskResult> = {}): TaskResult {
  return {
    request_id: "req-1",
    task_type: "summary",
    file_id: "file-1",
    document_name: "alpha.md",
    document_fingerprint: "fingerprint-1",
    model_name: "mock::summary",
    route_tier: "lite",
    route_model: "mock::summary",
    route_reason: "test",
    response_detail_level: "balanced",
    latency_ms: 120,
    result: "summary answer",
    outcome: "answered",
    cache_hit: false,
    retrieval_status: "coverage",
    retrieval_message: null,
    retrieval_applied: false,
    evidence_mode: "declared",
    retrieved_chunk_count: 0,
    retrieved_pages: [],
    used_chunk_ids: [],
    evidence_quotes: [],
    citations: [],
    candidate_chunks: [],
    source_chunks: [makeCitation()],
    source_document_chars: 240,
    used_document_chars: 240,
    truncation_message: null,
    context_truncated: false,
    token_usage: {
      prompt_tokens: 12,
      completion_tokens: 8,
      total_tokens: 20
    },
    ...overrides
  };
}

function setRecentState(documents: RecentDocument[], results: RecentResult[]): void {
  window.localStorage.setItem("yandatong_recent_documents", JSON.stringify(documents));
  window.localStorage.setItem("yandatong_recent_results", JSON.stringify(results));
}

function seedSession(session: AuthSession = makeAuthSession()): AuthSession {
  window.localStorage.setItem("yandatong_auth_session", JSON.stringify(session));
  fetchCurrentSessionMock.mockResolvedValue(session);
  return session;
}

describe("App smoke flows", () => {
  beforeEach(() => {
    window.localStorage.clear();
    loginSessionMock.mockReset();
    fetchCurrentSessionMock.mockReset();
    logoutSessionMock.mockReset();
    fetchLogSummaryMock.mockResolvedValue(makeLogSummary());
    uploadDocumentMock.mockReset();
    runTaskMock.mockReset();
    fetchDocumentMetadataMock.mockReset();
    fetchDocumentPageMock.mockReset();
    fetchCurrentSessionMock.mockRejectedValue(
      new ApiRequestError("trial session expired", "UNAUTHORIZED")
    );
    deleteDocumentMock.mockResolvedValue({
      deleted: true,
      file_id: "file-1",
      original_name: "alpha.md"
    });
    logoutSessionMock.mockResolvedValue();
    buildFileContentUrlMock.mockImplementation(
      (fileId: string, accessToken?: string | null, page?: number) =>
        `/mock/${fileId}/content${accessToken ? `?access_token=${accessToken}` : ""}${page ? `#page=${page}` : ""}`
    );
  });

  it("creates a trial session from the invite-code form", async () => {
    const session = makeAuthSession({
      session_id: "session-login",
      label: "lab-user"
    });
    loginSessionMock.mockResolvedValue(session);

    render(<App />);

    await waitFor(() =>
      expect(screen.getByTestId("invite-code-input")).toBeInTheDocument()
    );
    fireEvent.change(screen.getByTestId("invite-code-input"), {
      target: { value: "invite-123" }
    });
    fireEvent.change(screen.getByTestId("display-name-input"), {
      target: { value: "lab-user" }
    });
    fireEvent.click(screen.getByTestId("login-submit-button"));

    await waitFor(() =>
      expect(loginSessionMock).toHaveBeenCalledWith("invite-123", "lab-user")
    );
    await waitFor(() =>
      expect(screen.getByTestId("logout-button")).toBeInTheDocument()
    );
    expect(screen.queryByTestId("invite-code-input")).not.toBeInTheDocument();
  });

  it("logs out and returns to the invite-code screen", async () => {
    seedSession(makeAuthSession({ session_id: "session-logout" }));

    render(<App />);

    await waitFor(() => expect(fetchCurrentSessionMock).toHaveBeenCalled());
    fireEvent.click(screen.getByTestId("logout-button"));

    await waitFor(() => expect(logoutSessionMock).toHaveBeenCalledTimes(1));
    await waitFor(() =>
      expect(screen.getByTestId("invite-code-input")).toBeInTheDocument()
    );
    expect(window.localStorage.getItem("yandatong_auth_session")).toBeNull();
  });

  it("clears stale local auth state when the cookie session is gone", async () => {
    window.localStorage.setItem(
      "yandatong_auth_session",
      JSON.stringify(makeAuthSession({ session_id: "stale-session" }))
    );

    render(<App />);

    await waitFor(() => expect(fetchCurrentSessionMock).toHaveBeenCalled());
    await waitFor(() =>
      expect(screen.getByTestId("invite-code-input")).toBeInTheDocument()
    );
    expect(window.localStorage.getItem("yandatong_auth_session")).toBeNull();
  });

  it("runs the upload-to-summary happy path and stores recent history", async () => {
    seedSession();
    const metadata = makeMetadata({
      file_id: "file-summary",
      original_name: "brief.md",
      access_token: "token-summary"
    });
    const taskResult = makeTaskResult({
      request_id: "req-summary",
      file_id: metadata.file_id,
      document_name: metadata.original_name,
      document_fingerprint: metadata.document_fingerprint,
      result: "summary smoke result"
    });

    uploadDocumentMock.mockImplementation(async (_file, onProgress) => {
      onProgress?.(100);
      return { metadata };
    });
    runTaskMock.mockResolvedValue(taskResult);

    render(<App />);

    await waitFor(() => expect(fetchCurrentSessionMock).toHaveBeenCalled());

    const fileInput = screen.getByTestId("file-input") as HTMLInputElement;
    fireEvent.change(fileInput, {
      target: {
        files: [new File(["demo content"], "brief.md", { type: "text/markdown" })]
      }
    });
    fireEvent.click(screen.getByTestId("submit-task-button"));

    await waitFor(() => expect(uploadDocumentMock).toHaveBeenCalledTimes(1));
    await waitFor(() =>
      expect(runTaskMock).toHaveBeenCalledWith(
        "summary",
        "file-summary",
        "",
        "balanced",
        "token-summary"
      )
    );

    await waitFor(() =>
      expect(screen.getByTestId("result-output").textContent).toContain("summary smoke result")
    );
    expect(screen.getByTestId("current-document-name").textContent).toContain("brief.md");
    expect(screen.getByTestId("recent-document-file-summary")).toBeTruthy();
    expect(screen.getByTestId("recent-result-req-summary")).toBeTruthy();
  });

  it("opens and re-targets PDF preview from ask citations", async () => {
    seedSession();
    const metadata = makeMetadata({
      file_id: "file-pdf",
      original_name: "paper.pdf",
      access_token: "token-pdf",
      file_type: "pdf",
      page_count: 6
    });
    const taskResult = makeTaskResult({
      request_id: "req-ask",
      task_type: "ask",
      file_id: metadata.file_id,
      document_name: metadata.original_name,
      document_fingerprint: metadata.document_fingerprint,
      model_name: "mock::ask",
      route_tier: "pro",
      route_model: "mock::ask",
      response_detail_level: "balanced",
      result: "ask smoke result",
      retrieval_status: "matched",
      retrieval_applied: true,
      evidence_mode: "declared",
      retrieved_chunk_count: 2,
      retrieved_pages: [2, 5],
      used_chunk_ids: ["chunk-a", "chunk-b"],
      evidence_quotes: [{ chunk_id: "chunk-a", quote: "goal sentence" }],
      citations: [
        makeCitation({ chunk_id: "chunk-a", page_numbers: [2], snippet: "goal sentence" }),
        makeCitation({ chunk_id: "chunk-b", page_numbers: [5], snippet: "method sentence" })
      ],
      candidate_chunks: [],
      source_chunks: []
    });

    uploadDocumentMock.mockImplementation(async (_file, onProgress) => {
      onProgress?.(100);
      return { metadata };
    });
    runTaskMock.mockResolvedValue(taskResult);
    fetchDocumentPageMock.mockImplementation(async (_fileId, pageNumber) => ({
      page_number: pageNumber,
      char_count: 32,
      text:
        pageNumber === 5
          ? "Method sentence appears on page five."
          : "Goal sentence appears on page two."
    }));

    render(<App />);

    await waitFor(() => expect(fetchCurrentSessionMock).toHaveBeenCalled());

    fireEvent.change(screen.getByTestId("file-input"), {
      target: {
        files: [new File(["pdf bytes"], "paper.pdf", { type: "application/pdf" })]
      }
    });
    fireEvent.click(screen.getByTestId("task-option-ask"));
    fireEvent.change(screen.getByTestId("task-input"), {
      target: { value: "What is the goal?" }
    });
    fireEvent.click(screen.getByTestId("submit-task-button"));

    await waitFor(() =>
      expect(runTaskMock).toHaveBeenCalledWith(
        "ask",
        "file-pdf",
        "What is the goal?",
        "balanced",
        "token-pdf"
      )
    );
    await waitFor(() =>
      expect(fetchDocumentPageMock).toHaveBeenCalledWith("file-pdf", 2, "token-pdf")
    );
    expect(screen.getByTestId("pdf-preview-panel")).toBeTruthy();

    fireEvent.click(screen.getByTestId("open-pdf-chunk-b-1"));

    await waitFor(() =>
      expect(fetchDocumentPageMock).toHaveBeenCalledWith("file-pdf", 5, "token-pdf")
    );
    await waitFor(() =>
      expect((screen.getByTestId("pdf-preview-frame") as HTMLImageElement).src).toContain("/pages/5/render")
    );
  });

  it("restores a recent result with the saved access token and state", async () => {
    seedSession(makeAuthSession({ session_id: "session-restore" }));
    const metadata = makeMetadata({
      file_id: "file-restore",
      original_name: "restored.md",
      access_token: "token-restore"
    });
    const taskResult = makeTaskResult({
      request_id: "req-restore",
      task_type: "ask",
      file_id: metadata.file_id,
      document_name: metadata.original_name,
      document_fingerprint: metadata.document_fingerprint,
      response_detail_level: "detailed",
      result: "restored answer",
      retrieval_status: "matched",
      retrieval_applied: true,
      evidence_mode: "declared",
      retrieved_chunk_count: 1,
      retrieved_pages: [1],
      used_chunk_ids: ["chunk-restore"],
      evidence_quotes: [{ chunk_id: "chunk-restore", quote: "restore quote" }],
      citations: [makeCitation({ chunk_id: "chunk-restore", page_numbers: [1], snippet: "restore snippet" })],
      candidate_chunks: [],
      source_chunks: []
    });

    setRecentState(
      [
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
          saved_at: "2026-04-16T08:00:00Z"
        }
      ],
      [
        {
          id: "req-restore",
          task_type: "ask",
          input: "restored question",
          created_at: "2026-04-16T08:00:00Z",
          document_snapshot: metadata,
          task_result: taskResult
        }
      ]
    );

    fetchDocumentMetadataMock.mockResolvedValue({ metadata });

    render(<App />);

    await waitFor(() => expect(fetchCurrentSessionMock).toHaveBeenCalled());

    fireEvent.click(screen.getByTestId("recent-result-req-restore"));

    await waitFor(() =>
      expect(fetchDocumentMetadataMock).toHaveBeenCalledWith("file-restore", "token-restore")
    );
    await waitFor(() =>
      expect(screen.getByTestId("result-output").textContent).toContain("restored answer")
    );
    expect(screen.getByTestId("current-document-name").textContent).toContain("restored.md");
    expect(screen.getByTestId("task-input")).toHaveValue("restored question");
    expect(screen.getByTestId("task-option-ask")).toHaveAttribute("aria-pressed", "true");
    expect(screen.getByTestId("detail-option-detailed")).toHaveAttribute("aria-pressed", "true");
  });

  it("deletes the current document and clears recent history records", async () => {
    seedSession(makeAuthSession({ session_id: "session-delete" }));
    const metadata = makeMetadata({
      file_id: "file-delete",
      original_name: "to-delete.md",
      access_token: "token-delete"
    });
    const taskResult = makeTaskResult({
      request_id: "req-delete",
      file_id: metadata.file_id,
      document_name: metadata.original_name,
      document_fingerprint: metadata.document_fingerprint,
      result: "delete me"
    });

    setRecentState(
      [
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
          saved_at: "2026-04-16T08:30:00Z"
        }
      ],
      [
        {
          id: taskResult.request_id,
          task_type: taskResult.task_type,
          input: "delete question",
          created_at: "2026-04-16T08:30:00Z",
          document_snapshot: metadata,
          task_result: taskResult
        }
      ]
    );

    fetchDocumentMetadataMock.mockResolvedValue({ metadata });
    deleteDocumentMock.mockResolvedValue({
      deleted: true,
      file_id: metadata.file_id,
      original_name: metadata.original_name
    });

    render(<App />);

    await waitFor(() => expect(fetchCurrentSessionMock).toHaveBeenCalled());

    fireEvent.click(screen.getByTestId("recent-result-req-delete"));

    await waitFor(() =>
      expect(screen.getByTestId("current-document-name").textContent).toContain("to-delete.md")
    );

    fireEvent.click(screen.getByTestId("delete-current-document-button"));

    await waitFor(() =>
      expect(deleteDocumentMock).toHaveBeenCalledWith("file-delete", "token-delete")
    );
    await waitFor(() =>
      expect(screen.getByTestId("notice-banner").textContent).toContain("已删除")
    );
    await waitFor(() =>
      expect(screen.queryByTestId("recent-document-file-delete")).not.toBeInTheDocument()
    );
    await waitFor(() =>
      expect(screen.queryByTestId("recent-result-req-delete")).not.toBeInTheDocument()
    );
    await waitFor(() =>
      expect(screen.queryByTestId("delete-current-document-button")).not.toBeInTheDocument()
    );

    await waitFor(() => {
      const recentDocuments = JSON.parse(
        window.localStorage.getItem("yandatong_recent_documents") ?? "[]"
      );
      const recentResults = JSON.parse(
        window.localStorage.getItem("yandatong_recent_results") ?? "[]"
      );

      expect(recentDocuments).toEqual([]);
      expect(recentResults).toEqual([]);
    });
  });
});
