import { useEffect, useState } from "react";
import { listConversations } from "../lib/api";

export default function Admin() {
  const [rows, setRows] = useState<any[]>([]);
  const [err, setErr] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    (async () => {
      try {
        const data = await listConversations(50);
        setRows(data.items ?? data ?? []);
      } catch (e: any) {
        setErr(e?.message || "Failed to load");
      } finally {
        setLoading(false);
      }
    })();
  }, []);

  return (
    <main className="min-h-screen bg-gray-50">
      <header className="px-6 py-4 bg-white border-b">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <h1 className="text-lg font-semibold">Admin</h1>
          <a href="/" className="text-sm text-blue-600 hover:underline">Home</a>
        </div>
      </header>
      <section className="max-w-6xl mx-auto p-6">
        <h2 className="text-xl font-medium mb-4">Recent Conversations</h2>
        {loading && <div>Loading…</div>}
        {err && <div className="text-red-600">{err}</div>}
        {!loading && !err && (
          <div className="bg-white border rounded-xl overflow-hidden">
            <table className="w-full text-sm">
              <thead className="bg-gray-100 text-gray-600">
                <tr>
                  <th className="text-left px-3 py-2">Time</th>
                  <th className="text-left px-3 py-2">User Msg</th>
                  <th className="text-left px-3 py-2">Assistant Snippet</th>
                </tr>
              </thead>
              <tbody>
                {rows.map((r, i) => (
                  <tr key={i} className="border-t">
                    <td className="px-3 py-2">{new Date(r.ts ?? Date.now()).toLocaleString()}</td>
                    <td className="px-3 py-2">{r.user?.slice?.(0, 80) ?? ""}</td>
                    <td className="px-3 py-2">{r.assistant?.slice?.(0, 80) ?? ""}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </section>
    </main>
  );
}
