"use client";

export default function DeveloperPage() {
  const apiKeys = [
    { name: "Production API Key", key: "sk_live_...a1b2", created: "12.03.2026" },
    { name: "Test API Key", key: "sk_test_...c3d4", created: "01.01.2026" },
  ];

  const webhooks = [
    { url: "https://api.example.com/webhook", events: "order.created, payment.completed", status: "Aktif" },
  ];

  return (
    <main className="max-w-4xl mx-auto px-4 py-8">
      <h1 className="text-2xl font-bold text-gray-900 mb-6">Geliştirici Portalı</h1>
      <section className="mb-8">
        <h2 className="text-lg font-semibold text-gray-900 mb-3">API Anahtarları</h2>
        <div className="space-y-3">
          {apiKeys.map((k) => (
            <div key={k.name} className="bg-white border border-gray-200 rounded-lg p-4 flex items-center justify-between">
              <div>
                <div className="font-medium text-gray-900 text-sm">{k.name}</div>
                <code className="text-xs text-gray-500 font-mono">{k.key}</code>
                <div className="text-xs text-gray-400 mt-1">Oluşturma: {k.created}</div>
              </div>
              <button className="text-xs text-red-600 hover:text-red-800">İptal Et</button>
            </div>
          ))}
          <button className="text-sm text-blue-600 font-medium hover:text-blue-800">+ Yeni Anahtar Oluştur</button>
        </div>
      </section>
      <section>
        <h2 className="text-lg font-semibold text-gray-900 mb-3">Webhooklar</h2>
        <div className="space-y-3">
          {webhooks.map((w, i) => (
            <div key={i} className="bg-white border border-gray-200 rounded-lg p-4">
              <div className="flex items-center justify-between mb-1">
                <code className="text-sm font-mono text-gray-700">{w.url}</code>
                <span className="text-xs text-green-700 bg-green-50 px-2 py-0.5 rounded">{w.status}</span>
              </div>
              <div className="text-xs text-gray-500">Olaylar: {w.events}</div>
            </div>
          ))}
          <button className="text-sm text-blue-600 font-medium hover:text-blue-800">+ Webhook Ekle</button>
        </div>
      </section>
    </main>
  );
}
