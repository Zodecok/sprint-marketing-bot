import { useState } from "react";
import MessageBubble from "./MessageBubble";
import { useChat } from "../hooks/useChat";
import { logEvent } from "../lib/api";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const { messages, send, isStreaming, error } = useChat([
    { role: "assistant", content: "Hi! How can I help?" },
  ]);

  return (
    <>
      {/* Floating button */}
      {!open && (
        <button
          onClick={() => {
            setOpen(true);
            logEvent("widget_open");
          }}
          className="fixed bottom-4 right-4 rounded-full px-4 py-3 bg-blue-600 text-white shadow-xl"
        >
          Chat
        </button>
      )}

      {/* Panel */}
      {open && (
        <div className="fixed bottom-4 right-4 w-[360px] max-w-[95vw] h-[520px] bg-gray-50 border border-gray-200 rounded-2xl shadow-2xl flex flex-col">
          <div className="px-3 py-2 border-b flex items-center justify-between">
            <div className="font-medium">Sprint Assistant</div>
            <button
              onClick={() => setOpen(false)}
              className="text-sm text-gray-500 hover:text-gray-900"
            >
              Close
            </button>
          </div>
          <div className="flex-1 overflow-y-auto p-3">
            {messages.map((m, i) => (
              <MessageBubble
                key={i}
                role={m.role === "user" ? "user" : "assistant"}
              >
                {m.content}
              </MessageBubble>
            ))}
            {error && <div className="text-red-600 text-xs mt-2">{error}</div>}
          </div>
          <form
            className="p-2 border-t flex gap-2"
            onSubmit={(e) => {
              e.preventDefault();
              if (!input.trim() || isStreaming) return;
              const t = input.trim();
              setInput("");
              send(t);
            }}
          >
            <input
              className="flex-1 rounded-xl border border-gray-300 px-3 py-2 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              placeholder="Type your message…"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              disabled={isStreaming}
            />
            <button
              className="rounded-xl bg-blue-600 text-white px-3 py-2 text-sm disabled:opacity-50"
              disabled={isStreaming}
              type="submit"
            >
              Send
            </button>
          </form>
        </div>
      )}
    </>
  );
}
