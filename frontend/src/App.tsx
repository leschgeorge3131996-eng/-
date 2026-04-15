import { useEffect, useState } from "react";
import { ApiRequestError, fetchLogSummary, runTask, uploadDocument } from "./api";
import type {
  LogSummary,
  RecentDocument,
  RecentResult,
  TaskResult,
  TaskType,
  UploadMetadata
} from "./types";

const TASK_OPTIONS: Array<{
  value: TaskType;
  label: string;
  placeholder: string;
}> = [
  {
    value: "summary",
    label: "摘要",
    placeholder: "例如：请突出研究背景、方法和创新点"
  },
  {
    value: "ask",
    label: "问答",
    placeholder: "例如：这篇文档的核心方法是什么？"
  },
  {
    value: "outline",
    label: "提纲生成",
    placeholder: "例如：请生成 6 页答辩提纲"
  }
];

type LoadStage = "idle" | "uploading" | "model";
const RECENT_DOCUMENTS_KEY = "yandatong_recent_documents";
const RECENT_RESULTS_KEY = "yandatong_recent_results";
const MAX_RECENT_DOCUMENTS = 5;
const MAX_RECENT_RESULTS = 5;
const DEMO_DOCUMENT_NAME = "demo_research_brief.md";
const DEMO_DOCUMENT_CONTENT = `# 项目简介

研答通是一个面向科研与智能办公场景的个人智能文档助理。
第一阶段目标是支持用户上传文档，完成摘要、问答和提纲生成。

系统当前采用端云协同路线，优先保证能跑通、能演示、能扩展。
后续将逐步补充 PDF 结构化解析、文本分块、轻量检索、引用返回和评测闭环。`;

function readStorage<T>(key: string, fallback: T): T {
  try {
    const raw = window.localStorage.getItem(key);
    return raw ? (JSON.parse(raw) as T) : fallback;
  } catch {
    return fallback;
  }
}

function writeStorage<T>(key: string, value: T): void {
  window.localStorage.setItem(key, JSON.stringify(value));
}

function describeLoadStage(stage: LoadStage): string {
  if (stage === "uploading") {
    return "正在上传并解析文档...";
  }
  if (stage === "model") {
    return "模型处理中，首次请求可能需要 10 到 40 秒。";
  }
  return "";
}

function normalizeErrorMessage(error: unknown): string {
  if (error instanceof ApiRequestError) {
    if (error.message.includes("请求过快") || error.message.includes("HTTP 429")) {
      return "模型当前较忙，请等待 10 到 30 秒后重试，避免连续点击。";
    }
    if (error.message.includes("超时")) {
      return "模型处理超时，请稍后重试，或换更短的文档内容。";
    }
    return error.message;
  }

  if (error instanceof Error) {
    return error.message;
  }

  return "提交任务失败";
}

function App() {
  const [taskType, setTaskType] = useState<TaskType>("summary");
  const [input, setInput] = useState("");
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [uploadedMetadata, setUploadedMetadata] = useState<UploadMetadata | null>(null);
  const [result, setResult] = useState<TaskResult | null>(null);
  const [loading, setLoading] = useState(false);
  const [loadStage, setLoadStage] = useState<LoadStage>("idle");
  const [error, setError] = useState<string | null>(null);
  const [recentDocuments, setRecentDocuments] = useState<RecentDocument[]>(() =>
    readStorage<RecentDocument[]>(RECENT_DOCUMENTS_KEY, [])
  );
  const [recentResults, setRecentResults] = useState<RecentResult[]>(() =>
    readStorage<RecentResult[]>(RECENT_RESULTS_KEY, [])
  );
  const [logSummary, setLogSummary] = useState<LogSummary | null>(null);

  const currentOption = TASK_OPTIONS.find((item) => item.value === taskType)!;
  const canSubmit =
    !loading &&
    Boolean(selectedFile || uploadedMetadata) &&
    (taskType !== "ask" || Boolean(input.trim()));

  useEffect(() => {
    writeStorage(RECENT_DOCUMENTS_KEY, recentDocuments);
  }, [recentDocuments]);

  useEffect(() => {
    writeStorage(RECENT_RESULTS_KEY, recentResults);
  }, [recentResults]);

  useEffect(() => {
    let active = true;

    async function loadSummary() {
      try {
        const summary = await fetchLogSummary();
        if (active) {
          setLogSummary(summary);
        }
      } catch {
        if (active) {
          setLogSummary(null);
        }
      }
    }

    void loadSummary();
    return () => {
      active = false;
    };
  }, [recentResults.length]);

  function upsertRecentDocument(metadata: UploadMetadata) {
    const nextDocument: RecentDocument = {
      file_id: metadata.file_id,
      original_name: metadata.original_name,
      file_type: metadata.file_type,
      text_chars: metadata.text_chars,
      parse_status: metadata.parse_status,
      saved_at: new Date().toISOString()
    };

    setRecentDocuments((current) => {
      const next = [
        nextDocument,
        ...current.filter((item) => item.file_id !== metadata.file_id)
      ];
      return next.slice(0, MAX_RECENT_DOCUMENTS);
    });
  }

  function pushRecentResult(taskResult: TaskResult, promptText: string) {
    const item: RecentResult = {
      id: taskResult.request_id,
      task_type: taskResult.task_type,
      input: promptText,
      created_at: new Date().toISOString(),
      task_result: taskResult
    };

    setRecentResults((current) => [item, ...current].slice(0, MAX_RECENT_RESULTS));
  }

  function loadDemoDocument() {
    const file = new File([DEMO_DOCUMENT_CONTENT], DEMO_DOCUMENT_NAME, {
      type: "text/markdown"
    });
    setSelectedFile(file);
    setUploadedMetadata(null);
    setResult(null);
    setError(null);
  }

  async function handleSubmit(event: React.FormEvent<HTMLFormElement>) {
    event.preventDefault();
    setLoading(true);
    setLoadStage("idle");
    setError(null);

    try {
      let fileId = uploadedMetadata?.file_id ?? "";

      if (selectedFile) {
        setLoadStage("uploading");
        const upload = await uploadDocument(selectedFile);
        setUploadedMetadata(upload.metadata);
        upsertRecentDocument(upload.metadata);
        fileId = upload.metadata.file_id;
        setSelectedFile(null);
      }

      if (!fileId) {
        throw new Error("请先上传一个文档。");
      }

      if (taskType === "ask" && !input.trim()) {
        throw new Error("问答任务必须输入问题。");
      }

      setLoadStage("model");
      const taskResult = await runTask(taskType, fileId, input.trim());
      setResult(taskResult);
      pushRecentResult(taskResult, input.trim());
    } catch (submitError) {
      setError(normalizeErrorMessage(submitError));
      setResult(null);
    } finally {
      setLoading(false);
      setLoadStage("idle");
    }
  }

  return (
    <div className="page">
      <main className="container">
        <section className="hero">
          <p className="eyebrow">研答通 MVP</p>
          <h1>文档上传、云端处理、结果返回、日志留痕</h1>
          <p className="subtitle">
            第一阶段只做最小闭环：上传 TXT / Markdown / PDF，选择任务，后端调用模型并返回结果。
          </p>
        </section>

        <section className="grid secondary-grid">
          <article className="panel">
            <h2>运行统计</h2>
            {logSummary ? (
              <div className="stats-grid">
                <div className="stat-card">
                  <span>总请求数</span>
                  <strong>{logSummary.total_requests}</strong>
                </div>
                <div className="stat-card">
                  <span>成功率</span>
                  <strong>{Math.round(logSummary.success_rate * 100)}%</strong>
                </div>
                <div className="stat-card">
                  <span>平均延迟</span>
                  <strong>{logSummary.average_latency_ms} ms</strong>
                </div>
                <div className="stat-card">
                  <span>P95 延迟</span>
                  <strong>{logSummary.p95_latency_ms} ms</strong>
                </div>
              </div>
            ) : (
              <p className="empty">当前暂无统计数据，完成一次任务后会自动刷新。</p>
            )}
          </article>

          <article className="panel">
            <h2>Demo 模式</h2>
            <p className="subtitle compact">
              一键填充示例文档和常用指令，方便演示摘要、问答和提纲的完整链路。
            </p>
            <div className="demo-actions">
              <button className="ghost-button" type="button" disabled={loading} onClick={loadDemoDocument}>
                填充示例文档
              </button>
              <button
                className="ghost-button"
                type="button"
                disabled={loading}
                onClick={() => {
                  setTaskType("summary");
                  setInput("请用 3 条要点总结这个文档。");
                }}
              >
                示例摘要
              </button>
              <button
                className="ghost-button"
                type="button"
                disabled={loading}
                onClick={() => {
                  setTaskType("ask");
                  setInput("这个项目第一阶段要做什么？");
                }}
              >
                示例问答
              </button>
              <button
                className="ghost-button"
                type="button"
                disabled={loading}
                onClick={() => {
                  setTaskType("outline");
                  setInput("请生成一个 5 页汇报提纲。");
                }}
              >
                示例提纲
              </button>
            </div>
          </article>
        </section>

        <section className="panel">
          <form className="form" onSubmit={handleSubmit}>
            <label className="field">
              <span>上传文档</span>
              <input
                type="file"
                accept=".txt,.md,.pdf,text/plain,text/markdown,application/pdf"
                disabled={loading}
                onChange={(event) => {
                  const file = event.target.files?.[0] ?? null;
                  setSelectedFile(file);
                  if (file) {
                    setUploadedMetadata(null);
                    setResult(null);
                    setError(null);
                  }
                }}
              />
            </label>

            <label className="field">
              <span>任务类型</span>
              <select
                value={taskType}
                disabled={loading}
                onChange={(event) => setTaskType(event.target.value as TaskType)}
              >
                {TASK_OPTIONS.map((option) => (
                  <option key={option.value} value={option.value}>
                    {option.label}
                  </option>
                ))}
              </select>
            </label>

            <label className="field">
              <span>问题或指令</span>
              <textarea
                rows={5}
                value={input}
                placeholder={currentOption.placeholder}
                disabled={loading}
                onChange={(event) => setInput(event.target.value)}
              />
            </label>

            <button className="submit" type="submit" disabled={!canSubmit}>
              {loading ? "处理中..." : "提交任务"}
            </button>
          </form>
        </section>

        <section className="grid">
          <article className="panel">
            <h2>当前文档</h2>
            {uploadedMetadata ? (
              <div className="meta">
                <p>文件：{uploadedMetadata.original_name}</p>
                <p>类型：{uploadedMetadata.file_type}</p>
                <p>字符数：{uploadedMetadata.text_chars}</p>
                <p>状态：{uploadedMetadata.parse_status}</p>
                <div className="inline-actions">
                  <button
                    className="ghost-button"
                    type="button"
                    disabled={loading}
                    onClick={() => {
                      setUploadedMetadata(null);
                      setSelectedFile(null);
                      setResult(null);
                    }}
                  >
                    清空当前文档
                  </button>
                </div>
              </div>
            ) : (
              <p className="empty">尚未上传文档。</p>
            )}
          </article>

          <article className="panel">
            <h2>处理结果</h2>
            {error ? <p className="error">{error}</p> : null}
            {!error && loading ? <p className="status">{describeLoadStage(loadStage)}</p> : null}
            {!error && !loading && !result ? <p className="empty">提交任务后，这里会显示结果。</p> : null}
            {!error && result ? (
              <div className="result">
                <div className="result-meta">
                  <p>任务：{result.task_type}</p>
                  <p>模型：{result.model_name}</p>
                  <p>耗时：{result.latency_ms} ms</p>
                  <p>请求 ID：{result.request_id}</p>
                </div>
                {result.cache_hit ? (
                  <p className="cache-hit">本次结果命中本地缓存，未重复调用云端模型。</p>
                ) : null}
                {result.context_truncated ? (
                  <p className="warning">
                    {result.truncation_message ??
                      `文档内容过长，后端本次仅发送前 ${result.used_document_chars} / ${result.source_document_chars} 字符。`}
                  </p>
                ) : null}
                {result.token_usage?.total_tokens ? (
                  <p className="status">
                    Token 用量：{result.token_usage.prompt_tokens ?? 0} / {result.token_usage.completion_tokens ?? 0} /{" "}
                    {result.token_usage.total_tokens}
                  </p>
                ) : null}
                <pre>{result.result}</pre>
              </div>
            ) : null}
          </article>
        </section>

        <section className="grid secondary-grid">
          <article className="panel">
            <h2>最近文档</h2>
            {recentDocuments.length === 0 ? (
              <p className="empty">最近上传的文档会显示在这里，便于复用。</p>
            ) : (
              <div className="history-list">
                {recentDocuments.map((item) => (
                  <button
                    key={item.file_id}
                    className="history-card"
                    type="button"
                    disabled={loading}
                    onClick={() => {
                      setUploadedMetadata({
                        file_id: item.file_id,
                        original_name: item.original_name,
                        file_type: item.file_type,
                        size_bytes: 0,
                        text_chars: item.text_chars,
                        parse_status: item.parse_status
                      });
                      setSelectedFile(null);
                      setError(null);
                    }}
                  >
                    <strong>{item.original_name}</strong>
                    <span>
                      {item.file_type} · {item.text_chars} chars
                    </span>
                  </button>
                ))}
              </div>
            )}
          </article>

          <article className="panel">
            <h2>最近结果</h2>
            {recentResults.length === 0 ? (
              <p className="empty">最近 5 次任务结果会显示在这里，方便回看演示。</p>
            ) : (
              <div className="history-list">
                {recentResults.map((item) => (
                  <button
                    key={item.id}
                    className="history-card"
                    type="button"
                    disabled={loading}
                    onClick={() => {
                      setTaskType(item.task_type);
                      setInput(item.input);
                      setResult(item.task_result);
                      setError(null);
                    }}
                  >
                    <strong>{item.task_type.toUpperCase()}</strong>
                    <span>{item.task_result.document_name}</span>
                    <span>{item.input || "无附加输入"}</span>
                  </button>
                ))}
              </div>
            )}
          </article>
        </section>
      </main>
    </div>
  );
}

export default App;
