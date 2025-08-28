import ChatWidget from "./components/ChatWidget";
import { useState } from "react";

export default function App() {
  const [health, setHealth] = useState<string>("");

  async function ping() {
    const base = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";
    const res = await fetch(`${base}/health`, { method: "GET" });
    setHealth(`${res.status} ${res.statusText}`);
  }

  return (
    <main className="min-h-screen">
      <header className="px-6 py-4 bg-white border-b">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <h1 className="text-lg font-semibold">Sprint UI</h1>
          <a href="/admin" className="text-sm text-blue-600 hover:underline">Admin</a>
        </div>
      </header>
      <section className="max-w-6xl mx-auto p-6 space-y-3">
        <button onClick={ping} className="px-3 py-2 rounded-lg bg-blue-600 text-white">Ping /health</button>
        {health && <div className="text-sm text-gray-700">Health response: {health}</div>}
        <p className="text-gray-600">Open DevTools → Network to inspect CORS headers.</p>
      </section>
      <ChatWidget />
    </main>
  );
}
