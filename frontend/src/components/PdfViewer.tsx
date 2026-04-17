import { useEffect, useRef } from "react";
import * as pdfjsLib from "pdfjs-dist";
import {
  EventBus,
  PDFFindController,
  PDFLinkService,
  PDFViewer
} from "pdfjs-dist/web/pdf_viewer.mjs";
// eslint-disable-next-line import/no-unresolved
import workerUrl from "pdfjs-dist/build/pdf.worker.min.mjs?url";
import "pdfjs-dist/web/pdf_viewer.css";

pdfjsLib.GlobalWorkerOptions.workerSrc = workerUrl;

type PdfViewerProps = {
  src: string;
  page: number;
  highlightText?: string | null;
  onError?: (message: string) => void;
};

type ViewerHandle = {
  eventBus: EventBus;
  viewer: PDFViewer;
  linkService: PDFLinkService;
  findController: PDFFindController;
  document: { destroy: () => Promise<void> } | null;
  disposed: boolean;
};

function buildFindQuery(snippet: string | null | undefined): string {
  if (!snippet) {
    return "";
  }
  const cleaned = snippet
    .replace(/\.\.\./g, " ")
    .replace(/\s+/g, " ")
    .trim();
  if (!cleaned) {
    return "";
  }
  // PDF.js find works best on a compact substring; longer queries often fail
  // because the text layer inserts whitespace across column breaks. Take the
  // longest CJK/punctuation-free run we can find, capped at 40 chars.
  const runs = cleaned.split(/[，。；：,.!?\n]/).map((part) => part.trim());
  const longest = runs.reduce((acc, part) => (part.length > acc.length ? part : acc), "");
  const candidate = longest || cleaned;
  return candidate.slice(0, 40);
}

export default function PdfViewer({ src, page, highlightText, onError }: PdfViewerProps) {
  const containerRef = useRef<HTMLDivElement | null>(null);
  const viewerRef = useRef<HTMLDivElement | null>(null);
  const handleRef = useRef<ViewerHandle | null>(null);

  useEffect(() => {
    const container = containerRef.current;
    const viewerEl = viewerRef.current;
    if (!container || !viewerEl) {
      return;
    }

    const eventBus = new EventBus();
    const linkService = new PDFLinkService({ eventBus });
    const findController = new PDFFindController({ eventBus, linkService });
    const viewer = new PDFViewer({
      container,
      viewer: viewerEl,
      eventBus,
      linkService,
      findController,
      textLayerMode: 2
    });
    linkService.setViewer(viewer);

    const handle: ViewerHandle = {
      eventBus,
      viewer,
      linkService,
      findController,
      document: null,
      disposed: false
    };
    handleRef.current = handle;

    const loadingTask = pdfjsLib.getDocument({ url: src, withCredentials: true });

    loadingTask.promise
      .then((pdfDocument) => {
        if (handle.disposed) {
          void pdfDocument.destroy();
          return;
        }
        handle.document = pdfDocument;
        viewer.setDocument(pdfDocument);
        linkService.setDocument(pdfDocument, null);
      })
      .catch((error: unknown) => {
        if (handle.disposed) {
          return;
        }
        const message = error instanceof Error ? error.message : "PDF 加载失败";
        onError?.(message);
      });

    return () => {
      handle.disposed = true;
      try {
        viewer.setDocument(null as unknown as Parameters<typeof viewer.setDocument>[0]);
      } catch {
        // ignore
      }
      if (handle.document) {
        void handle.document.destroy();
      }
      handleRef.current = null;
    };
  }, [src, onError]);

  // Jump to requested page when document is ready, and react to page prop changes.
  useEffect(() => {
    const handle = handleRef.current;
    if (!handle) {
      return;
    }
    const applyPage = () => {
      if (handle.disposed) {
        return;
      }
      if (page > 0) {
        handle.viewer.currentPageNumber = page;
      }
    };

    const initListener = () => {
      applyPage();
    };
    handle.eventBus.on("pagesinit", initListener);
    applyPage();
    return () => {
      handle.eventBus.off("pagesinit", initListener);
    };
  }, [page]);

  // Run find-controller search whenever the target snippet changes.
  useEffect(() => {
    const handle = handleRef.current;
    if (!handle) {
      return;
    }
    const query = buildFindQuery(highlightText);
    const dispatch = () => {
      if (handle.disposed) {
        return;
      }
      handle.eventBus.dispatch("find", {
        source: window,
        type: "",
        query,
        caseSensitive: false,
        entireWord: false,
        highlightAll: true,
        findPrevious: false,
        matchDiacritics: false
      });
    };

    if (!query) {
      dispatch();
      return;
    }

    // Defer until text layers for the target page are ready, otherwise the
    // find controller matches nothing and silently gives up.
    const onTextLayer = () => {
      dispatch();
    };
    handle.eventBus.on("textlayerrendered", onTextLayer);
    dispatch();
    return () => {
      handle.eventBus.off("textlayerrendered", onTextLayer);
    };
  }, [highlightText]);

  return (
    <div className="pdfjs-host" ref={containerRef}>
      <div className="pdfViewer" ref={viewerRef} />
    </div>
  );
}
