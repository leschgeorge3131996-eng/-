import { useEffect, useLayoutEffect, useMemo, useRef, useState, type PointerEvent } from "react";
import { PDF_PAGE_RENDER_DPI, buildPdfPageRenderUrl, fetchDocumentPage } from "../api";
import type { BBoxRegion } from "../types";

type PdfPreviewPanelProps = {
  documentName: string;
  fileId: string;
  accessToken?: string | null;
  page: number;
  availablePages?: number[];
  highlightText?: string | null;
  bboxRegions?: BBoxRegion[];
  onSelectPage?: (page: number) => void;
  onClose: () => void;
};

type PageDimensions = {
  width: number;
  height: number;
};

type ManualHighlight = {
  id: string;
  page: number;
  rects: HighlightRect[];
  color: HighlightColor;
};

type Point = {
  xPct: number;
  yPct: number;
};

type HighlightRect = {
  leftPct: number;
  topPct: number;
  widthPct: number;
  heightPct: number;
};

const ZOOM_LEVELS = [0.7, 0.9, 1, 1.25, 1.5, 1.8, 2.2];

type HighlightColor = "yellow" | "green" | "blue" | "pink";

const HIGHLIGHT_COLORS: Array<{ value: HighlightColor; label: string; fill: string; draft: string }> = [
  { value: "yellow", label: "黄", fill: "rgba(255, 214, 79, 0.34)", draft: "rgba(255, 214, 79, 0.22)" },
  { value: "green", label: "绿", fill: "rgba(91, 203, 142, 0.28)", draft: "rgba(91, 203, 142, 0.18)" },
  { value: "blue", label: "蓝", fill: "rgba(91, 157, 238, 0.24)", draft: "rgba(91, 157, 238, 0.16)" },
  { value: "pink", label: "粉", fill: "rgba(241, 114, 168, 0.24)", draft: "rgba(241, 114, 168, 0.16)" }
];
function clamp(value: number, min: number, max: number): number {
  return Math.min(max, Math.max(min, value));
}

function escapeHtml(value: string): string {
  return value
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#39;");
}

function resolveDimensions(
  fromApi: PageDimensions | null,
  naturalWidth: number,
  naturalHeight: number
): PageDimensions | null {
  if (fromApi && fromApi.width > 0 && fromApi.height > 0) {
    return fromApi;
  }
  if (naturalWidth > 0 && naturalHeight > 0) {
    const scale = 72 / PDF_PAGE_RENDER_DPI;
    return {
      width: naturalWidth * scale,
      height: naturalHeight * scale
    };
  }
  return null;
}

export default function PdfPreviewPanel({
  documentName,
  fileId,
  accessToken,
  page,
  availablePages = [],
  highlightText,
  bboxRegions = [],
  onSelectPage,
  onClose
}: PdfPreviewPanelProps) {
  const [pageDimensions, setPageDimensions] = useState<PageDimensions | null>(null);
  const [pageError, setPageError] = useState<string | null>(null);
  const [imageLoaded, setImageLoaded] = useState(false);
  const [imageError, setImageError] = useState<string | null>(null);
  const [renderedSize, setRenderedSize] = useState<{ width: number; height: number } | null>(null);
  const [naturalSize, setNaturalSize] = useState<{ width: number; height: number } | null>(null);
  const [manualMode, setManualMode] = useState(false);
  const [manualHighlights, setManualHighlights] = useState<ManualHighlight[]>([]);
  const [draftHighlight, setDraftHighlight] = useState<ManualHighlight | null>(null);
  const [highlightColor, setHighlightColor] = useState<HighlightColor>("yellow");
  const [zoomIndex, setZoomIndex] = useState(3);
  const imageWrapRef = useRef<HTMLDivElement | null>(null);
  const dragStartRef = useRef<Point | null>(null);
  const zoom = ZOOM_LEVELS[zoomIndex];

  const imageUrl = useMemo(
    () => buildPdfPageRenderUrl(fileId, page, accessToken),
    [fileId, page, accessToken]
  );

  useEffect(() => {
    let active = true;
    setPageError(null);
    setPageDimensions(null);

    void fetchDocumentPage(fileId, page, accessToken)
      .then((payload) => {
        if (!active) {
          return;
        }
        if (payload.width && payload.height) {
          setPageDimensions({ width: payload.width, height: payload.height });
        } else {
          setPageDimensions(null);
        }
      })
      .catch((error) => {
        if (!active) {
          return;
        }
        setPageError(error instanceof Error ? error.message : "页面元数据加载失败");
      });

    return () => {
      active = false;
    };
  }, [accessToken, fileId, page]);

  useEffect(() => {
    setImageLoaded(false);
    setImageError(null);
  }, [imageUrl]);

  useLayoutEffect(() => {
    if (!imageLoaded || !imageWrapRef.current) {
      return undefined;
    }

    const element = imageWrapRef.current;
    const updateSize = () => {
      const image = element.querySelector("img");
      const rect = image?.getBoundingClientRect() ?? element.getBoundingClientRect();
      setRenderedSize({ width: rect.width, height: rect.height });
    };

    updateSize();
    const observer = new ResizeObserver(updateSize);
    observer.observe(element);
    return () => observer.disconnect();
  }, [imageLoaded, zoom]);

  const nativeDimensions = resolveDimensions(
    pageDimensions,
    naturalSize?.width ?? 0,
    naturalSize?.height ?? 0
  );

  const overlayRects = useMemo(() => {
    if (!nativeDimensions || !renderedSize || renderedSize.width === 0) {
      return [];
    }
    const scaleX = renderedSize.width / nativeDimensions.width;
    const scaleY = renderedSize.height / nativeDimensions.height;
    return bboxRegions
      .filter((region) => region.page === page)
      .map((region, index) => ({
        key: `${region.x0}-${region.y0}-${index}`,
        left: region.x0 * scaleX,
        top: region.y0 * scaleY,
        width: Math.max(0, (region.x1 - region.x0) * scaleX),
        height: Math.max(0, (region.y1 - region.y0) * scaleY)
      }));
  }, [bboxRegions, nativeDimensions, page, renderedSize]);

  const pageManualHighlights = manualHighlights.filter((highlight) => highlight.page === page);
  const hasManualHighlights = pageManualHighlights.length > 0 || Boolean(draftHighlight);
  const hasAutoHighlights = overlayRects.length > 0;
  const statusLabel = imageError
    ? imageError
    : !imageLoaded
      ? "正在加载 PDF 页面..."
      : hasAutoHighlights && hasManualHighlights
        ? `已定位到第 ${page} 页 · 证据与手动高亮已显示`
        : hasAutoHighlights
          ? `已定位到第 ${page} 页 · 原文证据已高亮`
          : hasManualHighlights
            ? `已定位到第 ${page} 页 · 可导出手动高亮`
            : `已定位到第 ${page} 页`;

  function getImagePoint(event: PointerEvent<HTMLDivElement>): Point | null {
    const image = imageWrapRef.current?.querySelector("img");
    if (!image) {
      return null;
    }
    const rect = image.getBoundingClientRect();
    if (rect.width <= 0 || rect.height <= 0) {
      return null;
    }
    return {
      xPct: clamp(((event.clientX - rect.left) / rect.width) * 100, 0, 100),
      yPct: clamp(((event.clientY - rect.top) / rect.height) * 100, 0, 100)
    };
  }

  function buildHighlightRect(start: Point, end: Point): HighlightRect {
    const leftPct = Math.min(start.xPct, end.xPct);
    const topPct = Math.min(start.yPct, end.yPct);
    return {
      leftPct,
      topPct,
      widthPct: Math.abs(end.xPct - start.xPct),
      heightPct: Math.abs(end.yPct - start.yPct)
    };
  }

  function getHighlightFill(value: HighlightColor, draft = false): string {
    const color = HIGHLIGHT_COLORS.find((item) => item.value === value) ?? HIGHLIGHT_COLORS[0];
    return draft ? color.draft : color.fill;
  }

  function handlePointerDown(event: PointerEvent<HTMLDivElement>) {
    if (!manualMode || !imageLoaded) {
      return;
    }
    const point = getImagePoint(event);
    if (!point) {
      return;
    }
    event.preventDefault();
    event.currentTarget.setPointerCapture(event.pointerId);
    dragStartRef.current = point;
    setDraftHighlight({
      id: `draft-${page}`,
      page,
      rects: [buildHighlightRect(point, point)],
      color: highlightColor
    });
  }

  function handlePointerMove(event: PointerEvent<HTMLDivElement>) {
    if (!manualMode || !dragStartRef.current) {
      return;
    }
    const point = getImagePoint(event);
    if (!point) {
      return;
    }
    event.preventDefault();
    setDraftHighlight((current) => {
      const rect = buildHighlightRect(dragStartRef.current!, point);
      if (!current) {
        return {
          id: `draft-${page}`,
          page,
          rects: [rect],
          color: highlightColor
        };
      }
      return { ...current, rects: [rect] };
    });
  }

  function handlePointerEnd(event: PointerEvent<HTMLDivElement>) {
    if (!manualMode || !dragStartRef.current) {
      return;
    }
    const point = getImagePoint(event);
    const start = dragStartRef.current;
    dragStartRef.current = null;
    setDraftHighlight(null);
    if (!point) {
      return;
    }
    const next = {
      id: `${page}-${Date.now()}`,
      page,
      rects: [buildHighlightRect(start, point)],
      color: draftHighlight?.color ?? highlightColor
    };
    const rect = next.rects[0];
    if (rect.widthPct < 0.8 || rect.heightPct < 0.35) {
      return;
    }
    setManualHighlights((current) => [...current, next]);
  }

  function zoomOut() {
    setZoomIndex((current) => Math.max(0, current - 1));
  }

  function zoomIn() {
    setZoomIndex((current) => Math.min(ZOOM_LEVELS.length - 1, current + 1));
  }

  function resetZoom() {
    setZoomIndex(3);
  }

  function clearCurrentPageHighlights() {
    setManualHighlights((current) => current.filter((highlight) => highlight.page !== page));
    setDraftHighlight(null);
    dragStartRef.current = null;
  }

  function exportAnnotatedPage() {
    const exportWindow = window.open("", "_blank");
    if (!exportWindow) {
      setImageError("浏览器阻止了导出窗口，请允许弹窗后重试。");
      return;
    }

    const highlightMarkup = pageManualHighlights
      .flatMap((highlight) =>
        highlight.rects.map(
          (rect) => `
          <rect class="manual-highlight" x="${rect.leftPct}" y="${rect.topPct}" width="${rect.widthPct}" height="${rect.heightPct}" rx="0.7" ry="0.7" style="fill:${getHighlightFill(highlight.color)};"></rect>`
        )
      )
      .join("");

    exportWindow.document.write(`
      <!doctype html>
      <html>
        <head>
          <meta charset="utf-8" />
          <title>${escapeHtml(documentName)} - 第 ${page} 页标注</title>
          <style>
            @page { margin: 12mm; }
            * { box-sizing: border-box; }
            body {
              margin: 0;
              font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
              color: #132238;
              background: white;
            }
            header {
              margin-bottom: 10px;
              font-size: 12px;
              color: #556273;
              display: flex;
              justify-content: space-between;
              gap: 16px;
            }
            .page {
              position: relative;
              width: 100%;
              max-width: 920px;
              margin: 0 auto;
              border: 1px solid #d8dde5;
            }
            img {
              display: block;
              width: 100%;
              height: auto;
            }
            .manual-layer {
              position: absolute;
              inset: 0;
              width: 100%;
              height: 100%;
              pointer-events: none;
            }
            .manual-highlight {
              fill: rgba(255, 214, 79, 0.34);
              stroke: none;
              mix-blend-mode: multiply;
            }
          </style>
        </head>
        <body>
          <header>
            <strong>${escapeHtml(documentName)}</strong>
            <span>第 ${page} 页 · 手动高亮</span>
          </header>
          <main class="page">
            <img src="${escapeHtml(imageUrl)}" alt="${escapeHtml(documentName)} 第 ${page} 页" />
            <svg class="manual-layer" viewBox="0 0 100 100" preserveAspectRatio="none">${highlightMarkup}</svg>
          </main>
          <script>
            const img = document.querySelector("img");
            const done = () => setTimeout(() => window.print(), 120);
            if (img.complete) done();
            else img.addEventListener("load", done, { once: true });
          </script>
        </body>
      </html>
    `);
    exportWindow.document.close();
  }

  return (
    <section className="panel pdf-preview-panel" data-testid="pdf-preview-panel">
      <div className="pdf-preview-head">
        <div>
          <p className="section-kicker">PDF 预览</p>
          <h2 className="panel-title">{documentName}</h2>
        </div>
        <div className="pdf-preview-actions">
          <span className="pdf-page-chip">第 {page} 页</span>
          <div className="pdf-zoom-controls" aria-label="PDF 缩放">
            <button
              className="ghost-button pdf-tool-button"
              type="button"
              disabled={zoomIndex === 0}
              onClick={zoomOut}
            >
              缩小
            </button>
            <button
              className="ghost-button pdf-tool-button pdf-zoom-value"
              type="button"
              onClick={resetZoom}
              aria-label={`当前缩放 ${Math.round(zoom * 100)}%，点击重置`}
            >
              {Math.round(zoom * 100)}%
            </button>
            <button
              className="ghost-button pdf-tool-button"
              type="button"
              disabled={zoomIndex === ZOOM_LEVELS.length - 1}
              onClick={zoomIn}
            >
              放大
            </button>
          </div>
          <button
            className={`ghost-button pdf-tool-button${manualMode ? " active" : ""}`}
            type="button"
            onClick={() => setManualMode((current) => !current)}
          >
            {manualMode ? "退出高亮" : "手动高亮"}
          </button>
          {manualMode ? (
            <div className="pdf-highlight-tools" aria-label="高亮样式">
              <div className="pdf-highlight-swatches">
                {HIGHLIGHT_COLORS.map((color) => (
                  <button
                    key={color.value}
                    className={`pdf-swatch${highlightColor === color.value ? " active" : ""}`}
                    type="button"
                    aria-label={`${color.label}色高亮`}
                    aria-pressed={highlightColor === color.value}
                    style={{ ["--swatch-color" as string]: color.fill }}
                    onClick={() => setHighlightColor(color.value)}
                  >
                    <span>{color.label}</span>
                  </button>
                ))}
              </div>
            </div>
          ) : null}
          <button
            className="ghost-button pdf-tool-button"
            type="button"
            disabled={!hasManualHighlights}
            onClick={clearCurrentPageHighlights}
          >
            清除本页
          </button>
          <button
            className="ghost-button pdf-tool-button"
            type="button"
            disabled={!imageLoaded || !hasManualHighlights}
            onClick={exportAnnotatedPage}
          >
            导出高亮
          </button>
          <button className="ghost-button" type="button" onClick={onClose}>
            关闭预览
          </button>
        </div>
      </div>

      {availablePages.length > 1 ? (
        <div className="pdf-page-tabs" aria-label="证据页切换">
          {availablePages.map((candidatePage) => (
            <button
              key={candidatePage}
              data-testid={`pdf-page-button-${candidatePage}`}
              className={`pdf-page-button${candidatePage === page ? " active" : ""}`}
              type="button"
              onClick={() => onSelectPage?.(candidatePage)}
            >
              第 {candidatePage} 页
            </button>
          ))}
        </div>
      ) : null}

      <div className="pdf-preview-status" data-testid="pdf-preview-status">
        {statusLabel}
        {pageError ? <span className="warning"> · {pageError}</span> : null}
      </div>

      {highlightText ? (
        <div className="pdf-evidence-snippet" data-testid="pdf-evidence-snippet">
          <span className="snippet-kicker">证据片段</span>
          <blockquote>{highlightText}</blockquote>
        </div>
      ) : null}

      <div className="pdf-render-wrap">
        <div
          className={`pdf-render-inner${manualMode ? " manual-highlight-mode" : ""}`}
          ref={imageWrapRef}
          style={{ ["--pdf-zoom" as string]: zoom }}
          onPointerDown={handlePointerDown}
          onPointerMove={handlePointerMove}
          onPointerUp={handlePointerEnd}
          onPointerCancel={handlePointerEnd}
        >
          <img
            key={imageUrl}
            className="pdf-render-image"
            data-testid="pdf-preview-frame"
            src={imageUrl}
            alt={`${documentName} 第 ${page} 页`}
            onLoad={(event) => {
              const img = event.currentTarget;
              setNaturalSize({ width: img.naturalWidth, height: img.naturalHeight });
              setImageLoaded(true);
              setImageError(null);
            }}
            onError={() => {
              setImageError("PDF 页面图像加载失败，请检查网络或登录状态。");
              setImageLoaded(false);
            }}
          />
          {overlayRects.length > 0 ? (
            <div
              className="pdf-highlight-layer auto-highlight-layer"
              data-testid="pdf-highlight-layer"
              aria-hidden="true"
            >
              {overlayRects.map((rect) => (
                <span
                  key={rect.key}
                  className="pdf-highlight-rect"
                  style={{
                    left: `${rect.left}px`,
                    top: `${rect.top}px`,
                    width: `${rect.width}px`,
                    height: `${rect.height}px`
                  }}
                />
              ))}
            </div>
          ) : null}
          {hasManualHighlights ? (
            <div className="pdf-highlight-layer manual-highlight-layer" aria-hidden="true">
              {[...pageManualHighlights, ...(draftHighlight ? [draftHighlight] : [])].map((highlight) => (
                <svg
                  key={highlight.id}
                  className={`pdf-manual-highlight${highlight.id.startsWith("draft-") ? " draft" : ""}`}
                  viewBox="0 0 100 100"
                  preserveAspectRatio="none"
                >
                  {highlight.rects.map((rect, index) => (
                    <rect
                      key={`${highlight.id}-${index}`}
                      x={rect.leftPct}
                      y={rect.topPct}
                      width={rect.widthPct}
                      height={rect.heightPct}
                      rx={0.7}
                      ry={0.7}
                      style={{ fill: getHighlightFill(highlight.color, highlight.id.startsWith("draft-")) }}
                    />
                  ))}
                </svg>
              ))}
            </div>
          ) : null}
        </div>
      </div>
    </section>
  );
}
