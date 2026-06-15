"use client";

export default function GiftRegistryPage() {
  const registries = [
    { type: "Düğün", couple: "Ali & Ayşe", date: "12 Eylül 2026", items: 24 },
    { type: "Bebek", couple: "Mehmet & Zeynep", date: "Ekim 2026", items: 18 },
    { type: "Düğün", couple: "Can & Elif", date: "5 Aralık 2026", items: 32 },
  ];

  return (
    <main className="max-w-5xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-6">
        <h1 className="text-2xl font-bold text-gray-900">Hediye Listeleri</h1>
        <button className="bg-blue-600 text-white rounded-lg px-4 py-2 text-sm font-medium hover:bg-blue-700 transition-colors">
          Yeni Liste Oluştur
        </button>
      </div>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
        {registries.map((r, i) => (
          <div key={i} className="bg-white border border-gray-200 rounded-lg p-5 hover:shadow-md transition-shadow">
            <span className="text-xs font-semibold text-pink-700 bg-pink-50 px-2 py-0.5 rounded">{r.type}</span>
            <h3 className="font-semibold text-gray-900 mt-2">{r.couple}</h3>
            <p className="text-sm text-gray-500">{r.date}</p>
            <p className="text-xs text-gray-400 mt-2">{r.items} ürün listelendi</p>
          </div>
        ))}
      </div>
    </main>
  );
}
