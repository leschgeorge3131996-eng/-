import { render, screen } from "@testing-library/react";
import React from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import ResultPanel from "./ResultPanel";
import type { TaskResult } from "../types";

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

function makeAskResult(overrides: Partial<TaskResult> = {}): TaskResult {
  return {
    request_id: "req-ledger-1",
    task_type: "ask",
    file_id: "file-1",
    document_name: "paper.pdf",
    document_fingerprint: "fp-1",
    model_name: "deepseek-v4-flash",
    route_tier: "task_specific",
    route_model: "deepseek-v4-flash",
    route_reason: null,
    response_detail_level: "balanced",
    latency_ms: 4200,
    result: "ask answer body",
    outcome: "answered",
    cache_hit: false,
    retrieval_status: "matched",
    retrieval_message: null,
    retrieval_applied: true,
    evidence_mode: "declared",
    retrieved_chunk_count: 3,
    retrieved_pages: [1, 2],
    used_chunk_ids: ["c1", "c2", "c3"],
    evidence_quotes: [],
    citations: [],
    candidate_chunks: [],
    source_chunks: [],
    source_document_chars: 10000,
    used_document_chars: 1300,
    truncation_message: null,
    context_truncated: false,
    token_usage: { prompt_tokens: 704, completion_tokens: 120, total_tokens: 824 },
    platform_request_id: "maas-req-xyz-123",
    ...overrides
  };
}

function renderPanel(result: TaskResult, documentTotalChars: number | null = 10000) {
  return render(
    <ResultPanel
      activeTaskType="ask"
      error={null}
      loading={false}
      loadMessage=""
      result={result}
      documentTotalChars={documentTotalChars}
    />
  );
}

describe("ResultPanel 端云协同 ledger (hidden ?ledger entrance)", () => {
  beforeEach(() => {
    window.history.replaceState({}, "", "/");
  });
  afterEach(() => {
    window.history.replaceState({}, "", "/");
  });

  it("stays hidden for real users (no ?ledger query param)", () => {
    renderPanel(makeAskResult());
    expect(screen.queryByTestId("duanyun-ledger")).not.toBeInTheDocument();
    // The answer itself must still render — gating the ledger must not hide it.
    expect(screen.getByTestId("result-output").textContent).toContain("ask answer body");
  });

  it("shows real, already-returned figures when ?ledger=1 is set", () => {
    window.history.replaceState({}, "", "/?ledger=1");
    renderPanel(makeAskResult());

    const ledger = screen.getByTestId("duanyun-ledger");
    expect(ledger).toBeInTheDocument();
    // char-based compression: used/source = 1300/10000 = 13.0%
    expect(ledger.textContent).toContain("仅上送 13.0%");
    // real platform input tokens, hit evidence, and the reconciliation id
    expect(ledger.textContent).toContain("704");
    expect(ledger.textContent).toContain("3 片段 / 2 页");
    expect(ledger.textContent).toContain("maas-req-xyz-123");
    // honest note carries the raw char counts + saved %
    expect(ledger.textContent).toContain("省约 87.0%");
    expect(ledger.textContent).toContain("无问芯穹控制台");
  });

  it("labels a cache hit as not having hit the cloud this turn", () => {
    window.history.replaceState({}, "", "/?ledger=1");
    renderPanel(makeAskResult({ cache_hit: true }));
    expect(screen.getByTestId("duanyun-ledger").textContent).toContain("未实际调用云端");
  });

  it("falls back gracefully when the full-document size is unknown", () => {
    window.history.replaceState({}, "", "/?ledger=1");
    renderPanel(makeAskResult(), null);
    expect(screen.getByTestId("duanyun-ledger").textContent).toContain(
      "本次文档规模未知或未启用上下文压缩"
    );
  });
});
