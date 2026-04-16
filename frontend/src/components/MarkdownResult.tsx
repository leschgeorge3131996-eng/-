import ReactMarkdown from "react-markdown";
import rehypeSanitize from "rehype-sanitize";

type MarkdownResultProps = {
  content: string;
};

export default function MarkdownResult({ content }: MarkdownResultProps) {
  return (
    <div className="rendered-markdown">
      <ReactMarkdown
        skipHtml
        rehypePlugins={[rehypeSanitize]}
        components={{
          a: ({ ...props }) => <a {...props} rel="noreferrer" target="_blank" />,
          code: ({ className, ...props }) => <code className={className} {...props} />
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
