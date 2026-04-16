import { useEffect, useMemo, useState } from "react";
import { fetchDocumentPage } from "../api";
import type { PdfPreviewMatchState } from "../types";

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

type HighlightRange = {
  start: number;
  end: number;
  matchState: Extract<PdfPreviewMatchState, "exact_match" | "fragment_match">;
};

type SentenceView = {
  focusBefore: string;
  focus: string;
  focusAfter: string;
  matchState: PdfPreviewMatchState;
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
  if (!snippetMap.collapsed) {
    return null;
  }
  const exactIndex = source.collapsed.indexOf(snippetMap.collapsed);
  if (exactIndex !== -1) {
    const start = source.map[exactIndex];
    const end = source.map[exactIndex + snippetMap.collapsed.length - 1] + 1;
    return { start, end, matchState: "exact_match" };
  }

  const fragmentCandidates = cleanSnippet
    .split(/[，。；：,.!?\n]/)
    .map((item) => item.trim())
    .filter((item) => item.length >= 8)
    .sort((left, right) => right.length - left.length);

  for (const fragment of fragmentCandidates) {
    const collapsedFragment = buildCollapsedTextMap(fragment).collapsed;
    const fragmentIndex = source.collapsed.indexOf(collapsedFragment);
    if (fragmentIndex !== -1) {
      const start = source.map[fragmentIndex];
      const end = source.map[fragmentIndex + collapsedFragment.length - 1] + 1;
      return { start, end, matchState: "fragment_match" };
    }
  }

  return null;
}

function looksLikeArtifactLine(line: string): boolean {
  const normalized = line.replace(/\s+/g, "").toLowerCase();
  if (!normalized) {
    return true;
  }

  if (/@mail|@gmail|@outlook|creativecommons|ccl24|eval/i.test(normalized)) {
    return true;
  }

  if (/(大学|学院|实验室|研究所|通讯作者|作者简介|基金项目)/.test(line) && /\d{5,}/.test(line)) {
    return true;
  }

  if (/^(摘要|abstract)\s*[:：]?\s*$/i.test(line.trim())) {
    return true;
  }

  if (/^(关键词|keywords?)\s*[:：]/i.test(line.trim())) {
    return true;
  }

  if (/spatial semantics|large language model|prompt engineering/i.test(line)) {
    return true;
  }

  const digitCount = Array.from(line).filter((char) => /\d/.test(char)).length;
  const cjkCount = Array.from(line).filter((char) => /[\u4e00-\u9fff]/.test(char)).length;
  if (digitCount >= 8 && cjkCount <= 6) {
    return true;
  }

  return false;
}

function normalizeLine(line: string): string {
  return line
    .replace(/\x00/g, " ")
    .replace(/(?<=[\u4e00-\u9fff])\s+(?=[\u4e00-\u9fff])/g, "")
    .replace(/([\u4e00-\u9fff])\1{2,}/g, "$1")
    .replace(/\s+/g, " ")
    .trim();
}

function extractDisplaySentences(text: string): string[] {
  const cleanedLines = text
    .split(/\r?\n/)
    .map((line) => normalizeLine(line))
    .filter((line) => line && !looksLikeArtifactLine(line));

  const merged = cleanedLines.join(" ");
  return merged
    .split(/(?<=[。！？!?])\s+|\n+/)
    .map((item) => item.trim())
    .filter((item) => item.length >= 4);
}

function buildFallbackText(sentences: string[]): string {
  return sentences.slice(0, 3).join(" ").trim();
}

function buildSentenceView(sentences: string[], snippet: string | null | undefined): SentenceView | null {
  if (sentences.length === 0) {
    return null;
  }

  if (!snippet) {
    return {
      focusBefore: buildFallbackText(sentences),
      focus: "",
      focusAfter: "",
      matchState: "no_snippet"
    };
  }

  for (const sentence of sentences) {
    const range = locateHighlightRange(sentence, snippet);
    if (!range) {
      continue;
    }

    return {
      focusBefore: sentence.slice(0, range.start),
      focus: sentence.slice(range.start, range.end),
      focusAfter: sentence.slice(range.end),
      matchState: range.matchState
    };
  }

  return {
    focusBefore: buildFallbackText(sentences),
    focus: "",
    focusAfter: "",
    matchState: "not_found"
  };
}

function describeMatchState(matchState: PdfPreviewMatchState): string {
  if (matchState === "exact_match") {
    return "已在当前页定位到证据原句";
  }
  if (matchState === "fragment_match") {
    return "已在当前页定位到证据片段";
  }
  if (matchState === "not_found") {
    return "未在当前页精确定位到该片段，仅展示本页清洗文本";
  }
  return "当前页未提供独立定位片段，仅展示本页清洗文本";
}

export default function PdfPreviewPanel({
  documentName,
  fileId,
  accessToken,
  page,
  availablePages = [],
  src,
  highlightText,
  onSelectPage,
  onClose
}: PdfPreviewPanelProps) {
  const [pageText, setPageText] = useState("");
  const [textLoading, setTextLoading] = useState(false);
  const [textError, setTextError] = useState<string | null>(null);

  useEffect(() => {
    let active = true;
    setTextLoading(true);
    setTextError(null);

    void fetchDocumentPage(fileId, page, accessToken)
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
  }, [accessToken, fileId, page]);

  const sentenceView = useMemo(
    () => buildSentenceView(extractDisplaySentences(pageText), highlightText),
    [pageText, highlightText]
  );
  const matchState = sentenceView?.matchState ?? "no_snippet";

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

      <div className="pdf-preview-body">
        <div className="pdf-frame-wrap">
          <iframe
            className="pdf-frame"
            data-testid="pdf-preview-frame"
            src={src}
            title={`${documentName} PDF 预览`}
          />
        </div>

        <aside className="page-text-panel">
          <div className="page-text-head">
            <strong>文本定位</strong>
            <span>{describeMatchState(matchState)}</span>
          </div>

          {textLoading ? <p className="status-card">正在加载第 {page} 页文本...</p> : null}
          {!textLoading && textError ? <p className="error status-card">{textError}</p> : null}
          {!textLoading && !textError && matchState === "not_found" ? (
            <p className="warning status-card preview-state-note">
              未在当前页精确定位到该片段，仅展示本页清洗文本。
            </p>
          ) : null}
          {!textLoading && !textError ? (
            <div className="page-text-content" data-testid="pdf-page-text">
              {sentenceView ? (
                <p className="page-text-block">
                  <span className="page-text-sentence">
                    {sentenceView.focusBefore}
                    {sentenceView.focus ? (
                      <mark className="page-text-highlight">{sentenceView.focus}</mark>
                    ) : null}
                    {sentenceView.focusAfter}
                  </span>
                </p>
              ) : (
                <p className="page-text-block">当前页暂无可用文本。</p>
              )}
            </div>
          ) : null}
        </aside>
      </div>
    </section>
  );
}
