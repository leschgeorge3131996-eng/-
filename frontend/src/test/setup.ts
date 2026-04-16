import "@testing-library/jest-dom/vitest";
import { cleanup } from "@testing-library/react";
import { afterEach, beforeEach, vi } from "vitest";

beforeEach(() => {
  window.localStorage.clear();
  vi.stubGlobal("scrollTo", vi.fn());
  vi.stubGlobal("confirm", vi.fn(() => true));

  if (!URL.createObjectURL) {
    Object.defineProperty(URL, "createObjectURL", {
      configurable: true,
      value: vi.fn(() => "blob:mock")
    });
  }

  if (!URL.revokeObjectURL) {
    Object.defineProperty(URL, "revokeObjectURL", {
      configurable: true,
      value: vi.fn()
    });
  }
});

afterEach(() => {
  cleanup();
  vi.restoreAllMocks();
});
