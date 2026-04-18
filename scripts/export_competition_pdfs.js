const fs = require("fs");
const fsp = require("fs/promises");
const path = require("path");
const { spawn } = require("child_process");

const ROOT = path.resolve(__dirname, "..");
const TMP_DIR = path.join(ROOT, "tmp");
const REMOTE_DEBUGGING_PORT = 9333;
const WINDOW_WIDTH = 1600;
const WINDOW_HEIGHT = 1200;

const JOBS = [
  {
    inputPath: path.join(ROOT, "deliverables", "competition_kit", "deck.html"),
    outputPath: path.join(ROOT, "deliverables", "competition_kit", "deck.pdf"),
    paperWidth: 16,
    paperHeight: 9,
    waitSelector: ".slide",
  },
  {
    inputPath: path.join(ROOT, "deliverables", "competition_kit", "poster.html"),
    outputPath: path.join(ROOT, "deliverables", "competition_kit", "poster.pdf"),
    paperWidth: 23.39,
    paperHeight: 33.11,
    waitSelector: ".poster",
  },
];

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function ensureDir(dirPath) {
  await fsp.mkdir(dirPath, { recursive: true });
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
    await sleep(300);
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
    const promise = new Promise((resolve, reject) => {
      this.pending.set(id, { resolve, reject });
    });
    this.ws.send(JSON.stringify({ id, method, params }));
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
  const userDataDir = path.join(TMP_DIR, `competition-pdf-browser-${Date.now()}`);
  await ensureDir(userDataDir);

  const child = spawn(
    browserPath,
    [
      "--headless=new",
      "--disable-gpu",
      "--no-first-run",
      "--no-default-browser-check",
      `--remote-debugging-port=${REMOTE_DEBUGGING_PORT}`,
      `--user-data-dir=${userDataDir}`,
      `--window-size=${WINDOW_WIDTH},${WINDOW_HEIGHT}`,
      "about:blank",
    ],
    {
      cwd: ROOT,
      stdio: "ignore",
      windowsHide: true,
    }
  );

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
  await cdp.send("Emulation.setDeviceMetricsOverride", {
    width: WINDOW_WIDTH,
    height: WINDOW_HEIGHT,
    deviceScaleFactor: 1,
    mobile: false,
  });

  return { child, cdp, userDataDir };
}

async function evaluate(cdp, expression) {
  const result = await cdp.send("Runtime.evaluate", {
    expression,
    awaitPromise: true,
    returnByValue: true,
  });
  return result.result?.value;
}

function toFileUrl(filePath) {
  const normalized = filePath.replace(/\\/g, "/");
  return `file:///${normalized}`;
}

async function waitForPageReady(cdp, selector) {
  await waitFor(
    () =>
      evaluate(
        cdp,
        `(() => {
          const root = document.querySelector(${JSON.stringify(selector)});
          return document.readyState === "complete"
            && Boolean(root)
            && Array.from(document.images).every((image) => image.complete);
        })()`
      ),
    20_000,
    `page ready for ${selector}`
  );
}

async function exportPdf(cdp, job) {
  await cdp.send("Page.navigate", { url: toFileUrl(job.inputPath) });
  await waitForPageReady(cdp, job.waitSelector);
  await sleep(600);

  const pdf = await cdp.send("Page.printToPDF", {
    printBackground: true,
    paperWidth: job.paperWidth,
    paperHeight: job.paperHeight,
    marginTop: 0,
    marginBottom: 0,
    marginLeft: 0,
    marginRight: 0,
    preferCSSPageSize: true,
  });

  await fsp.writeFile(job.outputPath, Buffer.from(pdf.data, "base64"));
}

async function main() {
  await ensureDir(TMP_DIR);
  for (const job of JOBS) {
    if (!fs.existsSync(job.inputPath)) {
      throw new Error(`Missing input file: ${job.inputPath}`);
    }
  }

  let browser = null;
  try {
    browser = await startBrowser();
    for (const job of JOBS) {
      await exportPdf(browser.cdp, job);
      console.log(`Created ${path.relative(ROOT, job.outputPath)}`);
    }
  } finally {
    if (browser) {
      await browser.cdp.close().catch(() => {});
      browser.child.kill();
      await fsp.rm(browser.userDataDir, { recursive: true, force: true }).catch(() => {});
    }
  }
}

main().catch((error) => {
  console.error(error instanceof Error ? error.stack || error.message : error);
  process.exitCode = 1;
});
