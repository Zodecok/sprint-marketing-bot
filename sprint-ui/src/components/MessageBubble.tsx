import { type ReactNode } from "react";

type MessageBubbleProps = {
  role: "user" | "assistant";
  children: ReactNode;
  author?: string;
};

export default function MessageBubble({ role, children, author }: MessageBubbleProps) {
  const isUser = role === "user";
  return (
    <article className={`msg ${isUser ? "msg--user" : "msg--bot"}`}>
      {!isUser && author && <span className="msg__author">{author}</span>}
      <div className="msg__bubble">{children}</div>
    </article>
  );
}
