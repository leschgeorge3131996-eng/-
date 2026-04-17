import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeSanitize from "rehype-sanitize";

type MarkdownResultProps = {
  content: string;
};

export default function MarkdownResult({ content }: MarkdownResultProps) {
  return (
    <div className="rendered-markdown">
      <ReactMarkdown
        skipHtml
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeSanitize]}
        components={{
          a: ({ ...props }) => <a {...props} rel="noreferrer" target="_blank" />,
          code: ({ className, ...props }) => <code className={className} {...props} />,
          table: ({ ...props }) => (
            <div className="markdown-table-wrap">
              <table {...props} />
            </div>
          )
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
