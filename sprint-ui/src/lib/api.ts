import { runtimeApiBase } from "./runtimeApi";

const run = runtimeApiBase();
const BASE = run || import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

export type ChatMessage = { role: "user" | "assistant" | "system"; content: string };

export async function* streamChat(messages: ChatMessage[]) {
  // Backend expects { query: string }, not a messages array.
  // Find the latest user message to send as the query.
  const lastUser = [...messages]
    .reverse()
    .find((m) => m.role === "user")?.content?.trim();

  if (!lastUser) throw new Error("No user message to send");

  const res = await fetch(`${BASE}/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ query: lastUser }),
  });
  if (!res.ok) throw new Error(`Chat failed: ${res.status}`);

  // Current backend returns JSON: { answer, ... }
  const contentType = res.headers.get("content-type") || "";
  if (contentType.includes("application/json")) {
    const data = await res.json();
    const answer = typeof data?.answer === "string" ? data.answer : "";
    if (!answer) throw new Error("Invalid response from server");
    yield answer;
    return;
  }

  // Fallback: if server streams text, handle incremental chunks
  if (!res.body) throw new Error("No response body");
  const reader = res.body.getReader();
  const decoder = new TextDecoder();
  while (true) {
    const { value, done } = await reader.read();
    if (done) break;
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
    // Use sendBeacon with a JSON Blob so FastAPI parses it as JSON
    if ("sendBeacon" in navigator) {
      const blob = new Blob([data], { type: "application/json" });
      const queued = navigator.sendBeacon(url, blob);
      if (queued) return;
    }
    // Fallback to fetch if Beacon not available or queuing failed
    fetch(url, { method: "POST", headers: { "Content-Type": "application/json" }, body: data });
  } catch {}
}
