import { forwardRef, type ReactNode } from "react";
import MessageBubble from "./MessageBubble";

type Message = { role: "user" | "assistant" | "system"; content: string };

type MessageListProps = {
  messages: Message[];
  agentName: string;
  error?: string | null;
  children?: ReactNode;
};

const MessageList = forwardRef<HTMLDivElement, MessageListProps>(function MessageList(
  { messages, agentName, error, children },
  ref,
) {
  return (
    <div
      ref={ref}
      className="chat-body"
      role="log"
      aria-live="polite"
      aria-label="Chat transcript"
    >
      {messages
        .filter((message) => message.role !== "system")
        .filter((message) => message.role !== "assistant" || message.content.trim().length > 0)
        .map((message, index) => (
          <MessageBubble
            key={`${message.role}-${index}`}
            role={message.role === "user" ? "user" : "assistant"}
            author={message.role === "assistant" ? agentName : undefined}
          >
            {message.content}
          </MessageBubble>
        ))}
      {error && (
        <div className="chat-error" role="alert">
          {error}
        </div>
      )}
      {children}
    </div>
  );
});

export default MessageList;
