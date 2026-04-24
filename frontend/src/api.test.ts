import { describe, expect, it, vi } from "vitest";
import { ApiRequestError, runTask } from "./api";

describe("api task timeout", () => {
  it("maps aborted task requests to a friendly timeout error", async () => {
    vi.useFakeTimers();
    const fetchMock = vi.fn((_url: RequestInfo | URL, init?: RequestInit) =>
      new Promise<Response>((_resolve, reject) => {
        init?.signal?.addEventListener("abort", () => {
          reject(new DOMException("Aborted", "AbortError"));
        });
      })
    );
    vi.stubGlobal("fetch", fetchMock);

    const taskPromise = runTask("summary", "file-timeout", "", "detailed", "token-timeout");
    const rejection = expect(taskPromise).rejects.toMatchObject({
      name: "ApiRequestError",
      code: "TASK_TIMEOUT"
    } satisfies Partial<ApiRequestError>);
    await vi.advanceTimersByTimeAsync(90_000);

    await rejection;
    expect(fetchMock).toHaveBeenCalledWith(
      "/api/summary",
      expect.objectContaining({ signal: expect.any(AbortSignal) })
    );

    vi.useRealTimers();
  });
});
