import { useState, useCallback } from "react";
import { streamChat, type ChatMessage, logEvent } from "../lib/api";

export function useChat(initial: ChatMessage[] = []) {
  const [messages, setMessages] = useState<ChatMessage[]>(initial);
  const [isStreaming, setIsStreaming] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const send = useCallback(async (text: string) => {
    const next = [
      ...messages,
      { role: "user", content: text } as ChatMessage,
      { role: "assistant", content: "" } as ChatMessage,
    ];
    setMessages(next);
    setError(null);
    setIsStreaming(true);
    logEvent("chat_send", { chars: text.length });

    try {
      let acc = "";
      for await (const chunk of streamChat(next.filter((m) => m.role !== "system"))) {
        acc += chunk;
        setMessages((prev) => {
          const copy = [...prev];
          copy[copy.length - 1] = { role: "assistant", content: acc } as ChatMessage;
          return copy;
        });
      }
      logEvent("chat_complete", { tokens: acc.length });
    } catch (e: any) {
      setError(e?.message || "Chat failed");
      logEvent("chat_error", { msg: e?.message });
    } finally {
      setIsStreaming(false);
    }
  }, [messages]);

  return { messages, send, isStreaming, error };
}

