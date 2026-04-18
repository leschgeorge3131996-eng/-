const fs = require("fs");
const fsp = require("fs/promises");
const http = require("http");
const path = require("path");
const { spawn } = require("child_process");

const ROOT = path.resolve(__dirname, "..");
const FRONTEND_DIR = path.join(ROOT, "frontend");
const FRONTEND_DIST_DIR = path.join(FRONTEND_DIR, "dist");
const TMP_DIR = path.join(ROOT, "tmp");
const SCREENSHOT_DIR = path.join(ROOT, "evidence", "screenshots");
const SAMPLE_PDF = path.join(ROOT, "evidence", "samples", "chinese_llm_spatial_eval.pdf");
const FRONTEND_URL = "http://127.0.0.1:5173";
const BACKEND_HEALTH_URL = "http://127.0.0.1:8000/api/health";
const REMOTE_DEBUGGING_PORT = 9222;
const WINDOW_WIDTH = 1440;
const WINDOW_HEIGHT = 2200;

const PROMPTS = {
  askResearchFocus: "这篇论文主要研究了什么问题？",
  askRankAccuracy: "作者最终的方法排名和总体准确率分别是多少？",
  refusal: "木星有几颗卫星？",
};

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function timestampDate() {
  const now = new Date();
  const year = String(now.getFullYear());
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  return `${year}${month}${day}`;
}

function readEnvFile(envPath) {
  if (!fs.existsSync(envPath)) {
    return {};
  }

  const values = {};
  const lines = fs.readFileSync(envPath, "utf8").split(/\r?\n/);
  for (const rawLine of lines) {
    const line = rawLine.trim();
    if (!line || line.startsWith("#") || !line.includes("=")) {
      continue;
    }
    const [rawKey, ...rawRest] = line.split("=");
    const key = rawKey.trim();
    const value = rawRest.join("=").trim().replace(/^['"]|['"]$/g, "");
    values[key] = value;
  }
  return values;
}

async function ensureDir(dirPath) {
  await fsp.mkdir(dirPath, { recursive: true });
}

async function httpOk(url) {
  try {
    const response = await fetch(url, { redirect: "follow" });
    return response.ok;
  } catch {
    return false;
  }
}

async function fetchJson(url) {
  const response = await fetch(url, { redirect: "follow" });
  if (!response.ok) {
    throw new Error(`Request failed: ${url} -> ${response.status}`);
  }
  return response.json();
}

async function waitFor(condition, timeoutMs, label) {
  const deadline = Date.now() + timeoutMs;
  while (Date.now() < deadline) {
    const result = await condition();
    if (result) {
      return result;
    }
    await sleep(400);
  }
  throw new Error(`Timed out waiting for ${label}`);
}

function resolveBrowserPath() {
  const candidates = [
    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
    "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe",
    "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe",
  ];

  for (const candidate of candidates) {
    if (fs.existsSync(candidate)) {
      return candidate;
    }
  }
  throw new Error("No supported browser found. Expected Edge or Chrome.");
}

function spawnLoggedProcess(command, args, options) {
  const logPath = options.logPath;
  const logStream = fs.createWriteStream(logPath, { flags: "a" });
  const child = spawn(command, args, {
    cwd: options.cwd,
    env: options.env,
    stdio: ["ignore", "pipe", "pipe"],
    shell: false,
    windowsHide: true,
  });

  child.stdout.on("data", (chunk) => logStream.write(chunk));
  child.stderr.on("data", (chunk) => logStream.write(chunk));
  child.on("exit", () => logStream.end());
  return child;
}

async function maybeStartBackend() {
  if (await httpOk(BACKEND_HEALTH_URL)) {
    return { child: null, reused: true };
  }

  const pythonExe = path.join(ROOT, ".venv", "Scripts", "python.exe");
  if (!fs.existsSync(pythonExe)) {
    throw new Error("Missing .venv Python. Run scripts/bootstrap.ps1 first.");
  }

  const logPath = path.join(TMP_DIR, "capture_gold_sample_backend.log");
  const child = spawnLoggedProcess(
    pythonExe,
    ["-m", "uvicorn", "backend.app.main:app", "--host", "127.0.0.1", "--port", "8000"],
    {
      cwd: ROOT,
      env: {
        ...process.env,
        PYTHONPATH: ROOT,
        TEMP: TMP_DIR,
        TMP: TMP_DIR,
      },
      logPath,
    }
  );

  await waitFor(() => httpOk(BACKEND_HEALTH_URL), 30_000, "backend health");
  return { child, reused: false };
}

function contentTypeFor(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  switch (ext) {
    case ".html":
      return "text/html; charset=utf-8";
    case ".js":
      return "application/javascript; charset=utf-8";
    case ".css":
      return "text/css; charset=utf-8";
    case ".json":
      return "application/json; charset=utf-8";
    case ".svg":
      return "image/svg+xml";
    case ".png":
      return "image/png";
    case ".jpg":
    case ".jpeg":
      return "image/jpeg";
    case ".ico":
      return "image/x-icon";
    default:
      return "application/octet-stream";
  }
}

function collectRequestBody(request) {
  return new Promise((resolve, reject) => {
    const chunks = [];
    request.on("data", (chunk) => chunks.push(chunk));
    request.on("end", () => resolve(Buffer.concat(chunks)));
    request.on("error", reject);
  });
}

async function handleProxyRequest(request, response) {
  const body =
    request.method === "GET" || request.method === "HEAD" ? undefined : await collectRequestBody(request);

  const upstreamResponse = await fetch(`http://127.0.0.1:8000${request.url}`, {
    method: request.method,
    headers: Object.fromEntries(
      Object.entries(request.headers).filter(([key]) => key.toLowerCase() !== "host")
    ),
    body,
    redirect: "manual",
  });

  response.statusCode = upstreamResponse.status;
  upstreamResponse.headers.forEach((value, key) => {
    if (key.toLowerCase() === "content-encoding") {
      return;
    }
    response.setHeader(key, value);
  });

  if (typeof upstreamResponse.headers.getSetCookie === "function") {
    const cookies = upstreamResponse.headers.getSetCookie();
    if (cookies.length > 0) {
      response.setHeader("set-cookie", cookies);
    }
  }

  if (request.method === "HEAD") {
    response.end();
    return;
  }

  const buffer = Buffer.from(await upstreamResponse.arrayBuffer());
  response.end(buffer);
}

async function handleStaticRequest(request, response) {
  const requestPath = request.url === "/" ? "/index.html" : request.url.split("?")[0];
  const normalized = path.normalize(requestPath).replace(/^([/\\])+/, "");
  let filePath = path.join(FRONTEND_DIST_DIR, normalized);

  if (!filePath.startsWith(FRONTEND_DIST_DIR)) {
    response.statusCode = 403;
    response.end("Forbidden");
    return;
  }

  let targetPath = filePath;
  if (!fs.existsSync(targetPath) || fs.statSync(targetPath).isDirectory()) {
    targetPath = path.join(FRONTEND_DIST_DIR, "index.html");
  }

  const content = await fsp.readFile(targetPath);
  response.statusCode = 200;
  response.setHeader("content-type", contentTypeFor(targetPath));
  response.end(content);
}

async function maybeStartFrontendServer() {
  if (await httpOk(FRONTEND_URL)) {
    return { server: null, reused: true };
  }

  if (!fs.existsSync(path.join(FRONTEND_DIST_DIR, "index.html"))) {
    throw new Error("Missing frontend/dist. Run `npm run build` in frontend before capturing screenshots.");
  }

  const server = http.createServer(async (request, response) => {
    try {
      if (!request.url) {
        response.statusCode = 400;
        response.end("Bad Request");
        return;
      }

      if (request.url.startsWith("/api/")) {
        await handleProxyRequest(request, response);
        return;
      }

      await handleStaticRequest(request, response);
    } catch (error) {
      response.statusCode = 500;
      response.end(error instanceof Error ? error.message : "Internal Server Error");
    }
  });

  await new Promise((resolve, reject) => {
    server.once("error", reject);
    server.listen(5173, "127.0.0.1", resolve);
  });

  await waitFor(() => httpOk(FRONTEND_URL), 10_000, "static frontend server");
  return { server, reused: false };
}

class CdpClient {
  constructor(wsUrl) {
    this.ws = new WebSocket(wsUrl);
    this.nextId = 1;
    this.pending = new Map();
    this.isOpen = false;
    this.openPromise = new Promise((resolve, reject) => {
      this.ws.addEventListener("open", () => {
        this.isOpen = true;
        resolve();
      });
      this.ws.addEventListener("error", (error) => reject(error));
    });

    this.ws.addEventListener("message", (event) => {
      const payload = JSON.parse(event.data);
      if (!payload.id) {
        return;
      }
      const pending = this.pending.get(payload.id);
      if (!pending) {
        return;
      }
      this.pending.delete(payload.id);
      if (payload.error) {
        pending.reject(new Error(payload.error.message || "CDP error"));
        return;
      }
      pending.resolve(payload.result);
    });
  }

  async ready() {
    await this.openPromise;
  }

  async send(method, params = {}) {
    await this.ready();
    const id = this.nextId++;
    const message = JSON.stringify({ id, method, params });
    const promise = new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
    });
    this.ws.send(message);
    return promise;
  }

  async close() {
    if (!this.isOpen) {
      return;
    }
    this.ws.close();
    this.isOpen = false;
  }
}

async function startBrowser() {
  const browserPath = resolveBrowserPath();
  const userDataDir = path.join(TMP_DIR, `capture-gold-sample-browser-${Date.now()}`);
  await ensureDir(userDataDir);

  const child = spawn(browserPath, [
    "--headless=new",
    "--disable-gpu",
    "--no-first-run",
    "--no-default-browser-check",
    `--remote-debugging-port=${REMOTE_DEBUGGING_PORT}`,
    `--user-data-dir=${userDataDir}`,
    `--window-size=${WINDOW_WIDTH},${WINDOW_HEIGHT}`,
    "about:blank",
  ], {
    cwd: ROOT,
    stdio: "ignore",
    windowsHide: true,
  });

  await waitFor(async () => {
    try {
      const list = await fetchJson(`http://127.0.0.1:${REMOTE_DEBUGGING_PORT}/json/list`);
      return Array.isArray(list) && list.find((item) => item.type === "page");
    } catch {
      return null;
    }
  }, 15_000, "browser devtools endpoint");

  const targets = await fetchJson(`http://127.0.0.1:${REMOTE_DEBUGGING_PORT}/json/list`);
  const pageTarget = targets.find((item) => item.type === "page");
  if (!pageTarget?.webSocketDebuggerUrl) {
    throw new Error("Failed to find a page target for the browser.");
  }

  const cdp = new CdpClient(pageTarget.webSocketDebuggerUrl);
  await cdp.ready();
  await cdp.send("Page.enable");
  await cdp.send("Runtime.enable");
  await cdp.send("DOM.enable");
  await cdp.send("Network.enable");
  await cdp.send("Emulation.setDeviceMetricsOverride", {
    width: WINDOW_WIDTH,
    height: WINDOW_HEIGHT,
    deviceScaleFactor: 1,
    mobile: false,
  });

  return { child, cdp, userDataDir };
}

function jsString(value) {
  return JSON.stringify(value);
}

async function evaluate(cdp, expression) {
  const result = await cdp.send("Runtime.evaluate", {
    expression,
    awaitPromise: true,
    returnByValue: true,
  });
  return result.result ? result.result.value : undefined;
}

async function describePageState(cdp) {
  return evaluate(
    cdp,
    `(() => ({
      hasFileInput: Boolean(document.querySelector('[data-testid="file-input"]')),
      hasInviteInput: Boolean(document.querySelector('[data-testid="invite-code-input"]')),
      hasLoginButton: Boolean(document.querySelector('[data-testid="login-submit-button"]')),
      hasRetryButton: Array.from(document.querySelectorAll('button')).some((button) => (button.innerText || '').includes('重新进入演示')),
      authError: document.querySelector('[data-testid="auth-error"]')?.innerText?.trim() || '',
      notice: document.querySelector('[data-testid="auth-notice"]')?.innerText?.trim() || '',
      textSample: document.body ? document.body.innerText.slice(0, 500) : ''
    }))()`
  );
}

async function navigate(cdp, url) {
  await cdp.send("Page.navigate", { url });
  await waitFor(
    () =>
      evaluate(
        cdp,
        "document.readyState === 'complete' && !!document.querySelector('#root')"
      ),
    20_000,
    `page load: ${url}`
  );
  await sleep(1000);
}

async function clearBrowserState(cdp) {
  await cdp.send("Network.clearBrowserCookies");
  await evaluate(
    cdp,
    "localStorage.clear(); sessionStorage.clear(); true;"
  );
}

async function setInputValue(cdp, selector, value) {
  const ok = await evaluate(
    cdp,
    `(() => {
      const el = document.querySelector(${jsString(selector)});
      if (!el) return false;
      el.focus();
      const prototype =
        el.tagName === 'TEXTAREA'
          ? HTMLTextAreaElement.prototype
          : HTMLInputElement.prototype;
      const descriptor = Object.getOwnPropertyDescriptor(prototype, 'value');
      if (!descriptor || typeof descriptor.set !== 'function') {
        return false;
      }
      descriptor.set.call(el, ${jsString(value)});
      el.dispatchEvent(new Event('input', { bubbles: true }));
      el.dispatchEvent(new Event('change', { bubbles: true }));
      return true;
    })()`
  );
  if (!ok) {
    throw new Error(`Failed to set input value for selector: ${selector}`);
  }
}

async function clickSelector(cdp, selector) {
  const ok = await evaluate(
    cdp,
    `(() => {
      const el = document.querySelector(${jsString(selector)});
      if (!el) return false;
      el.scrollIntoView({ block: 'center', inline: 'center' });
      el.click();
      return true;
    })()`
  );
  if (!ok) {
    throw new Error(`Failed to click selector: ${selector}`);
  }
}

async function waitForSelector(cdp, selector, timeoutMs) {
  return waitFor(
    () => evaluate(cdp, `Boolean(document.querySelector(${jsString(selector)}))`),
    timeoutMs,
    `selector ${selector}`
  );
}

async function waitForEnabledSelector(cdp, selector, timeoutMs) {
  return waitFor(
    () =>
      evaluate(
        cdp,
        `(() => {
          const el = document.querySelector(${jsString(selector)});
          return Boolean(el && !el.disabled);
        })()`
      ),
    timeoutMs,
    `enabled selector ${selector}`
  );
}

async function waitForOutputChange(cdp, previousText, { requirePdfButton = null, timeoutMs = 90_000 } = {}) {
  return waitFor(async () => {
    const state = await evaluate(
      cdp,
      `(() => {
        const output = document.querySelector('[data-testid="result-output"]');
        const submit = document.querySelector('[data-testid="submit-task-button"]');
        const pdfButtons = document.querySelectorAll('[data-testid^="open-pdf-"]').length;
        return {
          outputText: output ? output.innerText.trim() : '',
          submitText: submit ? submit.innerText.trim() : '',
          pdfButtons
        };
      })()`
    );
    if (!state || !state.outputText || state.submitText !== "提交任务") {
      return null;
    }
    if (state.outputText === previousText) {
      return null;
    }
    if (requirePdfButton === true && state.pdfButtons === 0) {
      return null;
    }
    if (requirePdfButton === false && state.pdfButtons !== 0) {
      return null;
    }
    return state.outputText;
  }, timeoutMs, "task result");
}

async function getRootNodeId(cdp) {
  const documentRoot = await cdp.send("DOM.getDocument", { depth: 1 });
  return documentRoot.root.nodeId;
}

async function setFileInput(cdp, selector, filePath) {
  const rootNodeId = await getRootNodeId(cdp);
  const result = await cdp.send("DOM.querySelector", {
    nodeId: rootNodeId,
    selector,
  });
  if (!result.nodeId) {
    throw new Error(`Failed to locate file input: ${selector}`);
  }
  await cdp.send("DOM.setFileInputFiles", {
    nodeId: result.nodeId,
    files: [filePath],
  });
}

async function getElementRect(cdp, selector) {
  const rect = await evaluate(
    cdp,
    `(() => {
      const el = document.querySelector(${jsString(selector)});
      if (!el) return null;
      el.scrollIntoView({ block: 'start', inline: 'nearest' });
      const r = el.getBoundingClientRect();
      return {
        x: r.left + window.scrollX,
        y: r.top + window.scrollY,
        width: r.width,
        height: r.height
      };
    })()`
  );
  if (!rect || !rect.width || !rect.height) {
    throw new Error(`Failed to get element rect for selector: ${selector}`);
  }
  return rect;
}

async function captureElementScreenshot(cdp, selector, outputPath, padding = 16) {
  const rect = await getElementRect(cdp, selector);
  const clip = {
    x: Math.max(0, rect.x - padding),
    y: Math.max(0, rect.y - padding),
    width: rect.width + padding * 2,
    height: rect.height + padding * 2,
    scale: 1,
  };
  const screenshot = await cdp.send("Page.captureScreenshot", {
    format: "png",
    fromSurface: true,
    captureBeyondViewport: true,
    clip,
  });
  await fsp.writeFile(outputPath, Buffer.from(screenshot.data, "base64"));
}

async function ensureAuthenticated(cdp, inviteCode, demoMode) {
  const initialState = await waitFor(async () => {
    const state = await describePageState(cdp);
    if (state.hasFileInput || state.hasInviteInput || state.hasRetryButton) {
      return state;
    }
    return null;
  }, 30_000, "auth UI state");

  if (initialState.hasFileInput) {
    return;
  }

  if (demoMode) {
    if (initialState.hasRetryButton) {
      await clickSelector(cdp, "button.submit");
    }
    await waitForSelector(cdp, '[data-testid="file-input"]', 30_000);
    return;
  }

  if (!initialState.hasInviteInput) {
    throw new Error(`Invite-code login UI not found. Page state: ${JSON.stringify(initialState)}`);
  }

  await setInputValue(cdp, '[data-testid="invite-code-input"]', inviteCode);
  await setInputValue(cdp, '[data-testid="display-name-input"]', "Codex");
  await waitForEnabledSelector(cdp, '[data-testid="login-submit-button"]', 10_000);
  await clickSelector(cdp, '[data-testid="login-submit-button"]');

  const loginResult = await waitFor(async () => {
    const state = await describePageState(cdp);
    if (state.hasFileInput) {
      return { ok: true, state };
    }
    if (state.authError) {
      return { ok: false, state };
    }
    return null;
  }, 30_000, "post-login state");

  if (!loginResult.ok) {
    throw new Error(`Login failed. Page state: ${JSON.stringify(loginResult.state)}`);
  }
}

async function setTaskPrompt(cdp, prompt) {
  await clickSelector(cdp, '[data-testid="task-option-ask"]');
  await clickSelector(cdp, '[data-testid="detail-option-balanced"]');
  await setInputValue(cdp, '[data-testid="task-input"]', prompt);
}

async function runAskAndCapture(cdp, { prompt, screenshotPath, previousOutput, requirePdfButton }) {
  await setTaskPrompt(cdp, prompt);
  await waitForEnabledSelector(cdp, '[data-testid="submit-task-button"]', 10_000);
  await clickSelector(cdp, '[data-testid="submit-task-button"]');
  const nextOutput = await waitForOutputChange(cdp, previousOutput, { requirePdfButton });
  await captureElementScreenshot(cdp, '[data-testid="result-panel"]', screenshotPath);
  return nextOutput;
}

async function waitForPdfPreviewLoaded(cdp) {
  await waitForSelector(cdp, '[data-testid="pdf-preview-panel"]', 20_000);
  await waitFor(
    () =>
      evaluate(
        cdp,
        `(() => {
          const status = document.querySelector('[data-testid="pdf-preview-status"]');
          const frame = document.querySelector('[data-testid="pdf-preview-frame"]');
          if (!status || !frame) return false;
          const text = status.innerText || '';
          return frame.complete && text.includes('已定位到第');
        })()`
      ),
    30_000,
    "PDF preview load"
  );
}

async function main() {
  await ensureDir(TMP_DIR);
  await ensureDir(SCREENSHOT_DIR);

  if (!fs.existsSync(SAMPLE_PDF)) {
    throw new Error(`Sample PDF not found: ${SAMPLE_PDF}`);
  }

  const envValues = readEnvFile(path.join(ROOT, ".env"));
  const inviteCode = (envValues.ALPHA_INVITE_CODES || "alpha-demo").split(",")[0].trim();

  let backend = null;
  let frontend = null;
  let browser = null;

  const createdPaths = [];
  try {
    backend = await maybeStartBackend();
    frontend = await maybeStartFrontendServer();
    browser = await startBrowser();
    const healthPayload = await fetchJson(BACKEND_HEALTH_URL);
    const demoMode = Boolean(healthPayload.demo_mode);

    await navigate(browser.cdp, FRONTEND_URL);
    await clearBrowserState(browser.cdp);
    await navigate(browser.cdp, FRONTEND_URL);
    await ensureAuthenticated(browser.cdp, inviteCode, demoMode);

    await setFileInput(browser.cdp, '[data-testid="file-input"]', SAMPLE_PDF);

    const datePrefix = timestampDate();
    let previousOutput = "";

    const ask1Path = path.join(SCREENSHOT_DIR, `${datePrefix}_gold_ask_research_focus.png`);
    previousOutput = await runAskAndCapture(browser.cdp, {
      prompt: PROMPTS.askResearchFocus,
      screenshotPath: ask1Path,
      previousOutput,
      requirePdfButton: true,
    });
    createdPaths.push(ask1Path);

    await clickSelector(browser.cdp, '[data-testid^="open-pdf-"]');
    await waitForPdfPreviewLoaded(browser.cdp);
    const pdfPath = path.join(SCREENSHOT_DIR, `${datePrefix}_gold_pdf_render.png`);
    await captureElementScreenshot(browser.cdp, '[data-testid="pdf-preview-panel"]', pdfPath);
    createdPaths.push(pdfPath);

    const ask2Path = path.join(SCREENSHOT_DIR, `${datePrefix}_gold_ask_rank_accuracy.png`);
    previousOutput = await runAskAndCapture(browser.cdp, {
      prompt: PROMPTS.askRankAccuracy,
      screenshotPath: ask2Path,
      previousOutput,
      requirePdfButton: true,
    });
    createdPaths.push(ask2Path);

    const refusalPath = path.join(SCREENSHOT_DIR, `${datePrefix}_gold_refusal.png`);
    previousOutput = await runAskAndCapture(browser.cdp, {
      prompt: PROMPTS.refusal,
      screenshotPath: refusalPath,
      previousOutput,
      requirePdfButton: false,
    });
    createdPaths.push(refusalPath);

    console.log("Created screenshots:");
    for (const screenshotPath of createdPaths) {
      console.log(`- ${path.relative(ROOT, screenshotPath)}`);
    }
  } finally {
    if (browser) {
      await browser.cdp.close().catch(() => {});
      browser.child.kill();
      await fsp.rm(browser.userDataDir, { recursive: true, force: true }).catch(() => {});
    }
    if (frontend?.server) {
      await new Promise((resolve) => frontend.server.close(resolve));
    }
    if (backend?.child) {
      backend.child.kill();
    }
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack || error.message : error);
  process.exitCode = 1;
});
