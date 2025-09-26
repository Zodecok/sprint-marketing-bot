import { useState, useEffect, useMemo, useRef } from "react";
import type { SVGProps } from "react";
import { useChat } from "../hooks/useChat";
import { logEvent } from "../lib/api";
import TypingIndicator from "./TypingIndicator";
import Composer from "./Composer";
import MessageList from "./MessageList";
import "./ChatWidget.css";

const AGENT_NAME = "Sprint AI Agent";

export default function ChatWidget() {
  const [open, setOpen] = useState(false);
  const [input, setInput] = useState("");
  const [placeholderActive, setPlaceholderActive] = useState(true);
  const { messages, send, isStreaming, error } = useChat([
    { role: "assistant", content: "Hi! How can I help?" },
  ]);

  const scrollRef = useRef<HTMLDivElement>(null);
  const textareaRef = useRef<HTMLTextAreaElement>(null);

  const showTyping = useMemo(() => {
    if (!isStreaming) return false;
    const latestAssistant = [...messages]
      .reverse()
      .find((m) => m.role === "assistant");
    return !latestAssistant || latestAssistant.content.trim().length === 0;
  }, [isStreaming, messages]);

  useEffect(() => {
    const el = scrollRef.current;
    if (!el) return;
    el.scrollTop = el.scrollHeight;
  }, [messages, showTyping]);

  useEffect(() => {
    const textarea = textareaRef.current;
    if (!textarea) return;
    textarea.style.height = "auto";
    textarea.style.height = `${Math.min(textarea.scrollHeight, 160)}px`;
  }, [input]);

  const handleOpen = () => {
    setOpen(true);
    logEvent("widget_open");
  };

  const handleClose = () => {
    setOpen(false);
    logEvent("widget_close");
  };

  const handleSubmit = () => {
    const trimmed = input.trim();
    if (!trimmed || isStreaming) return;
    setInput("");
    setPlaceholderActive(true);
    send(trimmed);
  };

  return (
    <>
      {!open && (
        <button
          onClick={handleOpen}
          className="chat-launcher"
          aria-label="Open chat"
        >
          <ChatBubbleIcon className="chat-launcher__icon" />
        </button>
      )}

      {open && (
        <section className="chat-widget" aria-label="Sprint chat widget">
          <div className="chat-panel">
            <header className="chat-panel__header">
              <div className="chat-panel__identity">
                <span className="chat-panel__avatar" aria-hidden="true">
                  {AGENT_NAME.charAt(0).toUpperCase()}
                </span>
                <div>
                  <p className="chat-panel__title">{AGENT_NAME}</p>
                  <p className="chat-panel__status">
                    <span className="chat-panel__status-dot" aria-hidden="true" />
                    Online
                  </p>
                </div>
              </div>
              <button
                type="button"
                className="chat-panel__close"
                onClick={handleClose}
                aria-label="Close chat"
              >
                <CloseIcon className="chat-panel__close-icon" />
              </button>
            </header>

            <MessageList
              ref={scrollRef}
              messages={messages}
              agentName={AGENT_NAME}
              error={error}
            >
              {showTyping && <TypingIndicator />}
            </MessageList>

            <Composer
              ref={textareaRef}
              value={input}
              onChange={(value) => {
                setInput(value);
                if (placeholderActive && value) setPlaceholderActive(false);
                if (!value) setPlaceholderActive(true);
              }}
              onSubmit={handleSubmit}
              placeholder={placeholderActive ? "Message..." : ""}
              disabled={isStreaming}
              ariaLabel="Message input"
              onFocus={() => {
                if (placeholderActive) setPlaceholderActive(false);
              }}
              onBlur={() => {
                if (!input) setPlaceholderActive(true);
              }}
            />
          </div>
        </section>
      )}
    </>
  );
}

function ChatBubbleIcon(props: SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="none" {...props}>
      <path
        fill="currentColor"
        d="M5.5 4h13a2.5 2.5 0 0 1 2.5 2.5v8a2.5 2.5 0 0 1-2.5 2.5H12l-3.6 3.2A1 1 0 0 1 7 19.4V17H5.5A2.5 2.5 0 0 1 3 14.5v-8A2.5 2.5 0 0 1 5.5 4Z"
      />
    </svg>
  );
}

function CloseIcon(props: SVGProps<SVGSVGElement>) {
  return (
    <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="1.8" {...props}>
      <path strokeLinecap="round" strokeLinejoin="round" d="M7 7l10 10M17 7l-10 10" />
    </svg>
  );
}
