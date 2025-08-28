import ChatWidget from "./components/ChatWidget";

export default function App() {
  return (
    <main className="min-h-screen">
      <header className="px-6 py-4 bg-white border-b">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <h1 className="text-lg font-semibold">Sprint UI</h1>
          <a href="/admin" className="text-sm text-blue-600 hover:underline">Admin</a>
        </div>
      </header>
      <section className="max-w-6xl mx-auto p-6">
        <h2 className="text-xl font-medium mb-2">Website Demo</h2>
        <p className="text-gray-600">This page simulates your public site. Open the chat in the bottom-right to test.</p>
      </section>
      <ChatWidget />
    </main>
  );
}
