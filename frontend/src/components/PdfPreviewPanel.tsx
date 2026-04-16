import { useEffect, useMemo, useState } from "react";
import { fetchDocumentPage } from "../api";

type PdfPreviewPanelProps = {
  documentName: string;
  fileId: string;
  page: number;
  src: string;
  highlightText?: string | null;
  onClose: () => void;
};

type HighlightRange = {
  start: number;
  end: number;
};

function buildCollapsedTextMap(text: string) {
  const chars: string[] = [];
  const map: number[] = [];

  for (let index = 0; index < text.length; index += 1) {
    const char = text[index];
    if (/\s/.test(char)) {
      continue;
    }
    chars.push(char.toLowerCase());
    map.push(index);
  }

  return {
    collapsed: chars.join(""),
    map
  };
}

function locateHighlightRange(text: string, snippet: string | null | undefined): HighlightRange | null {
  if (!snippet) {
    return null;
  }

  const cleanSnippet = snippet.replace(/\.\.\./g, " ").trim();
  if (!cleanSnippet) {
    return null;
  }

  const source = buildCollapsedTextMap(text);
  const snippetMap = buildCollapsedTextMap(cleanSnippet);
  const exactIndex = source.collapsed.indexOf(snippetMap.collapsed);
  if (exactIndex !== -1) {
    const start = source.map[exactIndex];
    const end = source.map[exactIndex + snippetMap.collapsed.length - 1] + 1;
    return { start, end };
  }

  const fragmentCandidates = cleanSnippet
    .split(/[，。；：,.!?、\n]/)
    .map((item) => item.trim())
    .filter((item) => item.length >= 10)
    .sort((left, right) => right.length - left.length);

  for (const fragment of fragmentCandidates) {
    const collapsedFragment = buildCollapsedTextMap(fragment).collapsed;
    const fragmentIndex = source.collapsed.indexOf(collapsedFragment);
    if (fragmentIndex !== -1) {
      const start = source.map[fragmentIndex];
      const end = source.map[fragmentIndex + collapsedFragment.length - 1] + 1;
      return { start, end };
    }
  }

  return null;
}

export default function PdfPreviewPanel({
  documentName,
  fileId,
  page,
  src,
  highlightText,
  onClose
}: PdfPreviewPanelProps) {
  const [pageText, setPageText] = useState("");
  const [textLoading, setTextLoading] = useState(false);
  const [textError, setTextError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    setTextLoading(true);
    setTextError(null);

    void fetchDocumentPage(fileId, page)
      .then((payload) => {
        if (!active) {
          return;
        }
        setPageText(payload.text);
      })
      .catch((error) => {
        if (!active) {
          return;
        }
        setTextError(error instanceof Error ? error.message : "页面文本加载失败");
        setPageText("");
      })
      .finally(() => {
        if (active) {
          setTextLoading(false);
        }
      });

    return () => {
      active = false;
    };
  }, [fileId, page]);

  const highlightRange = useMemo(
    () => locateHighlightRange(pageText, highlightText),
    [pageText, highlightText]
  );

  return (
    <section className="panel pdf-preview-panel">
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

      <div className="pdf-preview-body">
        <div className="pdf-frame-wrap">
          <iframe className="pdf-frame" src={src} title={`${documentName} PDF 预览`} />
        </div>

        <aside className="page-text-panel">
          <div className="page-text-head">
            <strong>页面文本定位</strong>
            <span>{highlightRange ? "已近似高亮匹配片段" : "未命中时显示整页文本"}</span>
          </div>

          {textLoading ? <p className="status-card">正在加载第 {page} 页文本...</p> : null}
          {!textLoading && textError ? <p className="error status-card">{textError}</p> : null}
          {!textLoading && !textError ? (
            <div className="page-text-content">
              {highlightRange ? (
                <p className="page-text-block">
                  {pageText.slice(0, highlightRange.start)}
                  <mark className="page-text-highlight">
                    {pageText.slice(highlightRange.start, highlightRange.end)}
                  </mark>
                  {pageText.slice(highlightRange.end)}
                </p>
              ) : (
                <p className="page-text-block">{pageText || "当前页暂无可用文本。"}</p>
              )}
            </div>
          ) : null}
        </aside>
      </div>
    </section>
  );
}
