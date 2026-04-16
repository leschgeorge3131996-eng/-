type PdfPreviewPanelProps = {
  documentName: string;
  page: number;
  src: string;
  onClose: () => void;
};

export default function PdfPreviewPanel({
  documentName,
  page,
  src,
  onClose
}: PdfPreviewPanelProps) {
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
      <div className="pdf-frame-wrap">
        <iframe className="pdf-frame" src={src} title={`${documentName} PDF 预览`} />
      </div>
    </section>
  );
}
