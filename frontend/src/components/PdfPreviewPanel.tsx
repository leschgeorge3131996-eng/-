import { useEffect, useLayoutEffect, useMemo, useRef, useState } from "react";
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
  const imageWrapRef = useRef<HTMLDivElement | null>(null);

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
      const rect = element.getBoundingClientRect();
      setRenderedSize({ width: rect.width, height: rect.height });
    };

    updateSize();
    const observer = new ResizeObserver(updateSize);
    observer.observe(element);
    return () => observer.disconnect();
  }, [imageLoaded]);

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

  const hasBboxHighlights = overlayRects.length > 0;
  const statusLabel = imageError
    ? imageError
    : !imageLoaded
      ? "正在加载 PDF 页面..."
      : hasBboxHighlights
        ? `已定位到第 ${page} 页 · 段落已高亮`
        : `已定位到第 ${page} 页`;

  return (
    <section className="panel pdf-preview-panel" data-testid="pdf-preview-panel">
      <div className="pdf-preview-head">
        <div>
          <p className="section-kicker">PDF 预览</p>
          <h2 className="panel-title">{documentName}</h2>
        </div>
        <div className="pdf-preview-actions">
          <span className="pdf-page-chip">第 {page} 页</span>
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
        <div className="pdf-render-inner" ref={imageWrapRef}>
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
          {hasBboxHighlights ? (
            <div
              className="pdf-highlight-layer"
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
        </div>
      </div>
    </section>
  );
}
