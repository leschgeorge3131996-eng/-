import { useState } from "react";
import PdfViewer from "./PdfViewer";

type PdfPreviewPanelProps = {
  documentName: string;
  fileId: string;
  accessToken?: string | null;
  page: number;
  availablePages?: number[];
  src: string;
  highlightText?: string | null;
  onSelectPage?: (page: number) => void;
  onClose: () => void;
};

export default function PdfPreviewPanel({
  documentName,
  page,
  availablePages = [],
  src,
  highlightText,
  onSelectPage,
  onClose
}: PdfPreviewPanelProps) {
  const [loadError, setLoadError] = useState<string | null>(null);

  return (
    <section className="panel pdf-preview-panel" data-testid="pdf-preview-panel">
      <div className="pdf-preview-head">
        <div>
          <p className="section-kicker">PDF 预览</p>
          <h2 className="panel-title">{documentName}</h2>
        </div>
        <div className="pdf-preview-actions">
          <span className="pdf-page-chip">第 {page} 页</span>
          {highlightText ? (
            <span
              className="pdf-highlight-chip"
              title={highlightText}
              aria-label="已在 PDF 中高亮证据片段"
            >
              已在 PDF 中高亮证据
            </span>
          ) : null}
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

      <div className="pdf-preview-body">
        <div className="pdf-frame-wrap">
          {loadError ? (
            <p className="error status-card">{loadError}</p>
          ) : (
            <PdfViewer
              src={src}
              page={page}
              highlightText={highlightText}
              onError={setLoadError}
            />
          )}
        </div>
      </div>
    </section>
  );
}
