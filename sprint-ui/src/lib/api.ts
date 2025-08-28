const BASE = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export type ChatMessage = { role: "user" | "assistant" | "system"; content: string };

export async function* streamChat(messages: ChatMessage[]) {
  // Streaming via fetch + ReadableStream (server should stream text/plain or text/event-stream)
  const res = await fetch(`${BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ messages }),
  });
  if (!res.ok || !res.body) throw new Error(`Chat failed: ${res.status}`);

  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  let done = false;
  while (!done) {
    const { value, done: d } = await reader.read();
    done = d;
    if (value) yield decoder.decode(value, { stream: true });
  }
}

export async function listConversations(limit = 50) {
  const res = await fetch(`${BASE}/conversations?limit=${limit}`);
  if (!res.ok) throw new Error("Failed to load conversations");
  return res.json();
}

export function logEvent(name: string, payload: Record<string, unknown> = {}) {
  try {
    const url = `${BASE}/ui_event`;
    const data = JSON.stringify({ name, payload, ts: Date.now() });
    if ("sendBeacon" in navigator) navigator.sendBeacon(url, data);
    else fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: data });
  } catch {}
}

